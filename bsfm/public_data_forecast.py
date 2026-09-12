"""Prospective BSFM-PD forecasts from public online evidence only."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import random

from .estimator import fit_shrunk_hazard, predict_cohort
from .integrity import digest, write_json_atomic
from .public_data_backtest import seasonal_naive_daily_path
from .temporal import (
    exposure_only_baseline,
    parameter_uncertainty,
    temporal_log_score,
    time_to_event_distribution,
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_public_spec(spec: dict) -> bool:
    required = {
        "model_id", "model_version", "non_retroactive", "target", "scope",
        "cohorts", "online_sources", "forecast_horizon_days", "forecast_cadence",
        "temporal_exposure_rule", "candidate_estimator", "baseline", "uncertainty",
        "validation_inheritance", "prospective_evaluation", "publication",
        "additional_data_value_test",
    }
    missing = sorted(required - set(spec))
    if missing:
        raise ValueError(f"incomplete public-data specification: {missing}")
    if spec["model_id"] != "BSFM-PD" or str(spec["model_version"]) != "1.4":
        raise ValueError("only registered BSFM-PD 1.4 is executable")
    if spec["candidate_estimator"] != "minimal_shrunk_hazard_v1":
        raise ValueError("unregistered public-data estimator")
    if spec["online_sources"].get("credentials_required") is not False:
        raise ValueError("public-online cycle cannot require credentials")
    if spec["online_sources"].get("commercial_data_required") is not False:
        raise ValueError("public-online cycle cannot require commercial data")
    if spec["forecast_cadence"].get("overlap_allowed") is not False:
        raise ValueError("prospective forecast horizons must not overlap")
    if spec["publication"].get("validated_claim_allowed") is not False:
        raise ValueError("BSFM-PD 1.4 cannot claim present validation")
    if spec["publication"].get("absolute_probability_claim_allowed") is not False:
        raise ValueError("BSFM-PD 1.4 cannot claim an absolute probability")
    if spec["publication"].get("append_only_forecasts") is not True:
        raise ValueError("BSFM-PD 1.4 forecasts must remain append-only")
    if spec["validation_inheritance"].get("may_be_rewritten") is not False:
        raise ValueError("BSFM-PD 1.3 result must remain immutable")
    evaluation = spec["prospective_evaluation"]
    if evaluation.get("paired_candidate_baseline") is not True:
        raise ValueError("prospective scoring must remain paired")
    if evaluation.get("superiority_rule") != "paired_bootstrap_improvement_lower_90_bound_above_zero":
        raise ValueError("prospective superiority rule changed without a new version")
    if int(evaluation.get("paired_bootstrap_samples", 0)) < 1000:
        raise ValueError("prospective paired bootstrap is underspecified")
    if int(evaluation.get("minimum_event_bearing_forecasts", 0)) != 10:
        raise ValueError("prospective minimum event-bearing rule changed")
    if evaluation.get("outcome_coverage_required_through_observed_event_or_horizon_end") is not True:
        raise ValueError("prospective scoring requires demonstrated outcome coverage")
    if evaluation.get("zero_rows_do_not_prove_no_event") is not True:
        raise ValueError("zero outcome rows cannot establish a censored horizon")
    if spec["additional_data_value_test"].get("prohibited_claim") != "Unavailable data would improve the forecast":
        raise ValueError("additional-data improvement cannot be assumed")
    return True


def validate_registered_public_spec(root: Path, spec: dict) -> bool:
    """Fail closed unless the executable contract matches its frozen registry hash."""
    registry_path = Path(root) / "config/public-data-model-registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    matches = [
        row for row in registry.get("models", [])
        if row.get("model_id") == spec.get("model_id")
        and str(row.get("model_version")) == str(spec.get("model_version"))
    ]
    if len(matches) != 1:
        raise ValueError("public-data model is not uniquely registered")
    entry = matches[0]
    if entry.get("spec_path") != "config/model-public-data-v1.4.json":
        raise ValueError("registered public-data specification path mismatch")
    if entry.get("spec_hash") != digest(spec):
        raise ValueError("public-data model contract changed without a new version")
    if registry.get("active_prospective_model") != "BSFM-PD 1.4":
        raise ValueError("BSFM-PD 1.4 is not the registered prospective model")
    return True


def _validate_frozen_record(record: dict) -> bool:
    if record.get("schema") != "bsfm.public-data-prospective-forecast.v1":
        raise ValueError("unrecognized public-data forecast record")
    if record.get("model_id") != "BSFM-PD" or str(record.get("model_version")) != "1.4":
        raise ValueError("forecast directory contains an incompatible model record")
    integrity = record.get("integrity")
    unsigned = {key: value for key, value in record.items() if key != "integrity"}
    if integrity != digest(unsigned):
        raise ValueError("immutable public-data forecast integrity failure")
    return True


def _load_public_outcomes(root: Path, cohorts: list[str]) -> tuple[dict, list[dict]]:
    """Load the append-only 1.4 ledger while protecting its frozen 1.3 seed."""
    root = Path(root)
    state = json.loads((root / "data/census/public-data-v1.4-outcomes.json").read_text(encoding="utf-8"))
    seed_path = state.get("historical_seed_path")
    if seed_path != "data/census/public-data-v1.3-outcomes.json":
        raise ValueError("unexpected public-data historical seed path")
    seed = json.loads((root / seed_path).read_text(encoding="utf-8"))
    if state.get("historical_seed_hash") != digest(seed):
        raise ValueError("public-data historical outcome seed integrity failure")
    events = state.get("events", [])
    seed_events = seed.get("events", [])
    if events[:len(seed_events)] != seed_events:
        raise ValueError("frozen historical outcome seed was rewritten")
    event_ids = [str(row.get("event_id", "")) for row in events]
    if not all(event_ids) or len(event_ids) != len(set(event_ids)):
        raise ValueError("public-data outcomes require unique non-empty ids")
    for index, row in enumerate(events):
        if row.get("pit_status") != "verified" or row.get("route_evidence_status") != "VERIFIED_AUTHORITY":
            raise ValueError("all public-data outcomes require verified authority and PIT evidence")
        if row.get("cohort") not in cohorts:
            raise ValueError("public-data outcome cohort is outside the frozen model")
        event_date = date.fromisoformat(str(row["event_date"])[:10])
        available_at = date.fromisoformat(str(row["available_at"])[:10])
        if available_at < event_date:
            raise ValueError("outcome cannot be public before it occurs")
        if index >= len(seed_events) and event_date < date(2026, 9, 7):
            raise ValueError("new BSFM-PD 1.4 outcome rows must be prospective")
    return state, events


def _eligible_training_exposure(rows: list[dict], cutoff: date, lag_days: int) -> list[dict]:
    eligible = []
    for row in rows:
        year = int(row["period"])
        if date(year, 12, 31) + timedelta(days=lag_days) <= cutoff:
            eligible.append(row)
    return eligible


def build_public_data_forecast(
    spec: dict,
    outcomes: list[dict],
    annual_exposure: list[dict],
    monthly_exposure: list[dict],
    issued_at: str,
    start_date: str | None = None,
) -> dict:
    """Build one immutable experimental forecast under the frozen 1.4 contract."""
    validate_public_spec(spec)
    issued = datetime.fromisoformat(issued_at.replace("Z", "+00:00"))
    if issued.tzinfo is None:
        raise ValueError("issued_at must be timezone-aware")
    cutoff = issued.astimezone(timezone.utc).date()
    earliest = date.fromisoformat(spec["forecast_cadence"]["first_eligible_start"])
    start = date.fromisoformat(start_date) if start_date else max(earliest, cutoff + timedelta(days=1))
    if start <= cutoff or start < earliest:
        raise ValueError("forecast must begin after issuance and first eligible start")

    cohorts = [str(value) for value in spec["cohorts"]]
    first_year = int(spec["exposure"]["training_start_year"])
    last_year = int(spec["exposure"]["training_end_year"])
    year_count = last_year - first_year + 1
    if year_count <= 0:
        raise ValueError("invalid public exposure training interval")
    expected_monthly = year_count * 12 * len(cohorts)
    expected_annual = year_count * len(cohorts)
    if len(monthly_exposure) != expected_monthly or len(annual_exposure) != expected_annual:
        raise ValueError("complete registered public exposure matrices required")
    annual_periods = {int(row["period"]) for row in annual_exposure}
    monthly_periods = {int(str(row["period"])[:4]) for row in monthly_exposure}
    expected_periods = set(range(first_year, last_year + 1))
    if annual_periods != expected_periods or monthly_periods != expected_periods:
        raise ValueError("public exposure interval does not match model contract")
    if any(row.get("scope") != spec["scope"] for row in annual_exposure + monthly_exposure):
        raise ValueError("exposure scope does not match model contract")
    if any(row.get("pit_status") != "verified" for row in outcomes):
        raise ValueError("all candidate outcomes require verified PIT status")

    lag = int(spec["temporal_exposure_rule"]["publication_lag_days"])
    training_events = [
        row for row in outcomes
        if date.fromisoformat(str(row["available_at"])[:10]) <= cutoff
    ]
    training_exposure = _eligible_training_exposure(annual_exposure, cutoff, lag)
    if not training_events or not training_exposure:
        raise ValueError("PIT-eligible public training data required")

    horizon = int(spec["forecast_horizon_days"])
    future = seasonal_naive_daily_path(
        monthly_exposure, cohorts, start.isoformat(), horizon, cutoff.isoformat(), lag,
    )
    model = fit_shrunk_hazard(training_events, training_exposure, cohorts)
    model["model_hash"] = digest(model)
    baseline = exposure_only_baseline(
        len(training_events),
        sum(float(row["departures"]) for row in training_exposure),
        cohorts,
    )
    baseline["model_hash"] = digest(baseline)
    candidate_distribution = time_to_event_distribution(model, future, start.isoformat(), horizon)
    baseline_distribution = time_to_event_distribution(baseline, future, start.isoformat(), horizon)
    uncertainty = parameter_uncertainty(
        model, future, start.isoformat(),
        spec["uncertainty"]["samples"], spec["uncertainty"]["seed"],
    )
    horizon_exposure = {
        cohort: sum(float(row["exposure_by_cohort"].get(cohort, 0.0)) for row in future)
        for cohort in cohorts
    }
    family_distribution = predict_cohort(model, horizon_exposure)
    source_periods = sorted({row["source_period"] for row in future})
    input_state = {
        "spec_hash": digest(spec),
        "outcomes_hash": digest(outcomes),
        "annual_exposure_hash": digest(annual_exposure),
        "monthly_exposure_hash": digest(monthly_exposure),
        "cutoff": cutoff.isoformat(),
        "start_date": start.isoformat(),
    }
    forecast_key = digest({
        "inputs": input_state,
        "model_hash": model["model_hash"],
        "candidate_distribution": candidate_distribution,
        "baseline_distribution": baseline_distribution,
    })
    record = {
        "schema": "bsfm.public-data-prospective-forecast.v1",
        "forecast_id": f"PD14-{start:%Y%m%d}-{forecast_key.split(':')[1][:12]}",
        "model_id": spec["model_id"],
        "model_version": spec["model_version"],
        "issued_at": issued.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "cutoff": cutoff.isoformat(),
        "status": "frozen_candidate_unvalidated",
        "claim_level": "experimental_unvalidated",
        "target": spec["target"],
        "scope": spec["scope"],
        "forecast_key": forecast_key,
        "input_state": input_state,
        "training": {
            "outcome_count": len(training_events),
            "outcome_ids": [row["event_id"] for row in training_events],
            "annual_exposure_cells": len(training_exposure),
            "latest_exposure_period": max(str(row["period"]) for row in training_exposure),
            "future_source_periods": source_periods,
        },
        "model": model,
        "baseline_model": baseline,
        "prediction": {
            "start_date": candidate_distribution["start_date"],
            "horizon_end": candidate_distribution["daily"][-1]["date"],
            "horizon_days": horizon,
            "modal_date": candidate_distribution["modal_date"],
            "conditional_interval_80": candidate_distribution["conditional_interval_80"],
            "family_distribution_conditional": family_distribution,
            "candidate_distribution": candidate_distribution,
            "baseline_distribution": baseline_distribution,
            "parameter_uncertainty": uncertainty,
        },
        "validation_reference": spec["validation_inheritance"],
        "additional_data_hypothesis": spec["additional_data_value_test"],
        "notice": (
            "Unvalidated prospective research forecast from public online data only. "
            "It is not an operational safety assessment, does not modify F-002, and "
            "does not establish predictive skill or an absolute accident probability."
        ),
    }
    record["integrity"] = digest(record)
    return record


def _public_view(record: dict, generated_new: bool, reason: str) -> dict:
    prediction = record["prediction"]
    return {
        "schema": "bsfm.public-data-forecast-state.v1",
        "generated_new": generated_new,
        "reason": reason,
        "forecast_id": record["forecast_id"],
        "model_id": record["model_id"],
        "model_version": record["model_version"],
        "issued_at": record["issued_at"],
        "cutoff": record["cutoff"],
        "status": record["status"],
        "claim_level": record["claim_level"],
        "validated_claim_allowed": False,
        "absolute_probability_claim_allowed": False,
        "target": record["target"],
        "scope": record["scope"],
        "prediction": {
            "start_date": prediction["start_date"],
            "horizon_end": prediction["horizon_end"],
            "horizon_days": prediction["horizon_days"],
            "modal_date": prediction["modal_date"],
            "conditional_interval_80": prediction["conditional_interval_80"],
            "family_distribution_conditional": prediction["family_distribution_conditional"],
        },
        "training": record["training"],
        "input_state": record["input_state"],
        "forecast_key": record["forecast_key"],
        "integrity": record["integrity"],
        "validation_reference": record["validation_reference"],
        "additional_data_hypothesis": record["additional_data_hypothesis"],
        "notice": record["notice"],
        "record_path": f"forecasts/public-data/{record['forecast_id']}.json",
    }


def execute_public_data_forecast(root: Path, issued_at: str | None = None) -> dict:
    """Issue one non-overlapping public-data forecast or retain the active one."""
    root = Path(root)
    issued_at = issued_at or _utcnow()
    issued = datetime.fromisoformat(issued_at.replace("Z", "+00:00"))
    if issued.tzinfo is None:
        raise ValueError("issued_at must be timezone-aware")
    cutoff = issued.astimezone(timezone.utc).date()
    spec = json.loads((root / "config/model-public-data-v1.4.json").read_text(encoding="utf-8"))
    validate_public_spec(spec)
    validate_registered_public_spec(root, spec)
    forecast_dir = root / "forecasts/public-data"
    existing = []
    for path in sorted(forecast_dir.glob("PD14-*.json")) if forecast_dir.exists() else []:
        record = json.loads(path.read_text(encoding="utf-8"))
        _validate_frozen_record(record)
        existing.append(record)
    latest = max(existing, key=lambda row: row["prediction"]["horizon_end"], default=None)
    if latest and date.fromisoformat(latest["prediction"]["horizon_end"]) >= cutoff + timedelta(days=1):
        public = _public_view(latest, False, "active_non_overlapping_forecast_exists")
        write_json_atomic(root / "site/data/public-data-forecast.json", public)
        return public

    _, outcomes = _load_public_outcomes(root, [str(value) for value in spec["cohorts"]])
    audit = json.loads((root / "data/exposure/bts-t100-2010-2025-audit.json").read_text(encoding="utf-8"))
    exposure = audit["prospective_merged_cohort_candidate"]
    if exposure.get("acceptance", {}).get("regional_matrix_complete") is not True:
        raise ValueError("public regional exposure matrix is incomplete")
    start = max(
        date.fromisoformat(spec["forecast_cadence"]["first_eligible_start"]),
        cutoff + timedelta(days=1),
        date.fromisoformat(latest["prediction"]["horizon_end"]) + timedelta(days=1) if latest else cutoff + timedelta(days=1),
    )
    record = build_public_data_forecast(
        spec, outcomes, exposure["exposure_rows"], exposure["monthly_exposure_rows"],
        issued_at, start.isoformat(),
    )
    destination = forecast_dir / f"{record['forecast_id']}.json"
    if destination.exists():
        prior = json.loads(destination.read_text(encoding="utf-8"))
        if prior.get("forecast_key") != record["forecast_key"]:
            raise RuntimeError("immutable public-data forecast id collision")
    else:
        write_json_atomic(destination, record)
    public = _public_view(record, True, "new_prospective_forecast_issued")
    write_json_atomic(root / "site/data/public-data-forecast.json", public)
    return public


def evaluate_public_data_forecasts(root: Path, evaluated_at: str | None = None) -> dict:
    """Score matured 1.4 forecasts only under explicit authority coverage."""
    root = Path(root)
    evaluated_at = evaluated_at or _utcnow()
    evaluated = datetime.fromisoformat(evaluated_at.replace("Z", "+00:00"))
    if evaluated.tzinfo is None:
        raise ValueError("evaluated_at must be timezone-aware")
    evaluation_cutoff = evaluated.astimezone(timezone.utc).date()
    spec = json.loads((root / "config/model-public-data-v1.4.json").read_text(encoding="utf-8"))
    validate_public_spec(spec)
    validate_registered_public_spec(root, spec)
    outcome_state, outcomes = _load_public_outcomes(root, [str(value) for value in spec["cohorts"]])
    monitoring = json.loads((root / "data/census/public-data-v1.4-monitoring.json").read_text(encoding="utf-8"))
    complete_through = monitoring.get("complete_through")
    coverage_date = date.fromisoformat(complete_through) if complete_through else None
    if coverage_date:
        evidence = monitoring.get("authority_evidence", [])
        if monitoring.get("status") != "VERIFIED_AUTHORITY_COVERAGE" or not evidence:
            raise ValueError("monitoring coverage date lacks authority evidence")
        if any(
            row.get("authority_status") != "official_or_competent"
            or row.get("coverage_scope") != "us_linked_commercial_target_v2"
            or not str(row.get("locator", "")).startswith("https://")
            or date.fromisoformat(row["coverage_through"]) < coverage_date
            for row in evidence
        ):
            raise ValueError("authority evidence does not cover the declared monitoring date")

    records = []
    forecast_dir = root / "forecasts/public-data"
    for path in sorted(forecast_dir.glob("PD14-*.json")) if forecast_dir.exists() else []:
        record = json.loads(path.read_text(encoding="utf-8"))
        _validate_frozen_record(record)
        records.append(record)
    scored, pending = [], []
    known_outcomes = [
        row for row in outcomes
        if date.fromisoformat(str(row["available_at"])[:10]) <= evaluation_cutoff
    ]
    for record in records:
        prediction = record["prediction"]
        start = date.fromisoformat(prediction["start_date"])
        end = date.fromisoformat(prediction["horizon_end"])
        possible = sorted(
            (
                row for row in known_outcomes
                if start <= date.fromisoformat(row["event_date"]) <= end
            ),
            key=lambda row: row["event_date"],
        )
        observed = possible[0] if possible else None
        required_coverage = date.fromisoformat(observed["event_date"]) if observed else end
        if coverage_date is None or coverage_date < required_coverage:
            pending.append({
                "forecast_id": record["forecast_id"],
                "reason": "outcome_coverage_not_verified_through_required_date",
                "required_coverage_through": required_coverage.isoformat(),
            })
            continue
        observed_date = observed["event_date"] if observed else None
        scored.append({
            "forecast_id": record["forecast_id"],
            "cutoff": record["cutoff"],
            "horizon_end": prediction["horizon_end"],
            "observed_event_id": observed["event_id"] if observed else None,
            "observed_date": observed_date,
            "candidate_log_score": temporal_log_score(prediction["candidate_distribution"], observed_date),
            "baseline_log_score": temporal_log_score(prediction["baseline_distribution"], observed_date),
        })

    candidate_mean = (
        sum(row["candidate_log_score"] for row in scored) / len(scored) if scored else None
    )
    baseline_mean = (
        sum(row["baseline_log_score"] for row in scored) / len(scored) if scored else None
    )
    candidate_better = (
        candidate_mean < baseline_mean if candidate_mean is not None and baseline_mean is not None else None
    )
    paired_uncertainty = None
    if scored:
        differences = [row["baseline_log_score"] - row["candidate_log_score"] for row in scored]
        samples = int(spec["prospective_evaluation"]["paired_bootstrap_samples"])
        rng = random.Random(int(spec["prospective_evaluation"]["paired_bootstrap_seed"]))
        bootstrap_means = [
            sum(rng.choice(differences) for _ in differences) / len(differences)
            for _ in range(samples)
        ]
        ordered = sorted(bootstrap_means)
        paired_uncertainty = {
            "method": "deterministic_paired_nonparametric_bootstrap",
            "samples": samples,
            "seed": int(spec["prospective_evaluation"]["paired_bootstrap_seed"]),
            "improvement_lower_90": ordered[int(0.05 * (samples - 1))],
            "improvement_upper_90": ordered[int(0.95 * (samples - 1))],
        }
    event_count = sum(row["observed_event_id"] is not None for row in scored)
    minimum = int(spec["prospective_evaluation"]["minimum_event_bearing_forecasts"])
    passed = (
        len(scored) > 0
        and event_count >= minimum
        and candidate_better is True
        and paired_uncertainty["improvement_lower_90"] > 0
    )
    if not records:
        reason = "no_frozen_forecasts"
    elif not scored:
        reason = "no_forecast_has_verified_outcome_coverage"
    elif event_count < minimum:
        reason = "insufficient_event_bearing_forecasts"
    elif candidate_better is not True:
        reason = "candidate_does_not_beat_baseline"
    elif paired_uncertainty["improvement_lower_90"] <= 0:
        reason = "candidate_superiority_not_supported_by_paired_uncertainty"
    else:
        reason = "preregistered_prospective_rule_passed"
    report = {
        "schema": "bsfm.public-data-prospective-evaluation.v1",
        "generated_at": evaluated.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": "PROSPECTIVE_EVALUATION_COMPLETE" if scored else "NO_SCORABLE_PROSPECTIVE_FORECASTS",
        "scientific_validation": "PASS" if passed else "BLOCKED",
        "reason": reason,
        "claim_level": "experimental_unvalidated" if not passed else "prospective_test_passed_pending_explicit_promotion",
        "forecast_count": len(records),
        "scored_forecasts": len(scored),
        "event_bearing_forecasts": event_count,
        "minimum_event_bearing_forecasts": minimum,
        "candidate_mean_log_score": candidate_mean,
        "baseline_mean_log_score": baseline_mean,
        "mean_log_score_improvement": (
            baseline_mean - candidate_mean if candidate_mean is not None and baseline_mean is not None else None
        ),
        "candidate_better": candidate_better,
        "paired_uncertainty": paired_uncertainty,
        "coverage_complete_through": complete_through,
        "outcomes_hash": digest(outcome_state),
        "monitoring_hash": digest(monitoring),
        "scored": scored,
        "pending": pending,
        "claim_limit": "No-event scoring requires positive authority coverage; absence of discovered rows is never treated as complete coverage.",
    }
    write_json_atomic(root / "evaluations/public-data-v1.4-prospective.json", report)
    write_json_atomic(root / "site/data/public-data-prospective-evaluation.json", report)
    return report

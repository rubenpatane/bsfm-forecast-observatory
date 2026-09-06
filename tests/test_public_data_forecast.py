import json
from pathlib import Path
import shutil

import pytest

from bsfm.integrity import digest
from bsfm.public_data_forecast import (
    _public_view,
    build_public_data_forecast,
    evaluate_public_data_forecasts,
    execute_public_data_forecast,
    validate_public_spec,
    validate_registered_public_spec,
)


ROOT = Path(__file__).resolve().parents[1]


def _inputs(root=ROOT):
    spec = json.loads((root / "config/model-public-data-v1.4.json").read_text())
    outcomes = json.loads((root / "data/census/public-data-v1.4-outcomes.json").read_text())["events"]
    exposure = json.loads((root / "data/exposure/bts-t100-2010-2025-audit.json").read_text())[
        "prospective_merged_cohort_candidate"
    ]
    return spec, outcomes, exposure


def _repository_fixture(tmp_path):
    for relative in (
        "config/model-public-data-v1.4.json",
        "config/public-data-model-registry.json",
        "data/census/public-data-v1.3-outcomes.json",
        "data/census/public-data-v1.4-outcomes.json",
        "data/census/public-data-v1.4-monitoring.json",
        "data/exposure/bts-t100-2010-2025-audit.json",
    ):
        source = ROOT / relative
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    return tmp_path


def test_registered_contract_hashes_are_frozen():
    registry = json.loads((ROOT / "config/public-data-model-registry.json").read_text())
    for entry in registry["models"]:
        spec = json.loads((ROOT / entry["spec_path"]).read_text())
        assert entry["spec_hash"] == digest(spec)
    spec, _, _ = _inputs()
    assert validate_registered_public_spec(ROOT, spec)


def test_builds_reproducible_public_online_temporal_forecast():
    spec, outcomes, exposure = _inputs()
    record = build_public_data_forecast(
        spec,
        outcomes,
        exposure["exposure_rows"],
        exposure["monthly_exposure_rows"],
        "2026-09-06T15:00:00Z",
    )
    assert record["model_version"] == "1.4"
    assert record["status"] == "frozen_candidate_unvalidated"
    assert record["prediction"]["start_date"] == "2026-09-07"
    assert record["prediction"]["horizon_end"] == "2026-12-05"
    assert record["prediction"]["horizon_days"] == 90
    assert record["prediction"]["modal_date"] == "2026-09-07"
    assert record["prediction"]["conditional_interval_80"] == {
        "lower": "2026-09-15",
        "upper": "2026-11-26",
        "coverage": 0.8,
        "conditional_on_event_within_horizon": True,
    }
    assert record["training"]["outcome_count"] == 3
    assert record["training"]["annual_exposure_cells"] == 135
    assert record["training"]["latest_exposure_period"] == "2024"
    assert record["training"]["future_source_periods"] == [
        "2024-09", "2024-10", "2024-11", "2024-12"
    ]
    distribution = record["prediction"]["candidate_distribution"]
    assert sum(row["probability"] for row in distribution["daily"]) == pytest.approx(
        distribution["event_probability"]
    )
    assert distribution["event_probability"] + distribution["no_event_probability"] == pytest.approx(1.0)
    assert sum(record["prediction"]["family_distribution_conditional"].values()) == pytest.approx(1.0)
    assert record["integrity"] == digest({key: value for key, value in record.items() if key != "integrity"})


def test_public_view_withholds_absolute_probability_claims():
    spec, outcomes, exposure = _inputs()
    record = build_public_data_forecast(
        spec, outcomes, exposure["exposure_rows"], exposure["monthly_exposure_rows"],
        "2026-09-06T15:00:00Z",
    )
    public = _public_view(record, True, "test")
    assert "candidate_distribution" not in public["prediction"]
    assert "baseline_distribution" not in public["prediction"]
    assert "event_probability" not in public["prediction"]
    assert public["claim_level"] == "experimental_unvalidated"
    assert public["validation_reference"]["result"].startswith("BLOCKED_")


def test_contract_rejects_silent_scientific_changes():
    spec, _, _ = _inputs()
    cases = []
    changed = json.loads(json.dumps(spec)); changed["candidate_estimator"] = "post_hoc_model"; cases.append(changed)
    changed = json.loads(json.dumps(spec)); changed["online_sources"]["credentials_required"] = True; cases.append(changed)
    changed = json.loads(json.dumps(spec)); changed["online_sources"]["commercial_data_required"] = True; cases.append(changed)
    changed = json.loads(json.dumps(spec)); changed["forecast_cadence"]["overlap_allowed"] = True; cases.append(changed)
    changed = json.loads(json.dumps(spec)); changed["publication"]["validated_claim_allowed"] = True; cases.append(changed)
    changed = json.loads(json.dumps(spec)); changed["validation_inheritance"]["may_be_rewritten"] = True; cases.append(changed)
    changed = json.loads(json.dumps(spec)); changed["prospective_evaluation"]["paired_candidate_baseline"] = False; cases.append(changed)
    changed = json.loads(json.dumps(spec)); changed["prospective_evaluation"]["zero_rows_do_not_prove_no_event"] = False; cases.append(changed)
    changed = json.loads(json.dumps(spec)); changed["additional_data_value_test"]["prohibited_claim"] = ""; cases.append(changed)
    for changed in cases:
        with pytest.raises(ValueError):
            validate_public_spec(changed)


def test_execution_is_append_only_deduplicated_and_non_overlapping(tmp_path):
    root = _repository_fixture(tmp_path)
    first = execute_public_data_forecast(root, "2026-09-06T15:00:00Z")
    retained = execute_public_data_forecast(root, "2026-09-07T15:00:00Z")
    assert first["generated_new"] is True
    assert retained["generated_new"] is False
    assert retained["forecast_id"] == first["forecast_id"]
    assert len(list((root / "forecasts/public-data").glob("PD14-*.json"))) == 1

    second = execute_public_data_forecast(root, "2026-12-05T15:00:00Z")
    assert second["generated_new"] is True
    assert second["prediction"]["start_date"] == "2026-12-06"
    assert second["prediction"]["start_date"] > first["prediction"]["horizon_end"]
    assert len(list((root / "forecasts/public-data").glob("PD14-*.json"))) == 2


def test_execution_refuses_mutated_immutable_record(tmp_path):
    root = _repository_fixture(tmp_path)
    public = execute_public_data_forecast(root, "2026-09-06T15:00:00Z")
    path = root / public["record_path"]
    record = json.loads(path.read_text())
    record["cutoff"] = "2026-09-05"
    path.write_text(json.dumps(record))
    with pytest.raises(ValueError, match="integrity"):
        execute_public_data_forecast(root, "2026-09-07T15:00:00Z")


def test_prospective_evaluation_requires_positive_authority_coverage(tmp_path):
    root = _repository_fixture(tmp_path)
    execute_public_data_forecast(root, "2026-09-06T15:00:00Z")
    blocked = evaluate_public_data_forecasts(root, "2026-12-06T15:00:00Z")
    assert blocked["forecast_count"] == 1
    assert blocked["scored_forecasts"] == 0
    assert blocked["reason"] == "no_forecast_has_verified_outcome_coverage"
    assert blocked["scientific_validation"] == "BLOCKED"
    assert blocked["pending"][0]["required_coverage_through"] == "2026-12-05"

    monitoring_path = root / "data/census/public-data-v1.4-monitoring.json"
    monitoring = json.loads(monitoring_path.read_text())
    monitoring.update({
        "status": "VERIFIED_AUTHORITY_COVERAGE",
        "complete_through": "2026-12-05",
        "authority_evidence": [{
            "authority_status": "official_or_competent",
            "coverage_scope": "us_linked_commercial_target_v2",
            "coverage_through": "2026-12-05",
            "locator": "https://authority.example/public-record",
        }],
    })
    monitoring_path.write_text(json.dumps(monitoring))
    scored = evaluate_public_data_forecasts(root, "2026-12-06T15:00:00Z")
    assert scored["scored_forecasts"] == 1
    assert scored["event_bearing_forecasts"] == 0
    assert scored["scored"][0]["observed_event_id"] is None
    assert scored["paired_uncertainty"]["samples"] == 5000
    assert scored["paired_uncertainty"]["seed"] == 1402
    assert scored["reason"] == "insufficient_event_bearing_forecasts"
    assert scored["scientific_validation"] == "BLOCKED"


def test_execution_refuses_rewriting_the_historical_outcome_seed(tmp_path):
    root = _repository_fixture(tmp_path)
    path = root / "data/census/public-data-v1.4-outcomes.json"
    state = json.loads(path.read_text())
    state["events"][0]["cohort"] = "737-MAX"
    path.write_text(json.dumps(state))
    with pytest.raises(ValueError, match="seed was rewritten"):
        execute_public_data_forecast(root, "2026-09-06T15:00:00Z")

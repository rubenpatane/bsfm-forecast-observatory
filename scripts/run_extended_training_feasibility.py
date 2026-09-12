#!/usr/bin/env python3
"""Run a non-promotable BSFM-PD 1990-2025 training feasibility scenario.

Administrative NTSB approval dates may be inspected as an explicitly invalid
optimistic scenario. The default uses only a conservative public snapshot bound.
Neither mode can validate or promote a model because target/route adjudication
is incomplete and the exercise was not prospectively preregistered.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import random
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bsfm.public_data_backtest import run_exploratory_backtest


INTERNATIONAL_US_LINKED = {
    "CHI92LA250",   # route fields in NTSB record include ORD/ANC
    "DCA96RA020",   # American 965, Miami-Cali
    "DCA96MA070",   # TWA 800, New York-Paris
    "MIA97WA226",   # Lima-Newark
    "DCA97MA058",   # Korean 801, Seoul-Guam
    "DCA98MA015",   # United 826, Tokyo-Honolulu
    "DCA00MA006",   # EgyptAir 990, New York-Cairo
    "DEN01FA157",   # British Airways ground fatality at Denver
    "DCA08RA078",   # Centurion 164, Bogota-Miami
}

UNLAWFUL_INTERFERENCE = {
    "DCA01MA060", "DCA01MA063", "DCA01MA064", "DCA01MA065",
}


def cohort_for_model(model: str) -> str | None:
    value = re.sub(r"\s+", "", str(model or "").upper())
    if "727" in value:
        return "727"
    if "737" in value:
        if "MAX" in value:
            return "737-MAX"
        if any(token in value for token in ("737-100", "737-200", "737-2", "B737-2", "-737-2")):
            return "737-Original"
        return "737-Classic+NG"
    if "747" in value:
        return "747"
    if "757" in value:
        return "757"
    if "767" in value:
        return "767"
    if "777" in value:
        return "777"
    if "787" in value:
        return "787"
    return None


def select_scenario_outcomes(discovery_payloads, availability_mode="administrative_approval"):
    rows = []
    seen = set()
    for payload in discovery_payloads:
        late_bound = payload.get("source", {}).get("snapshot_bound")
        if availability_mode == "late_snapshot" and not late_bound:
            raise ValueError("late_snapshot mode requires a source snapshot_bound")
        for source in payload["candidates"]:
            number = str(source.get("ntsb_number") or "").strip()
            if not number or number in seen or number in UNLAWFUL_INTERFERENCE:
                continue
            cohort = cohort_for_model(source.get("model"))
            domestic_part_121 = (
                source.get("event_type") == "ACC"
                and str(source.get("far_part") or "").strip() == "121"
                and str(source.get("domestic_international") or "").strip() == "DOM"
            )
            international_us_linked = number in INTERNATIONAL_US_LINKED
            if not cohort or not (domestic_part_121 or international_us_linked):
                continue
            approval = source.get("administrative_approval_date")
            if not approval:
                continue
            available_at = approval if availability_mode == "administrative_approval" else late_bound
            seen.add(number)
            rows.append({
                "event_id": f"NTSB-{number}",
                "event_date": source["event_date"],
                "available_at": available_at,
                "cohort": cohort,
                "route_evidence_status": "SCENARIO_ONLY",
                "pit_status": (
                    "not_verified_administrative_approval_proxy"
                    if availability_mode == "administrative_approval"
                    else "verified_late_public_snapshot_bound"
                ),
            })
    return sorted(rows, key=lambda row: row["event_date"])


def paired_bootstrap(folds, samples=5000, seed=1402):
    differences = [row["baseline_log_score"] - row["candidate_log_score"] for row in folds]
    if not differences:
        raise ValueError("at least one paired fold is required")
    rng = random.Random(seed)
    means = sorted(
        sum(rng.choice(differences) for _ in differences) / len(differences)
        for _ in range(samples)
    )
    return {
        "method": "deterministic_paired_nonparametric_bootstrap",
        "samples": samples,
        "seed": seed,
        "improvement_lower_90": means[int(0.05 * (samples - 1))],
        "improvement_upper_90": means[int(0.95 * (samples - 1))],
    }


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-discovery", type=Path, required=True)
    parser.add_argument("--modern-discovery", type=Path, required=True)
    parser.add_argument("--exposure-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--availability-mode",
        choices=("administrative_approval", "late_snapshot"),
        default="late_snapshot",
    )
    args = parser.parse_args()

    discoveries = [
        json.loads(args.legacy_discovery.read_text(encoding="utf-8")),
        json.loads(args.modern_discovery.read_text(encoding="utf-8")),
    ]
    events = select_scenario_outcomes(discoveries, args.availability_mode)
    # Preserve the already authority/PIT-reviewed 2010-2025 outcomes rather
    # than substituting modern NTSB administrative dates for them.
    reviewed = json.loads(
        (ROOT / "data/census/public-data-v1.3-outcomes.json").read_text(encoding="utf-8")
    )["events"]
    events = [row for row in events if row["event_date"] < "2010-01-01"] + reviewed

    spec = deepcopy(json.loads((ROOT / "config/model-public-data-v1.3.json").read_text(encoding="utf-8")))
    spec["validation_protocol"]["first_fold_start"] = "1992-01-01"
    exposure = json.loads(args.exposure_audit.read_text(encoding="utf-8"))[
        "prospective_merged_cohort_candidate"
    ]
    frozen_report = run_exploratory_backtest(
        events,
        exposure["exposure_rows"],
        exposure["monthly_exposure_rows"],
        spec["cohorts"],
        spec,
    )
    frozen_report["paired_uncertainty"] = paired_bootstrap(frozen_report["folds"])
    cohort_count = len(spec["cohorts"])
    matched_report = run_exploratory_backtest(
        events,
        exposure["exposure_rows"],
        exposure["monthly_exposure_rows"],
        spec["cohorts"],
        spec,
        candidate_alpha=0.5 / cohort_count,
        candidate_prior_departures=1_000_000.0 / cohort_count,
    )
    matched_report["paired_uncertainty"] = paired_bootstrap(matched_report["folds"])
    hard_limit = (
        "NTSB administrative approval dates are not public-availability evidence; "
        "this result cannot validate or promote a model."
        if args.availability_mode == "administrative_approval"
        else "Conservative exact-byte public snapshot bounds provide no historical training signal before those bounds; route and target census adjudication remains incomplete."
    )
    payload = {
        "schema": "bsfm.extended-training-feasibility.v1",
        "status": "DO_NOT_PROMOTE",
        "purpose": "Reject-or-continue feasibility check before any separately preregistered model extension.",
        "hard_limit": hard_limit,
        "availability_mode": args.availability_mode,
        "inputs": {
            "legacy_discovery_sha256": _sha256(args.legacy_discovery),
            "modern_discovery_sha256": _sha256(args.modern_discovery),
            "exposure_audit_sha256": _sha256(args.exposure_audit),
        },
        "outcome_count": len(events),
        "scenario_outcomes": events,
        "frozen_prior_backtest": frozen_report,
        "prior_mass_diagnostic": {
            "candidate_total_pseudo_events": 0.5 * cohort_count,
            "candidate_total_pseudo_departures": 1_000_000.0 * cohort_count,
            "baseline_total_pseudo_events": 0.5,
            "baseline_total_pseudo_departures": 1_000_000.0,
            "interpretation": "The frozen candidate starts with nine times the baseline total prior mass; apparent superiority can therefore be prior-driven rather than learned from outcomes.",
        },
        "matched_total_prior_sensitivity": matched_report,
        "decision": {
            "promote_or_replace_active_1_4": False,
            "reason": "The candidate advantage reverses under equal total prior mass, while historical route/census evidence is incomplete. A prior change would require a separately preregistered model version and new prospective evidence.",
        },
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

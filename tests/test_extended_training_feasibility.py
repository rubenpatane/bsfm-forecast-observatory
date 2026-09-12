import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.discover_legacy_ntsb_candidates import discover
from scripts.run_extended_training_feasibility import (
    cohort_for_model,
    paired_bootstrap,
    select_scenario_outcomes,
)


def _columns(rows):
    return {key: [row.get(key) for row in rows] for key in rows[0]}


def test_legacy_discovery_is_broad_but_privacy_minimal():
    events = _columns([{
        "ev_id": "E1", "ev_year": 1994, "ev_date": "1994-09-08",
        "inj_tot_f": 2, "inj_f_grnd": 0, "ev_type": "ACC", "ntsb_no": "N1",
    }])
    aircraft = _columns([{
        "ev_id": "E1", "Aircraft_Key": 1, "ntsb_no": "N1", "acft_make": "Boeing",
        "acft_model": "737-300", "acft_series": None, "regis_no": "NTEST",
        "far_part": "121", "oprtng_cert": None, "oper_cert": None,
        "oper_sched": "SCHD", "oper_dom_int": "DOM", "oper_pax_cargo": "PAX",
        "dprt_apt_id": "ORD", "dprt_city": "Chicago", "dprt_state": "IL",
        "dprt_country": "USA", "dest_apt_id": "PIT", "dest_city": "Pittsburgh",
        "dest_state": "PA", "dest_country": "USA", "owner_street": "must not leak",
    }])
    administration = _columns([{"ev_id": "E1", "approval_date": "1999-11-15"}])
    rows = discover(events, aircraft, administration, 1990, 2007)
    assert len(rows) == 1
    assert rows[0]["administrative_approval_date"] == "1999-11-15"
    assert "owner_street" not in rows[0]


def test_extended_scenario_keeps_admin_date_non_pit_and_late_snapshot_conservative():
    payload = {
        "interval": {"start_year": 1990, "end_year": 2007},
        "source": {"snapshot_bound": "2026-09-06"},
        "candidates": [{
            "ntsb_number": "DCA94MA076", "model": "737-300", "event_type": "ACC",
            "far_part": "121", "domestic_international": "DOM",
            "administrative_approval_date": "1999-11-15", "event_date": "1994-09-08",
        }],
    }
    optimistic = select_scenario_outcomes([payload], "administrative_approval")
    assert optimistic[0]["pit_status"] == "not_verified_administrative_approval_proxy"
    conservative = select_scenario_outcomes([payload], "late_snapshot")
    assert conservative[0]["available_at"] == "2026-09-06"
    assert conservative[0]["pit_status"] == "verified_late_public_snapshot_bound"


def test_model_mapping_and_paired_bootstrap_are_deterministic():
    assert cohort_for_model("B-737-200") == "737-Original"
    assert cohort_for_model("737-700") == "737-Classic+NG"
    assert cohort_for_model("737 MAX 8") == "737-MAX"
    folds = [
        {"baseline_log_score": 2.0, "candidate_log_score": 1.0},
        {"baseline_log_score": 1.0, "candidate_log_score": 2.0},
    ]
    assert paired_bootstrap(folds, samples=1000, seed=7) == paired_bootstrap(
        folds, samples=1000, seed=7,
    )


def test_checked_in_extended_training_result_is_fail_closed():
    report = json.loads(
        (ROOT / "evaluations/public-data-extended-training-feasibility.json").read_text()
    )
    frozen = report["frozen_prior_backtest"]
    matched = report["matched_total_prior_sensitivity"]
    assert report["status"] == "DO_NOT_PROMOTE"
    assert report["decision"]["promote_or_replace_active_1_4"] is False
    assert report["outcome_count"] == 23
    assert frozen["fold_count"] == 137
    assert frozen["event_bearing_fold_count"] == 15
    assert frozen["mean_log_score_improvement"] > 0
    assert matched["mean_log_score_improvement"] < 0
    assert matched["paired_uncertainty"]["improvement_lower_90"] < 0
    assert matched["paired_uncertainty"]["improvement_upper_90"] > 0
    diagnostic = report["prior_mass_diagnostic"]
    assert diagnostic["candidate_total_pseudo_events"] == 9 * diagnostic["baseline_total_pseudo_events"]
    assert diagnostic["candidate_total_pseudo_departures"] == 9 * diagnostic["baseline_total_pseudo_departures"]

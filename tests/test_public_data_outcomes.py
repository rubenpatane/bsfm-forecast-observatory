import json
from pathlib import Path

from bsfm.public_data_outcomes import audit_route_ledger, load_candidate_ids

ROOT = Path(__file__).resolve().parents[1]


def test_checked_in_ledger_is_fail_closed_and_identifies_only_verified_us_routes():
    candidates = load_candidate_ids(ROOT / "data/census")
    ledger = json.loads((ROOT / "data/census/public-data-v1.3-route-ledger.json").read_text())
    result = audit_route_ledger(ledger, candidates)
    assert len(candidates) == 38
    assert result["status"] == "READY"
    assert result["errors"] == []
    assert result["verified_included"] == ["G1-2013-AAR214", "G1-2018-SWA1380", "G1-2019-ATLAS3591"]
    assert len(result["verified_excluded"]) == 35
    assert result["missing_candidate_ids"] == []


def test_final_decision_requires_authority_verified_route():
    ledger = {"records": [{"event_id": "X", "route_status": "PENDING_ROUTE", "geographic_decision": "INCLUDE_US_ENDPOINT"}]}
    result = audit_route_ledger(ledger, {"X"})
    assert "unverified route has final decision: X" in result["errors"]


def test_endpoint_boolean_controls_geographic_decision():
    row = {"event_id": "X", "route_status": "VERIFIED_AUTHORITY", "geographic_decision": "EXCLUDE_NO_US_ENDPOINT",
           "origin": {"us_endpoint": True}, "destination": {"us_endpoint": False},
           "evidence": {"publisher": "p", "record": "r", "locator": "https://example.test", "observation": "o"}}
    result = audit_route_ledger({"records": [row]}, {"X"})
    assert "endpoint/decision mismatch: X" in result["errors"]


def test_public_data_outcomes_are_route_and_pit_verified():
    outcomes = json.loads((ROOT / "data/census/public-data-v1.3-outcomes.json").read_text())
    assert len(outcomes["events"]) == 3
    assert {row["cohort"] for row in outcomes["events"]} == {"777", "737-Classic+NG", "767"}
    assert all(row["route_evidence_status"] == "VERIFIED_AUTHORITY" for row in outcomes["events"])
    assert all(row["pit_status"] == "verified" and row["available_at"] > row["event_date"] for row in outcomes["events"])


def test_model_contract_keeps_validation_blocked_after_foundation_passes():
    model = json.loads((ROOT / "config/model-public-data-v1.3.json").read_text())
    gate = model["evidence_gate_checkpoint"]
    assert gate["route_census"] == "PASS_38_OF_38"
    assert gate["qualifying_outcome_pit"] == "PASS_3_OF_3"
    assert gate["regional_exposure_matrix"] == "PASS_144_OF_144"
    assert gate["regional_monthly_exposure_matrix"] == "PASS_1728_OF_1728"
    assert gate["predictive_validation"] == "BLOCKED"
    assert any("model 1.2" in blocker for blocker in model["validation_blockers"])

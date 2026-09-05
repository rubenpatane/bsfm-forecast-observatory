from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
from .integrity import digest, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]


def utcnow():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')


def candidate_gate(source_state: dict, backtest_report: dict | None = None) -> dict:
    """Decide whether an estimator candidate may be fitted/promoted.

    This gate deliberately separates data refresh from model learning. A successful
    source download is never sufficient: historical point-in-time availability,
    leakage-free evaluation, a baseline, historical cases and calibration are all
    required before promotion can be considered.
    """
    backtest_report = backtest_report or {}
    checks = {
        'source_integrity_ready': bool(source_state.get('source_integrity_ready')),
        'point_in_time_availability_verified': bool(source_state.get('point_in_time_availability_verified')),
        'leakage_free': bool(backtest_report.get('leakage_free')),
        'baseline_present': bool(backtest_report.get('baseline_present')),
        'historical_cases': bool(backtest_report.get('historical_cases')),
        'calibration_evaluated': bool(backtest_report.get('calibration_evaluated')),
    }
    missing = [name for name, ok in checks.items() if not ok]
    return {'pass': not missing, 'checks': checks, 'missing': missing}


def update_model(source_state: dict, backtest_report: dict | None = None, out_path=None) -> dict:
    """Fail-closed model lifecycle entry point used by AGGIORNA.

    No estimator is fitted yet: until the preregistered scientific gates pass, the
    only valid action is to retain the incumbent model and record why learning was
    blocked. This makes the future training/update stage auditable without silently
    learning from leakage-prone current snapshots.
    """
    gate = candidate_gate(source_state, backtest_report)
    state = {
        'schema': 'bsfm.model-lifecycle.v1',
        'evaluated_at': utcnow(),
        'candidate_fit_attempted': False,
        'candidate_promoted': False,
        'incumbent_retained': True,
        'gate': gate,
        'reason': 'model_update_gate_open_estimator_not_implemented' if gate['pass'] else 'model_update_blocked_scientific_gate',
    }
    state['state_hash'] = digest(state)
    path = Path(out_path) if out_path else ROOT/'evaluations'/'model-update-state.json'
    write_json_atomic(path, state)
    return state

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from .integrity import digest, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]


def utcnow():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')


def fit_gate(source_state: dict, backtest_report: dict | None = None) -> dict:
    """Evidence required before a candidate estimator may be fitted.

    Calibration cannot be a prerequisite to fitting the candidate that must
    subsequently be evaluated. Keeping this gate separate avoids that circular
    dependency while retaining all point-in-time/leakage requirements.
    """
    backtest_report = backtest_report or {}
    checks = {
        'source_integrity_ready': bool(source_state.get('source_integrity_ready')),
        'point_in_time_availability_verified': bool(source_state.get('point_in_time_availability_verified')),
        'leakage_free': bool(backtest_report.get('leakage_free')),
        'baseline_present': bool(backtest_report.get('baseline_present')),
        'historical_cases': bool(backtest_report.get('historical_cases')),
    }
    missing = [name for name, ok in checks.items() if not ok]
    return {'pass': not missing, 'checks': checks, 'missing': missing}


def promotion_gate(source_state: dict, backtest_report: dict | None = None) -> dict:
    """Evidence required before a fitted candidate may replace the incumbent."""
    backtest_report = backtest_report or {}
    prefit = fit_gate(source_state, backtest_report)
    checks = {
        **prefit['checks'],
        'calibration_evaluated': bool(backtest_report.get('calibration_evaluated')),
        'paired_baseline_comparison': bool(backtest_report.get('paired_baseline_comparison')),
        'candidate_better_than_baseline': bool(backtest_report.get('candidate_better_than_baseline')),
    }
    missing = [name for name, ok in checks.items() if not ok]
    return {'pass': not missing, 'checks': checks, 'missing': missing}


def candidate_gate(source_state: dict, backtest_report: dict | None = None) -> dict:
    """Backward-compatible name for the stricter promotion gate."""
    return promotion_gate(source_state, backtest_report)


def update_model(source_state: dict, backtest_report: dict | None = None, out_path=None) -> dict:
    """Fail-closed lifecycle state used by AGGIORNA.

    The repository still contains no production estimator fitting step. The
    state therefore records independent fit and promotion readiness but never
    pretends that a candidate was trained or promoted.
    """
    fit = fit_gate(source_state, backtest_report)
    promotion = promotion_gate(source_state, backtest_report)
    state = {
        'schema': 'bsfm.model-lifecycle.v2',
        'evaluated_at': utcnow(),
        'candidate_fit_attempted': False,
        'candidate_promoted': False,
        'incumbent_retained': True,
        'fit_gate': fit,
        'gate': promotion,
        'reason': 'candidate_fit_not_implemented' if fit['pass'] else 'model_update_blocked_scientific_gate',
    }
    state['state_hash'] = digest(state)
    path = Path(out_path) if out_path else ROOT/'evaluations'/'model-update-state.json'
    write_json_atomic(path, state)
    return state

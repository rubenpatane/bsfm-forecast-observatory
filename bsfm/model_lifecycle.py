from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from .integrity import digest, write_json_atomic
from .estimator import fit_shrunk_hazard

ROOT = Path(__file__).resolve().parents[1]


def utcnow():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')


def fit_gate(source_state: dict, backtest_report: dict | None = None) -> dict:
    backtest_report=backtest_report or {}
    checks={
        # Source-state owns transport/schema integrity only. Historical PIT and
        # leakage eligibility are scientific properties of the explicitly frozen
        # backtest predictor universe and therefore come from the foundation report.
        'source_integrity_ready':bool(source_state.get('source_integrity_ready')),
        'point_in_time_availability_verified':bool(backtest_report.get('point_in_time_availability_verified')),
        'leakage_free':bool(backtest_report.get('leakage_free')),
        'baseline_present':bool(backtest_report.get('baseline_present')),
        'historical_cases':bool(backtest_report.get('historical_cases')),
    }
    missing=[name for name,ok in checks.items() if not ok]
    return {'pass':not missing,'checks':checks,'missing':missing}


def promotion_gate(source_state: dict, backtest_report: dict | None = None) -> dict:
    backtest_report=backtest_report or {}; prefit=fit_gate(source_state,backtest_report)
    checks={**prefit['checks'],
        'calibration_evaluated':bool(backtest_report.get('calibration_evaluated')),
        'paired_baseline_comparison':bool(backtest_report.get('paired_baseline_comparison')),
        'candidate_better_than_baseline':bool(backtest_report.get('candidate_better_than_baseline')),
    }
    missing=[name for name,ok in checks.items() if not ok]
    return {'pass':not missing,'checks':checks,'missing':missing}


def candidate_gate(source_state: dict, backtest_report: dict | None = None) -> dict:
    return promotion_gate(source_state,backtest_report)


def fit_candidate(source_state, backtest_report, events, exposure_rows, cohorts):
    """Fit the implemented shrinkage candidate only after the independent fit gate."""
    gate=fit_gate(source_state,backtest_report)
    if not gate['pass']:
        return {'fitted':False,'gate':gate,'reason':'model_update_blocked_scientific_gate'}
    model=fit_shrunk_hazard(events,exposure_rows,cohorts)
    model['model_hash']=digest(model)
    return {'fitted':True,'gate':gate,'model':model}


def update_model(source_state: dict, backtest_report: dict | None = None, out_path=None) -> dict:
    """Record lifecycle readiness; fitting requires explicit immutable historical inputs.

    AGGIORNA does not fabricate those inputs when evidence gates are closed. Once
    they are green, `fit_candidate` is the auditable fitting entry point and a
    fitted model still cannot be promoted without post-fit OOS evidence.
    """
    fit=fit_gate(source_state,backtest_report); promotion=promotion_gate(source_state,backtest_report)
    state={
        'schema':'bsfm.model-lifecycle.v3','evaluated_at':utcnow(),
        'candidate_fit_attempted':False,'candidate_promoted':False,'incumbent_retained':True,
        'fit_gate':fit,'gate':promotion,
        'estimator_available':True,
        'reason':'candidate_inputs_required_for_fit' if fit['pass'] else 'model_update_blocked_scientific_gate',
    }
    state['state_hash']=digest(state)
    path=Path(out_path) if out_path else ROOT/'evaluations'/'model-update-state.json'
    write_json_atomic(path,state); return state

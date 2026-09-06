from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path

from .integrity import digest, write_json_atomic
from .model_lifecycle import fit_gate, promotion_gate
from .estimator import fit_shrunk_hazard
from .temporal import exposure_only_baseline, paired_temporal_evaluation, time_to_event_distribution


def _utcnow():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')


def validate_cycle_spec(spec):
    required={'cycle_version','model_contract_version','candidate_estimator','target_taxonomy','forecast_horizon_days','scoring','immutability_policy','cohorts'}
    missing=sorted(required-set(spec))
    if missing:
        raise ValueError(f'incomplete cycle specification: {missing}')
    if spec['immutability_policy']!='new_version_for_method_change':
        raise ValueError('method changes must require a new explicit version')
    if spec['candidate_estimator']!='minimal_shrunk_hazard_v1':
        raise ValueError('unregistered candidate estimator')
    return True


def validate_registered_spec(spec, registry):
    validate_cycle_spec(spec)
    entries={str(x['cycle_version']):x for x in registry.get('specifications',[])}
    version=str(spec['cycle_version'])
    if version not in entries or entries[version].get('spec_hash')!=digest(spec):
        raise ValueError('cycle specification hash is not registered for this version')
    return True


def build_training_snapshot(spec, events, exposure, future_exposure):
    """Content-address every scientific input; never include retrieval secrets."""
    validate_cycle_spec(spec)
    snapshot={'schema':'bsfm.training-snapshot.v1','cycle_spec_hash':digest(spec),'events':deepcopy(list(events)),'exposure':deepcopy(list(exposure)),'future_exposure':deepcopy(list(future_exposure))}
    snapshot['snapshot_hash']=digest(snapshot)
    return snapshot


def run_cycle(spec, source_state, foundation_report, events, exposure, future_exposure, cohorts, backtest_cases=None, evaluated_at=None):
    """Run the frozen automatic cycle, or emit an auditable blocked result.

    This executor updates parameters, never methodology. The minimal estimator is
    explicitly a candidate implementation and is not represented as the complete
    contractual BSFM 1.2 model.
    """
    validate_cycle_spec(spec)
    events=list(events); exposure=list(exposure); future_exposure=list(future_exposure); backtest_cases=list(backtest_cases or [])
    snapshot=build_training_snapshot(spec,events,exposure,future_exposure)
    gate=fit_gate(source_state,foundation_report)
    state={'schema':'bsfm.research-cycle-result.v1','evaluated_at':evaluated_at or _utcnow(),'cycle_version':spec['cycle_version'],'cycle_spec_hash':digest(spec),'model_contract_version':spec['model_contract_version'],'candidate_estimator':spec['candidate_estimator'],'training_snapshot_hash':snapshot['snapshot_hash'],'fit_gate':gate,'fitted':False,'backtest_evaluated':False,'forecast_generated':False,'promoted':False}
    if not gate['pass']:
        state['reason']='scientific_fit_gate_closed'; state['result_hash']=digest(state); return state
    model=fit_shrunk_hazard(events,exposure,cohorts); model['model_hash']=digest(model)
    start=future_exposure[0]['date'] if future_exposure else None
    forecast=time_to_event_distribution(model,future_exposure,start,int(spec['forecast_horizon_days']))
    baseline_model=exposure_only_baseline(len(list(events)),sum(float(x['departures']) for x in exposure),cohorts)
    baseline=time_to_event_distribution(baseline_model,future_exposure,start,int(spec['forecast_horizon_days']))
    evaluation=paired_temporal_evaluation(backtest_cases)
    state.update({'fitted':True,'model':model,'baseline_model':baseline_model,'forecast':forecast,'baseline_forecast':baseline,'backtest_evaluated':evaluation['evaluated'],'paired_backtest':evaluation})
    post=promotion_gate(source_state,foundation_report)
    better=evaluation.get('candidate_better') is True
    state['promoted']=post['pass'] and better
    state['promotion_gate']=post
    state['reason']='promoted' if state['promoted'] else ('paired_backtest_required' if not evaluation['evaluated'] else 'promotion_gate_closed_or_candidate_not_better')
    state['forecast_generated']=True
    state['result_hash']=digest(state); return state


def execute_repository_cycle(root, source_state, foundation_report, evaluated_at=None):
    """Execute the repository contract from declared paths, always publishing state."""
    root=Path(root); spec=json.loads((root/'config/research-cycle-v1.json').read_text(encoding='utf-8'))
    registry=json.loads((root/'config/research-cycle-registry.json').read_text(encoding='utf-8'))
    validate_registered_spec(spec,registry)
    gate=fit_gate(source_state,foundation_report)
    if not gate['pass']:
        result=run_cycle(spec,source_state,foundation_report,[],[],[],[],evaluated_at=evaluated_at)
    else:
        paths={
            'events':root/'data/model/training-events.json',
            'exposure':root/'data/model/training-exposure.json',
            'future':root/'data/model/future-daily-exposure.json',
            'backtest':root/'data/model/temporal-backtest-cases.json',
        }
        missing=sorted(k for k,p in paths.items() if not p.exists())
        if missing:
            result={'schema':'bsfm.research-cycle-result.v1','evaluated_at':evaluated_at or _utcnow(),'cycle_version':spec['cycle_version'],'cycle_spec_hash':digest(spec),'model_contract_version':spec['model_contract_version'],'candidate_estimator':spec['candidate_estimator'],'fit_gate':gate,'fitted':False,'backtest_evaluated':False,'forecast_generated':False,'promoted':False,'reason':'declared_input_artifacts_missing','missing_input_artifacts':missing}
            result['result_hash']=digest(result)
        else:
            load=lambda p:json.loads(p.read_text(encoding='utf-8'))
            result=run_cycle(spec,source_state,foundation_report,load(paths['events']),load(paths['exposure']),load(paths['future']),spec['cohorts'],load(paths['backtest']),evaluated_at=evaluated_at)
    write_json_atomic(root/'site/data/research-cycle.json',result)
    return result

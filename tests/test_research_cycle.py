import json
from pathlib import Path

from bsfm.research_cycle import build_training_snapshot, execute_repository_cycle, run_cycle, validate_registered_spec

ROOT=Path(__file__).resolve().parents[1]


def spec():
    return json.loads((ROOT/'config/research-cycle-v1.json').read_text())


def full_report():
    return {'point_in_time_availability_verified':True,'leakage_free':True,'baseline_present':True,'historical_cases':True,'calibration_evaluated':True,'paired_baseline_comparison':True,'candidate_better_than_baseline':True}


def rows():
    events=[{'cohort':'737-NG'}]
    exposure=[{'cohort':'737-NG','departures':1_000_000},{'cohort':'777','departures':1_000_000}]
    future=[{'date':f'2026-10-{i:02d}','exposure_by_cohort':{'737-NG':1000,'777':1000}} for i in range(1,32)]
    future += [{'date':f'2026-11-{i:02d}','exposure_by_cohort':{'737-NG':1000,'777':1000}} for i in range(1,31)]
    future += [{'date':f'2026-12-{i:02d}','exposure_by_cohort':{'737-NG':1000,'777':1000}} for i in range(1,30)]
    return events,exposure,future


def test_snapshot_is_content_addressed_and_spec_bound():
    events,exposure,future=rows(); a=build_training_snapshot(spec(),events,exposure,future)
    assert a['snapshot_hash'].startswith('sha256:') and a['cycle_spec_hash'].startswith('sha256:')


def test_cycle_fails_closed_before_reading_incomplete_scientific_inputs():
    result=run_cycle(spec(),{'source_integrity_ready':True},{},[],[],[],['737-NG'],evaluated_at='2026-09-06T00:00:00Z')
    assert not result['fitted'] and not result['forecast_generated']
    assert result['reason']=='scientific_fit_gate_closed'


def test_cycle_fits_and_forecasts_only_when_prefit_gate_is_open():
    events,exposure,future=rows()
    result=run_cycle(spec(),{'source_integrity_ready':True},full_report(),events,exposure,future,['737-NG','777'],evaluated_at='2026-09-06T00:00:00Z')
    assert result['fitted'] and result['forecast_generated']
    assert result['forecast']['horizon_days']==90
    assert not result['promoted'] and result['reason']=='paired_backtest_required'


def test_repository_cycle_always_publishes_auditable_blocked_state(tmp_path):
    (tmp_path/'config').mkdir(); (tmp_path/'site/data').mkdir(parents=True)
    (tmp_path/'config/research-cycle-v1.json').write_text(json.dumps(spec()))
    registry=json.loads((ROOT/'config/research-cycle-registry.json').read_text())
    (tmp_path/'config/research-cycle-registry.json').write_text(json.dumps(registry))
    result=execute_repository_cycle(tmp_path,{'source_integrity_ready':True},{},evaluated_at='2026-09-06T00:00:00Z')
    saved=json.loads((tmp_path/'site/data/research-cycle.json').read_text())
    assert result==saved and result['reason']=='scientific_fit_gate_closed'


def test_registered_cycle_spec_cannot_change_silently():
    registry=json.loads((ROOT/'config/research-cycle-registry.json').read_text())
    assert validate_registered_spec(spec(),registry)
    changed=spec(); changed['forecast_horizon_days']=91
    try:
        validate_registered_spec(changed,registry)
    except ValueError as exc:
        assert 'not registered' in str(exc)
    else:
        raise AssertionError('unregistered method change accepted')

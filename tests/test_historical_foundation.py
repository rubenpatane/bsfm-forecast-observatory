from bsfm.historical_foundation import HORIZONS, audit_historical_foundation, build_walk_forward_cases


def target():
    return {'event_date':'2024-06-30','manufacturer':'Boeing','model':'737-800'}


def test_walk_forward_builds_all_preregistered_horizons_for_isolated_target():
    cases=build_walk_forward_cases([target()],2010,2025)
    assert [c['horizon_days'] for c in cases]==list(HORIZONS)
    assert cases[-1]['cutoff']=='2024-06-23'
    assert cases[-1]['case_id']=='2024-06-30-T7'


def test_walk_forward_excludes_cutoff_if_another_target_intervenes():
    earlier={'event_date':'2024-05-01','manufacturer':'Boeing','model':'777'}
    later=target()
    cases=build_walk_forward_cases([earlier,later],2010,2025)
    later_cases=[c for c in cases if c['target_event_date']=='2024-06-30']
    assert [c['horizon_days'] for c in later_cases]==[30,7]


def test_walk_forward_excludes_targets_outside_evaluation_interval():
    row=target(); row['event_date']='2009-12-31'
    assert build_walk_forward_cases([row],2010,2025)==[]


def test_foundation_fails_closed_when_any_gate_is_missing():
    report=audit_historical_foundation({'complete':True},{'complete':True},{'point_in_time_availability_verified':False,'leakage_free':True})
    assert not report['ready_for_candidate_fit']
    assert report['blocked_reasons']==['point_in_time_availability_verified']


def test_foundation_does_not_infer_availability_from_missing_metadata():
    report=audit_historical_foundation({'complete':True},{'complete':True},{})
    assert not report['point_in_time_availability_verified']
    assert not report['leakage_free']
    assert not report['ready_for_candidate_fit']


def test_foundation_ready_only_when_every_independent_gate_passes():
    report=audit_historical_foundation({'complete':True},{'complete':True},{'point_in_time_availability_verified':True,'leakage_free':True})
    assert report['ready_for_candidate_fit']

from bsfm.model_lifecycle import candidate_gate, update_model


def test_candidate_gate_blocks_unverified_point_in_time():
    source={'source_integrity_ready':True,'point_in_time_availability_verified':False}
    report={'leakage_free':True,'baseline_present':True,'historical_cases':True,'calibration_evaluated':True}
    gate=candidate_gate(source,report)
    assert not gate['pass']
    assert 'point_in_time_availability_verified' in gate['missing']


def test_candidate_gate_requires_all_scientific_evidence():
    source={'source_integrity_ready':True,'point_in_time_availability_verified':True}
    report={'leakage_free':True,'baseline_present':True,'historical_cases':True,'calibration_evaluated':True}
    assert candidate_gate(source,report)['pass']


def test_update_model_does_not_fit_when_gate_closed(tmp_path):
    source={'source_integrity_ready':True,'point_in_time_availability_verified':False}
    state=update_model(source,{},tmp_path/'state.json')
    assert state['candidate_fit_attempted'] is False
    assert state['candidate_promoted'] is False
    assert state['incumbent_retained'] is True
    assert state['reason']=='model_update_blocked_scientific_gate'

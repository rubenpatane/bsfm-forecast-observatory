from bsfm.model_lifecycle import candidate_gate, fit_gate, promotion_gate, update_model


def full_report():
    return {
        'leakage_free':True,
        'baseline_present':True,
        'historical_cases':True,
        'calibration_evaluated':True,
        'paired_baseline_comparison':True,
        'candidate_better_than_baseline':True,
    }


def test_candidate_gate_blocks_unverified_point_in_time():
    source={'source_integrity_ready':True,'point_in_time_availability_verified':False}
    gate=candidate_gate(source,full_report())
    assert not gate['pass']
    assert 'point_in_time_availability_verified' in gate['missing']


def test_promotion_gate_requires_all_scientific_evidence():
    source={'source_integrity_ready':True,'point_in_time_availability_verified':True}
    assert candidate_gate(source,full_report())['pass']


def test_fit_gate_is_not_circular_on_postfit_calibration():
    source={'source_integrity_ready':True,'point_in_time_availability_verified':True}
    report={'leakage_free':True,'baseline_present':True,'historical_cases':True}
    assert fit_gate(source,report)['pass']
    promotion=promotion_gate(source,report)
    assert not promotion['pass']
    assert 'calibration_evaluated' in promotion['missing']
    assert 'paired_baseline_comparison' in promotion['missing']


def test_update_model_does_not_fit_when_gate_closed(tmp_path):
    source={'source_integrity_ready':True,'point_in_time_availability_verified':False}
    state=update_model(source,{},tmp_path/'state.json')
    assert state['candidate_fit_attempted'] is False
    assert state['candidate_promoted'] is False
    assert state['incumbent_retained'] is True
    assert state['reason']=='model_update_blocked_scientific_gate'

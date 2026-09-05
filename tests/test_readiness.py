from bsfm.readiness import final_readiness


def test_final_readiness_keeps_scientific_gates_closed_on_unknowns():
    report=final_readiness({'historical_cases':False,'baseline_present':False,'point_in_time_availability_verified':False,'leakage_free':False,'calibration_evaluated':False})
    assert report['software_audit_evaluable'] is True
    assert report['scientific_fit_ready'] is False
    assert report['scientific_promotion_ready'] is False
    assert report['absolute_accident_probabilities_enabled'] is False
    assert report['validated_prediction_claim_allowed'] is False
    assert 'paired_baseline_comparison' in report['blocked_reasons']


def test_final_readiness_does_not_equate_fit_with_promotion():
    foundation={'historical_cases':True,'baseline_present':True,'point_in_time_availability_verified':True,'leakage_free':True,'calibration_evaluated':False,'paired_baseline_comparison':True,'candidate_better_than_baseline':True}
    report=final_readiness(foundation,{'gate':{'pass':True}})
    assert report['scientific_fit_ready'] is True
    assert report['scientific_promotion_ready'] is False
    assert report['blocked_reasons']==['calibration_evaluated']


def test_final_readiness_requires_all_postfit_evidence_and_lifecycle_gate():
    foundation={'historical_cases':True,'baseline_present':True,'point_in_time_availability_verified':True,'leakage_free':True,'calibration_evaluated':True,'paired_baseline_comparison':True,'candidate_better_than_baseline':True}
    assert final_readiness(foundation,{'gate':{'pass':False,'missing':['candidate_registry_record']}})['scientific_promotion_ready'] is False
    report=final_readiness(foundation,{'gate':{'pass':True,'missing':[]}})
    assert report['scientific_promotion_ready'] is True
    assert report['blocked_reasons']==[]

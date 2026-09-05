from bsfm.readiness import final_readiness


def test_final_readiness_keeps_scientific_gates_closed_on_unknowns():
    report=final_readiness({
        'historical_cases':False,
        'baseline_present':False,
        'point_in_time_availability_verified':False,
        'leakage_free':False,
        'calibration_evaluated':False,
    })
    assert report['software_audit_evaluable'] is True
    assert report['scientific_fit_ready'] is False
    assert report['scientific_promotion_ready'] is False
    assert report['absolute_accident_probabilities_enabled'] is False
    assert report['validated_prediction_claim_allowed'] is False


def test_final_readiness_does_not_equate_fit_with_promotion():
    foundation={
        'historical_cases':True,
        'baseline_present':True,
        'point_in_time_availability_verified':True,
        'leakage_free':True,
        'calibration_evaluated':False,
    }
    report=final_readiness(foundation,{'gate':{'pass':True}})
    assert report['scientific_fit_ready'] is True
    assert report['scientific_promotion_ready'] is False
    assert report['blocked_reasons']==['calibration_evaluated']


def test_final_readiness_requires_lifecycle_promotion_gate_even_after_calibration():
    foundation={
        'historical_cases':True,
        'baseline_present':True,
        'point_in_time_availability_verified':True,
        'leakage_free':True,
        'calibration_evaluated':True,
    }
    assert final_readiness(foundation,{'gate':{'pass':False}})['scientific_promotion_ready'] is False
    assert final_readiness(foundation,{'gate':{'pass':True}})['scientific_promotion_ready'] is True

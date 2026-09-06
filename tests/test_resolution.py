from bsfm.resolution import audit_resolution, audit_resolution_dimension


def test_geography_can_be_supported_independently_of_msn():
    geo={'estimator_supported':True,'exposure_denominator_supported':True,'pit_supported':True,'provenance_supported':True,'uncertainty_supported':True}
    out=audit_resolution({'geography':geo})
    assert out['geography']['status']=='SUPPORTED'
    assert out['msn']['status']=='BLOCKED'
    assert out['flight_number']['status']=='BLOCKED'


def test_msn_fails_without_airframe_exposure_and_identity_history():
    out=audit_resolution_dimension('msn',{'estimator_supported':True,'pit_supported':True,'provenance_supported':True,'uncertainty_supported':True})
    assert out['status']=='BLOCKED'
    assert 'airframe_exposure_supported' in out['missing']
    assert 'identity_history_supported' in out['missing']

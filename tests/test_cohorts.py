from bsfm.cohorts import boeing_cohort


def test_boeing_cohort_maps_supported_families():
    assert boeing_cohort('737-200') == '737-Original'
    assert boeing_cohort('737-400') == '737-Classic'
    assert boeing_cohort('737-800') == '737-NG'
    assert boeing_cohort('737 MAX 8') == '737-MAX'
    assert boeing_cohort('737-8') == '737-MAX'
    assert boeing_cohort('727-200') == '727'
    assert boeing_cohort('777-300ER') == '777'
    assert boeing_cohort('787-9') == '787'


def test_boeing_cohort_fails_closed_for_unknown_model():
    assert boeing_cohort('A320') is None
    assert boeing_cohort('MD-83') is None
    assert boeing_cohort('') is None

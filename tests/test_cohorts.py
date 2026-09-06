from bsfm.cohorts import boeing_cohort, cohort_from_icao_equipment


def test_boeing_cohort_maps_supported_families():
    assert boeing_cohort('737-200') == '737-Original'
    assert boeing_cohort('737-236A') == '737-Original'
    assert boeing_cohort('737-400') == '737-Classic'
    assert boeing_cohort('737-476') == '737-Classic'
    assert boeing_cohort('737-800') == '737-NG'
    assert boeing_cohort('737-8K5') == '737-NG'
    assert boeing_cohort('737-7H4') == '737-NG'
    assert boeing_cohort('737 MAX 8') == '737-MAX'
    assert boeing_cohort('737-8 MAX') == '737-MAX'
    assert boeing_cohort('737-8') == '737-MAX'
    assert boeing_cohort('727-221') == '727'
    assert boeing_cohort('777-300ER') == '777'
    assert boeing_cohort('787-9') == '787'


def test_boeing_cohort_fails_closed_for_unknown_model():
    assert boeing_cohort('A320') is None
    assert boeing_cohort('MD-83') is None
    assert boeing_cohort('') is None


def test_icao_equipment_mapping_separates_737_generations_without_proxy_split():
    assert cohort_from_icao_equipment('B731') == '737-Original'
    assert cohort_from_icao_equipment('B732') == '737-Original'
    assert cohort_from_icao_equipment('B733') == '737-Classic'
    assert cohort_from_icao_equipment('B735') == '737-Classic'
    assert cohort_from_icao_equipment('B736') == '737-NG'
    assert cohort_from_icao_equipment('B738') == '737-NG'
    assert cohort_from_icao_equipment('B37M') == '737-MAX'
    assert cohort_from_icao_equipment('B38M') == '737-MAX'
    assert cohort_from_icao_equipment('B39M') == '737-MAX'


def test_icao_equipment_mapping_maps_other_target_families():
    assert cohort_from_icao_equipment('B721') == '727'
    assert cohort_from_icao_equipment('B744') == '747'
    assert cohort_from_icao_equipment('B752') == '757'
    assert cohort_from_icao_equipment('B763') == '767'
    assert cohort_from_icao_equipment('B77W') == '777'
    assert cohort_from_icao_equipment('B789') == '787'


def test_icao_equipment_mapping_fails_closed_for_unknown_or_generic_codes():
    assert cohort_from_icao_equipment('B737X') is None
    assert cohort_from_icao_equipment('737') is None
    assert cohort_from_icao_equipment('A320') is None
    assert cohort_from_icao_equipment('') is None

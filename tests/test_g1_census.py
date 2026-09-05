from bsfm.g1_census import audit_g1_records, parse_icao_official_accidents_csv, sha256_bytes


def test_parse_preserves_raw_and_source_provenance():
    data = b'Occurrence ID,Date,Manufacturer,Model,Fatalities,Commercial\nA1,2020-01-02,BOEING,737-800,2,Commercial\n'
    rows = parse_icao_official_accidents_csv(data)
    assert rows[0]['event_id'] == 'A1'
    assert rows[0]['manufacturer'] == 'BOEING'
    assert rows[0]['source_publisher'] == 'ICAO'
    assert rows[0]['raw']['Occurrence ID'] == 'A1'


def test_structural_audit_never_opens_g1_by_itself():
    rows = [{
        'event_id':'A1','event_date':'2020-01-02','manufacturer':'BOEING','model':'737-800',
        'fatalities':'2','commercial':'Commercial','source_publisher':'ICAO',
        'source_record_id':'A1','source_locator':'ICAO API Data Service / Official Accidents'
    }]
    audit = audit_g1_records(rows)
    assert audit['structurally_complete'] is True
    assert audit['global_census_complete'] is False
    assert audit['gate_status'] == 'BLOCKED'


def test_missing_provenance_fails_structural_audit():
    audit = audit_g1_records([{'event_date':'2020-01-02'}])
    assert audit['structurally_complete'] is False
    assert audit['gate_status'] == 'BLOCKED'


def test_sha256_is_deterministic():
    assert sha256_bytes(b'abc') == 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'

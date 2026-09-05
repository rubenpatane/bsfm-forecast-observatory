from bsfm.pit_evidence import audit_pit_manifest, audit_pit_record, strict_pit_admissible


def test_verified_requires_exact_publication_evidence():
    row = {
        'source_record_id': 'x',
        'pit_status': 'verified',
        'available_at': '2020-01-15T00:00:00Z',
        'availability_evidence': 'official release 2020-01-15',
        'availability_basis': 'explicit_publication_timestamp',
    }
    assert audit_pit_record(row) == []
    assert strict_pit_admissible(row, '2020-01-15T00:00:00Z')
    assert not strict_pit_admissible(row, '2020-01-14T23:59:59Z')


def test_approval_date_cannot_be_promoted_to_publication():
    row = {
        'source_record_id': 'x',
        'pit_status': 'verified',
        'available_at': '2020-01-15T00:00:00Z',
        'availability_evidence': 'administrative approval field',
        'availability_basis': 'approval_date',
    }
    assert 'administrative_or_event_timestamp_not_publication_evidence' in audit_pit_record(row)
    assert not strict_pit_admissible(row, '2020-02-01T00:00:00Z')


def test_unknown_and_bounded_are_fail_closed_for_strict_backtest():
    unknown = {'source_record_id': 'u', 'pit_status': 'unknown'}
    bounded = {
        'source_record_id': 'b', 'pit_status': 'bounded',
        'available_not_before': '2020-01-01T00:00:00Z',
        'available_not_after': '2020-02-01T00:00:00Z',
    }
    assert audit_pit_record(unknown) == []
    assert audit_pit_record(bounded) == []
    assert not strict_pit_admissible(unknown, '2021-01-01T00:00:00Z')
    assert not strict_pit_admissible(bounded, '2021-01-01T00:00:00Z')


def test_manifest_validation_never_opens_g3_by_itself():
    rows = [{
        'source_record_id': 'x',
        'pit_status': 'verified',
        'available_at': '2020-01-15T00:00:00Z',
        'availability_evidence': 'official release 2020-01-15',
        'availability_basis': 'explicit_publication_timestamp',
    }]
    audit = audit_pit_manifest(rows)
    assert audit['valid'] is True
    assert audit['strict_verified_count'] == 1
    assert audit['g3_pass'] is False

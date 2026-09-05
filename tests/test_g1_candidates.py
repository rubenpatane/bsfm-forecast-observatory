from bsfm.g1_candidates import audit_candidate_census, normalize_candidate


def candidate(**overrides):
    row = {
        'event_id': 'B2024-001',
        'event_date': '2024-01-02',
        'manufacturer': 'Boeing',
        'model': '737-800',
        'fatalities': 2,
        'commercial': True,
        'source_publisher': 'Boeing',
        'source_record_id': 'summary-2025-pX',
        'source_locator': 'Boeing Statistical Summary 2025',
        'decision': 'unresolved',
        'decision_reason': 'Awaiting independent authority reconciliation.',
    }
    row.update(overrides)
    return row


def test_candidate_normalization_does_not_infer_optional_fields():
    row = normalize_candidate(candidate())
    assert row['manufacturer'] == 'Boeing'
    assert row['registration'] is None
    assert row['operator'] is None
    assert row['reconciliation_evidence'] == []


def test_candidate_normalization_preserves_explicit_reconciliation_evidence():
    evidence = [{'publisher': 'Independent authority', 'locator': 'https://example.test/report'}]
    row = normalize_candidate(candidate(reconciliation_evidence=evidence))
    assert row['reconciliation_evidence'] == evidence


def test_candidate_audit_is_fail_closed_even_when_structurally_valid():
    audit = audit_candidate_census([candidate()])
    assert audit['candidate_dataset_structurally_valid'] is True
    assert audit['years'][2024]['unresolved'] == 1
    assert audit['global_census_complete'] is False
    assert audit['gate_status'] == 'BLOCKED'


def test_reconciliation_evidence_does_not_open_gate():
    audit = audit_candidate_census([candidate(reconciliation_evidence=[{'publisher': 'Boeing'}])])
    assert audit['candidate_dataset_structurally_valid'] is True
    assert audit['global_census_complete'] is False
    assert audit['gate_status'] == 'BLOCKED'


def test_candidate_requires_decision_reason_and_valid_decision():
    audit = audit_candidate_census([candidate(decision='maybe', decision_reason='')])
    assert audit['candidate_dataset_structurally_valid'] is False
    fields = audit['invalid_records'][0]['missing_or_invalid']
    assert 'decision_reason' in fields
    assert 'valid_decision' in fields


def test_duplicate_internal_ids_fail_structural_validity():
    audit = audit_candidate_census([candidate(), candidate(event_date='2024-02-03')])
    assert audit['candidate_dataset_structurally_valid'] is False
    assert audit['duplicate_event_ids'] == ['B2024-001']
    assert audit['gate_status'] == 'BLOCKED'

import json

from bsfm.g1_outcome_pit import audit_g1_outcome_pit


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding='utf-8')


def _candidate(**extra):
    row = {
        'event_id': 'E1',
        'event_date': '2019-01-01',
        'decision': 'include',
        'model': '737-800',
    }
    row.update(extra)
    return row


def test_g1_outcome_pit_fails_closed_without_publication_evidence(tmp_path):
    _write(tmp_path/'data/census/g1-candidates.json', {'records': [_candidate()]})
    out = audit_g1_outcome_pit(tmp_path)
    assert out['included_events'] == 1
    assert out['verified_events'] == 0
    assert out['complete'] is False
    assert out['unverified_event_ids'] == ['E1']


def test_g1_outcome_pit_accepts_explicit_verified_publication_basis(tmp_path):
    _write(tmp_path/'data/census/g1-candidates.json', {'records': [_candidate(
        available_at='2019-03-01',
        availability_basis='competent_authority_publication',
        availability_evidence_ids=['authority-report-2019-03-01'],
    )]})
    out = audit_g1_outcome_pit(tmp_path)
    assert out['verified_events'] == 1
    assert out['complete'] is True


def test_g1_outcome_pit_rejects_event_date_as_implicit_availability(tmp_path):
    _write(tmp_path/'data/census/g1-candidates.json', {'records': [_candidate(
        available_at='2019-01-01',
        availability_basis='event_date',
        availability_evidence_ids=['event-record'],
    )]})
    out = audit_g1_outcome_pit(tmp_path)
    assert out['complete'] is False
    assert 'missing_or_unapproved_availability_basis' in out['events'][0]['reasons']


def test_g1_outcome_pit_rejects_availability_before_event(tmp_path):
    _write(tmp_path/'data/census/g1-candidates.json', {'records': [_candidate(
        available_at='2018-12-31',
        availability_basis='archived_public_snapshot',
        availability_evidence_ids=['snapshot'],
    )]})
    out = audit_g1_outcome_pit(tmp_path)
    assert out['complete'] is False
    assert out['invalid_event_ids'] == ['E1']

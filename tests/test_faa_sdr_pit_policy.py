import json
from pathlib import Path


def _load(root, name):
    return json.loads((root / 'data/pit' / name).read_text(encoding='utf-8'))


def test_faa_sdr_policy_rejects_submission_and_difficulty_dates_as_publication():
    root = Path(__file__).resolve().parents[1]
    policy = _load(root, 'faa-sdr-field-release-policy.json')
    by_field = {row['field']: row for row in policy['rules']}
    assert by_field['SubmissionDate']['pit_status'] == 'unknown'
    assert by_field['SubmissionDate']['availability_basis'] == 'submission_timestamp_not_publication'
    assert by_field['DifficultyDate']['pit_status'] == 'unknown'
    assert by_field['DifficultyDate']['availability_basis'] == 'event_timestamp_not_publication'


def test_faa_sdr_current_csv_does_not_claim_historical_available_at():
    root = Path(__file__).resolve().parents[1]
    policy = _load(root, 'faa-sdr-field-release-policy.json')
    current = next(row for row in policy['rules'] if row['field'] == 'current annual CSV row and fields')
    assert current['pit_status'] == 'bounded'
    assert 'available_at' not in current
    assert policy['default_rule']['pit_status'] == 'unknown'
    assert policy['g3_status'] == 'BLOCKED'


def test_faa_sdr_release_inventory_stays_blocked():
    root = Path(__file__).resolve().parents[1]
    inventory = _load(root, 'faa-sdr-release-inventory.json')
    assert inventory['g3_status'] == 'BLOCKED'
    assert 'SubmissionDate must not populate available_at.' in inventory['pit_implications']
    assert 'DifficultyDate must not populate available_at.' in inventory['pit_implications']
    nara = next(row for row in inventory['official_public_evidence'] if row['artifact'].startswith('NARA'))
    assert 'permanent digital records' in nara['establishes']
    assert 'does_not_establish' in nara

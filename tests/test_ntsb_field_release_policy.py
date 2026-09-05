import json
from pathlib import Path


def test_ntsb_field_release_policy_is_fail_closed():
    root = Path(__file__).resolve().parents[1]
    policy = json.loads((root / 'data/pit/ntsb-field-release-policy.json').read_text(encoding='utf-8'))
    assert policy['g3_status'] == 'BLOCKED'
    assert policy['default_rule']['pit_status'] == 'unknown'

    by_field = {row['field']: row for row in policy['rules']}
    cm = by_field['Findings.cm_inPC']
    assert cm['earliest_verified_schema_publication'] == '2024-03-01T00:00:00Z'
    assert cm['pit_status'] == 'bounded'
    assert 'back-filled' in cm['evidence']


def test_product_release_bounds_do_not_claim_record_availability():
    root = Path(__file__).resolve().parents[1]
    policy = json.loads((root / 'data/pit/ntsb-field-release-policy.json').read_text(encoding='utf-8'))
    for row in policy['rules']:
        assert row['pit_status'] == 'bounded'
        assert row.get('earliest_verified_schema_publication')
        assert 'available_at' not in row

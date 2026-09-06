import json

from bsfm.g2_exposure_pit import audit_g2_exposure_pit


def _write_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')


def _row(period, cohort, departures=1.0, vintage='vp-1'):
    return {
        'period': str(period),
        'cohort': cohort,
        'departures': departures,
        'source': 'licensed-source',
        'scope': 'global_commercial',
        'provenance': 'query-spec-v1',
        'vintage_policy_id': vintage,
        'source_vintage_ids': ['snapshot-a'],
    }


def test_g2_exposure_pit_blocks_empty_dataset(tmp_path):
    path = tmp_path/'data/exposure/departures.jsonl'
    path.parent.mkdir(parents=True)
    path.write_text('', encoding='utf-8')
    out = audit_g2_exposure_pit(tmp_path, 2019, 2019, ['737-NG'])
    assert out['rows'] == 0
    assert out['complete'] is False


def test_g2_exposure_pit_accepts_complete_matrix_with_single_vintage_policy(tmp_path):
    _write_rows(tmp_path/'data/exposure/departures.jsonl', [
        _row(2019, '737-NG'),
        _row(2019, '737-MAX'),
        _row(2020, '737-NG'),
        _row(2020, '737-MAX'),
    ])
    out = audit_g2_exposure_pit(tmp_path, 2019, 2020, ['737-NG', '737-MAX'])
    assert out['matrix']['complete'] is True
    assert out['vintage_policy_ids'] == ['vp-1']
    assert out['metadata_errors'] == []
    assert out['complete'] is True


def test_g2_exposure_pit_rejects_missing_or_mixed_vintage_metadata(tmp_path):
    rows = [_row(2019, '737-NG'), _row(2020, '737-NG', vintage='vp-2')]
    rows[0]['source_vintage_ids'] = []
    _write_rows(tmp_path/'data/exposure/departures.jsonl', rows)
    out = audit_g2_exposure_pit(tmp_path, 2019, 2020, ['737-NG'])
    assert out['matrix']['complete'] is True
    assert out['complete'] is False
    assert any(e['error'] == 'missing_source_vintage_ids' for e in out['metadata_errors'])
    assert any(e['error'] == 'mixed_or_missing_vintage_policy' for e in out['metadata_errors'])


def test_g2_exposure_pit_rejects_non_global_scope(tmp_path):
    row = _row(2019, '737-NG')
    row['scope'] = 'regional_only'
    _write_rows(tmp_path/'data/exposure/departures.jsonl', [row])
    out = audit_g2_exposure_pit(tmp_path, 2019, 2019, ['737-NG'])
    assert out['complete'] is False
    assert any(e['error'] == 'noncanonical_scope' for e in out['metadata_errors'])

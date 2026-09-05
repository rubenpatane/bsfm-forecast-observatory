import json
from pathlib import Path

from bsfm.pit_coverage import build_operational_pit_coverage


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding='utf-8')


def test_valid_source_is_not_automatically_pit_ready(tmp_path):
    _write(tmp_path / 'data/manifests/faa-sdr-2020.json', {
        'source': 'FAA SDR', 'year': 2020, 'status': 'validated',
        'historical_public_availability': 'unverified',
        'max_submission_date': '2022-04-03',
    })
    _write(tmp_path / 'data/manifests/ntsb-avall.json', {'source': 'NTSB AVALL', 'status': 'validated'})
    _write(tmp_path / 'data/pit/faa-sdr-release-inventory.json', {'g3_status': 'BLOCKED'})
    _write(tmp_path / 'data/pit/faa-sdr-field-release-policy.json', {'g3_status': 'BLOCKED'})
    _write(tmp_path / 'data/pit/ntsb-release-inventory.json', {'g3_status': 'BLOCKED'})
    _write(tmp_path / 'data/pit/ntsb-field-release-policy.json', {'g3_status': 'BLOCKED'})

    state = build_operational_pit_coverage(tmp_path)
    faa = state['sources']['FAA SDR']
    ntsb = state['sources']['NTSB AVALL']
    assert faa['years'][0]['source_valid'] is True
    assert faa['years'][0]['strict_pit_ready'] is False
    assert faa['years'][0]['late_submission_tail'] is True
    assert faa['years'][0]['max_submission_lag_years'] == 2
    assert faa['late_submission_tail_years'] == [2020]
    assert faa['max_observed_submission_lag_years'] == 2
    assert faa['all_years_strict_ready'] is False
    assert ntsb['source_valid'] is True
    assert ntsb['strict_pit_ready'] is False
    assert state['strict_operational_pit_ready'] is False
    assert state['g3_status'] == 'BLOCKED'


def test_only_explicit_verified_faa_year_counts_as_strict_ready(tmp_path):
    _write(tmp_path / 'data/manifests/faa-sdr-2020.json', {
        'year': 2020, 'status': 'validated', 'historical_public_availability': 'verified',
        'max_submission_date': '2020-12-31',
    })
    _write(tmp_path / 'data/manifests/faa-sdr-2021.json', {
        'year': 2021, 'status': 'validated', 'historical_public_availability': 'unverified',
        'max_submission_date': '2021-12-31',
    })
    state = build_operational_pit_coverage(tmp_path)
    faa = state['sources']['FAA SDR']
    assert faa['verified_years'] == [2020]
    assert faa['unverified_years'] == [2021]
    assert faa['late_submission_tail_years'] == []
    assert faa['all_years_strict_ready'] is False
    assert state['g3_status'] == 'BLOCKED'

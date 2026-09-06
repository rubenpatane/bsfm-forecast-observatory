import csv
import hashlib
import json
from pathlib import Path
import zipfile

from bsfm.bts_t100 import (
    aggregate_t100_archive,
    aggregate_t100_segments,
    public_scope_acceptance,
)


MAPPING = {'614': '737-NG', '838': '737-MAX'}
ROOT = Path(__file__).resolve().parents[1]


def _row(year, aircraft, departures, service_class='F'):
    return {
        'YEAR': year,
        'AIRCRAFT_TYPE': aircraft,
        'DEPARTURES_PERFORMED': departures,
        'CLASS': service_class,
    }


def test_t100_aggregates_official_performed_departures_without_leg_expansion():
    out = aggregate_t100_segments([
        _row('2019', '614', '12'),
        _row('2019', '614', '8'),
        _row('2019', '838', '3'),
    ], MAPPING, ['F'])
    got = {(r['period'], r['cohort']): r['departures'] for r in out['exposure_rows']}
    assert got == {('2019', '737-MAX'): 3.0, ('2019', '737-NG'): 20.0}
    assert out['scope'] == 'us_linked_commercial'
    assert out['global_g2_eligible'] is False


def test_t100_requires_explicit_type_and_service_class_allowlists():
    out = aggregate_t100_segments([
        _row('2019', '999', '10'),
        _row('2019', '614', '20', service_class='Z'),
    ], MAPPING, ['F'], target_aircraft_types=['614', '838', '999'])
    assert out['unmapped_aircraft_types'] == [{'aircraft_type': '999', 'departures': 10}]
    assert out['diagnostics']['excluded_service_class_rows'] == 1
    assert out['regional_matrix_candidate'] is False


def test_t100_ignores_reviewed_outside_target_universe_without_calling_it_unknown():
    out = aggregate_t100_segments([
        _row('2019', '614', '20'),
        _row('2019', '320', '10'),
    ], MAPPING, ['F'])
    assert out['unmapped_aircraft_types'] == []
    assert out['diagnostics']['outside_target_universe_rows'] == 1
    assert out['diagnostics']['outside_target_universe_departures'] == 10
    assert out['regional_matrix_candidate'] is True


def test_t100_rejects_fractional_negative_and_malformed_counts():
    out = aggregate_t100_segments([
        _row('2019', '614', '-1'),
        _row('2019', '614', '1.5'),
        _row('bad', '614', '1'),
    ], MAPPING, ['F'])
    assert out['diagnostics']['invalid_rows'] == 3
    assert out['regional_matrix_candidate'] is False


def test_public_scope_can_complete_region_but_never_global_g2():
    out = aggregate_t100_segments([
        _row('2019', '614', '12'),
        _row('2019', '838', '3'),
        _row('2020', '614', '9'),
        _row('2020', '838', '1'),
    ], MAPPING, ['F'], start_year=2019, end_year=2020)
    report = public_scope_acceptance(out, [2019, 2020], ['737-NG', '737-MAX'])
    assert report['regional_matrix_complete'] is True
    assert report['global_g2_status'] == 'BLOCKED'
    assert report['global_g2_pass_candidate'] is False


def test_public_scope_reports_missing_cells():
    out = aggregate_t100_segments(
        [_row('2019', '614', '12')], MAPPING, ['F'], start_year=2019, end_year=2020,
    )
    report = public_scope_acceptance(out, [2019, 2020], ['737-NG'])
    assert report['regional_matrix_complete'] is False
    assert report['missing_cells'] == [('2020', '737-NG')]


def test_archive_reader_records_exact_zip_hash(tmp_path):
    csv_path = tmp_path / 'T_T100_SEGMENT_ALL_CARRIER.csv'
    with csv_path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['YEAR', 'AIRCRAFT_TYPE', 'DEPARTURES_PERFORMED', 'CLASS'])
        writer.writeheader()
        writer.writerow(_row('2019', '614', '12'))
    archive = tmp_path / 'official-download.zip'
    with zipfile.ZipFile(archive, 'w') as bundle:
        bundle.write(csv_path, arcname=csv_path.name)
    out = aggregate_t100_archive(archive, MAPPING, ['F'])
    assert out['artifact']['sha256'] == hashlib.sha256(archive.read_bytes()).hexdigest()
    assert out['artifact']['csv_member'] == csv_path.name
    assert out['diagnostics']['counted_departures'] == 12


def test_archive_reader_rejects_ambiguous_zip(tmp_path):
    archive = tmp_path / 'ambiguous.zip'
    with zipfile.ZipFile(archive, 'w') as bundle:
        bundle.writestr('one.csv', 'YEAR,AIRCRAFT_TYPE,DEPARTURES_PERFORMED,CLASS\n')
        bundle.writestr('two.csv', 'YEAR,AIRCRAFT_TYPE,DEPARTURES_PERFORMED,CLASS\n')
    try:
        aggregate_t100_archive(archive, MAPPING, ['F'])
    except ValueError as exc:
        assert 'exactly one CSV' in str(exc)
    else:
        raise AssertionError('ambiguous archive must fail closed')


def test_committed_mapping_preserves_known_cross_cohort_ambiguity():
    mapping = json.loads((ROOT / 'data/exposure/bts-t100-cohort-mapping-v1.json').read_text())
    assert mapping['global_g2_eligible'] is False
    assert mapping['aircraft_type_to_cohort']['612'] == '737-NG'
    assert '2010-2025' in mapping['time_bounded_decisions']['612']
    assert '615' not in mapping['aircraft_type_to_cohort']
    assert '615' in mapping['reviewed_target_aircraft_types']
    assert '737-Classic' in mapping['unmapped_ambiguous_codes']['615']
    assert '737-NG' in mapping['unmapped_ambiguous_codes']['615']


def test_committed_series_audit_is_complete_only_after_versioned_merge():
    report = json.loads((ROOT / 'data/exposure/bts-t100-2010-2025-audit.json').read_text())
    assert len(report['artifacts']) == 16
    assert len(report['exposure_rows']) == 160
    assert report['unmapped_target_aircraft_types'] == [
        {'aircraft_type': '615', 'departures': 14}
    ]
    assert report['acceptance']['regional_matrix_complete'] is False
    assert report['acceptance']['global_g2_status'] == 'BLOCKED'
    merged = report['prospective_merged_cohort_candidate']
    assert merged['status'] == 'METHOD_CHANGE_REQUIRES_NEW_MODEL_VERSION'
    assert len(merged['exposure_rows']) == 144
    assert merged['acceptance']['regional_matrix_complete'] is True
    assert merged['acceptance']['global_g2_status'] == 'BLOCKED'


def test_public_data_model_1_3_is_separate_and_prospective():
    model = json.loads((ROOT / 'config/model-public-data-v1.3.json').read_text())
    assert model['model_id'] == 'BSFM-PD'
    assert model['model_version'] == '1.3'
    assert model['non_retroactive'] is True
    assert model['scope'] == 'us_linked_commercial'
    assert '737-Classic+NG' in model['cohorts']
    assert '737-Classic' not in model['cohorts']
    assert model['candidate_estimator'] == 'minimal_shrunk_hazard_v1'
    assert 'faa_sdr_precursors' in model['excluded_model_1_2_contractual_components']
    assert model['current_gate_status'].startswith('BLOCKED')

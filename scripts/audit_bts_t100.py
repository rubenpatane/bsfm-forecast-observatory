#!/usr/bin/env python3
"""Build a redistributable audit from locally downloaded T-100 archives."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from bsfm.bts_t100 import aggregate_t100_archive, public_scope_acceptance


COHORTS = (
    '727', '737-Original', '737-Classic', '737-NG', '737-MAX',
    '747', '757', '767', '777', '787',
)


def build_report(archive_dir, mapping_path, start_year=2010, end_year=2025):
    archive_dir = Path(archive_dir)
    mapping_path = Path(mapping_path)
    mapping = json.loads(mapping_path.read_text(encoding='utf-8'))
    years = list(range(int(start_year), int(end_year) + 1))
    exposure_rows = []
    unmapped = Counter()
    ambiguous_by_year = []
    artifacts = []
    diagnostics = {}
    for year in years:
        path = archive_dir / f'bts-t100-segment-all-carriers-{year}.zip'
        if not path.exists():
            raise FileNotFoundError(path)
        result = aggregate_t100_archive(
            path,
            mapping['aircraft_type_to_cohort'],
            mapping['admitted_service_classes'],
            target_aircraft_types=mapping['reviewed_target_aircraft_types'],
            start_year=year,
            end_year=year,
        )
        manifest_path = path.with_suffix('.manifest.json')
        if not manifest_path.exists():
            raise FileNotFoundError(manifest_path)
        download_manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if download_manifest.get('sha256') != result['artifact']['sha256']:
            raise ValueError(f'download manifest hash mismatch: {path.name}')
        exposure_rows.extend(result['exposure_rows'])
        artifacts.append({
            'year': year,
            **result['artifact'],
            'retrieved_at': download_manifest.get('retrieved_at'),
            'source_url': download_manifest.get('source_url'),
            'query': download_manifest.get('query'),
        })
        for row in result['unmapped_aircraft_types']:
            unmapped[row['aircraft_type']] += row['departures']
            ambiguous_by_year.append({'year': year, **row})
        for key, value in result['diagnostics'].items():
            diagnostics[key] = diagnostics.get(key, 0) + value

    present = {(row['period'], row['cohort']) for row in exposure_rows}
    zero_filled_cells = []
    for year in years:
        for cohort in COHORTS:
            if (str(year), cohort) not in present:
                row = {
                    'period': str(year), 'cohort': cohort, 'departures': 0.0,
                    'scope': 'us_linked_commercial',
                }
                exposure_rows.append(row)
                zero_filled_cells.append([str(year), cohort])
    exposure_rows.sort(key=lambda row: (row['period'], row['cohort']))

    aggregation = {
        'scope': 'us_linked_commercial',
        'regional_matrix_candidate': not unmapped and diagnostics.get('invalid_rows', 0) == 0,
        'exposure_rows': exposure_rows,
    }
    acceptance = public_scope_acceptance(aggregation, years, COHORTS)
    ambiguous_for_year = {
        int(row['year']): int(row['departures']) for row in ambiguous_by_year
        if row['aircraft_type'] == '615'
    }
    merged_rows = []
    for year in years:
        annual = {row['cohort']: row['departures'] for row in exposure_rows if row['period'] == str(year)}
        for cohort in COHORTS:
            if cohort in {'737-Classic', '737-NG'}:
                continue
            merged_rows.append({
                'period': str(year), 'cohort': cohort,
                'departures': annual[cohort], 'scope': 'us_linked_commercial',
            })
        merged_rows.append({
            'period': str(year), 'cohort': '737-Classic+NG',
            'departures': annual['737-Classic'] + annual['737-NG'] + ambiguous_for_year.get(year, 0),
            'scope': 'us_linked_commercial',
        })
    merged_cohorts = tuple(c for c in COHORTS if c not in {'737-Classic', '737-NG'}) + ('737-Classic+NG',)
    merged_acceptance = public_scope_acceptance(
        {'scope': 'us_linked_commercial', 'regional_matrix_candidate': True, 'exposure_rows': merged_rows},
        years, merged_cohorts,
    )
    return {
        'schema': 'bsfm.bts-t100-series-audit.v1',
        'status': 'RESEARCH_ONLY_NOT_MODEL_ADOPTION',
        'period': {'start_year': years[0], 'end_year': years[-1]},
        'scope': 'us_linked_commercial',
        'mapping_path': mapping_path.as_posix(),
        'artifacts': artifacts,
        'diagnostics': diagnostics,
        'unmapped_target_aircraft_types': [
            {'aircraft_type': code, 'departures': value}
            for code, value in sorted(unmapped.items())
        ],
        'unmapped_target_aircraft_types_by_year': ambiguous_by_year,
        'zero_filled_cells': zero_filled_cells,
        'exposure_rows': exposure_rows,
        'acceptance': acceptance,
        'prospective_merged_cohort_candidate': {
            'status': 'METHOD_CHANGE_REQUIRES_NEW_MODEL_VERSION',
            'cohort_change': 'Replace 737-Classic and 737-NG with 737-Classic+NG.',
            'reason': 'This retains every code-615 departure without proxy splitting.',
            'exposure_rows': merged_rows,
            'acceptance': merged_acceptance,
        },
        'scientific_interpretation': (
            'This is a public regional exposure sensitivity dataset. It does not '
            'open global G2 or validate BSFM 1.2.'
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('archive_dir')
    parser.add_argument('--mapping', default='data/exposure/bts-t100-cohort-mapping-v1.json')
    parser.add_argument('--start-year', type=int, default=2010)
    parser.add_argument('--end-year', type=int, default=2025)
    parser.add_argument('--output')
    args = parser.parse_args()
    report = build_report(args.archive_dir, args.mapping, args.start_year, args.end_year)
    rendered = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        Path(args.output).write_text(rendered, encoding='utf-8')
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()

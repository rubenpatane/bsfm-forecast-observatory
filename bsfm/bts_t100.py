from __future__ import annotations

from collections import Counter, defaultdict
import csv
from decimal import Decimal, InvalidOperation
import hashlib
from pathlib import Path
import zipfile


REQUIRED_FIELDS = ('YEAR', 'AIRCRAFT_TYPE', 'DEPARTURES_PERFORMED', 'CLASS')
PUBLIC_SCOPE = 'us_linked_commercial'


def _whole_nonnegative(value):
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None
    if not number.is_finite() or number < 0 or number != number.to_integral_value():
        return None
    return int(number)


def aggregate_t100_segments(
    rows,
    aircraft_type_map,
    admitted_service_classes,
    *,
    target_aircraft_types=None,
    start_year=2010,
    end_year=2025,
):
    """Aggregate an official BTS T-100 Segment CSV under a regional scope.

    T-100 rows are monthly aggregates, not individual flight legs.  The caller
    must supply reviewed DOT aircraft-type and service-class allowlists.  No
    type is inferred from its label and no generic 737 count is proxy-split.
    """
    if int(start_year) > int(end_year):
        raise ValueError('start_year must not exceed end_year')
    mapping = {str(k).strip(): str(v).strip() for k, v in aircraft_type_map.items()}
    target_types = (
        {str(value).strip() for value in target_aircraft_types}
        if target_aircraft_types is not None else set(mapping)
    )
    if not set(mapping).issubset(target_types):
        raise ValueError('mapped aircraft types must belong to the reviewed target universe')
    classes = {str(value).strip() for value in admitted_service_classes}
    if not classes:
        raise ValueError('at least one admitted service class is required')

    counts = defaultdict(int)
    unknown_types = Counter()
    diagnostics = {
        'input_rows': 0,
        'counted_rows': 0,
        'counted_departures': 0,
        'excluded_service_class_rows': 0,
        'outside_target_universe_rows': 0,
        'outside_target_universe_departures': 0,
        'out_of_range_rows': 0,
        'invalid_rows': 0,
        'zero_departure_rows': 0,
    }
    for raw in rows:
        diagnostics['input_rows'] += 1
        row = raw if isinstance(raw, dict) else {}
        if any(field not in row for field in REQUIRED_FIELDS):
            diagnostics['invalid_rows'] += 1
            continue
        year = _whole_nonnegative(row.get('YEAR'))
        departures = _whole_nonnegative(row.get('DEPARTURES_PERFORMED'))
        aircraft_type = str(row.get('AIRCRAFT_TYPE') or '').strip()
        service_class = str(row.get('CLASS') or '').strip()
        if year is None or departures is None or not aircraft_type or not service_class:
            diagnostics['invalid_rows'] += 1
            continue
        if year < int(start_year) or year > int(end_year):
            diagnostics['out_of_range_rows'] += 1
            continue
        if service_class not in classes:
            diagnostics['excluded_service_class_rows'] += 1
            continue
        if aircraft_type not in target_types:
            diagnostics['outside_target_universe_rows'] += 1
            diagnostics['outside_target_universe_departures'] += departures
            continue
        cohort = mapping.get(aircraft_type)
        if not cohort:
            unknown_types[aircraft_type] += departures
            continue
        if departures == 0:
            diagnostics['zero_departure_rows'] += 1
        counts[(year, cohort)] += departures
        diagnostics['counted_rows'] += 1
        diagnostics['counted_departures'] += departures

    exposure_rows = [
        {
            'period': str(year),
            'cohort': cohort,
            'departures': float(departures),
            'scope': PUBLIC_SCOPE,
        }
        for (year, cohort), departures in sorted(counts.items())
    ]
    return {
        'schema': 'bsfm.bts-t100-regional-exposure.v1',
        'scope': PUBLIC_SCOPE,
        'global_g2_eligible': False,
        'start_year': int(start_year),
        'end_year': int(end_year),
        'admitted_service_classes': sorted(classes),
        'exposure_rows': exposure_rows,
        'unmapped_aircraft_types': [
            {'aircraft_type': code, 'departures': value}
            for code, value in sorted(unknown_types.items())
        ],
        'diagnostics': diagnostics,
        'regional_matrix_candidate': (
            diagnostics['invalid_rows'] == 0
            and not unknown_types
            and bool(exposure_rows)
        ),
    }


def public_scope_acceptance(aggregation, expected_periods, expected_cohorts):
    """Audit public T-100 coverage without ever promoting global G2."""
    present = {
        (str(row.get('period')), str(row.get('cohort')))
        for row in aggregation.get('exposure_rows', [])
    }
    expected = {(str(y), str(c)) for y in expected_periods for c in expected_cohorts}
    missing = sorted(expected - present)
    extra = sorted(present - expected)
    regional_complete = (
        aggregation.get('scope') == PUBLIC_SCOPE
        and aggregation.get('regional_matrix_candidate') is True
        and not missing
        and not extra
    )
    return {
        'schema': 'bsfm.bts-t100-public-scope-acceptance.v1',
        'scope': PUBLIC_SCOPE,
        'regional_matrix_complete': regional_complete,
        'missing_cells': missing,
        'extra_cells': extra,
        'global_g2_status': 'BLOCKED',
        'global_g2_pass_candidate': False,
        'reason': 'T-100 excludes operations with both endpoints outside the United States.',
    }


def aggregate_t100_archive(
    archive_path,
    aircraft_type_map,
    admitted_service_classes,
    *,
    target_aircraft_types=None,
    start_year=2010,
    end_year=2025,
):
    """Read one official CSV/ZIP download and attach content provenance."""
    path = Path(archive_path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if path.suffix.lower() == '.zip':
        with zipfile.ZipFile(path) as bundle:
            members = [name for name in bundle.namelist() if name.lower().endswith('.csv')]
            if len(members) != 1:
                raise ValueError('T-100 ZIP must contain exactly one CSV member')
            member = members[0]
            with bundle.open(member) as raw:
                rows = csv.DictReader((line.decode('utf-8-sig') for line in raw))
                result = aggregate_t100_segments(
                    rows, aircraft_type_map, admitted_service_classes,
                    target_aircraft_types=target_aircraft_types,
                    start_year=start_year, end_year=end_year,
                )
    else:
        member = path.name
        with path.open(encoding='utf-8-sig', newline='') as handle:
            result = aggregate_t100_segments(
                csv.DictReader(handle), aircraft_type_map, admitted_service_classes,
                target_aircraft_types=target_aircraft_types,
                start_year=start_year, end_year=end_year,
            )
    result['artifact'] = {
        'filename': path.name,
        'csv_member': member,
        'bytes': path.stat().st_size,
        'sha256': digest,
    }
    return result

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date

from .cohorts import cohort_from_icao_equipment
from .exposure import audit_exposure


REQUIRED_FIELDS = ('flight_date', 'equipment_code', 'leg_id', 'operated', 'scope', 'vintage_id')


def _as_date(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def aggregate_standardized_flight_legs(rows, start_year=2010, end_year=2025):
    """Aggregate standardized flight-leg observations into BSFM cohort exposure.

    Input is deliberately vendor-neutral. A vendor adapter must first produce one
    row per flight leg with the required fields. Only explicitly operated,
    global-commercial rows with allowlisted ICAO equipment codes are counted.
    Unknown equipment never gets allocated by fleet share or another proxy.
    """
    if int(start_year) > int(end_year):
        raise ValueError('start_year must not exceed end_year')

    counts = defaultdict(int)
    unknown = Counter()
    seen = {}
    diagnostics = {
        'input_rows': 0,
        'counted_rows': 0,
        'not_operated_rows': 0,
        'out_of_scope_rows': 0,
        'out_of_range_rows': 0,
        'invalid_rows': 0,
        'exact_duplicate_rows': 0,
        'conflicting_duplicate_rows': 0,
    }
    vintages = set()

    for raw in rows:
        diagnostics['input_rows'] += 1
        row = raw if isinstance(raw, dict) else {}
        if any(field not in row for field in REQUIRED_FIELDS):
            diagnostics['invalid_rows'] += 1
            continue
        d = _as_date(row.get('flight_date'))
        leg_id = str(row.get('leg_id') or '').strip()
        vintage_id = str(row.get('vintage_id') or '').strip()
        if d is None or not leg_id or not vintage_id or not isinstance(row.get('operated'), bool):
            diagnostics['invalid_rows'] += 1
            continue
        vintages.add(vintage_id)
        if d.year < int(start_year) or d.year > int(end_year):
            diagnostics['out_of_range_rows'] += 1
            continue
        if row.get('scope') != 'global_commercial':
            diagnostics['out_of_scope_rows'] += 1
            continue
        if row.get('operated') is not True:
            diagnostics['not_operated_rows'] += 1
            continue

        key = (d.isoformat(), leg_id)
        signature = (
            str(row.get('equipment_code') or '').upper().strip(),
            row.get('scope'), row.get('operated'), vintage_id,
        )
        previous = seen.get(key)
        if previous is not None:
            if previous == signature:
                diagnostics['exact_duplicate_rows'] += 1
            else:
                diagnostics['conflicting_duplicate_rows'] += 1
            continue
        seen[key] = signature

        equipment = signature[0]
        cohort = cohort_from_icao_equipment(equipment)
        if cohort is None:
            unknown[equipment or '<blank>'] += 1
            continue
        counts[(d.year, cohort)] += 1
        diagnostics['counted_rows'] += 1

    exposure_rows = [
        {'year': year, 'cohort': cohort, 'departures': float(value)}
        for (year, cohort), value in sorted(counts.items())
    ]
    return {
        'schema': 'bsfm.standardized-flight-exposure.v1',
        'start_year': int(start_year),
        'end_year': int(end_year),
        'exposure_rows': exposure_rows,
        'unknown_equipment': [{'equipment_code': code, 'rows': n} for code, n in sorted(unknown.items())],
        'vintage_ids': sorted(vintages),
        'diagnostics': diagnostics,
        'complete_for_g2': (
            diagnostics['invalid_rows'] == 0
            and diagnostics['conflicting_duplicate_rows'] == 0
            and not unknown
            and bool(exposure_rows)
        ),
    }


def g2_acceptance_report(rows, expected_periods, expected_cohorts, *, source, provenance, vintage_policy_id):
    """Run the canonical G2 matrix audit on standardized flight-leg observations."""
    source = str(source or '').strip()
    provenance = str(provenance or '').strip()
    vintage_policy_id = str(vintage_policy_id or '').strip()
    if not source or not provenance or not vintage_policy_id:
        raise ValueError('source, provenance and vintage_policy_id are required')
    periods = [int(p) for p in expected_periods]
    if not periods:
        raise ValueError('expected_periods required')
    aggregated = aggregate_standardized_flight_legs(rows, min(periods), max(periods))
    canonical = [
        {
            'period': str(row['year']),
            'cohort': row['cohort'],
            'departures': row['departures'],
            'source': source,
            'scope': 'global_commercial',
            'provenance': provenance,
            'vintage_policy_id': vintage_policy_id,
            'source_vintage_ids': aggregated['vintage_ids'],
        }
        for row in aggregated['exposure_rows']
    ]
    matrix = audit_exposure(canonical, periods, expected_cohorts)
    pass_candidate = aggregated['complete_for_g2'] and matrix['complete']
    return {
        'schema': 'bsfm.g2-acceptance-report.v1',
        'source': source,
        'provenance': provenance,
        'vintage_policy_id': vintage_policy_id,
        'import': aggregated,
        'canonical_exposure_rows': canonical,
        'matrix_audit': matrix,
        'g2_pass_candidate': pass_candidate,
        'g2_status': 'CANDIDATE_PASS' if pass_candidate else 'BLOCKED',
    }

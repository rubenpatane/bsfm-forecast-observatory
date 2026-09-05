from __future__ import annotations
from collections import defaultdict

REQUIRED_META = ('source', 'scope', 'provenance')


def validate_exposure(rows, require_metadata=False):
    errors = []; seen = set(); total = 0.0; scopes = set()
    for i, row in enumerate(rows):
        key = (row.get('period'), row.get('cohort'))
        if not all(key): errors.append(f'missing_period_or_cohort:{i}')
        if key in seen: errors.append(f'duplicate:{key}')
        seen.add(key)
        try: value = float(row['departures'])
        except (KeyError, TypeError, ValueError):
            errors.append(f'invalid_departures:{i}'); continue
        if value < 0: errors.append(f'negative_departures:{i}')
        total += max(value, 0.0)
        if require_metadata:
            for field in REQUIRED_META:
                if not str(row.get(field, '')).strip(): errors.append(f'missing_{field}:{i}')
            scope = str(row.get('scope', '')).strip()
            if scope: scopes.add(scope)
    if require_metadata and len(scopes) > 1: errors.append('mixed_scopes')
    return {'valid': not errors, 'errors': errors, 'total_departures': total, 'scopes': sorted(scopes)}


def audit_exposure(rows, expected_periods, expected_cohorts):
    rows = list(rows); base = validate_exposure(rows, require_metadata=True)
    present = {(str(r.get('period')), str(r.get('cohort'))) for r in rows}
    expected = {(str(p), str(c)) for p in expected_periods for c in expected_cohorts}
    missing = sorted(expected - present); extra = sorted(present - expected)
    period_totals = defaultdict(float)
    for r in rows:
        try: period_totals[str(r.get('period'))] += max(float(r.get('departures')), 0.0)
        except (TypeError, ValueError): pass
    zero_periods = sorted(str(p) for p in expected_periods if period_totals[str(p)] <= 0)
    return {**base, 'complete': base['valid'] and not missing and not extra and not zero_periods,
            'missing_cells': missing, 'extra_cells': extra, 'zero_departure_periods': zero_periods,
            'period_totals': dict(period_totals)}


def audit_target_universe_exposure(target_cohorts, exposure_cohorts, excluded_cohorts=()):
    """Fail closed when target-eligible cohorts lack exposure or explicit exclusion.

    An excluded cohort must be justified by a separately versioned/preregistered
    rule; this function only audits the set relation and never invents exclusions.
    """
    target = {str(x) for x in target_cohorts if str(x).strip()}
    exposure = {str(x) for x in exposure_cohorts if str(x).strip()}
    excluded = {str(x) for x in excluded_cohorts if str(x).strip()}
    uncovered = sorted(target - exposure - excluded)
    unknown_exposure = sorted(exposure - target)
    overlap = sorted(exposure & excluded)
    errors = []
    if uncovered: errors.append('target_cohorts_without_exposure_or_exclusion')
    if overlap: errors.append('cohort_both_exposed_and_excluded')
    return {
        'complete': not errors,
        'errors': errors,
        'target_cohorts': sorted(target),
        'exposure_cohorts': sorted(exposure),
        'excluded_cohorts': sorted(excluded),
        'uncovered_target_cohorts': uncovered,
        'extra_exposure_cohorts': unknown_exposure,
        'exposed_and_excluded': overlap,
    }


def exposure_only_probabilities(rows):
    rows = list(rows); audit = validate_exposure(rows)
    if not audit['valid']: raise ValueError('valid non-negative departures exposure required')
    totals = defaultdict(float)
    for row in rows: totals[str(row['period'])] += float(row['departures'])
    if any(v <= 0 for v in totals.values()): raise ValueError('each period requires positive departures exposure')
    return [{**row, 'baseline_probability': float(row['departures']) / totals[str(row['period'])]} for row in rows]

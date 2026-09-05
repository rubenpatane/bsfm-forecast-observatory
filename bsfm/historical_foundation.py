from __future__ import annotations

from datetime import date, timedelta

HORIZONS = (365, 90, 30, 7)


def build_walk_forward_cases(targets, start_year=2010, end_year=2025):
    """Build immutable target/cutoff descriptors without fitting a model.

    Only already-qualified census rows belong here. Outcome truth may be
    finalised after the event, but predictors are admitted separately by the
    point-in-time availability gate.
    """
    ordered = sorted(targets, key=lambda r: r['event_date'])
    cases = []
    for row in ordered:
        event = date.fromisoformat(str(row['event_date'])[:10])
        if not start_year <= event.year <= end_year:
            continue
        for horizon in HORIZONS:
            cutoff = event - timedelta(days=horizon)
            cases.append({
                'target_event_date': event.isoformat(),
                'cutoff': cutoff.isoformat(),
                'horizon_days': horizon,
                'manufacturer': row['manufacturer'],
                'model': row['model'],
            })
    return cases


def audit_historical_foundation(census_audit, exposure_audit, availability_audit=None):
    """Single fail-closed readiness report for historical model evaluation."""
    availability_audit = availability_audit or {}
    historical_cases = census_audit.get('complete') is True
    baseline_present = exposure_audit.get('complete') is True
    point_in_time = availability_audit.get('point_in_time_availability_verified') is True
    leakage_free = availability_audit.get('leakage_free') is True
    ready = historical_cases and baseline_present and point_in_time and leakage_free
    return {
        'historical_cases': historical_cases,
        'baseline_present': baseline_present,
        'point_in_time_availability_verified': point_in_time,
        'leakage_free': leakage_free,
        'ready_for_candidate_fit': ready,
        'blocked_reasons': [
            name for name, ok in (
                ('historical_cases', historical_cases),
                ('baseline_present', baseline_present),
                ('point_in_time_availability_verified', point_in_time),
                ('leakage_free', leakage_free),
            ) if not ok
        ],
    }

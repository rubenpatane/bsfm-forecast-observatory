"""Frozen exploratory temporal backtest for the BSFM-PD 1.3 model line."""

from __future__ import annotations

import calendar
from datetime import date, timedelta
from typing import Any

from .estimator import fit_shrunk_hazard
from .temporal import exposure_only_baseline, temporal_log_score, time_to_event_distribution


def seasonal_naive_daily_path(monthly_rows, cohorts, start_date, horizon_days, cutoff, publication_lag_days=365):
    """Build a daily path from the latest eligible same-month T-100 cell.

    Monthly totals are divided uniformly among source-month civil days. The
    same per-day value is used for the forecast calendar month. A source month
    is eligible only after its month end plus the frozen conservative lag.
    """
    start = date.fromisoformat(str(start_date)[:10])
    cutoff_date = date.fromisoformat(str(cutoff)[:10])
    values = {(str(r['period']), str(r['cohort'])): float(r['departures']) for r in monthly_rows}
    periods = sorted({str(r['period']) for r in monthly_rows})
    if not periods:
        raise ValueError('monthly exposure required')
    rows = []
    for index in range(int(horizon_days)):
        target = start + timedelta(days=index)
        eligible = []
        for period in periods:
            year, month = map(int, period.split('-'))
            if month != target.month:
                continue
            month_end = date(year, month, calendar.monthrange(year, month)[1])
            if month_end + timedelta(days=int(publication_lag_days)) <= cutoff_date:
                eligible.append((year, period))
        if not eligible:
            raise ValueError(f'no PIT-eligible seasonal reference for {target:%Y-%m}')
        _, source_period = max(eligible)
        source_year, source_month = map(int, source_period.split('-'))
        source_days = calendar.monthrange(source_year, source_month)[1]
        rows.append({
            'date': target.isoformat(),
            'exposure_by_cohort': {c: values.get((source_period, c), 0.0) / source_days for c in cohorts},
            'source_period': source_period,
        })
    return rows


def run_exploratory_backtest(events, annual_rows, monthly_rows, cohorts, spec):
    """Run fixed non-overlapping folds and report, but never overclaim, power."""
    cadence = int(spec['validation_protocol']['fold_step_days'])
    horizon = int(spec['forecast_horizon_days'])
    if cadence < horizon:
        raise ValueError('overlapping folds are prohibited by this protocol')
    start = date.fromisoformat(spec['validation_protocol']['first_fold_start'])
    end = date.fromisoformat(spec['validation_protocol']['last_observation_date'])
    lag = int(spec['temporal_exposure_rule']['publication_lag_days'])
    event_rows = sorted(events, key=lambda row: row['event_date'])
    folds: list[dict[str, Any]] = []
    cursor = start
    while cursor + timedelta(days=horizon - 1) <= end:
        cutoff = cursor - timedelta(days=1)
        training_events = [r for r in event_rows if date.fromisoformat(r['available_at']) <= cutoff]
        training_exposure = []
        for row in annual_rows:
            year = int(row['period'])
            if date(year, 12, 31) + timedelta(days=lag) <= cutoff:
                training_exposure.append(row)
        if training_exposure:
            future = seasonal_naive_daily_path(monthly_rows, cohorts, cursor, horizon, cutoff, lag)
            candidate = fit_shrunk_hazard(training_events, training_exposure, cohorts)
            baseline = exposure_only_baseline(
                len(training_events), sum(float(r['departures']) for r in training_exposure), cohorts,
            )
            cdist = time_to_event_distribution(candidate, future, cursor, horizon)
            bdist = time_to_event_distribution(baseline, future, cursor, horizon)
            horizon_end = cursor + timedelta(days=horizon - 1)
            observed = next((r for r in event_rows if cutoff < date.fromisoformat(r['event_date']) <= horizon_end), None)
            observed_date = observed['event_date'] if observed else None
            folds.append({
                'case_id': f'PD13-{cursor.isoformat()}', 'cutoff': cutoff.isoformat(),
                'horizon_end': horizon_end.isoformat(), 'observed_event_id': observed['event_id'] if observed else None,
                'observed_date': observed_date, 'candidate_log_score': temporal_log_score(cdist, observed_date),
                'baseline_log_score': temporal_log_score(bdist, observed_date),
            })
        cursor += timedelta(days=cadence)
    event_folds = sum(row['observed_event_id'] is not None for row in folds)
    cmean = sum(r['candidate_log_score'] for r in folds) / len(folds)
    bmean = sum(r['baseline_log_score'] for r in folds) / len(folds)
    minimum = int(spec['validation_protocol']['minimum_event_bearing_folds'])
    return {
        'schema': 'bsfm.public-data-exploratory-backtest.v1', 'status': 'EXPLORATORY_COMPLETE',
        'scientific_validation': 'PASS' if event_folds >= minimum else 'BLOCKED_INSUFFICIENT_EVENT_FOLDS',
        'fold_count': len(folds), 'event_bearing_fold_count': event_folds,
        'minimum_event_bearing_folds': minimum, 'candidate_mean_log_score': cmean,
        'baseline_mean_log_score': bmean, 'mean_log_score_improvement': bmean - cmean,
        'candidate_better_descriptive': cmean < bmean, 'folds': folds,
        'claim_limit': 'Descriptive execution does not establish predictive validity when the frozen minimum event-fold rule is unmet.',
    }

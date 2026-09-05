from __future__ import annotations

from collections import defaultdict


def fit_shrunk_hazard(events, exposure_rows, cohorts, alpha=0.5, prior_departures=1_000_000.0):
    """Fit a conservative Gamma-Poisson-style cohort hazard estimator.

    The estimator is intentionally small-data oriented. It estimates fatal-event
    hazard per departure with common pseudo-exposure shrinkage. It does not run
    unless callers have already passed the historical fit gate; this function
    itself accepts no current/prospective source snapshots.
    """
    cohorts=tuple(str(c) for c in cohorts)
    if not cohorts:
        raise ValueError('cohorts required')
    if alpha <= 0 or prior_departures <= 0:
        raise ValueError('positive shrinkage parameters required')
    counts=defaultdict(int); departures=defaultdict(float)
    for row in events:
        cohort=str(row.get('cohort',''))
        if cohort not in cohorts:
            raise ValueError(f'unknown event cohort: {cohort}')
        counts[cohort]+=1
    for row in exposure_rows:
        cohort=str(row.get('cohort',''))
        if cohort not in cohorts:
            raise ValueError(f'unknown exposure cohort: {cohort}')
        value=float(row.get('departures',-1))
        if value < 0:
            raise ValueError('departures must be non-negative')
        departures[cohort]+=value
    if sum(departures.values()) <= 0:
        raise ValueError('positive exposure required')
    rates={c:(counts[c]+alpha)/(departures[c]+prior_departures) for c in cohorts}
    return {
        'schema':'bsfm.shrunk-hazard-model.v1',
        'cohorts':list(cohorts),
        'alpha':float(alpha),
        'prior_departures':float(prior_departures),
        'event_counts':dict(counts),
        'departures':{c:departures[c] for c in cohorts},
        'rates_per_departure':rates,
    }


def predict_cohort(model, exposure_by_cohort):
    """Predict the cohort of the next target event as a probability simplex."""
    cohorts=model['cohorts']; rates=model['rates_per_departure']
    weights={}
    for cohort in cohorts:
        exposure=float(exposure_by_cohort.get(cohort,0.0))
        if exposure < 0:
            raise ValueError('future exposure must be non-negative')
        weights[cohort]=float(rates[cohort])*exposure
    total=sum(weights.values())
    if total <= 0:
        raise ValueError('positive prediction exposure required')
    return {c:weights[c]/total for c in cohorts}

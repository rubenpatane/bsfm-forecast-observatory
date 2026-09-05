from __future__ import annotations

from .estimator import fit_shrunk_hazard,predict_cohort
from .walk_forward import eligible_snapshot,score_multiclass


def run_oos_case(case, training_events, training_exposure, prediction_exposure, cohorts):
    """Run one leakage-safe historical cohort forecast.

    All supplied predictor/training rows must carry verified public availability.
    Rows not available at cutoff are rejected rather than silently filtered so a
    caller cannot mistake a partial snapshot for the intended training set.
    """
    cutoff=case['cutoff']; cohorts=tuple(cohorts)
    collections=(list(training_events),list(training_exposure),list(prediction_exposure))
    for rows in collections:
        if len(eligible_snapshot(rows,cutoff)) != len(rows):
            raise ValueError('unverified_or_future_row_in_oos_case')
    model=fit_shrunk_hazard(collections[0],collections[1],cohorts)
    future={str(r['cohort']):float(r['departures']) for r in collections[2]}
    if set(future)!=set(cohorts):
        raise ValueError('prediction exposure must cover every cohort exactly once')
    probabilities=predict_cohort(model,future)
    observed=str(case['observed_cohort'])
    return {
        'case_id':case['case_id'],'cutoff':cutoff,'observed_cohort':observed,
        'probabilities':probabilities,
        'multiclass_brier':score_multiclass(probabilities,observed),
    }

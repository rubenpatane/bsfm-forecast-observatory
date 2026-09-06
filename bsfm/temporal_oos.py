from __future__ import annotations

from datetime import date

from .estimator import fit_shrunk_hazard
from .temporal import exposure_only_baseline, paired_temporal_evaluation, time_to_event_distribution
from .walk_forward import eligible_snapshot


def run_temporal_oos_case(case, cohorts):
    """Refit candidate and baseline at one historical cutoff, then forecast."""
    required={'case_id','cutoff','outcome_available_at','historical_public_availability','training_events','training_exposure','future_daily_exposure'}
    missing=sorted(required-set(case))
    if missing:
        raise ValueError(f'incomplete temporal OOS case: {missing}')
    cutoff=str(case['cutoff'])[:10]
    if case['historical_public_availability']!='verified':
        raise ValueError('unverified outcome availability')
    if date.fromisoformat(str(case['outcome_available_at'])[:10]) <= date.fromisoformat(cutoff):
        raise ValueError('outcome must be published after cutoff')
    events=list(case['training_events']); exposure=list(case['training_exposure'])
    if len(eligible_snapshot(events,cutoff))!=len(events) or len(eligible_snapshot(exposure,cutoff))!=len(exposure):
        raise ValueError('unverified_or_future_training_row')
    future=list(case['future_daily_exposure'])
    if not future:
        raise ValueError('future exposure required')
    candidate=fit_shrunk_hazard(events,exposure,cohorts)
    baseline=exposure_only_baseline(len(events),sum(float(x['departures']) for x in exposure),cohorts)
    start=future[0]['date']
    candidate_distribution=time_to_event_distribution(candidate,future,start,len(future))
    baseline_distribution=time_to_event_distribution(baseline,future,start,len(future))
    return {'case_id':case['case_id'],'cutoff':cutoff,'outcome_available_at':case['outcome_available_at'],'historical_public_availability':'verified','observed_date':case.get('observed_date'),'candidate_distribution':candidate_distribution,'baseline_distribution':baseline_distribution}


def run_temporal_walk_forward(cases, cohorts):
    """Generate and score every declared fold; one invalid fold closes evaluation."""
    rows=[]
    try:
        for case in cases:
            rows.append(run_temporal_oos_case(case,cohorts))
    except (KeyError,TypeError,ValueError) as exc:
        return {'evaluated':False,'reason':'invalid_oos_fold','detail':str(exc),'n':len(rows)}
    return paired_temporal_evaluation(rows)

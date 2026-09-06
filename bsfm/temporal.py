from __future__ import annotations

from datetime import date, timedelta
from math import exp, log


def _daily_hazard(model, exposure):
    rates=model['rates_per_departure']; cohorts=tuple(model['cohorts'])
    unknown=set(exposure)-set(cohorts)
    if unknown:
        raise ValueError(f'unknown exposure cohorts: {sorted(unknown)}')
    values={c:float(exposure.get(c,0.0)) for c in cohorts}
    if any(v < 0 for v in values.values()):
        raise ValueError('daily exposure must be non-negative')
    return sum(float(rates[c])*values[c] for c in cohorts)


def time_to_event_distribution(model, daily_exposure, start_date, horizon_days=None):
    """Discrete first-event distribution from a frozen hazard and exposure path.

    Each input row represents exposure during one civil day. The returned daily
    probabilities plus ``no_event_probability`` form a complete simplex over the
    declared horizon. No extrapolation or post-hoc smoothing is performed.
    """
    start=date.fromisoformat(str(start_date)[:10]); rows=list(daily_exposure)
    if horizon_days is None:
        horizon_days=len(rows)
    horizon_days=int(horizon_days)
    if horizon_days <= 0 or len(rows)!=horizon_days:
        raise ValueError('daily exposure must exactly cover the forecast horizon')
    survival=1.0; distribution=[]
    for index,row in enumerate(rows):
        expected=start+timedelta(days=index)
        if str(row.get('date',''))[:10] != expected.isoformat():
            raise ValueError('daily exposure dates must be consecutive from start_date')
        hazard=_daily_hazard(model,row.get('exposure_by_cohort',{}))
        probability=survival*(1.0-exp(-hazard))
        distribution.append({'date':expected.isoformat(),'hazard':hazard,'probability':probability})
        survival*=exp(-hazard)
    total=1.0-survival
    modal=max(distribution,key=lambda r:(r['probability'],r['date']))['date'] if total>0 else None
    return {
        'schema':'bsfm.time-to-event-distribution.v1',
        'start_date':start.isoformat(),'horizon_days':horizon_days,
        'daily':distribution,'event_probability':total,
        'no_event_probability':survival,'modal_date':modal,
        'conditional_interval_80':_conditional_interval(distribution,total,0.1,0.9),
    }


def _conditional_interval(distribution,total,lower,upper):
    if total <= 0:
        return None
    cumulative=0.0; lo=hi=None
    for row in distribution:
        cumulative+=row['probability']/total
        if lo is None and cumulative>=lower:
            lo=row['date']
        if cumulative>=upper:
            hi=row['date']; break
    return {'lower':lo,'upper':hi,'coverage':upper-lower,'conditional_on_event_within_horizon':True}


def temporal_log_score(distribution, observed_date=None):
    """Log score for the full horizon, including right-censoring/no event."""
    if observed_date is None:
        probability=float(distribution['no_event_probability'])
    else:
        target=str(observed_date)[:10]
        probability=next((float(x['probability']) for x in distribution['daily'] if x['date']==target),0.0)
    return -log(max(probability,1e-15))


def exposure_only_baseline(training_events, training_departures, cohorts):
    """Pooled exposure-only comparator with no precursor differentiation."""
    cohorts=tuple(str(c) for c in cohorts); departures=float(training_departures)
    if not cohorts or departures <= 0 or int(training_events) < 0:
        raise ValueError('valid pooled training totals and cohorts required')
    rate=(int(training_events)+0.5)/(departures+1_000_000.0)
    return {'schema':'bsfm.exposure-only-temporal-baseline.v1','cohorts':list(cohorts),'rates_per_departure':{c:rate for c in cohorts},'training_events':int(training_events),'training_departures':departures}


def paired_temporal_evaluation(cases):
    """Evaluate frozen candidate/baseline distributions on identical OOS cases."""
    rows=list(cases)
    if not rows:
        return {'evaluated':False,'reason':'no_cases','n':0}
    paired=[]; seen=set()
    for case in rows:
        required={'case_id','cutoff','outcome_available_at','historical_public_availability','candidate_distribution','baseline_distribution'}
        if required-set(case):
            return {'evaluated':False,'reason':'incomplete_case','n':len(rows)}
        case_id=str(case['case_id'])
        if not case_id or case_id in seen:
            return {'evaluated':False,'reason':'duplicate_or_empty_case_id','n':len(rows)}
        seen.add(case_id)
        if case['historical_public_availability']!='verified':
            return {'evaluated':False,'reason':'unverified_case_availability','n':len(rows)}
        cutoff=date.fromisoformat(str(case['cutoff'])[:10]); available=date.fromisoformat(str(case['outcome_available_at'])[:10])
        if available <= cutoff:
            return {'evaluated':False,'reason':'outcome_not_strictly_after_cutoff','n':len(rows)}
        candidate=case['candidate_distribution']; baseline=case['baseline_distribution']
        candidate_dates=[x['date'] for x in candidate.get('daily',[])]
        baseline_dates=[x['date'] for x in baseline.get('daily',[])]
        if not candidate_dates or candidate_dates!=baseline_dates:
            return {'evaluated':False,'reason':'unpaired_horizon','n':len(rows)}
        observed=case.get('observed_date')
        if observed is not None and not (cutoff < date.fromisoformat(str(observed)[:10]) <= date.fromisoformat(candidate_dates[-1])):
            return {'evaluated':False,'reason':'observed_date_outside_oos_horizon','n':len(rows)}
        paired.append({'case_id':case_id,'candidate_log_score':temporal_log_score(candidate,observed),'baseline_log_score':temporal_log_score(baseline,observed)})
    candidate_mean=sum(x['candidate_log_score'] for x in paired)/len(paired)
    baseline_mean=sum(x['baseline_log_score'] for x in paired)/len(paired)
    return {'evaluated':True,'n':len(paired),'cases':paired,'candidate_mean_log_score':candidate_mean,'baseline_mean_log_score':baseline_mean,'mean_log_score_improvement':baseline_mean-candidate_mean,'candidate_better':candidate_mean<baseline_mean}

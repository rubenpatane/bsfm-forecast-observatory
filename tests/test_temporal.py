import pytest

from bsfm.temporal import exposure_only_baseline, paired_temporal_evaluation, parameter_uncertainty, temporal_log_score, time_to_event_distribution


def model():
    return {'cohorts':['737-NG','777'],'rates_per_departure':{'737-NG':2e-5,'777':1e-5}}


def path(n=3):
    return [{'date':f'2026-10-0{i+1}','exposure_by_cohort':{'737-NG':1000,'777':500}} for i in range(n)]


def test_temporal_distribution_is_complete_and_reproducible():
    result=time_to_event_distribution(model(),path(),'2026-10-01')
    assert sum(x['probability'] for x in result['daily'])+result['no_event_probability']==pytest.approx(1.0)
    assert result['modal_date']=='2026-10-01'
    assert result==time_to_event_distribution(model(),path(),'2026-10-01')
    assert result['conditional_interval_80']['conditional_on_event_within_horizon'] is True


def test_temporal_distribution_requires_exact_consecutive_exposure_path():
    bad=path(); bad[1]['date']='2026-10-04'
    with pytest.raises(ValueError,match='consecutive'):
        time_to_event_distribution(model(),bad,'2026-10-01')


def test_log_score_includes_no_event_and_baseline_is_pooled():
    dist=time_to_event_distribution(model(),path(),'2026-10-01')
    assert temporal_log_score(dist)>0
    assert temporal_log_score(dist,'2026-10-01')>0
    baseline=exposure_only_baseline(2,1_000_000,['737-NG','777'])
    assert baseline['rates_per_departure']['737-NG']==baseline['rates_per_departure']['777']


def test_exposure_only_baseline_accepts_explicit_versioned_prior():
    baseline=exposure_only_baseline(
        0, 9_000_000, ['737-NG','777'], alpha=4.5, prior_departures=9_000_000,
    )
    assert baseline['alpha']==4.5
    assert baseline['prior_departures']==9_000_000
    assert baseline['rates_per_departure']['737-NG']==4.5/18_000_000


def test_paired_temporal_evaluation_requires_verified_future_outcomes():
    dist=time_to_event_distribution(model(),path(),'2026-10-01')
    case={'case_id':'x','cutoff':'2026-09-30','outcome_available_at':'2026-10-05','historical_public_availability':'verified','observed_date':'2026-10-02','candidate_distribution':dist,'baseline_distribution':dist}
    report=paired_temporal_evaluation([case])
    assert report['evaluated'] and report['n']==1 and not report['candidate_better']
    case['historical_public_availability']='unknown'
    assert paired_temporal_evaluation([case])['reason']=='unverified_case_availability'


def test_parameter_uncertainty_is_reproducible_and_ordered():
    fitted={'cohorts':['737-NG','777'],'event_counts':{'737-NG':2},'departures':{'737-NG':100000,'777':200000},'alpha':0.5,'prior_departures':1000000}
    a=parameter_uncertainty(fitted,path(),'2026-10-01',samples=100,seed=7)
    b=parameter_uncertainty(fitted,path(),'2026-10-01',samples=100,seed=7)
    assert a==b
    q=a['horizon_event_probability']; assert q['p10']<=q['p50']<=q['p90']

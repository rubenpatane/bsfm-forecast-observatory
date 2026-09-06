import pytest

from bsfm.temporal import exposure_only_baseline, paired_temporal_evaluation, temporal_log_score, time_to_event_distribution


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


def test_paired_temporal_evaluation_requires_verified_future_outcomes():
    dist=time_to_event_distribution(model(),path(),'2026-10-01')
    case={'case_id':'x','cutoff':'2026-09-30','outcome_available_at':'2026-10-05','historical_public_availability':'verified','observed_date':'2026-10-02','candidate_distribution':dist,'baseline_distribution':dist}
    report=paired_temporal_evaluation([case])
    assert report['evaluated'] and report['n']==1 and not report['candidate_better']
    case['historical_public_availability']='unknown'
    assert paired_temporal_evaluation([case])['reason']=='unverified_case_availability'

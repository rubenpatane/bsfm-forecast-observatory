import pytest

from bsfm.oos import run_oos_case


def row(cohort,departures=None,available='2019-01-01'):
    r={'cohort':cohort,'historical_public_availability':'verified','available_at':available}
    if departures is not None:r['departures']=departures
    return r


def test_oos_case_runs_only_from_verified_point_in_time_inputs():
    case={'case_id':'x','cutoff':'2020-01-01','observed_cohort':'737-NG'}
    result=run_oos_case(case,[row('737-NG')],[row('737-NG',1000),row('777',1000)],[row('737-NG',1000),row('777',1000)],['737-NG','777'])
    assert result['case_id']=='x'
    assert sum(result['probabilities'].values())==pytest.approx(1.0)
    assert result['multiclass_brier']>=0


def test_oos_case_rejects_future_or_unverified_rows():
    case={'case_id':'x','cutoff':'2020-01-01','observed_cohort':'777'}
    with pytest.raises(ValueError,match='unverified_or_future'):
        run_oos_case(case,[],[row('777',1000,'2021-01-01')],[row('777',1000)],['777'])


def test_oos_case_rejects_duplicate_or_incomplete_prediction_exposure():
    case={'case_id':'x','cutoff':'2020-01-01','observed_cohort':'777'}
    training=[row('777',1000),row('737-NG',1000)]
    with pytest.raises(ValueError,match='exactly once'):
        run_oos_case(case,[],training,[row('777',1000),row('777',1000)],['777','737-NG'])

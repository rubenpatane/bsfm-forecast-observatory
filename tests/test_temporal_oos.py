from bsfm.temporal_oos import run_temporal_oos_case, run_temporal_walk_forward


def row(cohort,departures=None):
    value={'cohort':cohort,'historical_public_availability':'verified','available_at':'2019-01-01'}
    if departures is not None:value['departures']=departures
    return value


def case():
    return {'case_id':'fold-2020','cutoff':'2020-01-01','outcome_available_at':'2020-01-10','historical_public_availability':'verified','observed_date':'2020-01-03','training_events':[row('737-NG')],'training_exposure':[row('737-NG',100000),row('777',100000)],'future_daily_exposure':[{'date':f'2020-01-0{i}','exposure_by_cohort':{'737-NG':1000,'777':1000}} for i in range(2,10)]}


def test_temporal_oos_refits_candidate_and_baseline_at_each_cutoff():
    result=run_temporal_oos_case(case(),['737-NG','777'])
    assert result['candidate_distribution']['start_date']=='2020-01-02'
    assert result['candidate_distribution']['daily']==result['candidate_distribution']['daily']
    report=run_temporal_walk_forward([case()],['737-NG','777'])
    assert report['evaluated'] and report['n']==1


def test_temporal_oos_fails_closed_on_future_training_data():
    bad=case(); bad['training_events'][0]['available_at']='2020-02-01'
    report=run_temporal_walk_forward([bad],['737-NG','777'])
    assert not report['evaluated'] and report['reason']=='invalid_oos_fold'

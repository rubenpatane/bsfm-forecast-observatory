import pytest

from bsfm.walk_forward import eligible_snapshot, score_multiclass, evaluate_walk_forward, compare_candidate_to_baseline


def test_eligible_snapshot_requires_verified_public_availability():
    rows=[
        {'id':'ok','historical_public_availability':'verified','available_at':'2020-01-01'},
        {'id':'late','historical_public_availability':'verified','available_at':'2020-02-01'},
        {'id':'unknown','historical_public_availability':'unverified','available_at':'2019-01-01'},
        {'id':'missing','historical_public_availability':'verified'},
    ]
    assert [r['id'] for r in eligible_snapshot(rows,'2020-01-15')]==['ok']


def test_multiclass_brier_requires_probability_simplex():
    assert score_multiclass({'737NG':0.7,'MAX':0.3},'737NG') == pytest.approx(0.18)
    with pytest.raises(ValueError):
        score_multiclass({'737NG':0.7,'MAX':0.4},'737NG')


def test_walk_forward_report_and_paired_baseline_comparison():
    candidate=[{'case_id':'a','probability':0.8,'outcome':1},{'case_id':'b','probability':0.2,'outcome':0}]
    baseline=[{'case_id':'a','probability':0.5,'outcome':1},{'case_id':'b','probability':0.5,'outcome':0}]
    report=evaluate_walk_forward(candidate)
    assert report['evaluated'] and report['n']==2 and report['brier']==pytest.approx(0.04)
    comparison=compare_candidate_to_baseline(candidate,baseline)
    assert comparison['comparable'] and comparison['candidate_better']
    assert comparison['brier_improvement']==pytest.approx(0.21)


def test_comparison_fails_closed_on_unpaired_cases_or_outcomes():
    c=[{'case_id':'a','probability':0.8,'outcome':1}]
    assert not compare_candidate_to_baseline(c,[])['comparable']
    b=[{'case_id':'a','probability':0.5,'outcome':0}]
    assert compare_candidate_to_baseline(c,b)['reason']=='outcome_mismatch'


def test_prediction_rows_fail_closed_on_duplicate_case_ids():
    duplicate=[{'case_id':'a','probability':0.8,'outcome':1},{'case_id':'a','probability':0.7,'outcome':1}]
    report=evaluate_walk_forward(duplicate)
    assert not report['evaluated'] and report['reason']=='duplicate_or_empty_case_id'
    assert compare_candidate_to_baseline(duplicate,duplicate)['reason']=='duplicate_or_empty_case_id'


def test_prediction_rows_fail_closed_on_invalid_probability_or_outcome():
    assert evaluate_walk_forward([{'case_id':'a','probability':1.2,'outcome':1}])['reason']=='invalid_probability'
    assert evaluate_walk_forward([{'case_id':'a','probability':0.2,'outcome':2}])['reason']=='invalid_outcome'

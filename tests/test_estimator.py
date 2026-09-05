import pytest

from bsfm.estimator import fit_shrunk_hazard,predict_cohort


def test_shrunk_hazard_returns_finite_rates_for_zero_event_cohort():
    model=fit_shrunk_hazard(
        [{'cohort':'737-NG'}],
        [{'cohort':'737-NG','departures':2_000_000},{'cohort':'777','departures':1_000_000}],
        ['737-NG','777'],
    )
    assert model['rates_per_departure']['777'] > 0
    assert model['rates_per_departure']['737-NG'] > model['rates_per_departure']['777']


def test_prediction_is_probability_simplex_and_uses_exposure():
    model=fit_shrunk_hazard([], [
        {'cohort':'737-NG','departures':1_000_000},
        {'cohort':'777','departures':1_000_000},
    ], ['737-NG','777'])
    p=predict_cohort(model,{'737-NG':2_000_000,'777':1_000_000})
    assert sum(p.values())==pytest.approx(1.0)
    assert p['737-NG'] > p['777']


def test_estimator_rejects_unknown_cohorts_and_missing_exposure():
    with pytest.raises(ValueError):
        fit_shrunk_hazard([{'cohort':'787'}],[{'cohort':'777','departures':1}],['777'])
    with pytest.raises(ValueError):
        fit_shrunk_hazard([],[],['777'])

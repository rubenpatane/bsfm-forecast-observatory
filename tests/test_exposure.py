import pytest
from bsfm.exposure import validate_exposure,exposure_only_probabilities

def test_departure_probabilities_sum_to_one():
 rows=[{'period':'2024','cohort':'737NG','departures':3},{'period':'2024','cohort':'787','departures':1}]
 out=exposure_only_probabilities(rows)
 assert sum(r['baseline_probability'] for r in out)==1
 assert out[0]['baseline_probability']==0.75

def test_duplicate_and_negative_exposure_fail():
 rows=[{'period':'2024','cohort':'737NG','departures':1},{'period':'2024','cohort':'737NG','departures':-1}]
 assert not validate_exposure(rows)['valid']
 with pytest.raises(ValueError): exposure_only_probabilities(rows)

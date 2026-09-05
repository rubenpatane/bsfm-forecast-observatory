import pytest
from bsfm.exposure import validate_exposure,exposure_only_probabilities,audit_exposure

def test_departure_probabilities_sum_to_one():
 rows=[{'period':'2024','cohort':'737NG','departures':3},{'period':'2024','cohort':'787','departures':1}]
 out=exposure_only_probabilities(rows)
 assert sum(r['baseline_probability'] for r in out)==1
 assert out[0]['baseline_probability']==0.75

def test_duplicate_and_negative_exposure_fail():
 rows=[{'period':'2024','cohort':'737NG','departures':1},{'period':'2024','cohort':'737NG','departures':-1}]
 assert not validate_exposure(rows)['valid']
 with pytest.raises(ValueError): exposure_only_probabilities(rows)

def test_scientific_exposure_audit_requires_full_grid_and_metadata():
 rows=[{'period':'2024','cohort':'737NG','departures':3,'source':'IATA','scope':'global-commercial'}, {'period':'2024','cohort':'787','departures':1,'source':'IATA','scope':'global-commercial'}]
 assert audit_exposure(rows,['2024'],['737NG','787'])['complete']
 assert not audit_exposure(rows,['2024','2025'],['737NG','787'])['complete']

def test_scientific_exposure_audit_rejects_mixed_scope():
 rows=[{'period':'2024','cohort':'737NG','departures':3,'source':'A','scope':'global'}, {'period':'2024','cohort':'787','departures':1,'source':'B','scope':'US-only'}]
 audit=audit_exposure(rows,['2024'],['737NG','787'])
 assert not audit['complete'] and 'mixed_scopes' in audit['errors']

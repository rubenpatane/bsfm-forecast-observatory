import pytest
from bsfm.exposure import validate_exposure,exposure_only_probabilities,audit_exposure

def test_departure_probabilities_sum_to_one():
 rows=[{'period':'2024','cohort':'737NG','departures':3},{'period':'2024','cohort':'787','departures':1}]
 out=exposure_only_probabilities(rows)
 assert sum(r['baseline_probability'] for r in out)==1
 assert out[0]['baseline_probability']==0.75

def test_baseline_is_normalized_within_each_period():
 rows=[{'period':'2023','cohort':'737NG','departures':1},{'period':'2023','cohort':'787','departures':1},{'period':'2024','cohort':'737NG','departures':9},{'period':'2024','cohort':'787','departures':1}]
 out=exposure_only_probabilities(rows)
 for period in ('2023','2024'):
  assert sum(r['baseline_probability'] for r in out if r['period']==period)==pytest.approx(1.0)
 assert [r for r in out if r['period']=='2024' and r['cohort']=='737NG'][0]['baseline_probability']==pytest.approx(.9)

def test_duplicate_and_negative_exposure_fail():
 rows=[{'period':'2024','cohort':'737NG','departures':1},{'period':'2024','cohort':'737NG','departures':-1}]
 assert not validate_exposure(rows)['valid']
 with pytest.raises(ValueError): exposure_only_probabilities(rows)

def test_scientific_exposure_audit_requires_full_grid_and_metadata():
 rows=[{'period':'2024','cohort':'737NG','departures':3,'source':'ICAO','scope':'global-scheduled-commercial','provenance':'icao-2025-safety-report'}, {'period':'2024','cohort':'787','departures':1,'source':'ICAO','scope':'global-scheduled-commercial','provenance':'icao-2025-safety-report'}]
 assert audit_exposure(rows,['2024'],['737NG','787'])['complete']
 assert not audit_exposure(rows,['2024','2025'],['737NG','787'])['complete']

def test_scientific_exposure_audit_requires_provenance():
 rows=[{'period':'2024','cohort':'737NG','departures':3,'source':'ICAO','scope':'global-scheduled-commercial'}]
 audit=audit_exposure(rows,['2024'],['737NG'])
 assert not audit['complete'] and 'missing_provenance:0' in audit['errors']

def test_scientific_exposure_audit_rejects_mixed_scope():
 rows=[{'period':'2024','cohort':'737NG','departures':3,'source':'A','scope':'global','provenance':'a'}, {'period':'2024','cohort':'787','departures':1,'source':'B','scope':'US-only','provenance':'b'}]
 audit=audit_exposure(rows,['2024'],['737NG','787'])
 assert not audit['complete'] and 'mixed_scopes' in audit['errors']

def test_zero_departure_period_fails_closed():
 rows=[{'period':'2024','cohort':'737NG','departures':0,'source':'ICAO','scope':'global','provenance':'x'}]
 audit=audit_exposure(rows,['2024'],['737NG'])
 assert not audit['complete'] and audit['zero_departure_periods']==['2024']
 with pytest.raises(ValueError): exposure_only_probabilities(rows)

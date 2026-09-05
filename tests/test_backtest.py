import pytest
from bsfm.backtest import cutoffs_for_target,evaluate_temporal,publication_gate,admissible_features

def test_cutoffs_are_fixed_horizons():
 c=cutoffs_for_target('2020-12-31')
 assert c['T-7']=='2020-12-24' and c['T-30']=='2020-12-01' and c['T-365']=='2020-01-01'

def test_temporal_metrics():
 r=evaluate_temporal([0,2,20,40])
 assert r['n']==4 and r['hit_rates']['pm_1d']==0.25 and r['hit_rates']['pm_30d']==0.75

def test_publication_gate_fails_closed_and_requires_postfit_comparison():
 assert not publication_gate({})['pass']
 partial={'leakage_free':True,'baseline_present':True,'historical_cases':True,'calibration_evaluated':True}
 assert not publication_gate(partial)['pass']
 full={**partial,'paired_baseline_comparison':True,'candidate_better_than_baseline':True}
 assert publication_gate(full)['pass']

def test_legacy_admissible_features_uses_strict_verified_availability():
 rows=[{'id':'ok','historical_public_availability':'verified','available_at':'2020-01-01'},{'id':'unknown','available_at':'2019-01-01'}]
 assert [r['id'] for r in admissible_features(rows,'2020-01-02')]==['ok']
 with pytest.raises(ValueError): admissible_features(rows,'2020-01-02','event_date')

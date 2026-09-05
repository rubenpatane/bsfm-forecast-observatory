from bsfm.backtest import cutoffs_for_target,evaluate_temporal,publication_gate

def test_cutoffs_are_fixed_horizons():
 c=cutoffs_for_target('2020-12-31')
 assert c['T-7']=='2020-12-24'
 assert c['T-30']=='2020-12-01'
 assert c['T-365']=='2020-01-01'

def test_temporal_metrics():
 r=evaluate_temporal([0,2,20,40])
 assert r['n']==4
 assert r['hit_rates']['pm_1d']==0.25
 assert r['hit_rates']['pm_30d']==0.75

def test_publication_gate_fails_closed():
 assert not publication_gate({})['pass']
 r=publication_gate({'leakage_free':True,'baseline_present':True,'historical_cases':12,'calibration_evaluated':True})
 assert r['pass']

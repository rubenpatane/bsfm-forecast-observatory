import pytest
from bsfm.metrics import hit_rate,mae,brier,paired_brier_delta

def test_temporal_windows_are_absolute():
 errors=[-40,-7,0,3,20]
 assert hit_rate(errors,7)==3/5
 assert mae(errors)==14

def test_brier_and_baseline_delta():
 outcomes=[1,0]
 assert brier([1,0],outcomes)==0
 assert paired_brier_delta([1,0],[.5,.5],outcomes)==.25

def test_invalid_probability_rejected():
 with pytest.raises(ValueError): brier([1.2],[1])

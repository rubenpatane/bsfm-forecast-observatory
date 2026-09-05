import pytest
from bsfm.calibration import calibration_report


def test_calibration_fails_closed_without_observations():
    r=calibration_report([],[])
    assert not r['evaluated']


def test_calibration_reports_brier_and_reliability_bins():
    r=calibration_report([.1,.2,.8,.9],[0,0,1,1],bins=2)
    assert r['evaluated'] and r['n']==4
    assert r['brier']==pytest.approx(.025)
    assert r['bins'][0]['observed_rate']==0
    assert r['bins'][1]['observed_rate']==1


def test_calibration_rejects_nonbinary_truth():
    with pytest.raises(ValueError): calibration_report([.5],[2])

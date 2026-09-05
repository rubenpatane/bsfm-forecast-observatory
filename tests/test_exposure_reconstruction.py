from bsfm.exposure_reconstruction import cumulative_departure_interval,annual_difference_interval


def test_rounded_rate_yields_bounded_cumulative_departures():
    r=cumulative_departure_interval(23,.16)
    assert r['lower'] < r['midpoint'] < r['upper']
    assert r['midpoint']==143750000


def test_zero_rate_is_nonidentifying():
    assert cumulative_departure_interval(0,0) is None


def test_annual_difference_propagates_rounding_uncertainty():
    a=cumulative_departure_interval(21,.19)
    b=cumulative_departure_interval(23,.16)
    d=annual_difference_interval(a,b)
    assert d['identified'] and d['upper']>=d['lower']>=0

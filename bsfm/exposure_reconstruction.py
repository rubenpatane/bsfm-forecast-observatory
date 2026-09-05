from __future__ import annotations


def cumulative_departure_interval(accidents, rate_per_million, decimals=2):
    """Bound cumulative departures implied by a rounded published accident rate.

    If rate r is printed to `decimals`, the unrounded rate lies in the rounding
    interval around r. Since r = accidents/departures * 1e6, inversion yields
    a departure interval. This is suitable for sensitivity/reconstruction work,
    not an exact observed denominator. Zero accidents/rates are non-identifying.
    """
    a=int(accidents); r=float(rate_per_million)
    if a<=0 or r<=0: return None
    half=0.5*(10**(-decimals)); lo=max(r-half,0.0); hi=r+half
    if lo<=0: return None
    return {'lower':a*1_000_000/hi,'upper':a*1_000_000/lo,'midpoint':a*1_000_000/r}


def annual_difference_interval(previous,current):
    """Conservative interval for current cumulative minus previous cumulative."""
    if not previous or not current: return None
    lo=current['lower']-previous['upper']; hi=current['upper']-previous['lower']
    return {'lower':max(0.0,lo),'upper':max(0.0,hi),'identified':hi>=0}

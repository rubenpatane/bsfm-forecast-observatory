from __future__ import annotations

from .metrics import brier


def calibration_report(probabilities, outcomes, bins=10):
    """Return reliability diagnostics without claiming calibration validity.

    Empty samples, length mismatches, non-binary outcomes and invalid
    probabilities fail closed. `evaluated` means only that diagnostics were
    computed on supplied observations; promotion still depends on the
    preregistered historical gates and comparison against the null model.
    """
    probabilities=list(probabilities); outcomes=list(outcomes)
    if not probabilities or len(probabilities)!=len(outcomes):
        return {'evaluated':False,'reason':'empty_or_length_mismatch','n':len(outcomes),'bins':[]}
    if bins<1:
        raise ValueError('bins must be positive')
    if any(p<0 or p>1 for p in probabilities):
        raise ValueError('probabilities must be in [0,1]')
    if any(y not in (0,1,False,True) for y in outcomes):
        raise ValueError('outcomes must be binary')
    grouped=[]
    for i in range(bins):
        lo=i/bins; hi=(i+1)/bins
        idx=[j for j,p in enumerate(probabilities) if lo<=p<(hi if i<bins-1 else hi+1e-15)]
        if idx:
            grouped.append({'bin':i,'n':len(idx),'mean_probability':sum(probabilities[j] for j in idx)/len(idx),'observed_rate':sum(float(outcomes[j]) for j in idx)/len(idx)})
    return {'evaluated':True,'n':len(outcomes),'brier':brier(probabilities,outcomes),'bins':grouped}

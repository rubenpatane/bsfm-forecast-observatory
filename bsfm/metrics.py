from __future__ import annotations
from math import sqrt

def mean(values): return sum(values)/len(values) if values else None
def hit_rate(errors_days,window):
 if not errors_days: return None
 return sum(abs(x)<=window for x in errors_days)/len(errors_days)
def mae(errors_days): return mean([abs(x) for x in errors_days])
def brier(probabilities,outcomes):
 if len(probabilities)!=len(outcomes) or not probabilities: return None
 if any(p<0 or p>1 for p in probabilities): raise ValueError('probabilities must be in [0,1]')
 return mean([(p-float(y))**2 for p,y in zip(probabilities,outcomes)])
def accuracy(predicted,observed):
 if len(predicted)!=len(observed) or not predicted: return None
 return sum(a==b for a,b in zip(predicted,observed))/len(predicted)
def paired_brier_delta(model_p,baseline_p,outcomes):
 m=brier(model_p,outcomes); b=brier(baseline_p,outcomes)
 return None if m is None or b is None else b-m

from __future__ import annotations
from datetime import date,timedelta
from .point_in_time import point_in_time
from .metrics import hit_rate,mae,brier,paired_brier_delta

HORIZONS=(365,90,30,7)
WINDOWS=(30,14,7,3,1)
def cutoffs_for_target(target_date):
 d=date.fromisoformat(target_date) if isinstance(target_date,str) else target_date
 return {f'T-{h}':(d-timedelta(days=h)).isoformat() for h in HORIZONS}
def evaluate_temporal(errors):
 return {'n':len(errors),'mae_days':mae(errors),'hit_rates':{f'pm_{w}d':hit_rate(errors,w) for w in WINDOWS}}
def evaluate_probabilistic(model_p,baseline_p,outcomes):
 return {'n':len(outcomes),'model_brier':brier(model_p,outcomes),'baseline_brier':brier(baseline_p,outcomes),'paired_brier_improvement':paired_brier_delta(model_p,baseline_p,outcomes)}
def admissible_features(rows,cutoff,available_field='available_at'):
 return point_in_time(rows,cutoff,available_field)
def publication_gate(report):
 required=('leakage_free','baseline_present','historical_cases','calibration_evaluated')
 missing=[k for k in required if not report.get(k)]
 return {'pass':not missing,'missing':missing}

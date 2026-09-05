from __future__ import annotations
from datetime import date,timedelta
from .metrics import hit_rate,mae,brier,paired_brier_delta
from .walk_forward import eligible_snapshot

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
 """Backward-compatible strict PIT entry point; custom date fields are forbidden."""
 if available_field!='available_at':
  raise ValueError('historical eligibility requires canonical available_at')
 return eligible_snapshot(rows,cutoff)

def publication_gate(report):
 """Legacy publication gate aligned with the full post-fit evidence surface."""
 required=('leakage_free','baseline_present','historical_cases','calibration_evaluated','paired_baseline_comparison','candidate_better_than_baseline')
 missing=[k for k in required if report.get(k) is not True]
 return {'pass':not missing,'missing':missing}

from __future__ import annotations


def final_readiness(foundation: dict, lifecycle: dict | None = None) -> dict:
    """Summarise software/scientific readiness without converting UNKNOWN to PASS."""
    lifecycle=lifecycle or {}; promotion=lifecycle.get('gate',{}) or {}
    gates={
        'historical_cases':foundation.get('historical_cases') is True,
        'baseline_present':foundation.get('baseline_present') is True,
        'point_in_time_availability_verified':foundation.get('point_in_time_availability_verified') is True,
        'leakage_free':foundation.get('leakage_free') is True,
        'calibration_evaluated':foundation.get('calibration_evaluated') is True,
        'paired_baseline_comparison':foundation.get('paired_baseline_comparison') is True,
        'candidate_better_than_baseline':foundation.get('candidate_better_than_baseline') is True,
    }
    fit_names=('historical_cases','baseline_present','point_in_time_availability_verified','leakage_free')
    fit_ready=all(gates[k] for k in fit_names)
    promotion_ready=fit_ready and all(gates[k] for k in ('calibration_evaluated','paired_baseline_comparison','candidate_better_than_baseline')) and promotion.get('pass') is True
    blocked=[name for name,ok in gates.items() if not ok]
    for name in promotion.get('missing',[]):
        if name not in blocked: blocked.append(name)
    return {
        'schema':'bsfm.final-readiness.v2','software_audit_evaluable':True,
        'scientific_fit_ready':fit_ready,'scientific_promotion_ready':promotion_ready,
        'gates':gates,'blocked_reasons':blocked,
        'absolute_accident_probabilities_enabled':promotion_ready,
        'validated_prediction_claim_allowed':promotion_ready,
    }

from __future__ import annotations


def final_readiness(foundation: dict, lifecycle: dict | None = None) -> dict:
    """Summarise software/scientific readiness without converting UNKNOWN to PASS.

    Software completeness and empirical validation are deliberately distinct.
    A green software audit may coexist with blocked scientific evidence gates.
    """
    lifecycle = lifecycle or {}
    gates = {
        'historical_cases': foundation.get('historical_cases') is True,
        'baseline_present': foundation.get('baseline_present') is True,
        'point_in_time_availability_verified': foundation.get('point_in_time_availability_verified') is True,
        'leakage_free': foundation.get('leakage_free') is True,
        'calibration_evaluated': foundation.get('calibration_evaluated') is True,
    }
    fit_ready = all(gates[k] for k in (
        'historical_cases', 'baseline_present',
        'point_in_time_availability_verified', 'leakage_free'))
    promotion_ready = fit_ready and gates['calibration_evaluated'] and bool(
        lifecycle.get('gate', {}).get('pass'))
    blocked = [name for name, ok in gates.items() if not ok]
    return {
        'schema': 'bsfm.final-readiness.v1',
        'software_audit_evaluable': True,
        'scientific_fit_ready': fit_ready,
        'scientific_promotion_ready': promotion_ready,
        'gates': gates,
        'blocked_reasons': blocked,
        'absolute_accident_probabilities_enabled': promotion_ready,
        'validated_prediction_claim_allowed': promotion_ready,
    }

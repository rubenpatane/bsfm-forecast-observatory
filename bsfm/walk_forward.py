from __future__ import annotations

from collections import defaultdict
from datetime import date

from .calibration import calibration_report
from .metrics import brier


def eligible_snapshot(rows, cutoff):
    """Return predictor rows provably public no later than cutoff.

    A row without an explicit verified availability date is excluded. Event,
    submission, approval and last-change dates are deliberately not accepted as
    substitutes for public availability.
    """
    c = date.fromisoformat(str(cutoff)[:10])
    out = []
    for row in rows:
        if row.get('historical_public_availability') != 'verified':
            continue
        raw = row.get('available_at')
        try:
            available = date.fromisoformat(str(raw)[:10])
        except (TypeError, ValueError):
            continue
        if available <= c:
            out.append(row)
    return out


def score_multiclass(probabilities, observed_cohort):
    """Multiclass Brier score for one mutually-exclusive cohort outcome."""
    if not probabilities:
        raise ValueError('probabilities required')
    probs = {str(k): float(v) for k, v in probabilities.items()}
    if any(v < 0 or v > 1 for v in probs.values()):
        raise ValueError('probabilities must be in [0,1]')
    if abs(sum(probs.values()) - 1.0) > 1e-9:
        raise ValueError('probabilities must sum to one')
    if str(observed_cohort) not in probs:
        raise ValueError('observed cohort missing from probability simplex')
    return sum((p - (1.0 if cohort == str(observed_cohort) else 0.0)) ** 2 for cohort, p in probs.items())


def evaluate_walk_forward(predictions):
    """Aggregate immutable historical forecasts without opening scientific gates.

    Each row needs case_id, probability and binary outcome. Calibration is
    descriptive until the surrounding historical-foundation gates are green.
    """
    rows = list(predictions)
    if not rows:
        return {'evaluated': False, 'reason': 'no_predictions', 'n': 0}
    required = ('case_id', 'probability', 'outcome')
    if any(any(k not in row for k in required) for row in rows):
        return {'evaluated': False, 'reason': 'incomplete_prediction_rows', 'n': len(rows)}
    probs = [float(r['probability']) for r in rows]
    outcomes = [r['outcome'] for r in rows]
    report = calibration_report(probs, outcomes)
    return {
        'evaluated': report['evaluated'],
        'n': len(rows),
        'brier': brier(probs, outcomes),
        'calibration': report,
    }


def compare_candidate_to_baseline(candidate_rows, baseline_rows):
    """Paired Brier comparison; fail closed unless case IDs match exactly."""
    candidate = {str(r['case_id']): r for r in candidate_rows}
    baseline = {str(r['case_id']): r for r in baseline_rows}
    if not candidate or set(candidate) != set(baseline):
        return {'comparable': False, 'reason': 'unpaired_cases'}
    ids = sorted(candidate)
    if any(candidate[i].get('outcome') != baseline[i].get('outcome') for i in ids):
        return {'comparable': False, 'reason': 'outcome_mismatch'}
    cp = [float(candidate[i]['probability']) for i in ids]
    bp = [float(baseline[i]['probability']) for i in ids]
    y = [candidate[i]['outcome'] for i in ids]
    cs = brier(cp, y); bs = brier(bp, y)
    return {
        'comparable': True,
        'n': len(ids),
        'candidate_brier': cs,
        'baseline_brier': bs,
        'brier_improvement': bs - cs,
        'candidate_better': cs < bs,
    }

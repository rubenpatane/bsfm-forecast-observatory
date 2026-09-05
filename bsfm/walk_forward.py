from __future__ import annotations

from datetime import date

from .calibration import calibration_report
from .metrics import brier


def eligible_snapshot(rows, cutoff):
    """Return predictor rows provably public no later than cutoff."""
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


def _validate_prediction_rows(rows):
    required=('case_id','probability','outcome')
    if any(any(k not in row for k in required) for row in rows):
        return 'incomplete_prediction_rows'
    ids=[str(row['case_id']) for row in rows]
    if any(not i for i in ids) or len(ids)!=len(set(ids)):
        return 'duplicate_or_empty_case_id'
    try:
        probs=[float(row['probability']) for row in rows]
    except (TypeError,ValueError):
        return 'invalid_probability'
    if any(p < 0 or p > 1 for p in probs):
        return 'invalid_probability'
    if any(row['outcome'] not in (0,1,False,True) for row in rows):
        return 'invalid_outcome'
    return None


def evaluate_walk_forward(predictions):
    """Aggregate immutable historical forecasts without opening scientific gates."""
    rows=list(predictions)
    if not rows:
        return {'evaluated':False,'reason':'no_predictions','n':0}
    reason=_validate_prediction_rows(rows)
    if reason:
        return {'evaluated':False,'reason':reason,'n':len(rows)}
    probs=[float(r['probability']) for r in rows]
    outcomes=[r['outcome'] for r in rows]
    report=calibration_report(probs,outcomes)
    return {'evaluated':report['evaluated'],'n':len(rows),'brier':brier(probs,outcomes),'calibration':report}


def compare_candidate_to_baseline(candidate_rows, baseline_rows):
    """Paired Brier comparison; fail closed unless cases are unique and identical."""
    crows=list(candidate_rows); brows=list(baseline_rows)
    creason=_validate_prediction_rows(crows) if crows else 'no_predictions'
    breason=_validate_prediction_rows(brows) if brows else 'no_predictions'
    if creason or breason:
        return {'comparable':False,'reason':creason or breason}
    candidate={str(r['case_id']):r for r in crows}
    baseline={str(r['case_id']):r for r in brows}
    if set(candidate)!=set(baseline):
        return {'comparable':False,'reason':'unpaired_cases'}
    ids=sorted(candidate)
    if any(candidate[i]['outcome']!=baseline[i]['outcome'] for i in ids):
        return {'comparable':False,'reason':'outcome_mismatch'}
    cp=[float(candidate[i]['probability']) for i in ids]
    bp=[float(baseline[i]['probability']) for i in ids]
    y=[candidate[i]['outcome'] for i in ids]
    cs=brier(cp,y); bs=brier(bp,y)
    return {'comparable':True,'n':len(ids),'candidate_brier':cs,'baseline_brier':bs,'brier_improvement':bs-cs,'candidate_better':cs<bs}

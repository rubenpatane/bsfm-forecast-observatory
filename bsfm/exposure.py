from __future__ import annotations

REQUIRED_META=('source','scope')

def validate_exposure(rows,require_metadata=False):
    errors=[]; seen=set(); total=0.0; scopes=set()
    for i,row in enumerate(rows):
        key=(row.get('period'),row.get('cohort'))
        if not all(key): errors.append(f'missing_period_or_cohort:{i}')
        if key in seen: errors.append(f'duplicate:{key}')
        seen.add(key)
        try: value=float(row['departures'])
        except (KeyError,TypeError,ValueError):
            errors.append(f'invalid_departures:{i}'); continue
        if value<0: errors.append(f'negative_departures:{i}')
        total+=max(value,0.0)
        if require_metadata:
            for field in REQUIRED_META:
                if not str(row.get(field,'')).strip(): errors.append(f'missing_{field}:{i}')
            scope=str(row.get('scope','')).strip()
            if scope: scopes.add(scope)
    if require_metadata and len(scopes)>1: errors.append('mixed_scopes')
    return {'valid':not errors,'errors':errors,'total_departures':total,'scopes':sorted(scopes)}

def audit_exposure(rows,expected_periods,expected_cohorts):
    rows=list(rows); base=validate_exposure(rows,require_metadata=True)
    present={(str(r.get('period')),str(r.get('cohort'))) for r in rows}
    expected={(str(p),str(c)) for p in expected_periods for c in expected_cohorts}
    missing=sorted(expected-present)
    extra=sorted(present-expected)
    return {**base,'complete':base['valid'] and not missing and not extra and base['total_departures']>0,'missing_cells':missing,'extra_cells':extra}

def exposure_only_probabilities(rows):
    audit=validate_exposure(rows)
    if not audit['valid'] or audit['total_departures']<=0:
        raise ValueError('valid positive departures exposure required')
    total=audit['total_departures']
    return [{**row,'baseline_probability':float(row['departures'])/total} for row in rows]

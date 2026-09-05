from __future__ import annotations

def validate_exposure(rows):
    errors=[]
    seen=set()
    total=0.0
    for i,row in enumerate(rows):
        key=(row.get('period'),row.get('cohort'))
        if key in seen: errors.append(f'duplicate:{key}')
        seen.add(key)
        try: value=float(row['departures'])
        except (KeyError,TypeError,ValueError):
            errors.append(f'invalid_departures:{i}'); continue
        if value<0: errors.append(f'negative_departures:{i}')
        total+=max(value,0.0)
    return {'valid':not errors,'errors':errors,'total_departures':total}

def exposure_only_probabilities(rows):
    audit=validate_exposure(rows)
    if not audit['valid'] or audit['total_departures']<=0:
        raise ValueError('valid positive departures exposure required')
    total=audit['total_departures']
    return [{**row,'baseline_probability':float(row['departures'])/total} for row in rows]

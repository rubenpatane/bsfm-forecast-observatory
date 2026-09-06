from __future__ import annotations

EVENT_KEYS = ('event_id','date','flight_number','model','registration','msn','operator','phase','geography','decision','provenance')
VALID_DECISIONS = {'include','exclude','pending','unresolved'}


def validate_rich_annual_evidence(record):
    errors=[]
    if not isinstance(record,dict): return {'valid':False,'errors':['record_not_object']}
    try: int(record.get('year'))
    except (TypeError,ValueError): errors.append('invalid_year')
    controls=record.get('controls') or {}
    for event_index,event in enumerate(record.get('events') or []):
        for key in EVENT_KEYS:
            if key not in event: errors.append(f'missing_event_{key}:{event_index}')
        if event.get('decision') not in VALID_DECISIONS: errors.append(f'invalid_event_decision:{event_index}')
        if not isinstance(event.get('provenance'),list) or not event.get('provenance'):
            errors.append(f'missing_event_provenance:{event_index}')
    return {'valid':not errors,'errors':errors,'controls':controls}

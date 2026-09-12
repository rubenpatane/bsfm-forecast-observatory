"""Point-in-time feature snapshot builder for model 1.5 candidate work."""
import json
from datetime import date
from pathlib import Path

def _date(v):
    try:return date.fromisoformat(str(v)[:10])
    except (TypeError,ValueError):return None

def build_snapshot(rows, cutoff):
    c=_date(cutoff); out=[]
    for r in rows:
        event=_date(r.get('event_date')); available=_date(r.get('available_at'))
        if not event or event>c: continue
        # A record is admitted as a predictor snapshot only when its public
        # availability is explicit and not later than the simulated cutoff.
        pit=bool(available and available<=c)
        out.append({'event_id':r.get('event_id'),'event_date':event.isoformat(),'boeing':bool(r.get('boeing', r.get('manufacturer') == 'Boeing')),'cohort':r.get('cohort'),'aircraft_family':r.get('aircraft_family', r.get('cohort')),'model':r.get('model'),'aircraft_variant':r.get('aircraft_variant', r.get('model')),'icao_type':r.get('icao_type'),'serial_number':r.get('serial_number'),'serial_or_registration':r.get('serial_or_registration', r.get('registration')),'registration':r.get('registration'),'aircraft_age':r.get('aircraft_age'),'phase':r.get('phase'),'phase_of_flight':r.get('phase_of_flight', r.get('phase')),'system':r.get('system'),'failure_mode':r.get('failure_mode'),'severity':r.get('severity', r.get('accident_class')),'operation_type':r.get('operation_type'),'geography':r.get('geography', r.get('location')),'origin':r.get('origin'),'destination':r.get('destination'),'route':r.get('route'),'airport':r.get('airport'),'operator':r.get('operator'),'maintenance_signal':r.get('maintenance_signal'),'safety_report_signal':r.get('safety_report_signal'),'fatal':bool(r.get('fatal', r.get('fatalities', 0))), 'pit_available':pit,'feature_status':'admissible' if pit else 'target_only'})
    return out

def load_jsonl(path):
    p=Path(path)
    if not p.exists(): return []
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]

def build_unified_feature_table(root, cutoff=None):
    """Join the existing PIT event table with windowed signal features by event id.
    Missing values remain explicit; no value is inferred from absence.
    """
    root=Path(root)
    p=root/'data/model/pit-event-feature-table-v1.json'
    if not p.exists(): return []
    data=json.loads(p.read_text())
    rows=data.get('features', data.get('rows', []))
    sigp=root/'data/model/pit-signal-features-35-v1.json'
    signals={}
    if sigp.exists():
        for x in json.loads(sigp.read_text()).get('rows',[]): signals[x.get('case_id')]=x
    out=[]
    c=_date(cutoff) if cutoff else None
    for r in rows:
        if c and (_date(r.get('event_date')) or date.max)>c: continue
        x=dict(r); s=signals.get(r.get('event_id'),{})
        x['signal_windows']=s.get('windows',{})
        x['signal_admitted_rows']=s.get('admitted_rows',0)
        x['signal_status']=s.get('status','unknown')
        x['feature_status']='admissible' if r.get('pit_available') and s.get('status') in ('development','admissible') else r.get('feature_status','unknown')
        out.append(x)
    return out

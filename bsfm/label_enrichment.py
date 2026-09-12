"""Deterministic enrichment of existing public PIT event rows for BM1.5."""
from datetime import date
from pathlib import Path
import json

def _date(v):
    try:return date.fromisoformat(str(v)[:10])
    except (TypeError,ValueError):return None

def _icao(model):
    m=str(model or '').upper().replace(' ','')
    for prefix,typ in [('737','B73'),('747','B74'),('757','B75'),('767','B76'),('777','B77'),('787','B78'),('727','B72')]:
        if m.startswith(prefix): return typ
    return None

def enrich(rows):
    out=[]
    for r in rows:
        x=dict(r)
        ed=_date(r.get('event_date')); year=r.get('manufacture_year')
        if r.get('aircraft_age') is None and ed and str(year or '').isdigit(): x['aircraft_age']=ed.year-int(year)
        x['icao_type']=r.get('icao_type') or _icao(r.get('model') or r.get('aircraft_variant'))
        x['phase_of_flight']=r.get('phase_of_flight') or r.get('phase') or None
        x['system']=r.get('system') or r.get('failure_system') or None
        x['failure_mode']=r.get('failure_mode') or r.get('mode_of_failure') or None
        windows=r.get('signal_windows') or {}
        for w in ('7d','30d','90d'):
            z=windows.get(w,{})
            x['maintenance_'+w]=z.get('maintenance_count') if isinstance(z,dict) else None
            x['safety_report_'+w]=z.get('safety_report_count') if isinstance(z,dict) else None
        out.append(x)
    return out

def enrich_file(src,dst):
    d=json.loads(Path(src).read_text()); rows=d.get('rows',d.get('features',[])); e=enrich(rows)
    Path(dst).write_text(json.dumps({'schema':'bsfm.model-1.5-enriched-labels.v1','status':'development_only','source':str(src),'rows':e,'row_count':len(e),'unknown_policy':'missing or unverified values remain null/unknown'},indent=2,sort_keys=True)+'\n')
    return e

from __future__ import annotations
import csv,json
from pathlib import Path

ALIASES={
 'event_id':('ev_id','EventId','event_id'),
 'event_date':('ev_date','EventDate','event_date'),
 'publication_date':('PublicationDate','publication_date','pub_date'),
 'make':('acft_make','Make','make'),
 'model':('acft_model','Model','model'),
 'phase':('broad_phase','BroadPhaseOfFlight','phase'),
 'fatalities':('inj_tot_f','TotalFatalInjuries','fatalities'),
 'schedule':('sched','Schedule','schedule'),
 'carrier':('oper_name','AirCarrier','carrier'),
 'far_part':('far_part','FARDescription'),
}
def _pick(row,names):
 for n in names:
  v=row.get(n)
  if v not in (None,''): return str(v).strip()
 return None
def _int(v):
 try: return int(float(v or 0))
 except (ValueError,TypeError): return 0
def normalize_row(row):
 d={k:_pick(row,v) for k,v in ALIASES.items()}
 d['fatalities']=_int(d['fatalities']); d['fatal']=d['fatalities']>0
 d['boeing']='BOEING' in (d['make'] or '').upper()
 sched=(d['schedule'] or '').strip().upper(); carrier=(d['carrier'] or '').strip(); far=(d['far_part'] or '').upper()
 d['commercial']=bool(carrier) or sched not in ('','NONE','N/A','UNK','UNKNOWN') or any(x in far for x in ('121','129','135'))
 # AVALL does not guarantee a historical publication timestamp for every exported row.
 # Missing availability is deliberately retained as unknown; event date is never substituted.
 d['available_at']=d['publication_date']
 return d
def _read(path):
 with Path(path).open(errors='replace',newline='') as f: return list(csv.DictReader(f))
def join_events_aircraft(events_csv,aircraft_csv):
 events=_read(events_csv); aircraft=_read(aircraft_csv); by_event={}
 for a in aircraft: by_event.setdefault(_pick(a,ALIASES['event_id']),[]).append(a)
 rows=[]
 for e in events:
  eid=_pick(e,ALIASES['event_id']); matches=by_event.get(eid) or [{}]
  for a in matches:
   merged=dict(e); merged.update({k:v for k,v in a.items() if v not in (None,'')})
   rows.append(normalize_row(merged))
 return rows
def write_normalized(events_csv,aircraft_csv,out_jsonl):
 rows=join_events_aircraft(events_csv,aircraft_csv); p=Path(out_jsonl); p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w') as f:
  for r in rows: f.write(json.dumps(r,sort_keys=True)+'\n')
 return {'rows':len(rows),'boeing_rows':sum(r['boeing'] for r in rows),'fatal_boeing_rows':sum(r['boeing'] and r['fatal'] for r in rows),'commercial_boeing_rows':sum(r['boeing'] and r['commercial'] for r in rows),'availability_known':sum(bool(r['available_at']) for r in rows)}

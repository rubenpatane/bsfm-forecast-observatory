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
 d['fatalities']=_int(d['fatalities'])
 d['fatal']=d['fatalities']>0
 d['boeing']='BOEING' in (d['make'] or '').upper()
 # Conservative commercial flag: unknown schedule/carrier is not promoted to commercial.
 sched=(d['schedule'] or '').strip().upper(); carrier=(d['carrier'] or '').strip()
 d['commercial']=bool(carrier) or sched not in ('','NONE','N/A','UNK','UNKNOWN')
 # Publication date is the admissible AVALL availability proxy; absent publication stays unknown.
 d['available_at']=d['publication_date']
 return d
def normalize_csv(path):
 with Path(path).open(errors='replace',newline='') as f:
  return [normalize_row(r) for r in csv.DictReader(f)]
def write_normalized(events_csv,out_jsonl):
 rows=normalize_csv(events_csv); p=Path(out_jsonl); p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w') as f:
  for r in rows: f.write(json.dumps(r,sort_keys=True)+'\n')
 return {'rows':len(rows),'boeing_rows':sum(r['boeing'] for r in rows),'fatal_boeing_rows':sum(r['boeing'] and r['fatal'] for r in rows),'availability_known':sum(bool(r['available_at']) for r in rows)}

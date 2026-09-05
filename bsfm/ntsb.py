from __future__ import annotations
import csv,json
from datetime import datetime
from pathlib import Path

ALIASES={
 'event_id':('ev_id','EventId','event_id'),
 'aircraft_key':('Aircraft_Key','aircraft_key','acft_key'),
 'event_date':('ev_date','EventDate','event_date'),
 'publication_date':('PublicationDate','publication_date','pub_date'),
 'make':('acft_make','Make','make'),
 'model':('acft_model','Model','model'),
 'phase':('phase_flt_spec','broad_phase','BroadPhaseOfFlight','phase'),
 'fatalities':('inj_tot_f','TotalFatalInjuries','fatalities'),
 'schedule':('oper_sched','sched','Schedule','schedule'),
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
def _date(v):
 if not v: return None
 for fmt in ('%m/%d/%y %H:%M:%S','%m/%d/%Y %H:%M:%S','%Y-%m-%d','%m/%d/%Y'):
  try: return datetime.strptime(v.strip(),fmt).date().isoformat()
  except ValueError: pass
 return None
def normalize_row(row):
 d={k:_pick(row,v) for k,v in ALIASES.items()}
 d['event_date']=_date(d['event_date']) or d['event_date']
 d['fatalities']=_int(d['fatalities']); d['fatal']=d['fatalities']>0
 d['boeing']='BOEING' in (d['make'] or '').upper()
 sched=(d['schedule'] or '').strip().upper(); far=(d['far_part'] or '').strip().upper()
 # Operator-name presence is not evidence of commercial service.
 d['scheduled_service']=sched=='SCHD'
 d['commercial']=far in {'121','125','129','135'} or sched in {'SCHD','NSCH'}
 # Current AVALL is useful for final outcome labels. Historical public availability is
 # unknown unless an explicit defensible publication timestamp is present.
 d['available_at']=d['publication_date']
 return d
def _read(path):
 with Path(path).open(errors='replace',newline='') as f: return list(csv.DictReader(f))
def _key(row): return (_pick(row,ALIASES['event_id']),_pick(row,ALIASES['aircraft_key']))
def _group_details(path,kind):
 if not path or not Path(path).exists(): return {}
 grouped={}
 for row in _read(path):
  if kind=='sequence':
   item={'occurrence_no':_pick(row,('Occurrence_No',)),'occurrence_code':_pick(row,('Occurrence_Code',)),'occurrence_description':_pick(row,('Occurrence_Description',)),'phase_no':_pick(row,('phase_no',)),'defining_event':_pick(row,('Defining_ev',))}
  else:
   item={'finding_no':_pick(row,('finding_no',)),'finding_code':_pick(row,('finding_code',)),'finding_description':_pick(row,('finding_description',)),'cause_factor':_pick(row,('Cause_Factor',))}
  grouped.setdefault(_key(row),[]).append(item)
 return grouped
def join_events_aircraft(events_csv,aircraft_csv,sequence_csv=None,findings_csv=None):
 events=_read(events_csv); aircraft=_read(aircraft_csv); by_event={}
 sequence=_group_details(sequence_csv,'sequence'); findings=_group_details(findings_csv,'finding')
 for a in aircraft: by_event.setdefault(_pick(a,ALIASES['event_id']),[]).append(a)
 rows=[]
 for e in events:
  eid=_pick(e,ALIASES['event_id']); matches=by_event.get(eid) or [{}]
  for a in matches:
   merged=dict(e); merged.update({k:v for k,v in a.items() if v not in (None,'')})
   r=normalize_row(merged); key=(eid,r['aircraft_key'])
   r['event_sequence']=sequence.get(key,[]); r['findings']=findings.get(key,[])
   rows.append(r)
 return rows
def write_normalized(events_csv,aircraft_csv,out_jsonl,sequence_csv=None,findings_csv=None):
 rows=join_events_aircraft(events_csv,aircraft_csv,sequence_csv,findings_csv); p=Path(out_jsonl); p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w') as f:
  for r in rows: f.write(json.dumps(r,sort_keys=True)+'\n')
 return {
  'rows':len(rows),
  'boeing_rows':sum(r['boeing'] for r in rows),
  'fatal_boeing_rows':sum(r['boeing'] and r['fatal'] for r in rows),
  'commercial_boeing_rows':sum(r['boeing'] and r['commercial'] for r in rows),
  'scheduled_boeing_rows':sum(r['boeing'] and r['scheduled_service'] for r in rows),
  'availability_known':sum(bool(r['available_at']) for r in rows),
  'rows_with_sequence':sum(bool(r['event_sequence']) for r in rows),
  'rows_with_findings':sum(bool(r['findings']) for r in rows),
 }

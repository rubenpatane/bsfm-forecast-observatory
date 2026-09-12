"""Registration-level historical analysis for BM1.5 diagnostics."""
import json
from pathlib import Path

def build(root=Path('.')):
 root=Path(root); src=root/'data/model/model-1.5-enriched-labels-v1.json'
 rows=json.loads(src.read_text()).get('rows',[]) if src.exists() else []
 out=[]
 for r in rows:
  out.append({'event_id':r.get('event_id'),'event_date':r.get('event_date'),'registration':r.get('serial_or_registration') or r.get('registration'),'msn':r.get('msn'),'model':r.get('model') or r.get('aircraft_variant'),'icao_type':r.get('icao_type'),'operator':r.get('operator'),'geography':r.get('geography'),'manufacture_year':r.get('manufacture_year'),'aircraft_age':r.get('aircraft_age'),'source_locator':r.get('source_locator'),'join_status':'linked_event_registration','age_status':'derived' if r.get('aircraft_age') is not None else 'missing_manufacture_year'})
 return {'schema':'bsfm.registration-analysis.v1','status':'development_only','source':str(src),'rows':out,'row_count':len(out),'policy':'registration identifies historical cases; it is not a forecast of a future aircraft'}
if __name__=='__main__': print(json.dumps(build(),indent=2))

from __future__ import annotations
from datetime import datetime, timezone
import hashlib,json,re
from pathlib import Path

ALLOWED_STATUS={'exploratory','prospective_unvalidated','validated'}
REQUIRED={'refinement_id','parent_forecast_id','issued_at','model_version','input_hashes','changes','status'}
RID=re.compile(r'^R-F002-\d{3,}$')

def _time(value:str)->datetime:
 v=value.strip().replace('Z','+00:00'); d=datetime.fromisoformat(v)
 if d.tzinfo is None: d=d.replace(tzinfo=timezone.utc)
 return d.astimezone(timezone.utc)

def validate_refinement(record:dict,parent:dict)->list[str]:
 errors=[]; missing=sorted(k for k in REQUIRED if record.get(k) in (None,'',[],{}))
 if missing: errors.append('missing required fields: '+', '.join(missing))
 if not RID.match(record.get('refinement_id','')): errors.append('invalid refinement_id')
 if record.get('parent_forecast_id') != parent.get('forecast_id'): errors.append('parent_forecast_id does not match parent')
 if record.get('status') not in ALLOWED_STATUS: errors.append('invalid refinement status')
 try:
  if _time(record['issued_at']) <= _time(parent['cutoff']): errors.append('refinement must be issued after parent cutoff')
 except (KeyError,ValueError,TypeError): errors.append('invalid issued_at or parent cutoff')
 if record.get('alters_parent_scoring',False): errors.append('refinement may not alter parent scoring')
 for c in record.get('changes') or []:
  if not c.get('dimension') or 'new_value' not in c: errors.append('each change requires dimension and new_value')
 return errors

def public_view(record:dict)->dict:
 return {'refinement_id':record['refinement_id'],'parent_forecast_id':record['parent_forecast_id'],'issued_at':record['issued_at'],'model_version':record['model_version'],'status':record['status'],'changes':record['changes'],'uncertainty':record.get('uncertainty','not quantified'),'record_sha256':hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'notice':'Later refinement — not part of the original parent forecast and not counted in its original score.'}

def collect_public_refinements(root:Path,parent:dict)->list[dict]:
 """Append-only publication: invalid/unproven records never reach the public site."""
 d=Path(root)/'forecasts/refinements'; out=[]
 if not d.exists(): return out
 for path in sorted(d.glob('R-F002-*.json')):
  try: record=json.loads(path.read_text(encoding='utf-8'))
  except (OSError,json.JSONDecodeError): continue
  if not validate_refinement(record,parent) and record.get('provenance_gate_passed') is True:
   out.append(public_view(record))
 return sorted(out,key=lambda x:(x['issued_at'],x['refinement_id']))

def write_public_refinements(root:Path,parent:dict,out:Path|None=None)->list[dict]:
 rows=collect_public_refinements(root,parent); out=out or Path(root)/'site/data/refinements.json'; out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n',encoding='utf-8'); return rows

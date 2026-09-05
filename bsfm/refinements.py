from __future__ import annotations
from datetime import datetime, timezone

ALLOWED_STATUS={'exploratory','prospective_unvalidated','validated'}
REQUIRED={'refinement_id','parent_forecast_id','issued_at','model_version','input_hashes','changes','status'}

def _time(value:str)->datetime:
 v=value.strip().replace('Z','+00:00')
 d=datetime.fromisoformat(v)
 if d.tzinfo is None: d=d.replace(tzinfo=timezone.utc)
 return d.astimezone(timezone.utc)

def validate_refinement(record:dict,parent:dict)->list[str]:
 errors=[]
 missing=sorted(k for k in REQUIRED if record.get(k) in (None,'',[],{}))
 if missing: errors.append('missing required fields: '+', '.join(missing))
 if record.get('parent_forecast_id') != parent.get('forecast_id'):
  errors.append('parent_forecast_id does not match parent')
 if record.get('status') not in ALLOWED_STATUS:
  errors.append('invalid refinement status')
 try:
  if _time(record['issued_at']) <= _time(parent['cutoff']):
   errors.append('refinement must be issued after parent cutoff')
 except (KeyError,ValueError,TypeError):
  errors.append('invalid issued_at or parent cutoff')
 if record.get('alters_parent_scoring',False):
  errors.append('refinement may not alter parent scoring')
 for c in record.get('changes') or []:
  if not c.get('dimension') or 'new_value' not in c:
   errors.append('each change requires dimension and new_value')
 return errors

def public_view(record:dict)->dict:
 return {
  'refinement_id':record['refinement_id'],
  'parent_forecast_id':record['parent_forecast_id'],
  'issued_at':record['issued_at'],
  'model_version':record['model_version'],
  'status':record['status'],
  'changes':record['changes'],
  'uncertainty':record.get('uncertainty','not quantified'),
  'notice':'Later refinement — not part of the original parent forecast and not counted in its original score.'
 }

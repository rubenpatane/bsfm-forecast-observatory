from datetime import datetime,timezone
from pathlib import Path
import json
from .integrity import digest,write_json_atomic
from .registry import verify
ROOT=Path(__file__).resolve().parents[1]
def utcnow(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def validate_sources():
 ms=sorted((ROOT/'data'/'manifests').glob('*.json')); checks=[]
 for p in ms:
  d=json.loads(p.read_text())
  # The directory also contains operational state such as auto-cadence.json.
  # Only actual source manifests belong to the source-integrity gate.
  if not d.get('source'): continue
  checks.append({
   'manifest':p.name,'source':d.get('source'),'cutoff':d.get('cutoff'),'status':d.get('status','unknown'),
   'historical_public_availability':d.get('historical_public_availability'),
  })
 integrity_ready=bool(checks) and all(x['status']=='validated' for x in checks)
 # Fail closed: download/schema integrity is not leakage-free model readiness. Every
 # predictor manifest must explicitly say "verified"; missing/unknown values never pass.
 availability_verified=bool(checks) and all(x.get('historical_public_availability')=='verified' for x in checks)
 return {
  'checked_at':utcnow(),'manifests':checks,
  'source_integrity_ready':integrity_ready,
  'point_in_time_availability_verified':availability_verified,
  'ready_for_model':integrity_ready and availability_verified,
 }
def run():
 errors=verify(ROOT); sources=validate_sources()
 if errors: reason='registry_integrity_failure'
 elif not sources['source_integrity_ready']: reason='validated_source_snapshots_unavailable'
 elif not sources['point_in_time_availability_verified']: reason='historical_point_in_time_availability_unverified'
 else: reason='estimator_not_yet_calibrated'
 state={'run_at':utcnow(),'registry_integrity':'ok' if not errors else 'failed','integrity_errors':errors,'sources':sources,'forecast_generated':False,'reason':reason}
 state['run_hash']=digest(state); write_json_atomic(ROOT/'site'/'data'/'status.json',state); return state

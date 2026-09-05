from datetime import datetime,timezone
from pathlib import Path
import json
from .integrity import digest,write_json_atomic
from .registry import verify
ROOT=Path(__file__).resolve().parents[1]
def utcnow(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
def validate_sources():
 ms=sorted((ROOT/"data"/"manifests").glob("*.json")); checks=[]
 for p in ms:
  d=json.loads(p.read_text()); checks.append({"manifest":p.name,"source":d.get("source"),"cutoff":d.get("cutoff"),"status":d.get("status","unknown")})
 return {"checked_at":utcnow(),"manifests":checks,"ready_for_model":bool(checks) and all(x["status"]=="validated" for x in checks)}
def run():
 errors=verify(ROOT); sources=validate_sources(); reason="registry_integrity_failure" if errors else ("estimator_not_yet_calibrated" if sources["ready_for_model"] else "validated_source_snapshots_unavailable")
 state={"run_at":utcnow(),"registry_integrity":"ok" if not errors else "failed","integrity_errors":errors,"sources":sources,"forecast_generated":False,"reason":reason}; state["run_hash"]=digest(state); write_json_atomic(ROOT/"site"/"data"/"status.json",state); return state

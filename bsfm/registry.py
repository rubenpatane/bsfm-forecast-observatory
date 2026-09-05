from pathlib import Path
from .integrity import digest,read_json,write_json_atomic
REQUIRED={"forecast_id","model_version","cutoff","created_at","target","status","prediction"}
def validate_forecast(d):
 m=REQUIRED-d.keys()
 if m: raise ValueError(f"missing forecast fields: {sorted(m)}")
 if d["status"]!="frozen": raise ValueError("registry accepts only frozen forecasts")
def freeze(root:Path,d):
 validate_forecast(d); p=root/"forecasts"/f'{d["forecast_id"]}.json'; frozen=dict(d); frozen["integrity"]=digest(d)
 if p.exists():
  if read_json(p)!=frozen: raise RuntimeError(f"immutable forecast {d['forecast_id']} already exists")
  return p
 write_json_atomic(p,frozen); return p
def verify(root:Path):
 errors=[]
 for p in sorted((root/"forecasts").glob("F-*.json")):
  d=read_json(p); stored=d.pop("integrity",None)
  if stored!=digest(d): errors.append(f"{p}: integrity mismatch")
 return errors

import argparse,json
from pathlib import Path
from .pipeline import run,validate_sources
from .registry import verify
from .sources import ingest_current,ingest_history
from .foundation_report import build_foundation_report
from .model_lifecycle import update_model
from .readiness import final_readiness
ROOT=Path(__file__).resolve().parents[1]

def foundation():
 s=validate_sources()
 availability={'point_in_time_availability_verified':s['point_in_time_availability_verified'],'leakage_free':False}
 return build_foundation_report(ROOT,availability)

def main():
 p=argparse.ArgumentParser(); p.add_argument('command',choices=['run','verify','ingest','ingest-history','audit-foundation','audit-final']); a=p.parse_args()
 if a.command=='run': print(json.dumps(run(),indent=2))
 elif a.command=='ingest': print(json.dumps(ingest_current(),indent=2))
 elif a.command=='ingest-history': print(json.dumps(ingest_history(),indent=2))
 elif a.command=='audit-foundation': print(json.dumps(foundation(),indent=2))
 elif a.command=='audit-final':
  f=foundation(); state=update_model(validate_sources(),f)
  print(json.dumps({'foundation':f,'readiness':final_readiness(f,state)},indent=2))
 else:
  e=verify(ROOT)
  if e: raise SystemExit('\n'.join(e))
  print('forecast registry integrity: OK')
if __name__=='__main__': main()

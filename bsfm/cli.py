import argparse,json
from pathlib import Path
from .pipeline import run,validate_sources
from .registry import verify
from .sources import ingest_current,ingest_history
from .foundation_report import build_foundation_report
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(); p.add_argument('command',choices=['run','verify','ingest','ingest-history','audit-foundation']); a=p.parse_args()
 if a.command=='run': print(json.dumps(run(),indent=2))
 elif a.command=='ingest': print(json.dumps(ingest_current(),indent=2))
 elif a.command=='ingest-history': print(json.dumps(ingest_history(),indent=2))
 elif a.command=='audit-foundation':
  s=validate_sources(); availability={'point_in_time_availability_verified':s['point_in_time_availability_verified'],'leakage_free':False}
  print(json.dumps(build_foundation_report(ROOT,availability),indent=2))
 else:
  e=verify(ROOT)
  if e: raise SystemExit('\n'.join(e))
  print('forecast registry integrity: OK')
if __name__=='__main__': main()

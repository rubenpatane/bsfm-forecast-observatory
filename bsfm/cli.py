import argparse,json
from pathlib import Path
from .pipeline import run
from .registry import verify
from .sources import ingest_all
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(); p.add_argument('command',choices=['run','verify','ingest']); a=p.parse_args()
 if a.command=='run': print(json.dumps(run(),indent=2))
 elif a.command=='ingest': print(json.dumps(ingest_all(),indent=2))
 else:
  e=verify(ROOT)
  if e: raise SystemExit('\n'.join(e))
  print('forecast registry integrity: OK')
if __name__=='__main__': main()

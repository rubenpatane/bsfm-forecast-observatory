from __future__ import annotations
import csv, hashlib, io, json, urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FAA_SDR='https://external.apic4e.faa.gov/sdrs/retrieve/SDR-{year}.csv'

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def sha(b:bytes): return hashlib.sha256(b).hexdigest()
def fetch(url:str,timeout=90)->bytes:
 req=urllib.request.Request(url,headers={'User-Agent':'BSFM-Forecast-Observatory/1.0 (+https://github.com/rubenpatane/bsfm-forecast-observatory)'})
 with urllib.request.urlopen(req,timeout=timeout) as r: return r.read()
def ingest_faa_sdr(year:int|None=None):
 year=year or date.today().year; url=FAA_SDR.format(year=year); raw=fetch(url)
 text=raw.decode('utf-8-sig',errors='replace'); reader=csv.DictReader(io.StringIO(text)); rows=0; boeing=0; max_date=None
 for r in reader:
  rows+=1
  if 'BOEING' in (r.get('AircraftMake') or '').upper(): boeing+=1
  d=(r.get('DifficultyDate') or '').strip()
  if d and (max_date is None or d>max_date): max_date=d
 m={'schema':'bsfm.source-manifest.v1','source':'FAA SDR','year':year,'official_url':url,'retrieved_at':now(),'sha256':sha(raw),'bytes':len(raw),'rows':rows,'boeing_rows':boeing,'max_difficulty_date_raw':max_date,'status':'validated' if rows>0 else 'invalid','validation':['http_download_ok','csv_parse_ok','nonempty']}
 p=ROOT/'data'/'manifests'/f'faa-sdr-{year}.json'; p.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n'); return m

def ingest_all(): return {'faa_sdr':ingest_faa_sdr()}

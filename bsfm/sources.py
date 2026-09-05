from __future__ import annotations
import csv,hashlib,io,json,urllib.request
from datetime import date,datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FAA='https://external.apic4e.faa.gov/sdrs/retrieve/SDR-{year}.csv'
NTSB='https://data.ntsb.gov/avdata/avall.zip'
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def sha(b): return hashlib.sha256(b).hexdigest()
def fetch(url,timeout=120):
 req=urllib.request.Request(url,headers={'User-Agent':'BSFM-Research-Observatory/1.2'})
 with urllib.request.urlopen(req,timeout=timeout) as r: return r.read()
def manifest(name,data):
 p=ROOT/'data'/'manifests'/name; p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n'); return data
def ingest_faa_sdr(year):
 raw=fetch(FAA.format(year=year)); rd=csv.DictReader(io.StringIO(raw.decode('utf-8-sig',errors='replace'))); rows=boeing=0
 for r in rd:
  rows+=1; boeing+=int('BOEING' in (r.get('AircraftMake') or '').upper())
 d={'schema':'bsfm.source-manifest.v1','source':'FAA SDR','year':year,'official_url':FAA.format(year=year),'retrieved_at':now(),'sha256':sha(raw),'bytes':len(raw),'rows':rows,'boeing_rows':boeing,'status':'validated' if rows else 'invalid'}
 return manifest(f'faa-sdr-{year}.json',d)
def ingest_ntsb_metadata():
 raw=fetch(NTSB); d={'schema':'bsfm.source-manifest.v1','source':'NTSB AVALL','official_url':NTSB,'retrieved_at':now(),'sha256':sha(raw),'bytes':len(raw),'status':'validated' if raw[:2]==b'PK' else 'invalid','note':'Archive fingerprint only. MDB extraction occurs in the dedicated historical-build workflow.'}
 return manifest('ntsb-avall.json',d)
def ingest_current(): return {'faa_sdr':ingest_faa_sdr(date.today().year),'ntsb':ingest_ntsb_metadata()}
def ingest_history(start=2010,end=None):
 end=end or date.today().year; return {'faa_sdr':[ingest_faa_sdr(y) for y in range(start,end+1)]}

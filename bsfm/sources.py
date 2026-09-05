from __future__ import annotations
import csv,hashlib,io,json,urllib.request
from datetime import date,datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FAA='https://external.apic4e.faa.gov/sdrs/retrieve/SDR-{year}.csv'
NTSB='https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5Cavall.zip'
REQUIRED_SDR={'DifficultyDate','AircraftMake','AircraftModel','JASCCode'}
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def sha(b): return hashlib.sha256(b).hexdigest()
def fetch(url,timeout=120):
 req=urllib.request.Request(url,headers={'User-Agent':'BSFM-Research-Observatory/1.2'})
 with urllib.request.urlopen(req,timeout=timeout) as r: return r.read()
def manifest(name,data):
 p=ROOT/'data'/'manifests'/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n'); return data
def parse_sdr_date(value):
 value=(value or '').strip()
 for fmt in ('%m/%d/%Y','%Y-%m-%d','%m/%d/%y'):
  try: return datetime.strptime(value,fmt).date()
  except ValueError: pass
 return None
def inspect_faa_csv(raw):
 rd=csv.DictReader(io.StringIO(raw.decode('utf-8-sig',errors='replace'))); fields=set(rd.fieldnames or []); rows=boeing=bad_dates=0; dates=[]
 for r in rd:
  rows+=1; boeing+=int('BOEING' in (r.get('AircraftMake') or '').upper()); value=(r.get('DifficultyDate') or '').strip()
  if value:
   d=parse_sdr_date(value)
   if d: dates.append(d)
   else: bad_dates+=1
 return {'rows':rows,'boeing_rows':boeing,'fields':sorted(fields),'missing_fields':sorted(REQUIRED_SDR-fields),'bad_dates':bad_dates,'min_date':min(dates).isoformat() if dates else None,'max_date':max(dates).isoformat() if dates else None}
def ingest_faa_sdr(year):
 raw=fetch(FAA.format(year=year)); stats=inspect_faa_csv(raw); valid=stats['rows']>0 and not stats['missing_fields'] and stats['bad_dates']==0
 return manifest(f'faa-sdr-{year}.json',{'schema':'bsfm.source-manifest.v1','source':'FAA SDR','year':year,'official_url':FAA.format(year=year),'retrieved_at':now(),'sha256':sha(raw),'bytes':len(raw),**stats,'status':'validated' if valid else 'invalid','validation':['http_download_ok','csv_parse_ok','required_schema','difficulty_date_parse']})
def ingest_ntsb_metadata():
 raw=fetch(NTSB); is_zip=raw[:4]==b'PK\x03\x04'
 return manifest('ntsb-avall.json',{'schema':'bsfm.source-manifest.v1','source':'NTSB AVALL','official_url':NTSB,'retrieved_at':now(),'sha256':sha(raw),'bytes':len(raw),'status':'validated' if is_zip and len(raw)>1024 else 'invalid','validation':['http_download_ok','zip_signature','nontrivial_size'],'note':'Archive fingerprint only. MDB tables are exported in the dedicated historical source build.'})
def ingest_current(): return {'faa_sdr':ingest_faa_sdr(date.today().year),'ntsb':ingest_ntsb_metadata()}
def ingest_history(start=2010,end=None):
 end=end or date.today().year
 if start>end: raise ValueError('start year must not exceed end year')
 return {'faa_sdr':[ingest_faa_sdr(y) for y in range(start,end+1)]}

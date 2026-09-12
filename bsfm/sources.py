from __future__ import annotations
import csv,hashlib,io,json,urllib.request
from collections import Counter
from datetime import date,datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FAA='https://external.apic4e.faa.gov/sdrs/retrieve/SDR-{year}.csv'
NTSB='https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5Cavall.zip'
REQUIRED_SDR={'DifficultyDate','SubmissionDate','AircraftMake','AircraftModel','JASCCode'}
F002_CUTOFF=date(2026,8,19)
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def sha(b): return hashlib.sha256(b).hexdigest()
def fetch(url,timeout=120):
 req=urllib.request.Request(url,headers={'User-Agent':'BSFM-Research-Observatory/1.2'})
 with urllib.request.urlopen(req,timeout=timeout) as r: return r.read()
def manifest(name,data):
 p=ROOT/'data'/'manifests'/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n'); return data
def parse_sdr_date(value):
 value=(value or '').strip()
 if not value: return None
 # FAA instructions use yyyy/mm/dd for the submission date embedded in the
 # unique control number; yearly exports have also used conventional US and
 # ISO-like representations. Parsing is deliberately explicit, not locale based.
 for fmt in ('%m/%d/%Y','%Y/%m/%d','%Y-%m-%d','%m/%d/%y','%Y%m%d','%Y-%m-%d %H:%M:%S','%m/%d/%Y %H:%M:%S'):
  try: return datetime.strptime(value,fmt).date()
  except ValueError: pass
 try: return datetime.fromisoformat(value.replace('Z','+00:00')).date()
 except ValueError: return None
def inspect_faa_csv(raw):
 rd=csv.DictReader(io.StringIO(raw.decode('utf-8-sig',errors='replace'))); fields=set(rd.fieldnames or [])
 rows=boeing=bad_dates=bad_submission_dates=0; dates=[]; submissions=[]; bad_submission_examples=[]
 for r in rd:
  rows+=1; boeing+=int('BOEING' in (r.get('AircraftMake') or '').upper())
  value=(r.get('DifficultyDate') or '').strip()
  if value:
   d=parse_sdr_date(value)
   if d: dates.append(d)
   else: bad_dates+=1
  value=(r.get('SubmissionDate') or '').strip()
  if value:
   d=parse_sdr_date(value)
   if d: submissions.append(d)
   else:
    bad_submission_dates+=1
    if len(bad_submission_examples)<3: bad_submission_examples.append(value[:32])
 return {
  'rows':rows,'boeing_rows':boeing,'fields':sorted(fields),'missing_fields':sorted(REQUIRED_SDR-fields),
  'bad_dates':bad_dates,'min_date':min(dates).isoformat() if dates else None,'max_date':max(dates).isoformat() if dates else None,
  'bad_submission_dates':bad_submission_dates,'bad_submission_examples':bad_submission_examples,
  'min_submission_date':min(submissions).isoformat() if submissions else None,
  'max_submission_date':max(submissions).isoformat() if submissions else None,
  'historical_public_availability':'unverified',
 }
def _clean(value,limit=220):
 value=' '.join((value or '').split())
 return value[:limit]
def _sdr_similarity(model,stage,component,discrepancy):
 text=' '.join((component,discrepancy)).upper(); compact=model.upper().replace('BOEING','').replace(' ','').replace('-','')
 exact=compact.startswith('7378') and 'MAX' not in compact
 family=compact.startswith(('7376','7377','7378','7379')) and 'MAX' not in compact
 approach_landing=stage.upper() in {'APP','AP','LND','LDG','LA'} or any(x in text for x in ('APPROACH','LANDING','TOUCHDOWN'))
 gear_structural=any(x in text for x in ('LANDING GEAR','GEAR','TIRE','TYRE','BRAKE','STRUCTUR','FUSELAGE','TAIL STRIKE','HARD LANDING','HYDRAULIC'))
 propulsion=any(x in text for x in ('ENGINE','PROPULSION','THRUST','FAN BLADE'))
 tags=[]
 if exact: tags.append('exact_model')
 if family: tags.append('family_737_ng')
 if approach_landing: tags.append('approach_landing')
 if gear_structural: tags.append('gear_structural_cluster')
 if propulsion: tags.append('alternative_propulsion')
 score=(4 if exact else 0)+(2 if family else 0)+(3 if approach_landing else 0)+(2 if gear_structural else 0)+(1 if propulsion else 0)
 return tags,score
def summarize_faa_public(raw,limit=12):
 """Build a small public, auditable view of the current FAA SDR export.

 The rows are observations from the official SDR feed, not accident labels and
 not model predictions. They are sorted by DifficultyDate and deliberately keep
 only operationally useful public fields; free text is truncated for the site.
 """
 rd=csv.DictReader(io.StringIO(raw.decode('utf-8-sig',errors='replace')))
 records=[]; similar=[]; models=Counter(); stages=Counter(); conditions=Counter(); total=boeing=0
 for r in rd:
  total+=1
  if 'BOEING' not in (r.get('AircraftMake') or '').upper(): continue
  boeing+=1
  model=_clean(r.get('AircraftModel'),64) or '—'; models[model]+=1
  stage=_clean(r.get('StageOfOperationCode'),64) or '—'; stages[stage]+=1
  condition=_clean(r.get('NatureOfConditionA'),64) or '—'; conditions[condition]+=1
  d=parse_sdr_date(r.get('DifficultyDate'))
  public_row={
   'date':d.isoformat() if d else None,
   'model':model,
   'jasc_code':_clean(r.get('JASCCode'),32) or '—',
   'stage_code':stage,
   'condition_code':condition,
   'component':_clean(r.get('ComponentName') or r.get('PartName'),96) or '—',
   'discrepancy':_clean(r.get('Discrepancy'),220) or '—',
  }
  records.append(public_row)
  tags,score=_sdr_similarity(model,stage,public_row['component'],public_row['discrepancy'])
  if d and d>=F002_CUTOFF and ({'exact_model','family_737_ng'} & set(tags)) and ({'approach_landing','gear_structural_cluster','alternative_propulsion'} & set(tags)):
   similar.append({**public_row,'similarity_tags':tags,'similarity_score':score,'source':'FAA SDR','record_type':'service_difficulty_report'})
 records.sort(key=lambda x:(x['date'] or '',x['model']),reverse=True)
 similar.sort(key=lambda x:(x['similarity_score'],x['date'] or ''),reverse=True)
 def top(counter,n=8): return [{'value':k,'count':v} for k,v in counter.most_common(n)]
 return {
  'schema':'bsfm.public-real-data.v1',
  'generated_at':now(),
  'source':'FAA Service Difficulty Reports (SDR)',
  'source_scope':'Official current-year FAA SDR export; Boeing rows only for model-oriented summaries.',
  'interpretation_warning':'An SDR is a service-difficulty report, not necessarily an accident, a verified causal finding, or a BSFM prediction.',
  'rows_total':total,
  'boeing_rows':boeing,
  'latest_observation_date':next((r['date'] for r in records if r['date']),None),
  'top_models':top(models),
  'top_stage_codes':top(stages),
  'top_condition_codes':top(conditions),
  'latest_boeing_reports':records[:limit],
  'similarity_rule':'After F-002 cutoff; 737-800/737-NG plus approach/landing, gear/structural/operational or alternative propulsion text/code; fixed weighted score. SDRs are reports, not accident classifications or forecast hits.',
  'similar_boeing_reports':similar[:8],
 }
def write_public_real_data(summary):
 p=ROOT/'site'/'data'/'real-data.json'; p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 return summary
def ingest_faa_sdr(year):
 raw=fetch(FAA.format(year=year)); stats=inspect_faa_csv(raw)
 # Content validity and leakage-safe historical availability are distinct gates.
 # A valid FAA export must not be called invalid merely because public approval
 # time cannot be reconstructed. The model gate checks availability separately.
 valid=stats['rows']>0 and not stats['missing_fields'] and stats['bad_dates']==0
 submission_parse='ok' if stats['bad_submission_dates']==0 else 'diagnostic_failed'
 if year==date.today().year: write_public_real_data(summarize_faa_public(raw))
 return manifest(f'faa-sdr-{year}.json',{
  'schema':'bsfm.source-manifest.v1','source':'FAA SDR','year':year,'official_url':FAA.format(year=year),'retrieved_at':now(),
  'sha256':sha(raw),'bytes':len(raw),**stats,'status':'validated' if valid else 'invalid',
  'validation':['http_download_ok','csv_parse_ok','required_schema','difficulty_date_parse'],
  'submission_date_parse':submission_parse,
  'point_in_time_note':'SubmissionDate is a submission-timing field, but the FAA public query states recently submitted SDRs are unavailable until FAA approval. Without an approval/publication timestamp, SubmissionDate is not treated as public availability for leakage-sensitive backtests.'
 })
def ingest_ntsb_metadata():
 raw=fetch(NTSB); is_zip=raw[:4]==b'PK\x03\x04'
 return manifest('ntsb-avall.json',{'schema':'bsfm.source-manifest.v1','source':'NTSB AVALL','official_url':NTSB,'retrieved_at':now(),'sha256':sha(raw),'bytes':len(raw),'status':'validated' if is_zip and len(raw)>1024 else 'invalid','validation':['http_download_ok','zip_signature','nontrivial_size'],'note':'Archive fingerprint only. MDB tables are exported in the dedicated historical source build.'})
def ingest_current(): return {'faa_sdr':ingest_faa_sdr(date.today().year),'ntsb':ingest_ntsb_metadata()}
def ingest_history(start=2010,end=None):
 end=end or date.today().year
 if start>end: raise ValueError('start year must not exceed end year')
 return {'faa_sdr':[ingest_faa_sdr(y) for y in range(start,end+1)]}

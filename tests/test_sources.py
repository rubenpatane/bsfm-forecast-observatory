from bsfm.sources import sha,parse_sdr_date,inspect_faa_csv,summarize_faa_public

def test_sha_is_deterministic():
 assert sha(b'bsfm')==sha(b'bsfm')
 assert sha(b'bsfm')!=sha(b'BSFM')

def test_sdr_date_parser_is_not_lexicographic():
 assert parse_sdr_date('12/31/2025').isoformat()=='2025-12-31'
 assert parse_sdr_date('01/02/2026').isoformat()=='2026-01-02'
 assert parse_sdr_date('2026/01/03').isoformat()=='2026-01-03'
 assert parse_sdr_date('20260104').isoformat()=='2026-01-04'
 assert parse_sdr_date('2026-01-05T12:34:56Z').isoformat()=='2026-01-05'
 assert parse_sdr_date('not-a-date') is None

def test_faa_csv_requires_scientific_fields_and_audits_submission():
 raw=b'DifficultyDate,SubmissionDate,AircraftMake,AircraftModel,JASCCode\n01/02/2026,2026/01/03,BOEING,737-800,3210\n'
 x=inspect_faa_csv(raw)
 assert x['rows']==1 and x['boeing_rows']==1
 assert x['missing_fields']==[] and x['bad_dates']==0 and x['bad_submission_dates']==0
 assert x['max_date']=='2026-01-02' and x['max_submission_date']=='2026-01-03'
 assert x['historical_public_availability']=='unverified'

def test_faa_csv_keeps_bad_submission_as_diagnostic_not_event_date_failure():
 raw=b'DifficultyDate,SubmissionDate,AircraftMake,AircraftModel,JASCCode\n01/02/2026,opaque,BOEING,737-800,3210\n'
 x=inspect_faa_csv(raw)
 assert x['bad_dates']==0 and x['bad_submission_dates']==1
 assert x['bad_submission_examples']==['opaque']

def test_faa_csv_reports_missing_schema():
 x=inspect_faa_csv(b'DifficultyDate,AircraftMake\n01/02/2026,BOEING\n')
 assert x['missing_fields']==['AircraftModel','JASCCode','SubmissionDate']

def test_public_faa_summary_is_boeing_only_sorted_and_descriptive():
 raw=(
  'DifficultyDate,SubmissionDate,AircraftMake,AircraftModel,JASCCode,StageOfOperationCode,NatureOfConditionA,ComponentName,Discrepancy\n'
  '09/02/2026,2026/09/03,BOEING,737-800,3210,LDG,CRACK,GEAR,Earlier report\n'
  '09/04/2026,2026/09/05,AIRBUS,A320,1111,CRZ,OTHER,PANEL,Not Boeing\n'
  '09/05/2026,2026/09/05,BOEING,737-800,3220,APP,WORN,BRAKE,Latest report\n'
  '09/03/2026,2026/09/04,BOEING,777-300,7200,CRZ,LEAK,ENGINE,Middle report\n'
 ).encode()
 x=summarize_faa_public(raw,limit=2)
 assert x['schema']=='bsfm.public-real-data.v1'
 assert x['rows_total']==4 and x['boeing_rows']==3
 assert x['latest_observation_date']=='2026-09-05'
 assert [r['model'] for r in x['latest_boeing_reports']]==['737-800','777-300']
 assert x['top_models'][0]=={'value':'737-800','count':2}
 assert 'not necessarily an accident' in x['interpretation_warning']
 assert all('AIRBUS' not in str(r) for r in x['latest_boeing_reports'])

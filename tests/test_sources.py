from bsfm.sources import sha,parse_sdr_date,inspect_faa_csv

def test_sha_is_deterministic():
 assert sha(b'bsfm')==sha(b'bsfm')
 assert sha(b'bsfm')!=sha(b'BSFM')

def test_sdr_date_parser_is_not_lexicographic():
 assert parse_sdr_date('12/31/2025').isoformat()=='2025-12-31'
 assert parse_sdr_date('01/02/2026').isoformat()=='2026-01-02'
 assert parse_sdr_date('not-a-date') is None

def test_faa_csv_requires_scientific_fields_and_audits_submission():
 raw=b'DifficultyDate,SubmissionDate,AircraftMake,AircraftModel,JASCCode\n01/02/2026,01/03/2026,BOEING,737-800,3210\n'
 x=inspect_faa_csv(raw)
 assert x['rows']==1 and x['boeing_rows']==1
 assert x['missing_fields']==[] and x['bad_dates']==0 and x['bad_submission_dates']==0
 assert x['max_date']=='2026-01-02' and x['max_submission_date']=='2026-01-03'
 assert x['historical_public_availability']=='unverified'

def test_faa_csv_reports_missing_schema():
 x=inspect_faa_csv(b'DifficultyDate,AircraftMake\n01/02/2026,BOEING\n')
 assert x['missing_fields']==['AircraftModel','JASCCode','SubmissionDate']

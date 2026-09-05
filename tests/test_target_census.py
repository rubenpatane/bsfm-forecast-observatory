from bsfm.target_census import validate_target,qualifying_targets,audit_census

def base():
 return {'event_date':'2024-01-02','manufacturer':'Boeing','model':'737-800','commercial':True,'jet':True,'fatalities':1,'sources':[{'publisher':'ICAO'},{'publisher':'EASA'}]}

def test_requires_two_independent_publishers():
 r=base(); r['sources']=[{'publisher':'Boeing'}]
 assert not validate_target(r)['valid']
 assert not validate_target(r)['qualifies']

def test_qualifying_target_is_explicit():
 r=base()
 assert validate_target(r)['qualifies']
 assert qualifying_targets([r])==[r]

def test_nonfatal_or_noncommercial_does_not_qualify():
 r=base(); r['fatalities']=0
 assert not validate_target(r)['qualifies']
 r=base(); r['commercial']=None
 assert not validate_target(r)['qualifies']
 assert 'commercial_not_explicit_boolean' in validate_target(r)['errors']

def test_invalid_fatalities_fail_closed():
 r=base(); r['fatalities']='unknown'
 assert not validate_target(r)['valid']
 assert not validate_target(r)['qualifies']

def test_census_requires_explicit_attestation_even_for_zero_event_years():
 r=base(); r['event_date']='2024-01-02'
 audit=audit_census([r],2023,2024,{2024:{'reconciled':True,'publishers':['ICAO','EASA']}})
 assert not audit['complete'] and audit['missing_attested_years']==[2023]
 audit=audit_census([r],2023,2024,{2023:{'reconciled':True,'publishers':['ICAO','EASA']},2024:{'reconciled':True,'publishers':['ICAO','EASA']}})
 assert audit['complete']

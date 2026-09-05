from bsfm.target_census import validate_target,qualifying_targets,audit_census

def base():
 return {'event_date':'2024-01-02','manufacturer':'Boeing','model':'737-800','commercial':True,'jet':True,'fatalities':1,'sources':[{'publisher':'ICAO'},{'publisher':'EASA'}]}

def att(n):
 return {'reconciled':True,'publishers':['ICAO','EASA'],'qualifying_boeing_events':n,'scope':'global-commercial-jet','provenance':['icao-report','easa-asr']}

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
 audit=audit_census([r],2023,2024,{2024:att(1)})
 assert not audit['complete'] and audit['missing_attested_years']==[2023]
 audit=audit_census([r],2023,2024,{2023:att(0),2024:att(1)})
 assert audit['complete']

def test_census_rejects_attested_count_that_disagrees_with_rows():
 r=base()
 audit=audit_census([r],2024,2024,{2024:att(0)})
 assert not audit['complete']
 assert audit['count_mismatches']==[{'year':2024,'attested':0,'observed':1}]

def test_census_attestation_requires_scope_and_provenance():
 weak=att(1); weak['provenance']=[]
 audit=audit_census([base()],2024,2024,{2024:weak})
 assert not audit['complete'] and audit['weak_attestations']==[2024]

def test_census_null_publishers_fail_closed_instead_of_crashing():
 weak=att(1); weak['publishers']=None
 audit=audit_census([base()],2024,2024,{2024:weak})
 assert not audit['complete']
 assert audit['weak_attestations']==[2024]

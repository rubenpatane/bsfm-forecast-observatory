from bsfm.target_census import validate_target,qualifying_targets

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

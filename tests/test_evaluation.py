from bsfm.evaluation import score_f002_event,classify_f002_event

def test_nonfatal_descriptive_match_is_never_target_hit():
 e={'event_date':'2026-10-08','fatal':False,'commercial':True,'make':'Boeing','model':'737-800','phase':'landing','event_class':'landing gear'}
 s=score_f002_event(e)
 assert s['aircraft_exact'] and s['phase'] and s['failure_primary'] and s['time_window']
 assert not s['qualifying_target'] and not s['full_primary_match']
 assert classify_f002_event(e)=='descriptive_partial_only'

def test_pre_cutoff_event_cannot_qualify():
 e={'event_date':'2026-08-18','fatal':True,'commercial':True,'make':'Boeing','model':'737-800','phase':'landing','event_class':'SCF-NP landing gear'}
 assert not score_f002_event(e)['qualifying_target']

def test_target_occurrence_is_separate_from_dimension_match():
 e={'event_date':'2026-09-01','fatal':True,'commercial':True,'make':'Boeing','model':'787-9','phase':'cruise','event_class':'other'}
 s=score_f002_event(e)
 assert s['qualifying_target'] and not s['full_primary_match']
 assert classify_f002_event(e)=='qualifying_target_dimension_miss'

def test_full_primary_match_and_modal_error():
 e={'event_date':'2026-10-08','fatal':True,'commercial':True,'make':'Boeing','model':'737-800','phase':'landing','event_class':'SCF-NP landing gear','region':'Europe'}
 s=score_f002_event(e)
 assert s['full_primary_match'] and s['modal_day'] and s['absolute_day_error']==0 and s['geography_supported']

def test_secondary_max8_and_propulsion_are_scored_separately():
 e={'event_date':'2026-10-10','fatal':False,'commercial':True,'make':'Boeing','model':'737 MAX 8','phase':'approach','event_class':'engine propulsion'}
 s=score_f002_event(e)
 assert s['aircraft_secondary'] and s['failure_alternative'] and s['absolute_day_error']==2

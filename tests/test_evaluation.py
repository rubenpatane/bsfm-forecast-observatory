from bsfm.evaluation import score_f002_event,classify_f002_event

def test_nonfatal_descriptive_match_is_never_primary_hit():
 e={'event_date':'2026-10-08','fatal':False,'commercial':True,'make':'Boeing','model':'737-800','phase':'landing','event_class':'landing gear'}
 s=score_f002_event(e)
 assert s['aircraft_exact'] and s['phase'] and s['failure_class'] and s['time_window']
 assert not s['qualifying_target'] and not s['primary_hit_candidate']
 assert classify_f002_event(e)=='descriptive_partial_only'

def test_pre_cutoff_event_cannot_qualify():
 e={'event_date':'2026-08-18','fatal':True,'commercial':True,'make':'Boeing','model':'737-800','phase':'landing','event_class':'SCF-NP landing gear'}
 assert not score_f002_event(e)['qualifying_target']

def test_candidate_requires_all_preregistered_primary_dimensions():
 e={'event_date':'2026-10-08','fatal':True,'commercial':True,'make':'Boeing','model':'737-800','phase':'landing','event_class':'SCF-NP landing gear'}
 assert score_f002_event(e)['primary_hit_candidate']

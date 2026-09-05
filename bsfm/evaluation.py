from __future__ import annotations
from datetime import date

def _norm(value): return (value or '').strip().lower()
def _contains(value, needles):
 v=_norm(value); return any(n in v for n in needles)
def score_f002_event(event):
 event_date=date.fromisoformat(event['event_date'])
 fatal=bool(event.get('fatal'))
 commercial=bool(event.get('commercial'))
 boeing=_contains(event.get('make'),('boeing',))
 aircraft_exact=_contains(event.get('model'),('737-800','b737-800'))
 aircraft_family=aircraft_exact or _contains(event.get('model'),('737-700','737-900','737 ng'))
 phase=_contains(event.get('phase'),('approach','landing','final approach'))
 failure=_contains(event.get('event_class'),('scf-np','landing gear','gear','structural'))
 time_window=date(2026,10,5)<=event_date<=date(2026,10,11)
 after_cutoff=event_date>date(2026,8,19)
 qualifying_target=after_cutoff and fatal and commercial and boeing
 return {'aircraft_exact':aircraft_exact,'aircraft_family':aircraft_family,'phase':phase,'failure_class':failure,'time_window':time_window,'qualifying_target':qualifying_target,'primary_hit_candidate':qualifying_target and aircraft_exact and phase and failure and time_window}

def classify_f002_event(event):
 s=score_f002_event(event)
 if s['primary_hit_candidate']: return 'primary_hit_candidate'
 descriptive=sum(bool(s[k]) for k in ('aircraft_exact','phase','failure_class','time_window'))
 if descriptive>=2: return 'descriptive_partial_only'
 return 'no_primary_match'

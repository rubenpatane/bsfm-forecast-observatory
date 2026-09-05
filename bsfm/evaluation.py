from __future__ import annotations
from datetime import date

def _norm(value): return (value or '').strip().lower()
def _contains(value, needles):
 v=_norm(value); return any(n in v for n in needles)
def score_f002_event(event):
 event_date=date.fromisoformat(event['event_date']); modal=date(2026,10,8)
 fatal=bool(event.get('fatal')); commercial=bool(event.get('commercial'))
 boeing=_contains(event.get('make'),('boeing',)); model=_norm(event.get('model'))
 aircraft_exact=any(x in model for x in ('737-800','b737-800','737 800'))
 aircraft_secondary=any(x in model for x in ('737 max 8','737-8 max','737-8','max 8'))
 aircraft_family=aircraft_exact or _contains(model,('737-700','737-900','737 ng','737-600'))
 phase=_contains(event.get('phase'),('approach','landing','final approach','ldg','apr'))
 cls=event.get('event_class'); failure_primary=_contains(cls,('scf-np','landing gear','gear','structural'))
 failure_alternative=_contains(cls,('propulsion','engine','powerplant','scf-pp'))
 region=_norm(event.get('region')); geography_supported=region in {'europe','north america','apac','asia-pacific','asia pacific'}
 time_window=date(2026,10,5)<=event_date<=date(2026,10,11); after_cutoff=event_date>date(2026,8,19)
 qualifying_target=after_cutoff and fatal and commercial and boeing
 full_primary_match=qualifying_target and aircraft_exact and phase and failure_primary and time_window
 return {
  'qualifying_target':qualifying_target,
  'aircraft_exact':aircraft_exact,'aircraft_family':aircraft_family,'aircraft_secondary':aircraft_secondary,
  'phase':phase,'failure_class':failure_primary,'failure_primary':failure_primary,'failure_alternative':failure_alternative,
  'time_window':time_window,'modal_day':event_date==modal,'absolute_day_error':abs((event_date-modal).days),
  'geography_supported':geography_supported,
  # Kept for backward compatibility: this is a multidimensional match, not the definition of target occurrence.
  'primary_hit_candidate':full_primary_match,'full_primary_match':full_primary_match,
 }

def classify_f002_event(event):
 s=score_f002_event(event)
 if s['full_primary_match']: return 'full_primary_match'
 if s['qualifying_target']: return 'qualifying_target_dimension_miss'
 descriptive=sum(bool(s[k]) for k in ('aircraft_exact','aircraft_secondary','phase','failure_primary','failure_alternative','time_window'))
 if descriptive>=2: return 'descriptive_partial_only'
 return 'no_primary_match'

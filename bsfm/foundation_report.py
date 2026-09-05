from __future__ import annotations
from pathlib import Path
from .historical_io import load_json,load_jsonl,ledger_attestations
from .target_census import audit_census,qualifying_targets
from .exposure import audit_exposure
from .historical_foundation import audit_historical_foundation,build_walk_forward_cases

DEFAULT_COHORTS=('737-Classic','737-NG','737-MAX','747','757','767','777','787')


def build_foundation_report(root, availability_audit=None, cohorts=DEFAULT_COHORTS, start_year=2010, end_year=2025):
    root=Path(root)
    ledger=load_json(root/'data/census/year-ledger.json')
    events=load_jsonl(root/'data/census/events.jsonl')
    exposure=load_jsonl(root/'data/exposure/departures.jsonl')
    census=audit_census(events,start_year,end_year,ledger_attestations(ledger))
    exposure_audit=audit_exposure(exposure,[str(y) for y in range(start_year,end_year+1)],cohorts)
    foundation=audit_historical_foundation(census,exposure_audit,availability_audit)
    cases=build_walk_forward_cases(qualifying_targets(events),start_year,end_year) if census['complete'] else []
    return {
        'schema':'bsfm.historical-foundation-report.v1',
        'evaluation_interval':{'start_year':start_year,'end_year':end_year},
        'cohorts':list(cohorts),
        'census':census,
        'exposure':exposure_audit,
        'walk_forward_cases':len(cases),
        **foundation,
        'calibration_evaluated':False,
        'note':'Calibration remains false until real leakage-free probabilistic historical predictions exist.'
    }

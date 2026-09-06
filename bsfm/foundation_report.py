from __future__ import annotations
from pathlib import Path
from .historical_io import load_jsonl
from .g1_census import audit_integrated_g1_census
from .exposure import audit_exposure
from .historical_foundation import audit_historical_foundation,build_walk_forward_cases

DEFAULT_COHORTS=('727','737-Original','737-Classic','737-NG','737-MAX','747','757','767','777','787')


def build_foundation_report(root, availability_audit=None, cohorts=DEFAULT_COHORTS, start_year=2010, end_year=2025):
    root=Path(root)
    exposure=load_jsonl(root/'data/exposure/departures.jsonl')
    census=audit_integrated_g1_census(root,start_year,end_year)
    walk_rows=census.pop('rows_for_walk_forward',[])
    exposure_audit=audit_exposure(exposure,[str(y) for y in range(start_year,end_year+1)],cohorts)
    foundation=audit_historical_foundation(census,exposure_audit,availability_audit)
    cases=build_walk_forward_cases(walk_rows,start_year,end_year) if census['complete'] else []
    return {
        'schema':'bsfm.historical-foundation-report.v3',
        'evaluation_interval':{'start_year':start_year,'end_year':end_year},
        'cohorts':list(cohorts),
        'census':census,
        'exposure':exposure_audit,
        'walk_forward_cases':len(cases),
        **foundation,
        'calibration_evaluated':False,
        'paired_baseline_comparison':False,
        'candidate_better_than_baseline':False,
        'note':'Post-fit promotion evidence remains false until the integrated G1 census, compatible G2 exposure and strict G3 PIT evidence pass and real leakage-free probabilistic historical predictions are paired against the exposure-only baseline.'
    }

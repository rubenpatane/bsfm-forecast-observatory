from __future__ import annotations
from datetime import date

REQUIRED=("event_date","manufacturer","model","commercial","jet","fatalities","sources")

def validate_target(row: dict) -> dict:
    missing=[k for k in REQUIRED if k not in row]
    errors=[]
    try:
        event_date=date.fromisoformat(str(row.get("event_date",""))[:10])
    except ValueError:
        event_date=None; errors.append("invalid_event_date")
    if row.get('commercial') not in (True,False): errors.append('commercial_not_explicit_boolean')
    if row.get('jet') not in (True,False): errors.append('jet_not_explicit_boolean')
    try:
        fatalities=int(row.get('fatalities'))
        if fatalities<0: errors.append('negative_fatalities')
    except (TypeError,ValueError):
        fatalities=0; errors.append('invalid_fatalities')
    sources=row.get("sources") or []
    independent={str(s.get("publisher","" )).strip().lower() for s in sources if isinstance(s,dict) and str(s.get('publisher','')).strip()}
    if len(independent)<2: errors.append("insufficient_independent_provenance")
    qualifies=(not missing and not errors and str(row.get("manufacturer","")).strip().lower()=="boeing" and row.get("commercial") is True and row.get("jet") is True and fatalities>0)
    return {"valid":not missing and not errors,"qualifies":qualifies,"missing":missing,"errors":errors,'event_year':event_date.year if event_date else None,'independent_publishers':sorted(independent)}

def qualifying_targets(rows):
    return [row for row in rows if validate_target(row)["qualifies"]]

def audit_census(rows,start_year=2010,end_year=2025,year_attestations=None):
    """Fail-closed census audit.

    Event rows alone cannot prove that years with zero qualifying Boeing events were
    actually searched. year_attestations therefore records explicit annual source
    reconciliation, including zero-event years.
    """
    rows=list(rows); attest=year_attestations or {}
    invalid=[]; qualified=[]
    for i,row in enumerate(rows):
        check=validate_target(row)
        if not check['valid']: invalid.append({'index':i,'errors':check['errors'],'missing':check['missing']})
        if check['qualifies']: qualified.append(row)
    expected=set(range(start_year,end_year+1))
    attested=set()
    weak=[]
    for y,meta in attest.items():
        try: year=int(y)
        except (TypeError,ValueError): continue
        pubs={str(x).strip().lower() for x in (meta or {}).get('publishers',[]) if str(x).strip()}
        if (meta or {}).get('reconciled') is True and len(pubs)>=2: attested.add(year)
        else: weak.append(year)
    missing_years=sorted(expected-attested)
    out_of_range=[r.get('event_date') for r in qualified if validate_target(r)['event_year'] not in expected]
    return {'complete':not invalid and not missing_years and not out_of_range,'rows':len(rows),'qualifying_rows':len(qualified),'invalid_rows':invalid,'missing_attested_years':missing_years,'weak_attestations':sorted(set(weak)&expected),'out_of_range_qualifying_events':out_of_range}

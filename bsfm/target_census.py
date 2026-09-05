from __future__ import annotations
from datetime import date

REQUIRED=("event_date","manufacturer","model","commercial","jet","fatalities","sources")

def validate_target(row: dict) -> dict:
    missing=[k for k in REQUIRED if k not in row]
    errors=[]
    try:
        date.fromisoformat(str(row.get("event_date",""))[:10])
    except ValueError:
        errors.append("invalid_event_date")
    sources=row.get("sources") or []
    independent={str(s.get("publisher","" )).strip().lower() for s in sources if isinstance(s,dict)}
    if len(independent)<2:
        errors.append("insufficient_independent_provenance")
    qualifies=(
        not missing and not errors
        and str(row.get("manufacturer","")).strip().lower()=="boeing"
        and row.get("commercial") is True
        and row.get("jet") is True
        and int(row.get("fatalities") or 0)>0
    )
    return {"valid":not missing and not errors,"qualifies":qualifies,"missing":missing,"errors":errors}

def qualifying_targets(rows):
    return [row for row in rows if validate_target(row)["qualifies"]]

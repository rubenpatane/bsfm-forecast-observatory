from __future__ import annotations
import json
from pathlib import Path
from .annual_evidence import audit_annual_completeness
from .research_state import build_research_state
from .resolution import audit_resolution


def _load(path, default=None):
    try: return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError): return default


def _load_jsonl(path):
    out=[]
    try:
        for line in Path(path).read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            try: out.append(json.loads(line))
            except json.JSONDecodeError: continue
    except OSError:
        pass
    return out


def _candidate_public(row):
    return {
        'event_id': row.get('event_id'), 'date': row.get('event_date'),
        'flight_number': row.get('flight_number'), 'model': row.get('model'),
        'registration': row.get('registration'), 'msn': row.get('msn'),
        'operator': row.get('operator'), 'phase': row.get('phase'),
        'geography': row.get('location'), 'decision': row.get('decision'),
        'provenance': [x for x in [
            {'publisher':row.get('source_publisher'),'record':row.get('source_record_id'),'locator':row.get('source_locator'),'role':'primary/adjudication'} if row.get('source_publisher') else None,
            *[{'publisher':x.get('publisher'),'record':x.get('record'),'locator':x.get('locator'),'role':'reconciliation'} for x in (row.get('reconciliation_evidence') or [])]
        ] if x],
    }


def _all_candidates(root):
    """Aggregate the central workspace and annual JSONL ledgers by event_id.

    Annual files are appendable research surfaces. If the same event is present in
    both places, the annual JSONL copy wins because it is the narrower evidence
    record. This aggregation affects publication only; it never changes G1 gates.
    """
    root=Path(root); merged={}
    central=_load(root/'data/census/g1-candidates.json',{}) or {}
    for row in central.get('records') or []:
        event_id=row.get('event_id')
        if event_id: merged[event_id]=row
    for path in sorted((root/'data/census').glob('candidates-*.jsonl')):
        for row in _load_jsonl(path):
            event_id=row.get('event_id')
            if event_id: merged[event_id]=row
    return list(merged.values())


def build_public_research_state_from_root(root):
    root=Path(root)
    ledger=_load(root/'data/census/year-ledger.json',{}) or {}
    by_year={}
    for row in _all_candidates(root):
        try: year=int(str(row.get('event_date'))[:4])
        except (TypeError,ValueError): continue
        by_year.setdefault(year,[]).append(_candidate_public(row))
    for rows in by_year.values():
        rows.sort(key=lambda r:(r.get('date') or '',r.get('event_id') or ''))
    annual=[]
    for item in ledger.get('years') or []:
        year=int(item['year'])
        evidence=_load(root/f'data/census/year-evidence-{year}.json',{}) or {}
        controls=evidence.get('controls')
        audit=audit_annual_completeness(year,controls) if isinstance(controls,dict) else None
        evidence_status=str(evidence.get('status') or '')
        status='RECONCILED' if item.get('reconciled') is True else ('UNRESOLVED' if evidence_status.startswith('unresolved') else 'OPEN')
        annual.append({
            'year':year,'status':status,'reconciled':item.get('reconciled') is True,
            'evidence_progress':audit['evidence_progress'] if audit else None,
            'candidate_count':len(by_year.get(year,[])),'events':by_year.get(year,[]),
        })
    exposure_inventory=_load(root/'data/exposure/source-inventory.json',{}) or {}
    resolution_evidence=_load(root/'data/resolution/evidence.json',{}) or {}
    resolution=audit_resolution(resolution_evidence)
    return build_research_state(
        annual,
        {'coverage':exposure_inventory.get('conclusion',{}).get('next_research_direction'),'baseline_present':False},
        {'availability':'not yet field/source/cutoff complete'},
        resolution,
        _load(root/'site/data/refinements.json',[]) or [],
    )


def write_public_research_state(root, out=None):
    root=Path(root); out=Path(out) if out else root/'site/data/research-state.json'
    state=build_public_research_state_from_root(root)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return state

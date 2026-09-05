from __future__ import annotations
import json,re
from datetime import datetime, timezone
from pathlib import Path

from .cohorts import boeing_cohort


def _now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _compact_model(value):
    return str(value or '').upper().replace('BOEING', '').replace(' ', '').replace('_', '-').strip()


def _is_737_800(value):
    m=_compact_model(value)
    if 'MAX' in m: return False
    if '737-800' in m or m.startswith('737800'): return True
    # NTSB commonly stores Boeing customer variants such as 737-832/737-8H4.
    return bool(re.match(r'^737-?8[A-Z0-9]{2,}$',m))


def _is_737_ng(value):
    m=_compact_model(value)
    if boeing_cohort(value)=='737-NG': return True
    if 'MAX' in m: return False
    # Customer-code variants: 737-7H4, 737-824, 737-924ER, etc.
    return bool(re.match(r'^737-?[6789][A-Z0-9]{2,}$',m))


def _phase_match(value):
    p = str(value or '').upper()
    return any(x in p for x in ('APPROACH', 'LANDING', 'FINAL', 'APPR', 'LND'))


def _detail_text(row):
    parts=[]
    for item in row.get('event_sequence') or []:
        parts.extend(str(item.get(k) or '') for k in ('occurrence_description','defining_event'))
    for item in row.get('findings') or []:
        parts.extend(str(item.get(k) or '') for k in ('finding_description','cause_factor'))
    return ' '.join(parts).upper()


def _cluster_match(row):
    text=_detail_text(row)
    return any(x in text for x in ('LANDING GEAR','GEAR COLLAPSE','GEAR FAILURE','STRUCTURAL','FUSELAGE','TAIL STRIKE','HARD LANDING'))


def _tags(row):
    tags=[]
    if _is_737_800(row.get('model')): tags.append('exact_model')
    if _is_737_ng(row.get('model')): tags.append('family_737_ng')
    if _phase_match(row.get('phase')): tags.append('approach_landing')
    if _cluster_match(row): tags.append('gear_structural_cluster')
    return tags


def build_nonfatal_comparables(rows, limit=8):
    """Select recent nonfatal NTSB cases comparable to frozen F-002.

    Selection is descriptive only. A row must be Boeing, nonfatal and commercial,
    belong to the 737-NG / exact 737-800 hypothesis, and also match either the
    approach/landing phase or the gear/structural event cluster. These cases never
    satisfy or score the fatal target of F-002.
    """
    out=[]
    for row in rows:
        if not row.get('boeing') or row.get('fatal') or not row.get('commercial'):
            continue
        tags=_tags(row)
        if not ({'exact_model','family_737_ng'} & set(tags)):
            continue
        if not ({'approach_landing','gear_structural_cluster'} & set(tags)):
            continue
        date=str(row.get('event_date') or '')
        if not date:
            continue
        score=(4 if 'exact_model' in tags else 0)+(2 if 'family_737_ng' in tags else 0)+(3 if 'approach_landing' in tags else 0)+(2 if 'gear_structural_cluster' in tags else 0)
        out.append({
            'event_id': row.get('event_id'),
            'event_date': date,
            'model': row.get('model') or '—',
            'carrier': row.get('carrier') or '—',
            'phase': row.get('phase') or '—',
            'similarity_tags': tags,
            'similarity_score': score,
            'fatalities': int(row.get('fatalities') or 0),
            'source': 'NTSB AVALL',
        })
    out.sort(key=lambda x:(x['similarity_score'],x['event_date']), reverse=True)
    return out[:limit]


def read_jsonl(path):
    rows=[]
    with Path(path).open(encoding='utf-8') as f:
        for line in f:
            if line.strip(): rows.append(json.loads(line))
    return rows


def write_public_comparables(normalized_jsonl, out_path='site/data/comparable-cases.json', limit=8):
    cases=build_nonfatal_comparables(read_jsonl(normalized_jsonl), limit=limit)
    payload={
        'schema':'bsfm.public-comparables.v1',
        'generated_at':_now(),
        'forecast_id':'F-002',
        'source':'NTSB AVALL',
        'source_scope':'Current official NTSB AVALL snapshot; descriptive nonfatal comparables only, not a global census and not forecast hits.',
        'selection_rule':'Boeing + commercial + nonfatal + 737-800/737-NG + approach/landing or gear/structural similarity; ranked by fixed descriptive similarity then recency.',
        'interpretation_warning':'Comparable nonfatal events are context only. They do not satisfy F-002 primary target and do not change its score, validation state, or scientific gates.',
        'cases':cases,
    }
    p=Path(out_path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return payload

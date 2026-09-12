"""Historical case label extraction with explicit post-event/PIT separation."""
import json
from datetime import date
from pathlib import Path

def _d(v):
    try:return date.fromisoformat(str(v)[:10])
    except (TypeError,ValueError):return None

def build(root=Path('.'), cutoff=None):
    root=Path(root); c=_d(cutoff) if cutoff else None
    src=root/'data/model/model-1.5-unified-feature-table-v1.json'
    rows=json.loads(src.read_text()).get('rows',[]) if src.exists() else []
    out=[]
    for r in rows:
        event=_d(r.get('event_date')); pub=_d(r.get('available_at'))
        labels={k:r.get(k) for k in ('aircraft_age','airport','route','phase_of_flight','icao_type','system','failure_mode','operator','geography','serial_or_registration')}
        # descriptive labels may use the final record; PIT labels require availability evidence
        pit_ok=bool(pub and (not c or pub<=c))
        out.append({'event_id':r.get('event_id'),'event_date':r.get('event_date'),'registration':r.get('serial_or_registration'),'labels':labels,'source_locator':r.get('source_locator'),'source_publisher':r.get('source_publisher'),'publication_date':r.get('source_publication_date') or r.get('available_at'),'descriptive_status':'available' if any(v not in (None,'', 'unknown') for v in labels.values()) else 'sparse','pit_status':'admissible' if pit_ok else 'not_admissible','pit_rule':'publication_date <= cutoff and before event use' if c else 'requires explicit cutoff','cutoff':cutoff})
    return {'schema':'bsfm.historical-label-pipeline.v1','status':'development_only','steps':['extract','normalize','link','provenance','separate_descriptive_from_pit','emit_training_dataset'],'cutoff':cutoff,'rows':out,'row_count':len(out),'policy':'post-event descriptive labels never become retrospective predictors'}

if __name__=='__main__':
    print(json.dumps(build(),indent=2))

from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path

SCHEMA='bsfm.evidence-automation.v1'
GAPS={
 'G1':('historical_cases','Global qualifying Boeing commercial-jet fatal-event census 2010-2025'),
 'G2':('baseline_present','Annual Boeing-family departures/exposure 2010-2025'),
 'G3':('point_in_time_availability_verified','Historical public availability of predictor records'),
 'G4':('scientific_promotion_ready','Leakage-free paired OOS calibration and candidate-vs-baseline result'),
}

def _sha(path:Path):
 h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def _load(path:Path):
 try: return json.loads(path.read_text(encoding='utf-8'))
 except (OSError,json.JSONDecodeError): return None

def build_evidence_state(root:Path,readiness:dict)->dict:
 """Describe evidence acquisition without manufacturing scientific passes.

    Automation may inventory machine-readable evidence and provenance. A gate is
    passed only when the canonical readiness audit has independently admitted it.
    """
 root=Path(root); artifacts=[]
 for rel in ('data/historical','data/exposure','data/manifests','evaluations'):
  base=root/rel
  if not base.exists(): continue
  for p in sorted(x for x in base.rglob('*') if x.is_file()):
   artifacts.append({'path':p.relative_to(root).as_posix(),'sha256':_sha(p),'bytes':p.stat().st_size})
 gates=readiness.get('gates',{})
 gaps={}
 for gid,(gate,label) in GAPS.items():
  if gid=='G4': passed=readiness.get('scientific_promotion_ready') is True
  else: passed=gates.get(gate) is True
  gaps[gid]={'label':label,'status':'PASS' if passed else 'BLOCKED','gate':gate}
 return {'schema':SCHEMA,'generated_at':datetime.now(timezone.utc).isoformat(),'policy':'fail-closed','gaps':gaps,'artifacts':artifacts}

def write_evidence_state(root:Path,readiness:dict,out:Path|None=None)->dict:
 state=build_evidence_state(root,readiness)
 out=out or Path(root)/'site/data/evidence-state.json'; out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 return state

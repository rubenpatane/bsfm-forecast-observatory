from pathlib import Path
from bsfm.evidence_automation import build_evidence_state

def test_evidence_automation_never_opens_missing_gates(tmp_path:Path):
 (tmp_path/'evaluations').mkdir(); (tmp_path/'evaluations/x.json').write_text('{}')
 readiness={'gates':{'historical_cases':False,'baseline_present':False,'point_in_time_availability_verified':False},'scientific_promotion_ready':False}
 s=build_evidence_state(tmp_path,readiness)
 assert s['policy']=='fail-closed'
 assert all(v['status']=='BLOCKED' for v in s['gaps'].values())
 assert s['artifacts'][0]['sha256']

def test_evidence_state_only_mirrors_canonical_readiness(tmp_path:Path):
 readiness={'gates':{'historical_cases':True,'baseline_present':True,'point_in_time_availability_verified':True},'scientific_promotion_ready':True}
 s=build_evidence_state(tmp_path,readiness)
 assert all(v['status']=='PASS' for v in s['gaps'].values())

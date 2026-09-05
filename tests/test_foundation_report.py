import json
from bsfm.foundation_report import build_foundation_report


def test_construction_data_cannot_open_scientific_gates(tmp_path):
    (tmp_path/'data/census').mkdir(parents=True); (tmp_path/'data/exposure').mkdir(parents=True)
    ledger={'years':[{'year':y,'reconciled':False} for y in range(2010,2026)]}
    (tmp_path/'data/census/year-ledger.json').write_text(json.dumps(ledger))
    (tmp_path/'data/census/events.jsonl').write_text('')
    (tmp_path/'data/exposure/departures.jsonl').write_text('')
    r=build_foundation_report(tmp_path,{'point_in_time_availability_verified':False,'leakage_free':False})
    assert not r['historical_cases']
    assert not r['baseline_present']
    assert not r['ready_for_candidate_fit']
    assert not r['calibration_evaluated']
    assert r['walk_forward_cases']==0

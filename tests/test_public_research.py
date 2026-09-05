import json
from bsfm.public_research import write_public_research_state


def test_public_research_generator_never_turns_candidate_population_into_g1_pass(tmp_path):
    (tmp_path/'data/census').mkdir(parents=True); (tmp_path/'site/data').mkdir(parents=True)
    (tmp_path/'data/census/year-ledger.json').write_text(json.dumps({'years':[{'year':2024,'reconciled':False}]}))
    (tmp_path/'data/census/g1-candidates.json').write_text(json.dumps({'records':[{'event_id':'x','event_date':'2024-01-01','model':'737-800','decision':'include','source_publisher':'Authority','source_record_id':'R'}]}))
    state=write_public_research_state(tmp_path)
    year=state['gates']['G1']['years'][0]
    assert year['candidate_count']==1 and year['status']=='OPEN'
    assert state['gates']['G1']['status']=='BLOCKED'
    assert state['gates']['G2']['baseline_present'] is False

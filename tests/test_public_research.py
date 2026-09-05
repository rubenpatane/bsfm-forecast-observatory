import json
from bsfm.public_research import write_public_research_state


def _base(tmp_path, years):
    (tmp_path/'data/census').mkdir(parents=True); (tmp_path/'site/data').mkdir(parents=True)
    (tmp_path/'data/census/year-ledger.json').write_text(json.dumps({'years':years}))
    (tmp_path/'data/census/g1-candidates.json').write_text(json.dumps({'records':[]}))


def test_public_research_generator_never_turns_candidate_population_into_g1_pass(tmp_path):
    _base(tmp_path,[{'year':2024,'reconciled':False}])
    (tmp_path/'data/census/g1-candidates.json').write_text(json.dumps({'records':[{'event_id':'x','event_date':'2024-01-01','model':'737-800','decision':'include','source_publisher':'Authority','source_record_id':'R'}]}))
    state=write_public_research_state(tmp_path)
    year=state['gates']['G1']['years'][0]
    assert year['candidate_count']==1 and year['status']=='OPEN'
    assert state['gates']['G1']['status']=='BLOCKED'
    assert state['gates']['G2']['baseline_present'] is False


def test_public_research_aggregates_annual_jsonl_and_deduplicates_event_ids(tmp_path):
    _base(tmp_path,[{'year':2017,'reconciled':True},{'year':2018,'reconciled':False}])
    (tmp_path/'data/census/g1-candidates.json').write_text(json.dumps({'records':[{'event_id':'dup','event_date':'2018-01-01','decision':'include','model':'old'}]}))
    (tmp_path/'data/census/candidates-2018.jsonl').write_text(json.dumps({'event_id':'dup','event_date':'2018-01-01','decision':'include','model':'737-800'})+'\n'+json.dumps({'event_id':'new','event_date':'2018-02-01','decision':'unresolved','model':'777'})+'\n')
    (tmp_path/'data/census/year-evidence-2017.json').write_text(json.dumps({'status':'reconciled','controls':{'annual_source_scope_demonstrated':True,'all_fatal_jets_mapped':True,'boeing_target_membership_mapped':True,'competent_authority_per_candidate':True,'independent_reconciliation':True,'target_taxonomies_resolved':True}}))
    state=write_public_research_state(tmp_path)
    years={x['year']:x for x in state['gates']['G1']['years']}
    assert years[2017]['status']=='RECONCILED'
    assert years[2018]['candidate_count']==2
    assert [x for x in years[2018]['events'] if x['event_id']=='dup'][0]['model']=='737-800'


def test_unresolved_taxonomy_surfaces_as_unresolved(tmp_path):
    _base(tmp_path,[{'year':2014,'reconciled':False}])
    (tmp_path/'data/census/year-evidence-2014.json').write_text(json.dumps({'status':'unresolved-taxonomy'}))
    state=write_public_research_state(tmp_path)
    assert state['gates']['G1']['years'][0]['status']=='UNRESOLVED'

from bsfm.research_state import build_research_state


def test_public_state_keeps_all_scientific_gates_blocked():
    state=build_research_state([],{'coverage':'incomplete'},{'availability':'unknown'},{'msn':{'status':'BLOCKED'}})
    assert all(state['gates'][g]['status']=='BLOCKED' for g in ('G1','G2','G3','G4'))
    assert state['gates']['G2']['baseline_present'] is False
    assert 'not part of the original F-002' in state['refinement_notice']

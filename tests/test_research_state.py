from bsfm.research_state import build_research_state


def test_public_state_defaults_to_blocked_without_g1_closure():
    state=build_research_state([],{'coverage':'incomplete'},{'availability':'unknown'},{'msn':{'status':'BLOCKED'}})
    assert all(state['gates'][g]['status']=='BLOCKED' for g in ('G1','G2','G3','G4'))
    assert state['gates']['G2']['baseline_present'] is False
    assert 'not part of the original F-002' in state['refinement_notice']


def test_public_state_propagates_g1_closed_with_limitation():
    state=build_research_state(
        [],
        {'coverage':'incomplete'},
        {'availability':'unknown'},
        {'msn':{'status':'BLOCKED'}},
        g1={
            'status':'CLOSED_WITH_LIMITATION',
            'gate_acceptable':True,
            'strict_complete':False,
            'non_identifiable_years':[2014,2020],
        },
    )
    assert state['gates']['G1']['status']=='CLOSED_WITH_LIMITATION'
    assert state['gates']['G1']['gate_acceptable'] is True
    assert state['gates']['G1']['strict_complete'] is False
    assert state['gates']['G1']['non_identifiable_years']==[2014,2020]
    assert state['gates']['G2']['status']=='BLOCKED'
    assert state['gates']['G3']['status']=='BLOCKED'
    assert state['gates']['G4']['status']=='BLOCKED'

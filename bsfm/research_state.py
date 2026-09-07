from __future__ import annotations


def build_research_state(annual_rows, exposure, pit, resolution, refinements=None, g1=None):
    annual_rows=list(annual_rows or [])
    g1=dict(g1 or {})
    g1_status=str(g1.pop('status','BLOCKED'))
    return {
        'schema':'bsfm.public-research-state.v1',
        'notice':'Research observatory, not an operational safety tool.',
        'forecast':{'id':'F-002','status':'FROZEN','claim_level':'experimental_unvalidated'},
        'gates':{
            'G1':{'status':g1_status,'years':annual_rows,**g1},
            'G2':{'status':'BLOCKED','baseline_present':False,**(exposure or {})},
            'G3':{'status':'BLOCKED',**(pit or {})},
            'G4':{'status':'BLOCKED','reason':'downstream of G2-G3; G1 is acceptable only under its declared closure limitation'},
        },
        'resolution':resolution or {},
        'refinements':list(refinements or []),
        'refinement_notice':'Later refinement — not part of the original F-002 forecast and not counted in its original score.',
        'prohibited_public_claims':['individual-aircraft live risk ranking','absolute accident probability while gates are blocked'],
    }

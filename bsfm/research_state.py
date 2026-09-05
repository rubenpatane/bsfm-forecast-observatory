from __future__ import annotations


def build_research_state(annual_rows, exposure, pit, resolution, refinements=None):
    annual_rows=list(annual_rows or [])
    return {
        'schema':'bsfm.public-research-state.v1',
        'notice':'Research observatory, not an operational safety tool.',
        'forecast':{'id':'F-002','status':'FROZEN','claim_level':'experimental_unvalidated'},
        'gates':{
            'G1':{'status':'BLOCKED','years':annual_rows},
            'G2':{'status':'BLOCKED','baseline_present':False,**(exposure or {})},
            'G3':{'status':'BLOCKED',**(pit or {})},
            'G4':{'status':'BLOCKED','reason':'downstream of G1-G3'},
        },
        'resolution':resolution or {},
        'refinements':list(refinements or []),
        'refinement_notice':'Later refinement — not part of the original F-002 forecast and not counted in its original score.',
        'prohibited_public_claims':['individual-aircraft live risk ranking','absolute accident probability while gates are blocked'],
    }

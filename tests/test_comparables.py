from bsfm.comparables import build_nonfatal_comparables


def row(**kw):
    base={
        'event_id':'X1','event_date':'2025-01-01','model':'737-832','carrier':'Demo Air',
        'phase':'LANDING','boeing':True,'fatal':False,'fatalities':0,'commercial':True,
        'event_sequence':[],'findings':[],
    }
    base.update(kw)
    return base


def test_selects_nonfatal_737_800_landing_case():
    out=build_nonfatal_comparables([row()])
    assert len(out)==1
    assert 'exact_model' in out[0]['similarity_tags']
    assert 'family_737_ng' in out[0]['similarity_tags']
    assert 'approach_landing' in out[0]['similarity_tags']
    assert out[0]['fatalities']==0


def test_rejects_fatal_noncommercial_and_unrelated_cases():
    rows=[
        row(event_id='F',fatal=True,fatalities=1),
        row(event_id='N',commercial=False),
        row(event_id='U',model='777-300',phase='LANDING'),
        row(event_id='C',model='737-832',phase='CRUISE'),
    ]
    assert build_nonfatal_comparables(rows)==[]


def test_cluster_can_supply_second_similarity_dimension():
    r=row(phase='CRUISE',event_sequence=[{'occurrence_description':'LANDING GEAR FAILURE','defining_event':''}])
    out=build_nonfatal_comparables([r])
    assert len(out)==1
    assert 'gear_structural_cluster' in out[0]['similarity_tags']


def test_rank_is_similarity_then_recency():
    a=row(event_id='A',event_date='2024-01-01')
    b=row(event_id='B',event_date='2025-01-01',event_sequence=[{'occurrence_description':'HARD LANDING STRUCTURAL DAMAGE','defining_event':''}])
    out=build_nonfatal_comparables([a,b])
    assert [x['event_id'] for x in out]==['B','A']


def test_old_cases_age_out_against_newest_snapshot_year():
    old=row(event_id='OLD',event_date='2018-01-01')
    newest=row(event_id='NEW',event_date='2026-01-01')
    out=build_nonfatal_comparables([old,newest],recent_years=5)
    assert [x['event_id'] for x in out]==['NEW']

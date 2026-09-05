from bsfm.refinements import validate_refinement,public_view

P={'forecast_id':'F-002','cutoff':'2026-08-19T00:00:00Z'}

def base():
 return {'refinement_id':'R-F002-001','parent_forecast_id':'F-002','issued_at':'2026-09-05T10:00:00Z','model_version':'1.2','input_hashes':['sha256:x'],'changes':[{'dimension':'geography','old_value':'unresolved','new_value':'Europe'}],'status':'prospective_unvalidated','alters_parent_scoring':False}

def test_valid_refinement_is_separate_and_prospective():
 r=base(); assert validate_refinement(r,P)==[]
 assert 'not part of the original' in public_view(r)['notice']

def test_refinement_cannot_backdate_to_parent_cutoff():
 r=base(); r['issued_at']='2026-08-19T00:00:00Z'
 assert any('after parent cutoff' in x for x in validate_refinement(r,P))

def test_refinement_cannot_rewrite_parent_score():
 r=base(); r['alters_parent_scoring']=True
 assert any('may not alter parent scoring' in x for x in validate_refinement(r,P))

def test_refinement_requires_auditable_inputs():
 r=base(); r['input_hashes']=[]
 assert any('input_hashes' in x for x in validate_refinement(r,P))

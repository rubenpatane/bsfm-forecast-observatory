import pytest

from bsfm.model_registry import build_model_record,promote_record


def test_model_record_hashes_model_inputs_and_evaluation():
    r=build_model_record('M-001',{'x':1},{'cutoff':'2020-01-01'},{'brier':0.2})
    assert r['status']=='candidate'
    assert all(r[k].startswith('sha256:') for k in ('model_hash','training_snapshot_hash','evaluation_hash','record_hash'))


def test_promotion_requires_explicit_gate_and_rehashes_record():
    r=build_model_record('M-001',{'x':1},{'cutoff':'2020-01-01'},{'brier':0.2})
    with pytest.raises(ValueError): promote_record(r,{'pass':False})
    p=promote_record(r,{'pass':True})
    assert p['status']=='promoted'
    assert p['record_hash']!=r['record_hash']

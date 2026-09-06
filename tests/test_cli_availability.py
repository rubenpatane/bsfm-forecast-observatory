import json
import bsfm.cli as cli


def _coverage(ready):
    return {'strict_operational_pit_ready': ready, 'g3_status': 'PASS' if ready else 'BLOCKED'}


def test_availability_audit_defaults_leakage_false(tmp_path,monkeypatch):
    monkeypatch.setattr(cli,'ROOT',tmp_path)
    monkeypatch.setattr(cli,'build_operational_pit_coverage',lambda root:_coverage(True))
    out=cli.availability_audit({'source_integrity_ready':True})
    assert out=={'point_in_time_availability_verified':True,'leakage_free':False,'operational_pit_status':'PASS'}


def test_availability_audit_requires_integrity_even_if_file_claims_leakage_free(tmp_path,monkeypatch):
    monkeypatch.setattr(cli,'ROOT',tmp_path)
    monkeypatch.setattr(cli,'build_operational_pit_coverage',lambda root:_coverage(True))
    p=tmp_path/'evaluations'/'availability-audit.json'; p.parent.mkdir()
    p.write_text(json.dumps({'leakage_free':True}))
    assert cli.availability_audit({'source_integrity_ready':False})['leakage_free'] is False
    assert cli.availability_audit({'source_integrity_ready':True})['leakage_free'] is True


def test_availability_audit_requires_operational_source_coverage(tmp_path,monkeypatch):
    monkeypatch.setattr(cli,'ROOT',tmp_path)
    monkeypatch.setattr(cli,'build_operational_pit_coverage',lambda root:_coverage(False))
    p=tmp_path/'evaluations'/'availability-audit.json'; p.parent.mkdir()
    p.write_text(json.dumps({'leakage_free':True}))
    out=cli.availability_audit({'source_integrity_ready':True})
    assert out['point_in_time_availability_verified'] is False
    assert out['leakage_free'] is False
    assert out['operational_pit_status'] == 'BLOCKED'


def test_availability_audit_does_not_use_global_manifest_pit_boolean(tmp_path,monkeypatch):
    monkeypatch.setattr(cli,'ROOT',tmp_path)
    monkeypatch.setattr(cli,'build_operational_pit_coverage',lambda root:_coverage(True))
    out=cli.availability_audit({
        'source_integrity_ready':True,
        'point_in_time_availability_verified':False,
    })
    assert out['point_in_time_availability_verified'] is True


def test_availability_audit_ignores_malformed_evidence(tmp_path,monkeypatch):
    monkeypatch.setattr(cli,'ROOT',tmp_path)
    monkeypatch.setattr(cli,'build_operational_pit_coverage',lambda root:_coverage(True))
    p=tmp_path/'evaluations'/'availability-audit.json'; p.parent.mkdir(); p.write_text('{bad')
    assert cli.availability_audit({'source_integrity_ready':True})['leakage_free'] is False

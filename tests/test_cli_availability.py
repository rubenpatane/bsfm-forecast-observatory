import json
import bsfm.cli as cli


def test_availability_audit_defaults_leakage_false(tmp_path,monkeypatch):
    monkeypatch.setattr(cli,'ROOT',tmp_path)
    out=cli.availability_audit({'point_in_time_availability_verified':True})
    assert out=={'point_in_time_availability_verified':True,'leakage_free':False}


def test_availability_audit_requires_pit_even_if_file_claims_leakage_free(tmp_path,monkeypatch):
    monkeypatch.setattr(cli,'ROOT',tmp_path)
    p=tmp_path/'evaluations'/'availability-audit.json'; p.parent.mkdir()
    p.write_text(json.dumps({'leakage_free':True}))
    assert cli.availability_audit({'point_in_time_availability_verified':False})['leakage_free'] is False
    assert cli.availability_audit({'point_in_time_availability_verified':True})['leakage_free'] is True


def test_availability_audit_ignores_malformed_evidence(tmp_path,monkeypatch):
    monkeypatch.setattr(cli,'ROOT',tmp_path)
    p=tmp_path/'evaluations'/'availability-audit.json'; p.parent.mkdir(); p.write_text('{bad')
    assert cli.availability_audit({'point_in_time_availability_verified':True})['leakage_free'] is False

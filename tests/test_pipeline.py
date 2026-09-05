import json
from bsfm import pipeline

def test_source_integrity_is_not_model_readiness(tmp_path,monkeypatch):
 root=tmp_path; d=root/'data'/'manifests'; d.mkdir(parents=True)
 (d/'faa.json').write_text(json.dumps({'source':'FAA SDR','status':'validated','historical_public_availability':'unverified'}))
 monkeypatch.setattr(pipeline,'ROOT',root)
 s=pipeline.validate_sources()
 assert s['source_integrity_ready'] is True
 assert s['point_in_time_availability_verified'] is False
 assert s['ready_for_model'] is False

def test_missing_availability_metadata_does_not_pass(tmp_path,monkeypatch):
 root=tmp_path; d=root/'data'/'manifests'; d.mkdir(parents=True)
 (d/'source.json').write_text(json.dumps({'source':'Example','status':'validated'}))
 monkeypatch.setattr(pipeline,'ROOT',root)
 s=pipeline.validate_sources()
 assert s['source_integrity_ready'] is True
 assert s['point_in_time_availability_verified'] is False
 assert s['ready_for_model'] is False

def test_only_explicit_verified_availability_passes(tmp_path,monkeypatch):
 root=tmp_path; d=root/'data'/'manifests'; d.mkdir(parents=True)
 (d/'source.json').write_text(json.dumps({'source':'Example','status':'validated','historical_public_availability':'verified'}))
 monkeypatch.setattr(pipeline,'ROOT',root)
 s=pipeline.validate_sources()
 assert s['point_in_time_availability_verified'] is True
 assert s['ready_for_model'] is True

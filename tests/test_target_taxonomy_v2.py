import json
from pathlib import Path


def _taxonomy():
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / 'data/census/prospective-target-taxonomy-v2.json').read_text(encoding='utf-8'))


def test_v2_is_prospective_and_does_not_reclassify_f002_or_g1_v1():
    t = _taxonomy()
    assert t['status'] == 'ADOPTED_PROSPECTIVE_ONLY'
    assert t['applies_to']['f002'] is False
    assert t['applies_to']['historical_g1_v1'] is False
    nr = t['non_retroactivity']
    assert nr['f002_unchanged'] is True
    assert nr['historical_g1_v1_unchanged'] is True
    assert nr['mh370_reclassified'] is False
    assert nr['mh17_reclassified'] is False
    assert nr['ps752_reclassified'] is False


def test_v2_excludes_official_security_events_from_primary_target():
    t = _taxonomy()
    r = t['rules']['hostile_unlawful_security']
    assert r['decision'] == 'EXCLUDE_SECURITY'
    assert r['parallel_census'] is True
    assert r['media_inference_allowed'] is False
    assert t['primary_outcome_state'] == 'INCLUDE_ACCIDENT'


def test_v2_missing_aircraft_fails_closed_until_authoritative_threshold():
    t = _taxonomy()
    r = t['rules']['missing_aircraft']
    assert r['default_decision'] == 'PENDING_MISSING'
    assert len(r['include_when']) == 2
    assert r['security_rule_precedence'] is True


def test_v2_preserves_external_fatalities_and_authoritative_operation_status():
    t = _taxonomy()
    f = t['rules']['fatalities']
    assert f['ground_allowed'] is True
    assert f['other_aircraft_allowed'] is True
    assert f['preserve_external_counts_separately'] is True
    assert t['rules']['commercial_status']['operator_name_inference_allowed'] is False

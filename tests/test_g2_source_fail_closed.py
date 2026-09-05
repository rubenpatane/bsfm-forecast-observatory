import json
from pathlib import Path


def _load(root, rel):
    return json.loads((root / rel).read_text(encoding='utf-8'))


def test_g2_candidate_inventories_remain_fail_closed():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        'data/exposure/source-inventory.json',
        'data/exposure/open-adsb-alternatives.json',
    ]:
        data = _load(root, rel)
        conclusion = data['conclusion']
        assert conclusion['g2_status'] == 'BLOCKED'
        assert conclusion['baseline_present'] is False


def test_open_adsb_sources_are_not_primary_baseline():
    root = Path(__file__).resolve().parents[1]
    data = _load(root, 'data/exposure/open-adsb-alternatives.json')
    assert data['status'] == 'reconciliation-only'
    for source in data['sources']:
        assert 'not a complete compatible global annual denominator' in source.get('g2_use', '') or 'prohibited as primary annual exposure baseline' in source.get('g2_use', '')

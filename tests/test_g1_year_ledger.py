import json
from pathlib import Path

from bsfm.annual_evidence import ANNUAL_CONTROLS, audit_annual_completeness


ROOT = Path(__file__).resolve().parents[1]


def _load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def test_reconciled_years_require_six_of_six_evidence():
    ledger = _load(ROOT / 'data/census/year-ledger.json')
    assert [row['year'] for row in ledger['years']] == list(range(2010, 2026))

    for row in ledger['years']:
        year = row['year']
        evidence_path = ROOT / f'data/census/year-evidence-{year}.json'
        assert evidence_path.exists(), f'missing year evidence: {year}'
        evidence = _load(evidence_path)
        controls = evidence.get('controls')

        if row['reconciled']:
            assert evidence.get('reconciled') is True, year
            assert isinstance(controls, dict), year
            assert set(ANNUAL_CONTROLS) <= set(controls), year
            audit = audit_annual_completeness(year, controls)
            assert audit['complete'] is True, (year, audit)
            assert audit['evidence_progress'] == '6/6', year
        else:
            assert evidence.get('reconciled') is not True, year
            if isinstance(controls, dict):
                assert audit_annual_completeness(year, controls)['complete'] is False, year


def test_current_taxonomy_blocks_remain_fail_closed():
    ledger = _load(ROOT / 'data/census/year-ledger.json')
    state = {row['year']: row['reconciled'] for row in ledger['years']}
    assert state[2014] is False
    assert state[2020] is False

    for year in (2014, 2020):
        evidence = _load(ROOT / f'data/census/year-evidence-{year}.json')
        assert str(evidence.get('status', '')).startswith('unresolved')
        assert evidence['controls']['boeing_target_membership_mapped'] is False
        assert evidence['controls']['target_taxonomies_resolved'] is False

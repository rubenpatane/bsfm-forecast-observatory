from pathlib import Path

from bsfm.g1_census import audit_integrated_g1_census

ROOT = Path(__file__).resolve().parents[1]


def test_integrated_census_matches_current_14_of_16_checkpoint():
    audit = audit_integrated_g1_census(ROOT)
    assert audit['complete'] is False
    assert audit['unreconciled_years'] == [2014, 2020]
    assert audit['reconciled_years'] == [
        2010, 2011, 2012, 2013, 2015, 2016, 2017,
        2018, 2019, 2021, 2022, 2023, 2024, 2025,
    ]
    assert audit['missing_candidate_ids'] == []
    assert audit['extra_candidate_ids'] == []
    assert audit['duplicate_candidate_ids'] == []
    assert audit['evidence_errors'] == []


def test_unresolved_years_remain_event_level_visible():
    audit = audit_integrated_g1_census(ROOT)
    annual = {row['year']: row for row in audit['annual']}
    assert annual[2014]['unresolved_candidate_ids'] == ['G1-2014-MH17', 'G1-2014-MH370']
    assert annual[2020]['unresolved_candidate_ids'] == ['G1-2020-PS752']
    assert annual[2014]['reconciled'] is False
    assert annual[2020]['reconciled'] is False

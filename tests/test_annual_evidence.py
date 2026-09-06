from bsfm.annual_evidence import ANNUAL_CONTROLS, audit_annual_completeness


def test_annual_completeness_is_six_independent_fail_closed_controls():
    controls = {name: True for name in ANNUAL_CONTROLS}
    controls['target_taxonomies_resolved'] = False
    audit = audit_annual_completeness(2014, controls)
    assert audit['evidence_progress'] == '5/6'
    assert not audit['reconciled'] and audit['status'] == 'OPEN'


def test_only_six_of_six_can_reconcile_year():
    audit = audit_annual_completeness(2023, {name: True for name in ANNUAL_CONTROLS})
    assert audit['reconciled'] and audit['status'] == 'RECONCILED'

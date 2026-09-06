from bsfm.exposure import audit_target_universe_exposure


def test_target_universe_requires_every_cohort_covered_or_excluded():
    audit = audit_target_universe_exposure(
        ['727', '737-Original', '737-Classic', '737-NG', '737-MAX', '747', '757', '767', '777', '787'],
        ['737-Classic', '737-NG', '737-MAX', '747', '757', '767', '777', '787'],
    )
    assert not audit['complete']
    assert audit['uncovered_target_cohorts'] == ['727', '737-Original']


def test_explicit_versioned_exclusion_can_close_set_relation_only():
    audit = audit_target_universe_exposure(
        ['727', '737-Original', '737-Classic'],
        ['737-Classic'],
        ['727', '737-Original'],
    )
    assert audit['complete']


def test_exposure_and_exclusion_overlap_fails_closed():
    audit = audit_target_universe_exposure(['737-NG'], ['737-NG'], ['737-NG'])
    assert not audit['complete']
    assert 'cohort_both_exposed_and_excluded' in audit['errors']

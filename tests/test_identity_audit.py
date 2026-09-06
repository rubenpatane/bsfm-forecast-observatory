from bsfm.identity_audit import audit_identity_conflicts


def test_serial_conflict_is_detected_not_silently_corrected():
    rows=[
        {'publisher':'NTSB','authority_role':'accredited/supporting','serial_number':'333024','registration':'P2-PXE','event_date':'2018-09-28','model':'737'},
        {'publisher':'PNG AIC','authority_role':'competent investigation authority','serial_number':'33024','registration':'P2-PXE','event_date':'2018-09-28','model':'737-800'},
    ]
    audit=audit_identity_conflicts(rows)
    assert audit['conflict']
    assert 'serial_number' in audit['conflict_fields']
    assert audit['adjudication']=='required'

# Real AVALL integration is intentionally not a unit-test dependency. The audit
# function is exercised against the downloaded AGGIORNA artifact in research runs.
from bsfm.ntsb_snapshot_audit import audit_snapshot


def test_audit_function_is_importable():
    assert callable(audit_snapshot)

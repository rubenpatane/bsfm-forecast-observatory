from __future__ import annotations

IDENTITY_FIELDS = ('event_date', 'registration', 'serial_number', 'model')


def audit_identity_conflicts(records):
    """Detect source-to-source identity disagreements without auto-adjudicating them."""
    rows = list(records or [])
    values = {}
    conflicts = {}
    for field in IDENTITY_FIELDS:
        observed = {}
        for row in rows:
            value = str(row.get(field) or '').strip()
            if not value: continue
            observed.setdefault(value, []).append({
                'publisher': row.get('publisher'),
                'authority_role': row.get('authority_role'),
                'record_id': row.get('record_id'),
            })
        values[field] = observed
        if len(observed) > 1: conflicts[field] = observed
    return {
        'conflict': bool(conflicts),
        'conflict_fields': sorted(conflicts),
        'conflicts': conflicts,
        'observed_values': values,
        'adjudication': 'required' if conflicts else 'not_required',
    }

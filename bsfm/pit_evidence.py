from __future__ import annotations
from datetime import datetime, timezone

STATUSES = {'verified', 'bounded', 'unknown'}


def _time(value: str) -> datetime:
    v = str(value).strip().replace('Z', '+00:00')
    dt = datetime.fromisoformat(v)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def audit_pit_record(row: dict) -> list[str]:
    """Validate publication-availability evidence without promoting admin timestamps."""
    errors = []
    status = row.get('pit_status')
    if status not in STATUSES:
        errors.append('invalid_pit_status')
        return errors

    if not str(row.get('source_record_id', '')).strip():
        errors.append('missing_source_record_id')

    if status == 'verified':
        if not row.get('available_at'):
            errors.append('verified_requires_available_at')
        if not str(row.get('availability_evidence', '')).strip():
            errors.append('verified_requires_availability_evidence')
    elif status == 'bounded':
        if not row.get('available_not_before') or not row.get('available_not_after'):
            errors.append('bounded_requires_interval')
        else:
            try:
                if _time(row['available_not_before']) > _time(row['available_not_after']):
                    errors.append('invalid_availability_interval')
            except (ValueError, TypeError):
                errors.append('invalid_availability_interval')
        if row.get('available_at'):
            errors.append('bounded_must_not_claim_exact_available_at')
    else:  # unknown
        if row.get('available_at'):
            errors.append('unknown_must_not_claim_available_at')

    if row.get('availability_basis') in {'approval_date', 'last_change', 'event_date'}:
        errors.append('administrative_or_event_timestamp_not_publication_evidence')
    return errors


def strict_pit_admissible(row: dict, cutoff: str) -> bool:
    """Strict backtest admission: only exact, evidenced public availability may pass."""
    if audit_pit_record(row) or row.get('pit_status') != 'verified':
        return False
    try:
        return _time(row['available_at']) <= _time(cutoff)
    except (ValueError, TypeError, KeyError):
        return False


def audit_pit_manifest(rows: list[dict]) -> dict:
    failures = []
    counts = {s: 0 for s in sorted(STATUSES)}
    for i, row in enumerate(rows):
        status = row.get('pit_status')
        if status in counts:
            counts[status] += 1
        errors = audit_pit_record(row)
        if errors:
            failures.append({'index': i, 'source_record_id': row.get('source_record_id'), 'errors': errors})
    return {
        'valid': not failures,
        'counts': counts,
        'strict_verified_count': counts['verified'] if not failures else None,
        'failures': failures,
        'g3_pass': False,
        'note': 'A valid source manifest does not open G3; every predictor admitted to a backtest still requires record-level verified PIT evidence.'
    }

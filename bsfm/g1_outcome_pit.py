from __future__ import annotations

from datetime import date
from pathlib import Path

from .g1_census import load_integrated_candidates


ALLOWED_BASES = {
    'competent_authority_publication',
    'official_database_publication',
    'archived_public_snapshot',
}


def _date(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def audit_g1_outcome_pit(root, start_year=2010, end_year=2025):
    """Audit whether included historical G1 outcomes are usable at simulated cutoffs.

    This does not re-adjudicate target membership. It asks only whether each
    already-included event has an auditable public-availability date and basis.
    Event date alone is never sufficient.
    """
    root = Path(root)
    rows = load_integrated_candidates(root)['rows']
    included = [
        row for row in rows
        if str(row.get('decision') or '').lower() == 'include'
        and start_year <= int(str(row.get('event_date') or '0000')[:4] or 0) <= end_year
    ]
    audited = []
    missing = []
    invalid = []
    for row in sorted(included, key=lambda r: (str(r.get('event_date') or ''), str(r.get('event_id') or ''))):
        event_id = str(row.get('event_id') or '').strip()
        event_date = _date(row.get('event_date'))
        available_at = _date(row.get('available_at'))
        basis = str(row.get('availability_basis') or '').strip()
        evidence_ids = row.get('availability_evidence_ids') if isinstance(row.get('availability_evidence_ids'), list) else []
        reasons = []
        if available_at is None:
            reasons.append('missing_available_at')
        if basis not in ALLOWED_BASES:
            reasons.append('missing_or_unapproved_availability_basis')
        if not evidence_ids:
            reasons.append('missing_availability_evidence_ids')
        if event_date and available_at and available_at < event_date:
            reasons.append('available_at_before_event_date')
        status = 'verified' if not reasons else 'unverified'
        item = {
            'event_id': event_id,
            'event_date': row.get('event_date'),
            'available_at': row.get('available_at'),
            'availability_basis': basis or None,
            'availability_evidence_ids': evidence_ids,
            'pit_status': status,
            'reasons': reasons,
        }
        audited.append(item)
        if reasons:
            missing.append(event_id)
        if 'available_at_before_event_date' in reasons:
            invalid.append(event_id)
    verified = [row['event_id'] for row in audited if row['pit_status'] == 'verified']
    return {
        'schema': 'bsfm.g1-outcome-pit-audit.v1',
        'interval': {'start_year': start_year, 'end_year': end_year},
        'included_events': len(audited),
        'verified_events': len(verified),
        'verified_event_ids': verified,
        'unverified_event_ids': missing,
        'invalid_event_ids': invalid,
        'complete': bool(audited) and not missing and not invalid,
        'events': audited,
        'rule': 'Only explicit public publication/snapshot evidence may populate available_at; event date or current retrospective knowledge is insufficient.',
    }

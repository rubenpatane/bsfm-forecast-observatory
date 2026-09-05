from __future__ import annotations

import json
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


def _rows_from_json(path: Path):
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return None
    return payload.get('events') if isinstance(payload.get('events'), list) else []


def _load_publication_ledger(root: Path):
    base_path = root / 'data/pit/g1-outcome-publication-ledger.json'
    base_rows = _rows_from_json(base_path)
    if base_rows is None:
        return {}, ['missing_or_invalid_publication_ledger']

    by_id = {}
    errors = []
    for row in base_rows:
        row = row if isinstance(row, dict) else {}
        event_id = str(row.get('event_id') or '').strip()
        if not event_id:
            continue
        if event_id in by_id:
            errors.append({'error': 'duplicate_ledger_event_id', 'event_id': event_id})
        by_id[event_id] = row

    # Reviewed annual/batch evidence may override an unverified base placeholder,
    # but may never introduce a new event id or redefine an already verified base
    # row. This keeps the 35-event index stable while making provenance additions
    # small and reviewable.
    evidence_dir = root / 'data/pit/g1-outcome-publication-evidence'
    overlay_seen = set()
    for path in sorted(evidence_dir.glob('*.json')) if evidence_dir.exists() else []:
        rows = _rows_from_json(path)
        if rows is None:
            errors.append({'error': 'invalid_publication_overlay', 'path': path.name})
            continue
        for raw in rows:
            row = raw if isinstance(raw, dict) else {}
            event_id = str(row.get('event_id') or '').strip()
            if not event_id:
                errors.append({'error': 'overlay_missing_event_id', 'path': path.name})
                continue
            if event_id in overlay_seen:
                errors.append({'error': 'duplicate_overlay_event_id', 'event_id': event_id})
                continue
            overlay_seen.add(event_id)
            if event_id not in by_id:
                errors.append({'error': 'overlay_event_not_in_base_ledger', 'event_id': event_id})
                continue
            base = by_id[event_id]
            if base.get('available_at') or base.get('availability_basis') or base.get('availability_evidence_ids'):
                errors.append({'error': 'overlay_redefines_verified_base_row', 'event_id': event_id})
                continue
            by_id[event_id] = {**base, **row}
    return by_id, errors


def audit_g1_outcome_pit(root, start_year=2010, end_year=2025):
    """Audit whether included historical G1 outcomes are usable at simulated cutoffs.

    Target membership stays in G1 candidate files; publication timing lives in a
    separate PIT ledger/evidence layer so temporal research cannot silently mutate
    the historical census. Event date alone is never sufficient.
    """
    root = Path(root)
    rows = load_integrated_candidates(root)['rows']
    ledger, ledger_errors = _load_publication_ledger(root)
    included = [
        row for row in rows
        if str(row.get('decision') or '').lower() == 'include'
        and start_year <= int(str(row.get('event_date') or '0000')[:4] or 0) <= end_year
    ]
    included_ids = {str(row.get('event_id') or '').strip() for row in included}
    extra_ledger_ids = sorted(set(ledger) - included_ids)
    if extra_ledger_ids:
        ledger_errors.extend({'error': 'ledger_event_not_in_included_census', 'event_id': event_id} for event_id in extra_ledger_ids)

    audited = []
    missing = []
    invalid = []
    for row in sorted(included, key=lambda r: (str(r.get('event_date') or ''), str(r.get('event_id') or ''))):
        event_id = str(row.get('event_id') or '').strip()
        event_date = _date(row.get('event_date'))
        temporal = ledger.get(event_id, {})
        available_at = _date(temporal.get('available_at'))
        basis = str(temporal.get('availability_basis') or '').strip()
        evidence_ids = temporal.get('availability_evidence_ids') if isinstance(temporal.get('availability_evidence_ids'), list) else []
        reasons = []
        if event_id not in ledger:
            reasons.append('missing_publication_ledger_row')
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
            'available_at': temporal.get('available_at'),
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
        'schema': 'bsfm.g1-outcome-pit-audit.v3',
        'interval': {'start_year': start_year, 'end_year': end_year},
        'included_events': len(audited),
        'ledger_rows': len(ledger),
        'verified_events': len(verified),
        'verified_event_ids': verified,
        'unverified_event_ids': missing,
        'invalid_event_ids': invalid,
        'ledger_errors': ledger_errors,
        'complete': bool(audited) and not missing and not invalid and not ledger_errors,
        'events': audited,
        'rule': 'Only explicit public publication/snapshot evidence in the separate PIT ledger/evidence layer may populate available_at; event date or current retrospective knowledge is insufficient.',
    }

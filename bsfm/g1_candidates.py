from __future__ import annotations

from datetime import date


REQUIRED_CANDIDATE_FIELDS = (
    'event_id', 'event_date', 'manufacturer', 'model', 'fatalities', 'commercial',
    'source_publisher', 'source_record_id', 'source_locator', 'decision', 'decision_reason'
)

ALLOWED_DECISIONS = {'include', 'exclude', 'unresolved'}
_DECISION_COUNT_KEY = {'include': 'included', 'exclude': 'excluded', 'unresolved': 'unresolved'}


def normalize_candidate(row: dict) -> dict:
    """Normalize a public-source G1 candidate without inferring missing target facts."""
    out = {field: row.get(field) for field in REQUIRED_CANDIDATE_FIELDS}
    out['registration'] = row.get('registration')
    out['operator'] = row.get('operator')
    out['operation_type'] = row.get('operation_type')
    out['location'] = row.get('location')
    out['accident_class'] = row.get('accident_class')
    out['duplicate_of'] = row.get('duplicate_of')
    out['source_publication_date'] = row.get('source_publication_date')
    out['source_retrieved_at'] = row.get('source_retrieved_at')
    # Independent corroboration is evidence, not an attestation. Preserve only explicit rows.
    out['reconciliation_evidence'] = list(row.get('reconciliation_evidence') or [])
    return out


def audit_candidate_census(rows: list[dict], start_year: int = 2010, end_year: int = 2025) -> dict:
    """Audit candidate evidence. Candidate extraction can never attest G1 reconciliation."""
    years = {year: {'candidates': 0, 'included': 0, 'excluded': 0, 'unresolved': 0} for year in range(start_year, end_year + 1)}
    invalid: list[dict] = []
    duplicate_ids: list[str] = []
    seen: set[str] = set()

    for index, raw in enumerate(rows):
        row = normalize_candidate(raw)
        missing = [field for field in REQUIRED_CANDIDATE_FIELDS if row.get(field) in (None, '')]
        event_id = row.get('event_id')
        if event_id:
            if event_id in seen:
                duplicate_ids.append(str(event_id))
            seen.add(str(event_id))
        decision = row.get('decision')
        if decision not in ALLOWED_DECISIONS:
            missing.append('valid_decision')
        try:
            year = date.fromisoformat(str(row.get('event_date', ''))[:10]).year
        except ValueError:
            year = None
            if 'event_date' not in missing:
                missing.append('event_date')
        if year in years:
            years[year]['candidates'] += 1
            if decision in ALLOWED_DECISIONS:
                years[year][_DECISION_COUNT_KEY[decision]] += 1
        if missing:
            invalid.append({'index': index, 'event_id': event_id, 'missing_or_invalid': sorted(set(missing))})

    return {
        'schema': 'bsfm.g1-candidate-census-audit.v1',
        'interval': {'start_year': start_year, 'end_year': end_year},
        'records': len(rows),
        'years': years,
        'invalid_records': invalid,
        'duplicate_event_ids': sorted(set(duplicate_ids)),
        'candidate_dataset_structurally_valid': not invalid and not duplicate_ids,
        'global_census_complete': False,
        'gate_status': 'BLOCKED',
        'gate_reason': 'A candidate census cannot establish global completeness; independent year-level reconciliation and authoritative event adjudication are required.',
    }

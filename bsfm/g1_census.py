from __future__ import annotations

import csv
import hashlib
import io
import json
from datetime import date
from pathlib import Path

from .annual_evidence import audit_annual_completeness

REQUIRED_FIELDS = (
    'event_id', 'event_date', 'manufacturer', 'model', 'fatalities',
    'commercial', 'source_publisher', 'source_record_id', 'source_locator'
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_icao_official_accidents_csv(data: bytes) -> list[dict]:
    """Parse an acquired ICAO Official Accidents CSV without asserting G1 completeness.

    ICAO API field names can evolve. We preserve the raw row and map only fields
    whose semantic aliases are explicitly known. Missing target-critical fields
    remain missing and therefore cannot open G1.
    """
    text = data.decode('utf-8-sig')
    rows = []
    for raw in csv.DictReader(io.StringIO(text)):
        norm = {str(k).strip().lower().replace(' ', '_'): v for k, v in raw.items() if k is not None}
        def pick(*names):
            for name in names:
                value = norm.get(name)
                if value not in (None, ''):
                    return str(value).strip()
            return None
        rows.append({
            'event_id': pick('occurrence_id', 'event_id', 'accident_id', 'id'),
            'event_date': pick('date', 'event_date', 'occurrence_date', 'date_of_occurrence'),
            'manufacturer': pick('manufacturer', 'aircraft_manufacturer', 'make'),
            'model': pick('model', 'aircraft_model', 'aircraft_type'),
            'fatalities': pick('fatalities', 'fatal_injuries', 'number_of_fatalities'),
            'commercial': pick('commercial', 'operation_type', 'type_of_operation'),
            'source_publisher': 'ICAO',
            'source_record_id': pick('occurrence_id', 'event_id', 'accident_id', 'id'),
            'source_locator': 'ICAO API Data Service / Official Accidents',
            'raw': raw,
        })
    return rows


def audit_g1_records(records: list[dict], start_year: int = 2010, end_year: int = 2025) -> dict:
    """Fail-closed structural audit; this cannot by itself attest global completeness."""
    years = {year: 0 for year in range(start_year, end_year + 1)}
    invalid = []
    for i, row in enumerate(records):
        missing = [field for field in REQUIRED_FIELDS if row.get(field) in (None, '')]
        try:
            event_year = date.fromisoformat(str(row.get('event_date', ''))[:10]).year
        except ValueError:
            event_year = None
            if 'event_date' not in missing:
                missing.append('event_date')
        if event_year in years:
            years[event_year] += 1
        if missing:
            invalid.append({'index': i, 'missing': sorted(set(missing))})
    return {
        'schema': 'bsfm.g1-structural-audit.v1',
        'interval': {'start_year': start_year, 'end_year': end_year},
        'records': len(records),
        'records_by_year': years,
        'structurally_complete': not invalid,
        'invalid_records': invalid,
        'global_census_complete': False,
        'gate_status': 'BLOCKED',
        'gate_reason': 'Structural ingestion alone cannot prove exhaustive global target coverage; year-level reconciliation and event-level provenance are required.',
    }


def write_acquisition_manifest(path: Path, *, source: str, locator: str, data: bytes, records: int) -> dict:
    manifest = {
        'schema': 'bsfm.g1-acquisition-manifest.v1',
        'source': source,
        'locator': locator,
        'sha256': sha256_bytes(data),
        'bytes': len(data),
        'records': records,
        'scientific_gate_effect': 'none_without_reconciliation',
    }
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return manifest


def _load_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return default


def _load_jsonl(path):
    try:
        lines = Path(path).read_text(encoding='utf-8').splitlines()
    except OSError:
        return []
    return [json.loads(line) for line in lines if line.strip()]


def load_integrated_candidates(root):
    """Load central + annual G1 candidate surfaces, with annual rows authoritative."""
    root = Path(root)
    merged = {}
    duplicates = []
    central = _load_json(root / 'data/census/g1-candidates.json', {}) or {}
    seen = set()
    for row in central.get('records') or []:
        event_id = str(row.get('event_id') or '').strip()
        if not event_id:
            continue
        if event_id in seen:
            duplicates.append({'surface': 'g1-candidates.json', 'event_id': event_id})
        seen.add(event_id)
        merged[event_id] = row
    for path in sorted((root / 'data/census').glob('candidates-*.jsonl')):
        seen = set()
        for row in _load_jsonl(path):
            event_id = str(row.get('event_id') or '').strip()
            if not event_id:
                continue
            if event_id in seen:
                duplicates.append({'surface': path.name, 'event_id': event_id})
            seen.add(event_id)
            merged[event_id] = row
    return {'rows': list(merged.values()), 'by_id': merged, 'duplicates': duplicates}


def _candidate_year(row):
    try:
        return int(str(row.get('event_date'))[:4])
    except (TypeError, ValueError):
        return None


def audit_integrated_g1_census(root, start_year=2010, end_year=2025):
    """Audit the canonical annual ledger against event-level candidate evidence."""
    root = Path(root)
    ledger = _load_json(root / 'data/census/year-ledger.json', {}) or {}
    candidates = load_integrated_candidates(root)
    by_id = candidates['by_id']
    ledger_rows = {int(r['year']): r for r in (ledger.get('years') or []) if r.get('year') is not None}
    expected_years = list(range(start_year, end_year + 1))

    annual = []
    missing_candidate_ids = []
    extra_candidate_ids = []
    evidence_errors = []
    referenced = set()

    for year in expected_years:
        evidence = _load_json(root / f'data/census/year-evidence-{year}.json', {}) or {}
        included = set(evidence.get('qualifying_candidate_ids') or [])
        unresolved = set(evidence.get('unresolved_candidate_ids') or [])
        expected_ids = included | unresolved
        referenced |= expected_ids
        present_ids = {eid for eid, row in by_id.items() if _candidate_year(row) == year}
        missing = sorted(expected_ids - present_ids)
        extras = sorted(
            eid for eid in present_ids - expected_ids
            if str((by_id[eid] or {}).get('decision') or '').lower() in {'include', 'unresolved'}
        )
        missing_candidate_ids.extend({'year': year, 'event_id': x} for x in missing)
        extra_candidate_ids.extend({'year': year, 'event_id': x} for x in extras)

        controls = evidence.get('controls')
        control_audit = audit_annual_completeness(year, controls) if isinstance(controls, dict) else None
        ledger_reconciled = bool(ledger_rows.get(year, {}).get('reconciled') is True)
        evidence_reconciled = evidence.get('reconciled') is True
        if ledger_reconciled and not (control_audit and control_audit['complete'] and evidence_reconciled):
            evidence_errors.append({'year': year, 'error': 'ledger_reconciled_without_six_of_six_evidence'})
        if evidence_reconciled and not ledger_reconciled:
            evidence_errors.append({'year': year, 'error': 'evidence_reconciled_but_ledger_open'})
        annual.append({
            'year': year,
            'reconciled': ledger_reconciled and evidence_reconciled and bool(control_audit and control_audit['complete']),
            'evidence_progress': control_audit['evidence_progress'] if control_audit else None,
            'qualifying_candidate_ids': sorted(included),
            'unresolved_candidate_ids': sorted(unresolved),
            'missing_candidate_ids': missing,
            'extra_candidate_ids': extras,
        })

    unreferenced = sorted(
        eid for eid, row in by_id.items()
        if start_year <= (_candidate_year(row) or 0) <= end_year
        and str((row or {}).get('decision') or '').lower() in {'include', 'unresolved'}
        and eid not in referenced
    )
    extra_candidate_ids.extend({'year': _candidate_year(by_id[eid]), 'event_id': eid} for eid in unreferenced)
    unreconciled_years = [row['year'] for row in annual if not row['reconciled']]
    qualifying_rows = [
        row for row in candidates['rows']
        if str(row.get('decision') or '').lower() == 'include'
        and start_year <= (_candidate_year(row) or 0) <= end_year
    ]
    complete = not (
        candidates['duplicates'] or missing_candidate_ids or extra_candidate_ids
        or evidence_errors or unreconciled_years
    )
    return {
        'complete': complete,
        'annual': annual,
        'reconciled_years': [row['year'] for row in annual if row['reconciled']],
        'unreconciled_years': unreconciled_years,
        'candidate_rows': len(candidates['rows']),
        'qualifying_rows': len(qualifying_rows),
        'missing_candidate_ids': missing_candidate_ids,
        'extra_candidate_ids': extra_candidate_ids,
        'duplicate_candidate_ids': candidates['duplicates'],
        'evidence_errors': evidence_errors,
        'rows_for_walk_forward': qualifying_rows,
    }

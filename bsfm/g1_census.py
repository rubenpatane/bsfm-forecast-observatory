from __future__ import annotations

import csv
import hashlib
import io
import json
from datetime import date
from pathlib import Path

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

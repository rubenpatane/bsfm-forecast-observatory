from __future__ import annotations

import json
from pathlib import Path

from .exposure import audit_exposure


DEFAULT_COHORTS = (
    '727', '737-Original', '737-Classic', '737-NG', '737-MAX',
    '747', '757', '767', '777', '787',
)


def _load_jsonl(path):
    try:
        lines = Path(path).read_text(encoding='utf-8').splitlines()
    except OSError:
        return []
    rows = []
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            rows.append({'_invalid_json_line': index})
            continue
        rows.append(value if isinstance(value, dict) else {'_invalid_json_line': index})
    return rows


def audit_g2_exposure_pit(root, start_year=2010, end_year=2025, cohorts=DEFAULT_COHORTS):
    """Audit canonical G2 exposure plus vintage/reproducibility metadata."""
    root = Path(root)
    rows = _load_jsonl(root / 'data/exposure/departures.jsonl')
    periods = list(range(int(start_year), int(end_year) + 1))
    matrix = audit_exposure(rows, periods, cohorts)
    metadata_errors = []
    vintage_ids = set()
    for index, row in enumerate(rows):
        if row.get('_invalid_json_line'):
            metadata_errors.append({'index': index, 'error': 'invalid_json'})
            continue
        vintage_policy_id = str(row.get('vintage_policy_id') or '').strip()
        source_vintage_ids = row.get('source_vintage_ids') if isinstance(row.get('source_vintage_ids'), list) else []
        if not vintage_policy_id:
            metadata_errors.append({'index': index, 'error': 'missing_vintage_policy_id'})
        else:
            vintage_ids.add(vintage_policy_id)
        if not source_vintage_ids or any(not str(v).strip() for v in source_vintage_ids):
            metadata_errors.append({'index': index, 'error': 'missing_source_vintage_ids'})
        if row.get('scope') != 'global_commercial':
            metadata_errors.append({'index': index, 'error': 'noncanonical_scope'})
    one_vintage_policy = len(vintage_ids) == 1
    if rows and not one_vintage_policy:
        metadata_errors.append({'error': 'mixed_or_missing_vintage_policy'})
    complete = bool(rows) and matrix['complete'] and not metadata_errors and one_vintage_policy
    return {
        'schema': 'bsfm.g2-exposure-pit-audit.v1',
        'rows': len(rows),
        'matrix': matrix,
        'vintage_policy_ids': sorted(vintage_ids),
        'metadata_errors': metadata_errors,
        'complete': complete,
        'rule': 'G2 requires a complete global cohort-year matrix with one explicit frozen vintage policy and record-level source-vintage provenance; later revisions cannot be mixed silently.',
    }

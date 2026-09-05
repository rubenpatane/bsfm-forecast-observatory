from __future__ import annotations
import json
from datetime import date
from pathlib import Path


def _load(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return default


def _date(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def build_operational_pit_coverage(root) -> dict:
    """Summarize PIT readiness for the currently ingested predictor sources.

    This is deliberately stricter than source/file validity. A successfully
    downloaded historical CSV or AVALL snapshot is not PIT-ready merely because
    it contains old records today. FAA annual files are also checked for a
    late-submission tail: records attributed to an occurrence year can have a
    SubmissionDate years later, directly demonstrating why occurrence/file year
    is not a public-availability timestamp.
    """
    root = Path(root)
    manifests = root / 'data' / 'manifests'

    faa = []
    for path in sorted(manifests.glob('faa-sdr-*.json')):
        row = _load(path, {}) or {}
        year = row.get('year')
        status = row.get('historical_public_availability') or 'unknown'
        max_submission = _date(row.get('max_submission_date'))
        try:
            occurrence_year = int(year)
        except (TypeError, ValueError):
            occurrence_year = None
        submission_lag_years = None
        if occurrence_year is not None and max_submission is not None:
            submission_lag_years = max_submission.year - occurrence_year
        late_tail = bool(submission_lag_years is not None and submission_lag_years > 0)
        faa.append({
            'year': year,
            'manifest': path.name,
            'source_valid': row.get('status') == 'validated',
            'historical_public_availability': status,
            'strict_pit_ready': status == 'verified',
            'max_submission_date': row.get('max_submission_date'),
            'max_submission_lag_years': submission_lag_years,
            'late_submission_tail': late_tail,
        })

    ntsb = _load(manifests / 'ntsb-avall.json', {}) or {}
    ntsb_release = _load(root / 'data/pit/ntsb-release-inventory.json', {}) or {}
    ntsb_field = _load(root / 'data/pit/ntsb-field-release-policy.json', {}) or {}
    faa_release = _load(root / 'data/pit/faa-sdr-release-inventory.json', {}) or {}
    faa_field = _load(root / 'data/pit/faa-sdr-field-release-policy.json', {}) or {}

    faa_verified_years = [r['year'] for r in faa if r['strict_pit_ready']]
    late_tail_years = [r['year'] for r in faa if r['late_submission_tail']]
    max_lag = max((r['max_submission_lag_years'] for r in faa if r['max_submission_lag_years'] is not None), default=None)
    return {
        'schema': 'bsfm.g3-operational-coverage.v2',
        'sources': {
            'FAA SDR': {
                'years': faa,
                'verified_years': faa_verified_years,
                'unverified_years': [r['year'] for r in faa if not r['strict_pit_ready']],
                'all_years_strict_ready': bool(faa) and len(faa_verified_years) == len(faa),
                'release_policy_present': bool(faa_release) and bool(faa_field),
                'late_submission_tail_years': late_tail_years,
                'max_observed_submission_lag_years': max_lag,
                'late_submission_tail_note': 'A late SubmissionDate demonstrates later entry/submission relative to occurrence year; it does not itself establish public approval/release timing.',
            },
            'NTSB AVALL': {
                'source_valid': ntsb.get('status') == 'validated',
                'release_policy_present': bool(ntsb_release) and bool(ntsb_field),
                'record_level_history_complete': False,
                'strict_pit_ready': False,
            },
        },
        'strict_operational_pit_ready': False,
        'g3_status': 'BLOCKED',
        'reason': 'Operational source policies exist, but FAA historical rows remain unverified and NTSB lacks complete record-level historical release/version evidence.'
    }


def write_operational_pit_coverage(root, out=None) -> dict:
    root = Path(root)
    state = build_operational_pit_coverage(root)
    out = Path(out) if out else root / 'data/pit/operational-coverage.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(state, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return state

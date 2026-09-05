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
    """Summarize strict PIT readiness for the explicitly admitted predictor universe."""
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
    universe = _load(root / 'data/pit/predictor-universe-v1.json', {}) or {}

    faa_verified_years = [r['year'] for r in faa if r['strict_pit_ready']]
    faa_all_ready = bool(faa) and len(faa_verified_years) == len(faa)
    faa_policy_ready = bool(faa_release) and bool(faa_field)
    faa_strict_ready = faa_all_ready and faa_policy_ready
    late_tail_years = [r['year'] for r in faa if r['late_submission_tail']]
    max_lag = max((r['max_submission_lag_years'] for r in faa if r['max_submission_lag_years'] is not None), default=None)

    # Current AVALL is a current-state snapshot. Release/schema anchors exist, but
    # a complete record-level historical snapshot chain is not yet evidenced.
    ntsb_record_history_complete = False
    ntsb_strict_ready = (
        ntsb.get('status') == 'validated'
        and bool(ntsb_release) and bool(ntsb_field)
        and ntsb_record_history_complete
    )

    # These are the actual dependency surfaces of the implemented shrinkage
    # estimator. They remain fail-closed until their own PIT/vintage evidence is
    # materialized; research-only FAA/NTSB enrichment cannot substitute for them.
    g1_target_history_ready = False
    g2_exposure_history_ready = False

    admitted = universe.get('admitted_predictors') if isinstance(universe.get('admitted_predictors'), list) else []
    universe_frozen = universe.get('frozen') is True and universe.get('status') == 'FROZEN'
    source_ready = {
        'G1 target census': g1_target_history_ready,
        'G2 exposure matrix': g2_exposure_history_ready,
        'FAA SDR': faa_strict_ready,
        'NTSB AVALL': ntsb_strict_ready,
    }
    admitted_checks = []
    for row in admitted:
        row = row if isinstance(row, dict) else {}
        source = row.get('source')
        fields = row.get('fields') if isinstance(row.get('fields'), list) else []
        evidence_ids = row.get('evidence_ids') if isinstance(row.get('evidence_ids'), list) else []
        row_ready = (
            bool(source) and bool(fields) and bool(evidence_ids)
            and row.get('pit_status') == 'verified'
            and row.get('field_evidence_complete') is True
            and row.get('snapshot_evidence_complete') is True
            and source_ready.get(source) is True
        )
        admitted_checks.append({
            'source': source,
            'fields': fields,
            'pit_status': row.get('pit_status', 'unknown'),
            'evidence_ids': evidence_ids,
            'strict_pit_ready': row_ready,
            'known_source': source in source_ready,
        })

    strict_ready = universe_frozen and bool(admitted_checks) and all(r['strict_pit_ready'] for r in admitted_checks)
    if not universe_frozen:
        reason = 'The predictor universe is not frozen; no strict historical backtest may pass G3.'
    elif not admitted_checks:
        reason = 'The frozen predictor universe contains no admitted predictors.'
    elif not strict_ready:
        reason = 'At least one admitted predictor lacks complete source/field/snapshot PIT evidence.'
    else:
        reason = None

    return {
        'schema': 'bsfm.g3-operational-coverage.v3',
        'predictor_universe': {
            'schema': universe.get('schema'),
            'status': universe.get('status', 'MISSING'),
            'frozen': universe_frozen,
            'admitted_count': len(admitted_checks),
            'admitted_predictors': admitted_checks,
        },
        'sources': {
            'G1 target census': {
                'strict_pit_ready': g1_target_history_ready,
                'reason': 'Historical outcome/publication timing is not yet complete for a frozen cutoff-by-cutoff event-history input.',
            },
            'G2 exposure matrix': {
                'strict_pit_ready': g2_exposure_history_ready,
                'reason': 'Compatible global cohort-year exposure and its vintage policy remain unavailable.',
            },
            'FAA SDR': {
                'years': faa,
                'verified_years': faa_verified_years,
                'unverified_years': [r['year'] for r in faa if not r['strict_pit_ready']],
                'all_years_strict_ready': faa_all_ready,
                'release_policy_present': faa_policy_ready,
                'strict_pit_ready': faa_strict_ready,
                'late_submission_tail_years': late_tail_years,
                'max_observed_submission_lag_years': max_lag,
                'late_submission_tail_note': 'A late SubmissionDate demonstrates later entry/submission relative to occurrence year; it does not itself establish public approval/release timing.',
            },
            'NTSB AVALL': {
                'source_valid': ntsb.get('status') == 'validated',
                'release_policy_present': bool(ntsb_release) and bool(ntsb_field),
                'record_level_history_complete': ntsb_record_history_complete,
                'strict_pit_ready': ntsb_strict_ready,
            },
        },
        'strict_operational_pit_ready': strict_ready,
        'g3_status': 'PASS' if strict_ready else 'BLOCKED',
        'reason': reason,
    }


def write_operational_pit_coverage(root, out=None) -> dict:
    root = Path(root)
    state = build_operational_pit_coverage(root)
    out = Path(out) if out else root / 'data/pit/operational-coverage.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(state, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return state

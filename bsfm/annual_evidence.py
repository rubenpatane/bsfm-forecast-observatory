from __future__ import annotations

ANNUAL_CONTROLS = (
    'annual_source_scope_demonstrated',
    'all_fatal_jets_mapped',
    'boeing_target_membership_mapped',
    'competent_authority_per_candidate',
    'independent_reconciliation',
    'target_taxonomies_resolved',
)


def audit_annual_completeness(year, controls):
    """Six-cell fail-closed annual attestation audit for G1."""
    normalized = {name: bool((controls or {}).get(name, False)) for name in ANNUAL_CONTROLS}
    passed = sum(normalized.values())
    unresolved = [name for name, ok in normalized.items() if not ok]
    reconciled = passed == len(ANNUAL_CONTROLS)
    return {
        'year': int(year), 'controls': normalized, 'passed_controls': passed,
        'total_controls': len(ANNUAL_CONTROLS), 'evidence_progress': f'{passed}/{len(ANNUAL_CONTROLS)}',
        'unresolved_controls': unresolved, 'reconciled': reconciled,
        'status': 'RECONCILED' if reconciled else 'OPEN',
    }

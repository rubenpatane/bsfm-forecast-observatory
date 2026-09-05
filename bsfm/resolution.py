from __future__ import annotations

DIMENSION_REQUIREMENTS = {
    'geography': ('estimator_supported','exposure_denominator_supported','pit_supported','provenance_supported','uncertainty_supported'),
    'msn': ('estimator_supported','airframe_exposure_supported','identity_history_supported','pit_supported','provenance_supported','uncertainty_supported'),
    'flight_number': ('estimator_supported','operational_source_access_supported','flight_exposure_supported','pit_supported','provenance_supported','uncertainty_supported'),
}


def audit_resolution_dimension(dimension, evidence):
    req = DIMENSION_REQUIREMENTS[dimension]
    checks = {name: (evidence or {}).get(name) is True for name in req}
    missing = [name for name, ok in checks.items() if not ok]
    return {'dimension':dimension,'status':'SUPPORTED' if not missing else 'BLOCKED','checks':checks,'missing':missing}


def audit_resolution(evidence_by_dimension):
    return {name:audit_resolution_dimension(name,(evidence_by_dimension or {}).get(name,{})) for name in DIMENSION_REQUIREMENTS}

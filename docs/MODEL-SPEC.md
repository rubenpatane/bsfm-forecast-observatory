# BSFM Model Specification

Status: canonical model-level orientation
Updated: 2026-09-05

BSFM is an experimental prospective forecasting laboratory for hazards/events involving Boeing commercial jets. It freezes forecasts ex ante, acquires auditable evidence and evaluates them prospectively. It is not certification or a safety assessment of a specific flight, aircraft, operator, route or person.

## Model lineage and forecast objects
Current lineage: BSFM v1.2, Dynamic Airframe Hazard, extending airframe/family reasoning toward time-varying hazard/exposure information. Ambition does not imply that all historical inputs are available/validated. A forecast is a versioned record with cutoff, target, frozen prediction fields, claim level and provenance/integrity metadata. Once frozen, prediction content is immutable; later evidence/scoring/refinements are separate records.

F-002 is the current frozen prospective forecast. Authoritative values: `forecasts/F-002.json`; evaluation: `docs/F-002-PREREGISTRATION-v1.md`. Never reconstruct or modify it from this summary.

BSFM-PD 1.3 is a separate U.S.-linked minimal public-data estimator whose
historical result is negative and underpowered. BSFM-PD 1.4 preserves its
target, scope, estimator, exposure rule, horizon and baseline, and adds only
preregistered prospective issuance/evaluation governance. It may publish
experimental unvalidated records from public online sources while global BSFM
1.2 remains blocked. Its contract and protocol are
`config/model-public-data-v1.4.json` and
`docs/PUBLIC-DATA-PROSPECTIVE-v1.4.md`.

## Target/evidence semantics
Historical validation requires an event universe with inclusion/exclusion semantics fixed before scoring. Event evidence must support target and commercial/Boeing eligibility; ambiguity remains unresolved. Potential evidence families include airframe/family/configuration, utilization/exposure, operational/route/airport/phase, service-difficulty/occurrence and temporal/seasonal information. Historical predictors are admissible only when their point-in-time public availability at the simulated cutoff is established under G3. Never back-project a current field merely because it exists today.

## Outputs/baseline/validation
Keep target-event hazard, escalation, phase, geography and time-to-event distinct. MSN/operator/location specificity requires actual model/evidence support; otherwise it remains unspecified. A meaningful baseline uses defensible exposure under G2. Candidate and baseline use identical rolling-origin/walk-forward cutoffs/universe. Calibration, sharpness/proper scores apply where ex-ante probabilities permit. Never manufacture retrospective probabilities for F-002. Report dimension-level results rather than selecting a post-hoc composite `hit`.

G1 is global/reconciled target census; G2 exposure; G3 PIT predictor availability; G4 genuine OOS candidate-vs-baseline evaluation. Detailed criteria are in `docs/G1-G3-EVIDENCE-PLAN-v1.md` and `docs/LABORATORY-PROTOCOL.md`. Material target/predictor/exposure/validation/scoring changes must be versioned before interpreting new outcomes; frozen forecasts remain attached to their original specification.

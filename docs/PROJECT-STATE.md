# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository; F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`; it remains manual (`workflow_dispatch`).
- **AGGIORNA #11 completed successfully on `e24e27e1…`; 65 tests passed before and after refresh.** Registry integrity passed and the generated auditable-state commit is `a5fb38cfb120d57bed7003f08557cc267f003dd2`.
- Live NTSB normalization remains 31,670 event-aircraft rows, 1,894 Boeing rows and 50 fatal Boeing rows. `availability_known=0`; approval/change timestamps remain outcome/administrative metadata, not demonstrated historical public availability.
- FAA SDR 2010-2026 refresh remains operational, but historical public availability is unverified because FAA approval/QC occurs after submission. SDR predictor eligibility therefore remains blocked.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7. Scientific gates remain fail-closed.

## Execution rule — final implementation batch
`docs/FINAL-IMPLEMENTATION-PLAN.md` is now the persistent execution checklist. From commit `74925a7046e6f66703aa8bc855291ca1a2edafbb` onward, **no intermediate AGGIORNA is requested**. Code, data, tests, scientific audits and documentation are accumulated to maximum defensible completion first. One integrated AGGIORNA is requested only after the final pre-verification audit. A further run is justified only if that integrated run exposes a real defect.

## Historical Backtest Foundation / Model Evaluation batch
Implemented after AGGIORNA #11 and not yet workflow-verified:
- fail-closed machine-readable census event ledger and annual reconciliation ledger;
- fail-closed departures exposure ledger and explicit prohibition on deriving Boeing-family denominators from global traffic totals, fleet counts or accident counts;
- integrated historical-foundation audit combining census, exposure, point-in-time availability and leakage gates;
- walk-forward descriptors with strict **next-event-after-cutoff** semantics: a T-365/T-90 case is excluded when another qualifying target occurs between cutoff and the nominal target;
- explicit case IDs for paired candidate/reference scoring;
- point-in-time snapshot helper that admits only rows with `historical_public_availability=verified` and an explicit `available_at <= cutoff`;
- binary calibration/reliability diagnostics and Brier scoring;
- multiclass Brier primitive for mutually exclusive cohort outcomes;
- paired candidate-versus-exposure-baseline comparison that fails closed on unpaired cases or outcome disagreement;
- lifecycle split into a pre-fit evidence gate and a stricter post-fit promotion gate, removing the circular requirement that calibration exist before a candidate can be fitted;
- promotion additionally requires calibration, a paired baseline comparison and measured improvement over baseline;
- CLI `audit-foundation` command for an auditable readiness report;
- regression tests covering construction ledgers, next-event semantics, eligibility, scoring and lifecycle gates.

## Source reconciliation evidence
- EASA Annual Safety Review archive and ICAO safety reporting provide authoritative scope/case reconciliation layers, but their scopes are not silently merged.
- ICAO global scheduled traffic values are retained as context only. The context ledger includes 2023 (>35m departures), 2024 (37.09m scheduled-commercial departures for the >5,700 kg safety-report scope), and 2025 (~38m flights) in addition to earlier context observations.
- These global totals are **not** Boeing-family denominators and cannot set `baseline_present`.
- A defensible annual Boeing-family departures matrix for 2010-2025 has not yet been established from public authoritative evidence; no fleet-share allocation or invented denominator is permitted.

## Scientific gate
No new prospective forecast may be represented as validated until leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Source integrity is ready; historical point-in-time predictor availability, provenance-complete global historical cases and Boeing-cohort exposure remain incomplete. Construction placeholders are never interpreted as zero-event or zero-exposure evidence.

The lifecycle distinguishes two stages:
1. **fit gate** — source integrity + verified point-in-time availability + leakage-free historical cases + complete exposure baseline;
2. **promotion gate** — all fit evidence plus calibration + paired baseline comparison + candidate improvement.

No estimator is currently fitted or promoted.

## Exact next step
Follow `docs/FINAL-IMPLEMENTATION-PLAN.md` from workstream A through H without intermediate workflow requests. Continue event-level 2010-2025 reconciliation, authoritative Boeing-family exposure research, point-in-time eligibility, integrated evaluation/lifecycle implementation, tests and repository audit. Preserve unresolved evidence as BLOCKED rather than estimating it. Request one AGGIORNA only after the final pre-verification HEAD has been frozen here.

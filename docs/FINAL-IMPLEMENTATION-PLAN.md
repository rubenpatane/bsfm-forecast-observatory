# BSFM final implementation plan — single AGGIORNA strategy

Status: ACTIVE
Date: 2026-09-05
Owner: BSFM Forecast Observatory

## Operating rule

From this point, implementation is accumulated on `main` without requesting intermediate AGGIORNA runs. AGGIORNA is requested only after the complete implementation/audit batch is ready. A second run is requested only if the final integrated run reveals a real defect.

This document is the persistent execution checklist. It must be updated as work advances so a new session can resume without relying on chat memory.

## Scientific invariants

1. F-002 is immutable and remains experimental/unvalidated.
2. No retrospective predictor may enter a historical case unless its public availability at the cutoff is verified.
3. Outcome/final-report timestamps never establish predictor availability.
4. Census, exposure, point-in-time availability, leakage, calibration and promotion gates remain independent and fail closed.
5. Global ICAO traffic totals are context only; they are never silently allocated to Boeing cohorts.
6. Manufacturer material may triangulate target truth but is not sole independent ground truth.
7. Missing evidence is represented as BLOCKED/UNKNOWN, never as zero.
8. No candidate is promoted merely because code/tests execute.
9. Failed backtests and negative results are retained.
10. Absolute accident probabilities remain disabled until empirical calibration is defensible.

## Final implementation workstreams

### A. Historical target truth 2010–2025
- Complete event-level candidate census for the preregistered target definition.
- Reconcile each year explicitly, including genuine zero-event years.
- Require scope/provenance and independent publishers.
- Preserve unresolved scope conflicts instead of guessing.
- Populate `data/census/events.jsonl` only with admitted qualifying targets.
- Populate `data/census/year-ledger.json` only when annual reconciliation is defensible.
- Keep unresolved candidates in separate construction/evidence ledgers.

### B. Exposure baseline
- Search authoritative historical Boeing-family departures/exposure evidence.
- Prefer directly observed annual departures.
- Permit reconstructed cumulative/annual intervals only when mathematically identified from published counts/rates, with uncertainty retained.
- Never convert global traffic or fleet share into fabricated family departures.
- Complete `data/exposure/departures.jsonl` only where source scope and provenance support the cell.
- If a full 2010–2025 Boeing-family matrix cannot be defensibly reconstructed, record the exact limitation and keep `baseline_present=false`.

### C. Point-in-time predictor eligibility
- Finish manifest-level availability semantics.
- Require `available_at <= cutoff` for every historical predictor.
- Missing, malformed, inferred, approval-only, or later availability fails closed.
- Keep FAA SDR historical eligibility blocked unless public-release evidence is demonstrated.
- Keep NTSB outcome/admin dates separate from predictor-publication evidence.

### D. Walk-forward evaluation
- Generate T-365/T-90/T-30/T-7 cases from admitted targets.
- Enforce next-event-after-cutoff target semantics.
- Prevent future-event/census leakage.
- Produce stable case IDs and immutable evaluation descriptors.
- Score temporal, family/model, phase, event/failure class and coarse geography dimensions.

### E. Baseline, candidate and calibration
- Implement paired candidate-vs-exposure-null evaluation on identical cases.
- Compute proper probabilistic scores (Brier; multiclass where applicable).
- Produce reliability/calibration diagnostics only on real OOS predictions.
- Do not set `calibration_evaluated=true` from scaffolding or synthetic fixtures.
- Define promotion criteria against incumbent and exposure-only null with minimum evidence checks.

### F. Model lifecycle
- Keep fit-readiness distinct from promotion-readiness.
- Candidate fitting requires source integrity + PIT + leakage-free + historical cases + baseline.
- Promotion additionally requires completed OOS comparison/calibration and explicit improvement criteria.
- Retain incumbent on any failed/unknown gate.
- Record version/hash/input snapshot/evaluation evidence for any future candidate.

### G. Integrated audit and UX
- `audit-foundation` must expose every gate and blocked reason.
- Add machine-readable final readiness report.
- Ensure public-facing language never implies validated crash prediction.
- Verify exactly one GitHub workflow remains: AGGIORNA.
- Verify workflow performs source refresh, tests, integrity, foundation audit, lifecycle gate, auditable-state commit/artifacts.

### H. Tests and final audit
- Unit tests for every fail-closed edge case.
- End-to-end tests for census → exposure → PIT → walk-forward → scoring → lifecycle.
- Regression tests preventing scientific gates from opening on placeholders.
- Audit repository for duplicate/dead/conflicting logic.
- Audit documentation against actual code and data.
- Update `docs/PROJECT-STATE.md` with exact final pre-AGGIORNA HEAD and blocked evidence.

## Final verification protocol

Only after A–H are complete to the maximum defensible extent:

1. Freeze the pre-verification HEAD in PROJECT-STATE.
2. Request one manual `Actions → AGGIORNA → Run workflow`.
3. Verify the run used that exact SHA.
4. Verify all tests before/after refresh, registry integrity, source refresh, foundation report, lifecycle state and generated auditable-state commit.
5. If green, record the generated-state SHA and declare the software batch verified.
6. Scientific gates that lack real-world evidence remain explicitly blocked even when software verification is green.
7. Request another AGGIORNA only if the integrated run exposes a real implementation defect.

## Resume rule

At every continuation, read this file and `docs/PROJECT-STATE.md` first. Continue from the first incomplete workstream. Do not request an intermediate AGGIORNA merely to gain confidence; use code review, source evidence and tests added to the batch, reserving the workflow for final integrated verification.

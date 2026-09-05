# BSFM Project State

Updated: 2026-09-05

## Last workflow-verified baseline
- F-002 remains frozen and explicitly experimental/unvalidated.
- Exactly one operational GitHub Actions workflow exists: `AGGIORNA`, manual `workflow_dispatch`.
- **AGGIORNA #11 passed on `e24e27e1…`; 65 tests passed before and after refresh.** Generated auditable-state commit: `a5fb38cfb120d57bed7003f08557cc267f003dd2`.
- Everything after that generated-state commit belongs to the accumulated final implementation batch and has intentionally not received an intermediate workflow run.

## Final implementation freeze
Implementation/static-audit anchor immediately before this state-only freeze commit: `14a5747067f7737926bc91e2262cb31b32e7ad6c`.

The final batch now contains:
- strict census/year reconciliation and construction-candidate separation;
- strict Boeing-cohort exposure audit plus context-only global traffic separation;
- cumulative-rate exposure reconstruction with uncertainty retained;
- verified-public-availability PIT eligibility;
- strict next-event T-365/T-90/T-30/T-7 walk-forward descriptors;
- stable case IDs and duplicate/malformed prediction rejection;
- temporal and multidimensional scoring primitives;
- binary reliability/Brier and multiclass Brier;
- paired candidate-versus-exposure-null comparison;
- shrinkage hazard candidate estimator for rare/small-sample cohort data;
- explicit leakage-safe OOS case runner;
- centralized Boeing model→cohort mapping;
- independent fit gate and stricter post-fit promotion gate;
- content-addressed candidate model registry and explicit promotion transition;
- machine-readable `audit-foundation` and `audit-final` readiness surfaces;
- one AGGIORNA workflow extended to execute the scientific audits as part of the integrated run;
- regression tests for the new fail-closed paths;
- final implementation plan, evidence-gap register and static audit.

## Static audit result
`docs/FINAL-STATIC-AUDIT.md` records the pre-workflow audit. Conflicting legacy logic was corrected: generic timestamp eligibility no longer bypasses verified PIT status; legacy publication gating now requires paired-baseline/superiority evidence; duplicate case IDs cannot be silently overwritten; fit and promotion readiness are non-circular.

## Empirical evidence state
`docs/FINAL-EVIDENCE-GAPS.md` is authoritative. Software implementation does not fabricate missing science:
- G1 global target census 2010–2025: BLOCKED pending exhaustive reconciliation;
- G2 Boeing-family annual departures matrix: BLOCKED pending defensible authoritative exposure;
- G3 historical public availability for current FAA SDR/NTSB snapshots: BLOCKED where release timing is unverified;
- G4 real calibration/candidate superiority: BLOCKED downstream of G1–G3.

Accordingly `historical_cases`, `baseline_present`, `point_in_time_availability_verified`, `leakage_free`, `calibration_evaluated`, paired comparison and promotion remain fail closed unless real evidence opens them. Absolute accident probabilities and validated-prediction claims remain disabled.

## Execution rule
No more implementation changes should be made before the integrated verification unless static inspection finds a concrete defect. The next action is exactly one manual `Actions → AGGIORNA → Run workflow` on the current `main` HEAD. After it completes, inspect the exact SHA, pre/post test totals, registry integrity, source refresh, NTSB normalization, foundation/final audits, lifecycle state, artifact and generated-state commit. A second AGGIORNA is permitted only if this final run reveals a real defect.

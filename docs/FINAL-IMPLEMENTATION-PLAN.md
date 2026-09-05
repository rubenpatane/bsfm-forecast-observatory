# BSFM final implementation plan — single AGGIORNA strategy

Status: PRE-VERIFICATION AUDIT
Date: 2026-09-05
Owner: BSFM Forecast Observatory

## Operating rule
Implementation is accumulated on `main` without intermediate AGGIORNA runs. One integrated AGGIORNA is requested only after the complete implementation/audit batch is frozen. A second run is justified only by a real defect found in that final run.

## Scientific invariants
1. F-002 is immutable and experimental/unvalidated.
2. Historical predictors require verified public availability at cutoff.
3. Outcome/final-report timestamps never establish predictor availability.
4. Census, exposure, PIT, leakage, calibration and promotion gates are independent and fail closed.
5. Global ICAO traffic totals are context only, never Boeing-cohort exposure.
6. Missing evidence is BLOCKED/UNKNOWN, never zero.
7. Unit/synthetic tests validate software only, never empirical calibration.
8. Failed backtests and negative results are retained.
9. Absolute accident probabilities stay disabled until empirical calibration/promotion evidence passes.

## Workstream state

### A. Historical target truth 2010–2025 — SOFTWARE COMPLETE / EMPIRICAL RECONCILIATION BLOCKED
Implemented event schema, independent-provenance validation, annual attestations including explicit zero years, count reconciliation, construction candidate separation and fail-closed census audit. 2024 construction candidates are evidence-backed but are not treated as proof of an exhaustive global year. Full 2010–2025 global reconciliation remains an empirical evidence task; see `docs/FINAL-EVIDENCE-GAPS.md` G1.

### B. Exposure baseline — SOFTWARE COMPLETE / EMPIRICAL MATRIX BLOCKED
Implemented strict period×cohort audit, metadata/scope validation, exposure-only null, global-context separation and bounded cumulative-rate reconstruction primitives. No fleet-share/delivery/accident proxy is admitted. A complete authoritative Boeing-family annual departures matrix has not been established; `baseline_present=false` remains scientifically correct. See G2.

### C. Point-in-time predictor eligibility — SOFTWARE COMPLETE / CURRENT HISTORICAL SOURCES BLOCKED
Implemented verified `available_at <= cutoff` eligibility and OOS rejection of future/unverified rows. FAA SDR and current NTSB snapshots remain blocked where public-release timing is not demonstrated. See G3.

### D. Walk-forward evaluation — IMPLEMENTED, PENDING FINAL AGGIORNA
Implemented T-365/T-90/T-30/T-7 descriptors, strict next-event semantics, stable case IDs, duplicate/malformed-case rejection, PIT OOS execution and multidimensional F-002 scoring primitives.

### E. Baseline, candidate and calibration — IMPLEMENTED, EMPIRICAL RESULTS BLOCKED
Implemented exposure-only null, paired Brier comparison, binary reliability/calibration diagnostics, multiclass Brier and a small-data shrinkage hazard candidate estimator. Calibration/pairwise superiority cannot become scientific PASS until real leakage-free OOS cases exist. See G4.

### F. Model lifecycle — IMPLEMENTED, PENDING FINAL AGGIORNA
Implemented independent fit and promotion gates, gated estimator fitting, incumbent retention, content-addressed candidate model records and explicit promotion-only record transition. Candidate fitting cannot bypass the evidence gate.

### G. Integrated audit and workflow — IMPLEMENTED, PENDING FINAL AGGIORNA
`audit-foundation` and `audit-final` expose scientific blockers. Exactly one workflow remains, `AGGIORNA`. It now runs foundation/final audits in addition to tests, registry integrity, source refresh, NTSB normalization, lifecycle evaluation, artifact upload and auditable generated-state commit.

### H. Tests and final audit — CODE REVIEW COMPLETE / RUNTIME VERIFICATION PENDING
Added regression coverage for census, exposure, PIT, next-event semantics, calibration, paired scoring, duplicate/invalid cases, estimator, OOS execution, lifecycle, model registry and final readiness. No intermediate workflow run is used. Runtime verification is intentionally reserved for the single final AGGIORNA.

## Evidence-gap rule
`docs/FINAL-EVIDENCE-GAPS.md` is authoritative for unresolved empirical blockers. A green workflow means **software batch verified**. It does not mean **predictive validity demonstrated** unless the evidence gates independently pass.

## Final verification protocol
1. Finish static repository/documentation audit.
2. Freeze the exact pre-verification HEAD in `docs/PROJECT-STATE.md`.
3. Request one manual `Actions → AGGIORNA → Run workflow`.
4. Verify the run used that SHA and inspect pre/post tests, registry, source refresh, audits, lifecycle, artifact and generated-state commit.
5. If green, record generated-state SHA and close the software implementation batch.
6. Request another AGGIORNA only if the integrated run exposes a real implementation defect.

## Resume rule
Read this file, `docs/PROJECT-STATE.md`, and `docs/FINAL-EVIDENCE-GAPS.md`. Do not reopen empirical BLOCKED items by estimation. The only remaining implementation activity before involving the user is the static final audit and freezing of the pre-verification HEAD.

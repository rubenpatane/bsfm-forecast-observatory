# BSFM Project State

Updated: 2026-09-05

## Last workflow-verified baseline
- F-002 remains frozen and explicitly experimental/unvalidated.
- Exactly one operational GitHub Actions workflow exists: `AGGIORNA`, manual `workflow_dispatch`.
- AGGIORNA #14 passed end-to-end: 95 tests before/after refresh, registry/source/audit lifecycle successful, generated state committed and GitHub Pages deployed.

## New pre-verification batch
Implemented after #14, intentionally without an intermediate AGGIORNA:
- `bsfm/evidence_automation.py`: machine-readable G1–G4 evidence inventory with SHA-256 artifact provenance and canonical fail-closed gate mirroring;
- AGGIORNA now generates `site/data/evidence-state.json` after the scientific audit; acquisition/inventory can never manufacture a PASS;
- existing NTSB normalization retains explicit `PublicationDate` when present as `available_at`, while approval/change dates remain non-substitutable; the canonical availability/leakage audit still decides admission;
- `bsfm/refinements.py` now supports automatic append-only publication of `R-F002-*` records only when structurally valid and `provenance_gate_passed=true`;
- F-002 is never rewritten and every public refinement explicitly states that it does not alter the original F-002 score;
- AGGIORNA generates `site/data/refinements.json`; no refinement is invented when no provenance-gated record exists;
- Overview exposes the refinement timeline and G1–G4 evidence state;
- all four public pages include persistent `ITA | EN` controls with URL `?lang=` sharing and local preference persistence;
- dynamic scientific state remains language-neutral and single-source, preventing IT/EN scientific divergence;
- tests extended for bilingual controls, evidence fail-closed behavior and refinement publication gate.

## Evidence policy
G1 global census, G2 Boeing-family annual exposure, G3 historical PIT availability and G4 OOS calibration/superiority remain scientific evidence gates, not software completion flags. Missing evidence remains BLOCKED. Current official NTSB downloadable data remain a US civil aviation census rather than global truth; FAA SDR records remain predictors only where historical public availability can be demonstrated. No proxy denominator is promoted merely to make G2 computable.

## NTSB transition resilience
The acquisition/scientific layers remain separated because NTSB states that the downloadable aviation dataset will transition to its Enterprise API on 2027-04-05. The current MDB adapter can therefore be replaced without changing gate semantics.

## Verification boundary
This batch is frozen for integrated verification. Do not make further implementation changes before verification unless static inspection identifies a concrete defect.

Exact next step: run exactly one manual `Actions → AGGIORNA → Run workflow` from current `main`. Verify tests, registry, FAA/NTSB refresh, final scientific audit, evidence-state generation, refinement publication, generated-state commit and GitHub Pages deployment. A second run is allowed only if this integrated run reveals a real defect.

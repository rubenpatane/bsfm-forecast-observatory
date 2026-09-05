# BSFM Project State

Updated: 2026-09-05

## Last workflow-verified baseline
- F-002 remains frozen and explicitly experimental/unvalidated.
- Exactly one operational GitHub Actions workflow exists: `AGGIORNA`, manual `workflow_dispatch`.
- AGGIORNA #14 passed end-to-end: 95 tests before/after refresh, registry/source/audit lifecycle successful, generated state committed and GitHub Pages deployed.
- That run remains the last runtime-verified baseline. Changes below are a new pre-verification batch and must not be described as deployed or runtime-verified until a new AGGIORNA succeeds.

## Public observatory UX / localization batch
Implemented after #14:
- Italian is now the default public language; Italian and English dictionaries cover the Overview, Validation, Methodology and Provenance pages, including dynamically rendered gate labels.
- Every public page now has a responsive mobile navigation button with expanded/collapsed menu, `aria-expanded`, close-on-navigation and Escape handling.
- Overview now explains in plain language what BSFM is, what it is not, why forecasts are frozen before outcomes, and the six-step path from official source acquisition to prospective scoring and baseline comparison.
- The safety boundary remains explicit: BSFM is experimental research and does not assess the safety of a specific flight, aircraft, airline, route or person.

## Real acquired-data publication
A new auditable descriptive-data surface has been added without changing any scientific gate:
- current-year FAA SDR ingestion generates `site/data/real-data.json` with total rows, Boeing rows, latest observed `DifficultyDate`, model frequencies and the latest Boeing service-difficulty reports;
- published FAA detail is deliberately small and derived: date, model, JASC/stage/condition codes, component and truncated discrepancy text;
- every public surface states that an FAA SDR is a service-difficulty report, not necessarily an accident, a verified causal finding or a BSFM prediction;
- during the same AGGIORNA, the current official NTSB AVALL normalization statistics are merged into the public real-data state;
- the NTSB snapshot remains outcome evidence for its documented scope and is never presented as a global Boeing accident census;
- real-data publication is generated from the official sources acquired by the same workflow, rather than from manually entered examples.

## Evidence/refinement automation already in the batch
- `bsfm/evidence_automation.py`: machine-readable G1–G4 evidence inventory with SHA-256 artifact provenance and canonical fail-closed gate mirroring;
- AGGIORNA generates `site/data/evidence-state.json`; acquisition/inventory can never manufacture a PASS;
- NTSB normalization retains explicit `PublicationDate` when present as `available_at`, while approval/change dates remain non-substitutable; the canonical availability/leakage audit still decides admission;
- `bsfm/refinements.py` supports automatic append-only publication of `R-F002-*` records only when structurally valid and `provenance_gate_passed=true`;
- F-002 is never rewritten and public refinements do not alter its original score;
- AGGIORNA generates `site/data/refinements.json`; no refinement is invented when no provenance-gated record exists.

## Tests added/updated
Static and unit tests now cover:
- mobile navigation markup and responsive behavior contract on all four pages;
- Italian-default bilingual persistence and translation-key coverage;
- explanatory/real-data public surfaces and the absence of a scientific-validation claim;
- FAA public summary Boeing filtering, date ordering, model aggregation and interpretation warning;
- AGGIORNA generation of FAA/NTSB public real-data state alongside evidence/refinement state and Pages deployment.

## Evidence policy
G1 global census, G2 Boeing-family annual exposure, G3 historical PIT availability and G4 OOS calibration/superiority remain scientific evidence gates, not software completion flags. Missing evidence remains BLOCKED. Current official NTSB downloadable data remain a US civil aviation dataset rather than global truth; FAA SDR records remain predictors only where historical public availability can be demonstrated. No proxy denominator is promoted merely to make G2 computable.

## NTSB transition resilience
The acquisition/scientific layers remain separated because NTSB states that the downloadable aviation dataset will transition to its Enterprise API on 2027-04-05. The current MDB adapter can therefore be replaced without changing gate semantics.

## Verification boundary
No manually fabricated latest-report list is committed. The real-data JSON must be produced from the next official FAA/NTSB acquisition. Therefore the current source changes require one integrated runtime verification/deployment.

Exact next step: run one manual `Actions → AGGIORNA → Run workflow` from current `main`. It must pass the complete test/audit chain, acquire current FAA SDR and NTSB AVALL data, generate `site/data/real-data.json`, merge NTSB statistics, commit generated auditable state, and deploy GitHub Pages. Only after that run succeeds may this UX/data batch be called live and runtime-verified.

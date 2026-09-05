# BSFM Project State

Updated: 2026-09-05

## Last workflow-verified baseline
- F-002 remains frozen and explicitly experimental/unvalidated.
- Exactly one operational GitHub Actions workflow exists: `AGGIORNA`, manual `workflow_dispatch`.
- AGGIORNA #16 (`33968206601`) passed end-to-end from source commit `e21e5cab72b3a51008dbe0da847bd38fada7364e`.
- All workflow steps completed successfully: pre-update tests/integrity, FAA current refresh, FAA 2010-current historical manifests, NTSB AVALL download/extraction/normalization, post-update tests and scientific audits, readiness/evidence/refinement generation, auditable generated-state commit, GitHub Pages upload and deployment.
- The workflow committed the refreshed auditable state as `2fc06b555f6ea4676e093a928cccb96b87b887d0` (`chore(observatory): AGGIORNA auditable state`).
- The public observatory UX/localization/real-data batch is therefore runtime-verified and deployed.

## What AGGIORNA does
`AGGIORNA` is the single full refresh, verification and publication pipeline for the observatory. In one controlled run it:
1. checks out the current repository and installs the pinned/runtime dependencies;
2. executes tests, registry verification and foundation audit before touching refreshed data;
3. downloads the current official FAA Service Difficulty Reports dataset;
4. refreshes the FAA SDR historical manifests from 2010 through the current year;
5. downloads and extracts the current official NTSB AVALL snapshot;
6. normalizes NTSB event-aircraft data conservatively, without substituting administrative dates for unproven publication dates;
7. derives the current nonfatal comparison set for F-002 from that same NTSB snapshot using a fixed, machine-readable similarity rule;
8. reruns the full test, registry and scientific-audit chain after acquisition;
9. evaluates the fail-closed model lifecycle and final scientific readiness;
10. generates the public machine-readable state: readiness, G1-G4 evidence inventory, provenance-gated refinements, real acquired-data statistics/recent FAA Boeing reports, and F-002 comparable nonfatal cases;
11. uploads the normalized NTSB research artifact;
12. commits changed generated state back to `main` through the bounded rebase/retry workflow without force-pushing;
13. packages and deploys the static observatory to GitHub Pages.

`AGGIORNA` does not fabricate missing evidence, reinterpret an FAA SDR as an accident, rewrite F-002, force scientific gates open, or claim predictive validation when the evidence gates remain blocked.

## Public observatory UX / localization
Verified live by AGGIORNA #16:
- Italian is the default public language; Italian and English dictionaries cover the Overview, Validation, Methodology and Provenance pages, including dynamically rendered gate labels.
- Every public page has a responsive mobile navigation button with expanded/collapsed menu, `aria-expanded`, close-on-navigation and Escape handling.
- Overview explains in plain language what BSFM is, what it is not, why forecasts are frozen before outcomes, and the six-step path from official source acquisition to prospective scoring and baseline comparison.
- The safety boundary remains explicit: BSFM is experimental research and does not assess the safety of a specific flight, aircraft, airline, route or person.

## Boeing scope / origin
Implemented after the last verified run and awaiting the next integrated AGGIORNA deployment:
- the Overview explicitly states that BSFM is deliberately focused on Boeing commercial jets;
- the project origin is documented as the author's decision to investigate the questions raised after learning about the Netflix documentary `Freefall: A Reckoning for Boeing`;
- the documentary and official 737 MAX investigations are motivation/context, not predictive evidence;
- the public copy explicitly states that BSFM does not assume Boeing is intrinsically less safe than other manufacturers and that a negative empirical result remains scientifically valid;
- Italian and English versions are both supplied.

## Real acquired-data publication
AGGIORNA #16 generated and deployed `site/data/real-data.json` directly from the official acquisition performed in the same run.

Verified 2026-09-05 snapshot:
- FAA SDR current-year rows: 39,245;
- FAA SDR Boeing rows: 20,799;
- latest observed FAA `DifficultyDate`: 2026-09-04;
- latest Boeing reports are published in descending observation-date order with model, component, JASC/stage/condition codes and truncated discrepancy text;
- current NTSB AVALL normalized snapshot: 31,670 event-aircraft rows, 1,894 Boeing rows, 1,247 commercial-Boeing rows, 996 scheduled-Boeing rows and 50 fatal-Boeing rows;
- NTSB historical public availability remains unverified (`availability_known=0`) and the snapshot is explicitly presented as outcome evidence for its documented scope, not as a global census.

An FAA SDR is a service-difficulty report, not necessarily an accident, a verified causal finding, or a BSFM prediction. These descriptive live-data surfaces do not alter any scientific readiness gate.

## Automatic nonfatal comparables for F-002
Implemented after AGGIORNA #16 and awaiting integrated runtime verification:
- `bsfm/comparables.py` derives a maximum of eight recent nonfatal comparison cases from the normalized NTSB AVALL snapshot acquired by the same AGGIORNA run;
- no comparable case is hard-coded in the website;
- candidates must be Boeing, commercial, nonfatal, match the 737-800/737-NG hypothesis, and also match either approach/landing phase or the gear/structural cluster;
- Boeing customer-code variants such as `737-832`, `737-8H4` and related NG forms are recognized conservatively, while MAX strings are excluded from NG matching;
- cases are ranked by a fixed descriptive similarity score and then recency;
- AGGIORNA writes `site/data/comparable-cases.json`; the public bilingual renderer loads that generated file on every page refresh;
- every public comparison states that nonfatal similarity is descriptive context only: it is not a forecast hit, does not satisfy the fatal F-002 target, does not change the F-002 score, and does not open a scientific gate;
- unit/static tests cover fatal/noncommercial/unrelated exclusion, phase/cluster matching, ranking, generated-file loading and the absence of hard-coded comparison cases.

## Evidence/refinement automation
- `bsfm/evidence_automation.py` maintains a machine-readable G1-G4 evidence inventory with SHA-256 artifact provenance and canonical fail-closed gate mirroring.
- AGGIORNA generates `site/data/evidence-state.json`; acquisition/inventory can never manufacture a PASS.
- NTSB normalization retains explicit `PublicationDate` when present as `available_at`, while approval/change dates remain non-substitutable; the canonical availability/leakage audit still decides admission.
- `bsfm/refinements.py` supports automatic append-only publication of `R-F002-*` records only when structurally valid and `provenance_gate_passed=true`.
- F-002 is never rewritten and public refinements do not alter its original score.
- AGGIORNA generates `site/data/refinements.json`; no refinement is invented when no provenance-gated record exists.

## Evidence policy / scientific boundary
G1 global census, G2 Boeing-family annual exposure, G3 historical PIT availability and G4 OOS calibration/superiority remain scientific evidence gates, not software-completion flags. Missing evidence remains BLOCKED. Current official NTSB downloadable data remain a US civil aviation dataset rather than global truth; FAA SDR records remain predictors only where historical public availability can be demonstrated. No proxy denominator is promoted merely to make G2 computable.

Therefore a successful AGGIORNA means the software, acquisition, audits, generated state and publication pipeline are healthy. It does not mean BSFM has demonstrated predictive validity.

## NTSB transition resilience
The acquisition/scientific layers remain separated because NTSB states that the downloadable aviation dataset will transition to its Enterprise API on 2027-04-05. The current MDB adapter can therefore be replaced without changing gate semantics.

## Current operational state
The implementation is live and runtime-verified through AGGIORNA #16. The Boeing-origin copy and automatic F-002 comparable-case pipeline are a new post-#16 batch and must not be called runtime-verified until the next AGGIORNA succeeds.

Exact next step: run one manual `Actions → AGGIORNA → Run workflow` from current `main`. It must pass pre/post tests and audits, acquire the fresh FAA/NTSB data, generate `site/data/comparable-cases.json` from the acquired NTSB snapshot, commit generated state, and deploy Pages. After that run, verify the public bilingual comparison section and record the new workflow baseline. Do not alter frozen F-002 retrospectively.

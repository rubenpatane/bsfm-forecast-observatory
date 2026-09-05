# BSFM Project State

Updated: 2026-09-05

## Last workflow-verified baseline
- F-002 remains frozen and explicitly experimental/unvalidated.
- Exactly one operational GitHub Actions workflow exists: `AGGIORNA`.
- AGGIORNA #20 (`33972138158`) completed successfully from source commit `cbfefb9a555b5f5d5dc3a917214b3f348dcaa15d`.
- Run #20 started at `2026-09-05T14:32:55Z` and completed successfully at `2026-09-05T14:36:14Z`.
- The run verifies the current acquisition/audit/publication pipeline and the post-#17 public UX changes, including the persistent mobile language control, GitHub-source navigation link and generated-data update timestamp.
- The run refreshed/deployed the observatory from the corrected current `main`; the earlier #19 pre-test failure was superseded by this successful run.
- Successful workflow execution verifies software/acquisition/audit/publication health only; it does not establish predictive validity.

## Automatic schedule
- manual `workflow_dispatch` remains available and always executes a full refresh;
- a lightweight scheduled cadence check runs daily at `13:47 UTC`;
- the heavy AGGIORNA job runs automatically only when at least four full days have elapsed since the persisted scheduled-refresh marker;
- `data/manifests/auto-cadence.json` stores cadence state;
- manual runs do not reset the automatic four-day cadence;
- after each successful scheduled refresh, AGGIORNA advances `last_completed_refresh_at` and commits it with generated auditable state;
- if a scheduled heavy refresh fails before marker update, the marker is not advanced and a later daily check can retry.

This daily-check + persisted-marker design is used instead of `*/4` in the day-of-month cron field because that cron expression does not preserve an exact four-day interval across month boundaries.

## What AGGIORNA does
`AGGIORNA` is the single full refresh, verification and publication pipeline for the observatory. In one controlled heavy run it:
1. checks out the current repository and installs dependencies;
2. executes tests, registry verification and foundation audit before refreshed data;
3. downloads the current official FAA Service Difficulty Reports dataset;
4. refreshes FAA SDR historical manifests from 2010 through the current year;
5. downloads and extracts the current official NTSB AVALL snapshot;
6. normalizes NTSB event-aircraft data conservatively;
7. derives the current nonfatal comparison set for F-002 from that same NTSB snapshot using the fixed machine-readable similarity rule;
8. reruns the test, registry and scientific-audit chain after acquisition;
9. evaluates the fail-closed model lifecycle and final scientific readiness;
10. generates public readiness, G1-G4 evidence inventory, provenance-gated refinements, real acquired-data statistics/recent FAA Boeing reports, and F-002 comparable nonfatal cases;
11. uploads the normalized NTSB research artifact;
12. commits changed generated state back to `main` through bounded rebase/retry without force-pushing;
13. packages and deploys the observatory to GitHub Pages.

`AGGIORNA` does not fabricate missing evidence, reinterpret an FAA SDR as an accident, rewrite F-002, force scientific gates open, or claim predictive validation when evidence gates remain blocked.

## Public observatory UX / localization
- Italian is the default public language; Italian and English cover Overview, Validation, Methodology and Provenance, including dynamically rendered state.
- Every public page has responsive mobile navigation.
- The language switch remains visibly accessible in the mobile header rather than being hidden inside the dropdown navigation.
- Every public page exposes a direct `Codice GitHub / GitHub source` link.
- Every public page displays `Ultimo aggiornamento / Last updated`; the value is derived from generated observatory data rather than browser load time and is rendered in Europe/Rome time.
- Overview explains what BSFM is, why it focuses on Boeing, how the project was motivated by the public Boeing investigations/documentary context, how forecasts are frozen, and how prospective scoring works.
- The safety boundary remains explicit: BSFM is experimental research and does not assess the safety of a specific flight, aircraft, airline, route or person.
- These UX changes are runtime-verified and deployed by AGGIORNA #20.

## Real acquired-data publication
The public real-data surface is generated directly from official acquisition in AGGIORNA. Exact current counts are generated state and may change at each successful refresh.

The verified 2026-09-05 lineage includes FAA SDR and NTSB AVALL acquisition. NTSB historical public availability remains unverified (`availability_known=0`) unless a later evidence artifact proves otherwise, and NTSB outcome data remain scoped evidence rather than a global accident census.

An FAA SDR is a service-difficulty report, not necessarily an accident, a verified causal finding, or a BSFM prediction. These descriptive live-data surfaces do not alter scientific readiness gates.

## Automatic nonfatal comparables for F-002
- `bsfm/comparables.py` derives a maximum of eight recent nonfatal comparison cases from the normalized NTSB AVALL snapshot acquired by the same AGGIORNA run;
- no comparable case is hard-coded in the website;
- candidates must be Boeing, commercial, nonfatal, match the 737-800/737-NG hypothesis, and also match either approach/landing phase or the gear/structural cluster;
- a rolling five-year window anchored to the newest event in the snapshot makes old cases age out automatically;
- cases are ranked by fixed descriptive similarity score and then recency;
- AGGIORNA writes `site/data/comparable-cases.json` and the bilingual renderer loads it;
- nonfatal similarity is descriptive context only: it is not a forecast hit, does not satisfy the fatal F-002 target, does not change F-002 score, and does not open a scientific gate.

## Evidence/refinement automation
- `bsfm/evidence_automation.py` maintains machine-readable G1-G4 evidence inventory with provenance and fail-closed gate mirroring.
- AGGIORNA generates `site/data/evidence-state.json`; acquisition cannot manufacture a PASS.
- `bsfm/refinements.py` publishes append-only `R-F002-*` only when structurally valid and provenance-gated.
- F-002 is never rewritten and refinements do not alter its original score.

## Evidence policy / scientific boundary
G1 global census, G2 Boeing-family annual exposure, G3 historical PIT availability and G4 OOS calibration/superiority remain scientific evidence gates. Missing evidence remains BLOCKED. Current NTSB downloadable data are not global truth; FAA SDR records are predictors only where historical public availability can be demonstrated. No proxy denominator is promoted merely to make G2 computable.

Therefore a successful AGGIORNA means the software, acquisition, audits, generated state and publication pipeline are healthy. It does not mean BSFM has demonstrated predictive validity.

## NTSB transition resilience
The acquisition/scientific layers remain separated because NTSB states that the downloadable aviation dataset will transition to its Enterprise API on 2027-04-05. The current MDB adapter can therefore be replaced without changing gate semantics.

## Current operational state
Runtime-verified through AGGIORNA #20 (`33972138158`) on source commit `cbfefb9a555b5f5d5dc3a917214b3f348dcaa15d`. Current public UX changes are verified/deployed. Automatic four-day cadence remains configured independently of manual refreshes.

## Exact next step
Freeze a prospective evaluation/preregistration protocol before the F-002 modal window. The protocol must define target adjudication, temporal/family/phase/event-class scoring, baseline comparison, treatment of partial matches and multiple dimensions, point-in-time admissibility, proper scoring where probabilities are available, falsification criteria and the rule that F-002 itself is immutable. G4 remains BLOCKED until G1-G3 are satisfied and genuine out-of-sample evidence exists.

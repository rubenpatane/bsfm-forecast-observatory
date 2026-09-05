# BSFM Project State

Updated: 2026-09-05

## Last workflow-verified baseline
- F-002 remains frozen and explicitly experimental/unvalidated.
- Exactly one operational GitHub Actions workflow exists: `AGGIORNA`.
- AGGIORNA #17 (`33969684499`) completed successfully from source commit `473f54048dc289788534bafcfb918f75b5011e26`.
- The run refreshed FAA/NTSB data, regenerated the public comparable-case set, reran tests/audits, committed generated state and deployed GitHub Pages.
- The Boeing-origin copy and automatic F-002 nonfatal-comparable pipeline are therefore runtime-verified and deployed.
- The generated comparable state from #17 contains two current NTSB cases selected by the fixed rule: Alaska Airlines 737-890 (2023-08-21) and Sun Country Airlines 737-8K2 (2022-02-04), both nonfatal and tagged as exact-model/family/gear-structural comparables. These are descriptive context only, not F-002 hits.

## Automatic schedule
Implemented after successful AGGIORNA #17:
- manual `workflow_dispatch` remains available and always executes a full refresh;
- a lightweight scheduled cadence check runs daily at `13:47 UTC`;
- the heavy AGGIORNA job runs automatically only when at least four full days have elapsed since the last completed scheduled refresh;
- `data/manifests/auto-cadence.json` stores the cadence state;
- the successful manual #17 completion time (`2026-09-05T13:45:43Z`) anchors the first automatic interval, so the first due automatic refresh is on or just after `2026-09-09T13:45:43Z` (the daily scheduler checks at 13:47 UTC);
- after each successful scheduled refresh, AGGIORNA updates `last_completed_refresh_at` and commits it with the generated auditable state;
- if a scheduled heavy refresh does not complete, the cadence marker is not advanced, so the next daily cadence check can retry;
- manual runs do not reset the automatic four-day cadence.

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
- Overview explains what BSFM is, why it focuses on Boeing, how the project was motivated by the public Boeing investigations/documentary context, how forecasts are frozen, and how prospective scoring works.
- The safety boundary remains explicit: BSFM is experimental research and does not assess the safety of a specific flight, aircraft, airline, route or person.
- New post-#17 static UI change: every page now injects a direct `Codice GitHub / GitHub source` link in the navigation menu to `https://github.com/rubenpatane/bsfm-forecast-observatory`.
- New post-#17 static UI change: every page displays `Ultimo aggiornamento / Last updated` both in the navigation menu and in a small status strip below the header.
- The displayed timestamp is derived from generated observatory data (`site/data/real-data.json` and `site/data/comparable-cases.json`) and rendered in Europe/Rome time; it is not the browser load time and is therefore tied to the last successful data-generation run.

## Real acquired-data publication
The public real-data surface is generated directly from official acquisition in AGGIORNA.

Verified 2026-09-05 snapshot:
- FAA SDR current-year rows: 39,245;
- FAA SDR Boeing rows: 20,799;
- latest observed FAA `DifficultyDate`: 2026-09-04;
- current NTSB AVALL normalized snapshot: 31,670 event-aircraft rows, 1,894 Boeing rows, 1,247 commercial-Boeing rows, 996 scheduled-Boeing rows and 50 fatal-Boeing rows;
- NTSB historical public availability remains unverified (`availability_known=0`) and the snapshot is outcome evidence for its documented scope, not a global census.

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
Runtime-verified through AGGIORNA #17. Four-day automatic scheduling is configured but has not yet reached its first scheduled due time. The GitHub-source-link and last-update timestamp UI changes are committed after #17 and therefore require the next Pages deployment before they are publicly visible.

Exact next step: no manual action is required for routine refresh. If immediate publication of the new navigation/update-timestamp UI is desired, run one manual `AGGIORNA`; otherwise the next automatic heavy refresh will deploy it when the four-day cadence becomes due. Manual AGGIORNA remains available without shifting the automatic cadence.

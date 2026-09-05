# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository; F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`; it remains manual (`workflow_dispatch`).
- AGGIORNA #9 completed successfully on `5092ea14`; **46 tests passed before and after refresh**. The generated auditable-state commit is `dafd232b14459cbb96695d85ff42a13f5477170a`.
- Live NTSB extraction v2 confirms `NTSB_Admin.csv` has 31,124 rows; normalized NTSB has 31,670 event-aircraft rows, 1,894 Boeing rows and 50 fatal Boeing rows. `availability_known=0`; approval/change timestamps remain outcome/administrative metadata, not demonstrated historical public availability.
- FAA SDR 2010-2026 manifests are valid. 2026 contains 39,245 reports, 20,799 Boeing rows, through DifficultyDate 2026-09-04. SubmissionDate parsing has zero failures, but historical public availability remains unverified because FAA approval/QC occurs after submission.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7. Model lifecycle remains fail-closed until point-in-time availability, leakage-free evaluation, baseline, historical cases and calibration gates pass.
- F-002 and its score remain immutable; prospective refinements are separately versioned.
- Global-census and exposure rules are preregistered at `docs/GLOBAL-CENSUS-AND-EXPOSURE.md`.

## Work added after AGGIORNA #9 — awaiting next execution
- Exposure-only probabilities are now normalized **within each historical period**, not across years. This fixes a methodological error that would otherwise let departures from other years distort a cutoff's null forecast.
- Exposure audit now requires explicit provenance as well as source/scope, rejects zero-total periods, duplicate cells, mixed scopes and incomplete period×cohort grids.
- Annual target-census attestations now require scope, provenance, at least two independent publishers and an explicit `qualifying_boeing_events` count. The attested count must equal the qualifying event rows for that year, including explicit zero-event years.
- Additional regression tests cover period-conditional normalization, missing provenance, zero exposure, annual count mismatch and weak census attestations.

## Scientific evidence
ICAO's 2025 Safety Report reports 95 accidents, 10 fatal accidents, 296 fatalities and over 37 million departures in 2024 for scheduled commercial air transport. EASA ASR 2025 reports 14 worldwide fatal airline accidents under its own scope and publishes fatal-accident detail; Boeing's Statistical Summary provides manufacturer-specific triangulation and departures-based accident statistics. These scope differences must be reconciled explicitly rather than silently merged.

## Scientific gate
No new prospective forecast may be represented as validated until leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Source integrity is ready; historical point-in-time predictor availability, provenance-complete global historical cases and cohort exposure remain incomplete.

## Exact next step
Execute AGGIORNA once on the current head to independently verify the post-#9 census/exposure changes. If green, continue the authoritative 2010-2025 annual target reconciliation and build the consistent cohort-departure exposure table. Do not open `historical_cases`, `baseline_present`, candidate fitting or promotion until their respective audits pass.

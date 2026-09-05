# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository; F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`; it remains manual (`workflow_dispatch`).
- **AGGIORNA #10 completed successfully on `651bf031…`; 51 tests passed before and after refresh.** Registry integrity passed and the generated auditable-state commit is `a568780`.
- Live NTSB normalization remains 31,670 event-aircraft rows, 1,894 Boeing rows and 50 fatal Boeing rows. `availability_known=0`; approval/change timestamps remain outcome/administrative metadata, not demonstrated historical public availability.
- FAA SDR 2010-2026 refresh remains operational, but historical public availability is unverified because FAA approval/QC occurs after submission. SDR predictor eligibility therefore remains blocked.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7. Model lifecycle remains fail-closed until point-in-time availability, leakage-free evaluation, baseline, historical cases and calibration gates pass.
- F-002 and its score remain immutable; prospective refinements are separately versioned.
- Global-census and exposure rules are preregistered at `docs/GLOBAL-CENSUS-AND-EXPOSURE.md`.

## Census/exposure implementation verified by AGGIORNA #10
- Exposure-only probabilities normalize within each historical period.
- Exposure audit requires explicit provenance and source/scope; it rejects zero-total periods, duplicate cells, mixed scopes and incomplete period×cohort grids.
- Annual target-census attestations require scope, provenance, at least two independent publishers and explicit `qualifying_boeing_events`; the attested count must equal qualifying event rows, including zero-event years.
- The real runner passed all 51 tests after these changes.

## Work after AGGIORNA #10
- Added `data/census/` as the fail-closed construction area for the authoritative 2010-2025 target census.
- Seeded `year-ledger.json` with every evaluation year explicitly unresolved. This is intentionally not ground truth and cannot satisfy `historical_cases`.
- Source hierarchy remains ICAO annual Safety Reports + EASA Annual Safety Reviews/fatal-accident appendices, with national investigation authorities for event-level ambiguity and Boeing Statistical Summary only as manufacturer triangulation.
- Confirmed a key historical source: EASA Annual Safety Review 2010 contains an Appendix 4 listing fatal accidents in 2010 for commercial air transport aeroplanes over 2,250 kg MTOM. ICAO's 2012 Safety Report reports 121 scheduled-commercial accidents in 2010 and 29.023 million scheduled-commercial flights for 2010. These demonstrate why scope metadata must be retained rather than merging annual totals.
- Boeing's 2025 Statistical Summary supplies worldwide commercial-jet type-level cumulative hull-loss/fatal-hull-loss statistics and departure-based rates, useful for triangulation and exposure methodology but not sufficient as event-level global ground truth by itself.

## Scientific gate
No new prospective forecast may be represented as validated until leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Source integrity is ready; historical point-in-time predictor availability, provenance-complete global historical cases and cohort exposure remain incomplete.

## Exact next step
Populate the annual ledger case-by-case from 2010 forward, recording exact source scope and event-level provenance. In parallel identify a defensible annual Boeing-family departures source; do not substitute fleet counts or accident counts. Only after all 2010-2025 annual attestations and the complete period×cohort departures grid pass their audits may `historical_cases` or `baseline_present` become true. Keep candidate fitting/promotion disabled.

# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository; F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`; it remains manual (`workflow_dispatch`).
- AGGIORNA #7 completed successfully on `921f6b7f46f228c72d96b0a2953c117dc8115d34`; 35 tests passed and generated state was committed as `a48e97c`. The live normalization produced 31,670 event-aircraft rows, 1,894 Boeing, 50 fatal Boeing, 1,247 conservatively commercial Boeing, 996 scheduled Boeing, 28,414 with outcome approval metadata, 30,956 with sequence evidence and 24,724 with findings evidence; predictor `availability_known` remains correctly zero.
- FAA SDR 2010-2026 manifests are valid. 2026 contains 39,245 reports, 20,799 Boeing rows, through DifficultyDate 2026-09-04. SubmissionDate parsing has zero failures, but historical public availability remains unverified because FAA approval/QC occurs after submission.
- `NTSB_Admin` approval dates are outcome/finalization metadata, not silently substituted for public `available_at`; Findings, Events_Sequence and administrative last-change dates are likewise excluded from predictor availability by implication.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7. Model lifecycle remains fail-closed until point-in-time availability, leakage-free evaluation, baseline, historical cases and calibration gates pass.
- F-002 and its score remain immutable; prospective refinements are separately versioned.
- Prior-art review is recorded at `docs/PRIOR-ART-AND-NOVELTY.md`; no unsupported first/unique claim is permitted.
- Global-census and exposure rules are now preregistered at `docs/GLOBAL-CENSUS-AND-EXPOSURE.md`. `bsfm/target_census.py` requires explicit target fields and at least two independent publisher provenances. `bsfm/exposure.py` implements a departures-proportional null model and rejects invalid/duplicate exposure rows. Tests enforce both rules. Code scaffolding alone does not open the scientific gates.

## Scientific evidence added
ICAO Safety Report 2025 gives 2024 scheduled commercial air transport (>5,700 kg) as 37.09 million departures, 95 accidents and 10 fatal accidents. EASA ASR 2025 reports 14 worldwide fatal accidents in its commercial-large-aeroplane overview and publishes a fatal-accident appendix. The differing counts demonstrate why scope must be harmonised rather than silently merged. Boeing's 2025 Statistical Summary remains useful manufacturer triangulation and reports accident rates on a departures basis.

## Scientific gate
No new prospective forecast may be represented as validated until leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Source integrity is ready; historical point-in-time predictor availability, provenance-complete global historical cases and cohort exposure remain incomplete.

## Exact next step
Populate the 2010-2025 target census case-by-case from authoritative annual sources with scope/provenance reconciliation, then populate cohort departures under a consistent global scope. Only after coverage audits pass may `historical_cases` or `baseline_present` become true. Continue point-in-time source investigation in parallel; keep FAA SDR predictor eligibility blocked absent defensible public availability evidence.

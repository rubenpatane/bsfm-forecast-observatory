# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository; F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`; it remains manual (`workflow_dispatch`).
- AGGIORNA #8 completed successfully on `493c4134be4cd3a87ca03b31b720b294c7e95743`; 40 tests passed. The generated auditable-state commit is `6b752d48fc16c1121bfb7fee26113259d3711b98` and the NTSB artifact digest is `sha256:46b184ec1a9a76fc39e1e0c413170b69024846cf49a700e9c38f7622314e35c9`.
- Live NTSB extraction v2 confirms `NTSB_Admin.csv` has 31,124 rows and fields `ev_id, rec_stat, approval_date, lchg_userid, lchg_date`; `dt_aircraft.csv` has 269,968 rows; `engines.csv` 28,527; `injury.csv` 180,418. `approval_date` is retained as outcome/administrative metadata and is not asserted to be public `available_at`.
- The NTSB public accident-data page identifies AVALL as the official U.S. civil aviation accident census and separately exposes daily/pending publication reporting. The downloadable AVALL is updated monthly; this supports keeping approval/change timestamps distinct from demonstrated historical public availability.
- FAA SDR 2010-2026 manifests are valid. 2026 contains 39,245 reports, 20,799 Boeing rows, through DifficultyDate 2026-09-04. SubmissionDate parsing has zero failures, but historical public availability remains unverified because FAA approval/QC occurs after submission.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7. Model lifecycle remains fail-closed until point-in-time availability, leakage-free evaluation, baseline, historical cases and calibration gates pass.
- F-002 and its score remain immutable; prospective refinements are separately versioned.
- Global-census and exposure rules are preregistered at `docs/GLOBAL-CENSUS-AND-EXPOSURE.md`.

## Work added after AGGIORNA #8 — awaiting next execution
- `bsfm/target_census.py` now fails closed on non-explicit commercial/jet labels and invalid fatalities, and adds an annual census audit. Zero-event years require explicit reconciliation attestations from at least two independent publishers; absence of event rows can no longer masquerade as complete coverage.
- `bsfm/exposure.py` now adds a scientific exposure audit requiring provenance, a single compatible scope and a complete period×cohort grid before baseline completeness can be asserted.
- `bsfm/pipeline.py` closes a gate weakness: point-in-time availability now passes only when every relevant manifest explicitly declares `historical_public_availability=verified`; missing/unknown metadata cannot pass by omission.
- Tests were added for these fail-closed rules. They are committed but not yet independently executed by AGGIORNA.

## Scientific evidence
ICAO reports global scheduled commercial air transport on a departures basis and reported 37.09 million departures, 95 accidents and 10 fatal accidents for 2024 in its 2025 Safety Report. EASA ASR 2025 reports 14 worldwide fatal airline accidents under its own scope and publishes a fatal-accident appendix. Boeing's Statistical Summary provides manufacturer triangulation and departures-based accident statistics. The differing counts require explicit scope reconciliation, not silent merging.

## Scientific gate
No new prospective forecast may be represented as validated until leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Source integrity is ready; historical point-in-time predictor availability, provenance-complete global historical cases and cohort exposure remain incomplete.

## Exact next step
Execute AGGIORNA once on the current head to verify the new census/exposure/gate tests. If green, continue populating the 2010-2025 target census case-by-case from authoritative annual sources, with explicit annual reconciliation including zero-event years, then populate a consistent global cohort-departure table. Only audited completeness may set `historical_cases` or `baseline_present` true.

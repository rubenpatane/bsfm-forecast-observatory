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

## Historical Backtest Foundation batch
Work is accumulated on branch `dev` before one integrated AGGIORNA verification.

Implemented:
- fail-closed machine-readable census event ledger and annual reconciliation ledger;
- fail-closed departures exposure ledger and explicit prohibition on deriving Boeing-family denominators from global traffic totals, fleet counts or accident counts;
- integrated historical-foundation audit combining census, exposure, point-in-time availability and leakage gates;
- walk-forward descriptor generation at T-365/T-90/T-30/T-7 only after census completion;
- calibration/reliability diagnostics with Brier score, while `calibration_evaluated` remains false until real leakage-free probabilistic historical predictions exist;
- CLI `audit-foundation` command for an auditable readiness report;
- regression tests ensuring empty/construction ledgers cannot open scientific gates.

## Source reconciliation evidence
- EASA Annual Safety Review 2012 reports fatal-accident counts for EASA and third-country CAT aeroplanes above 2,250 kg and explicitly bases scheduled-passenger fatal-accident rates on flights carried out.
- ICAO reports global scheduled departures reached about 32 million in 2013 and 33 million in 2014. Those values are stored only as scope/context evidence and are not Boeing-family denominators.
- ICAO's 2013 global safety analysis uses scheduled commercial air transport aircraft above 5,700 kg and reports 90 accidents, 9 fatal accidents and 173 fatalities; EASA historical reports use different scopes. Scope differences are retained rather than silently merged.
- EASA maintains an official Annual Safety Review archive covering the historical interval.

## Scientific gate
No new prospective forecast may be represented as validated until leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Source integrity is ready; historical point-in-time predictor availability, provenance-complete global historical cases and Boeing-cohort exposure remain incomplete. Construction placeholders are never interpreted as zero-event or zero-exposure evidence.

## Exact next step
Continue event-level 2010-2025 reconciliation and search for defensible annual Boeing-family departures. If no authoritative family-level denominator is publicly reconstructable, document that limitation rather than estimate it. Complete all offline code/tests/docs in the batch, then merge to main and request one AGGIORNA run for integrated verification. Candidate fitting/promotion remains disabled until every independent gate passes.

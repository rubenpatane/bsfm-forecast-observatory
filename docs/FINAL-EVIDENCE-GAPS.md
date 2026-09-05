# Final empirical evidence gaps

Updated: 2026-09-05
Status: fail-closed evidence register

This register distinguishes implementation completeness from empirical claims. A green AGGIORNA run can verify software behavior; it cannot manufacture historical evidence that public authoritative sources do not expose.

## G1 — Global target census 2010–2025

**State:** BLOCKED / reconciliation incomplete.

The target is the next fatal accident involving a Boeing commercial jet under the preregistered scope. NTSB is not a global census. EASA/ICAO/Boeing reports provide important triangulation but use differing scopes. Candidate events may be stored before annual reconciliation, but `historical_cases` remains false until every year is explicitly reconciled and attested with provenance.

2024 has three evidence-backed construction candidates (SQ321 B777-300ER, Swiftair B737-400, Jeju Air B737-800). They do not by themselves establish that the global 2024 census is exhaustive.

## G2 — Boeing-family annual departures 2010–2025

**State:** BLOCKED / full denominator matrix not established.

ICAO global scheduled departures are not Boeing-family denominators. Boeing's Statistical Summary publishes cumulative type-level accident counts/rates per million departures, which can support bounded sensitivity reconstruction when archived editions are available, but the public material reviewed does not directly provide the required complete annual family-by-year departures matrix.

Official references reviewed include:
- Boeing 2025 Statistical Summary: https://www.boeing.com/content/dam/boeing/v2/safety/statsum.pdf
- Boeing 2020 Statistical Summary: https://www.boeing.com/content/dam/boeing/boeingdotcom/company/about_bca/pdf/Boeing-Statistical-Summary-2020-Report.pdf
- Boeing safety/CASO pages and archived-report navigation.

No fleet-share allocation, accident-count proxy, delivery-count proxy, or interpolation is admitted as observed exposure. `baseline_present` therefore remains false unless the complete preregistered matrix is defensibly populated.

## G3 — Historical point-in-time predictor availability

**State:** BLOCKED for current FAA SDR/NTSB snapshots.

FAA SDR `DifficultyDate` is occurrence/discovery timing and `SubmissionDate` is not demonstrated public-release timing; FAA states recent reports may be unavailable until approval/QC. Current NTSB AVALL administrative approval/change fields describe outcome/finalization state and do not prove the first date predictor information was publicly available. These datasets therefore cannot be used retrospectively at arbitrary cutoffs without archived/publication evidence.

`point_in_time_availability_verified` remains false and missing availability is never replaced by event date, submission date, approval date, or last-change date.

## G4 — Calibration and candidate superiority

**State:** BLOCKED downstream of G1–G3.

Calibration and candidate-vs-baseline superiority require real leakage-free out-of-sample forecasts. Synthetic/unit-test fixtures validate code only and never set `calibration_evaluated`, `paired_baseline_comparison`, or `candidate_better_than_baseline` in scientific state.

## What is nevertheless implementable and testable

The repository contains the complete fail-closed machinery needed to proceed when evidence becomes available: census/exposure audits, PIT eligibility, next-event walk-forward cases, proper scoring, calibration diagnostics, exposure-only comparison, shrinkage hazard candidate estimator, gated fitting, immutable model records, promotion gate, final readiness audit and one integrated AGGIORNA workflow.

A final green workflow therefore means **software batch verified**, not **predictive validity demonstrated**, unless G1–G4 have independently become PASS from real evidence.

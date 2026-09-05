# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository; F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`; it remains manual (`workflow_dispatch`).
- Run `33960646521` (AGGIORNA #6) completed successfully on commit `50a5fba529be238a21ef0769d2ea9fdf89284d21`; 34 tests passed before and after refresh. Generated state was committed by the observatory bot as `e42ab4f`.
- FAA SDR 2010-2026 manifests are valid. The 2026 snapshot contains 39,245 reports, 20,799 Boeing rows, through DifficultyDate 2026-09-04. SubmissionDate parsing has zero failures, but historical public availability remains unverified because FAA approval/QC occurs after submission.
- NTSB AVALL snapshot SHA-256 is `5cf380f0061817c0331a6b2d8cc7e0ee3a79bea469a1001dc5c10e56f35f5ab3` (96,148,686 bytes). Run #6 artifact `9967844568` has SHA-256 `250f702d1eb0ea723f3637a6ecc7a97e014aa4c138ec5d1b11fda183a51fcd75`.
- NTSB normalization produced 31,670 event-aircraft rows, 1,894 Boeing rows, 50 fatal Boeing rows, 1,247 conservatively classified commercial Boeing rows and 996 scheduled Boeing rows. 30,956 rows have event-sequence evidence and 24,724 have findings evidence.
- Newly extracted `NTSB_Admin` contains 31,124 rows with fields `ev_id`, `rec_stat`, `approval_date`, `lchg_userid`, `lchg_date`. Approval dates never preceded event dates in the current snapshot; they are retained as final-report/outcome approval metadata. They are **not** silently substituted for public `available_at`, because approval/finalization is not by itself proof of the exact public-access instant.
- `dt_events`, `dt_aircraft`, Findings, Events_Sequence and administrative last-change dates are likewise not treated as historical public-availability timestamps.
- Point-in-time tests cover equality at cutoff, timezone normalization, unknown availability and malformed timestamps. NTSB tests explicitly enforce that approval/findings/sequence metadata do not become predictor availability by implication.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7. Backtest primitives implement fixed cutoffs, temporal metrics, probabilistic BSFM-vs-baseline comparison and a fail-closed publication gate.
- The model lifecycle is wired into AGGIORNA and is fail-closed: no candidate fit/promotion occurs until point-in-time availability, leakage-free evaluation, baseline, historical cases and calibration gates all pass.
- F-002 evaluation separates target occurrence from multidimensional forecast match. Prospective refinements are versioned separately and cannot alter the original F-002 score or be backdated.

## Scientific gate
No new prospective forecast may be represented as validated until a leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Source integrity is ready; historical point-in-time predictor availability is not yet verified.

## Global coverage
NTSB is not a global commercial-jet ground truth. Boeing's Statistical Summary provides a worldwide commercial-jet reference and states that departures are the preferred accident-rate denominator. ICAO's global safety reporting covers scheduled commercial operations and EASA publishes annual safety reviews plus fatal-accident appendices. The global target census must be triangulated and retain provenance rather than relying silently on a single manufacturer source.

## Publication readiness
The repository and Observatory may ultimately be published as an **open experimental research protocol/observatory** while clearly reporting NOT YET VALIDATED. They must not be presented as a validated accident-prediction service. A predictive-performance claim requires the historical gate to pass.

## Exact next step
Execute AGGIORNA after commit `7c911060` to verify the NTSB_Admin join and approval-date statistics on the runner. In parallel, build the global fatal-commercial-jet target census from authoritative annual sources (ICAO/EASA, triangulated with Boeing) and the exposure-only reference model using departures as denominator. Keep FAA SDR historical predictor eligibility blocked unless an approval/publication timestamp or defensible archived snapshot establishes public availability at each cutoff.

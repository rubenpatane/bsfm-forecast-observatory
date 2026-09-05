# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository; F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`; it remains manual (`workflow_dispatch`).
- AGGIORNA #7 completed successfully after the NTSB_Admin integration; 35 tests passed and the generated auditable state was committed as `a48e97c`.
- FAA SDR 2010-2026 manifests are valid. The 2026 snapshot contains 39,245 reports, 20,799 Boeing rows, through DifficultyDate 2026-09-04. SubmissionDate parsing has zero failures, but historical public availability remains unverified because FAA approval/QC occurs after submission.
- NTSB normalization produces 31,670 event-aircraft rows, 1,894 Boeing rows, 50 fatal Boeing rows, 1,247 conservatively classified commercial Boeing rows and 996 scheduled Boeing rows. 30,956 rows have event-sequence evidence, 24,724 have findings evidence and 28,414 have outcome approval metadata.
- `NTSB_Admin` fields include `ev_id`, `rec_stat`, `approval_date`, `lchg_userid`, `lchg_date`. Approval dates are retained as final-report/outcome approval metadata. They are **not** silently substituted for public `available_at`, because approval/finalization is not by itself proof of the exact public-access instant. Current normalization therefore correctly retains `availability_known = 0`.
- `dt_events`, `dt_aircraft`, Findings, Events_Sequence and administrative last-change dates are likewise not treated as historical public-availability timestamps.
- Point-in-time tests cover equality at cutoff, timezone normalization, unknown availability and malformed timestamps. NTSB tests explicitly enforce that approval/findings/sequence metadata do not become predictor availability by implication.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7. Backtest primitives implement fixed cutoffs, temporal metrics, probabilistic BSFM-vs-baseline comparison and a fail-closed publication gate.
- The model lifecycle is wired into AGGIORNA and is fail-closed: no candidate fit/promotion occurs until point-in-time availability, leakage-free evaluation, baseline, historical cases and calibration gates all pass.
- F-002 evaluation separates target occurrence from multidimensional forecast match. Prospective refinements are versioned separately and cannot alter the original F-002 score or be backdated.
- A formal working prior-art/novelty review now lives at `docs/PRIOR-ART-AND-NOVELTY.md`. Verified prior art includes EASA Data4Safety and published Bayesian/hierarchical aviation-safety prediction research. BSFM therefore makes no unsupported claim to have invented predictive aviation safety, precursor analysis, Bayesian/hierarchical modelling, exposure-normalized risk, or failure-event forecasting.

## Scientific gate
No new prospective forecast may be represented as validated until a leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Source integrity is ready; historical point-in-time predictor availability is not yet verified.

## Global coverage
NTSB is not a global commercial-jet ground truth. Boeing's Statistical Summary provides a worldwide commercial-jet reference and states that departures are the preferred accident-rate denominator. ICAO's global safety reporting covers scheduled commercial operations and EASA publishes annual safety reviews plus fatal-accident appendices. The global target census must be triangulated and retain provenance rather than relying silently on a single manufacturer source.

## Prior art / contribution framing
Predictive aviation-safety analytics is established prior art. EASA Data4Safety explicitly targets predictive safety intelligence from heterogeneous aviation data, and Safety Science literature has already demonstrated Bayesian/hierarchical prediction of aircraft safety incidents. The candidate BSFM contribution is narrower: an open combination of next-event target definition, multidimensional hazard decomposition, immutable ex-ante forecasts, strict point-in-time admissibility, preregistered walk-forward comparison against exposure-only baseline, prospective scoring including failures, separate refinement lineage, and fail-closed model promotion. This is a candidate contribution, not a proven novelty claim; a broader systematic literature/patent review is required before any `first` or `unique` statement.

## Publication readiness
The repository and Observatory may ultimately be published as an **open experimental research protocol/observatory** while clearly reporting NOT YET VALIDATED. They must not be presented as a validated accident-prediction service. A predictive-performance claim requires the historical gate to pass.

## Exact next step
Build the global fatal-commercial-jet target census from authoritative annual sources (ICAO/EASA, triangulated with Boeing) and the exposure-only reference model using departures as denominator. In parallel, continue the systematic prior-art matrix and point-in-time source investigation. Keep FAA SDR historical predictor eligibility blocked unless an approval/publication timestamp or defensible archived snapshot establishes public availability at each cutoff.

# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository.
- F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`.
- `AGGIORNA` is manual (`workflow_dispatch`); production scheduling is intentionally undecided and is not part of model semantics.
- FAA SDR current-year and 2010-current historical manifest ingestion are implemented with required-schema and date parsing validation.
- NTSB AVALL archive fingerprint ingestion and MDB extraction are implemented.
- NTSB normalization is implemented conservatively: missing carrier/schedule does not imply commercial use and missing publication date remains unavailable rather than being replaced by event date.
- Point-in-time helpers reject rows unavailable at a requested cutoff.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7.
- Backtest primitives implement fixed cutoffs, temporal metrics, probabilistic BSFM-vs-baseline comparison and a fail-closed publication gate.
- Observatory UI is structured as frozen forecast -> post-cutoff evidence -> preregistered comparison -> assessment -> historical validation -> calibration -> provenance -> limitations -> archive/version history.

## Scientific gate
No new prospective forecast may be represented as validated until a leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled.

## Coverage constraint discovered during implementation
A current NTSB AVALL snapshot can expose a latest publication date, but by itself does not reconstruct every historical version of every report field. Consequently, a 2010-2025 feature backtest must exclude fields whose historical availability cannot be demonstrated. NTSB is also U.S.-centric and cannot by itself support a global Boeing accident ground truth.

## Publication readiness
The repository and Observatory may ultimately be published as an **open experimental research protocol/observatory** while clearly reporting NOT YET VALIDATED. They must not be presented as a validated accident-prediction service. A predictive-performance claim requires the historical gate to pass.

## Remaining implementation gate
1. Exercise current `AGGIORNA` end-to-end on GitHub-hosted runner and inspect its artifact/logs.
2. Build an authoritative global target-event census or explicitly narrow the scientific population to the coverage that can be validated.
3. Add defensible exposure denominators for that population.
4. Populate the preregistered walk-forward evaluation and exposure-only comparator.
5. Evaluate calibration and publish all results, including negative/regressive results.
6. Only after those gates, enable Pages and optionally choose a schedule for the same `AGGIORNA` workflow.

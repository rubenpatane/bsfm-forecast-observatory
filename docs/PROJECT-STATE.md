# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository.
- F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`.
- `AGGIORNA` is manual (`workflow_dispatch`); production scheduling is intentionally undecided and is not part of model semantics.
- Run `33959321000` completed successfully on 2026-09-05. All workflow steps passed, 25 tests passed, and the generated auditable source state was committed by the observatory bot as `b2522e4`.
- FAA SDR 2010-2026 manifests were generated from official CSVs. The 2026 snapshot contained 39,245 reports, including 20,799 Boeing rows, through DifficultyDate 2026-09-04.
- NTSB AVALL downloaded successfully (96,148,686 bytes). The derived artifact was uploaded with SHA-256 `aee45d4bdfc49f6e033dbdcaf9826d196d51fe890849008d3f046bad45a351af`.
- The NTSB normalization produced 31,670 event-aircraft rows, 1,894 Boeing rows, 50 fatal Boeing rows, 1,247 conservatively classified commercial Boeing rows and 996 scheduled Boeing rows.
- NTSB `events`/`aircraft` normalization provided zero usable historical public-availability timestamps. The pipeline correctly treats this as a scientific limitation rather than silently calling sources model-ready.
- FAA CSVs contain `SubmissionDate`. The FAA single-submission instructions distinguish Difficulty Date from submission timing, while the public SDR query/FAQ states recently submitted records are unavailable until FAA approval/quality-control review. Therefore `SubmissionDate` is useful for timing diagnostics but is **not** an exact `available_at` timestamp for leakage-sensitive historical reconstruction.
- The first parser accepted only a narrow set of date representations and consequently reported all `SubmissionDate` values as unparseable. The parser now accepts the FAA-documented `yyyy/mm/dd` representation plus explicit US, compact and ISO-like forms. Source-content validity is now separated from point-in-time availability: an otherwise valid FAA export is not labelled invalid merely because historical public approval time is unavailable. The model gate remains fail-closed on `historical_public_availability=unverified`.
- Point-in-time tests cover equality at cutoff, timezone normalization, unknown availability and malformed timestamps.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7. Backtest primitives implement fixed cutoffs, temporal metrics, probabilistic BSFM-vs-baseline comparison and a fail-closed publication gate.
- F-002 evaluation separates target occurrence from multidimensional forecast match and separately scores exact 737-800, 737 NG family, secondary MAX 8, phase, primary failure class, propulsion alternative, modal window/day error and coarse geography support.
- Prospective refinements are versioned separately from frozen F-002. A refinement may narrow a dimension only from information available at its own later cutoff; it cannot alter the original F-002 score or be backdated.
- `docs/DATA-PROVENANCE.md` defines the fail-closed point-in-time and global-ground-truth policy.

## Scientific gate
No new prospective forecast may be represented as validated until a leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Download/schema integrity is explicitly separated from point-in-time model readiness.

## Global coverage
NTSB is not a global commercial-jet ground truth. Boeing's Statistical Summary provides a worldwide commercial-jet reference and states that departures are the preferred accident-rate denominator; ICAO/EASA provide independent authoritative context. Ambiguous target adjudication must retain provenance and must not rely silently on a single manufacturer source.

## Publication readiness
The repository and Observatory may ultimately be published as an **open experimental research protocol/observatory** while clearly reporting NOT YET VALIDATED. They must not be presented as a validated accident-prediction service. A predictive-performance claim requires the historical gate to pass.

## Exact next step
Run `AGGIORNA` once after commit `2b67fca` so the real FAA exports exercise the broadened SubmissionDate parser and regenerate the manifests. Inspect `bad_submission_examples`, parsed date ranges and the NTSB `dt_events`/data dictionary. Even if SubmissionDate parses perfectly, keep historical predictor eligibility blocked unless an FAA approval/publication timestamp or defensible archived snapshot establishes when each record became public. In parallel, continue building the prospective-refinement data path so later information can narrow F-002 dimensions without modifying or rescoring the frozen forecast.

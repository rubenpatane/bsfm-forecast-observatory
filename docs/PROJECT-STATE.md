# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository.
- F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Model update workflow is manual (`workflow_dispatch`); production scheduling is intentionally undecided and external to model semantics.
- FAA SDR current-year and 2010-current historical manifest ingestion are implemented with required-schema and date parsing validation.
- NTSB AVALL archive fingerprint ingestion is implemented.
- NTSB MDB extraction script is implemented for events, aircraft, Occurrences and findings.
- Historical source workflow installs mdbtools, downloads AVALL, exports derived CSVs, tests the repository and uploads derived data as a temporary workflow artifact.
- Point-in-time helpers reject rows unavailable at the requested cutoff; leakage tests exist.
- Observatory UI is structured as forecast -> post-cutoff evidence -> preregistered comparison -> assessment -> historical validation -> calibration -> provenance -> limitations -> archive/version history.

## CI status
The earlier CI failures were traced to unconstrained setuptools flat-layout package discovery. `pyproject.toml` now explicitly limits package discovery to `bsfm*`. The latest CI run must pass before publication readiness can be declared.

## Scientific gate
No new prospective forecast may be generated until the historical estimator is implemented and calibrated against a point-in-time backtest. Absolute accident probabilities remain disabled.

## Known coverage limits
NTSB is authoritative for the U.S. civil aviation accident census, not a complete global Boeing accident ground truth. A global truth set therefore requires additional authoritative sources before global predictive claims can be evaluated.

## Publication gate
Do not enable the public Pages deployment until CI is green, the source build is exercised, historical validation is populated, evidence scoring is automated, and the public page contains no unsupported predictive-performance claim.

## Exact next step
Exercise the corrected CI and historical source workflow. Then normalize exported NTSB tables with publication/availability timestamps, build the Boeing-commercial historical target set, add exposure data, implement the exposure-only baseline and walk-forward backtest, and only then fit/calibrate the estimator.

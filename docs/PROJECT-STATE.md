# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository.
- F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Daily autonomous workflow exists.
- FAA SDR current-year ingestion is implemented.
- NTSB AVALL archive fingerprint ingestion is implemented; MDB extraction is not yet implemented.
- Manual historical workflow can build FAA SDR manifests from 2010 through current year.
- Observatory UI exists under `site/`.

## Scientific gate
No new prospective forecast may be generated until the historical estimator is implemented and calibrated against a point-in-time backtest. Absolute accident probabilities remain disabled.

## Known coverage limits
NTSB is authoritative for the U.S. civil aviation accident census, not a complete global Boeing accident ground truth. A global truth set therefore requires additional authoritative sources before global predictive claims can be evaluated.

## Exact next step
Implement NTSB MDB extraction in GitHub Actions, normalize Boeing commercial occurrences, add availability-time fields, and build leakage tests before fitting any estimator.

# BSFM Project State

Updated: 2026-09-05

## Verified repository state
- Public research repository.
- F-002 remains frozen and explicitly experimental/unvalidated.
- Immutable forecast registry with SHA-256 integrity checks.
- Exactly one operational GitHub Actions workflow is retained: `AGGIORNA`.
- `AGGIORNA` is manual (`workflow_dispatch`); production scheduling is intentionally undecided and is not part of model semantics.
- Run `33959058000` completed successfully on 2026-09-05. All workflow steps passed and the generated source state was committed by the observatory bot as `3ff1797`.
- FAA SDR 2010-2026 manifests were generated from official CSVs. The 2026 snapshot contained 39,245 reports, including 20,799 Boeing rows, through DifficultyDate 2026-09-04.
- NTSB AVALL downloaded successfully (96,148,686 bytes). The derived artifact was uploaded with SHA-256 `faeb3fd00c8f3bdfcbd4228aea2d1170587181616a8c8304e403d737dc8d00ca`.
- The successful NTSB join produced 31,670 event-aircraft rows, 1,894 Boeing rows and 50 fatal Boeing rows. The first implementation reported 1,485 commercial Boeing rows but an audit found that operator-name presence was too permissive; this has been corrected to rely on explicit FAR/schedule fields and requires a new run before those commercial counts are accepted.
- NTSB `events`/`aircraft` exports in that artifact provided zero usable historical public-availability timestamps. The pipeline now treats this as a scientific limitation rather than silently calling sources model-ready.
- FAA CSVs contain `SubmissionDate`; the ingestion now audits it. Because the FAA states recently submitted reports are not publicly searchable until approval, `SubmissionDate` is not treated as an exact public-availability timestamp.
- Point-in-time tests now cover equality at cutoff, timezone normalization, unknown availability and malformed timestamps.
- Backtest protocol is preregistered for 2010-2025 at T-365/T-90/T-30/T-7. Backtest primitives implement fixed cutoffs, temporal metrics, probabilistic BSFM-vs-baseline comparison and a fail-closed publication gate.
- F-002 evaluation now separates target occurrence from multidimensional forecast match and separately scores exact 737-800, 737 NG family, secondary MAX 8, phase, primary failure class, propulsion alternative, modal window/day error and coarse geography support.
- `docs/DATA-PROVENANCE.md` defines the fail-closed point-in-time and global-ground-truth policy.

## Scientific gate
No new prospective forecast may be represented as validated until a leakage-free historical evaluation and calibration are populated. Absolute accident probabilities remain disabled. Download/schema integrity is explicitly separated from point-in-time model readiness.

## Global coverage
NTSB is not a global commercial-jet ground truth. Boeing's Statistical Summary provides a worldwide commercial-jet reference and states that departures are the preferred accident-rate denominator; ICAO/EASA provide independent authoritative context. Ambiguous target adjudication must retain provenance and must not rely silently on a single manufacturer source.

## Publication readiness
The repository and Observatory may ultimately be published as an **open experimental research protocol/observatory** while clearly reporting NOT YET VALIDATED. They must not be presented as a validated accident-prediction service. A predictive-performance claim requires the historical gate to pass.

## Exact next step
Run the updated `AGGIORNA` once to execute the tightened tests, export the additional NTSB provenance tables, regenerate FAA manifests with submission-date audits, and verify that the corrected pipeline reports `historical_point_in_time_availability_unverified` rather than `ready_for_model`. After that run, inspect the new artifact to determine whether `dt_events` or the data dictionary exposes a defensible historical publication field. If not, historical predictor construction must use archived point-in-time material or remain explicitly blocked rather than weakening the leakage rule.

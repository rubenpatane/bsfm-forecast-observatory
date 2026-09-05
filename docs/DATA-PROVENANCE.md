# BSFM Data Provenance and Point-in-Time Policy

Updated: 2026-09-05

## Principle
A field may be used as a predictor at cutoff `t` only when the repository can demonstrate that the information was available to the intended model at or before `t`. Event occurrence time is not a substitute for publication/availability time.

## FAA Service Difficulty Reports
The official annual CSVs contain both `DifficultyDate` and `SubmissionDate`. `DifficultyDate` is the date of the service difficulty, not publication. `SubmissionDate` records submission timing. The FAA public query explicitly warns that recently submitted SDRs are not available until FAA approval. Therefore neither field is currently accepted as an exact historical public-availability timestamp. Historical SDR files can be used for descriptive/source audits, but leakage-sensitive walk-forward predictor construction remains blocked until a defensible availability policy or archived point-in-time snapshots are available.

## NTSB AVALL
The current AVALL snapshot is authoritative for the NTSB records it contains and can be used as a final-state outcome/reference source within its scope. The exported current `events` and `aircraft` tables do not provide a complete historical public-availability timestamp for every row. `lchg_date` is a change timestamp, not proof of first public availability. It must not be substituted for publication time. AVALL is also not a complete global commercial-jet accident census.

## Global target ground truth
F-002 targets the next fatal accident involving a Boeing commercial jet, so a global target requires global coverage. NTSB alone is insufficient. Candidate authoritative/primary reference layers include ICAO/EASA material and the Boeing Statistical Summary of Commercial Jet Airplane Accidents. The Boeing summary explicitly describes worldwide commercial-jet coverage and uses departures as the accident-rate denominator, but a manufacturer publication must not silently become the sole adjudicator of ambiguous events. Target adjudication must preserve source provenance and conflicts.

## Exposure baseline
The exposure-only null must match the population used for target outcomes. U.S.-only BTS exposure cannot be used as if it were global. A narrower U.S. experiment may be reported separately if its population is explicitly defined. Global claims require a defensible global departure/exposure denominator.

## Fail-closed rules
1. Unknown availability => predictor excluded at historical cutoff.
2. Missing operator/schedule => commercial status remains unknown unless another explicit operational field resolves it.
3. Current/final outcome labels may not be reused as historical predictors.
4. No absolute probability is published before calibration evaluation.
5. No predictive-validity claim is made until the preregistered leakage-free backtest and exposure-only comparator are populated.

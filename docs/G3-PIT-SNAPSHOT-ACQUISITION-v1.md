# BSFM G3 PIT Snapshot Acquisition v1

Status: ACTIVE EVIDENCE CONTRACT — FAIL CLOSED
Date: 2026-09-06
Purpose: define what historical evidence is sufficient to establish point-in-time public availability for predictor records/fields.

## Core rule

G3 does not ask whether a value is true today. It asks whether the value used by a simulated historical forecast was publicly available no later than that forecast cutoff.

A current database row containing an old event date is not PIT evidence. A current correction/back-fill is not admissible at an earlier cutoff unless an earlier public artifact proves the value was already present.

## PIT statuses

### `verified`
May be assigned only when a dated public artifact establishes the record/field value no later than the simulated cutoff.

Acceptable evidence classes:
- official public report/release containing the value;
- official versioned dataset snapshot with release/publication date;
- archived copy of an official public dataset/file with trustworthy capture timestamp and preserved bytes;
- versioned public data repository whose historical object and publication time are independently auditable.

### `bounded`
Use when evidence establishes only an interval or source-level release boundary, not the exact record/field availability needed for the cutoff.

Examples:
- a release note proves a field existed by 2024-03-01 but not when a particular historical row received its value;
- AVALL is known to have been publicly distributed by 2012 but the specific record is not preserved in a 2012 snapshot;
- a web archive proves a file endpoint existed but the captured file bytes are unavailable.

`bounded` is excluded from strict backtests.

### `unknown`
Use when no defensible public-availability evidence exists.

`unknown` is excluded from strict backtests.

## Prohibited timestamp substitutions

The following must never be promoted to public `available_at` without separate release evidence:
- accident/occurrence/difficulty date;
- FAA SDR `SubmissionDate`;
- NTSB administrative approval/finalization date;
- database last-change timestamp;
- current retrieval date used as though it were historical publication;
- current presence of the field/value in CAROL, AVALL or an FAA historical CSV.

## Archived dataset snapshot requirements

For a historical dataset snapshot to support `verified`, retain or record as permitted:

- source/publisher;
- original official URL;
- archive/capture URL if applicable;
- capture/release timestamp;
- SHA-256 of the acquired bytes;
- file size;
- schema/field list;
- extraction tool/version;
- exact record/source identifier;
- exact field(s) relied upon;
- evidence that the record and field value are present in that snapshot;
- cutoff(s) for which the snapshot is admissible;
- licensing/redistribution restrictions.

If the raw snapshot cannot be redistributed, store only lawful provenance, hash, extraction instructions and permitted derived evidence.

## NTSB AVALL / CAROL strategy

Known source-level anchors are useful but insufficient alone:
- historical AVALL public distribution predates CAROL and has an evidenced anchor by 2012;
- CAROL public launch and later aviation-search expansions provide dated system-level bounds;
- MDB release notes document later field/schema changes and back-fills.

Priority acquisition:
1. archived `avall.zip` or MDB files around historical forecast cutoffs;
2. archived weekly/monthly NTSB update packages where complete state can be reconstructed;
3. official investigation/report publication artifacts for predictor fields where dataset snapshots are unavailable.

A later release note that says a field was back-filled is positive evidence **against** using the current value at earlier cutoffs unless an earlier snapshot proves otherwise.

## FAA SDR strategy

Current annual SDR CSVs contain historical rows but are not PIT snapshots. Some annual files include `SubmissionDate` values years after the `DifficultyDate` year; this directly demonstrates that occurrence/file year is not public availability.

Priority acquisition:
1. archived official annual CSV snapshots captured near the relevant historical dates;
2. archived FAA public-query/export pages with downloadable result bytes and capture timestamps;
3. official dated releases/publications containing the predictor field/value.

`SubmissionDate` may help diagnose lag, but must not be used as public release time unless FAA evidence establishes that semantic for the relevant period.

## Coverage measurement

G3 should be measured at the predictor observation level, not merely source/year level.

For every candidate historical forecast cutoff, report:
- total predictor observations considered;
- `verified` count;
- `bounded` count;
- `unknown` count;
- strict admissible count (`verified` and `available_at <= cutoff` only);
- excluded fraction by reason/source/field;
- earliest/latest admissible release dates;
- fields with known back-fill/revision risk.

A smaller leakage-free backtest is preferable to a larger reconstructed sample with uncertain availability.

## G3 acceptance gate

G3 can PASS for a defined backtest universe only when:
1. every admitted predictor observation is `verified` under this contract;
2. every admitted `available_at` is no later than its simulated cutoff;
3. source-specific field semantics are documented;
4. known revisions/back-fills cannot leak later information into earlier folds;
5. the admitted set can be reproduced from the recorded evidence/provenance;
6. automated tests reject prohibited timestamp substitutions and future/unverified rows.

G3 does not need every modern field to be historically available. It may PASS for a narrower predictor universe if that universe is fully PIT-verifiable and is fixed before model-skill interpretation.

Until then:

`G3 = BLOCKED`.

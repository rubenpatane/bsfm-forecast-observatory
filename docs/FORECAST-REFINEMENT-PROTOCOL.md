# Forecast Refinement Protocol

Status: preregistered reporting rule
Date: 2026-09-05

## Purpose
BSFM may discover additional resolution after a forecast has been frozen. Additional detail must be visible without rewriting history or making the original forecast appear more specific than it was.

## Two-track rule
1. **Frozen core forecast** — the original forecast record (for example F-002) is immutable and is scored only on dimensions explicitly present at its original cutoff.
2. **Prospective refinement track** — any later narrowing is a new, timestamped, append-only record linked to the parent forecast. It never changes the parent and never receives retrospective credit as part of the parent.

A refinement is therefore not an edit. It is a new prospective prediction conditional on information demonstrably available at its own `issued_at` cutoff.

## Permitted refinement dimensions
Subject to data support, a refinement may add or narrow: aircraft family/model/variant; phase of flight; failure/event class; temporal distribution/window/modal date; broad geography; operator cohort; engine/configuration cohort; or airframe/MSN cohort. Individual aircraft/operator claims are prohibited unless the estimator, exposure denominator, sample size and uncertainty support that resolution. Missing fields remain unknown.

## Required fields
Every refinement must record:
- `refinement_id` and `parent_forecast_id`;
- `issued_at` and model/code version;
- immutable input snapshot hashes and source provenance;
- dimensions changed, old value and new value;
- whether each dimension was present in the parent;
- method used to derive the refinement;
- uncertainty/resolution state;
- scientific status (`exploratory`, `prospective_unvalidated`, or later `validated` only after the validation gate);
- explicit statement that the refinement does not alter parent scoring.

## Scoring
Parent and refinement are evaluated separately. A refinement can earn prospective evidence only for events after its own `issued_at`. It cannot improve F-002's original score. Negative refinements and reversals remain in the append-only history.

## Display rule
The Observatory displays the frozen forecast first. Beneath it, a visually distinct **Prospective refinements** panel shows a chronological refinement ladder:

`F-002 frozen -> R-F002-001 -> R-F002-002 -> ...`

For every refinement the page shows `issued_at`, added/narrowed dimensions, uncertainty, source snapshot, model version and status. A permanent notice states: **Later refinement — not part of the original F-002 forecast and not counted in its original score.**

## Scientific rationale
This separation follows the general transparency principle that model specification, evaluation and updating must be reported explicitly rather than silently changing the evaluated prediction. It also prevents hindsight leakage: information observed after the parent cutoff can create a new prospective forecast, but cannot be imported into the frozen parent.

## Publication gate
A refinement may be displayed before full BSFM validation only as `prospective_unvalidated` or `exploratory`. Absolute probabilities remain hidden until calibration is supportable. Refinement generation must fail closed when source availability/provenance cannot be demonstrated.

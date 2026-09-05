# Global target census and exposure baseline

Status: preregistered construction rule, 2026-09-05.

## Target census
The historical outcome is the next fatal accident involving a Boeing commercial jet after each cutoff. A row is eligible only when event date, manufacturer/model, commercial-operation status, jet status and attributable fatalities are explicit. Unknown commercial status is not coerced to true.

A target row must carry at least two independent publisher provenances before it is admitted to the scored global census. Manufacturer material may triangulate a case but must not silently be the sole ground truth. Current intended authoritative layers are ICAO global scheduled-commercial safety reporting, EASA Annual Safety Review fatal-accident appendices, national investigation authorities where needed, and Boeing Statistical Summary as manufacturer triangulation.

Scope differences are preserved rather than reconciled by guesswork: ICAO 2025 reports 10 fatal accidents in 2024 for scheduled commercial air transport over 5,700 kg, whereas EASA ASR 2025 reports 14 worldwide fatal accidents under its commercial-large-aeroplane overview. These are not treated as contradictory counts until scope definitions are harmonised.

## Exposure-only baseline
The primary null/reference model allocates next-event probability in proportion to departures within the exact eligible cohort and period. Raw SDR counts, fleet counts and accident counts are not denominators. Flight hours/cycles may be retained as sensitivity analyses, but departures remain primary because accident-rate reporting by ICAO and Boeing is departure-based and Boeing reports departures as the stronger accident-rate exposure basis.

A baseline dataset must identify period, cohort, departures, source, retrieval/publication provenance and coverage scope. Duplicate period/cohort rows, negative values, mixed incompatible scopes and missing denominators fail closed.

## Leakage and publication
Outcome details may be finalised after the event; they are used only to label outcomes. Predictor features must independently satisfy point-in-time availability at the historical cutoff. No outcome approval/findings timestamp is allowed to leak into predictor eligibility.

## Gate
`baseline_present` can become true only after a complete exposure table covers every evaluated cohort/cutoff under a consistent scope. `historical_cases` can become true only after the global census is provenance-complete for the evaluation interval. Neither flag is inferred from the existence of code scaffolding.

# BSFM G1–G3 Evidence Acquisition Plan v1

Status: ACTIVE RESEARCH PLAN — FAIL CLOSED
Date: 2026-09-05
Scope: scientific evidence required before G4 candidate-vs-baseline validation can be promoted.

## Purpose

This plan separates three evidence problems that must not be collapsed into one dataset:

- **G1 — global qualifying-event census**: establish the historical outcome set for the BSFM target.
- **G2 — Boeing family/year exposure**: establish denominators needed for an exposure-aware baseline.
- **G3 — point-in-time (PIT) availability**: establish what predictor information was publicly available at each historical forecast cutoff.

No source is promoted merely because it is convenient or currently downloadable. Missing evidence remains missing. A successful acquisition pipeline does not imply a scientific PASS.

## G1 — Global qualifying-event census

### Required object
A deduplicated, auditable event-level census for 2010–2025 of qualifying fatal accidents involving Boeing commercial jets, with at minimum:

- stable internal event id;
- occurrence date/time where available;
- aircraft manufacturer/model/family;
- registration where available;
- operator and operation type;
- location/state of occurrence;
- fatalities and fatal/nonfatal target classification;
- accident/incident classification;
- source authority and source record identifier;
- source retrieval/publication metadata;
- inclusion/exclusion decision plus machine-readable reason;
- links between duplicate records from different authorities.

### Source hierarchy
1. **ICAO ADREP / official ICAO accident data** — preferred global authority. ICAO Annex 13 reporting feeds ADREP; ICAO reports that commercial-air-transport accident/incident data for aircraft above 5,700 kg are reviewed/validated through its occurrence-validation process. ICAO also exposes an `Official Accidents` API endpoint, but access/coverage/field semantics must be verified before use.
2. **National/Regional investigation authorities** — authoritative event-level confirmation and adjudication where accessible (for example NTSB for US events, EASA/member-state safety-investigation material for Europe).
3. **Boeing Statistical Summary of Commercial Jet Airplane Accidents** — strong worldwide cross-check and reconciliation source; it must not silently define BSFM target semantics unless its inclusion rules are proven compatible.
4. Non-official aggregators may be used only for candidate discovery/reconciliation, never as the sole evidence for G1 PASS.

### Acceptance gate
G1 may PASS only if all years 2010–2025 are covered by a documented global or reconciled-global process, target inclusion semantics are fixed, duplicates are resolved, exclusions are auditable, and an independent coverage reconciliation finds no unexplained qualifying gaps.

NTSB alone cannot satisfy G1 because its scope is not a global census.

## G2 — Boeing family/year exposure

### Required object
For each calendar year 2010–2025 and each model/family used by the forecasting system, obtain an exposure denominator with documented semantics. Preferred hierarchy:

1. departures/cycles;
2. flight hours;
3. another directly measured operational exposure only if its relationship to the target hazard is justified in advance.

Required fields include family, year, exposure value, unit, geographic/operational scope, source, extraction method, coverage caveats and uncertainty/revision metadata where available.

### Evidence candidates
- Boeing worldwide statistical summaries are a primary candidate because they publish worldwide commercial-jet accident statistics and departure-based rates/context. Family-level denominator tables must be inspected rather than inferred from aggregate rates.
- ICAO traffic/operator statistics are candidate official denominator sources where access and family granularity permit.
- EASA traffic figures are useful regional reconciliation evidence, not a substitute for global Boeing-family denominators.

### Prohibited shortcuts
Do not infer departures from fleet share, deliveries, aircraft counts, seat capacity, utilization assumptions, interpolated market share or other proxies merely to make the baseline computable. A proxy may be explored in a separately labelled sensitivity analysis but cannot open G2.

### Acceptance gate
G2 may PASS only when the chosen denominator is available with compatible semantics for the required family/year cells, missingness and revisions are explicit, and the baseline can be reproduced from source evidence without hidden imputation.

## G3 — Historical point-in-time availability

### Required object
For every predictor observation admitted to a historical backtest, preserve evidence that the information was publicly available no later than the simulated cutoff.

Minimum fields:

- predictor/source record id;
- event/discovery date where applicable;
- source publication/release timestamp or bounded availability interval;
- retrieval timestamp;
- archived URL/snapshot or immutable official release artifact where available;
- fields known to be present at that release;
- PIT status: `verified`, `bounded`, or `unknown`;
- admissibility decision and reason.

### Conservative rules
- occurrence/discovery date is not publication date;
- submission/approval/change timestamps are not automatically public-release timestamps;
- a field being present in today's database does not prove it existed at an earlier cutoff;
- `unknown` is excluded from strict PIT backtests;
- later corrections/revisions must not leak into earlier simulated cutoffs unless version history proves their earlier availability.

### Evidence strategy
Prefer dated official releases, archived official files, release manifests, web publication dates, versioned datasets and trustworthy web archives. Build source-specific PIT adapters rather than applying one generic timestamp interpretation to all sources.

### Acceptance gate
G3 may PASS only for a backtest universe in which every admitted predictor is supported by PIT evidence under the fixed policy. Coverage may be narrower than the modern dataset; scientific validity takes priority over sample size.

## Cross-gate reconciliation

G1 outcome evidence and G3 predictor availability are different concepts. An accident can be valid outcome evidence even if its investigation fields were published much later. Conversely, a predictor can be PIT-valid without proving the global outcome census.

G2 exposure is likewise independent: accident counts must never be treated as exposure.

## Execution order

1. Build G1 candidate census schema and official-source adapters.
2. Reconcile G1 against at least one independent worldwide summary and authoritative national/regional records for discrepancies.
3. Inventory G2 source tables at family/year granularity before implementing any denominator transformation.
4. Build G3 source-specific publication-history manifests and strict admissibility tests.
5. Freeze resulting evidence artifacts with hashes/provenance.
6. Re-run the scientific gate audit.
7. Only if G1, G2 and G3 PASS, construct G4 rolling-origin/walk-forward candidate-vs-exposure-baseline evaluation.

## Current conclusion

As of this plan's creation, **G1 = BLOCKED, G2 = BLOCKED, G3 = BLOCKED**. The research performed to identify authoritative candidate sources does not itself change those statuses.

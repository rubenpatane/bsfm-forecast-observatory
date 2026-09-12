# BSFM G1–G3 Evidence Acquisition Plan v1

Status: ACTIVE RESEARCH PLAN — FAIL CLOSED
Date: 2026-09-07
Scope: scientific evidence required before G4 candidate-vs-baseline validation can be promoted.

## Purpose

This plan separates three evidence problems that must not be collapsed into one dataset:

- **G1 — global qualifying-event census**: establish the historical outcome set for the BSFM target.
- **G2 — Boeing family/year exposure**: establish denominators needed for an exposure-aware baseline.
- **G3 — point-in-time (PIT) availability**: establish what predictor information was publicly available at each historical forecast cutoff.

No source is promoted merely because it is convenient or currently downloadable. Missing evidence remains missing. A successful acquisition pipeline does not imply a scientific PASS.

## Permanent ICAO retrieval freeze

Effective 2026-09-05, **no new ICAO API retrieval is permitted in routine or research automation**. The previous trial/API access is exhausted/expired and paid ICAO API calls are not an operational dependency of this project. The already acquired AGGIORNA #21 snapshot (4,669 returned rows across the requested 2010–2025 annual queries, with observed rows through 2022) remains historical evidence/provenance subject to its licence and known coverage limitations. It must not be interpreted as a complete 2010–2025 census, and zero returned rows for 2023–2025 are not evidence of zero accidents.

The acquisition script is historical/reproducibility code only. It must not be invoked by `AGGIORNA`, scheduled automation, tests, or normal development. G1/G2/G3 must be completable without any future ICAO API call.

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

### Sustainable source hierarchy
1. **Boeing Statistical Summary of Commercial Jet Airplane Accidents** — worldwide commercial-jet accident summary and principal sustainable global reconciliation source. Its inclusion rules must be checked against the BSFM target; Boeing data must not silently redefine target semantics.
2. **EASA Annual Safety Review and fatal-accident appendices** — independent regional/global safety-review evidence. EASA states its occurrence database includes accidents and serious incidents notified by Safety Investigation Authorities worldwide and is augmented by other sources. Use event lists and annual global summaries where scope matches.
3. **National/regional safety investigation authorities** — authoritative event-level confirmation/adjudication, including NTSB for US events and relevant authorities for non-US events.
4. **Frozen ICAO snapshot from AGGIORNA #21** — historical cross-check only; no further retrieval and no assumption of 2023–2025 coverage.
5. Non-official aggregators may be used only for candidate discovery/reconciliation, never as sole evidence for G1 PASS.

### Acceptance gate
Strict G1 PASS requires all years 2010–2025 to be covered by a documented reconciled-global process, fixed target semantics, duplicate resolution, auditable exclusions and no unexplained qualifying gaps.

Historical G1 v1 may instead be accepted as `CLOSED_WITH_LIMITATION` when an independently documented structural ambiguity in the frozen target makes specific annual cells non-identifiable, all other annual cells satisfy the reconciliation controls, event/census consistency is clean, and a versioned censoring contract prevents the unresolved cells from being converted to binary labels or traversed by scored historical intervals. The adopted contract is `data/census/g1-closure-v1.json`: 14/16 annual cells are identifiable; 2014 and 2020 are non-identifiable because the frozen v1 target did not preregister missing-aircraft and hostile/unlawful-action boundaries. MH370, MH17 and PS752 remain unresolved under frozen historical v1. This is not a retrospective include/exclude decision and is not strict 16/16 completeness.

Neither NTSB alone nor the frozen ICAO snapshot alone can satisfy G1.

## G2 — Boeing family/year exposure

### Required object
For each calendar year 2010–2025 and each model/family used by the forecasting system, obtain an exposure denominator with documented semantics. Preferred hierarchy:

1. departures/cycles;
2. flight hours;
3. another directly measured operational exposure only if its relationship to the target hazard is justified in advance.

Required fields include family, year, exposure value, unit, geographic/operational scope, source, extraction method, coverage caveats and uncertainty/revision metadata where available.

### Evidence candidates
- Boeing worldwide statistical summaries are the primary sustainable candidate because they publish worldwide commercial-jet accident statistics and departure-based rates/context. Family-level denominator tables must be inspected rather than inferred from aggregate rates.
- EASA traffic figures are useful regional reconciliation evidence, not a substitute for global Boeing-family denominators.
- National/regional official traffic statistics may be used for reconciliation when their scope and aircraft-family granularity are explicit.
- ICAO API traffic statistics are **not** an available project dependency and must not be newly retrieved.

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
Prefer dated official releases, archived official files, release manifests, web publication dates, versioned datasets and trustworthy web archives. Build source-specific PIT adapters rather than applying one generic timestamp interpretation to all sources. No future ICAO API access is assumed.

### Acceptance gate
G3 may PASS only for a backtest universe in which every admitted predictor is supported by PIT evidence under the fixed policy. Coverage may be narrower than the modern dataset; scientific validity takes priority over sample size.

## Cross-gate reconciliation

G1 outcome evidence and G3 predictor availability are different concepts. An accident can be valid outcome evidence even if its investigation fields were published much later. Conversely, a predictor can be PIT-valid without proving the global outcome census.

G2 exposure is likewise independent: accident counts must never be treated as exposure.

## Execution order

1. Maintain the 2010–2025 G1 candidate census and closure contract without retroactive target redefinition.
2. Enforce censoring of the declared non-identifiable G1 cells in every historical evaluation path.
3. Inventory and acquire G2 source tables at family/year granularity without proxy splitting.
4. Build G3 source-specific publication-history manifests and strict admissibility tests.
5. Freeze resulting evidence artifacts with hashes/provenance.
6. Re-run the scientific gate audit.
7. Only when G1 is strict PASS or valid `CLOSED_WITH_LIMITATION` with censoring enforced, and G2 and G3 PASS, construct G4 rolling-origin/walk-forward candidate-vs-exposure-baseline evaluation.

## Current conclusion

**G1 = CLOSED_WITH_LIMITATION; G2 = BLOCKED; G3 = BLOCKED.** Historical G1 v1 has 14/16 identifiable annual cells; 2014 and 2020 remain non-identifiable under frozen target semantics and are censored rather than imputed. ICAO API access is no longer an operational dependency. This G1 closure removes an active research blocker but does not open G2, G3 or G4.

# BSFM G2 Data Access Requirements v1

Status: ACTIVE ACCESS CONTRACT — FAIL CLOSED
Date: 2026-09-06
Purpose: define the minimum evidence/data contract for a source to be considered capable of unblocking G2.

## Required scientific object

G2 requires directly measured operational exposure for the BSFM target cohorts over calendar years 2010–2025, with compatible global commercial-jet scope and reproducible provenance.

Current target cohort universe:
- 727
- 737-Original
- 737-Classic
- 737-NG
- 737-MAX
- 747
- 757
- 767
- 777
- 787

Preferred unit hierarchy:
1. departures/cycles;
2. flight hours;
3. another directly measured operational exposure only if prospectively justified before use.

## Minimum row-level/data fields

A candidate dataset must make it possible to derive, without convenience allocation:

- operation/flight date or year;
- aircraft manufacturer;
- aircraft type/model/equipment code at enough resolution to map to the BSFM cohorts;
- one directly measured exposure observation (for example one performed departure/flight) or a documented aggregate count;
- geographic/operational scope;
- commercial/scheduled/charter/cargo semantics sufficient to reconcile with the target universe;
- source release/vintage or historical-schedule version;
- stable source identifier or reproducible extraction key.

Helpful but not mandatory if type mapping is otherwise authoritative:
- registration/tail number;
- operator;
- origin/destination;
- actual versus scheduled indicator.

## Historical-vintage requirement

The source must distinguish at least one of:
- the value as published/available at the historical cutoff;
- a versioned snapshot with release date;
- an explicit revision history that allows the selected vintage to be reproduced.

A current database query that silently returns revised historical traffic is not enough for leakage-sensitive baseline work unless the project prospectively adopts and documents a fixed reconstruction-vintage policy appropriate to the validation design.

## 737 resolution requirement

An all-variant `Boeing 737` total is insufficient for the current canonical G2 because the model distinguishes:
- 737-Original;
- 737-Classic;
- 737-NG;
- 737-MAX.

Acceptable evidence must either:
1. directly identify variants/models that map to those cohorts; or
2. provide another externally validated deterministic mapping that does not estimate shares from fleet counts, deliveries, accident counts, market share or similar proxies.

If the only available source is all-737 aggregate, it may be used for reconciliation/context, not to populate four canonical exposure cells.

## Scope requirement

The canonical denominator is global. Regional datasets such as U.S. T-100 or EUROCONTROL can be used to:
- verify transformations;
- compare trends;
- detect implausible source values;
- run explicitly regional sensitivity analyses.

They cannot be silently scaled to global exposure.

## Licensing / operational requirement

Before data is acquired, the access terms must permit the intended research use. The public repository does not require redistribution of proprietary raw rows: if redistribution is restricted, BSFM may retain only lawful derived aggregates, extraction code/configuration, source metadata, hashes and reproducibility instructions as permitted by the licence.

Credentials/tokens must never be committed to the public repository.

## OAG candidate assessment

OAG Historical Flight Data is currently the strongest identified technical candidate because published product documentation indicates:
- global historical coverage extending before 2010;
- aircraft/equipment fields;
- scheduled and/or operated-flight records depending on product access;
- historical schedule versions / ability to inspect schedules as published at earlier dates.

It is **not** currently a G2 baseline because:
- no licensed project access is connected;
- exact purchased fields/coverage have not been inspected;
- cohort mapping completeness has not been tested;
- extraction reproducibility and licence constraints have not been audited.

## IATA WATS candidate assessment

IATA WATS Global exposes long-run aircraft/model utilization information, but is proprietary and the public releases inspected do not establish a complete 2010–2025 BSFM cohort matrix. Historical values can be revision-sensitive. It remains a candidate source, not a baseline.

## Acceptance test before G2 PASS

A source can contribute to G2 PASS only after the repository can demonstrate:

1. every required year/cohort cell is either populated by compatible measured exposure or covered by a separately preregistered exclusion/design rule;
2. no aggregate-to-cohort proxy split is used;
3. source scope is compatible with the target census;
4. units and transformations are deterministic and tested;
5. vintage/revision policy is explicit;
6. provenance and licensing are recorded;
7. `audit_exposure` and target-universe/exposure audit pass without hidden imputation;
8. the baseline can be reproduced by an authorized researcher from the documented source/extraction contract.

Until all criteria are satisfied:

`G2 = BLOCKED` and `baseline_present = false`.

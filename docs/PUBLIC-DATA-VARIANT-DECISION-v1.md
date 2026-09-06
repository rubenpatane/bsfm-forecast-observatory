# Public-data model variant decision v1

Status: ADOPTED FOR PROSPECTIVE CONSTRUCTION — EVIDENCE GATES BLOCKED

Date: 2026-09-06

## Decision

Following a final official/public-source review, no compatible free global
2010-2025 aircraft-type performed-flight denominator was found. BSFM therefore
adopts `config/model-public-data-v1.3.json` for prospective construction using
official BTS T-100 performed departures. This is a new scientific object, not a
repair or silent reinterpretation of BSFM 1.2.

## Fixed boundaries

- F-002 and its evaluation remain unchanged.
- The global BSFM 1.2 G2 gate remains BLOCKED.
- Historical G1 v1 remains 14/16 BLOCKED.
- Prospective Target Taxonomy v2 remains prospective only.
- T-100 is labelled `us_linked_commercial`: it includes U.S. domestic traffic
  and international traffic represented in T-100, but excludes foreign-to-
  foreign operations.
- A regional T-100 matrix can never be submitted as a global G2 PASS.
- DOT aircraft types must be mapped through a reviewed allowlist. Ambiguous or
  generic types remain unmapped; no fleet-share or other proxy split is allowed.
- Service classes and treatment of scheduled/non-scheduled passenger/cargo
  operations must be frozen before any outcomes are evaluated.
- Raw downloads require query/release provenance and SHA-256. Credentials are
  neither required by T-100 nor permitted in the repository.

## What is implemented now

`bsfm.bts_t100` accepts the official aggregated table shape, totals only
`DEPARTURES_PERFORMED`, audits unmapped types and service classes, and emits a
regional acceptance report that hard-codes global G2 as BLOCKED. It reads an
official CSV or single-CSV ZIP directly and records the exact archive SHA-256,
filename, member name and byte size in the result.

`scripts/download_bts_t100.py` performs year-scoped WebForm downloads directly
from TranStats, requests only the five required fields, refuses non-ZIP
responses, and writes a UTC retrieval/query/SHA-256 manifest beside every raw
archive. It needs no account or secret. It is not wired into AGGIORNA while the
BSFM-PD 1.3 evidence gates remain closed; automation cannot publish a forecast
until its separate outcome/PIT/backtest inputs pass.

## Remaining evidence gates

1. Build and reconcile a qualifying outcome census using the identical
   U.S.-linked segment rule.
2. Establish PIT admissibility for every lagged outcome and exposure vintage
   used at each historical cutoff.
3. Generate historical future-exposure paths without using information after
   each simulated cutoff.
4. Run the frozen paired rolling-origin candidate/baseline backtest.
5. Publish all folds and retain BLOCKED/negative/inconclusive results.

Until all five gates pass, BSFM-PD 1.3 is preregistered construction work and no
new forecast or predictive-validity claim is authorized.

## 2010-2025 acquisition result

All 16 year-scoped archives were downloaded successfully from the official
WebForm and recorded in `data/exposure/bts-t100-2010-2025-audit.json`. The fixed
mapping attributes 56,637,727 performed departures. Mixed code `615` contributes
14 departures across the entire interval; they remain unallocated in the
original cohort design. Structurally absent pre-entry MAX/787 cells are retained
as explicit zeros.

The audit also emits—but does not adopt—a lossless alternative that replaces
`737-Classic` and `737-NG` with the single cohort `737-Classic+NG`. This includes
all 14 ambiguous departures without a proxy split and produces a complete
144-cell regional matrix under nine cohorts. Adopting it is a model
change and therefore requires the new prospective version before backtesting.

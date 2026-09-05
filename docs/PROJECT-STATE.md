# BSFM Project State

Updated: 2026-09-06

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #25 (`33978802087`) completed successfully on source SHA `971cdd6a1ec0576208191e2d18fe76fce2742c86`; it remains the latest full operational/workflow-verified baseline.
- The generated-state commit on `main` is `ce33ea54b36613cf122e3201c2825a329700f656` and uses privacy-safe Git metadata.
- No new ICAO API retrieval is permitted. Frozen historical ICAO evidence is cross-check material only.
- Workflow/software success verifies only executed checks; it does not establish predictive validity or open a scientific gate.

## F-002
`forecasts/F-002.json` is frozen. Its target string is `next_fatal_accident_involving_boeing_commercial_jet`; the forecast object contains no explicit hostile/unlawful-action or missing-aircraft inclusion/exclusion clause. Later research must not silently add one.

F-002 is byte-identical to `main` on the active research branch (blob `eb55a77210d2fd254483ff74c3d02fcd60c1f0ad`) and is not part of PR #2's diff.

## Current research branch and verification
Draft PR #2, branch `research/privacy-safe-rebuild-20260905`, is the privacy-safe reconstruction of post-#25 research. It was created from current `main`; it does not import the commit history of closed PR #1. New Git metadata uses GitHub privacy-safe noreply identity.

A temporary read-only branch Research CI was used only to verify the research head and was then removed, restoring the repository's single-workflow invariant. Successful run `33996825005` executed:
- full `pytest -q`: **157 passed**;
- `python -m bsfm.cli verify`: forecast registry integrity OK;
- `python -m bsfm.cli audit-foundation`: completed successfully;
- `python -m bsfm.cli audit-final`: completed successfully.

The final audit correctly kept scientific readiness false. The temporary CI did not ingest sources, deploy Pages, write generated state or push to `main`; it is no longer in the PR diff. This is a software/audit verification checkpoint, not AGGIORNA and not scientific validation.

## G1 — BLOCKED, 14/16 annual cells reconciled
`data/census/year-ledger.json` is the canonical 2010-2025 annual ledger. A cell passes only if all six controls are true: annual source scope demonstrated; all fatal jets mapped; Boeing target membership mapped; competent authority per candidate; independent reconciliation; target taxonomies resolved.

Reconciled 6/6 cells: 2010, 2011, 2012, 2013, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024 and 2025.

The integrated G1 census now reconciles annual evidence with event-level candidate surfaces. The verified foundation audit reports 38 candidate rows, 35 included qualifying rows, no missing candidate IDs, no extra candidate IDs, no duplicate candidate IDs and no ledger/evidence consistency errors. Event-level gaps previously found in the annual reconstruction were synchronized, including 2010, 2011, Aerosucre 157 in 2016 and 2025.

The reconstruction explicitly preserves external/ground/other-aircraft fatalities and source disagreements rather than silently normalizing them. Earlier incomplete assumptions corrected by the audit include Tatarstan 363 in 2013, Aerosucre 157 in 2016 and Atlas Air 3591 in 2019.

### Unresolved cells
- 2014 = 4/6: MH370 missing-aircraft boundary and MH17 hostile/unlawful-action boundary.
- 2020 = 4/6: PS752 hostile/unlawful-action boundary.

`data/census/target-taxonomy-boundaries.json` records these ambiguities without resolving them or modifying F-002. The remaining G1 blocker is target taxonomy, not ordinary annual candidate discovery. Choosing a source convention after observing MH17, MH370 and PS752 would be post-outcome target editing.

## NTSB AVALL audit
The AGGIORNA #25 `ntsb-derived` artifact was recovered and audited. The repository stores provenance/hash metadata rather than the ~51 MB ZIP in normal Git history.

For Boeing-commercial airplane rows in 2010-2025, 1,250 of 1,358 rows recover an official sequence phase from `Events_Sequence` using the eADMS dictionary (92.05%); among rows with sequence data the result is 1,250 of 1,252. `NUSC` is explicit Non-U.S. Commercial, `NUSN` explicit Non-U.S. Noncommercial, and absent/unknown operation codes remain unknown. `inj_tot_f` and `inj_f_grnd` remain distinct so external fatalities are preserved.

## G2 — BLOCKED; denominator gap characterized
A complete defensible global Boeing family/year exposure denominator for 2010-2025 is still missing. The foundation audit now uses the full target-cohort universe: `727`, `737-Original`, `737-Classic`, `737-NG`, `737-MAX`, `747`, `757`, `767`, `777`, `787`; the current departures dataset has no canonical cells, so the audit remains explicitly incomplete rather than accepting aggregate traffic.

Historical IATA Safety Report Annex 4 editions publicly provide annual global sectors by manufacturer/model over overlapping windows through 2019. Later public reports inspected do not demonstrate a continuous compatible manufacturer/model table for 2020-2023. Historical IATA/OAG sector values are revision-sensitive, requiring an explicit vintage policy.

IATA WATS Global is proprietary. OAG Historical Flight Data is technically promising because it provides global historical schedules/operations, aircraft/equipment fields and historical schedule versions, but it is licensed/premium and unavailable to the current pipeline. OpenSky/ADS-B alternatives remain reconciliation/sensitivity sources only.

`data/exposure/cohort-aggregation-audit.json` records that all-variant Boeing 737 exposure cannot satisfy distinct Original/Classic/NG/MAX cells without an additional allocation model. Collapsing the cohorts would change the baseline/model comparison object; fleet-share, deliveries, accident counts or similar allocations remain prohibited. `baseline_present=false` is mandatory.

## G3 — BLOCKED; source-specific PIT evidence layer active
`bsfm/pit_evidence.py` and source-specific PIT inventories implement strict `verified / bounded / unknown` adjudication. Event date, approval/finalization, database last-change, retrieval date or current database presence are not publication evidence.

NTSB evidence now includes source/schema release anchors and field-release constraints. `Findings.cm_inPC`, for example, was added/back-filled in a 2024 release and cannot be leaked into earlier simulated cutoffs merely because it is present today. A historical AVALL distribution anchor exists by 2012, but source-level availability does not prove record/field-level availability.

FAA SDR now has its own release/field policy inventory and tests. As with NTSB, source-level releases can bound availability but cannot automatically verify a specific record/field at an earlier cutoff. Broad G3 PASS still requires archived/versioned source snapshots or record-specific official release evidence for every predictor admitted to a strict historical backtest.

## G4 — BLOCKED
G4 remains downstream of G1-G3. No candidate-vs-baseline model-skill claim is allowed while any upstream gate is blocked. The verified final audit reports `scientific_fit_ready=false`, `scientific_promotion_ready=false`, absolute accident probabilities disabled and validated-prediction claims disallowed.

## Resolution research — separate from F-002 scoring
Geography, MSN and flight number have independent fail-closed support gates. Retrospective discoverability is not predictive support. Estimator support, denominators/exposure, PIT evidence, provenance and uncertainty are required before a dimension can be promoted.

## Public/privacy/licensing state
Public UI must keep experimental/status boundaries. NTSB AVALL and FAA SDR remain supporting/descriptive sources with scope limits. The public repository contains no private user data or credentials. No new ICAO API retrieval is permitted. PR #1 remains closed without merge.

## Operational state
AGGIORNA #25 remains the latest successful full operational workflow. PR #2 has a successful read-only research verification at run `33996825005` but is still Draft / **do not merge yet**. G1-G4 remain BLOCKED.

## Exact next step
1. Keep 2014/2020 unresolved unless a separately versioned, scientifically defensible target-taxonomy rule is chosen; do not infer one from F-002.
2. Continue G2 only via genuinely compatible exposure evidence (lawful OAG/WATS access or another global cohort-level source) or a separately preregistered baseline redesign; do not use proxy splitting.
3. Continue G3 by acquiring archived/versioned record-level snapshots or official publication artifacts for NTSB/FAA SDR predictors and measuring strict PIT coverage; do not promote source-level release dates to record-level verification.
4. Keep PR #2 draft and F-002 immutable. Do not run AGGIORNA from the research branch. A post-merge AGGIORNA checkpoint is only appropriate after the remaining merge decision and scientific blockers have been explicitly handled.

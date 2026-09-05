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

## Prospective Target Taxonomy v2 — ADOPTED
Option B was selected on 2026-09-06. `docs/TARGET-TAXONOMY-v2-PROSPECTIVE.md` and `data/census/prospective-target-taxonomy-v2.json` now define the target semantics for future forecasts created after adoption.

The v2 primary target is a fatal aviation **safety accident** involving a Boeing commercial jet. Officially classified deliberate hostile/security/unlawful-interference events are excluded from the primary target and retained in a parallel descriptive census. Missing aircraft remain `PENDING_MISSING` until competent authority evidence establishes accident/equivalent fatal loss plus attributable fatality. External/ground/other-aircraft fatalities remain eligible when authoritatively attributable.

This taxonomy is explicitly non-retroactive:
- it does not apply to F-002;
- it does not change historical G1 v1;
- it does not reclassify MH370, MH17 or PS752;
- any future historical study using v2 must be separately versioned and re-adjudicate the whole interval symmetrically.

## Current research branch and verification
Draft PR #2, branch `research/privacy-safe-rebuild-20260905`, is the privacy-safe reconstruction of post-#25 research. It was created from current `main`; it does not import the commit history of closed PR #1. New Git metadata uses GitHub privacy-safe noreply identity.

A temporary read-only branch Research CI was used only to verify the research head and was then removed, restoring the repository's single-workflow invariant. The latest completed verification before the prospective-v2-only additions is `33997082566` and executed:
- full `pytest -q`: **158 passed**;
- `python -m bsfm.cli verify`: forecast registry integrity OK;
- `python -m bsfm.cli audit-foundation`: completed successfully;
- `python -m bsfm.cli audit-final`: completed successfully.

That run includes the strict source-specific G3 PIT gate wired into `availability_audit`: a generic PIT boolean can no longer bypass FAA/NTSB record-release evidence. The final audit correctly kept `point_in_time_availability_verified=false`, `leakage_free=false`, scientific fit readiness false and scientific promotion false.

The temporary CI had read-only repository permissions, did not ingest sources, deploy Pages, write generated state or push to `main`, and is no longer in the PR diff. This is a software/audit verification checkpoint, not AGGIORNA and not scientific validation.

## G1 — BLOCKED, 14/16 annual cells reconciled
`data/census/year-ledger.json` is the canonical 2010-2025 annual ledger. A cell passes only if all six controls are true: annual source scope demonstrated; all fatal jets mapped; Boeing target membership mapped; competent authority per candidate; independent reconciliation; target taxonomies resolved.

Reconciled 6/6 cells: 2010, 2011, 2012, 2013, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024 and 2025.

The integrated G1 census reconciles annual evidence with event-level candidate surfaces. The verified foundation audit reports 38 candidate rows, 35 included qualifying rows, no missing candidate IDs, no extra candidate IDs, no duplicate candidate IDs and no ledger/evidence consistency errors.

### Unresolved historical v1 cells
- 2014 = 4/6: MH370 missing-aircraft boundary and MH17 hostile/unlawful-action boundary.
- 2020 = 4/6: PS752 hostile/unlawful-action boundary.

`data/census/target-taxonomy-boundaries.json` preserves these ambiguities. The adoption of prospective v2 does not resolve them retroactively. Historical G1 v1 therefore remains BLOCKED at 14/16.

## NTSB AVALL audit
The AGGIORNA #25 `ntsb-derived` artifact was recovered and audited. The repository stores provenance/hash metadata rather than the ~51 MB ZIP in normal Git history.

For Boeing-commercial airplane rows in 2010-2025, 1,250 of 1,358 rows recover an official sequence phase from `Events_Sequence` using the eADMS dictionary (92.05%); among rows with sequence data the result is 1,250 of 1,252. `NUSC` is explicit Non-U.S. Commercial, `NUSN` explicit Non-U.S. Noncommercial, and absent/unknown operation codes remain unknown. `inj_tot_f` and `inj_f_grnd` remain distinct so external fatalities are preserved.

## G2 — BLOCKED; denominator gap characterized
A complete defensible global Boeing family/year exposure denominator for 2010-2025 is still missing. The foundation audit uses the full target-cohort universe: `727`, `737-Original`, `737-Classic`, `737-NG`, `737-MAX`, `747`, `757`, `767`, `777`, `787`; the current departures dataset has no canonical cells, so the audit remains explicitly incomplete rather than accepting aggregate traffic.

Historical IATA Safety Report Annex 4 editions publicly provide annual global sectors by manufacturer/model over overlapping windows through 2019. Later public reports inspected do not demonstrate a continuous compatible manufacturer/model table for 2020-2023. Historical IATA/OAG sector values are revision-sensitive, requiring an explicit vintage policy.

IATA WATS Global is proprietary. OAG Historical Flight Data is technically promising because it provides global historical schedules/operations, aircraft/equipment fields and historical schedule versions, but it is licensed/premium and unavailable to the current pipeline. OpenSky/ADS-B alternatives remain reconciliation/sensitivity sources only.

`data/exposure/cohort-aggregation-audit.json` records that all-variant Boeing 737 exposure cannot satisfy distinct Original/Classic/NG/MAX cells without an additional allocation model. `docs/G2-DATA-ACCESS-REQUIREMENTS-v1.md` defines the exact contract for any future exposure source. `baseline_present=false` remains mandatory.

## G3 — BLOCKED; strict source-specific PIT gate active
`bsfm/pit_evidence.py`, `bsfm/pit_coverage.py` and source-specific PIT inventories implement strict `verified / bounded / unknown` adjudication. Event date, approval/finalization, database last-change, retrieval date or current database presence are not publication evidence.

NTSB evidence includes source/schema release anchors and field-release constraints. A historical AVALL distribution anchor exists by 2012, but source-level availability does not prove record/field-level availability. NTSB `record_level_history_complete` therefore remains false and strict PIT readiness remains false.

FAA SDR has its own release/field policy and operational coverage audit. FAA states that SDRs become publicly searchable only after Quality Control review; therefore `SubmissionDate` cannot be treated as public `available_at`. Current annual CSVs also contain late submissions, demonstrating direct leakage risk if event/file year is used as availability.

`bsfm.cli.availability_audit()` requires both the generic source-state PIT signal and `strict_operational_pit_ready=true`; a generic PIT boolean cannot bypass source-specific evidence. `docs/G3-PIT-SNAPSHOT-ACQUISITION-v1.md` defines what archived evidence is sufficient for future `verified` PIT adjudication.

## G4 — BLOCKED
G4 remains downstream of G1-G3. No candidate-vs-baseline model-skill claim is allowed while any upstream gate is blocked. The verified final audit reports `scientific_fit_ready=false`, `scientific_promotion_ready=false`, absolute accident probabilities disabled and validated-prediction claims disallowed.

## Resolution research — separate from F-002 scoring
Geography, MSN and flight number have independent fail-closed support gates. Retrospective discoverability is not predictive support. Estimator support, denominators/exposure, PIT evidence, provenance and uncertainty are required before a dimension can be promoted.

## Public/privacy/licensing state
Public UI must keep experimental/status boundaries. NTSB AVALL and FAA SDR remain supporting/descriptive sources with scope limits. The public repository contains no private user data or credentials. No new ICAO API retrieval is permitted. PR #1 remains closed without merge.

## Operational state
AGGIORNA #25 remains the latest successful full operational workflow. PR #2 remains Draft / **do not merge yet**. G1-G4 remain BLOCKED. Prospective Target Taxonomy v2 is adopted for future forecasts only and does not change the current gate state.

## Exact next step
1. Keep historical G1 v1 at 14/16; do not retroapply v2 to 2014/2020 or F-002.
2. Use Target Taxonomy v2 for the next new forecast after F-002 and freeze the taxonomy reference in that forecast before its cutoff.
3. Continue G2 only via genuinely compatible exposure evidence (lawful OAG/WATS access or another global cohort-level source) or a separately preregistered baseline redesign; do not use proxy splitting.
4. Continue G3 by acquiring archived/versioned record-level snapshots or official publication artifacts for NTSB/FAA SDR predictors and measuring strict PIT coverage.
5. Keep PR #2 draft and F-002 immutable. Do not run AGGIORNA from the research branch.

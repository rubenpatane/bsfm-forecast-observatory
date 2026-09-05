# BSFM Project State

Updated: 2026-09-06

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #25 (`33978802087`) completed successfully on source SHA `971cdd6a1ec0576208191e2d18fe76fce2742c86`; it is the latest workflow-verified baseline.
- The generated-state commit on `main` is `ce33ea54b36613cf122e3201c2825a329700f656` and uses privacy-safe Git metadata.
- No new ICAO API retrieval is permitted. The frozen historical ICAO evidence is cross-check material only.
- Workflow/CI success verifies only executed software checks; it does not establish predictive validity or open a scientific gate.

## Canonical documents
`AGENTS.md` is the constitution/privacy/bootstrap; `docs/MODEL-SPEC.md` the model contract; `docs/LABORATORY-PROTOCOL.md` the scientific protocol; `docs/NEW-CHAT.md` the fresh-session bootstrap; `docs/F-002-PREREGISTRATION-v1.md` the frozen F-002 evaluation; `docs/G1-G3-EVIDENCE-PLAN-v1.md` the detailed evidence plan.

## F-002
`forecasts/F-002.json` is frozen. Its target string is `next_fatal_accident_involving_boeing_commercial_jet`; the forecast object contains no explicit hostile/unlawful-action or missing-aircraft inclusion/exclusion clause. Later research must not silently add one to F-002.

F-002 is byte-identical to `main` on the active research branch (blob `eb55a77210d2fd254483ff74c3d02fcd60c1f0ad`) and is not part of PR #2's diff.

## Current research branch
Draft PR #2, branch `research/privacy-safe-rebuild-20260905`, is the privacy-safe reconstruction of post-#25 research work. It was created directly from current `main`; it does not import the commit history of the superseded PR #1. New commits use GitHub `users.noreply.github.com` metadata. PR #1 was closed without merge after its scientific/data artifacts were ported to the privacy-safe branch.

A focused local rebuild suite previously reported `23 passed` with `PYTHONPATH=. pytest -q`. That result predates the latest annual-evidence and G3 expansion and is not repository CI or AGGIORNA verification. `tests/test_g1_year_ledger.py` enforces that every `reconciled=true` year must have all six annual controls true. `tests/test_pit_evidence.py` falsifies administrative-timestamp leakage and requires exact evidenced publication timing for strict PIT admission. The current branch still requires a fresh full workflow run before merge.

The only workflow is AGGIORNA and it is triggered by `workflow_dispatch` or schedule, not `pull_request`; absence of automatic PR checks is therefore expected. The local runtime used in the current research session cannot resolve `github.com`, so it cannot clone the complete repository for a fresh full-suite run.

## G1 — BLOCKED, 14/16 annual cells reconciled
`data/census/year-ledger.json` is the canonical 2010-2025 reconciliation ledger. An annual cell passes only if all six controls are true:
1. annual source scope demonstrated;
2. all fatal jets mapped;
3. Boeing target membership mapped;
4. competent authority per candidate;
5. independent reconciliation;
6. target taxonomies resolved.

`14/16` is an annual-cell evidence result, not predictive validation.

### Reconciled annual cells — 6/6
- 2010
- 2011
- 2012
- 2013
- 2015
- 2016
- 2017
- 2018
- 2019
- 2021
- 2022
- 2023
- 2024
- 2025

These cells include explicit handling of external/ground/other-aircraft fatalities rather than relying on historical onboard-only fatality summaries. Notable reconciled edge cases include Allied Air 2012, CEIBA 2015, Emirates EK521 in 2016, ACT Airlines Bishkek 2017, Fly Jamaica 2018, and ACT Airlines Hong Kong 2025.

The reconstruction also corrected several incomplete earlier candidate assumptions: Tatarstan 363 is part of the 2013 Boeing set; Aerosucre 157 is part of 2016; Atlas Air 3591 is part of 2019. Source-specific discrepancies are retained rather than silently corrected, including Allied Air external-fatality counts and Air Niugini P2-PXE serial-number disagreement.

### Unresolved annual cells
#### 2014 — 4/6
The fatal-jet universe is mapped, but target membership/taxonomy remain unresolved for:
- MH370 — missing-aircraft boundary;
- MH17 — hostile/unlawful-action boundary.

#### 2020 — 4/6
The fatal-jet universe is mapped. Pegasus PC2193 and Air India Express IX1344 are qualifying Boeing candidates. PS752 remains unresolved because the competent Annex 13 investigation describes a fatal Boeing accident while IATA safety statistics exclude the event as an unlawful/security act.

`data/census/target-taxonomy-boundaries.json` records these ambiguities explicitly. It does not resolve them or modify F-002.

### Why G1 remains blocked
The remaining problem is no longer missing annual discovery work. The frozen target and canonical evidence plan do not contain a pre-existing rule that decides:
- whether hostile/unlawful-action occurrences belong to the BSFM accident target;
- whether a missing aircraft such as MH370 qualifies before a fully established accident sequence is available.

Choosing a favorable source convention after inspecting MH17, MH370 and PS752 would create a post-outcome target rule. Therefore 2014 and 2020 remain fail-closed unless an independently pre-existing rule is recovered. A new taxonomy may be versioned prospectively, but it must not be assumed to rewrite F-002 or its historical G1 validation.

### NTSB AVALL audit
The AGGIORNA #25 `ntsb-derived` artifact was recovered and audited. The repository stores provenance/hash metadata instead of the ~51 MB ZIP in normal Git history.

For Boeing-commercial airplane rows in 2010-2025 under the implemented AVALL classification, 1,250 of 1,358 rows recover an official sequence phase from `Events_Sequence` using the eADMS dictionary (92.05%); among rows with sequence data the result is 1,250 of 1,252. These are research diagnostics only.

`NUSC` is explicit Non-U.S. Commercial, `NUSN` explicit Non-U.S. Noncommercial, and absent/unknown operation codes remain unknown. `inj_tot_f` and `inj_f_grnd` remain distinct so external fatalities are preserved. Foreign NTSB records never silently override the competent investigation authority.

## G2 — BLOCKED; public-source gap now characterized
A complete defensible global Boeing family/year exposure denominator for 2010-2025 is still missing.

### Public IATA path
Historical IATA Safety Report Annex 4 editions publicly provide annual global sectors by manufacturer/model over overlapping windows through 2019. The 2019 edition contains model-level 2015-2019 sectors.

The inspected later public reports no longer demonstrate the same continuous manufacturer/model table: the 2021 report exposes jet/turboprop sector landings by region, and the 2023 public material exposes aggregate sector/rate information rather than the former model matrix. A reproducible public manufacturer/model bridge for 2020-2023 has not been demonstrated.

IATA also states that historical sector figures can change between report vintages as source data/classifications are updated. Therefore G2 requires an explicit vintage policy; revised modern history and contemporaneous report vintages must not be mixed silently.

### Commercial longitudinal candidates
IATA WATS Global advertises 2010-2025 history and aircraft/model utilization but is a subscription/proprietary product. Public WATS releases for 2024-2025 expose Boeing 737 all-variant flight frequencies, which are not sufficient to split 737 Original/Classic/NG/MAX.

`data/exposure/oag-historical-source.json` registers OAG Historical Flight Data/Schedules as a second high-priority candidate. OAG documents global history from 2004, aircraft/equipment fields, scheduled and actual flight records, and a historical mode that can retrieve schedules as they were published at the time. This is methodologically promising for vintage control, but the project currently has no licensed OAG dataset and has not demonstrated equipment-code coverage for every BSFM cohort.

EUROCONTROL provides valuable free flight-level research datasets with aircraft types, but its scope is European rather than global and therefore cannot serve as the BSFM global denominator.

### G2 consequence
The 2020-2023 problem is no longer treated as a simple missing-download task. A G2 PASS now requires either:
- lawful/licensed extraction from a global source such as OAG or WATS with reproducible query/code mapping, actual/performed-flight semantics, cohort coverage and a frozen vintage policy; or
- a prospectively versioned alternative cohort/denominator design that does not rewrite the frozen F-002 evaluation.

No cumulative-rate inversion, fleet-share allocation, delivery-share split, accident-based allocation or hidden imputation is permitted. `baseline_present=false` remains mandatory.

## G3 — BLOCKED; source-level PIT policy now explicit
`bsfm/pit_evidence.py`, `data/pit/ntsb-avall-policy.json`, `data/pit/ntsb-release-inventory.json` and `tests/test_pit_evidence.py` define a strict source-specific PIT evidence layer.

Only `pit_status=verified` with an explicit evidenced public-release timestamp may enter a strict cutoff. `bounded` and `unknown` are excluded. Event date, administrative approval/finalization, database last-change, current retrieval time, or simple presence in today's AVALL database are not publication evidence.

NTSB official evidence now establishes several source-level release anchors:
- eADMS public schema listed in the legacy public AV-data directory in 2010;
- AVALL.ZIP publicly listed there with a 2012-06-01 timestamp;
- CAROL public launch on 2020-10-13;
- expanded aviation dataset/CSV/JSON search announced on 2023-07-17;
- MDB release 2.9 on 2023-10-26;
- MDB release 3.0 on 2024-03-01, including `cm_inPC` addition/back-fill;
- current monthly/weekly AVALL distribution in 2026.

These anchors prove source-level public distribution epochs, not record-level or field-level historical presence. In particular, a back-filled modern field must inherit the later release evidence unless an earlier snapshot proves otherwise.

The accessible official surfaces do not provide a complete retained archive of monthly AVALL contents for every 2010-2025 cutoff. A third-party preserved NTSB snapshot dated 2025-04-21 exists and can serve as one additional anchor, but it does not close the historical series. Broad G3 PASS therefore still requires archived/versioned snapshots or record-specific official publication artifacts.

## G4 — BLOCKED
G4 remains downstream of G1-G3. No candidate-vs-baseline model-skill claim is allowed while any upstream gate is blocked.

## Resolution research — separate from F-002 scoring
Geography, MSN and flight number have independent fail-closed support gates. Retrospective discoverability is not predictive support. Estimator support, denominators/exposure, PIT evidence, provenance and uncertainty are required before a dimension can be promoted.

## Public/privacy/licensing state
Public UI must keep experimental/status boundaries. NTSB AVALL and FAA SDR remain supporting/descriptive sources with scope limits. The NTSB snapshot directory contains provenance and hashes rather than the large ZIP. The public repository contains no private user data or credentials. No new ICAO API retrieval is permitted.

## Operational state
AGGIORNA #25 remains the latest successful full workflow run. All privacy-safe rebuild commits, the NTSB normalization work, the 14/16 annual G1 reconciliation, the G2 source characterization and the G3 PIT policy are newer and therefore not workflow-verified. Draft PR #2 remains **do not merge yet**. G1-G4 remain BLOCKED.

## Exact next step
1. Keep 2014 and 2020 unresolved for the frozen F-002 validation unless an independently pre-existing target rule is recovered; do not create a post-hoc rule merely to reach 16/16.
2. If BSFM is to have a future target version, create a separately versioned prospective taxonomy for hostile/unlawful-action and missing-aircraft semantics, with an explicit statement that it does not retroactively rewrite F-002 unless a defensible preregistration basis is demonstrated.
3. For G2, decide whether the project will obtain lawful access to a global historical dataset such as OAG or WATS. Without such access, retain G2 BLOCKED rather than fabricating the 2020-2023/model-cohort bridge.
4. For G3, continue only with versioned/archived dataset snapshots or record-specific official publication evidence; source-level dates alone are not enough.
5. Run AGGIORNA manually on the research branch/merged checkpoint when the branch is ready for workflow verification. The current workflow has no pull-request trigger.
6. Keep F-002 immutable and every unresolved scientific gate fail-closed.

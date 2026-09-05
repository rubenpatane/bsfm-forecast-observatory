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

## F-002
`forecasts/F-002.json` is frozen. Its target string is `next_fatal_accident_involving_boeing_commercial_jet`; the forecast object contains no explicit hostile/unlawful-action or missing-aircraft inclusion/exclusion clause. Later research must not silently add one to F-002.

F-002 is byte-identical to `main` on the active research branch (blob `eb55a77210d2fd254483ff74c3d02fcd60c1f0ad`) and is not part of PR #2's diff.

## Current research branch
Draft PR #2, branch `research/privacy-safe-rebuild-20260905`, is the privacy-safe reconstruction of post-#25 research work. It was created directly from current `main`; it does not import the commit history of the superseded PR #1. New commits use GitHub `users.noreply.github.com` metadata. PR #1 was closed without merge after its scientific/data artifacts were ported to the privacy-safe branch.

A focused local rebuild suite previously reported `23 passed` with `PYTHONPATH=. pytest -q`. That result predates the latest annual-evidence, G2 and G3 expansion and is not repository CI or AGGIORNA verification. New tests now enforce annual ledger/evidence consistency, fail-closed G2 candidate-source status, PIT evidence rules and NTSB field-release bounds. These newer tests have not yet been executed in a fresh full verifiable repository run.

The repository has no `pull_request` workflow trigger. AGGIORNA is dispatch/scheduled only and contains generated-state logic that can push to `main`; therefore it must not be used as an ad-hoc PR test runner from the research branch.

## G1 — BLOCKED, 14/16 annual cells reconciled
`data/census/year-ledger.json` is the canonical 2010-2025 reconciliation ledger. An annual cell passes only if all six controls are true: annual source scope demonstrated; all fatal jets mapped; Boeing target membership mapped; competent authority per candidate; independent reconciliation; target taxonomies resolved.

Reconciled 6/6 cells: 2010, 2011, 2012, 2013, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024 and 2025.

The reconstruction explicitly preserves external/ground/other-aircraft fatalities. It also corrected incomplete earlier candidate assumptions, including Tatarstan 363 in 2013, Aerosucre 157 in 2016 and Atlas Air 3591 in 2019. Source discrepancies remain visible rather than being silently corrected.

### Unresolved cells
- 2014 = 4/6: MH370 missing-aircraft boundary and MH17 hostile/unlawful-action boundary.
- 2020 = 4/6: PS752 hostile/unlawful-action boundary.

`data/census/target-taxonomy-boundaries.json` records these ambiguities without resolving them or modifying F-002. The remaining G1 blocker is target taxonomy, not ordinary annual candidate discovery. Choosing a favorable source convention after inspecting MH17, MH370 and PS752 would be post-outcome target editing.

## NTSB AVALL audit
The AGGIORNA #25 `ntsb-derived` artifact was recovered and audited. The repository stores provenance/hash metadata rather than the ~51 MB ZIP in normal Git history.

For Boeing-commercial airplane rows in 2010-2025 under the implemented AVALL classification, 1,250 of 1,358 rows recover an official sequence phase from `Events_Sequence` using the eADMS dictionary (92.05%); among rows with sequence data the result is 1,250 of 1,252. `NUSC` is explicit Non-U.S. Commercial, `NUSN` explicit Non-U.S. Noncommercial, and absent/unknown operation codes remain unknown. `inj_tot_f` and `inj_f_grnd` remain distinct so external fatalities are preserved.

## G2 — BLOCKED; public-source gap characterized
A complete defensible global Boeing family/year exposure denominator for 2010-2025 is still missing.

Historical IATA Safety Report Annex 4 editions publicly provide annual global sectors by manufacturer/model over overlapping windows through 2019. Later public reports inspected do not demonstrate the same continuous manufacturer/model table for 2020-2023. IATA also states that historical sector figures can change between report vintages, so a future denominator requires an explicit vintage policy.

IATA WATS Global advertises longitudinal aircraft/model utilization but is a subscription/proprietary product. OAG Historical Flight Data is technically promising because it provides global historical schedules/operations, aircraft/equipment fields and historical schedule versions, but it is a licensed/premium source not available to the current project pipeline.

Open alternatives do not close the gap. `data/exposure/open-adsb-alternatives.json` records OpenSky and ADS-B Exchange as reconciliation/sensitivity sources only: OpenSky lacks pre-2013 data, has uneven receiver coverage, relies on external/crowdsourced aircraft metadata and does not natively provide commercial-schedule semantics; free ADS-B Exchange historical samples do not cover every day and cannot be extrapolated into a canonical annual denominator. `data/exposure/oag-historical-source.json` remains candidate-only. `baseline_present=false` remains mandatory.

No cumulative-rate inversion, fleet-share allocation, delivery-share split, accident-based allocation, ADS-B sample extrapolation or hidden imputation is permitted.

## G3 — BLOCKED; source-level PIT policy explicit
`bsfm/pit_evidence.py`, `data/pit/ntsb-avall-policy.json`, `data/pit/ntsb-release-inventory.json`, `data/pit/ntsb-field-release-policy.json` and their tests define a strict source-specific PIT evidence layer.

Only `pit_status=verified` with explicit evidenced public-release timing may enter a strict cutoff. `bounded` and `unknown` are excluded. Event date, administrative approval/finalization, database last-change, current retrieval time, or simple presence in today's AVALL/CAROL database are not publication evidence.

Official NTSB evidence establishes datasource/schema milestones including CAROL public launch on 2020-10-13, expanded aviation search/CSV/JSON availability on 2023-07-17, MDB release 2.9 on 2023-10-26 and MDB release 3.0 on 2024-03-01. The 2024 release added `Findings.cm_inPC` and back-filled historical rows, so `cm_inPC` must not be admitted at earlier simulated cutoffs merely because it is present today.

These milestones bound datasource/schema availability; they do not prove record-level field publication. Broad G3 PASS still requires archived/versioned snapshots or record-specific official publication artifacts for every predictor admitted to historical backtests.

## G4 — BLOCKED
G4 remains downstream of G1-G3. No candidate-vs-baseline model-skill claim is allowed while any upstream gate is blocked.

## Resolution research — separate from F-002 scoring
Geography, MSN and flight number have independent fail-closed support gates. Retrospective discoverability is not predictive support. Estimator support, denominators/exposure, PIT evidence, provenance and uncertainty are required before a dimension can be promoted.

## Public/privacy/licensing state
Public UI must keep experimental/status boundaries. NTSB AVALL and FAA SDR remain supporting/descriptive sources with scope limits. The public repository contains no private user data or credentials. No new ICAO API retrieval is permitted.

## Operational state
AGGIORNA #25 remains the latest successful full workflow run. All privacy-safe rebuild commits and the current G1/G2/G3 work are newer and therefore not workflow-verified. Draft PR #2 remains **do not merge yet**. G1-G4 remain BLOCKED.

## Exact next step
Build the same source-specific PIT release/availability inventory for FAA SDR that now exists for NTSB, preserving `unknown`/`bounded` whenever historical public availability cannot be proven; do not modify F-002, resolve the 2014/2020 taxonomy post hoc, promote any G2 proxy, add a new workflow, merge PR #2, or run AGGIORNA from the research branch as part of that step.

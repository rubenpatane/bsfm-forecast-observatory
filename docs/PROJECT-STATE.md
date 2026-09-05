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

## Current research branch
Draft PR #2, branch `research/privacy-safe-rebuild-20260905`, is the privacy-safe reconstruction of post-#25 research work. It was created directly from current `main`; it does not import the commit history of the superseded PR #1. New commits use GitHub `users.noreply.github.com` metadata. PR #1 was closed without merge after its scientific/data artifacts were ported to the privacy-safe branch.

A focused local rebuild suite previously reported `23 passed` with `PYTHONPATH=. pytest -q`. That result predates the latest annual-evidence expansion and is not repository CI or AGGIORNA verification. A new `tests/test_g1_year_ledger.py` now enforces that every `reconciled=true` year must have all six annual controls true, but the current branch still requires a fresh full test/workflow run before merge.

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

Choosing a favorable source convention after inspecting MH17, MH370 and PS752 would create a post-outcome target rule. Therefore 2014 and 2020 remain fail-closed until a scientifically defensible, versioned taxonomy decision is made with its applicability to frozen forecasts explicitly stated.

### NTSB AVALL audit
The AGGIORNA #25 `ntsb-derived` artifact was recovered and audited. The repository stores provenance/hash metadata instead of the ~51 MB ZIP in normal Git history.

For Boeing-commercial airplane rows in 2010-2025 under the implemented AVALL classification, 1,250 of 1,358 rows recover an official sequence phase from `Events_Sequence` using the eADMS dictionary (92.05%); among rows with sequence data the result is 1,250 of 1,252. These are research diagnostics only.

`NUSC` is explicit Non-U.S. Commercial, `NUSN` explicit Non-U.S. Noncommercial, and absent/unknown operation codes remain unknown. `inj_tot_f` and `inj_f_grnd` remain distinct so external fatalities are preserved. Foreign NTSB records never silently override the competent investigation authority.

## G2 — BLOCKED
A complete defensible global Boeing family/year exposure denominator for 2010-2025 is still missing.

Public IATA Annex 4 material supports manufacturer/model sector observations over overlapping windows through at least 2019, but:
- a sustainable compatible 2020-2023 public bridge has not been demonstrated;
- Boeing 737 all-variant exposure cannot be split into Original/Classic/NG/MAX with fleet share, deliveries, accident counts or other convenience proxies;
- historical IATA/OAG values are revision-sensitive and require a declared vintage rule;
- historically eligible families such as 727 and 737-Original require compatible exposure or a separately preregistered exclusion before G2/G4 can pass.

No cumulative-rate inversion, fleet-share allocation or hidden imputation is permitted.

## G3 — BLOCKED
Historical predictor records still lack complete field-level point-in-time public-availability evidence at simulated cutoffs. Current presence in NTSB AVALL or a later administrative timestamp does not establish historical public availability. Strict backtests must exclude PIT-unknown fields.

## G4 — BLOCKED
G4 remains downstream of G1-G3. No candidate-vs-baseline model-skill claim is allowed while any upstream gate is blocked.

## Resolution research — separate from F-002 scoring
Geography, MSN and flight number have independent fail-closed support gates. Retrospective discoverability is not predictive support. Estimator support, denominators/exposure, PIT evidence, provenance and uncertainty are required before a dimension can be promoted.

## Public/privacy/licensing state
Public UI must keep experimental/status boundaries. NTSB AVALL and FAA SDR remain supporting/descriptive sources with scope limits. The NTSB snapshot directory contains provenance and hashes rather than the large ZIP. The public repository contains no private user data or credentials. No new ICAO API retrieval is permitted.

## Operational state
AGGIORNA #25 remains the latest successful full workflow run. All privacy-safe rebuild commits, the NTSB normalization work, and the 14/16 annual G1 reconciliation are newer and therefore not workflow-verified. Draft PR #2 remains **do not merge yet**. G1-G4 remain BLOCKED.

## Exact next step
1. Do not continue searching ordinary annual G1 candidates as if 2014/2020 were data gaps; their remaining blocker is target taxonomy.
2. Decide whether BSFM should create an append-only target-taxonomy specification that prospectively defines hostile/unlawful-action and missing-aircraft semantics, and separately decide whether such a new rule is scientifically allowed to affect the already-frozen F-002 evaluation and the current historical G1 census. Do not apply it retroactively by assumption.
3. In parallel, continue G2 research for a compatible global 2020-2023 model/family exposure bridge and G3 PIT manifests; these gates remain independently blocked regardless of the G1 taxonomy decision.
4. Run a fresh full repository test/workflow checkpoint on PR #2 before any merge. Keep F-002 immutable and keep every unresolved gate fail-closed.

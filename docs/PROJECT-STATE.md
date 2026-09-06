# BSFM Project State

Updated: 2026-09-06

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #27 (`34001974951`) completed successfully on source SHA `843dd6abc1a30f8e318fcee9d34d4ec9bff3e43a`; it is the latest full operational/workflow-verified baseline.
- The generated-state commit on `main` is `a6c3602` and uses privacy-safe Git metadata.
- No new ICAO API retrieval is permitted. Frozen historical ICAO evidence is cross-check material only.
- Workflow/software success verifies only executed checks; it does not establish predictive validity or open a scientific gate.

## F-002
`forecasts/F-002.json` is frozen. Its target string is `next_fatal_accident_involving_boeing_commercial_jet`; the forecast object contains no explicit hostile/unlawful-action or missing-aircraft inclusion/exclusion clause. Later research must not silently add one.

F-002 remained byte-identical through the PR #2 integration (blob `eb55a77210d2fd254483ff74c3d02fcd60c1f0ad`) and was not part of that PR's diff.

## Prospective Target Taxonomy v2 — ADOPTED
Option B was selected on 2026-09-06. `docs/TARGET-TAXONOMY-v2-PROSPECTIVE.md` and `data/census/prospective-target-taxonomy-v2.json` define target semantics for future forecasts created after adoption.

The v2 primary target is a fatal aviation **safety accident** involving a Boeing commercial jet. Officially classified deliberate hostile/security/unlawful-interference events are excluded from the primary target and retained in a parallel descriptive census. Missing aircraft remain `PENDING_MISSING` until competent-authority evidence establishes accident/equivalent fatal loss plus attributable fatality. External/ground/other-aircraft fatalities remain eligible when authoritatively attributable.

This taxonomy is explicitly non-retroactive: it does not apply to F-002, historical G1 v1, MH370, MH17 or PS752. Any future historical study using v2 must be separately versioned and re-adjudicate the full interval symmetrically.

## Current research branch and verification
PR #2, branch `research/privacy-safe-rebuild-20260905`, was the privacy-safe reconstruction of post-#25 research. It was squash-merged into `main` as `80333b03658cc89cec80b35d4abb629f824487aa`; the integration does not import the commit history of closed PR #1.

The latest successful read-only Research CI run is `34000757503`, verified at research SHA `c5cc3e63a1a21605ee416f971fbe1d1cf8493bdd` before removal of the temporary workflow. It executed:
- full `pytest -q`: **188 passed**;
- `python -m bsfm.cli verify`: forecast registry integrity OK;
- `python -m bsfm.cli audit-foundation`: completed successfully;
- `python -m bsfm.cli audit-final`: completed successfully.

The temporary research workflow was subsequently removed, restoring the single-workflow repository invariant. The verified final audit still reports historical G1 incomplete, `baseline_present=false`, `point_in_time_availability_verified=false`, `leakage_free=false`, scientific fit readiness false and scientific promotion false. This is software/audit verification, not scientific validation.

The public validation surface has now been completed on the research branch. `site/data/research-state.json` exposes the fail-closed annual G1 state, and AGGIORNA is wired to regenerate it before publication. The bilingual validation page displays 14/16 historical G1 reconciliation, the separate 35/35 outcome-publication ledger, the fixed G2 no-proxy rule, the model 1.2 `faa_sdr_precursors` obligation and the distinction from the minimal shrinkage estimator. Desktop/mobile browser checks passed, including language switching, generated-data loading, responsive navigation and absence of horizontal overflow. The full local suite passed with 188 tests plus registry verification and both scientific audits; this page batch has not been run through AGGIORNA and does not change any scientific gate.

## G1 — BLOCKED, 14/16 annual cells reconciled
`data/census/year-ledger.json` is the canonical 2010-2025 annual ledger. A cell passes only if all six controls are true: annual source scope demonstrated; all fatal jets mapped; Boeing target membership mapped; competent authority per candidate; independent reconciliation; target taxonomies resolved.

Reconciled 6/6 cells: 2010, 2011, 2012, 2013, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024 and 2025.

The integrated G1 census reports 38 candidate rows, 35 included qualifying rows, no missing candidate IDs, no extra candidate IDs, no duplicate candidate IDs and no ledger/evidence consistency errors.

Unresolved historical v1 cells remain:
- 2014 = 4/6: MH370 missing-aircraft boundary and MH17 hostile/unlawful-action boundary;
- 2020 = 4/6: PS752 hostile/unlawful-action boundary.

Prospective taxonomy v2 does not resolve these retroactively. Historical G1 v1 remains BLOCKED at 14/16.

## G2 — BLOCKED; acquisition path is now executable
A complete defensible global Boeing family/year exposure denominator for 2010-2025 is still missing. The required cohort universe remains `727`, `737-Original`, `737-Classic`, `737-NG`, `737-MAX`, `747`, `757`, `767`, `777`, `787`.

Public discovery has not produced a complete compatible source. Historical IATA Safety Report Annex 4 data provide model-level sectors through 2019, but no compatible public bridge for the full later interval has been demonstrated. Aggregate Boeing or all-737 traffic cannot be disaggregated by proxy.

The highest-priority lawful commercial candidates are now OAG Historical Flight Data, Cirium Historical Flight Status/Schedules and IATA WATS Global. `data/exposure/source-inventory.json` records their current status; OAG and Cirium appear technically capable of exposing historical flight/equipment information, but no licensed BSFM extract has yet been inspected and their exact operated-flight scope, cargo/charter coverage, equipment resolution, vintage semantics and licence constraints must be audited.

`bsfm/exposure_import.py` now provides a vendor-neutral ingestion/acceptance surface for a future lawful extract. It requires one standardized row per flight leg with `flight_date`, `equipment_code`, `leg_id`, `operated`, `scope` and `vintage_id`; counts only explicitly operated `global_commercial` rows; maps only deterministic allowlisted equipment; rejects invalid/conflicting duplicates and unknown equipment; and runs the canonical full cohort-year matrix audit. No convenience allocation or fleet-share split is permitted.

Therefore the remaining G2 blocker is primarily **lawful source access plus product-scope validation**, not missing importer code. `baseline_present=false` remains mandatory until a full accepted matrix exists.

## G3 — BLOCKED; predictor-universe gate is explicit
`data/pit/predictor-universe-v1.json` now defines the G3 predictor-universe registry. It is intentionally `DRAFT_UNFROZEN`, `frozen=false`, with no admitted predictors. Candidate NTSB/FAA fields are not automatically admissible.

`bsfm/pit_coverage.py` now evaluates strict PIT readiness only for an explicitly frozen, non-empty admitted predictor universe. Every admitted predictor must identify source/fields/evidence, be `pit_status=verified`, have complete field/snapshot evidence and depend on a source that is itself strict-PIT ready. This prevents both failure modes: unrelated manifests cannot accidentally define the scientific universe, and problematic predictors cannot be silently ignored.

NTSB evidence now includes a strong later snapshot anchor: ICPSR/DataLumos V1 preserves an `avall.zip` in a versioned public deposit dated 2025-04-21. Exact bytes/hash and record/field inspection are still required before individual values can be promoted to `verified`; it does not establish availability before 2025-04-21. The older official NTSB directory proves AVALL public distribution by 2012, but the historical file URL now returns 404 and preserved 2012 bytes have not been acquired, so that remains a source-level bound only.

FAA SDR remains the harder PIT blocker. FAA states reports must complete Quality Control before becoming publicly searchable, so `SubmissionDate` is not public `available_at`; current annual CSVs contain later submissions and are reconstructed current-state files, not historical snapshots. Public research has not located a byte-preserved official historical CSV sequence sufficient for broad record-level PIT verification.

The separate G1 outcome publication ledger is now **35/35 verified and complete**. Reviewed annual overlays provide conservative competent-authority, official-government or stable public-snapshot bounds for every included outcome. When an artifact establishes only a month or year, `available_at` is normalized to the last calendar day of that period; later stable bounds are preferred over unproven earliest dates. This does not change the historical G1 census or resolve its 2014/2020 target-taxonomy boundaries. Outcome publication timing also remains distinct from predictor PIT: ledger completion does not open G3 while the model 1.2 predictor obligations remain unmet.

The canonical `config/model.json` model 1.2 explicitly includes `faa_sdr_precursors`. Therefore simply dropping FAA SDR from G3 to manufacture a PASS would be a **model redesign**, not a harmless narrowing of the predictor universe. Any model that removes/replaces that component must be separately versioned prospectively before skill interpretation.

## NTSB AVALL descriptive audit
The AGGIORNA #25 `ntsb-derived` artifact was recovered and audited. For Boeing-commercial airplane rows in 2010-2025, 1,250 of 1,358 rows recover an official sequence phase from `Events_Sequence` (92.05%); among rows with sequence data the result is 1,250 of 1,252. These descriptive results do not make historical predictor values PIT-admissible.

## G4 — BLOCKED
G4 remains downstream of G1-G3. No candidate-vs-baseline model-skill claim is allowed while upstream gates are blocked. The latest verified final audit keeps `scientific_fit_ready=false`, `scientific_promotion_ready=false`, absolute accident probabilities disabled and validated-prediction claims disallowed.

The committed-but-not-yet-workflow-verified automatic-cycle implementation now adds a frozen machine-readable cycle contract, content-addressed training snapshots, fail-closed parameter fitting, a 90-day discrete first-event distribution, probability of no event in the horizon, modal date, conditional 80% interval and an exposure-only temporal baseline on the identical future exposure path. Paired temporal evaluation rejects unverified outcomes, non-future outcomes and unequal horizons, and uses full-horizon logarithmic score including right censoring. This completes the internal executable architecture, not real G4 evidence. The executable `minimal_shrunk_hazard_v1` remains explicitly a candidate estimator and is not relabelled as the complete model 1.2 contract.

## Public/privacy/licensing state
Public UI must keep experimental/status boundaries. NTSB AVALL and FAA SDR remain supporting/descriptive sources with scope limits. The public repository contains no private user data or credentials. No new ICAO API retrieval is permitted. PR #1 remains closed without merge.

## Operational state
AGGIORNA #27 is the latest successful full operational workflow. It refreshed FAA SDR and NTSB AVALL state, generated eight post-cutoff FAA SDR similarity signals, committed auditable state and deployed the GitHub Pages observatory. The live page was verified to render all eight signals without browser errors. PR #2 is merged into `main`; the temporary research workflow remains absent.

The current local batch extends AGGIORNA with the versioned automatic research-cycle state and extends the methodology page with its live status and scientific boundary. `docs/AUTOMATED-RESEARCH-CYCLE-v1.md` is the detailed publication contract. Local verification passed with 199 tests, registry verification and both audits; workflow verification is still required before this batch can become the new operational baseline.

## Exact next step / external dependencies
Obtain and acceptance-audit a lawful OAG/Cirium/IATA WATS global Boeing cohort×year operated-flight extract for G2; without it the real automatic fit, temporal backtest and forecast remain correctly blocked even though their execution path is implemented.

# BSFM Project State

Updated: 2026-09-06

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #33 (`34037238514`) completed successfully on source SHA `49e03e42c4f2ce1e331329a87681f04d15ac344e`; it is the latest full operational/workflow-verified baseline.
- The generated-state commit on `main` is `bba9f32db03fd6d7b660bc535d0c9b6e00213af9` and uses privacy-safe Git metadata.
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

The latest successful read-only Research CI run is #24 (`34033044616`), verified at research SHA `3edd6fcc522848ba73f6e4902e113eb164a88a55` before removal of the temporary workflow. It executed:
- full `pytest -q`: **241 passed**;
- `python -m bsfm.cli verify`: forecast registry integrity OK;
- `python -m bsfm.cli audit-foundation`: completed successfully;
- `python -m bsfm.cli audit-final`: completed successfully.

The temporary research workflow was subsequently removed, restoring the single-workflow repository invariant. The verified final audit still reports historical G1 incomplete, `baseline_present=false`, `point_in_time_availability_verified=false`, `leakage_free=false`, scientific fit readiness false and scientific promotion false. This is software/audit verification, not scientific validation.

The public validation surface exposes the fail-closed annual G1 state, the separate 35/35 outcome-publication ledger, the fixed G2 no-proxy rule, the model 1.2 `faa_sdr_precursors` obligation and the distinction from the minimal shrinkage estimator. It is workflow-verified and deployed; it does not change any scientific gate.

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

NARA records schedule DAA-0237-2023-0006 now adds an official retention path: mandatory FAA SDR records are permanent digital records, cut off upon processing and transferred to the National Archives 20 years after cutoff. It does not expose the processing/public-release timestamp of individual 2010-2025 records or provide the needed online historical snapshots; therefore G3 remains BLOCKED. A targeted FAA records/FOIA request for processing timestamps or retained historical exports is now the only identified non-model-redesign acquisition path.

The separate G1 outcome publication ledger is now **35/35 verified and complete**. Reviewed annual overlays provide conservative competent-authority, official-government or stable public-snapshot bounds for every included outcome. When an artifact establishes only a month or year, `available_at` is normalized to the last calendar day of that period; later stable bounds are preferred over unproven earliest dates. This does not change the historical G1 census or resolve its 2014/2020 target-taxonomy boundaries. Outcome publication timing also remains distinct from predictor PIT: ledger completion does not open G3 while the model 1.2 predictor obligations remain unmet.

The canonical `config/model.json` model 1.2 explicitly includes `faa_sdr_precursors`. Therefore simply dropping FAA SDR from G3 to manufacture a PASS would be a **model redesign**, not a harmless narrowing of the predictor universe. Any model that removes/replaces that component must be separately versioned prospectively before skill interpretation.

## NTSB AVALL descriptive audit
The AGGIORNA #25 `ntsb-derived` artifact was recovered and audited. For Boeing-commercial airplane rows in 2010-2025, 1,250 of 1,358 rows recover an official sequence phase from `Events_Sequence` (92.05%); among rows with sequence data the result is 1,250 of 1,252. These descriptive results do not make historical predictor values PIT-admissible.

## G4 — BLOCKED
G4 remains downstream of G1-G3. No candidate-vs-baseline model-skill claim is allowed while upstream gates are blocked. The latest verified final audit keeps `scientific_fit_ready=false`, `scientific_promotion_ready=false`, absolute accident probabilities disabled and validated-prediction claims disallowed.

The committed automatic-cycle 1.0 implementation added the first frozen machine-readable cycle contract, content-addressed training snapshots, fail-closed parameter fitting, a 90-day discrete first-event distribution, probability of no event in the horizon, modal date, conditional 80% interval and an exposure-only temporal baseline on the identical future exposure path. The current local cycle 1.1 extension preserves 1.0 and adds estimator refitting inside every historical fold, reproducible Gamma-posterior parameter-uncertainty bands and content-addressed append-only candidate forecast records that deduplicate identical scientific inputs. Paired temporal evaluation rejects unverified outcomes, non-future outcomes and unequal horizons, and uses full-horizon logarithmic score including right censoring. This completes the internal executable architecture, not real G4 evidence. The executable `minimal_shrunk_hazard_v1` remains explicitly a candidate estimator and is not relabelled as the complete model 1.2 contract.

## Public/privacy/licensing state
Public UI must keep experimental/status boundaries. NTSB AVALL and FAA SDR remain supporting/descriptive sources with scope limits. The public repository contains no private user data or credentials. No new ICAO API retrieval is permitted. PR #1 remains closed without merge.

## Complete public pages — workflow-verified and deployed

Branch `site/complete-observatory-pages-20260906` completes the bilingual public
observatory without changing scientific semantics. It adds a dedicated F-002
dossier generated from the canonical frozen record, exposes descriptive
geography plus explicitly unsupported operator/MSN, and retains automatically
refreshed NTSB/FAA similarities as non-scoring context. Validation now displays
the separate BSFM-PD 1.3 candidate-vs-baseline scores and the frozen 3/10
event-bearing-fold shortfall. Methodology documents the automatic refit,
time-distribution, uncertainty and version-control contract while keeping BSFM
1.2, `minimal_shrunk_hazard_v1` and BSFM-PD 1.3 distinct. Provenance exposes the
source boundaries and core machine-readable public artifacts.

Local verification completed with **232 tests**, forecast-registry verification,
foundation audit and final audit passing. AGGIORNA #31 repeated the integrated
checks successfully and deployed the five-page observatory plus generated F-002
projection. Scientific gates remain unchanged: historical G1 v1 is 14/16
BLOCKED, global G2/G3/G4 are BLOCKED, the public-data result remains
negative/underpowered, and absolute probabilities remain disabled. F-002 stayed
byte-identical.

## Operational state
AGGIORNA #33 is the latest successful full operational workflow. It refreshed FAA SDR and NTSB AVALL state, executed cycle 1.1, repeated the BSFM-PD 1.3 negative/underpowered backtest, issued the first BSFM-PD 1.4 forecast, committed auditable state and deployed the complete GitHub Pages observatory. Every workflow step succeeded, including both test/audit phases, artifact upload and Pages deployment. The public cycle remains blocked on the global BSFM 1.2 scientific gates; BSFM-PD 1.3 remains blocked for insufficient event-bearing folds and lack of candidate superiority. F-002 remains byte-identical to the PR #2 integration blob. The temporary research workflow remains absent.

The global automatic-cycle 1.1 remains fail-closed with `scientific_fit_gate_closed`. The separate BSFM-PD 1.4 path is permitted to issue explicitly unvalidated prospective records from its public-data contract; that issuance does not open global G2/G3/G4.

## BSFM-PD 1.4 public-online prospective cycle — CI-verified checkpoint

PR #4 from branch `research/public-online-prospective-20260906` was
squash-merged into `main` as
`eaa1e4cd367790b02fa10a96cba8c77b1d2f7d04`. It adds a separately registered
operational path using only public online evidence. It does not
modify F-002, BSFM 1.2, historical G1 v1 or the negative/underpowered BSFM-PD
1.3 result. Contract hash
`sha256:35868ea7b54ea60d6341a0cdcf0de70831ef113a6d0edf43e28de78dd9d0e2a5`
freezes target, scope, nine cohorts, minimal estimator, T-100 exposure rule,
90-day non-overlapping cadence, baseline, scoring, uncertainty and claim limits.

The executable cycle now:

- admits only verified authority outcomes public by the cutoff and conservatively
  lag-eligible T-100 exposure;
- refits the minimal candidate and pooled exposure baseline automatically;
- produces a complete frozen time-to-first-event distribution, modal date,
  conditional 80% time interval, conditional family distribution and parameter
  uncertainty;
- retains at most one active non-overlapping forecast and writes immutable,
  content-addressed `PD14-*` records;
- scores expired records candidate-vs-baseline only when competent-authority
  coverage is demonstrated through the observed first event or horizon end;
- requires ten event-bearing prospective forecasts, candidate superiority and a
  positive lower 90% paired-bootstrap improvement bound before the frozen
  evidence threshold can pass; crossing it still requires an explicit promotion
  decision and never silently enables absolute probability claims.

AGGIORNA #33 issued the first post-contract record,
`PD14-20260907-7fa7c48bc555`, at `2026-09-06T13:51:19Z`. Its cutoff is
2026-09-06 and its non-overlapping 90-day horizon is 2026-09-07 through
2026-12-05. The modal date is 2026-09-07 and the conditional 80% interval is
2026-09-15 through 2026-11-26. It uses three PIT-eligible outcomes, 135
lag-eligible annual exposure cells through 2024 and source months 2024-09
through 2024-12. Its immutable record integrity is
`sha256:bd4f05c5b90f21001274a6a6fc67da34ff2773b076f1de477237519f9e8063cc`.

The public summary exposes conditional timing/family output but no absolute
event probability. Prospective evaluation remains `BLOCKED`, with one frozen
forecast, zero scored forecasts and no authority-verified outcome coverage yet.
This is the preregistered initial state, not a software failure.

Local verification completed with **241 tests**, forecast-registry integrity,
foundation audit and final audit passing. These checks verify implementation,
not predictive skill. Global G1 remains 14/16 BLOCKED; global G2/G3/G4 remain
BLOCKED; BSFM-PD 1.3 remains negative/underpowered. Online authority monitoring
can fail closed and requires positive coverage evidence: automation cannot infer
“no event” from zero rows.

Temporary read-only Research CI run #24 (`34033044616`) completed successfully
on SHA `3edd6fcc522848ba73f6e4902e113eb164a88a55`. It repeated the full test suite,
forecast-registry verification, foundation audit and final audit. The temporary
workflow was then removed, restoring the single-workflow invariant before merge.

Additional global exposure and historical PIT precursor data are registered as
a value-of-information hypothesis. They would make richer components and a
paired comparison testable, but no improvement is claimed before the frozen
future score and uncertainty support it.

## Workflow-verified public-data result

PR #3, branch `research/public-data-t100-20260906`, was squash-merged into
`main` as `f36da9fa82f21f85debfc5a686a7fbf32301caec`. It is locally verified but
has now also passed the full AGGIORNA #30 workflow and its public validation
card/data are live.

A separate T-100 aggregated-data adapter and draft public-data model decision
have been added locally. They preserve performed-departure counts, require
explicit DOT aircraft/service-class allowlists, label coverage as
`us_linked_commercial`, and make global G2 promotion impossible. This work does
not adopt a new model, change F-002, open G2/G3/G4 or alter the last
workflow-verified baseline. Local verification completed with 225 tests,
forecast-registry verification, foundation audit and final audit passing. The
scientific gates remain correctly closed. Official T-100 data/support-table
acquisition and workflow verification remain outstanding before adoption. The
official current DOT aircraft/service-class lookups and the NTL-preserved 2021
support-table archive were downloaded and hashed. The reviewed candidate mapping
keeps mixed code 615 unmapped because it crosses 737-Classic/737-NG; code 612 is
time-bounded to NG for the closed 2010-2025 interval and must be reviewed again
for later intervals.

The complete official 2010-2025 T-100 extract set has now been acquired into
temporary non-repository storage and reduced to a redistributable hash/provenance
audit. It contains 56,637,727 deterministically mapped Boeing performed
departures and only 14 mixed-code-615 departures. The original separate
Classic/NG design therefore stays fail-closed. A lossless nine-cohort regional
candidate merging `737-Classic+NG` passes the structural regional matrix audit,
and has now been adopted only for the separately versioned BSFM-PD 1.3
construction. Neither result opens global G2.

A final public-source review considered Eurostat flight-stage data, OpenSky
historical/scientific datasets, EUROCONTROL material and national UK/Australia/
Japan statistics. Each is valuable for regional reconciliation, but none supplies
a compatible free global 2010-2025 Boeing cohort performed-flight denominator;
a mosaic would introduce unresolved overlap, scope and coverage gaps. The user
therefore authorized proceeding with the available public data. BSFM-PD 1.3 is
now separately preregistered for prospective construction with U.S.-linked scope,
nine cohorts including `737-Classic+NG`, the minimal shrunk-hazard estimator and
an exposure-only pooled baseline. It explicitly excludes the unfulfilled BSFM
1.2 components rather than relabelling the minimal estimator as model 1.2.

The BSFM-PD 1.3 geographic foundation is now complete locally. The route ledger
authority-reconciles all 38 historical candidates: three operated segments have
a United States endpoint (Asiana 214, Southwest 1380 and Atlas 3591), while 35
do not. The three admitted outcomes have verified conservative PIT publication
bounds. This does not modify or retroactively resolve historical global G1 v1.

The T-100 audit now preserves the complete 2010–2025 monthly nine-cohort matrix
(1,728 cells; zero-filled where the source has no qualifying departures) as well
as the annual matrix. BSFM-PD 1.3 freezes a same-calendar-month seasonal-naive
future exposure rule with a conservative 365-day admissibility lag and uniform
within-month allocation. These daily inputs are deterministic assumptions, not
observed daily traffic.

The local exploratory temporal backtest executed 52 non-overlapping 90-day
folds. Only three folds contain an observed target event, below the frozen
minimum of ten, so predictive validation is BLOCKED. The candidate mean log
score is 0.4991095350 versus 0.4968174063 for the pooled exposure-only baseline,
an improvement of −0.0022921287: the candidate is not descriptively better.
No methodology may be changed post hoc to reverse this result. This is a
scientific negative/underpowered result, not a software failure and not evidence
about BSFM 1.2.

## Public-data extended-training feasibility — completed, not promoted

The official online-only acquisition path was extended backward through 1990.
The hash-bound BTS audit covers 36 annual archives, 324 annual and 3,888 monthly
nine-cohort cells, 133,799,417 mapped performed departures and zero invalid
rows. It remains a U.S.-linked denominator and cannot open global G2. The
official NTSB Pre-2008 and current AVALL downloads produced privacy-minimal
discovery sets of 99 and 53 broad candidates; 20 pre-2010 rows were selected
only as an incomplete target/route scenario and combined with the three already
reviewed BSFM-PD outcomes.

The exact older NTSB bytes have a conservative public snapshot bound of
2026-09-06, so their present-day fields are not admitted into historical
training cutoffs. The resulting 1990–2025 audit contains 137 non-overlapping
folds and 15 event-bearing folds, but it diagnoses priors rather than learning
from those older outcomes. Under the frozen BSFM-PD prior the apparent mean
log-score improvement is +0.1130865826 (paired 90% bootstrap interval
+0.0475368234 to +0.1824773010). This is not skill evidence: assigning the
same prior separately to nine cohorts gives the candidate nine times the total
pseudo-events and pseudo-exposure of the pooled baseline.

When total prior mass is matched, the improvement reverses to −0.0163818330
(90% interval −0.0330389484 to +0.0017098171). An explicitly invalid
administrative-approval-date counterfactual suggests that verified historical
publication evidence could have value, but administrative dates do not prove
public availability and the exercise is now post-hoc. The machine-readable
decision is therefore `DO_NOT_PROMOTE`: BSFM-PD 1.4 and its active forecast are
unchanged, and any balanced-prior or enlarged-history successor requires a new
preregistered model version plus genuinely future evidence. Full method and
claim limits are recorded in
`docs/PUBLIC-DATA-EXTENDED-TRAINING-FEASIBILITY.md`.

PR #5 on branch `research/public-data-extended-training-20260906` preserves this
audit. Temporary read-only Research CI run #26 (`34042331486`) completed
successfully at research SHA
`5052843751a7f74b2c7735049da0f48b5852f676`: 246 tests passed, forecast-registry
integrity passed, and both foundation and final audits completed while retaining
the scientific blockers. The temporary workflow was then removed to restore the
single-workflow repository invariant before integration.

## Exact next step / external dependencies
Keep the active `PD14-20260907-7fa7c48bc555` record immutable and accumulate
genuinely new competent-authority outcome coverage. AGGIORNA must retain this
forecast until its horizon ends; score it only when coverage is verified through
the first target event or 2026-12-05, then issue the next non-overlapping record.
Do not run repeated updates as a substitute for new evidence. Keep global BSFM
1.2 blocked pending lawful OAG/Cirium/IATA WATS exposure and FAA PIT-release
evidence. The post-#33 seed-state correction and extended-training audit must be
repeated by the next AGGIORNA verification run after integration.

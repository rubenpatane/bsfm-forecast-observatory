# BSFM Project State

Updated: 2026-09-08

## Time-to-event model selection checkpoint — 2026-09-09

Added `bsfm/time_model_selection.py`, `bsfm/discrete_hazard.py` and their machine-readable result
`data/model/time-model-selection-v1.json`. A leave-one-out diagnostic over the
35 historical cases compared uniform, month-smoothed and circular-kernel
calendar distributions. Uniform was best by mean log loss (5.900); the best
shrunk hazard (alpha 140) scored 5.971; every candidate had zero exact-date
hits. The repeated July dates are therefore an artifact of the earlier proxy
curve and are not retained as a valid date forecast. The hazard implementation
is now unit-tested but not promoted. This does not open G2/G3/G4.

A labelled EuroNOVA/IATA proxy-shape sensitivity was also scored. Its best
hazard candidate had leave-one-out log-loss 6.006 and rolling-origin log-loss
5.994, both worse than uniform; one exact-date hit is not evidence of skill.
Full local test suite after this change: **216 passed**. No scientific gate was
opened and no frozen forecast was modified.

The public US DOT daily departures table was downloaded and schema-checked;
823 domestic-commercial daily rows covering 2020-01-01 through 2022-03-26
were reduced to `data/exposure/us-dot-daily-departures-derived-v1.json` with a
source hash. Used as a temporal-shape sensitivity, its hazard scored 5.973
leave-one-out and 5.932 rolling-origin, still worse than the uniform baseline
(5.900), so it was not promoted and cannot open G2 because it has no Boeing
type resolution.

## Revised time-target decision — 2026-09-09

The development target is revised prospectively for the next model iteration:
estimate the narrowest calibrated time window (7, 14, 30, 60 or 90 days), not
an exact day. A modal day may be shown only as secondary information. Window
selection must use the 35-case leave-one-out and rolling-origin comparison,
with coverage and proper scoring reported; no official forecast is promoted by
this decision.

The uniform temporal baseline was materialized for all 35 control cases in
`data/model/control-comparison-35-uniform-baseline-v1.json` and
`docs/MODEL-1.5-CONTROL-35-UNIFORM-BASELINE.md`. It intentionally reports no
modal day and only the full calendar-year window; family/phase values remain
separate exploratory outputs.

Public-source search identified the OpenSky 2019–2020 scientific flight
dataset as a candidate daily aircraft-type sensitivity. Its documented
coverage and fields are recorded in `data/exposure/opensky-covid-public-coverage-v1.json`
and `docs/G2-OPENSKY-COVID-PUBLIC-COVERAGE-v1.md`. It is receiver-coverage data,
not a global operated-flight denominator, so G2 remains closed; immutable
download, licence verification and a leakage-free 35-case sensitivity test
remain outstanding.

Exact next step: implement the exposure-offset hazard candidate and compare it
against the uniform baseline only after its input denominator and PIT status
are explicitly recorded.

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

### Readable Model 1.5 test output — 2026-09-09

Added a public, read-only Model 1.5 test card to the existing overview page. It
loads the versioned 365-day replay status, shows cutoff, relative modal date,
horizon and comparison target, and explicitly labels the result as an
unpromoted test with no absolute probability. This is presentation wiring only:
it does not alter F-002, training inputs or gate status. Full suite: 255 passed.
G2/G3/G4 remain BLOCKED.

Exact next step: acquire a lawful exposure extract with historical availability metadata and run the existing PIT and rolling-origin admission audits.

### Public-source follow-up search — 2026-09-09

A targeted review of official EUROCONTROL and ICAO/BTS material found no new
freely downloadable, continuous global Boeing family-by-day denominator. ADRR
continues to describe detailed research flight data but requires OneSky access
and has sampled coverage/terms constraints; BTS remains a US regional source
with aircraft-type fields at different table scopes. No source was admitted,
and no model, forecast or gate status changed.

Exact next step: acquire a lawful exposure extract with historical availability metadata and run the existing PIT and rolling-origin admission audits.

### Model 1.5 cutoff replay — 2025-01-31 — 2026-09-09

Ran a new development training replay using only 13 eligible events available
by 2025-01-31. The 365-day kernel-30 temporal layer selected 2025-08-05 as its
relative modal date. The known post-cutoff events AI171 (2025-06-12) and ACT747
(2025-10-20) were both inside the horizon, at -54 and +76 days from the modal
date respectively; neither was an exact-date hit. Artifacts are
`data/model/model-1.5-trained-cutoff-20250131-v1.json`,
`data/model/model-1.5-cutoff-20250131-comparison-v1.json` and the human table
in `docs/MODEL-1.5-CUTOFF-20250131-COMPARISON-v1.md`. This remains a scoped
development test: no absolute probability, promotion or gate change, and all
frozen forecasts are unchanged.

Exact next step: acquire a lawful exposure extract with historical availability metadata and run the existing PIT and rolling-origin admission audits.

### Derived exposure sensitivity — 2026-09-09

Executed the existing `bsfm.hybrid_exposure` reconstruction. It maps the
EuroNOVA 2022 daily family shape onto IATA annual family totals and produced
365 dated cells in `data/model/hybrid-daily-exposure-sensitivity-v1.json`.
The artifact is explicitly `proxy=true`, `global_observed=false` and
`development_sensitivity`; no values were imputed as observed global traffic.
The existing regression test and full suite pass (**255 tests**). This path is
available for sensitivity experiments only and does not open G2/G3/G4.

Exact next step: run a preregistered sensitivity replay with this derived path and report its divergence from the uniform and regional candidates without promoting it.

### Feasibility exposure ensemble — 2026-09-09

Added `bsfm.feasibility_exposure`, which merges observed and derived daily
cells while preserving a provenance tier and confidence weight. It never
converts missing traffic into observed zeroes and always returns
`global_denominator=false`. A 2022 feasibility artifact contains 31 observed
OPDI days and 334 explicitly derived days:
`data/model/feasibility-exposure-ensemble-2022-v1.json`. This is suitable for
the requested feasibility experiment and sensitivity comparison only; it does
not open G2/G3/G4. Full suite: **256 tests passed**.

Exact next step: run a preregistered sensitivity replay with this tiered ensemble and report its divergence from uniform and regional candidates without promoting it.

### Feasibility replay comparison — 2026-09-09

Executed the tier-aware feasibility replay for the covered 2022 horizon after
the 2022-01-31 cutoff. Uniform, regional-derived and tiered-ensemble paths all
remain relative sensitivities; the latter two selected 2022-07-06 as the modal
date, while uniform has no informed date (first future day is used only as a
deterministic tie-break). Results are in
`data/model/feasibility-replay-comparison-2022-v1.json`. This is not G4
validation and does not open any gate. Full suite: **257 tests passed**.

Exact next step: extend the tier-aware replay across every available observed month and compare date/window scores without promoting the proxy path.

### Pre-cutoff candidate selection — 2025-01-31 — 2026-09-09

Selected the temporal candidate using only the 33 historical events at or
before the 2025-01-31 cutoff. Leave-one-out log loss selected the uniform
calendar distribution (5.900), ahead of kernel-90 (5.920) and kernel-60
(5.939); the selected modal date is therefore the deterministic first future
day, 2025-02-01. AI171 and ACT747 remain held-out comparisons at +131 and
+261 days. Artifact: `data/model/model-1.5-precutoff-selection-20250131-v1.json`.
This result demonstrates that forcing a concentrated date to reach a target
percentage would be post-hoc overfitting; no absolute probability or gate was
changed and frozen forecasts are unchanged.

Exact next step: extend the pre-cutoff candidate selection to tiered exposure and calibrated windows, retaining the same leakage-free selection rule.

### Full data utilization audit — 2026-09-09

Audited the feature registry, 35-case PIT signals, exposure assets and derived
paths. The machine-readable audit is
`data/model/data-utilization-audit-v1.json`: 42,114 OPDI daily rows, 823 US
DOT temporal rows, 35 control cases, 365-day derived and tiered paths, but
zero admitted maintenance/safety PIT rows across the controls. A public-source
search added a Zenodo open traffic/CO2 dataset and the MrAirspace schedules as
research leads; both are estimated or ADS-B-derived and require field,
coverage, vintage and licence audits before use. No forecast or gate changed.

Exact next step: acquire and audit one lawful flight-level release from the new research leads, then feed only its pre-cutoff admitted fields into the tiered replay.

### Workspace raw-data audit — 2026-09-09

The workspace contains substantial raw data previously acquired and now
audited: a roughly 96 MB EuroNOVA 2022 flight-level CSV with aircraft type,
operator hash, routes and timings, plus 31,670 normalized NTSB rows (1,894
Boeing) and phase-enrichment JSONL. The EuroNOVA file is already the source of
the regional exposure sensitivity. The NTSB rows contain useful outcome,
phase, model and nonfatal-control fields, but **zero** rows carry an
`available_at` timestamp, so none can enter strict PIT predictor features for
the 2025-01-31 cutoff. The audit is recorded in
`data/model/workspace-data-audit-v1.json`; no forecast or gate changed.

Exact next step: use the raw EuroNOVA fields to build the family/operator/route sensitivity features and keep NTSB phase/nonfatal fields as outcome-side controls until publication timing is recovered.

### Raw EuroNOVA profile selection — cutoff 2025-01-31 — 2026-09-09

Used the raw EuroNOVA CSV rather than its aggregate: Boeing flight counts,
flight-hours, distance and a combined profile were evaluated. Metric and prior
strength were selected only by leave-one-out log loss on the 33 pre-cutoff
events. The best sensitivity was flight count with prior strength 20; its modal
date is **2025-05-22**. AI171 is 21 days later (inside a 30-day window), while
ACT747 is 151 days later. The result improves the descriptive window comparison
but is not an exact-date 60% result and remains regional/derived sensitivity.
Artifact: `data/model/model-1.5-raw-euronova-selection-20250131-v1.json`.
No gate or frozen forecast changed.

Exact next step: combine the raw EuroNOVA family/operator profile with the tiered exposure replay and evaluate calibrated windows on every available month.

### Scientific method review — 2026-09-09

Reviewed discrete-time subdistribution-hazard calibration and conformal
survival prediction methods. The relevant improvement is calibration of a
time-to-event distribution and prediction set/window coverage, not forcing an
exact-day hit rate. The current implementation already has a discrete hazard,
rolling-origin selection and conformal windows; the raw EuroNOVA sensitivity
now supplies additional exposure covariates. New literature leads are logged
without importing unverifiable claims or changing the preregistered target.

Exact next step: combine the raw EuroNOVA family/operator profile with the tiered exposure replay and evaluate calibrated windows on every available month.

### Family-exposure sensitivity — cutoff 2025-01-31 — 2026-09-09

Added a family-weighted daily exposure sensitivity using raw EuroNOVA aircraft
types and pre-cutoff event-family rates, with leave-one-out selection of the
exposure prior strength. The selected path (alpha 50) produces modal date
2025-07-06; AI171 is 24 days earlier and ACT747 is 106 days later. This is a
relative sensitivity, not a global denominator or exact-date 60% result.
Artifact: `data/model/model-1.5-family-exposure-selection-20250131-v1.json`.
No forecast or gate changed.

Exact next step: combine the family-weighted path with operator and route features, then evaluate calibrated windows without using post-cutoff outcomes for selection.

### Operator/route sensitivity — cutoff 2025-01-31 — 2026-09-09

Evaluated raw EuroNOVA daily operator concentration (HHI), airport breadth,
route distance mix, hours, distance and count using pre-cutoff leave-one-out
selection. Operator HHI with alpha 50 had the best pre-cutoff log loss among
these candidates (6.151), but its modal date moved to 2026-01-09 and was less
useful for the held-out events than the family-count path. This negative result
is retained; no post-cutoff tuning was performed. Artifact:
`data/model/model-1.5-operator-route-selection-20250131-v1.json`.

Exact next step: retain family-count exposure as the current sensitivity candidate and evaluate its calibrated windows across all available months.

### Calibrated family-count windows — cutoff 2025-01-31 — 2026-09-09

Applied the pre-existing 29-case rolling conformal calibration to the
family-count modal date (2025-07-06). The 50% calibrated window is
2025-03-27/2025-10-15 and contains AI171 but not ACT747 (1/2 held-out
coverage). The 80% window is 2025-02-08/2025-12-01 and contains both known
events (2/2). This is the strongest honest result currently available; it is
window coverage, not a 60% exact-date probability. Artifact:
`data/model/model-1.5-family-exposure-calibrated-20250131-v1.json`.

Exact next step: evaluate this calibrated candidate over all available historical cutoffs and report coverage and proper scores before any promotion.

### Family-count rolling-origin audit — 2026-09-09

The fixed family-count/alpha-50 candidate was tested on 25 eligible historical
rolling cutoffs. Mean absolute day error was **189.9 days**; coverage within
30/60/90 days was respectively **8% / 16% / 16%**. The candidate therefore
does not support a 60% exact-date claim and is not promoted. Artifact:
`data/model/model-1.5-family-count-rolling-v1.json`.

Exact next step: use the raw flight-hour/distance profiles only as covariates in a pre-cutoff ensemble and re-evaluate against this rolling baseline.

### Raw exposure ensemble selection — cutoff 2025-01-31 — 2026-09-09

Tested a pre-cutoff grid over flight-count, flight-hour and distance profiles
with shrinkage strengths 5–100. Leave-one-out selected count-only weights
(1,0,0) with alpha 100 and mean log loss 6.049; its modal date is 2025-05-22,
21 days before AI171 and 151 days before ACT747. Hours and distance did not
improve the pre-cutoff score, so they are retained as rejected alternatives.
Artifact: `data/model/model-1.5-raw-exposure-ensemble-20250131-v1.json`.

Exact next step: calibrate a family-count window from this selected ensemble and compare it with the rolling-origin baseline.

### Family-count rolling windows — 2026-09-09

Calibrated the selected family-count path across the same 25 rolling cutoffs.
Coverage was 8% within 30 days, 16% within 60/90 days, 24% within 120 days
and 48% within 180 days. The 60% target is therefore not supported even as a
180-day rolling window on this small historical sample. Artifact:
`data/model/model-1.5-family-count-window-rolling-v1.json`.

Exact next step: expand the independent control series and acquire longer historical exposure before retuning any date model.

### Expanded nonfatal control series — 2026-09-09

Extracted 1,528 commercial Boeing nonfatal NTSB records from the workspace
(2008-01-03 to 2026-08-15), retaining model, phase, carrier and date fields.
None has a verified `available_at` timestamp, so the series is admitted only as
an outcome/feature-quality control and is excluded from strict pre-cutoff
prediction. Artifact: `data/model/expanded-nonfatal-control-v1.json`.
The fatal target universe and frozen forecasts are unchanged.

Exact next step: use the expanded nonfatal series for descriptive signal-density checks while keeping it outside leakage-sensitive skill scoring.

### Covariate-to-hazard composition — 2026-09-09

Added `bsfm.covariate_hazard.compose`, which connects family, operator and area
rates from the hierarchical empirical-Bayes estimator with the dynamic 7/30/90
day signal multiplier. When a cutoff is supplied, every signal row must carry
`available_at <= cutoff`; missing or late timestamps fail closed. The result is
explicitly a relative development hazard and never an absolute probability.
Regression coverage raises the suite to **258 tests passed**. No forecast or
gate changed.

Exact next step: feed admitted EuroNOVA family/operator cells and any verified PIT signal rows into this composer for a cutoff replay.

### Covariate replay — cutoff 2025-01-31 — 2026-09-09

Ran the composer on 422 aggregated OPDI family/operator/area cells and the
pre-cutoff fatal labels. It produced six family profiles with relative hazard
scores; no maintenance, safety-report or nonfatal signal was admitted because
their PIT timestamps are missing. Artifact:
`data/model/model-1.5-covariate-replay-20250131-v1.json`. The replay remains a
regional sensitivity because OPDI vintage is not a strict historical global
denominator; no forecast or gate changed.

Exact next step: connect this relative profile score to the daily date layer and compare its held-out date/window output with the family-count baseline.

### Daily covariate hazard path — 2026-09-09

Added `bsfm.daily_covariate_path.build` and applied it to all 42,114 OPDI
family/operator cells, producing 180 observed dates. Each day now combines
hierarchical family/operator/area rates with its exposure and any admitted
signals; missing signals contribute zero rather than being invented. Artifact:
`data/model/model-1.5-daily-covariate-path-opdi-v1.json`. It remains a relative
regional sensitivity and cannot open G2/G3/G4. Full suite: **259 tests passed**.

Exact next step: feed this daily path into the 365-day date summarizer through an explicitly labelled derived extension and compare it with the family-count baseline.

### Covariate 365-day wiring check — 2026-09-09

The covariate path was successfully passed through the 365-day summarizer, but
the available exposure cells are dated 2022 only. The resulting modal date
(2022-01-01) is therefore a wiring diagnostic, not a valid forecast after the
2025-01-31 cutoff. It is explicitly marked `historical_sensitivity_only` in
`data/model/model-1.5-covariate-365-summary-20250131-v1.json` and is not used
for accuracy claims. This confirms the pipeline fails semantically rather than
silently shifting 2022 exposure into 2025.

Exact next step: obtain or derive a declared 2025-dated exposure path before producing a 2025 cutoff forecast from the covariate layer.

### Derived 2025 covariate replay — 2026-09-09

Shifted the 2022 seasonal exposure profile onto 2025-02-01/2026-01-31 and
ran the covariate-to-daily summarizer. Because operator/area rates are
unresolved and all extension cells are derived, the resulting hazard is nearly
flat and the modal tie-break is 2025-02-01. Artifact:
`data/model/model-1.5-covariate-derived-2025-forecast-v1.json`.
This negative diagnostic confirms that date-shifting alone adds no predictive
information; it is not used for the 60% claim or promotion.

Exact next step: obtain real 2025-dated operator/family exposure or verified PIT signals before expecting covariates to sharpen the date distribution.

### Complete Model 1.5 test output — cutoff 2025-01-31 — 2026-09-09

Consolidated all current candidate outputs (uniform, raw count, family-weighted,
operator/route, raw exposure ensemble, calibrated family and covariate OPDI)
into `data/model/model-1.5-complete-test-output-20250131-v1.json` and the
human-readable table `docs/MODEL-1.5-COMPLETE-TEST-OUTPUT-20250131-v1.md`.
The table includes modal dates and relative scores; known post-cutoff events
remain comparison-only. No absolute probabilities, gate changes or forecast
rewrites were made.

Exact next step: run the complete table through the existing site results view and retain all candidate rows for auditability.

### Frozen-training operational simulation — cutoff 2025-07-06 — 2026-09-09

Simulated a live forecast with training frozen at 2025-01-31 and operational
cutoff moved to 2025-07-06. No retraining or post-cutoff outcome was used; no
additional signal was admitted because PIT timestamps are unavailable. The
365-day relative modal date is 2026-05-22, with top dates recorded in
`data/model/model-1.5-simulated-forecast-20250706-v1.json`. This is a
development simulation only and does not alter frozen forecasts or gates.

Exact next step: render this simulated forecast in the existing results view with its training and operational cutoffs shown separately.

### Frozen-training operational simulation — cutoff 2026-08-24 — 2026-09-09

Replayed the same frozen 2025-01-31 training as of the user-specified
2026-08-24 operational date. The 365-day relative modal date is 2027-05-22;
the top-five dates and provenance are in
`data/model/model-1.5-simulated-forecast-20260824-v1.json`. No retraining,
post-cutoff outcome use, absolute probability or forecast rewrite occurred.

Exact next step: render this simulated forecast in the existing results view with its training and operational cutoffs shown separately.

### Frozen-training operational simulation — cutoff 2025-02-05 — 2026-09-09

With training still frozen at 2025-01-31, generated the operational replay as
of 2025-02-05. The 365-day relative modal date is 2025-05-22; top dates and
provenance are in `data/model/model-1.5-simulated-forecast-20250205-v1.json`.
No retraining, post-cutoff outcome use or forecast rewrite occurred.

Exact next step: render this simulated forecast in the existing results view with its training and operational cutoffs shown separately.

### Post-cutoff survival hazard — operational cutoff 2025-07-01 — 2026-09-09

Implemented `bsfm.post_cutoff_hazard.update`: frozen pre-2025 parameters are
conditioned on survival to the operational cutoff and reweighted only by the
future exposure path. It returns modal date, top five dates and 30/60/90-day
relative windows. The July 1 replay selects 2026-02-18; the 60-day relative
mass is 62.2%. This is a derived regional sensitivity, not an absolute
probability or a claim about ACT747. Full suite: **260 tests passed**.
Artifact: `data/model/model-1.5-post-cutoff-hazard-20250701-v1.json`.

Exact next step: add family-specific future exposure paths to the post-cutoff update and compare its held-out window coverage with the previous family-count forecast.

### Grouped post-cutoff survival hazard — 2026-09-09

Added `update_by_group` to combine separate frozen family/operator paths with
declared weights before conditioning on survival. It validates matching paths
and weights and preserves the relative, non-absolute semantics. Regression
suite: **261 tests passed**. No forecast or gate changed.

Exact next step: feed actual 737/747/787 future exposure paths into the grouped updater when those cells are available; retain unknown groups rather than imputing them.

## Last workflow-verified baseline
### Public-source expansion checkpoint — 2026-09-08

`docs/G2-PUBLIC-SOURCE-EXPANSION-v1.md` records 20 source groups, with explicit
priority, access, scope, licensing and unverified dimensions. New concrete
priorities include UK CAA variant-level stage flights/hours, Argentina ANAC
model-level movements and OPDI monthly observed flights. Discovery is not
acquisition or denominator acceptance.

The public 4TU PRC 2024 version 2 manifest and README establish CC BY 4.0 and
match the existing CSV's size and publisher MD5. The append-only
`data/exposure/euronova-release-reconciliation-v1.json` supersedes the earlier
release/licence uncertainty; it does not resolve the incompatible older
86,420-row Boeing aggregate. PRC remains a selected Europe-linked sample.

`data/exposure/opdi-flight-list-manifest-v1.json` preserves 48 official monthly
download links for 2022–2025, with acquisition=false and unknown byte hashes.
Dataset-specific terms and coverage must be audited before use. A small CAA
2024 CSV was downloaded temporarily and its actual schema inspected alongside
the official PDF notes; reuse terms and full historical continuity remain open.
Airservices access and Eurostat/Statistics Canada granularity claims are
qualified in the expansion report to avoid overstating public availability.

Read-only public downloads succeeded via permitted network execution after
the earlier sandbox DNS failure. No remote Git/workflow refresh was performed,
so workflow baselines below remain unchanged. New records are uncommitted and
not workflow-verified. JSON/manifest/hash consistency checks and diff whitespace
checks passed. No code behavior changed in this research batch; earlier test
results are not claimed as a new full-suite run. G2 remains BLOCKED,
baseline_present=false; G1/G3/G4 and frozen forecasts remain unchanged.
No push, merge, publication, private-account access or ICAO API retrieval occurred.

### Local G2 resumption checkpoint — 2026-09-08

This checkpoint supersedes stale operational claims below, which describe the
older research branch baseline. Git access and worktree read/write permissions
were checked before edits. Active branch `research/privacy-safe-rebuild-20260905`
is at `4ca70d1`, one commit ahead of its recorded upstream, with pre-existing
untracked EuroNOVA inputs. No branch switch, merge, push or publication occurred.

Local `main` is `4bc73d3df3410fdaaddf3dbf9f874ae07a0bfec6`. Its project state
documents AGGIORNA #34 from source
`fcc1b8e35129ab9ba7f8b0b13b1934d4d9ba0b3c`, generated commit
`548bfe6658c41b3fbac4d05b56f9af1477b30b69`, and G1
`CLOSED_WITH_LIMITATION`. Those newer changes are absent from this research
checkout and were not transplanted. Remote workflow freshness could not be
verified because the public GitHub API hostname did not resolve. #25 below is
the older branch baseline, not an independently verified latest remote run.

The new local, uncommitted EuroNOVA audit is documented in
`docs/G2-EURONOVA-LOCAL-AUDIT-v1.md`. The unchanged CSV has 527,162 rows,
123,186 mapped Boeing observations, 365 dates in 2022 and no invalid required
observations or duplicate flight IDs. Its hash and counts disagree with the
unchanged earlier aggregate (86,420 Boeing rows). The separate audit records
this discrepancy without rewriting either input. Acquisition provenance and
data redistribution rights remain unverified; all new evidence is local and
not approved for publication. The regional sample cannot open global G2.

Local verification: 10 targeted EuroNOVA/importer tests passed, forecast registry
integrity OK, and F-002 is byte-identical to local main. No full-suite or new
workflow verification is claimed. The bundled Python lacked pytest; targeted
tests executed successfully with the available system Python. G2 stays BLOCKED
and baseline_present=false; no G1/G3/G4 or frozen forecast changes were made.
The existing `4ca70d1` commit remains unverified by a workflow in this session.

### Older research-branch baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #25 (`33978802087`) completed successfully on source SHA `971cdd6a1ec0576208191e2d18fe76fce2742c86`; it remains the latest full operational/workflow-verified baseline.
- The generated-state commit on `main` is `ce33ea54b36613cf122e3201c2825a329700f656` and uses privacy-safe Git metadata.
- No new ICAO API retrieval is permitted. Frozen historical ICAO evidence is cross-check material only.
- Workflow/software success verifies only executed checks; it does not establish predictive validity or open a scientific gate.

## F-002
`forecasts/F-002.json` is frozen. Its target string is `next_fatal_accident_involving_boeing_commercial_jet`; the forecast object contains no explicit hostile/unlawful-action or missing-aircraft inclusion/exclusion clause. Later research must not silently add one.

F-002 remains byte-identical to `main` on the active research branch (blob `eb55a77210d2fd254483ff74c3d02fcd60c1f0ad`) and is not part of PR #2's diff.

## Prospective Target Taxonomy v2 — ADOPTED
Option B was selected on 2026-09-06. `docs/TARGET-TAXONOMY-v2-PROSPECTIVE.md` and `data/census/prospective-target-taxonomy-v2.json` define target semantics for future forecasts created after adoption.

The v2 primary target is a fatal aviation **safety accident** involving a Boeing commercial jet. Officially classified deliberate hostile/security/unlawful-interference events are excluded from the primary target and retained in a parallel descriptive census. Missing aircraft remain `PENDING_MISSING` until competent-authority evidence establishes accident/equivalent fatal loss plus attributable fatality. External/ground/other-aircraft fatalities remain eligible when authoritatively attributable.

This taxonomy is explicitly non-retroactive: it does not apply to F-002, historical G1 v1, MH370, MH17 or PS752. Any future historical study using v2 must be separately versioned and re-adjudicate the full interval symmetrically.

## Current research branch and verification
Draft PR #2, branch `research/privacy-safe-rebuild-20260905`, is the privacy-safe reconstruction of post-#25 research. It was created from current `main`; it does not import the commit history of closed PR #1.

The latest successful read-only Research CI run is `34000757503`, verified at research SHA `c5cc3e63a1a21605ee416f971fbe1d1cf8493bdd` before removal of the temporary workflow. It executed:
- full `pytest -q`: **188 passed**;
- `python -m bsfm.cli verify`: forecast registry integrity OK;
- `python -m bsfm.cli audit-foundation`: completed successfully;
- `python -m bsfm.cli audit-final`: completed successfully.

The temporary research workflow was subsequently removed, restoring the single-workflow repository invariant. The verified final audit still reports historical G1 incomplete, `baseline_present=false`, `point_in_time_availability_verified=false`, `leakage_free=false`, scientific fit readiness false and scientific promotion false. This is software/audit verification, not scientific validation.

The public validation surface has now been completed on the research branch. `site/data/research-state.json` exposes the fail-closed annual G1 state, and AGGIORNA is wired to regenerate it before publication. The bilingual validation page displays the historical G1 reconciliation and formalized exclusions, the separate 35/35 outcome-publication ledger, the fixed G2 no-proxy rule, the model 1.2 `faa_sdr_precursors` obligation and the distinction from the minimal shrinkage estimator. Desktop/mobile browser checks passed, including language switching, generated-data loading, responsive navigation and absence of horizontal overflow. The full local suite passed with 188 tests plus registry verification and both scientific audits; this page batch has not been run through AGGIORNA and does not change any scientific gate.

## G1 — RECONCILED, 16/16 annual cells reconciled under formalized exclusions
`data/census/year-ledger.json` is the canonical 2010-2025 annual ledger. A cell passes only if all six controls are true: annual source scope demonstrated; all fatal jets mapped; Boeing target membership mapped; competent authority per candidate; independent reconciliation; target taxonomies resolved.

Reconciled 6/6 cells: 2010, 2011, 2012, 2013, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024 and 2025.

The integrated G1 census reports 38 candidate rows, 35 included qualifying rows, no missing candidate IDs, no extra candidate IDs, no duplicate candidate IDs and no ledger/evidence consistency errors.

The historical boundary cases are now explicitly excluded from the primary target under `docs/TARGET-TAXONOMY-HISTORICAL-FORMALIZATION-v1.md`: MH370 under the missing-aircraft rule, MH17 and PS752 as hostile/unlawful/security acts. They remain in the descriptive census. Historical G1 is reconciled at 16/16 under this declared rule. F-002 remains frozen and unchanged.

## G2 — BLOCKED; acquisition path is now executable
A complete defensible global Boeing family/year exposure denominator for 2010-2025 is still missing. The required cohort universe remains `727`, `737-Original`, `737-Classic`, `737-NG`, `737-MAX`, `747`, `757`, `767`, `777`, `787`.

Public discovery has not produced a complete compatible source. Historical IATA Safety Report Annex 4 data provide model-level sectors through 2019, but no compatible public bridge for the full later interval has been demonstrated. Aggregate Boeing or all-737 traffic cannot be disaggregated by proxy.

The highest-priority lawful commercial candidates are now OAG Historical Flight Data, Cirium Historical Flight Status/Schedules and IATA WATS Global. `data/exposure/source-inventory.json` records their current status; OAG and Cirium appear technically capable of exposing historical flight/equipment information, but no licensed BSFM extract has yet been inspected and their exact operated-flight scope, cargo/charter coverage, equipment resolution, vintage semantics and licence constraints must be audited.

`bsfm/exposure_import.py` now provides a vendor-neutral ingestion/acceptance surface for a future lawful extract. It requires one standardized row per flight leg with `flight_date`, `equipment_code`, `leg_id`, `operated`, `scope` and `vintage_id`; counts only explicitly operated `global_commercial` rows; maps only deterministic allowlisted equipment; rejects invalid/conflicting duplicates and unknown equipment; and runs the canonical full cohort-year matrix audit. No convenience allocation or fleet-share split is permitted.

Therefore the remaining G2 blocker is primarily **lawful source access plus product-scope validation**, not missing importer code. `baseline_present=false` remains mandatory until a full accepted matrix exists.

### Public IATA reconciliation checkpoint (2026-09-08)
`data/exposure/iata-public-coverage-v1.json` records the maximum IATA evidence recoverable from public reports: model-level sectors for overlapping 2013–2019 windows and aggregate all-737 observations for 2024–2025. The canonical 2010–2025 matrix remains incomplete; 737-Original/Classic/NG/MAX cannot be separated, 2020–2023 lack a demonstrated continuous public table, and detailed WATS records require authorized access. No proxy split is applied; G2 remains `BLOCKED` and `baseline_present=false`.

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

## Public/privacy/licensing state
Public UI must keep experimental/status boundaries. NTSB AVALL and FAA SDR remain supporting/descriptive sources with scope limits. The public repository contains no private user data or credentials. No new ICAO API retrieval is permitted. PR #1 remains closed without merge.

## Operational state
AGGIORNA #25 remains the latest successful full operational workflow. PR #2 remains Draft / **do not merge yet**. G1-G4 remain BLOCKED. The research branch is software-verified through Research CI `34000757503` with 188 tests passed, and the temporary workflow has been removed.

### Autonomous G2 checkpoint — 2026-09-08

The official Argentina ANAC 2021–2025 CSV resources were acquired from the public CC BY 4.0
catalogue and audited locally. The artifact is
`data/exposure/anac-argentina-2025-audit-v1.json`: 357,800 movement rows,
and corresponding artifacts cover: 2021 44,243 rows / 3,450 737-NG
departures; 2022 91,395 / 13,279 737-NG; 2023 179,324 / 26,618 737-NG plus
one 737-Original; 2024 320,410 / 45,488 737-NG and 7 Classic; 2025 465,227 /
59,112 737-NG, 1,059 MAX and 88 Classic. Arrivals are excluded to avoid
double-counting movements. The source remains regional, includes
non-commercial classes, and does not establish the global denominator; G2
remains BLOCKED and baseline_present=false.

The adapter and one regression test were added. Verification completed with 11
targeted tests, forecast registry integrity OK and clean diff whitespace. No
AGGIORNA, push, merge, publication, private access or new ICAO retrieval was
performed. The downloaded raw CSV remains outside the repository; only the
derived audit, public locator, license, hash and scope metadata are retained.

Full repository verification on 2026-09-08 completed with 195 tests passed after adding bundle artifact-integrity validation. The workspace still contains only public/project-safe derived audits and intentionally uncommitted research artifacts; no push, merge or publication was performed.

The five requested uses are now implemented in `bsfm/g2_regional_evidence.py` and `data/exposure/g2-regional-evidence-v1.json`: regional ledgers, non-additive reconciliation, RAB model crosswalk, quality/provenance checks and constrained sensitivity analysis. Regression coverage is 196 tests; global denominator admission remains false.

The model-1.5 optimization layer is implemented locally while retaining the existing four pages: prediction label schema, embedded model-dimension sections in overview/validation/methodology/provenance, point-in-time feature snapshot builder, fail-closed `monthly_candidate` coordinator and AGGIORNA workflow step. Current candidate run is correctly `candidate_blocked` with 0 feature rows because no normalized NTSB snapshot is present locally and upstream gates are false; frozen forecasts remain unchanged. Verification completed with 199 tests and registry integrity OK.

### Deep public-research checkpoint — 2026-09-08

A deeper search across IATA, university research, Zenodo, Hugging Face and open ADS-B projects added `docs/G2-PUBLIC-RESEARCH-LEADS-v2.md` and `data/exposure/public-research-leads-v2.json`. IATA Annex 4 is a historical global-sector lead through 2019; MrAirspace/ADSB.lol is an ODbL 2024+ observational sensitivity source; AeroSCOPE is a 2019 academic context compilation with explicit source and academic-use caveats; NGAFID on Hugging Face is CC BY 4.0 but general-aviation feature research only; ICAO Data+ Traffic by Flight Stage is the strongest official authorized-access candidate and requires a lawful subscription or extract. No bypass, private access or raw copyrighted redistribution occurred. Source inventory updated. G2 remains BLOCKED and baseline_present=false.

The lawful extract specification is now recorded in `docs/G2-AUTHORIZED-EXTRACT-REQUEST-v1.md`; it is ready to send to a provider when the user has an authorized account or contact.

### Pandemic aggregate scope decision — 2026-09-08

Option 3 was selected: 2020–2023 public global totals are retained as pandemic/recovery context only. No Boeing-family split is inferred from all-jet totals, fleet shares, deliveries or regional observations. `data/exposure/iata-post2019-public-context-v1.json` records the decision; canonical G2 remains BLOCKED and `baseline_present=false`.

### Scoped G2 acceptance — 2026-09-09

The restricted IATA baseline for 2010–2019 now passes the complete 10-year × 7-family matrix audit: 70 cells, one global-commercial scope, no missing or duplicate cells, non-negative sectors and positive annual totals. It is recorded as `PASS_SCOPED_2010_2019` in `data/exposure/g2-scoped-acceptance-report-v1.json`. The all-period G2 2010–2025 remains BLOCKED because 2020–2023 lack a compatible Boeing-family matrix and 2024–2025 are all-737 aggregate context only. F-002 is unchanged.

### Scoped G3 acceptance — 2026-09-09

G3 is now PASS for the separately versioned candidate `BSFM-1.5-SCOPED-SHRINKAGE-2010-2019`, with eligible cutoffs on or after 2020-04-30. The fixed IATA 2019 vintage is declared, all 35 G1 outcome observations have verified publication bounds, and FAA SDR/current NTSB snapshots are excluded. Evidence is in `data/pit/scoped-g3-audit-v1.json`. Canonical model 1.2 remains blocked and F-002 is unchanged.

### Model 1.5 scoped candidate — 2026-09-09

The separately versioned candidate is defined in `config/model-1.5-scoped.json` and `docs/MODEL-1.5-SCOPED-SPEC.md`. It uses the scoped IATA 2010–2019 exposure, verified prior G1 outcomes and hierarchical shrinkage; FAA SDR/current NTSB predictors remain excluded. G4 rolling-origin evaluation is required before promotion. Existing pages were not rewritten before validation, and frozen forecasts remain unchanged.

### Scoped G4 evaluation — 2026-09-09

A first rolling-origin candidate evaluation was executed from `data/model/g4-scoped-evaluation-v1.json` over five eligible cutoffs. Candidate Brier score was 0.5971 versus 0.6241 for the exposure-only baseline, so the artifact is `PASS_CANDIDATE`. The sample is small and the result is not a canonical model-1.2 validation or permission to publish absolute probabilities; promotion remains false pending broader review and page rendering updates.

### F-002 visual summary — 2026-09-09

Created `docs/F-002-VISUAL-SUMMARY.md`, a read-only visual summary of the frozen F-002 record. The repository record is Model 1.2; no separate frozen Model 1.4 record was found. F-002 remains unchanged.

### Model 1.5 point-in-time replay — 2026-09-09

A retrospective replay at the PD14 issue instant (`2026-09-06T13:51:19Z`) produced a separate Model 1.5 scoped family distribution: 737-all-variants 59.1%, 747 15.2%, 777 10.4%, 787 5.9%, 727 3.4%, 767 3.1%, 757 2.9%. The replay uses 13 admitted prior events and does not publish an absolute event probability. PD14 and F-002 remain unchanged.

### Time-to-event candidate layer — 2026-09-09

Added `bsfm/time_to_event.py` and tests. Model 1.5 now has a discrete-survival date layer that requires a declared daily exposure path. The PD14 replay artifact records a demonstrative 7 September 2026 modal date, but its daily path is explicitly marked pending source evidence; no validated absolute probability is published.

### Model 1.5 feature expansion — 2026-09-09

Added the exploratory feature registry `data/model/model-1.5-feature-registry-v1.json` and plan `docs/MODEL-1.5-FEATURE-EXPANSION-v1.md`. Candidate collection now covers exposure, aircraft identity/age, phase, system, failure mode, severity, geography, operator, maintenance and safety-report signals. Nothing is frozen or promoted by this registry; official activation still requires point-in-time, coverage, licensing and leakage checks.

### Development feature activation — 2026-09-09

Model 1.5 development configuration now activates the full candidate feature registry, including time-to-event, aircraft identity/age, phase, system, failure mode, severity, geography, route, airport, operator, maintenance and safety-report signals. Missing values remain explicit missing values; activation is exploratory and does not imply that every field is currently populated or predictive.

### Previsione test Model 1.5 — cutoff PD14 — 2026-09-09

The point-in-time replay is formally named `Previsione test Model 1.5 — cutoff PD14` and is linked to `PD14-20260907-7fa7c48bc555` for comparison only. It is not an official forecast and cannot modify PD14 or F-002.

### Model 1.5 training run — 2026-09-09

Trained the development candidate from 13 point-in-time admissible events at the PD14 cutoff. Artifact: `data/model/model-1.5-trained-20260909.json`. The trained candidate retains the 737-all-variants 59.1% family share and 7 September 2026 technical modal date under the neutral daily exposure path. Promotion remains false and frozen forecasts are unchanged.

### Development evidence bundle integration — 2026-09-09

Integrated the locally available EuroNOVA 2022 flight list into `bsfm/evidence_bundle.py` and generated `data/model/development-evidence-bundle-v1.json`: 365 daily Boeing exposure profiles from 527,162 flights, including 123,186 Boeing rows. OPDI 2024, ANAC Brazil and FAA SDR inventories are registered as enrichment sources with explicit global-denominator=false boundaries; FAA SDR remains unnormalized.

## Exact next step / external dependencies

### OPDI four-month series checkpoint — 2026-09-09

The OPDI observed exposure sensitivity now spans January 2022, 2023, 2024,
February 2024, March 2024 and January 2025. Accepted unique flights are
respectively 155,446, 154,147, 186,461, 177,774, 198,454 and 175,299;
distinct operators are 223, 208, 225, 227, 227 and 232. Each derived
artifact has deterministic family/operator/day cells and retains source size
and SHA-256 in the manifest. The observed family set is stable across all
six months (737, 747, 757, 767, 777, 787; no observed 727), including a
consecutive January–March 2024 window. This is enough for a multi-year
regional sensitivity check, but not a global denominator:
receiver coverage, OPDI scope and licensing remain explicit limits. G2,
G3 and G4 canonical gates remain unchanged.

The series audit now reports day completeness: five months are complete and
January 2023 has 27 observed days; the longest consecutive complete window is
three months (January–March 2024). This is the explicit rolling-origin
coverage bound, not a claim of global continuity.

The new precision implementation is documented in
`docs/MODEL-1.5-PRECISION-IMPLEMENTATION-v1.md`. `bsfm/prospective_hazard.py`
now composes directly observed daily exposure with fixed cohort rates and
produces survival windows while failing closed on invalid exposure. This is a
development component; global denominator and PIT blockers remain unchanged.

The OPDI adapter `bsfm/opdi_hazard_path.py` now feeds the survival component
with direct family/day observations. The 2024 regional sensitivity artifact is
`data/model/opdi-regional-hazard-sensitivity-2024-v1.json`; it reports a
30-day development window and remains explicitly non-global.

The prospective development forecast is recorded in
`data/model/model-1.5-prospective-forecast-20260909.json`: post-cutoff window
2027-07-17 to 2027-08-15, modal day 2027-08-01, no absolute event probability.

Historical replay at cutoff **2025-07-01** is recorded in
`data/model/model-1.5-replay-cutoff-20250701.json`. It admits 13 events,
excludes the later ACT747 event and all post-cutoff evidence, and predicts
2025-07-12–2025-08-10 (modal 2025-07-28); the actual 2025-10-20 event is
outside the predeclared 30-day window. This negative result is retained
unchanged and is not used to tune the forecast retrospectively.

`bsfm/opdi_series_audit.py` and `data/exposure/opdi-series-audit-v1.json`
quantify month-to-month family-share stability and operator coverage. The
artifact is explicitly regional observed sensitivity with
`global_denominator=false`, so it is eligible for development diagnostics
only.

`bsfm/evidence_bundle.py` now consumes this four-month audit and exposes it to
the Model 1.5 development bundle with the same fail-closed global-denominator
flag. The generated bundle was rebuilt and the full test suite remains green.

The bundle now also contains `data/exposure/opdi-daily-exposure-v1.json`,
with 27,571 direct daily operator-family observations across the four January
months. It is suitable for development pooling diagnostics only; no proxy
allocation is applied and the global denominator remains false.

The separate `data/model/historical-control-audit-v1.json` now audits the
NTSB-derived descriptive controls for 2010–2025: 27 fatal and 1,334 non-fatal
Boeing-commercial rows. Fatal/non-fatal classes and field presence are
reported separately; none is admitted as a predictor because historical
public availability before each cutoff remains unverified.

The five-element completion audit is now consolidated in
`docs/MODEL-1.5-FIVE-ELEMENT-COMPLETION-AUDIT-v1.md`. It records OPDI family
and operator exposure as regional development sensitivity, PIT signals as
fail-closed, historical controls as descriptive, and rolling-origin/conformal
components as development-ready but not canonical G4 validation. No forecast
or scientific gate changed.

The ICAO Data+ source audit is now explicit in
`data/exposure/icao-dataplus-traffic-stage-audit-v1.json` and
`docs/G2-ICAO-DATAPLUS-AUDIT-v1.md`: the documented product has carrier,
aircraft type and operated-flight fields, but annual international scope,
restricted access and no public daily bulk extract. It remains the highest
priority authorized G2 candidate; no denominator admission occurred.

The FAA SDR maintenance series is now summarized in
`data/model/faa-sdr-series-audit-v1.json`: 17 annual manifests and 513,787
Boeing rows are available as descriptive volume signals. They remain excluded
from PIT prediction because FAA approval/publication timing is not preserved;
`SubmissionDate` is not treated as `available_at`.

The IATA contextual safety-report ledger is now in
`data/pit/iata-safety-report-publication-ledger-v1.json`. Public bounds are
recorded for the 2021, 2022 and 2023 annual reports. These can support an
aggregate context feature only; no event-level or operator-level join is
admitted, and G3 remains blocked for the broader predictor universe.

The development evidence bundle now consumes that ledger under
`iata_safety_context`, preserving both `pit=true` for the report publication
bounds and `event_level_join=false`. This is a contextual feature path only;
no canonical predictor universe or frozen forecast changed.

`bsfm/pit_context.py` now applies the same cutoff rule programmatically: only
IATA reports with `available_at <= cutoff` are returned, and the result is
explicitly marked `context_only` with no event-level join.

The Model 1.5 development training artifact now records the OPDI daily-row
count and IATA context count under `development_sources`, while retaining
EuroNOVA as the declared daily time-to-event sensitivity. This makes source
usage auditable without silently changing the exposure denominator or frozen
forecast fields.

The requested human-readable 35-case test table is now in
`docs/MODEL-1.5-PREDICTION-TEST-35-HUMAN.md` and includes real date, predicted
date, family, predicted share and both hit flags. The leave-one-out temporal
layer has 1/35 exact-date matches (2.9%) and the family top-1 score is 54.3%;
this remains a development diagnostic, not an official date forecast.

The operating objective is now explicitly prospective: the 35 cases validate
the predeclared method, while future predictions use a frozen cutoff and are
scored only after new evidence arrives. The protocol is
`docs/MODEL-1.5-PROSPECTIVE-PREDICTION-PROTOCOL.md`; historical coverage is not
optimized post hoc by widening the window.


### OPDI two-month family/operator checkpoint — 2026-09-09

Two official OPDI v0.0.2 monthly Parquet extracts are now verified by size and
SHA-256 and reduced without publishing raw files. January 2022 contains
814,040 source rows and 155,446 accepted unique flights; January 2024 contains
1,058,992 source rows and 186,461 accepted flights. The derived artifacts
provide 186 daily family cells each and respectively 7,231 and 7,315 daily
operator-family cells, with 223 and 225 distinct operators. Both months expose
737, 747, 757, 767, 777 and 787; 727 is unobserved. Numeric flight IDs are
normalized deterministically and duplicates/missing fields are rejected.
This confirms a reproducible regional/operator sensitivity across two months,
but ADS-B receiver coverage and OPDI terms prevent treating it as a global
denominator. G2 remains BLOCKED and no forecast or gate changed.

A representative official OPDI parquet for 2024-01 was acquired outside the repository (34,795,180 bytes, SHA-256 `ed359b3ec6b8fc9d92f7c269e7201ab5b2aa318b6a50e1983f8cca32ca8026dd`). The verified Parquet schema has 1,058,992 rows and columns `id`, `icao24`, `flt_id`, `dof`, `adep`, `ades`, `adep_p`, `ades_p`, `registration`, `model`, `typecode`, `icao_aircraft_class`, `icao_operator`, `first_seen`, `last_seen`, `version`, `unix_time`; all observed version values are `v2.0.0`. The audit is `data/exposure/opdi-flight-list-202401-audit-v1.json`. Scope remains ADS-B-derived and regional/methodology-defined; terms/license are unresolved, so G2 remains BLOCKED.

A bounded public-prefix audit was completed for the official Brazil ANAC statistical-flight CSV. The server index reports a 357,795,130-byte CSV updated 2026-08-09; a 1 MiB retrieval prefix verified semicolon-delimited fields including year/month, origin/destination, nature/group of flight, aircraft-independent stage counts (`DECOLAGENS`) and model-related transport measures. Prefix SHA-256 is `5472a554648bd9d2c2300ebb9ce3ecc27fba9a963305552c1a977cac4329ea63`; no aggregate was admitted. Exact reuse licensing remains unverified and the full file is large.

OpenSky Zenodo license metadata was verified from the publisher LICENSE.txt (14,973 bytes; hashed in `data/exposure/opensky-zenodo-license-audit-v1.json`). The agreement is limited to approved non-profit research/education, internal testing/evaluation or government use and is not a general redistribution license; no flight CSV was downloaded. ADSB.lol remains index-only because its selected release exceeds 3.5 GB.

Next action: obtain a lawful representative extract/data dictionary from ICAO Data+, OAG, Cirium or IATA WATS and run the fixed vendor-neutral G2 acceptance contract; until then retain G2 BLOCKED.

The revised time-window diagnostic is implemented in `bsfm/window_selection.py`
with results in `data/model/time-window-selection-v1.json`. The 30-day
circular-kernel candidate is selected for development: it improves both
coverage and window log-loss against the uniform baseline in leave-one-out and
rolling-origin. It remains experimental and does not open G2/G3/G4.

Point-in-time signal extraction for maintenance, safety-report and non-fatal
rows is implemented in `bsfm/pit_signal_features.py`. Across the 35 controls,
the local NTSB snapshot admitted zero rows because no verified public
`available_at` dates were present. This fail-closed result is recorded in
`data/model/pit-signal-features-35-v1.json`; FAA SDR remains unavailable for
strict PIT use.

The longer annual rolling-origin audit is now implemented in
`bsfm/long_rolling_origin.py` with results in
`data/model/long-rolling-origin-v1.json` for 2015–2025 cutoffs. Fatal cases
remain the only predictive training universe; 20k+ NTSB non-fatal rows are
reported as descriptive controls and remain excluded from skill claims.

Six-point improvement checkpoint: `docs/MODEL-1.5-SIX-POINT-STATUS-v1.md`.
Family/operator partial pooling, dynamic 7/30/90-day multiplier and conformal
circular windows are implemented and tested. Real global daily Boeing exposure
and strict PIT expansion remain blocked; no scientific gate or frozen forecast
was changed. Full suite: 223 passed.

The ADSB.lol daily-release extractor is now implemented in
`bsfm/adsblol_exposure.py` and tested. It produces deduplicated observed
Boeing-family counts plus a source hash when a release is acquired. A release
artifact has not been admitted as a global denominator; coverage remains an
explicit limitation.

### Frozen replay training checkpoint — 2026-09-09

A cutoff-faithful Model 1.5 replay baseline is now frozen in
`data/model/model-1.5-replay-trained-cutoff-20250701-v1.json`, with its human
record in `docs/MODEL-1.5-REPLAY-TRAINING-FREEZE-v1.md`. Training uses only the
13 eligible fatal events and evidence available by 2025-07-01; the Hong Kong
ACT747 event dated 2025-10-20 is retained only as a future comparison target.
The unchanged replay window is 2025-07-12–2025-08-10 with modal date
2025-07-28 and 737-family top share 59.1%. This is a development sensitivity,
not an official forecast: global denominator, G2, G3 and G4 remain blocked.
The freeze policy forbids retraining or rewriting this artifact until an
explicit promotion decision; a later all-data model must be a new version.
Full test suite: 238 passed.

Exact next step: keep this replay baseline unchanged while collecting only
lawful, point-in-time evidence; promote a new all-data training version only
after the evidence and validation gates are independently satisfied.

### Future-date selection correction — 2026-09-09

The date layer no longer treats the 30-day kernel as a mandatory forecast
window. `bsfm.window_selection.future_modal_date` searches every future day in
a declared 365-day horizon (extendable to 730), using kernel-30 only as a
seasonal smoothing component. It returns the highest relative daily score and
never publishes an absolute event probability. The historical 2025-07-01
replay remains frozen and unchanged; the corrected policy applies to the next
versioned prediction artifact. Targeted tests pass.

Exact next step: run a new versioned 365-day replay prediction and inspect its
modal date before any promotion or official use.

### Unfrozen 365-day replay test — 2026-09-09

At the user's direction, a new test-only replay was generated as if the
cutoff were 2025-07-01. It searches 365 future dates rather than forcing a
30-day window. The modal date is 2025-07-31; Hong Kong 2025-10-20 is inside the
search horizon and was not used in training. Artifact:
`data/model/model-1.5-test-replay-cutoff-20250701-v3.json` and its human table
in `docs/MODEL-1.5-REPLAY-CUTOFF-20250701-V3-HUMAN.md`. This artifact is
explicitly unfrozen and experimental; no official probability or gate changed.

Exact next step: compare this unfrozen 365-day date rule against the 35-case
rolling-origin controls before choosing a production horizon.

### Future distribution output layer — 2026-09-09

Implemented `bsfm/future_forecast.py` to convert a declared daily hazard path
into a ranked modal date, top-5 dates, relative daily percentages and shortest
sets reaching 50% and 80% relative mass. The output explicitly refuses to
represent these shares as absolute global incident probabilities. Targeted and
full tests pass: 240 passed.

Exact next step: feed a verified family/day exposure path and the hierarchical
family/operator/area rates into this output layer, then run the fixed
rolling-origin comparison.

### Hierarchical daily hazard composition — 2026-09-09

The hierarchical estimator now exposes family, operator and optional area
rates with empirical-Bayes shrinkage. `bsfm/daily_hierarchical_forecast.py`
aggregates only declared, non-negative daily exposure cells into a dated hazard
path and fails closed on invalid cells. This path is ready to feed the annual
ranked-date and credible-mass output; it does not create a global denominator
or open G2. Full suite: 242 passed.

Exact next step: connect the verified OPDI daily family/operator cells to this
composer and run the rolling-origin calibration using only point-in-time rows.

### OPDI hierarchical connection — 2026-09-09

`bsfm/opdi_hierarchical.py` now fits the family/operator/area-shrinkage model
from admitted events and OPDI observed regional exposure cells. Exact operator
matches are used where present; unmatched cells remain in the pooled regional
sensitivity. The artifact is explicitly `global_denominator=false` and cannot
open G2. Full suite: 243 passed.

Exact next step: construct a dated 365-day path only from verified exposure
coverage; do not repeat or impute missing OPDI days silently.

### Annual coverage fail-closed audit — 2026-09-09

`build_covered_horizon` now requires every date in a requested horizon and
raises on missing exposure days. The OPDI audit finds 180 observed days across
six monthly extracts (2022-01, 2023-01, 2024-01..03, 2025-01), so a verified
365-day path is not available and no values were imputed. Audit artifact:
`data/model/opdi-covered-horizon-audit-v1.json`. Full suite remains green.

Exact next step: add a lawful source with continuous daily family exposure or
keep the annual hazard forecast explicitly unavailable rather than filling the
coverage gap.

### Rolling-origin date validation — 2026-09-09

Implemented `bsfm/rolling_date_validation.py`, which evaluates the 365-day
modal-date rule at historical cutoffs using only prior events. On the available
35-case control table it produced 30 eligible cutoffs with mean absolute date
error 183.17 days. This is a transparent development diagnostic and does not
support G4 or an official forecast. Artifact:
`data/model/rolling-date-validation-v1.json`. Full suite: 245 passed.

Exact next step: compare this rolling result against uniform and shorter/longer
calendar baselines, then retain the candidate only if the predeclared score
improves without post-cutoff information.

### Rolling baseline comparison — 2026-09-09

The rolling-origin comparison now evaluates uniform, kernel-7, kernel-30 and
kernel-60 under the same strict post-cutoff target rule. On 29 eligible
cutoffs, mean absolute day errors were respectively 178.93, 164.21, 161.97
and 157.52 days; kernel-60 is the current development candidate by the
predeclared lowest-error rule. This is still a small historical diagnostic and
not G4 validation. Artifact: `data/model/rolling-date-baseline-comparison-v1.json`.

Exact next step: repeat the comparison with the composed family/operator
hazard path once continuous exposure coverage exists; do not promote
kernel-60 solely from this calendar-only result.

### Rolling conformal calibration — 2026-09-09

Added `bsfm/rolling_calibration.py` and calibrated circular date windows from
29 strict rolling-origin residuals. Development radii are 101 days for 50%
relative coverage and 148 days for 80%; the wide radii honestly reflect the
current uncertainty. Artifact: `data/model/rolling-date-conformal-calibration-v1.json`.
These are conditional relative windows, not absolute safety probabilities.
Full suite: 247 passed.

Exact next step: apply these calibrated windows to the ranked future hazard
output once a complete verified daily exposure path is available.

### Calibrated readable forecast output — 2026-09-09

`attach_calibrated_windows` now connects the conformal rolling calibration to
the future hazard summary. A consumer can display modal date, top dates,
relative shares and calibrated 50%/80% date windows with their calibration
sample size. Semantics remain relative coverage, never absolute incident
probability. Full suite: 248 passed.

Exact next step: wire this combined summary into the existing results page
only after a complete verified daily exposure path is available.

### Point-in-time exposure enforcement — 2026-09-09

Daily hazard composition now accepts an explicit cutoff and requires every
exposure cell to carry `available_at <= cutoff`. Missing or late availability
metadata fails closed. This enforces the PIT rule at the forecast boundary and
keeps current OPDI rows out of historical replay unless their publication
availability is documented. Full suite: 250 passed.

Exact next step: add verified availability metadata to each admitted exposure
extract, then rebuild the rolling hazard path without bypassing this check.

### Exposure PIT admission loader — 2026-09-09

Added `bsfm/pit_exposure.py`, which admits exposure rows only when
`available_at` is present and no later than the declared cutoff. Missing or
late rows are returned in an exclusion audit rather than silently dropped or
counted. Full suite: 251 passed.

Exact next step: run this admission audit on each OPDI manifest and retain only
rows with lawful, cutoff-valid publication metadata for historical replay.

### OPDI manifest PIT audit — 2026-09-09

Applied the PIT admission loader to all 42,114 OPDI daily cells. The manifest
retrieval timestamp is 2026-09-07, so **0 rows** are admissible for a
2025-07-01 replay; all 42,114 are excluded. All rows are admissible only for a
current 2026-09-09 sensitivity, which cannot validate a historical forecast.
Artifacts: `data/model/opdi-pit-admission-2025-07-01.json` and
`data/model/opdi-pit-admission-2026-09-09.json`. This confirms the PIT gate is
working and G3/G4 remain closed.

Exact next step: acquire a source whose public availability predates each
historical cutoff, or retain OPDI only as current descriptive sensitivity.

### Objective completion audit — 2026-09-09

Added `docs/MODEL-1.5-OBJECTIVE-COMPLETION-AUDIT-v1.md`, mapping every stated
improvement to repository evidence and marking it implemented, partial or
blocked. The audit confirms the software layers are present, while a complete
365-day verified exposure path, historical PIT exposure and G2/G3/G4 remain
unresolved. It does not alter any forecast. Full suite remains 251 passed.

Exact next step: resolve the external exposure/PIT evidence gap; until then
continue only regional sensitivity tests and diagnostics.

### EUROCONTROL ADR daily exposure lead — 2026-09-09

A new official candidate was identified: EUROCONTROL's Aviation Data
Repository for Research. Its public description states a complete commercial
flight list with aircraft types, operators and dates from March 2015 onward,
released with at least a two-year delay through the OneSky research portal.
This is the strongest lead for historical daily family/operator exposure and
PIT replay, but it is not yet acquired, its network scope may not be global,
and access/reuse/vintage checks remain open. Registered in
`data/exposure/eurocontrol-adr-daily-candidate-v1.json` and
`docs/G2-EUROCONTROL-ADR-DAILY-CANDIDATE-v1.md`; G2 status unchanged.

Exact next step: obtain a lawful representative OneSky extract or public data
file, then run the fixed family/day/operator coverage and vintage audit.

### ADSB.lol-derived global schedule candidate — 2026-09-09

An additional public candidate was audited: the ODbL-licensed
`MrAirspace/aircraft-flight-schedules` repository. It publishes quarterly
Parquet releases from 2024 onward with flight date/time, ICAO aircraft type,
airline code, registration and route, derived from ADS-B. This is useful for a
post-2024 observed family/operator sensitivity and adapter testing, but it is
not a global denominator: receiver coverage, missing/duplicate tracks, absent
2010–2023 controls and release-vintage verification remain unresolved.
Registered in `data/exposure/aircraft-flight-schedules-adsblol-candidate-v1.json`;
G2/G3/G4 and frozen forecasts are unchanged.

Exact next step: acquire one lawful release, hash it and run the declared
coverage/duplicate/vintage audit before allowing it into any sensitivity path.

### ADSB.lol schedule adapter — 2026-09-09

Added `bsfm/adsblol_schedule_exposure.py` to normalize a lawful release into
daily family/operator observations. The adapter requires an origin timestamp,
operator, stable aircraft/flight key and an allowlisted ICAO Boeing type; it
records duplicates, unknown types and missing fields instead of imputing them.
It explicitly returns `global_denominator=false` and remains observed
sensitivity until release hash, coverage and publication vintage are audited.
No forecast or gate status changed.

Exact next step: run the adapter on one acquired release and retain its hash,
coverage audit and point-in-time admission result.

### ADSB.lol schedule release index — 2026-09-09

The public release page was checked and records quarterly releases from
2024-Q2 through 2026-Q2. The 2026-Q2 release explicitly reports missing or
considerably incomplete data on 5–7 May 2026, confirming that daily coverage
must be audited rather than assumed. The release index is recorded in
`data/exposure/aircraft-flight-schedules-release-index-v1.json`; no Parquet was
downloaded, hashed or admitted, and G2/G3/G4 remain unchanged.

Exact next step: acquire one permitted Parquet release, hash it and execute the
adapter plus missing-day/duplicate and PIT-vintage audits.

### ADSB.lol schedule coverage/PIT audit — 2026-09-09

Added `bsfm/adsblol_schedule_audit.py` and regression tests. The audit reports
expected versus observed days, missing dates, duplicate normalized keys and
rows unavailable by a declared cutoff. It never fills gaps and always marks
the result as observed sensitivity with `global_denominator=false`.

Exact next step: apply the adapter and audit to a downloaded release only after
its lawful acquisition and file hash have been recorded.

### EUROCONTROL ADR terms and coverage refinement — 2026-09-09

The official ADR dashboard and terms were verified. ADRR is free for approved
R&D through OneSky, but requires registration, a data request and acceptance of
terms; the terms describe four non-consecutive calendar months per year with
commercial-flight details including aircraft type and operator. Therefore ADRR
is a strong PIT-compatible sampled exposure source from 2015 onward, not a
continuous 365-day census and not automatically global. Candidate metadata and
documentation were corrected accordingly; G2 status is unchanged.

### ADRR terms audit — 2026-09-09

The EUROCONTROL ADRR Terms of Use were recorded separately. They permit
research and development after OneSky registration/request, prohibit
redistribution without written permission, and define four non-consecutive
months per year with commercial flight, aircraft type and operator details.
Artifact: `data/exposure/eurocontrol-adr-terms-audit-v1.json`. No raw data were
acquired or admitted.

### BTS TranStats regional lead — 2026-09-09

A US DOT/BTS TranStats lead was audited. Daily on-time records expose flight
 date, reporting carrier, tail number, origin and destination; T-100 segment
 tables add aircraft type and departures performed at monthly/segment scope.
It is useful for a US regional cross-check, not a global daily Boeing
denominator, and aircraft-family mapping is not directly present in the daily
table. Registered as non-admitted in
`data/exposure/bts-transtats-candidate-v1.json`; G2 unchanged.

### EUROCONTROL Data app daily aggregate audit — 2026-09-09

The official EUROCONTROL Data app API documentation was checked as an
additional public lead. It exposes daily country/network traffic aggregates,
including departures/arrivals, overflights, delay and punctuality, but does not
document a daily Boeing-family or operator breakdown and is not a global
commercial denominator. It is therefore recorded only as a possible regional
descriptive covariate in
`data/exposure/eurocontrol-data-app-daily-network-audit-v1.json`; G2/G3/G4
status is unchanged and no forecast was modified.

Exact next step: obtain a lawful ADRR/OneSky extract or another source with
verified daily family/operator cells and historical availability metadata; do
not derive Boeing exposure from these aggregates.

### ADS-B Exchange archive lead — 2026-09-09

The public ADS-B Exchange sample-data page was checked. It advertises global
airborne snapshots at five-second cadence from May 2020 (with a different
cadence for earlier data), but this does not establish bulk historical access,
complete receiver coverage, audited Boeing-family/operator fields or permitted
redistribution of derived data. It is recorded as a research lead in
`data/exposure/public-research-leads-v2.json`; no raw data were acquired and
G2/G3/G4 and all frozen forecasts are unchanged.

Exact next step: obtain a lawful, hashable historical extract with verified
family/operator cells and publication-vintage metadata, or document that no
such extract is available without access approval.

### OPDI partial-coverage sensitivity policy — 2026-09-09

Formalized `docs/MODEL-1.5-OPDI-PARTIAL-COVERAGE-POLICY-v1.md` and its machine-
readable companion `data/exposure/opdi-partial-coverage-policy-v1.json`. Model
1.5 may now run an explicitly labelled sensitivity analysis on the six
acquired OPDI periods (2022-01, 2023-01, 2024-01..03 and 2025-01), while
retaining missing months, forbidding imputation and widening or withholding
uncertainty when calibration coverage is insufficient. No gate or frozen
forecast changed; G2 and canonical G4 remain BLOCKED.

Exact next step: run the partial-coverage protocol on the 35-case control set
and publish its coverage ledger alongside the comparison, without promoting
the result to a global validation.

### Partial OPDI 35-case coverage audit — 2026-09-09

Applied the partial-coverage rule to the existing 35-case register. The
acquired OPDI periods cover **0/35 event months** in that control set; no
exposure was imputed and no forecast was rewritten. The machine-readable
ledger is `data/model/model-1.5-partial-opdi-control-35-coverage-v1.json` and
the human-readable explanation is `docs/MODEL-1.5-PARTIAL-OPDI-CONTROL-35-v1.md`.
This confirms fail-closed behavior but is not a predictive validation.

Exact next step: use the partial OPDI periods only for prospective/sensitivity
replays whose cutoff and covered dates fall inside an observed period; retain
the 35-case result as a coverage diagnostic.

### OPDI 2025–2026 monthly recovery — 2026-09-10

The public OPDI download page was rechecked and lists monthly Parquet flight
lists from 2025-01 through 2026-07. February 2025 was acquired, hashed and
normalized into `data/exposure/opdi-202502-family-operator-derived-v1.json`:
1,066,341 source rows, 173,561 deduplicated Boeing-family/operator flights,
28 observed dates, 230 operators and families 737/747/757/767/777/787. The
full public URL index is `data/exposure/opdi-2025-2026-public-index-v1.json`
and the recovery note is `docs/G2-OPDI-2025-2026-RECOVERY-v1.md`.

This remains OPDI/OpenSky ADS-B traffic in a wider-European methodology scope,
not a global denominator. The acquired file's HTTP last-modified metadata is
2026-02-23, so its historical point-in-time availability for a 2025 cutoff is
unknown and it is not admitted to G3/G4. No missing days were imputed and no
forecast or frozen record changed.

Exact next step: acquire the remaining 2025 monthly files only with lawful provenance, then audit archived publication vintage before using any row in a historical replay.

### OPDI 2025 complete monthly acquisition — 2026-09-12

Acquired the remaining public OPDI Parquet flight lists for March–December
2025 and derived family/operator daily artifacts. The combined OPDI sensitivity
now covers 17 listed months (2022-01, 2023-01, 2024-01..03 and all 2025
months), 125,364 daily family/operator cells after normalization. Monthly
source hashes and counts are stored in the derived JSON artifacts under
`data/exposure/`; original Parquet files remain outside the public repository
because redistribution terms are not yet cleared.

All 2025 files are current public downloads; their historical publication
vintage is not established for the 2025 cutoffs. Scope remains wider-European
ADS-B observed traffic, `global_denominator=false`; no imputation, forecast
rewrite or gate change occurred. Full suite: 261 passed.

Exact next step: audit archived publication timestamps and terms for each 2025 extract before admitting any row to a historical replay.

### OPDI 2025 publication-vintage audit — 2026-09-12

Checked HTTP `Last-Modified` for every 2025 OPDI monthly file. January through
November report 23 February 2026; December reports 13 April 2026. These are
current object metadata and do not prove an archived release before the
2025-01-31 cutoff. The PIT audit is
`data/exposure/opdi-2025-publication-pit-audit-v1.json`: 0/12 months admitted
for historical replay. The expanded files remain valid current descriptive
sensitivity data; G2/G3/G4 and forecasts are unchanged.

Exact next step: search for archived OPDI release snapshots or an alternative source carrying a verifiable pre-cutoff publication vintage.

### OPDI 2025 series audit — 2026-09-12

The 12 monthly 2025 derivatives were audited. Eleven months have complete
calendar-day coverage; August has 29/31 observed days. The audit is
`data/model/opdi-2025-series-audit-v1.json`. Missing August dates remain
missing and are not imputed. This is still regional ADS-B sensitivity data,
not a global denominator or PIT-admitted historical exposure.

Exact next step: preserve the missing August dates in the daily path and run a sensitivity-only hazard replay with explicit coverage flags.

### OPDI 2025 daily hazard sensitivity replay — 2026-09-12

Ran a new sensitivity replay with model parameters frozen at 2025-01-31 and
OPDI daily family exposure from 2025-02-01 through 2025-12-31. The path has
332/334 observed days; the two August gaps remain explicit. Family weights and
survival-conditioned daily hazard are applied, while operator cells remain
available for grouping. The relative modal date is 2025-08-10 (0.383% relative
share); top dates are recorded in
`data/model/model-1.5-opdi-2025-sensitivity-replay-v1.json`.

This is an observed regional sensitivity over 2025, not an absolute incident
probability, and is not PIT-admitted for the 2025 cutoff because publication
vintage is unresolved. No forecast or gate changed.

Exact next step: extend this sensitivity path with the calibrated 30/60/90-day windows and compare it against the predeclared rolling-origin baselines.

### OPDI sensitivity calibrated windows — 2026-09-12

The OPDI 2025 sensitivity replay now reports centered 30/60/90-day windows
around modal date 2025-08-10 and attaches the existing conformal calibration
(radii 101 and 148 days from 29 rolling residuals). The enriched artifact is
`data/model/model-1.5-opdi-2025-sensitivity-replay-v1.json` and remains
relative, development-only output. The predeclared rolling-origin selector
still governs method choice; OPDI cannot enter that comparison until PIT and
global-denominator criteria are met. Full suite: 261 passed.

Exact next step: keep the OPDI path as sensitivity and do not promote it until PIT vintage and denominator evidence are independently verified.

### Operator coverage audit — 2026-09-12

Compared OPDI ICAO operator codes with the frozen training event operator names
at the 2025-01-31 cutoff. OPDI contains 316 distinct operator codes across the
2025 daily cells; the training events contain seven operator names and there
are zero exact matches. The audit is
`data/model/model-1.5-operator-coverage-audit-20250131-v1.json`.
The model therefore correctly falls back to pooled family/regional rates rather
than fabricating operator effects. A licensed operator-code crosswalk or
point-in-time event coding is required before operator-specific weighting can
be admitted.

Exact next step: add a public, versioned ICAO/IATA operator-code crosswalk and rerun the exact-match audit without changing frozen parameters.

### Public operator-code crosswalk audit — 2026-09-12

Acquired the OpenFlights airline table under ODbL and audited it against OPDI
operator codes. It maps 275/316 observed OPDI codes; normalized name matching
finds 6/7 frozen training-event operators. The diagnostic is
`data/model/model-1.5-operator-code-crosswalk-audit-v1.json` and records the
source hash, license and current-snapshot limitation. This enables a candidate
crosswalk for sensitivity analysis, but historical PIT validity and ODbL
attribution/share-alike obligations must be resolved before publication or
G3 admission. Frozen parameters and forecasts remain unchanged.

Exact next step: use only the six auditable name matches in a new operator-weighted sensitivity replay, then compare it with the family-only path.

### Operator-weighted OPDI sensitivity — 2026-09-12

Built a separate operator-weighted sensitivity replay using the public
OpenFlights crosswalk for exact auditable matches only and empirical-Bayes
pooling. The artifact is
`data/model/model-1.5-opdi-2025-operator-weighted-sensitivity-v1.json`.
Only four unique OPDI codes produce usable exact name links after duplicate
normalization; all other operators remain pooled. The output is explicitly
sensitivity-only and does not alter frozen training parameters, forecasts or
G2/G3/G4 status.

Exact next step: expand the crosswalk with a historically versioned source before treating operator effects as predictive.

### Operator crosswalk adapter — 2026-09-12

Added `bsfm/operator_crosswalk.py` to load the versioned crosswalk and apply
only single exact matches; unmatched codes are explicitly marked pooled and
never guessed. Regression coverage is in `tests/test_operator_crosswalk.py`.
Full suite: 262 passed. No forecast or gate changed.

Exact next step: wire this adapter into AGGIORNA's sensitivity path after its input crosswalk is refreshed and provenance checked.

### OPDI release-vintage lead — 2026-09-12

The OPDI roadmap documents v0.0.2 release 3 on 2024-12-01 covering a
three-year period. This is useful version-level evidence before the cutoff,
but it does not prove that each current monthly Parquet object was publicly
available or immutable on 2025-01-31. The PIT audit now records this lead while
keeping all rows excluded pending object-level archival evidence.

Exact next step: obtain an archived object listing or checksum dated on/before 2025-01-31 for the January 2025 file.

### Web-archive OPDI check — 2026-09-12

Queried the public web archive CDX endpoint for the January 2025 OPDI Parquet
object; it returned no matching HTTP 200 snapshot. This is a negative search
result, not proof of historical unavailability. The PIT audit records the
query and retains the rows as not admitted.

Exact next step: retain OPDI as sensitivity unless an independently archived checksum or release manifest is found.

### Historical operator crosswalk recovered — 2026-09-12

Recovered a pre-cutoff OpenFlights `airlines.dat` from Git commit
`5d623a6969a1adee7961cf1c9a8a212c4a784713`, dated 2017-02-02, under ODbL.
SHA-256 is `39be1a432e8b04ebc12860c29281c974a9cb52169c82b2456a835d66ab1548a1`.
It maps 275/316 OPDI codes and yields six conservative event-name matches.
The artifact is `data/model/model-1.5-operator-crosswalk-historical-2017-v1.json`.
This resolves the crosswalk vintage requirement as a candidate, but does not
resolve OPDI object-level publication or global-denominator evidence.

Exact next step: retain the historical crosswalk and run the operator-weighted replay only after exposure PIT admission is independently satisfied.

### Pre-cutoff OPDI portal release recovered — 2026-09-12

The public OPDI portal Git history contains release `37fef9b78a73` dated
2025-01-16. Its generated flight-list page lists v0.0.2 monthly links through
2024-12, but not January 2025. The saved page hash and month ledger are in
`data/exposure/opdi-portal-release-202501-pit-v1.json`. This is the strongest
pre-cutoff publication evidence found: it supports 2022–2024 exposure as
public before 2025-01-31, while confirming that January 2025 itself is not
proven available by that cutoff.

Exact next step: use only the pre-cutoff-listed 2024 exposure for admissible historical training audits; keep 2025 exposure excluded from PIT replay.

### Conditional PIT admission of pre-cutoff OPDI months — 2026-09-12

Applied the 2025-01-16 portal release evidence to the OPDI 2024-01..03
artifacts. All 21,858 family/operator cells are conditionally admitted for
the 2025-01-31 cutoff in `data/model/opdi-pit-admission-release-20250131-v1.json`.
The admission remains conditional because the release page proves public
listing, not object immutability or a file checksum at that date. The admitted
months cover no complete future horizon after the cutoff, so a valid
rolling-origin daily-hazard comparison cannot yet be run from them.

Exact next step: find a pre-cutoff object checksum or a contemporaneous full daily exposure source; otherwise keep rolling-origin status not admitted.

### OPDI mirror and portal-history search — 2026-09-12

Searched exact filename mirrors, GitHub code/history, public catalogs and the
OPDI portal repository. The portal repository's last pre-cutoff release is
2025-01-16 and lists files only through 2024-12; no independent January 2025
manifest, checksum or mirror was found. The negative search is recorded in the
PIT audit. No evidence was fabricated and no gate changed.

Exact next step: stop treating January 2025 exposure as PIT-valid unless a new public archival copy appears; use the conditional 2024 path only for diagnostic replay.

### Exclusion policy for unverifiable January 2025 — 2026-09-12

Formalized `docs/MODEL-1.5-EXCLUDED-PERIOD-POLICY-v1.md`. January 2025 OPDI
exposure is excluded from training/validation because object-level PIT evidence
is missing. No zeros or interpolations are introduced. The 2024 pre-cutoff
listed months remain available for conditional diagnostics; this decision does
not open G2 or G4 and does not alter frozen forecasts.

Exact next step: run the diagnostic rolling-origin comparison on eligible pre-cutoff periods and publish its coverage ledger.

### Rolling-origin PIT admission audit — 2026-09-12

Applied the exclusion policy to the requested 2025-01-31 cutoff. The
365-day future exposure horizon has no PIT-valid rows after the cutoff, so the
candidate-vs-baseline rolling-origin run is correctly marked `not_admitted` in
`data/model/model-1.5-rolling-origin-pit-admission-v1.json`. No method was
selected or frozen from an ineligible path, and no forecast changed.

Exact next step: obtain a contemporaneous daily exposure source covering the post-cutoff horizon; then rerun the paired rolling-origin comparison.

### Diagnostic comparison of all 35 controls — 2026-09-12

Generated the complete local comparison table with real/simulated date, date
error, family, operator, phase and available failure/area fields. Artifacts:
`data/model/model-1.5-control-35-diagnostic-complete-v1.json` and
`docs/MODEL-1.5-CONTROL-35-DIAGNOSTIC-COMPLETE.md`. Mean absolute date error is
87.9 days for this pre-existing hybrid diagnostic table. It is explicitly not
published, not PIT/G4 validation and does not select a method using ACT747.
Full suite: 262 passed.

Exact next step: inspect the 35-row diagnostic table to choose data-quality fixes, not model parameters, before any admitted replay.

### Analisi casi post-cutoff — 2026-09-12

Analizzati i due soli controlli successivi al 2025-01-31: AI171 (23 giorni di
errore con la vecchia data diagnostica; 59 con la sensibilità OPDI) e ACT747
(107; 71 con OPDI). La data ripetuta 2025-07-05 deriva dal fallback ibrido; la
famiglia 737 assegnata a entrambi evidenzia il limite del pooling senza match
famiglia/operatore. Analisi completa in
`docs/MODEL-1.5-POST-CUTOFF-ANALYSIS-v1.md`. Nessun caso post-cutoff è stato
usato per selezionare parametri.

Exact next step: replace the fallback family/date layer with the operator-crosswalk and daily OPDI sensitivity path, then report unchanged post-cutoff comparisons.

### Linear relative-hazard output mode — 2026-09-12

`bsfm.future_forecast.summarize_daily_hazard` now supports an explicit
`weight_mode="linear"` for normalized relative hazard paths. This prevents
exponential saturation when OPDI flight counts are large; the prior survival
mode remains available for discrete event-probability paths. A regression test
covers the new mode. Full suite: 263 passed.

Exact next step: regenerate the OPDI sensitivity artifacts with linear mode and retain their existing coverage and non-global labels.

### Linear OPDI sensitivity replay v2 — 2026-09-12

Regenerated the OPDI 2025 sensitivity artifact with deterministic typecode to
family mapping, linear normalized hazard (no exponential saturation), explicit
survival conditioning and no imputation. Output:
`data/model/model-1.5-opdi-2025-sensitivity-replay-v2.json`. The modal date
remains 2025-08-10; the top-five ordering is stable. Operator crosswalk/pooling
remains available in the separate hierarchical path. Full suite: 263 passed.

Exact next step: compare v2 against the predeclared rolling-origin baselines as a diagnostic only; do not promote without PIT exposure coverage.

### Post-cutoff baseline comparison for v2 — 2026-09-12

Compared OPDI linear v2 with the prior hybrid and uniform baselines on the two
post-cutoff cases for descriptive diagnostics only. v2 errors are 59 days
(AI171) and 71 days (ACT747); hybrid errors are 23 and 107; uniform errors are
131 and 261. No method was selected from these cases, and ACT747 remains
excluded from selection. Artifact:
`data/model/model-1.5-post-cutoff-diagnostic-baseline-comparison-v1.json`.
Full suite: 263 passed.

Exact next step: use only pre-cutoff rolling-origin rows to select the candidate, then apply it unchanged to post-cutoff cases.

### Model 1.5 requirement integration contract — 2026-09-12

Added `tests/test_model15_requirements.py`, an integration contract asserting
frozen cutoff, deterministic typecode mapping, linear hazard, explicit missing
days, survival conditioning, 30/60/90 windows and ACT747 exclusion from
selection. Full suite: 265 passed.

Exact next step: use this contract in AGGIORNA CI and regenerate sensitivity output only when the declared source coverage changes.

### Valutazione diagnostica temporale Model 1.5 — 2026-09-12

Eseguito il confronto leakage-free sui 35 casi con leave-one-out e rolling-origin.
Il miglior log-loss leave-one-out è la baseline uniforme (5,900); nel rolling-origin
la hazard alpha-140 ha errore circolare medio 85,6 giorni, equivalente alla baseline,
mentre le forme USDOT e di esposizione ibrida risultano peggiori. Il risultato è
salvato in `data/model/time-model-selection-v1.json` e nella tabella leggibile
`docs/MODEL-1.5-DIAGNOSTIC-EVALUATION-v1.md`. È una valutazione diagnostica: non
apre G2/G4, non usa i casi post-cutoff per la selezione e non modifica forecast
congelati.

Exact next step: estendere la serie con esposizione PIT verificabile e ripetere il rolling-origin prima di promuovere un candidato.

### AGGIORNA integra valutazione temporale — 2026-09-12

Il workflow AGGIORNA ora esegue anche `bsfm.time_model_selection` dopo il gate di
training mensile, rigenerando l’artefatto diagnostico senza promuovere candidati.
Il collaudo locale completo è passato: 265 test superati. La compilazione bytecode
non è stata usata come criterio perché il sistema macOS reindirizza la cache Python
fuori dall’area scrivibile; non risultano errori di sintassi nel percorso eseguito.

Exact next step: ottenere una fonte di esposizione giornaliera con disponibilità point-in-time per completare la validazione rolling-origin ammessa.

### Replay a orizzonte osservato senza imputazioni — 2026-09-12

Creato il replay diagnostico `data/model/model-1.5-opdi-truncated-horizon-replay-v1.json`
con intervallo operativo 2025-02-01–2025-12-31. Gennaio 2026 è escluso e i due
 giorni OPDI mancanti restano dichiarati; nessun valore è stato ricavato o imputato.
La policy è documentata in `docs/MODEL-1.5-TRUNCATED-HORIZON-POLICY-v1.md`.
Il percorso consente test sul periodo osservato, ma mantiene G2/G4 chiusi perché
non costituisce denominatore globale né copertura PIT completa. Full suite: 265 passed.

Exact next step: usare questo replay troncato per il confronto diagnostico delle date e mantenere separato il futuro non osservato.

### Confronto replay troncato — 2026-09-12

Eseguito il calcolo Model 1.5 sul solo intervallo osservato fino al 2025-12-31.
La data modale kernel-30 risulta 2025-12-31 con quota relativa 0,566% e massa
osservata 82,8%; il confronto separato con AI171 e ACT747 è stato registrato
nell’artefatto `data/model/model-1.5-truncated-horizon-comparison-v1.json`.
Il risultato resta diagnostico e non modifica i gate.

Exact next step: mostrare questo confronto nella pagina diagnostica del progetto senza presentarlo come previsione validata.

### Verifica fonte OPDI gennaio 2026 — 2026-09-12

La pagina pubblica OPDI conferma l’esistenza del file `flight_list_202601.parquet`
e la copertura dichiarata fino a luglio 2026. La fonte è stata registrata nella
recovery note, ma l’acquisizione locale non è riuscita per assenza di risoluzione
DNS nell’ambiente. Il file resta candidato non acquisito e non PIT-admissible.

Exact next step: acquisire `flight_list_202601.parquet` in un ambiente con accesso di rete e conservarne hash e metadati di pubblicazione.

### Acquisizione OPDI completata, copertura gennaio parziale — 2026-09-12

Acquisiti e verificati come Parquet i file `flight_list_202601.parquet` e
`flight_list_202508.parquet`; hash e derivati sono stati registrati negli
artefatti locali. Agosto 2025 espone 29 giorni con righe Boeing; gennaio 2026
21 giorni. I giorni senza righe non sono interpretati come zero traffico, quindi
la copertura utile resta parziale e G2/G4 non vengono aperti. La suite completa
passa: 265 test.

Exact next step: distinguere nei report i giorni senza osservazioni dai giorni a esposizione zero e rigenerare il replay solo dopo questa classificazione.

### Classificazione giornaliera OPDI — 2026-09-12

Analizzati i Parquet acquisiti: 50 giorni hanno righe Boeing (29 agosto 2025,
21 gennaio 2026) e 12 giorni sono realmente assenti dal file (2 agosto 2025,
10 gennaio 2026). Non risultano giorni con file presente e zero Boeing: nessun
buco è stato riclassificato artificialmente come esposizione zero.

Exact next step: usare la classificazione per il replay, mantenendo i 12 giorni assenti come missing e non come zero.

### Registro PIT aggiornato con copertura classificata — 2026-09-12

Il registro `data/model/model-1.5-rolling-origin-pit-admission-v1.json` è stato
aggiornato: l’orizzonte 2025-02-01–2026-01-31 conta ora 353 giorni osservati e
12 giorni privi di righe sorgente. I giorni mancanti non sono imputati e il
cutoff resta non eleggibile per G2/G4 finché la provenienza PIT non è verificata.
Full suite: 265 passed.

Exact next step: rigenerare la sensibilità Model 1.5 con i 353 giorni osservati e confrontarla con il replay precedente.

### Sensibilità OPDI aggiornata a 353 giorni — 2026-09-12

Creato `data/model/model-1.5-opdi-353-day-sensitivity-replay-v1.json` con il
nuovo registro di copertura: 353 giorni osservati, 12 missing, intervallo fino
al 2026-01-31. Il forecast precedente non viene riutilizzato come risultato a
365 giorni; la rigenerazione parziale resta esplicitamente diagnostica.
Full suite: 265 passed.

Exact next step: rigenerare i punteggi giornalieri usando la maschera dei 12 giorni missing e produrre il confronto finale con i due casi post-cutoff.

### Punteggio giornaliero aggiornato su 353 giorni — 2026-09-12

Rigenerato il percorso relativo OPDI con la maschera dei giorni mancanti. Su 353
giorni osservati, la data modale del punteggio di esposizione è 2025-08-22 con
quota relativa 0,395%; i 12 giorni assenti sono esclusi, non imputati. Artefatto:
`data/model/model-1.5-opdi-353-day-daily-score-v1.json`. Full suite: 265 passed.

Exact next step: usare il punteggio aggiornato nel confronto diagnostico Model 1.5 e lasciare invariati i gate scientifici.

### Verifica alternativa copertura giornaliera — 2026-09-12

La ricerca ha individuato la pagina pubblica EUROCONTROL **Daily Operated Schedules – Airports**, con serie giornaliere aggregate 2022–2026. La fonte non pubblica una ripartizione giornaliera Boeing per famiglia e operatore e quindi non può sostituire i 12 giorni OPDI mancanti nel denominatore G2. Può essere registrata solo come covariata aggregata di sensibilità, senza trasformare i giorni OPDI privi di righe in esposizione Boeing osservata.

**Exact next step:** mantenere i 12 giorni come `missing_source_day` e, se serve un esperimento separato, usare gli schedules EUROCONTROL solo come covariata aggregata marcata `development_sensitivity`.

### Simulatore diagnostico a copertura parziale — 2026-09-12

È stato creato `site/data/model-15-simulator.json`, input machine-readable per il simulatore Model 1.5. Usa il punteggio giornaliero OPDI già calcolato su 353 giorni osservati, esclude esplicitamente i 12 `missing_source_day` e conserva G1–G4 `BLOCKED`, `global_denominator=false` e `promotion_allowed=false`. La data modale diagnostica è 22 agosto 2025 con quota relativa 0,3955%; non è una probabilità assoluta.

**Exact next step:** collegare il simulatore/UI a `site/data/model-15-simulator.json` mostrando sempre il banner “diagnostico a copertura parziale”.

### Confronto simulatore con casi post-cutoff — 2026-09-12

La simulazione diagnostica Model 1.5 (cutoff 2025-01-31, copertura OPDI parziale, 12 giorni esclusi) è stata confrontata con i due casi successivi noti: AI171 del 12 giugno 2025 e ACT747 del 20 ottobre 2025. La data modale è 22 agosto 2025; entrambi i casi ricadono nell’orizzonte, nessuno coincide con la moda, errore assoluto medio 65,0 giorni. Output: `data/model/model-1.5-diagnostic-simulator-comparison-v1.json` e `docs/MODEL-1.5-DIAGNOSTIC-SIMULATOR-COMPARISON-v1.md`.

**Exact next step:** mostrare nel simulatore la tabella dei due casi con errore in giorni e avviso diagnostico.

### Simulazione cutoff 5 novembre 2025 — 2026-09-12

Il simulatore Model 1.5 è stato eseguito con cutoff 2025-11-05, dopo UPS 2976 del 2025-11-04. Sull’orizzonte 2025-11-06–2026-11-05 la sensibilità EuroNOVA produce come moda 22 maggio 2026 con decadimenti 7–60 giorni; con decadimenti 90–270 la moda è 6 luglio 2026. La baseline calendario produce 9 gennaio 2026. Output: `data/model/model-1.5-simulator-cutoff-20251105-v1.json`.

**Exact next step:** confrontare questa simulazione con il primo evento confermato successivo al 5 novembre 2025 quando il suo record sarà ammesso nel ledger.

### Default simulatore aggiornato — 2026-09-12

La configurazione diagnostica predefinita è ora `EuroNOVA` con decadimento 90–270 giorni (`config/model-1.5-scoped.json`). Nel simulatore con cutoff 2025-11-05 la moda corrispondente è 6 luglio 2026. I gate scientifici, il denominatore globale e le previsioni congelate non cambiano. Suite verificata: 265 test superati.

**Exact next step:** usare questa configurazione come default nelle nuove simulazioni diagnostiche e riportare sempre l’etichetta di sensibilità regionale.

### Nuova previsione diagnostica cutoff 7 settembre 2026 — 2026-09-12

È stato eseguito il training Model 1.5 con cutoff 2026-09-07 e generata una previsione prospettica separata dopo l’evento Miami del 2026-09-06. Con default EuroNOVA e decadimento 90–270 giorni, tutte le 181 configurazioni producono la data modale **6 luglio 2027** sull’orizzonte 2026-09-08–2027-09-07. Il record è diagnostico: `global_denominator=false`, `pit_admitted=false`, `promotion_allowed=false`, e resta marcato da non modificare fino al prossimo caso confermato. Output: `data/model/model-1.5-prospective-forecast-cutoff-20260907-v1.json` e training `data/model/model-1.5-trained-development-v2.json`.

**Exact next step:** non modificare questa previsione; riaprire il ciclo solo quando un nuovo evento confermato e la relativa evidenza point-in-time saranno acquisiti.

### Freeze AGGIORNA collegato — 2026-09-12

AGGIORNA ora verifica la presenza della previsione diagnostica con cutoff 2026-09-07 e, se presente, ne impedisce la ricalcolazione automatica finché `frozen_until_next_confirmed_case=true`. Il controllo richiede anche cutoff e stato attesi. I retry di acquisizione FAA/NTSB restano nel workflow; l’ultimo tentativo locale è fallito per DNS. Suite: 265 test superati.

**Exact next step:** al prossimo caso confermato, acquisire e verificare il record, quindi creare una nuova previsione append-only con cutoff successivo.

### Etichetta previsione di prova — 2026-09-12

La previsione 6 luglio 2027 con cutoff 2026-09-07 è ora esplicitamente marcata `diagnostic_test_unfrozen` e `test_only=true`. Data e calcoli non sono cambiati; AGGIORNA continua a preservarla senza promuoverla a previsione ufficiale. Suite: 265 test superati.

**Exact next step:** usare il record solo per simulazioni e confronti diagnostici fino all’acquisizione del prossimo caso confermato.

### Collegamento training–previsione corretto — 2026-09-12

Il training `model-1.5-trained-development-v2.json` ora riferisce esplicitamente la previsione diagnostica con cutoff 2026-09-07 e moda 2027-07-06. La traiettoria storica `time_to_event` resta separata come diagnostica e non viene più interpretata come previsione operativa corrente. Suite: 265 test superati.

**Exact next step:** attendere un nuovo caso confermato o una nuova acquisizione; non modificare il record diagnostico corrente.

### Pagine BM1.5 test e AGGIORNA manuale — 2026-09-12

Aggiunta `site/model-15.html` con spiegazione rapida, previsione di prova congelata al cutoff 2026-09-07 (6 luglio 2027), struttura SVG del modello e dati in ingresso. Le pagine esistenti collegano BM1.5 e descrivono l’archivio storico senza presentare affinamenti attivi. AGGIORNA ora si attiva esclusivamente con `workflow_dispatch`; rimossa la schedulazione automatica ogni quattro giorni. Suite: 265 test superati.

**Exact next step:** verificare il rendering su GitHub Pages e pubblicare la versione BM1.5 come test di sviluppo.

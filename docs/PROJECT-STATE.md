# BSFM Project State

Updated: 2026-09-05

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #25 (`33978802087`) completed successfully on source SHA `971cdd6a1ec0576208191e2d18fe76fce2742c86`; it is the latest workflow-verified baseline.
- The generated-state commit on `main` is `ce33ea54b36613cf122e3201c2825a329700f656` and uses privacy-safe Git metadata.
- AGGIORNA #22 failed at the retired ICAO acquisition step and is retained only as historical operational evidence. No new ICAO API retrieval is permitted.
- Success/failure of CI verifies only checks actually executed; it does not establish predictive validity or open a scientific gate.

## Canonical documents
`AGENTS.md` is the constitution/privacy/bootstrap; `docs/MODEL-SPEC.md` the model contract; `docs/LABORATORY-PROTOCOL.md` the scientific protocol; `docs/NEW-CHAT.md` the fresh-session bootstrap; `docs/F-002-PREREGISTRATION-v1.md` the frozen F-002 evaluation; `docs/G1-G3-EVIDENCE-PLAN-v1.md` the detailed evidence plan.

## F-002
`forecasts/F-002.json` is frozen. Later evidence/refinements cannot rewrite it or add retroactive probabilities. Geography, MSN and flight-number resolution research is explicitly separate from the original F-002 scoring.

## Current research branch
Draft PR #2, branch `research/privacy-safe-rebuild-20260905`, is the privacy-safe reconstruction of post-#25 research work. It was created directly from current `main`; it does not import the commit history of PR #1. New commits use GitHub `users.noreply.github.com` metadata. PR #1 must not be merged.

Focused local verification of the rebuild reports `23 passed` with `PYTHONPATH=. pytest -q`. This is a local focused-suite result, not a substitute for repository CI or AGGIORNA.

## G1 — BLOCKED
`data/census/year-ledger.json` remains the canonical 2010-2025 reconciliation ledger; every year remains `reconciled=false` unless all six annual completeness controls pass.

The annual fail-closed controls are:
1. annual source scope demonstrated;
2. all fatal jets mapped;
3. Boeing target membership mapped;
4. competent authority per candidate;
5. independent reconciliation;
6. target taxonomies resolved.

Evidence progress such as `4/6` or `5/6` is an evidence-control count, not a scientific validation percentage.

### Candidate/evidence state
The privacy-safe branch preserves the existing 2024 candidate set and ports the prior research evidence for 2019-2023 without importing legacy Git history:
- 2019: ET302 candidate supported; year remains partial/unreconciled.
- 2020: PC2193 and IX1344 included as candidates; PS752 remains explicitly unresolved because the frozen target does not settle the Annex-13-accident versus unlawful/security-act boundary.
- 2021: SJY182 candidate supported; year remains partial/unreconciled.
- 2022: MU5735 candidate supported; Boeing-table absence is retained as a scope/classification issue, not a negative attestation.
- 2023: Boeing/IATA zero-fatal-jet evidence is retained, but wider EASA scope still requires reconciliation before any global zero-Boeing attestation.
- 2024: existing SQ321, Swiftair/BCS18D and Jeju Air 2216 candidate layer remains candidate evidence, not a year attestation.

No candidate count, source count or structurally valid file can open G1 by itself.

### NTSB AVALL audit
The AGGIORNA #25 `ntsb-derived` artifact was recovered and audited. The repository stores provenance/hash metadata rather than the ~51 MB ZIP in ordinary Git history.

For Boeing-commercial airplane rows in 2010-2025 under the implemented AVALL classification, 1,250 of 1,358 rows recover an official phase from `Events_Sequence.Occurrence_Code` using the eADMS public data dictionary (92.05%); among rows with sequence data the result is 1,250 of 1,252. These are research diagnostics only.

`NUSC` is treated as explicit Non-U.S. Commercial, `NUSN` as explicit Non-U.S. Noncommercial, and missing/unknown operation codes remain `unknown` rather than being inferred from operator names. `inj_tot_f` and `inj_f_grnd` are preserved separately so external/ground fatalities are not lost. Foreign NTSB records remain supporting/discovery evidence and never silently override the competent investigation authority.

## G2 — BLOCKED
Annual Boeing-family departures/cycles or another predeclared defensible global exposure denominator remain incomplete for 2010-2025.

The source inventory now records that public IATA Annex 4 editions expose manufacturer/model sector counts across overlapping windows covering at least 2010-2019, while recent WATS releases expose Boeing 737 all-variant flight-frequency observations. This does not close G2 because:
- a sustainable public 2020-2023 bridge has not yet been demonstrated;
- Boeing 737 aggregate exposure cannot be split into Classic/NG/MAX using fleet share, deliveries, market share or accident counts;
- historical IATA/OAG values are revision-sensitive and require an explicit vintage rule;
- target-universe cohorts such as 727 and 737-Original require compatible exposure or a separately preregistered exclusion before G2/G4 can pass.

No convenience proxy, cumulative-rate inversion or aggregate disaggregation is permitted.

## G3 — BLOCKED
Historical predictor records do not yet establish field-level public availability at simulated cutoffs. Current presence in NTSB AVALL or later administrative approval does not prove historical point-in-time public availability. Dated official releases and archived/versioned public artifacts remain preferred evidence.

## G4 — BLOCKED
Downstream of G1-G3. Genuine paired OOS candidate-vs-exposure-baseline evaluation begins only after upstream PASS.

## Resolution research — separate from F-002 scoring
Geography, MSN and flight number have independent fail-closed support gates. A dimension is not supported merely because a value can be found retrospectively. Estimator support, denominator/exposure support, point-in-time support, provenance and uncertainty are required; MSN additionally requires airframe exposure and identity history, while flight number requires operational-source access and flight exposure.

## Public/privacy/licensing state
Public UI keeps experimental/status boundaries. FAA SDR and NTSB AVALL remain supporting/descriptive sources with scope limitations. The NTSB snapshot directory stores provenance and hashes, not the large derived ZIP. This public repository must contain no personal/private/sensitive user data or credential values. No new ICAO API retrieval is permitted.

## Operational state
AGGIORNA #25 is the latest successful full workflow run. The privacy-safe rebuild and the newly ported G1/G2 research are later than that run and therefore are not yet workflow-verified. Draft PR #2 remains explicitly non-mergeable as a scientific checkpoint until remaining evidence/repository checks are complete. G1-G4 remain BLOCKED.

## Exact next step
Continue the G1 census from the currently ported 2019-2024 evidence by reconstructing and independently reconciling 2018 backward to 2010 and 2025 forward, with competent-authority evidence and all six annual controls. In parallel, test whether a sustainable public 2020-2023 IATA/OAG or equivalent bridge can provide compatible global model/family exposure without proxy splitting; if not, keep G2 BLOCKED. Re-run the repository's full test/CI surface when available, keep PR #2 draft until these checks are complete, do not merge PR #1, and do not alter F-002 or set any G1-G4 gate to PASS without the documented criteria.

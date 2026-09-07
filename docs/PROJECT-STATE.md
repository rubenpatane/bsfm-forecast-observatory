# BSFM Project State

Updated: 2026-09-07

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md`, `docs/NEW-CHAT.md`, `docs/MODEL-SPEC.md` and `docs/LABORATORY-PROTOCOL.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` remains the single operational workflow.
- AGGIORNA #34 is the latest successful full operational workflow. It ran from `fcc1b8e35129ab9ba7f8b0b13b1934d4d9ba0b3c`, committed auditable generated state as `548bfe6658c41b3fbac4d05b56f9af1477b30b69`, retained `PD14-20260907-7fa7c48bc555` byte-identical and deployed the public observatory/manual editorial board.
- The pre-G1-closure `main` checkpoint was `b65368bedc0d2ab37533b7c246c8eb342b482493`.
- No new ICAO API retrieval is permitted. Frozen historical ICAO evidence is cross-check material only.
- Workflow/software success verifies only executed checks; it does not establish predictive validity.

## F-002 and target semantics
`forecasts/F-002.json` is frozen. Its target string is `next_fatal_accident_involving_boeing_commercial_jet`; the object contains no explicit hostile/unlawful-action or missing-aircraft inclusion/exclusion clause. F-002 must remain outside G1 closure diffs.

Prospective Target Taxonomy v2 remains adopted and explicitly non-retroactive. It excludes officially classified deliberate hostile/security/unlawful-interference events from the prospective primary safety target and keeps missing aircraft pending until competent-authority evidence establishes the required status. It does not retroactively adjudicate MH370, MH17, PS752 or historical G1 v1.

## G1 — CLOSED_WITH_LIMITATION
Historical G1 v1 research is closed with a structural limitation rather than left as an active evidence blocker.

Canonical closure contract: `data/census/g1-closure-v1.json`.

- 14/16 annual cells are fully identifiable/reconciled: 2010, 2011, 2012, 2013, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024 and 2025.
- 2014 and 2020 remain non-identifiable under the frozen historical v1 target semantics.
- 2014 retains the MH370 missing-aircraft boundary and MH17 hostile/unlawful-action boundary unresolved.
- 2020 retains the PS752 hostile/unlawful-action boundary unresolved.
- `data/census/year-ledger.json` and the annual evidence files remain unchanged in meaning: 2014 and 2020 are still not `reconciled=true` and do not become false zero-event cells.
- MH370, MH17 and PS752 are not retrospectively included or excluded by this decision.
- Prospective Target Taxonomy v2 has no retroactive effect.

The integrated G1 audit now distinguishes strict completeness from gate acceptability. Strict 16/16 `complete` remains false; `gate_status=CLOSED_WITH_LIMITATION` and `gate_acceptable=true` are valid only when the closure contract exactly matches the two unreconciled cells and all other candidate/ledger/evidence consistency checks remain clean.

The downstream walk-forward path is censor-aware. Targets inside 2014 or 2020 are excluded, and any forecast interval whose post-cutoff through target-event interval intersects either non-identifiable year is excluded. This prevents unresolved events from being silently interpreted as non-events.

This G1 closure removes G1 as an active research blocker. It does not open G2, G3 or G4 and is not equivalent to a strict 16/16 PASS.

## G1 closure implementation status
Branch `science/close-g1-with-limitation-20260907` was created from `b65368b` and adds:
- machine-readable `g1-closure-v1` contract;
- explicit `PASS` / `CLOSED_WITH_LIMITATION` / `BLOCKED` audit semantics;
- censor-aware walk-forward construction;
- downstream foundation propagation of G1 status/censored years;
- regression tests preserving unresolved event visibility and prohibiting false-zero/cross-censored scoring;
- aligned agent constitution, laboratory protocol and G1-G3 evidence plan.

The chat execution environment could not clone GitHub because outbound DNS from the container is unavailable, so the full repository test suite and CLI audits have not been executed here and must not be claimed as passed. A direct static Python compile/logic check of the censor-aware walk-forward change did execute successfully (`STATIC_AND_CENSOR_LOGIC_OK`). This checkpoint is therefore committed-but-not-yet-workflow-verified until the normal repository verification environment runs it. `AGGIORNA` was not invoked for this change.

## G2 — BLOCKED
A complete defensible global Boeing family/year operational exposure denominator for 2010-2025 is still missing. Required cohorts remain `727`, `737-Original`, `737-Classic`, `737-NG`, `737-MAX`, `747`, `757`, `767`, `777`, `787`.

Historical IATA Safety Report Annex 4 provides useful global model-level sectors through 2019 but aggregates all 737 variants. The preferred lawful solution remains an aircraft-model-level source such as IATA WATS Global, OAG Historical Flight Data or Cirium historical products, with directly observed model/operator/year activity that can be deterministically mapped to the BSFM cohorts. Aggregate 737 traffic must never be proxy-split by fleet share, deliveries, market share or accident counts. `baseline_present=false` remains mandatory until the full accepted matrix exists.

## G3 — BLOCKED
The predictor universe remains intentionally fail-closed. `data/pit/predictor-universe-v1.json` is not yet a frozen, non-empty admitted universe with strict PIT evidence for every required predictor. NTSB historical availability has partial anchors; FAA SDR public-release timing remains the harder blocker. The model 1.2 `faa_sdr_precursors` obligation cannot be silently dropped to manufacture a PASS.

The separate G1 outcome-publication ledger is complete and does not open G3.

## G4 — BLOCKED
G4 remains blocked by G2 and G3. G1 is now acceptable only under its registered censoring contract; any future historical evaluation must preserve that censoring. No candidate-vs-baseline skill claim, absolute accident probability enablement or validated-prediction claim is allowed while the remaining scientific prerequisites are unmet.

The automatic-cycle architecture and BSFM-PD public-data paths remain implementation/research surfaces, not proof of global BSFM 1.2 predictive validity.

## BSFM-PD public-data paths
BSFM-PD 1.3 remains a separate U.S.-linked public-data experiment with a negative/underpowered historical result. It does not open global G2/G3/G4.

BSFM-PD 1.4 remains the separately preregistered public-online prospective path. Active immutable record `PD14-20260907-7fa7c48bc555` remains governed by its own contract and 90-day horizon; no G1 closure change rewrites or rescales it.

The manual Miami editorial entry remains `PENDING_OFFICIAL_ADJUDICATION` and has `scientific_effect: NONE` until sufficient competent-authority evidence is public.

## Public/privacy/licensing state
The repository remains public and privacy-safe. No private user data, credentials or secret values may enter Git history. No new ICAO API retrieval is permitted. Protected third-party data may not be redistributed without appropriate rights; permissible provenance/hashes/acquisition instructions may be retained.

## Exact next step / external dependencies
Run the standard full test suite plus `python -m bsfm.cli verify`, `audit-foundation` and `audit-final` for the integrated G1 closure in a repository environment with GitHub/network access, without invoking AGGIORNA solely for verification. If those checks are clean, retain G1 as `CLOSED_WITH_LIMITATION` and continue with the G2 lawful aircraft-model exposure acquisition path; do not revisit 2014/2020 unless genuinely pre-existing independent target-semantics evidence is discovered.

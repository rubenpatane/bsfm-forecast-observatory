# BSFM Project State

Updated: 2026-09-05

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #21 (`33974695186`) completed successfully and is the last successful full workflow run.
- AGGIORNA #22 (`33975985882`) failed at the now-retired ICAO acquisition step. Pre-update verification completed successfully with 115 tests passed, registry integrity OK and the scientific foundation correctly fail-closed. The ICAO step returned HTTP 403 at the 2019 request after returning rows for 2010–2018; all later workflow steps were skipped. This failed run is not a scientific regression and must not be retried against ICAO.
- Success/failure of CI verifies only checks actually executed; it does not establish predictive validity or open a scientific gate.

## Canonical documents
`AGENTS.md` is the constitution/privacy/bootstrap; `docs/MODEL-SPEC.md` the model contract; `docs/LABORATORY-PROTOCOL.md` the scientific protocol; `docs/NEW-CHAT.md` the fresh-session bootstrap; `docs/F-002-PREREGISTRATION-v1.md` the frozen F-002 evaluation; `docs/G1-G3-EVIDENCE-PLAN-v1.md` the detailed evidence plan.

## F-002
`forecasts/F-002.json` is frozen. Later evidence/refinements cannot rewrite it or add retroactive probabilities. The repository does not claim cryptographic proof of public publication on its declared 2026-08-19 cutoff.

## G1 — BLOCKED
`data/census/year-ledger.json` is the canonical 2010-2025 reconciliation ledger; keep years `reconciled=false` until evidenced. AGGIORNA #21 acquired 4,669 ICAO Official Accidents rows, retained only as historical evidence/provenance; no new ICAO retrieval is permitted.

### Sustainable G1 path
`data/census/boeing-statistical-summary-source.json` and `data/census/easa-asr-source.json` register sustainable public reconciliation sources. Boeing's worldwide Statistical Summary contains accident summaries/rates and EASA maintains Annual Safety Review editions, with recent editions exposing fatal-accident appendices. These source capabilities are not census attestations.

A new fail-closed candidate layer is committed in `bsfm/g1_candidates.py`, `tests/test_g1_candidates.py` and `data/census/g1-candidates.json`. It separates candidate discovery/adjudication from the canonical year ledger. Candidate rows require event/date/model/fatality/commercial/source provenance plus an explicit `include`, `exclude` or `unresolved` decision and reason; missing facts are not inferred, duplicate internal IDs invalidate structural audit, and even a structurally valid candidate dataset always reports `global_census_complete=false` / `gate_status=BLOCKED`. No candidate has yet been inserted merely from narrative web snippets.

### ICAO retrieval freeze
ICAO API retrieval is disabled from operational automation. AGGIORNA #22 empirically confirmed prior access is unusable for the project (HTTP 403). BSFM will not purchase paid ICAO calls under the current research plan. Event-level ICAO rows must not be reconstructed by new API calls or published contrary to licence terms.

## G2 — BLOCKED
Annual Boeing-family departures/cycles or another predeclared defensible exposure denominator are incomplete for 2010-2025. Boeing Statistical Summary provides worldwide traffic context and cumulative airplane-type statistics, but inspection has not established annual departures/cycles for every BSFM Boeing family-year cell. Cumulative rates or aggregate traffic must not be inverted/disaggregated to manufacture exposure.

## G3 — BLOCKED
Historical predictor records do not yet establish field-level public availability at simulated cutoffs. Dated official releases and archived/versioned public artifacts remain preferred evidence.

## G4 — BLOCKED
Downstream of G1-G3. Genuine paired OOS candidate-vs-exposure-baseline evaluation begins only after upstream PASS.

## Public/privacy/licensing state
Public UI keeps experimental/status boundaries. FAA SDR and NTSB AVALL remain supporting/descriptive sources with scope limitations. This public repository must contain no personal/private/sensitive user data or credential values. Public Boeing/EASA source records contain source metadata/scientific observations only. ICAO raw/event-level API data is not to be published.

## Operational state
AGGIORNA #21 is the last successful full run. #22 is an obsolete-path ICAO failure. The current ICAO-free workflow and the new G1 candidate-census foundation are committed but not yet runtime-verified by a later AGGIORNA. Repository inspection after the candidate commit found no newer workflow run than #22.

## Exact next step
Populate `data/census/g1-candidates.json` only from directly inspected official event-level evidence, beginning with the Boeing 2025 accident summaries and EASA 2025/2024 fatal-accident appendices for 2024/2023, then work backward through archived editions. For every Boeing candidate preserve source record/locator and leave target eligibility `unresolved` whenever commercial/fatal/model semantics are not directly evidenced. Reconcile each candidate against NTSB or the competent national investigation authority before considering year-ledger attestation. In parallel continue searching for genuine Boeing family-by-year exposure; do not infer missing denominators. Keep all gates BLOCKED until criteria are actually met.

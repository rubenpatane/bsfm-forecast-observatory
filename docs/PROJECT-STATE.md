# BSFM Project State

Updated: 2026-09-05

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #23 (`33977244308`) completed successfully on source SHA `7c3ca88c9e9943df81e12e701233f47010f25ad4`; it is the latest workflow-verified baseline and verified the ICAO-free workflow plus G1 candidate-census foundation.
- AGGIORNA #22 (`33975985882`) failed at the retired ICAO acquisition step and is retained only as historical operational evidence. No new ICAO retrieval is permitted.
- Success/failure of CI verifies only checks actually executed; it does not establish predictive validity or open a scientific gate.

## Canonical documents
`AGENTS.md` is the constitution/privacy/bootstrap; `docs/MODEL-SPEC.md` the model contract; `docs/LABORATORY-PROTOCOL.md` the scientific protocol; `docs/NEW-CHAT.md` the fresh-session bootstrap; `docs/F-002-PREREGISTRATION-v1.md` the frozen F-002 evaluation; `docs/G1-G3-EVIDENCE-PLAN-v1.md` the detailed evidence plan.

## F-002
`forecasts/F-002.json` is frozen. Later evidence/refinements cannot rewrite it or add retroactive probabilities. The repository does not claim cryptographic proof of public publication on its declared 2026-08-19 cutoff.

## G1 — BLOCKED
`data/census/year-ledger.json` is the canonical 2010-2025 reconciliation ledger; keep years `reconciled=false` until evidenced. AGGIORNA #21 acquired 4,669 ICAO Official Accidents rows, retained only as historical evidence/provenance; no new ICAO retrieval is permitted.

### Sustainable G1 path
`data/census/boeing-statistical-summary-source.json` and `data/census/easa-asr-source.json` register sustainable public reconciliation sources. Boeing's worldwide Statistical Summary contains accident summaries/rates and EASA maintains Annual Safety Review editions, with recent editions exposing fatal-accident appendices. These source capabilities are not census attestations.

The fail-closed candidate layer lives in `bsfm/g1_candidates.py`, `tests/test_g1_candidates.py` and `data/census/g1-candidates.json`. Candidate rows require event/date/model/fatality/commercial/source provenance plus an explicit `include`, `exclude` or `unresolved` decision and reason; missing facts are not inferred, duplicate internal IDs invalidate structural audit, and even a structurally valid candidate dataset always reports `global_census_complete=false` / `gate_status=BLOCKED`.

The candidate workspace now contains the first three 2024 Boeing records grounded in directly inspected official investigation evidence: Singapore Airlines SQ321 (B777-300ER, one fatality), Swiftair/BCS18D at Vilnius (B737-400SF family, one fatality), and Jeju Air 2216 at Muan (B737-800, 179 fatalities). They are candidate inclusions, not a 2024 reconciliation attestation. EASA ASR 2025 independently reports 14 fatal airline accidents worldwide in 2024, so the broader 2024 universe still requires event-level reconciliation. The Jeju candidate currently uses NTSB Annex 13 accredited-representative evidence and still requires the competent Korean investigation authority before any year attestation.

### ICAO retrieval freeze
ICAO API retrieval is disabled from operational automation. AGGIORNA #22 empirically confirmed prior access is unusable for the project (HTTP 403). BSFM will not purchase paid ICAO calls under the current research plan. Event-level ICAO rows must not be reconstructed by new API calls or published contrary to licence terms.

## G2 — BLOCKED
Annual Boeing-family departures/cycles or another predeclared defensible exposure denominator are incomplete for 2010-2025. Boeing Statistical Summary provides worldwide traffic context and cumulative airplane-type statistics, but inspection has not established annual departures/cycles for every BSFM Boeing family-year cell. Cumulative rates or aggregate traffic must not be inverted/disaggregated to manufacture exposure.

## G3 — BLOCKED
Historical predictor records do not yet establish field-level public availability at simulated cutoffs. Dated official releases and archived/versioned public artifacts remain preferred evidence.

## G4 — BLOCKED
Downstream of G1-G3. Genuine paired OOS candidate-vs-exposure-baseline evaluation begins only after upstream PASS.

## Public/privacy/licensing state
Public UI keeps experimental/status boundaries. FAA SDR and NTSB AVALL remain supporting/descriptive sources with scope limitations. This public repository must contain no personal/private/sensitive user data or credential values. Public Boeing/EASA/source records contain source metadata/scientific observations only. ICAO raw/event-level API data is not to be published.

## Operational state
AGGIORNA #23 is the latest successful full run and verifies the ICAO-free workflow/candidate foundation at source SHA `7c3ca88c9e9943df81e12e701233f47010f25ad4`. The subsequent 2024 candidate population and this state update are committed after that run and therefore are not yet workflow-verified. G1-G4 remain BLOCKED.

## Exact next step
Complete 2024 event-level reconciliation against EASA ASR 2025 Appendix 1 and competent national investigation authorities, obtaining the Korean authority record for Jeju Air 2216 and checking whether any additional 2024 Boeing fatal-airline accidents belong to the fixed BSFM target. Then inspect EASA ASR 2024 Appendix 1 for 2023 and record explicit zero-Boeing evidence only if the complete appendix supports it; never infer a zero-event year from aggregate counts alone. Keep `data/census/year-ledger.json` unchanged until independent reconciliation criteria are met, and continue searching separately for genuine Boeing family-by-year exposure without deriving missing denominators.

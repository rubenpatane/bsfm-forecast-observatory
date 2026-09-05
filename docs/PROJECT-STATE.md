# BSFM Project State

Updated: 2026-09-05

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #24 (`33978310106`) completed successfully on source SHA `bc37cbfc3802c6579cb8130f70d6ce0d9a2b2bc4`; it is the latest workflow-verified baseline and verified the ICAO-free workflow plus the first official 2024 G1 candidate population.
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

The fail-closed candidate layer lives in `bsfm/g1_candidates.py`, `tests/test_g1_candidates.py` and `data/census/g1-candidates.json`. Candidate rows require event/date/model/fatality/commercial/source provenance plus an explicit `include`, `exclude` or `unresolved` decision and reason; missing facts are not inferred, duplicate internal IDs invalidate structural audit, and even a structurally valid candidate dataset always reports `global_census_complete=false` / `gate_status=BLOCKED`. The normalizer now also preserves explicit independent `reconciliation_evidence`; corroboration cannot open G1 by itself.

The candidate workspace contains three 2024 Boeing fatal-commercial-jet candidates: Singapore Airlines SQ321 (B777-300ER, one fatality), Swiftair/BCS18D at Vilnius (B737-400SF family, one fatality), and Jeju Air 2216 at Muan (B737-800, 179 fatalities). The Boeing 2024 Statistical Summary independently lists all three in its worldwide commercial-jet 2024 accident table. Jeju is now grounded primarily in the competent Republic of Korea ARAIB record (AAR2404 / HL8088 / 7C2216), with Boeing and BEA as independent reconciliation evidence. These remain candidate inclusions, not a 2024 year attestation.

EASA ASR 2025 reports 14 fatal airline accidents worldwide in 2024, but that aggregate count is not a Boeing-only event census. Direct inspection of EASA ASR 2024 Appendix 1 shows domain-organized fatal-accident lists through 2023; its commercial-air-transport complex-aeroplane section is not demonstrated to be an exhaustive worldwide commercial-jet census. Therefore absence of a Boeing row there must not be interpreted as a global zero-Boeing year for 2023.

### ICAO retrieval freeze
ICAO API retrieval is disabled from operational automation. AGGIORNA #22 empirically confirmed prior access is unusable for the project (HTTP 403). BSFM will not purchase paid ICAO calls under the current research plan. Event-level ICAO rows must not be reconstructed by new API calls or published contrary to licence terms.

## G2 — BLOCKED
Annual Boeing-family departures/cycles or another predeclared defensible exposure denominator are incomplete for 2010-2025. Direct inspection of Boeing's 2025 Statistical Summary confirms annual worldwide fleet-level departures/flight-hours context and cumulative Boeing-vs-total shares, but not annual departures/cycles for every BSFM Boeing family-year cell. Cumulative airplane-type rates, cumulative Boeing shares or aggregate worldwide traffic must not be inverted, interpolated or disaggregated to manufacture family-year exposure.

## G3 — BLOCKED
Historical predictor records do not yet establish field-level public availability at simulated cutoffs. Dated official releases and archived/versioned public artifacts remain preferred evidence.

## G4 — BLOCKED
Downstream of G1-G3. Genuine paired OOS candidate-vs-exposure-baseline evaluation begins only after upstream PASS.

## Public/privacy/licensing state
Public UI keeps experimental/status boundaries. FAA SDR and NTSB AVALL remain supporting/descriptive sources with scope limitations. This public repository must contain no personal/private/sensitive user data or credential values. Public Boeing/EASA/source records contain source metadata/scientific observations only. ICAO raw/event-level API data is not to be published.

## Operational state
AGGIORNA #24 is the latest successful full run and verifies the ICAO-free workflow plus the initial 2024 candidate population at source SHA `bc37cbfc3802c6579cb8130f70d6ce0d9a2b2bc4`. Subsequent source-scope hardening, Korean-authority reconciliation, independent evidence preservation and new tests are committed after that run and therefore are not yet workflow-verified. G1-G4 remain BLOCKED.

## Exact next step
Batch-verify the post-AGGIORNA-24 reconciliation changes, then continue the G1 census backward from 2023 using worldwide Boeing Statistical Summary evidence plus competent national investigation authorities; treat EASA appendices only within their demonstrated scope and never infer global zero years from their absence. In parallel, search sustainable official/primary sources for genuine Boeing family-by-year departures/cycles; if none provide the required denominator, keep G2 BLOCKED rather than deriving it from aggregate or cumulative statistics. Keep every year in `data/census/year-ledger.json` `reconciled=false` until the full year-level completeness and independent-reconciliation criteria are evidenced.

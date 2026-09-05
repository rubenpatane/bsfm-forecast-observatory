# BSFM Project State

Updated: 2026-09-05

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #25 (`33978802087`) completed successfully on source SHA `971cdd6a1ec0576208191e2d18fe76fce2742c86`. Pre-update tests/integrity, official-source refresh, FAA SDR history, NTSB AVALL normalization, post-update tests/scientific audits, readiness generation and Pages deployment all completed successfully. The workflow then published generated-state commit `ce33ea54b36613cf122e3201c2825a329700f656`.
- AGGIORNA #25 batch-verifies the reconciliation/source-scope/test changes that were committed after AGGIORNA #24.
- AGGIORNA #22 (`33975985882`) failed at the retired ICAO acquisition step and is retained only as historical operational evidence. No new ICAO API retrieval is permitted.
- Success/failure of CI verifies only checks actually executed; it does not establish predictive validity or open a scientific gate.

## Canonical documents
`AGENTS.md` is the constitution/privacy/bootstrap; `docs/MODEL-SPEC.md` the model contract; `docs/LABORATORY-PROTOCOL.md` the scientific protocol; `docs/NEW-CHAT.md` the fresh-session bootstrap; `docs/F-002-PREREGISTRATION-v1.md` the frozen F-002 evaluation; `docs/G1-G3-EVIDENCE-PLAN-v1.md` the detailed evidence plan.

## F-002
`forecasts/F-002.json` is frozen. Later evidence/refinements cannot rewrite it or add retroactive probabilities. The repository does not claim cryptographic proof of public publication on its declared 2026-08-19 cutoff.

## G1 — BLOCKED
`data/census/year-ledger.json` is the canonical 2010-2025 reconciliation ledger; every year remains `reconciled=false`. AGGIORNA #21 acquired 4,669 ICAO Official Accidents rows, retained only as historical evidence/provenance; no new ICAO retrieval is permitted.

### Sustainable G1 path
`data/census/boeing-statistical-summary-source.json` and `data/census/easa-asr-source.json` register sustainable public reconciliation sources. `data/census/year-evidence-YYYY.json` now records partial annual reconciliation and source-scope conflicts without changing the canonical ledger. Candidate rows remain fail-closed in `data/census/g1-candidates.json`; candidate population and independent corroboration never attest global completeness by themselves.

The candidate workspace contains the three previously verified 2024 candidates plus China Eastern MU5735 on 21 March 2022. For MU5735, CAAC identifies Boeing 737-800 B-1791 on a scheduled passenger flight and records all 132 occupants as fatalities; IATA independently lists the B737-800 as a jet hull-loss event with 132 onboard fatalities. It is therefore retained as an `include` candidate under the fixed BSFM event semantics.

### 2022 partial reconciliation
`data/census/year-evidence-2022.json` records a material source-definition conflict. The FAA-hosted Boeing 2022 Statistical Summary's worldwide 2022 accident table does not list MU5735 even though CAAC and IATA establish the event. Boeing-table absence therefore cannot be interpreted as evidence of no qualifying event. The Boeing inclusion/exclusion semantics and the rest of the 2022 candidate universe require reconciliation before a year attestation.

### 2023 partial reconciliation
`data/census/year-evidence-2023.json` records that the inspected Boeing 2023 Statistical Summary reports no fatalities in the airplane operations it tracks and its 2023 worldwide table has no fatal listed accident; IATA independently reports zero fatal jet accidents in 2023. EASA ASR 2024 uses a broader worldwide large-aeroplane passenger/cargo universe and reports two fatal accidents / 77 fatalities, led by the ATR 72 Pokhara accident. These scope differences are preserved. 2023 remains unreconciled until the complete wider fatal set is mapped against the fixed Boeing-commercial-jet target and source completeness is evidenced.

### ICAO retrieval freeze
ICAO API retrieval is disabled from operational automation. AGGIORNA #22 empirically confirmed prior access is unusable for the project (HTTP 403). BSFM will not purchase paid ICAO calls under the current research plan. Event-level ICAO rows must not be reconstructed by new API calls or published contrary to licence terms. Public static ICAO reports/products may be assessed only within their demonstrated scope and do not reopen the retired API dependency.

## G2 — BLOCKED
Annual Boeing-family departures/cycles or another predeclared defensible exposure denominator are incomplete for 2010-2025. `data/exposure/source-inventory.json` now records inspected sustainable candidates:
- Boeing Statistical Summary: annual worldwide fleet-level traffic plus cumulative Boeing/type statistics, but no demonstrated annual Boeing-family matrix.
- U.S. DOT/BTS T-100 Segment: aircraft-type scheduled/performed departures and aircraft hours, but coverage is U.S. domestic plus international operations with a U.S./territory service point; foreign-to-foreign flights are excluded.
- ICAO Long Term Traffic Forecast product: public description exposes historical traffic and forecast/fleet functions, but does not establish a reproducible historical actual-departures matrix at BSFM Boeing-family-by-year granularity; forecast values cannot substitute for measured historical exposure.

No aggregate/cumulative statistic, fleet share, forecast or regional partial dataset is promoted into the primary baseline. `baseline_present=false` remains the only supported state.

## G3 — BLOCKED
Historical predictor records do not yet establish field-level public availability at simulated cutoffs. Dated official releases and archived/versioned public artifacts remain preferred evidence.

## G4 — BLOCKED
Downstream of G1-G3. Genuine paired OOS candidate-vs-exposure-baseline evaluation begins only after upstream PASS.

## Public/privacy/licensing state
Public UI keeps experimental/status boundaries. FAA SDR and NTSB AVALL remain supporting/descriptive sources with scope limitations. This public repository must contain no personal/private/sensitive user data or credential values. New annual/source evidence stores public scientific metadata, observations and locators rather than third-party report contents. ICAO raw/event-level API data is not to be published.

## Operational state
AGGIORNA #25 is the latest successful full workflow. Source SHA `971cdd6a1ec0576208191e2d18fe76fce2742c86` is workflow-verified and generated-state commit `ce33ea54b36613cf122e3201c2825a329700f656` was published by that run. The subsequent 2022/2023 G1 evidence and G2 source-inventory batch is repository evidence only until independently re-run through the applicable tests/workflow. G1-G4 remain BLOCKED.

## Exact next step
Continue the G1 census backward with 2021, using worldwide annual evidence to discover the candidate set and competent national investigation authorities plus an independent publisher to adjudicate each Boeing fatal-commercial-jet candidate; at the same time resolve the Boeing-2022/MU5735 inclusion-rule discrepancy and continue searching for a genuinely global historical Boeing-family/type departures-or-cycles source for G2, retaining every `year-ledger.json` row `reconciled=false` and `baseline_present=false` until the full evidence criteria are met.

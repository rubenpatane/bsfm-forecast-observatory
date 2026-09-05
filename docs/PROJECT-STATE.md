# BSFM Project State

Updated: 2026-09-05

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #21 (`33974695186`) completed successfully and is the last workflow-verified ICAO acquisition.
- Success verifies only checks actually executed; it does not establish predictive validity or open a scientific gate.

## Canonical documents
`AGENTS.md` is the constitution/privacy/bootstrap; `docs/MODEL-SPEC.md` the model contract; `docs/LABORATORY-PROTOCOL.md` the scientific protocol; `docs/NEW-CHAT.md` the fresh-session bootstrap; `docs/F-002-PREREGISTRATION-v1.md` the frozen F-002 evaluation; `docs/G1-G3-EVIDENCE-PLAN-v1.md` the detailed evidence plan.

## F-002
`forecasts/F-002.json` is frozen. Later evidence/refinements cannot rewrite it or add retroactive probabilities. The repository does not claim cryptographic proof of public publication on its declared 2026-08-19 cutoff.

## G1 — BLOCKED
`data/census/year-ledger.json` is the canonical 2010-2025 reconciliation ledger; keep years `reconciled=false` until evidenced. `data/census/icao-official-accidents-source.json` records the historical ICAO source contract. `bsfm/g1_census.py` normalizes conservatively and cannot open G1 by itself; tests enforce fail-closed behavior.

AGGIORNA #21 successfully acquired 4,669 ICAO Official Accidents rows across annual requests for 2010-2025, with returned records through 2022 and zero returned rows for 2023-2025. Those observations are retained as historical evidence/provenance only. Zero rows are not evidence of zero qualifying accidents.

### ICAO retrieval freeze
Effective 2026-09-05, ICAO API retrieval is disabled from all operational automation. The trial/API access is no longer treated as an available project dependency and BSFM will not purchase paid ICAO calls as part of the current research plan. `.github/workflows/autonomous-update.yml` contains no ICAO API call and does not require `ICAO_API_KEY`. `scripts/acquire_icao_g1.py` is retained only as historical/reproducibility code and must not be invoked by routine automation.

Previously acquired ICAO evidence may continue to be used within the licence constraints and with its original provenance. Event-level ICAO rows must not be reconstructed by new API calls, committed, published in Pages, or exposed in public artifacts unless redistribution rights are explicitly established. G1 completion must therefore reconcile the already-obtained ICAO snapshot with sustainable public/official alternatives (Boeing, EASA, NTSB and relevant national investigation authorities) rather than depend on future ICAO retrieval.

## G2 — BLOCKED
Annual Boeing-family departures/cycles or another predeclared defensible exposure denominator are incomplete for 2010-2025. Convenience proxies do not open G2.

## G3 — BLOCKED
Historical predictor records do not yet establish field-level public availability at simulated cutoffs.

## G4 — BLOCKED
Downstream of G1-G3. Genuine paired OOS candidate-vs-exposure-baseline evaluation begins only after upstream PASS.

## Public/privacy/licensing state
Public UI keeps experimental/status boundaries. FAA SDR and NTSB AVALL remain supporting/descriptive sources with scope limitations; nonfatal F-002 comparables cannot score as fatal-target hits. This public repository must contain no personal/private/sensitive user data or credential values. ICAO raw/event-level API data must not be committed, published in Pages, or exposed in public artifacts unless redistribution rights are explicitly established.

## Operational state
Workflow verification is established through AGGIORNA #21 (`33974695186`) for checks executed by that run. The post-#21 change disabling all future ICAO retrieval is committed but requires a later ordinary AGGIORNA run (which no longer calls ICAO) before that workflow revision can be called runtime-verified.

## Exact next step
Do not call ICAO again. Continue G1 using the evidence already obtained from AGGIORNA #21 plus sustainable official/public sources. Build the year-by-year Boeing fatal-accident reconciliation for 2010-2025 from Boeing/EASA/NTSB/national-authority evidence, treating the frozen ICAO snapshot as one historical cross-check. Resolve the 2023-2025 coverage gap entirely without ICAO API retrieval. Keep every year `reconciled=false` until G1 evidence criteria are actually met.

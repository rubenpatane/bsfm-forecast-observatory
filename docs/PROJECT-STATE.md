# BSFM Project State

Updated: 2026-09-05

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #21 (`33974695186`) completed successfully and is the last successful full workflow run.
- AGGIORNA #22 (`33975985882`) failed at the now-retired ICAO acquisition step. Pre-update verification completed successfully with **115 tests passed**, registry integrity OK and the scientific foundation correctly fail-closed. The ICAO step returned HTTP 403 at the 2019 request after returning rows for 2010–2018; all later workflow steps were skipped. This failed run is not a scientific regression and must not be retried against ICAO.
- Success/failure of CI verifies only checks actually executed; it does not establish predictive validity or open a scientific gate.

## Canonical documents
`AGENTS.md` is the constitution/privacy/bootstrap; `docs/MODEL-SPEC.md` the model contract; `docs/LABORATORY-PROTOCOL.md` the scientific protocol; `docs/NEW-CHAT.md` the fresh-session bootstrap; `docs/F-002-PREREGISTRATION-v1.md` the frozen F-002 evaluation; `docs/G1-G3-EVIDENCE-PLAN-v1.md` the detailed evidence plan.

## F-002
`forecasts/F-002.json` is frozen. Later evidence/refinements cannot rewrite it or add retroactive probabilities. The repository does not claim cryptographic proof of public publication on its declared 2026-08-19 cutoff.

## G1 — BLOCKED
`data/census/year-ledger.json` is the canonical 2010-2025 reconciliation ledger; keep years `reconciled=false` until evidenced. `data/census/icao-official-accidents-source.json` records the historical ICAO source contract. `bsfm/g1_census.py` normalizes conservatively and cannot open G1 by itself; tests enforce fail-closed behavior.

AGGIORNA #21 successfully acquired 4,669 ICAO Official Accidents rows across annual requests for 2010-2025, with returned records through 2022 and zero returned rows for 2023-2025. Those observations are retained as historical evidence/provenance only. Zero rows are not evidence of zero qualifying accidents.

### ICAO retrieval freeze
Effective 2026-09-05, ICAO API retrieval is disabled from all operational automation. AGGIORNA #22 empirically confirmed that the prior access is no longer usable for the project (HTTP 403 during acquisition). BSFM will not purchase paid ICAO calls as part of the current research plan. `.github/workflows/autonomous-update.yml` now contains no ICAO API call and does not require `ICAO_API_KEY`. `scripts/acquire_icao_g1.py` is retained only as historical/reproducibility code and must not be invoked by routine automation.

Previously acquired ICAO evidence may continue to be used within licence constraints and with its original provenance. Event-level ICAO rows must not be reconstructed by new API calls, committed, published in Pages, or exposed in public artifacts unless redistribution rights are explicitly established. G1 completion must reconcile the already-obtained ICAO snapshot with sustainable public/official alternatives.

### Sustainable G1 path
The primary global reconciliation source is now the Boeing Statistical Summary of Commercial Jet Airplane Accidents, cross-checked independently with EASA Annual Safety Reviews/fatal-accident appendices and authoritative national/regional investigation records. NTSB remains authoritative for its US scope but cannot alone establish a global census. The frozen ICAO #21 evidence is a historical cross-check, not the backbone of future acquisition.

## G2 — BLOCKED
Annual Boeing-family departures/cycles or another predeclared defensible exposure denominator are incomplete for 2010-2025. Boeing worldwide statistical summaries are the first sustainable source to inspect for family/year denominators. Convenience proxies do not open G2; no new ICAO API traffic retrieval is permitted.

## G3 — BLOCKED
Historical predictor records do not yet establish field-level public availability at simulated cutoffs. Dated official releases and archived/versioned public artifacts remain the preferred evidence. No future ICAO API access is assumed.

## G4 — BLOCKED
Downstream of G1-G3. Genuine paired OOS candidate-vs-exposure-baseline evaluation begins only after upstream PASS.

## Public/privacy/licensing state
Public UI keeps experimental/status boundaries. FAA SDR and NTSB AVALL remain supporting/descriptive sources with scope limitations; nonfatal F-002 comparables cannot score as fatal-target hits. This public repository must contain no personal/private/sensitive user data or credential values. ICAO raw/event-level API data must not be committed, published in Pages, or exposed in public artifacts unless redistribution rights are explicitly established.

## Operational state
AGGIORNA #21 (`33974695186`) is the last successful full run. AGGIORNA #22 (`33975985882`) is a documented expected-obsolete-path failure caused by the ICAO step that has since been removed. The current ICAO-free workflow revision is committed but not yet runtime-verified. Do not rerun #22 or any ICAO acquisition job.

## Exact next step
Continue without ICAO retrieval. Build the year-by-year Boeing fatal-accident candidate census for 2010–2025 from the Boeing worldwide Statistical Summary and EASA fatal-accident appendices, then reconcile candidates against NTSB/national investigation authorities. In parallel, inspect Boeing statistical-summary tables for genuine family/year exposure denominators for G2 without inferring missing cells. Resolve 2023–2025 entirely from sustainable sources. Keep every year `reconciled=false` and G1/G2/G3 BLOCKED until their evidence criteria are actually satisfied. A later ordinary ICAO-free AGGIORNA run is required only to runtime-verify the revised automation, not to obtain scientific evidence.

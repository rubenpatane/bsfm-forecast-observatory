# BSFM Project State

Updated: 2026-09-05

## Continuity
This is the live public checkpoint, not a full specification. Start with `AGENTS.md` and `docs/NEW-CHAT.md`. No personal/private/sensitive information or secret values may be recorded here.

## Last workflow-verified baseline
- F-002 remains frozen and experimental/unvalidated.
- `AGGIORNA` is the single operational workflow.
- AGGIORNA #21 (`33974695186`) completed successfully after ICAO G1 acquisition was connected through a repository secret.
- Success verifies only checks actually executed; it does not establish predictive validity or open a scientific gate.
- No ICAO API key value is stored in the repository; automation references the secret via environment only.

## Canonical documents
`AGENTS.md` is the constitution/privacy/bootstrap; `docs/MODEL-SPEC.md` the model contract; `docs/LABORATORY-PROTOCOL.md` the scientific protocol; `docs/NEW-CHAT.md` the fresh-session bootstrap; `docs/F-002-PREREGISTRATION-v1.md` the frozen F-002 evaluation; `docs/G1-G3-EVIDENCE-PLAN-v1.md` the detailed evidence plan.

## F-002
`forecasts/F-002.json` is frozen. Later evidence/refinements cannot rewrite it or add retroactive probabilities. The repository does not claim cryptographic proof of public publication on its declared 2026-08-19 cutoff.

## G1 — BLOCKED
`data/census/year-ledger.json` is the canonical 2010-2025 reconciliation ledger; keep years `reconciled=false` until evidenced. `data/census/icao-official-accidents-source.json` records the ICAO contract. `bsfm/g1_census.py` normalizes conservatively and cannot open G1 by itself; tests enforce fail-closed behavior. `scripts/acquire_icao_g1.py` performs authenticated annual acquisition without embedding the secret. AGGIORNA #21 successfully executed acquisition: 4,669 records across requested annual queries; observed records through 2022 and zero returned rows for 2023-2025. Zero rows are not evidence of zero qualifying accidents; coverage/update reconciliation is required. Real ICAO schema still requires evidence-driven inspection/adaptation; independent year-by-year reconciliation remains required.

## G2 — BLOCKED
Annual Boeing-family departures/cycles or another predeclared defensible exposure denominator are incomplete for 2010-2025. Convenience proxies do not open G2.

## G3 — BLOCKED
Historical predictor records do not yet establish field-level public availability at simulated cutoffs.

## G4 — BLOCKED
Downstream of G1-G3. Genuine paired OOS candidate-vs-exposure-baseline evaluation begins only after upstream PASS.

## Public/privacy state
Public UI keeps experimental/status boundaries. FAA SDR and NTSB AVALL remain supporting/descriptive sources with scope limitations; nonfatal F-002 comparables cannot score as fatal-target hits. This public repository must contain no personal/private/sensitive user data or credential values. `ICAO_API_KEY` is only a secret/environment-variable name. Third-party raw data must not be publicly committed unless redistribution rights are established.

## Operational state
Workflow verification is established through AGGIORNA #21 (`33974695186`) for checks executed by that run. Documentation introduced after #21 is committed state and needs a later AGGIORNA before being called workflow-verified.

## Exact next step
Inspect the actual ICAO Official Accidents artifacts/schema from AGGIORNA #21 without exposing secrets or publishing data contrary to source terms; adapt G1 normalization only from observed fields; determine why annual queries return no records for 2023-2025; then begin year-by-year Boeing filtering/deduplication and independent reconciliation. Keep every year `reconciled=false` until G1 evidence criteria are actually met.

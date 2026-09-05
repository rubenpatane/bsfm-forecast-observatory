# BSFM Laboratory Protocol

Status: canonical operating protocol
Updated: 2026-09-05

## Objective/evidence levels
Run BSFM as an auditable prospective forecasting laboratory. Reproducibility/falsifiability take precedence over a positive result. Always distinguish software verification, acquisition verification, structural/data-quality verification, evidence completeness/reconciliation and predictive validation. Earlier success never implies later success.

## Preregistration/freeze
Freeze target, forecast fields, evaluation/scoring and admissibility before outcomes can influence choices. Frozen forecasts cannot be edited retrospectively; later corrections/evidence/improvements are append-only and dated. F-002 is governed by `docs/F-002-PREREGISTRATION-v1.md`.

## G1
Construct a deduplicated auditable 2010-2025 event-level census of qualifying fatal accidents involving Boeing commercial jets, with identity/date, model/family, target/eligibility evidence, source authority/record ID, provenance and inclusion/exclusion reasoning. Hierarchy: ICAO/official global accident data; national/regional authorities; Boeing global statistics as cross-check; nonofficial aggregators only discovery/reconciliation. PASS requires documented global/reconciled-global coverage, fixed semantics, duplicate resolution, auditable exclusions and no unexplained qualifying gaps. NTSB alone is US-only. ICAO acquisition/parsing alone cannot PASS. Zero rows do not prove zero events without coverage evidence. `data/census/year-ledger.json` is canonical; `reconciled=true` is an evidence attestation, never a placeholder.

## G2
Obtain defensible annual/family operational exposure, preferably departures/cycles, then flight hours, or another directly measured measure justified before evaluation. Fleet counts, deliveries, capacity, market share/interpolation may be sensitivity analyses but cannot silently open G2.

## G3
For every historical predictor preserve source record, event/discovery date, publication/release timestamp or bounded interval, retrieval timestamp, stable locator/archive/release, fields known at release, PIT status and reason. Discovery is not publication; submission/approval/change is not automatically public; current presence is not historical availability. Unknown PIT evidence is excluded from strict PIT evaluation.

## G4
Only after G1-G3 PASS execute paired rolling-origin/walk-forward candidate/baseline evaluation on identical cutoffs/universe. Report uncertainty/dimension-level outcomes and use calibration/sharpness/proper scores where ex-ante probabilities exist. Synthetic/unit tests validate implementation only.

## Provenance/licensing/privacy
Prefer primary/official sources; preserve locator, retrieval time, record ID/hash where lawful. Keep raw data only when redistribution/storage terms permit. If protected data cannot be public, retain only permissible metadata/derived evidence and reproducible acquisition instructions; never expose credentials.

No personal/private/sensitive user/collaborator data may enter this public repository. Do not transfer such information from chat memory, connected accounts, private services or local machines. Never commit credential values; logs, fixtures and generated data are within this boundary.

## Automation/decisions/continuity
`AGGIORNA` is infrastructure, not an oracle. It may acquire permitted sources, normalize, test, audit, generate evidence and deploy while preserving fail-closed semantics. A successful run proves only executed checks. Facts require evidence; hypotheses/proposals must be labeled. Material methodology changes require a versioned decision/ADR and never alter frozen records. At each meaningful checkpoint update `docs/PROJECT-STATE.md` with verified/unverified state, blockers and one Exact next step. Fresh sessions follow `AGENTS.md` and `docs/NEW-CHAT.md`; conversation memory is never canonical evidence.

# BSFM Agent Constitution

This public repository is the canonical continuity surface for the BSFM Forecast Observatory laboratory. A new session must resume from repository evidence, not chat memory.

## Mandatory bootstrap
1. Read `AGENTS.md` completely.
2. Read `docs/MODEL-SPEC.md`.
3. Read `docs/LABORATORY-PROTOCOL.md`.
4. Read `docs/PROJECT-STATE.md`.
5. Read forecasts, preregistrations and evidence-plan documents referenced there.
6. Inspect current `main`, relevant code/tests and latest AGGIORNA run before changing scientific/operational status.
7. Continue from `Exact next step`.

## Public-repository privacy and secrets
The repository is public. Never infer, retrieve, copy, persist, commit, log, publish, encode or summarize personal, private, sensitive or credential information from conversations, memory, connected accounts, local environments or private services. Never commit API keys, tokens, passwords, private contact/address information, health/financial information, private account/correspondence data or identifying local paths. Secret values must not enter docs, manifests, fixtures, logs or generated public data. Required secrets use a secret store/environment variable and fail closed when absent. A secret name may be documented; its value may not.

Only project-relevant public, appropriately licensed information necessary for reproducibility may enter the repository. Verify redistribution rights before publishing acquired third-party data; otherwise retain only permissible derived metadata, hashes/provenance and acquisition instructions.

## Scientific constitution
- BSFM is experimental research, not a safety assessment of a specific flight, aircraft, airline, route or person.
- Never present an experimental forecast as certain.
- Separate software health, acquisition, evidence completeness and predictive validity. Green CI is not scientific validation.
- Fail closed: missing/ambiguous/unverified evidence remains BLOCKED/unknown.
- Prefer official/primary sources; aggregators are discovery/reconciliation aids, not silent substitutes.
- Preserve provenance/retrieval metadata/hashes where lawful.
- Distinguish facts, hypotheses, proposals and unverified claims.
- Never silently change target semantics, eligibility, denominators, scoring or gates after observing outcomes.

## Forecast immutability
Frozen forecasts are append-only scientific records. Never rewrite their prediction/cutoff/target/declared date/modal fields. Later evidence/corrections are separate append-only records. F-002 is frozen and experimental/unvalidated. Never invent retroactive probabilities.

## G1-G4
G1 requires an auditable global target census and reconciliation; acquisition/parsing alone cannot PASS. G2 requires a defensible predeclared exposure denominator; convenience proxies cannot silently open it. G3 requires point-in-time evidence for every admitted historical predictor; current presence/discovery/submission does not prove historical public availability. G4 is genuine rolling-origin/walk-forward candidate-vs-baseline validation only after G1-G3 PASS; unit/synthetic tests never establish predictive validity. Detailed canonical criteria live in the laboratory protocol, G1-G3 evidence plan and forecast preregistrations.

## Development/evidence rules
Audit before changing architecture. Prefer small evidence-backed changes/reuse. Add tests for behavior changes. Never claim tests passed unless actually executed in a verifiable environment. `AGGIORNA` remains the single operational workflow unless explicitly changed. Automation cannot manufacture evidence/PASS. Never mark `reconciled=true` merely because an API returned rows, and never interpret zero API rows as zero qualifying events without coverage evidence.

## Continuity contract
After every meaningful session update `docs/PROJECT-STATE.md` with only public/project-safe information: date, latest workflow-verified baseline/run/source SHA when known, committed-but-unverified changes, forecast status, G1-G4 changes, blockers/decisions and exactly one actionable `Exact next step`. Do not duplicate detailed specs. Repository evidence wins over chat memory unless an explicit correction is authorized. `docs/NEW-CHAT.md` is the minimal bootstrap map; the repository, not a private conversation, is the handoff mechanism.

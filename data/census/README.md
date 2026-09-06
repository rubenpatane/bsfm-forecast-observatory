# Historical target census working area

`public-data-v1.3-route-ledger.json` is the fail-closed geographic ledger for
the separately versioned BSFM-PD 1.3 model. It does not alter historical G1 v1
or F-002. A route receives a geographic decision only from authority evidence
for the operated segment's origin and destination; accident location, operator
and registration are deliberately insufficient.

This directory is intentionally **not** a completed ground-truth dataset yet.

Evaluation interval: 2010–2025 inclusive.

A year may move from `unresolved` to `reconciled` only after the annual source scopes have been checked and the Boeing commercial-jet fatal-event count has been reconciled from at least two independent publishers. A source merely mentioning an accident, or a cumulative manufacturer table, is not enough by itself.

Primary source families:

- ICAO annual Safety Reports — global scheduled commercial air transport; scope varies by edition and must be recorded verbatim. No new ICAO API retrieval is permitted; only sustainable public reports and the already frozen historical evidence may be used under the project rules.
- EASA Annual Safety Reviews and fatal-accident appendices — annual global/European tables; scope must be recorded per edition.
- National investigation authorities — event-level confirmation where annual tables are ambiguous.
- Boeing Statistical Summary of Commercial Jet Airplane Accidents — manufacturer/fleet triangulation; never sole global ground truth.
- Other independent aviation-safety publishers may be retained as reconciliation evidence when their methodology and scope are explicit; they do not replace authoritative event adjudication.

Important scope warning: annual totals from ICAO, EASA, Boeing and other publishers are not assumed to be interchangeable. Differences in MTOW threshold, scheduled vs broader commercial operation, aircraft category, accident definition, fatality definition and source-specific exclusions must be retained.

`year-evidence-YYYY.json` files are fail-closed research artifacts. They record partial annual reconciliation, source-scope conflicts and candidate links without changing the canonical year status. `reconciled=false` inside these artifacts is deliberate. A partial evidence file must never be interpreted as a zero-event attestation.

The machine-readable ledger is `year-ledger.json`. `reconciled=false` is deliberate until case-by-case evidence is complete. These placeholders MUST NOT satisfy the `historical_cases` scientific gate.

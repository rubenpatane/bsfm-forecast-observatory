# Historical target census working area

This directory is intentionally **not** a completed ground-truth dataset yet.

Evaluation interval: 2010–2025 inclusive.

A year may move from `unresolved` to `reconciled` only after the annual source scopes have been checked and the Boeing commercial-jet fatal-event count has been reconciled from at least two independent publishers. A source merely mentioning an accident, or a cumulative manufacturer table, is not enough by itself.

Primary source families:

- ICAO annual Safety Reports — global scheduled commercial air transport; scope varies by edition and must be recorded verbatim.
- EASA Annual Safety Reviews and fatal-accident appendices — annual global/European tables; scope must be recorded per edition.
- National investigation authorities — event-level confirmation where annual tables are ambiguous.
- Boeing Statistical Summary of Commercial Jet Airplane Accidents — manufacturer/fleet triangulation; never sole global ground truth.

Important scope warning: annual totals from ICAO, EASA and Boeing are not assumed to be interchangeable. Differences in MTOW threshold, scheduled vs broader commercial operation, aircraft category, accident definition and fatality definition must be retained.

The machine-readable ledger is `year-ledger.json`. `reconciled=false` is deliberate until case-by-case evidence is complete. These placeholders MUST NOT satisfy the `historical_cases` scientific gate.

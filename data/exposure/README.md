# Historical Boeing departures exposure

Status: construction; **not baseline-ready**.

`departures.jsonl` will contain one row per period × Boeing cohort. Required fields are `period`, `cohort`, `departures`, `source`, `scope`, and `provenance`.

The primary scientific baseline is departures-only and normalized within period. Global all-airline traffic totals are context/audit evidence, not Boeing-family denominators. A year is not complete until every preregistered Boeing cohort has a compatible denominator under one consistent scope. Missing cohorts, mixed scopes, missing provenance and zero-total periods fail closed.

Do not estimate family departures from fleet counts or accident counts. If authoritative Boeing-family departures cannot be reconstructed for a period, retain the gap and keep `baseline_present=false`.

`source-inventory.json` records official/sustainable source candidates and why they do or do not satisfy G2. A source with aircraft-type departures but only regional or U.S.-linked coverage remains partial-scope evidence; forecast traffic or fleet values are not historical measured exposure.

`iata-public-coverage-v1.json` records the maximum IATA evidence recoverable from public reports. It is reconciliation evidence only: aggregate 737 values are never split by variant, missing years remain explicit, and G2 stays fail-closed until a complete licensed cohort-year matrix exists.

`iata-annex4-public-sectors-v1.json` contains the numeric public Annex 4 observations currently verified. `g2-public-coverage-matrix-v1.json` maps those observations to the canonical cohort/year universe and records unresolved, missing and regional-only cells.

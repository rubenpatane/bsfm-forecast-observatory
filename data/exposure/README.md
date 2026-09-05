# Historical Boeing departures exposure

Status: construction; **not baseline-ready**.

`departures.jsonl` will contain one row per period × Boeing cohort. Required fields are `period`, `cohort`, `departures`, `source`, `scope`, and `provenance`.

The primary scientific baseline is departures-only and normalized within period. Global all-airline traffic totals are context/audit evidence, not Boeing-family denominators. A year is not complete until every preregistered Boeing cohort has a compatible denominator under one consistent scope. Missing cohorts, mixed scopes, missing provenance and zero-total periods fail closed.

Do not estimate family departures from fleet counts or accident counts. If authoritative Boeing-family departures cannot be reconstructed for a period, retain the gap and keep `baseline_present=false`.

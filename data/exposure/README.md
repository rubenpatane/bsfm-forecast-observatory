# Historical Boeing departures exposure

Status: construction; **not baseline-ready**.

`departures.jsonl` will contain one row per period × Boeing cohort. Required fields are `period`, `cohort`, `departures`, `source`, `scope`, and `provenance`.

The primary scientific baseline is departures-only and normalized within period. Global all-airline traffic totals are context/audit evidence, not Boeing-family denominators. A year is not complete until every preregistered Boeing cohort has a compatible denominator under one consistent scope. Missing cohorts, mixed scopes, missing provenance and zero-total periods fail closed.

Do not estimate family departures from fleet counts or accident counts. If authoritative Boeing-family departures cannot be reconstructed for a period, retain the gap and keep `baseline_present=false`.

`source-inventory.json` records official/sustainable source candidates and why they do or do not satisfy G2. A source with aircraft-type departures but only regional or U.S.-linked coverage remains partial-scope evidence; forecast traffic or fleet values are not historical measured exposure.

## Public T-100 research path

`bts-t100-public-source.json` and `bsfm.bts_t100` define a separate adapter for
the official aggregated T-100 table. It deliberately emits
`scope=us_linked_commercial` and `global_g2_eligible=false`. A complete regional
matrix therefore cannot change the global BSFM 1.2 G2 status. Any forecast use
requires the separately versioned prospective decision described in
`docs/PUBLIC-DATA-VARIANT-DECISION-v1.md`. BSFM-PD 1.4 reuses the accepted
nine-cohort regional matrix under the frozen online-only prospective protocol
in `docs/PUBLIC-DATA-PROSPECTIVE-v1.4.md`; it does not promote global G2.

# Public-data extended-training feasibility

Status: COMPLETE — DO NOT PROMOTE

Date: 2026-09-06

## Question

Can the public-data BSFM line gain enough historical training and out-of-sample
event folds using only sources downloadable online, without changing the active
BSFM-PD 1.4 forecast or silently redesigning the estimator?

## Online evidence acquired

The official BTS T-100 Segment downloads cover 1990–2025. The checked-in audit
records 36 archive hashes, 324 annual cohort cells, 3,888 monthly cohort cells,
133,799,417 mapped Boeing performed departures and zero invalid rows. Sixteen
mixed aircraft-code-615 departures are retained losslessly by the already
defined `737-Classic+NG` cohort. The scope remains
`us_linked_commercial`; foreign-to-foreign operations are absent, so global G2
remains BLOCKED.

The official NTSB Pre-2008 and current AVALL databases were downloaded and
hashed. Their privacy-minimal derived discovery files contain 99 and 53 broad
Boeing fatal-event candidates respectively. The feasibility selector identifies
20 pre-2010 scenario outcomes under explicit domestic Part 121 or listed
U.S.-linked route rules, then retains the three already authority/PIT-reviewed
2010–2025 BSFM-PD outcomes. The 20 older rows remain `SCENARIO_ONLY`: a complete
route and prospective-v2 target adjudication was not performed.

## PIT result

The exact downloaded NTSB bytes are conservatively known public only by the
2026-09-06 retrieval checkpoint. They may be used now for discovery and
retrospective scoring, but their present-day database fields cannot be inserted
into earlier training cutoffs. NTSB administrative approval dates were also
tested as an explicitly invalid counterfactual; they are not publication dates
and are never admitted as PIT evidence.

Consequently the admissible 1990–2025 run contains 137 non-overlapping 90-day
folds and 15 event-bearing folds, but the older candidate rows supply no
historical training signal. The run is useful for diagnosing the frozen model,
not for claiming that the additional outcomes were learned at the time.

## Prior-mass diagnosis

With the frozen BSFM-PD prior, each of nine candidate cohorts receives 0.5
pseudo-events and 1,000,000 pseudo-departures. The pooled baseline receives
those quantities only once. The candidate therefore starts with nine times the
total prior mass.

That unequal-prior run appears positive: mean log-score improvement
`+0.1130865826`, with paired bootstrap 90% interval
`[+0.0475368234, +0.1824773010]`. Because the older rows were unavailable for
training and the advantage exists before learning them, this is prior-driven
and is not evidence of predictive skill.

An explicit sensitivity matches total prior mass across candidate and baseline.
Its improvement is `-0.0163818330`, with 90% interval
`[-0.0330389484, +0.0017098171]`. The candidate is worse on average and the
interval crosses zero.

For value-of-information only, the invalid administrative-date counterfactual
allows older rows into later folds and yields a small matched-prior improvement
of `+0.0069196541` with 90% interval
`[+0.0001210106, +0.0125794169]`. This indicates that verified historical
publication evidence could be useful; it cannot substitute for that evidence,
and it cannot become a validation result after the outcomes and sensitivities
have already been inspected.

## Decision

- Do not alter or replace active BSFM-PD 1.4.
- Do not reinterpret the frozen-prior result as successful training.
- Do not backfill current NTSB values into historical cutoffs.
- Treat a balanced-prior estimator, enlarged historical taxonomy or changed
  interval as a separately preregistered future model version.
- Retain the public-source artifacts and negative/inconclusive audit so the
  result cannot be optimized away later.

F-002 is untouched. Historical G1 v1 remains 14/16 BLOCKED. Target Taxonomy v2
remains prospective only. Global G2/G3/G4 remain BLOCKED. The active prospective
forecast `PD14-20260907-7fa7c48bc555` remains immutable and non-overlapping.

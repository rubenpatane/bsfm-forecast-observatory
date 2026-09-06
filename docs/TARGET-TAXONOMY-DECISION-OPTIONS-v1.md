# BSFM Target Taxonomy Decision Options v1

Status: DECISION RECORDED — OPTION B SELECTED
Date: 2026-09-06
Decision date: 2026-09-06
Applies to: unresolved G1 boundaries in 2014 and 2020

## Decision

**Option B is selected.** BSFM adopts a new prospective target taxonomy for future forecasts only. The adopted rule is versioned separately in `docs/TARGET-TAXONOMY-v2-PROSPECTIVE.md` and `data/census/prospective-target-taxonomy-v2.json`.

This decision does **not** reclassify F-002, MH370, MH17, PS752, or the current historical G1 v1 census. G1 v1 therefore remains 14/16 and BLOCKED.

## Purpose

G1 has 14/16 annual cells reconciled. The remaining two cells are not ordinary evidence gaps:

- 2014: MH370 (missing-aircraft boundary) and MH17 (hostile/unlawful-action boundary);
- 2020: PS752 (hostile/unlawful-action boundary).

The frozen F-002 target is `next_fatal_accident_involving_boeing_commercial_jet`. The frozen evaluation protocol requires an accident, a Boeing commercial jet, attributable human fatality and sufficient authoritative evidence; materially disputed qualification remains `PENDING`. The canonical model specification also says event-universe semantics must be fixed before scoring and ambiguity remains unresolved.

The decision therefore separates prospective taxonomy design from retrospective historical adjudication.

## Non-negotiable constraints

Any future rule must:

1. be versioned and dated;
2. apply symmetrically to all comparable events, not only MH370/MH17/PS752;
3. state treatment of intentional hostile/unlawful acts;
4. state treatment of missing-aircraft events and the evidence threshold for qualification;
5. preserve competent-authority evidence and source-taxonomy disagreements;
6. never rewrite F-002 or its frozen preregistration;
7. state separately whether it governs only future forecasts, a new historical-census version, or both;
8. never be presented as though it had existed at the F-002 cutoff if it did not.

## Option A — Keep current historical G1 unresolved

Rule action: no new target-taxonomy rule is adopted for the current G1 version.

Consequences:
- 2014 and 2020 remain `reconciled=false`;
- G1 remains BLOCKED at 14/16;
- G4 remains blocked independently by G2/G3 anyway;
- no retrospective researcher degree of freedom is introduced;
- future BSFM forecasts should use a new prospective target specification that resolves these boundaries before their cutoffs.

Scientific advantage: strongest protection against post-outcome target editing.

Cost: current historical G1 can never reach 16/16 under this version unless genuinely pre-existing authoritative project semantics are discovered.

## Option B — Create a new prospective taxonomy for future forecasts only — SELECTED

Rule action: version a new target specification now, but declare it inapplicable to F-002 and to the current historical G1 attestation.

Consequences:
- current G1 remains 14/16 BLOCKED;
- future forecasts gain deterministic treatment of hostile/unlawful and missing-aircraft events;
- a later historical study may use the new rule only as a clearly labelled new analysis/version, not as proof that the old G1 was pre-specified.

Scientific advantage: solves the ambiguity going forward without pretending the rule was frozen earlier.

Cost: does not unblock current G1.

### Adopted prospective semantics

For future governed forecasts:
- the primary target is a fatal aviation **safety accident** involving a Boeing commercial jet;
- officially classified deliberate hostile/security/unlawful-interference events are excluded from the primary target but retained in a parallel descriptive census;
- missing aircraft remain `PENDING_MISSING` until competent authority evidence establishes accident/equivalent fatal loss plus attributable fatality;
- external, ground and other-aircraft fatalities remain eligible when authoritatively attributable;
- unknown commercial status, identity conflicts or material taxonomy disagreement remain fail-closed pending states.

See `docs/TARGET-TAXONOMY-v2-PROSPECTIVE.md` for the full adopted specification.

## Option C — Version a new historical-census taxonomy and re-run G1 as a new analysis

Rule action: adopt a rule now and create a distinctly versioned historical census whose target semantics explicitly differ from the current unresolved census.

Required safeguards:
- preserve the 14/16 current census unchanged as the pre-decision record;
- identify the new census/version as post-2026-09-06 taxonomy;
- re-adjudicate **all** 2010–2025 events under the new rule, not only the three boundary cases;
- document every event whose membership changes;
- do not claim the new rule was preregistered for F-002;
- decide separately whether the new census is suitable for training future model versions.

Scientific advantage: permits a complete internally consistent dataset for future research.

Cost: it is a new post-hoc historical analysis, not a retroactive completion of the original target semantics.

## Candidate rule dimensions

### Hostile / unlawful action

The selected prospective rule excludes officially classified deliberate hostile/unlawful/security events from the primary safety-accident target and retains them in a parallel descriptive census. The classification must come from competent official evidence, not media or model inference.

### Missing aircraft

The selected prospective rule keeps a missing aircraft pending until competent authority evidence establishes accident/equivalent fatal loss and attributable fatality. Complete wreckage or probable cause is not required once that threshold is met.

### Time of qualification

Event occurrence date remains distinct from later adjudication/publication date. Later evidence may resolve outcome membership, while predictor point-in-time availability remains governed independently by G3.

## Current state after the decision

The repository remains fail-closed for the historical G1 v1:
- MH370 = unresolved;
- MH17 = unresolved;
- PS752 = unresolved;
- 2014 = 4/6;
- 2020 = 4/6;
- G1 v1 = BLOCKED.

The prospective v2 taxonomy governs only future forecasts created after adoption. It does not alter any frozen forecast or historical candidate decision.

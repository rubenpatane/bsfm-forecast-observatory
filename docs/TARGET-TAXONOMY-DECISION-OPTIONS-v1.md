# BSFM Target Taxonomy Decision Options v1

Status: DECISION ANALYSIS — NON-CANONICAL / DOES NOT CHANGE F-002 OR G1
Date: 2026-09-06
Applies to: unresolved G1 boundaries in 2014 and 2020

## Purpose

G1 has 14/16 annual cells reconciled. The remaining two cells are not ordinary evidence gaps:

- 2014: MH370 (missing-aircraft boundary) and MH17 (hostile/unlawful-action boundary);
- 2020: PS752 (hostile/unlawful-action boundary).

The frozen F-002 target is `next_fatal_accident_involving_boeing_commercial_jet`. The frozen evaluation protocol requires an accident, a Boeing commercial jet, attributable human fatality and sufficient authoritative evidence; materially disputed qualification remains `PENDING`. The canonical model specification also says event-universe semantics must be fixed before scoring and ambiguity remains unresolved.

This document therefore does **not** choose a rule. It makes the remaining decision explicit and separates prospective taxonomy design from retrospective historical adjudication.

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

## Option B — Create a new prospective taxonomy for future forecasts only

Rule action: version a new target specification now, but declare it inapplicable to F-002 and to the current historical G1 attestation.

Consequences:
- current G1 remains 14/16 BLOCKED;
- future forecasts gain deterministic treatment of hostile/unlawful and missing-aircraft events;
- a later historical study may use the new rule only as a clearly labelled new analysis/version, not as proof that the old G1 was pre-specified.

Scientific advantage: solves the ambiguity going forward without pretending the rule was frozen earlier.

Cost: does not unblock current G1.

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

## Candidate rule dimensions if a new taxonomy is created

The eventual specification should answer these questions without reference to whether an individual case helps model performance:

### Hostile / unlawful action
Possible rule families include:
- exclude intentional hostile/unlawful/security acts from the safety-accident target;
- include an occurrence when the competent Annex 13/safety authority classifies it as an accident, regardless of initiating hostile action;
- define a dedicated security-event class outside the accident target but retain it in a parallel descriptive census.

No choice is endorsed here.

### Missing aircraft
The rule must state when a missing commercial jet becomes a qualifying fatal accident. Possible evidence thresholds include:
- competent authority final classification as an accident;
- sufficient authoritative evidence of destruction/fatality even if the complete sequence/cause is unknown;
- exclusion/pending status until a defined investigation threshold is met.

No choice is endorsed here.

### Time of qualification
The rule must also distinguish event occurrence date from later adjudication/publication date. Historical outcome membership can use later authoritative evidence, but predictor point-in-time availability remains a separate G3 question.

## Current recommendation encoded by the repository

Until a decision is explicitly made, the repository remains fail-closed:
- MH370 = unresolved;
- MH17 = unresolved;
- PS752 = unresolved;
- 2014 = 4/6;
- 2020 = 4/6;
- G1 = BLOCKED.

This document is a decision aid only. Committing it does not select Option A, B or C and does not alter any forecast, candidate decision or gate.

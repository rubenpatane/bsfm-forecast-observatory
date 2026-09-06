# BSFM Target Taxonomy v2 — Prospective

Status: ADOPTED — PROSPECTIVE ONLY
Adopted: 2026-09-06
Applies to: BSFM forecasts created after this adoption date, beginning with the next new forecast after F-002
Does not apply to: F-002, its preregistration, or the current historical G1 v1 census

## 1. Purpose

This specification removes target-semantics ambiguity **before future outcomes occur**. It defines the primary BSFM target as a fatal **aviation safety accident** involving a Boeing commercial jet.

It is intentionally non-retroactive. The unresolved 2014/2020 G1 v1 cells remain unresolved; this document must never be cited as evidence that MH370, MH17 or PS752 had a pre-existing BSFM classification at the F-002 cutoff.

## 2. Primary prospective target

A future occurrence qualifies for the primary target only when all of the following are satisfied:

1. a Boeing jet in the adopted commercial-air-transport universe is involved;
2. the occurrence is an aviation **safety accident**, not an officially classified deliberate hostile/security/unlawful-interference event;
3. at least one human fatality is authoritatively attributable to the occurrence;
4. aircraft identity and commercial-operation status are supported by competent-authority or equivalent authoritative evidence;
5. any material target-membership ambiguity is resolved by the rules below; otherwise status is `PENDING`.

Cause, probable cause and complete accident sequence need not be known for target membership if the competent authority has already established the occurrence as an accident and the other requirements are satisfied.

## 3. Deliberate hostile / unlawful / security events

### Rule

Exclude from the **primary safety-accident target** an occurrence that a competent investigating authority or recognized aviation-security authority officially classifies as deliberate hostile action, unlawful interference, terrorism, sabotage, intentional attack or intentional destruction rather than an unintentional safety accident.

Do not infer this classification from media reporting, political claims, operator statements or model output.

### Treatment

- primary target decision: `EXCLUDE_SECURITY`
- retain the event in a separate descriptive security/unlawful-interference census;
- preserve the authority classification and any disagreement among sources;
- never silently delete the occurrence from the research record.

### Precedence

If an Annex 13-style investigation is conducted for an occurrence but competent evidence establishes that the initiating event was deliberate hostile/unlawful interference, the prospective primary BSFM target uses `EXCLUDE_SECURITY`. The existence of a safety investigation does not by itself convert a deliberate security event into the primary safety-accident target.

## 4. Missing aircraft

### Rule

A missing commercial jet is **not automatically included or excluded**.

Use `PENDING_MISSING` until authoritative evidence establishes both:

1. the competent authority formally treats/classifies the occurrence as an accident or equivalent fatal loss under the applicable investigation framework; and
2. at least one human fatality is authoritatively established or formally presumed/deemed attributable to the occurrence.

Once both conditions are satisfied, the occurrence may be included even if the wreckage is incomplete, the full sequence is unknown, or probable cause remains unresolved.

If the competent authority instead establishes a deliberate hostile/security/unlawful-interference event, Section 3 takes precedence and the event is `EXCLUDE_SECURITY` from the primary target.

## 5. Fatality semantics

A qualifying fatality may be:

- aboard the Boeing aircraft;
- on the ground;
- aboard another aircraft involved in the same occurrence;
- another human fatality that the competent investigation attributes to the occurrence.

Do not require an onboard fatality. Preserve onboard and external fatality counts separately whenever the sources permit.

For delayed deaths, follow the competent authority's final injury/fatality classification rather than inventing an independent BSFM time threshold.

## 6. Commercial-air-transport status

Commercial status must be established from authoritative operation evidence, not operator-name inference. Unknown or materially conflicting operation status remains `PENDING`.

The Boeing cohort taxonomy remains separate from this document and must map the aircraft to the adopted target universe without proxy inference.

## 7. Evidence hierarchy and disagreement

Preferred evidence order for target membership:

1. competent accident-investigation authority / State investigation record;
2. official aviation-security or government authority where the disputed dimension is deliberate hostile/unlawful action;
3. accredited-representative or manufacturer safety evidence for corroboration;
4. independent global safety-statistical source for reconciliation.

A lower-priority source must not silently override a competent authority. Material disagreement is recorded explicitly and, when it changes target membership, remains `PENDING` until adjudicated under this specification.

## 8. Time and point-in-time separation

Outcome membership and predictor availability are different questions.

- The event occurrence date determines where the outcome belongs chronologically.
- Later authoritative evidence may resolve an outcome from `PENDING` to include/exclude.
- That later evidence must **not** be made available to predictors at an earlier simulated cutoff.
- G3 PIT rules continue to govern predictor leakage independently.

## 9. Decision states

Prospective event adjudication uses these explicit states:

- `INCLUDE_ACCIDENT`
- `EXCLUDE_SECURITY`
- `EXCLUDE_NONCOMMERCIAL`
- `EXCLUDE_NONBOEING`
- `PENDING_MISSING`
- `PENDING_OPERATION`
- `PENDING_IDENTITY`
- `PENDING_TAXONOMY`

Only `INCLUDE_ACCIDENT` enters the primary fatal-safety-accident outcome set.

## 10. Non-retroactivity

This specification is adopted after F-002. Therefore:

- F-002 remains unchanged and frozen;
- current historical G1 v1 remains 14/16 with 2014 and 2020 unresolved;
- MH370, MH17 and PS752 are **not** reclassified by this document;
- any future historical re-analysis using v2 must be a separately versioned study and must re-adjudicate the entire historical interval symmetrically.

## 11. Change control

Any future modification requires a new version, adoption date and explicit applicability statement before it can govern a new forecast. No taxonomy version may be edited in place after an outcome in its governed forecast period becomes known.

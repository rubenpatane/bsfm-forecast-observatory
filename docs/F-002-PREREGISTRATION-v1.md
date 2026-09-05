# F-002 Prospective Evaluation Preregistration v1

Status: FROZEN EVALUATION SPECIFICATION
Preregistered: 2026-09-05
Applies to: `forecasts/F-002.json`
Forecast cutoff declared in F-002: 2026-08-19
Purpose: define evaluation rules before the F-002 modal forecast window and before observing the qualifying target outcome.

## 1. Non-retroactivity

This document does not modify F-002. F-002 remains the immutable forecast object and retains its existing integrity hash. This protocol only fixes how later outcomes will be adjudicated and reported.

No future observation, refinement, comparable case, source update, model change, or outcome may be used to alter the original F-002 prediction or to choose a more favorable scoring rule after the fact.

If this protocol is later improved, the new version must be append-only, dated, and must not replace this version for scoring F-002 unless the change was committed before the relevant outcome and is explicitly shown not to use outcome information. Any ambiguity is resolved conservatively against a success claim.

## 2. Frozen F-002 prediction to be evaluated

Target: next fatal accident involving a Boeing commercial jet.

Declared forecast dimensions:
- modal week: 2026-10-05 through 2026-10-11 inclusive;
- modal day: 2026-10-08;
- primary family/variant: Boeing 737-800 / 737 NG;
- secondary family/variant: Boeing 737 MAX 8;
- phase: final approach / landing;
- primary event class: SCF-NP / landing-gear-structural-operational cluster;
- alternative event class: propulsion;
- geography: Europe / North America / APAC, explicitly not treated as a discriminating prediction;
- MSN: unsupported;
- operator: unsupported.

The repository history is not claimed to prove that F-002 was publicly published on 2026-08-19. Its file explicitly records that the exact original creation time is not established. This limitation must remain visible in any scientific claim.

## 3. Target adjudication

The target outcome is the chronologically next event after the F-002 cutoff that satisfies all of the following:
1. an accident rather than merely a service-difficulty report, incident report, maintenance finding, or unverified allegation;
2. involves a Boeing commercial jet aircraft;
3. is fatal, meaning at least one human fatality attributable to the accident under the authoritative accident record;
4. has sufficient authoritative evidence to establish event date, aircraft model/family, fatal status and relevant phase/class dimensions used for scoring.

Target adjudication must use authoritative accident-investigation or civil-aviation sources where available. News reports may be used for discovery but are not sufficient alone for final scientific adjudication when an authoritative record is reasonably obtainable.

If two qualifying accidents occur on the same UTC date and chronology cannot be established reliably, the primary target is marked `AMBIGUOUS` and both are reported; no favorable tie-breaking is allowed.

If the qualification of the apparent next event remains materially disputed or incomplete, scoring remains `PENDING` rather than selecting a convenient interpretation.

## 4. No binary overall "hit" from a composite forecast

F-002 contains several dimensions. A single post-hoc binary label would conceal important misses and create researcher degrees of freedom. Therefore the canonical result is a vector of dimension-level outcomes, not an all-purpose hit/miss label.

Required result vector:
- target qualification: QUALIFIED / NOT_QUALIFIED / PENDING / AMBIGUOUS;
- temporal-week result;
- temporal-day result;
- aircraft-family result;
- phase result;
- event-class result;
- geography: descriptive only;
- MSN/operator: not scored.

A public summary may say that one or more dimensions matched, but must enumerate the misses with equal prominence. It must not call F-002 "validated" because one event resembles part of the forecast.

## 5. Temporal scoring

### 5.1 Modal week
`WEEK_EXACT = 1` only if the qualifying target event date is from 2026-10-05 through 2026-10-11 inclusive. Otherwise `WEEK_EXACT = 0`.

No grace days are added to the frozen modal week.

### 5.2 Modal day
`DAY_EXACT = 1` only if the qualifying target event date is 2026-10-08 in the local civil date at the accident location. Otherwise `DAY_EXACT = 0`.

UTC date is retained as provenance where available, but no UTC/local conversion may be chosen opportunistically to create a match. If the authoritative event date is unambiguous, that civil date controls.

### 5.3 Distance diagnostics
In addition to exact indicators, report signed and absolute day distance from 2026-10-08. These are diagnostics, not a mechanism for redefining a miss as a hit.

## 6. Aircraft-family scoring

Canonical mutually exclusive categories:
- `PRIMARY_EXACT`: Boeing 737-800 variant;
- `PRIMARY_FAMILY`: other Boeing 737 NG variant compatible with the frozen primary family hypothesis;
- `SECONDARY`: Boeing 737 MAX 8;
- `OTHER_BOEING`: qualifying Boeing commercial jet outside the above hypotheses;
- `UNKNOWN`: authoritative model identification insufficient.

Customer-code variants of the 737-800 may count as `PRIMARY_EXACT` when authoritative type/model mapping establishes they are 737-800 variants. A MAX aircraft must never be silently mapped into NG.

The primary and secondary predictions must always remain distinguishable in reporting. A secondary match is not reported as a primary-family hit.

## 7. Flight-phase scoring

Canonical phase match is `PHASE_MATCH = 1` only when authoritative evidence places the accident in final approach or landing, including an equivalent controlled taxonomy mapping fixed independently of the outcome.

Takeoff, climb, cruise, descent without final-approach qualification, taxi, standing, maintenance and unknown phase are not matches.

If phase cannot yet be established authoritatively, result is `UNKNOWN/PENDING`, not a miss or hit selected from press wording.

## 8. Event-class scoring

Primary event-class assessment must preserve the frozen wording: `SCF-NP / landing-gear-structural-operational cluster`.

Report separately:
- `PRIMARY_CLASS_MATCH` for evidence compatible with the frozen primary cluster;
- `ALTERNATIVE_PROPULSION_MATCH` for the frozen propulsion alternative;
- `OTHER_CLASS`;
- `UNKNOWN/PENDING`.

The alternative propulsion class must never be combined with the primary class to claim that the primary event-class prediction succeeded.

Final class mapping should preferentially use established accident taxonomies (for example occurrence categories from authoritative investigation records) and must retain the source evidence used for mapping.

## 9. Geography, MSN and operator

Geography is not scored because F-002 explicitly lists Europe, North America and APAC as not reliably separable. It may be reported descriptively only.

MSN and operator are not scored because F-002 explicitly records them as unsupported/null. Their later identity cannot be represented as predictive success or failure.

## 10. Prospective versus reconstructed status

F-002 is an experimental frozen forecast with a declared 2026-08-19 cutoff, but the file states that exact original creation time is not established and the later repository commit is not cryptographic proof of publication on that date.

Therefore two claims must remain separate:
1. `forecast-content frozen`: supported by the current immutable repository artifact and integrity controls from the time it entered the repository;
2. `publicly preregistered on 2026-08-19`: NOT ESTABLISHED.

This preregistration, committed before the modal window, strengthens prospective evaluation of the scoring rules but does not retroactively establish publication of F-002 at its declared cutoff.

## 11. Baseline and model-skill evaluation

F-002 outcome adjudication and BSFM model validation are different questions.

A dimension match can be reported immediately after authoritative target adjudication. Predictive skill cannot be claimed from a single F-002 event.

Scientific model-skill evaluation remains gated:
- G1: complete/defensible global qualifying-event census;
- G2: defensible Boeing family/year exposure denominators;
- G3: point-in-time predictor availability sufficient to prevent historical leakage;
- G4: genuine out-of-sample candidate-versus-baseline evaluation and calibration.

Until G1-G3 pass, G4 remains BLOCKED.

The primary comparator for model skill must be an exposure-based baseline fixed without using evaluation outcomes. Family prevalence, fleet counts or other proxies may be explored descriptively but may not be substituted for missing exposure merely to obtain a favorable comparison.

## 12. Probabilistic scoring

Proper scoring rules are the preferred canonical tools when BSFM emits genuine predictive probabilities. They reward calibrated probabilistic forecasts and avoid incentives created by ad-hoc accuracy measures.

For future binary event probabilities, preregister Brier score and logarithmic score before evaluation. For full time-to-event predictive distributions, use a proper distributional score appropriate to the forecast representation and account explicitly for censoring where relevant.

F-002 itself contains modal categorical/time predictions but does not contain a complete calibrated predictive probability distribution. Therefore this protocol MUST NOT invent probabilities retrospectively in order to calculate Brier, log, CRPS or survival scores for F-002.

F-002 is scored using the frozen dimension-level rules above. Proper probabilistic scoring applies prospectively to later forecasts only when the probabilities/distributions themselves were frozen before the outcome.

## 13. Repeated prospective evaluation

One forecast cannot establish calibration or superiority. Future BSFM forecasts intended for scientific comparison must be evaluated sequentially under a fixed protocol.

Preferred design:
- rolling-origin / walk-forward forecasting;
- training and feature construction use only information admissible at each cutoff;
- forecasts are frozen before outcomes;
- candidate and baseline predictions are both recorded at the same cutoff;
- no random cross-validation that allows future observations to inform past folds;
- report every eligible forecast, including failures;
- preserve missing/blocked forecasts rather than silently excluding difficult periods.

Aggregate model claims require a sufficient prospective or genuinely point-in-time reconstructed sample. No fixed minimum number of events is invented here; uncertainty intervals and power/sensitivity analysis must accompany any later threshold chosen for a scientific claim.

## 14. Multiple dimensions and multiplicity

Family, time, phase and event class are separate hypotheses. They must not be searched after the outcome for the most flattering subset.

Canonical reporting always includes the complete result vector. Any later composite score must be specified prospectively and validated for its statistical interpretation before use. This v1 protocol intentionally does not assign arbitrary weights to the dimensions.

Exploratory analyses may be performed after the outcome only if clearly labelled `POST-HOC / EXPLORATORY` and kept separate from the preregistered F-002 evaluation.

## 15. Falsification and prohibited claims

F-002 is not a validated predictive model regardless of the outcome of one forecast.

The following are prohibited:
- declaring validation from a partial or complete F-002 match;
- moving the modal window after observing the event;
- broadening 737 NG/MAX definitions after the event to manufacture a family match;
- using a nonfatal comparable as the fatal target;
- treating an FAA SDR as the target accident without authoritative accident qualification;
- using geography, operator or MSN as successful predictions when F-002 did not discriminate/predict them;
- assigning retrospective probabilities to F-002;
- suppressing misses while highlighting matches;
- opening G4 while G1-G3 remain unsatisfied.

A failure on any dimension remains permanently visible. If no qualifying target occurs in the modal week/day, the corresponding exact temporal predictions are misses even if a later target resembles the aircraft/phase/class hypotheses.

## 16. Outcome record requirements

When the qualifying target is adjudicated, create an append-only outcome artifact containing at minimum:
- forecast id and forecast integrity hash;
- this preregistration path and commit identity;
- authoritative event identifiers and sources;
- event date/time and location where established;
- aircraft model/family;
- fatalities and target-qualification rationale;
- phase evidence;
- event-class evidence;
- complete dimension-level result vector;
- temporal distance diagnostics;
- unresolved fields explicitly marked unknown/pending;
- adjudication timestamp;
- code/version used for deterministic scoring, if applicable.

Corrections to source facts must be versioned rather than silently overwriting the original adjudication.

## 17. Scientific rationale

The protocol follows the forecasting principle that evaluation rules should be fixed independently of realized outcomes and that probabilistic forecasts, when available, should be assessed with proper scoring rules. Calibration and sharpness are distinct properties; useful probabilistic forecasts should seek sharpness subject to calibration. For a rare-event, time-dependent problem, temporal ordering and point-in-time feature admissibility are essential to prevent leakage.

This protocol is deliberately conservative. Its purpose is not to maximize the probability that F-002 will be called correct. Its purpose is to make the eventual result interpretable, reproducible and difficult to improve retrospectively.

## 18. References informing the protocol

- Gneiting, T. & Raftery, A. E. (2007), Strictly Proper Scoring Rules, Prediction, and Estimation, Journal of the American Statistical Association 102(477), 359-378. DOI: 10.1198/016214506000001437.
- Gneiting, T., Balabdaoui, F. & Raftery, A. E. (2007), Probabilistic Forecasts, Calibration and Sharpness, Journal of the Royal Statistical Society Series B 69(2), 243-268. DOI: 10.1111/j.1467-9868.2007.00587.x.
- Waghmare, K. & Ziegel, J. (2026), Proper Scoring Rules for Estimation and Forecast Evaluation, Annual Review of Statistics and Its Application 13, 271-296. DOI: 10.1146/annurev-statistics-042424-050626.

## 19. Freeze rule

This v1 document becomes the canonical F-002 evaluation preregistration at its first commit to `main`. The commit timestamp and Git object provide the repository evidence for when these evaluation rules became public in this repository.

Any future amendment must preserve this file and identify itself as a later version. Outcome knowledge must never be used to alter this v1 scoring specification.

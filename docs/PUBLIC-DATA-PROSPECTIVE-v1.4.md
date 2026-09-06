# BSFM-PD 1.4 Public-Online Prospective Protocol

Status: **PREREGISTERED FOR PROSPECTIVE UNVALIDATED FORECASTS**  
Adopted: 2026-09-06  
Canonical contract: `config/model-public-data-v1.4.json`

## Purpose

BSFM-PD 1.4 makes the research cycle operational using only evidence that can
be retrieved lawfully online without credentials: BTS T-100 exposure, NTSB
AVALL discovery/outcome material and public competent-authority records. It
issues immutable experimental forecasts so genuinely prospective evidence can
accumulate. It does not claim that the model is validated.

## Non-retroactivity

This version does not modify BSFM 1.2, F-002, historical G1 v1 or the observed
BSFM-PD 1.3 result. Version 1.3 remains underpowered and descriptively worse
than its pooled exposure baseline. Version 1.4 retains that negative result and
does not change target, scope, cohorts, estimator, exposure rule, horizon or
baseline to reverse it.

The version increment changes publication governance: a reproducible forecast
may be issued with `experimental_unvalidated` status before validation, solely
to build a prospective sequence. Promotion and validated claims remain
prohibited.

## Frozen forecast procedure

At each eligible issuance cutoff the cycle:

1. admits only outcomes whose conservative public `available_at` is no later
   than the cutoff;
2. admits annual T-100 exposure only after year end plus the frozen 365-day lag;
3. constructs the next 90 daily exposure rows using the latest lag-eligible
   same-calendar-month T-100 totals, divided uniformly across source-month days;
4. refits `minimal_shrunk_hazard_v1` and the pooled exposure-only baseline;
5. emits the complete first-event distribution, no-event probability, modal
   date, conditional 80% interval and deterministic parameter-uncertainty bands;
6. records contract/input/model/forecast hashes and writes an append-only file.

Forecast horizons cannot overlap. The first eligible start is 2026-09-07. A
later forecast begins only after the previous 90-day horizon. Identical
scientific inputs are deduplicated.

`config/public-data-model-registry.json` freezes the contract hash. AGGIORNA
refuses execution if target, scope, cohorts, estimator, exposure rule, cadence,
horizon, baseline, evaluation or claim rules change under the same version.
Such a change requires a separately preregistered version.

## Prospective evaluation

Every expired forecast is paired with the exposure-only baseline that was
frozen at the same cutoff. The primary score is the full-horizon logarithmic
score, including right censoring when no event occurs. Predictive validation
remains blocked until at least ten scored forecasts contain a target event and
the candidate has a lower mean score than the baseline. Superiority additionally
requires the lower bound of the frozen deterministic paired-bootstrap 90%
interval for mean score improvement to be above zero (5,000 draws, seed 1402).
Crossing that evidence threshold does not automatically enable an absolute
probability or promotion claim; promotion remains an explicit versioned
scientific decision.

Scoring also requires positive outcome-coverage evidence. A verified event may
be scored only when competent-authority monitoring covers the interval through
that event. A no-event horizon may be scored only when such coverage reaches
the horizon end. An empty discovery result never proves that no event occurred.
Unscorable windows remain published as pending rather than being treated as
successes.

The append-only inputs are
`data/census/public-data-v1.4-outcomes.json` and
`data/census/public-data-v1.4-monitoring.json`. The machine-readable cumulative
result is `evaluations/public-data-v1.4-prospective.json`.

## Interpretation

The numerical distribution is a research output for a regional statistical
target. It is not an absolute operational accident probability and must not be
used to assess a flight, aircraft, operator, route or person. Family
probabilities are conditional model outputs, not safety rankings.

The public page therefore shows the modal day, conditional 80% interval and
conditional family distribution, but does not publish an absolute accident
probability. The complete frozen research record retains the mathematical
distribution needed for later proper scoring.

## Online-only automation boundary

No credential or commercial source is required to execute 1.4. T-100 archives
are downloadable from BTS, AVALL is downloaded from NTSB at every full update,
and outcome adjudication accepts only public competent-authority evidence. New
accepted rows trigger parameter refitting without editing model code or rules.

Authority adjudication and proof that a period contains no qualifying event
cannot be manufactured by automation. If online evidence is incomplete, the
forecast can still be issued from the last lag-eligible training snapshot, but
evaluation remains fail-closed. This is an evidence-coverage limitation, not a
reason to silently substitute an aggregator or change the target.

## Additional-data hypothesis

Global performed-flight exposure and point-in-time precursor histories would
make the excluded BSFM 1.2 components testable. That is evidence of added
**information capability**, not evidence that the score would improve.

If those data later become available, their value must be tested prospectively
on identical frozen cutoffs and outcomes against BSFM-PD 1.4. Improvement means
a lower preregistered proper score with uncertainty reported. No favorable
claim is allowed merely because the richer data exist, and no method may be
changed after inspecting the paired result.

## Freeze

This protocol and its JSON contract become frozen at their first commit to
`main`. The first forecast must be issued only by a later AGGIORNA run from that
committed contract.

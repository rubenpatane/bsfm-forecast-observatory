# BSFM Backtest Protocol v1

Status: preregistered protocol; results must not alter these rules retrospectively.

## Scientific question
Does BSFM add out-of-sample predictive information beyond an exposure-only reference model for the next qualifying fatal accident involving a Boeing commercial jet?

## Evaluation interval
Historical evaluation covers 2010-2025. For each eligible target event, forecasts are reconstructed at T-365, T-90, T-30 and T-7 days. Features must be restricted to records demonstrably available at the cutoff.

## Point-in-time rule
A predictor row is eligible only when `available_at <= cutoff`. Missing, malformed or later availability timestamps are not admissible. Event occurrence date must never be substituted for publication/availability date when the latter is required to establish what the model could have known.

Current AVALL snapshots may contain later report/publication state. They must not be treated as proof that every field was historically available at an earlier cutoff. Where historical availability cannot be established, that feature is excluded or the evaluation is marked unavailable rather than imputed from future knowledge.

## Target
Primary target: the next fatal accident after each cutoff involving a Boeing commercial jet. Fatality must be attributable to the qualifying accident. Non-fatal incidents may be retained for precursor research but cannot be scored as primary target hits.

## Forecast dimensions
Scored separately:
- Boeing family;
- exact model/variant where supported;
- event/failure class;
- phase of flight;
- coarse geography when supported;
- temporal error in days.

No operator, registration or MSN score is reported unless the model and exposure data support that resolution prospectively.

## Temporal metrics
Report absolute day error and hit rates at ±30, ±14, ±7, ±3 and ±1 days. Include no-event periods where the probabilistic formulation requires them.

## Probabilistic metrics
When calibrated probabilities are available, report Brier score and calibration diagnostics. Absolute public probabilities remain disabled until the calibration gate passes.

## Baseline
BSFM must be compared with an exposure-only reference model using the same cutoffs, target definition and evaluation cases. A BSFM improvement claim requires paired out-of-sample evidence; raw event counts are not an exposure baseline.

## Leakage gate
Any future-dated predictor, unavailable publication timestamp, target-derived predictor, or retrospective forecast modification invalidates the affected evaluation case. Invalid cases are reported, not silently removed.

## Versioning
Every evaluated forecast records model version, cutoff, source snapshot/manifests and immutable forecast payload/hash. Frozen prospective forecasts, including F-002, are never rewritten after observing outcomes.

## Interpretation
Partial descriptive matches are reported as partial descriptive evidence only. They are not primary hits. A successful historical backtest does not establish operational safety capability; a failed backtest is retained and published as evidence against the model.

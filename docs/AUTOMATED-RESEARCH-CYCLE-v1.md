# BSFM Automated Research Cycle v1

Status: FROZEN IMPLEMENTATION CONTRACT — SCIENTIFIC GATES FAIL CLOSED  
Adopted: 2026-09-06

Cycle 1.0 remains frozen. Cycle 1.1 is the active prospective implementation: it adds mandatory refitting inside every historical walk-forward fold and deterministic Gamma-posterior Monte Carlo bands. The 1.0 specification is preserved unchanged in the registry.

## Purpose

This contract defines the automatic path:

`new data → PIT audit → exposure/predictor snapshot → parameter refit → paired walk-forward backtest → time-to-next-event distribution → append-only publication`

Automation may update data and fitted parameters. It may not change the target, admitted predictors, exposure semantics, estimator, scoring rule, forecast horizon or promotion rule. Any such change requires a new committed cycle specification and model version before it can be evaluated.

## Version boundary

`config/research-cycle-v1.json` is the machine-readable contract. Its canonical JSON hash is frozen in `config/research-cycle-registry.json` and embedded in every training snapshot and cycle result. A changed contract with the same version is rejected. The executable candidate is `minimal_shrunk_hazard_v1`; it is not represented as the complete contractual BSFM 1.2 model. Model 1.2 continues to require all components declared in `config/model.json`, including `faa_sdr_precursors`.

## Inputs and gates

The automatic fit may begin only when:

- source/schema integrity passes;
- G1 supplies historical cases under fixed semantics;
- G2 supplies the complete, directly measured Boeing cohort×year exposure matrix;
- G3 supplies a frozen, non-empty predictor universe with record/field/snapshot PIT evidence;
- leakage controls pass.

If any condition is missing, AGGIORNA publishes a content-addressed `scientific_fit_gate_closed` result and does not fit. If the scientific gate opens but a declared model input artifact is absent, it publishes `declared_input_artifacts_missing` and does not improvise a substitute.

## Temporal distribution

For each future civil day and aircraft cohort, the input contains predeclared projected departures. The fitted cohort hazard and daily exposure imply a discrete first-event distribution:

`P(T=d) = S(d-1) × (1 − exp(−hazard(d)))`.

The published distribution contains every day in the 90-day horizon, probability of no event within the horizon, modal date and an 80% central interval conditional on an event occurring within the horizon. The exposure-only baseline uses a pooled shrunken event rate and the identical future exposure path.

Cycle 1.1 additionally publishes parameter-uncertainty bands for cumulative event probability. It draws from each cohort's Gamma posterior using the frozen sample count and random seed, making the Monte Carlo result exactly reproducible. These bands quantify uncertainty in fitted rates; they do not compensate for missing exposure or PIT evidence.

This is a reproducible statistical distribution, not certainty about a flight, operator, aircraft or location. Operator/MSN specificity remains unsupported unless a later separately versioned model and evidence contract genuinely support it.

## Backtest and promotion

Each historical forecast must use only rows proven public at its simulated cutoff. Cycle 1.1 refits the candidate and pooled baseline separately at every cutoff; it never evaluates a model fitted using later folds. Candidate and exposure-only baseline use the same cutoff, outcome universe, horizon and exposure path. The primary temporal score is the full-horizon logarithmic score, including right-censored periods with no event. All folds—including blocked and failed ones—remain visible.

A fitted candidate is not promoted merely because it produces a forecast. Promotion additionally requires paired out-of-sample evaluation, calibration evidence and candidate superiority under the frozen rule. A negative or inconclusive comparison retains the incumbent and is a valid research result.

After a successful gated fit, AGGIORNA writes an immutable candidate forecast under `forecasts/candidates/`. Its identifier is derived from the cycle specification, training snapshot, fitted model and paired candidate/baseline distributions. Repeating the same scientific inputs reuses the same record; changed inputs create a new record. Candidate status remains `frozen_candidate_unvalidated` unless the independent promotion gate passes, and no automatic record modifies F-002.

## Current limitation

The execution machinery is implemented and testable with synthetic fixtures, but real fitting and scientific validation remain blocked by the real G2/G3 evidence gaps recorded in `docs/PROJECT-STATE.md`. Synthetic tests demonstrate software behavior only.

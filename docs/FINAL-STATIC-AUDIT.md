# Final static audit — pre-AGGIORNA

Date: 2026-09-05
Scope baseline: generated-state commit `a5fb38cfb120d57bed7003f08557cc267f003dd2` through final implementation batch.
Runtime status: NOT YET VERIFIED; reserved for the single final AGGIORNA.

## Repository architecture

PASS by static inspection:
- exactly one operational workflow path: `.github/workflows/autonomous-update.yml`, named `AGGIORNA`;
- package discovery includes all new `bsfm.*` modules;
- F-002 registry/evaluation code was not retrospectively rewritten by this batch;
- source refresh remains separate from scientific evidence gates;
- generated model state remains auditable and fail closed.

## Conflicting-logic audit

Resolved before final workflow:
- legacy `backtest.admissible_features` previously accepted any `available_at`; it now delegates to verified PIT eligibility and forbids alternate timestamp fields;
- legacy `publication_gate` previously omitted paired-baseline and superiority evidence; it now matches the post-fit promotion evidence surface;
- duplicate `case_id` rows previously could be silently overwritten during paired comparison; they now fail closed;
- malformed probabilities/outcomes now fail closed before scoring;
- fit readiness is separate from post-fit calibration/promotion, avoiding a circular calibration-before-fit requirement;
- workflow and CLI now use the same fail-closed availability semantics rather than permanently hard-coding a future leakage PASS or silently inferring one.

## Candidate estimator

Implemented a deliberately low-complexity shrinkage hazard candidate suitable for rare-event/small-sample conditions. It estimates cohort event hazard per departure with pseudo-exposure shrinkage and predicts a next-event cohort simplex using prediction-period exposure. It is not fitted unless the independent fit gate passes. This implementation is a candidate, not a claim of predictive superiority.

## OOS path

The OOS runner:
- requires explicit immutable case descriptors;
- rejects every training/prediction row not proven public by cutoff;
- requires prediction exposure for every cohort exactly once;
- fits only from supplied historical inputs;
- returns a probability simplex and proper multiclass Brier score.

## Model governance

Implemented:
- fit gate;
- promotion gate;
- incumbent retention;
- content hashes for model, training snapshot and evaluation;
- candidate/promoted/rejected registry states;
- promotion transition only on explicit passed gate;
- machine-readable final readiness report;
- absolute probability/validated-claim flags remain false until promotion readiness.

## Empirical blockers

The static audit does not change G1–G4 in `docs/FINAL-EVIDENCE-GAPS.md`. In particular, current public evidence does not justify silently completing the global 2010–2025 target census, Boeing-family annual exposure matrix, or historical public-release timestamps for current FAA/NTSB snapshots. These are evidence limitations, not reasons to fabricate inputs.

## Runtime verification decision

The implementation batch is now ready for one integrated AGGIORNA. No intermediate workflow was used after AGGIORNA #11. The final workflow is expected to be the first runtime execution of the accumulated batch and must be inspected in full before the software batch is declared verified.

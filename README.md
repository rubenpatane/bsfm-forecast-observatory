# BSFM Forecast Observatory

Autonomous, auditable observatory for the Boeing Safety Forecast Model (BSFM).

Research system: forecasts are probabilistic experiments, not safety certifications or operational go/no-go advice.

Core rules: point-in-time data only; no future leakage; immutable frozen forecasts; outcomes stored separately; calibration before probabilistic claims; reproducible model/data/code provenance.

Autonomous loop: `ingest -> validate -> feature snapshot -> forecast -> freeze -> evaluate matured forecasts -> build observatory`.

Current baseline: BSFM v1.2 Dynamic Airframe Hazard. F-002 is preserved with declared cutoff 2026-08-19; repository publication occurs later and must not be misrepresented as proof of publication on that date.

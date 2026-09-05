# BSFM Forecast Observatory

Autonomous, auditable observatory for the Boeing Safety Forecast Model (BSFM).

## Scope and origin
BSFM is intentionally focused on the observation of **Boeing commercial jets**. It is not a general aviation-safety rating system and it does not assess whether a specific flight, aircraft, airline or route is safe.

The project was started by **Ruben Patanè** after learning about the Netflix documentary **Freefall: A Reckoning for Boeing** (2026), Rory Kennedy's follow-up to **Downfall: The Case Against Boeing** (2022). The investigations surrounding Boeing and the 737 MAX raised a research question that BSFM tries to test prospectively rather than answer by assumption: **can public, time-valid safety signals improve forecasting of future Boeing commercial-jet events beyond exposure alone?**

The documentary is the motivation for the research scope, **not evidence that validates the model**. BSFM requires official/public sources, point-in-time admissibility, immutable forecasts, explicit outcomes, calibration, baseline comparison and fail-closed scientific gates.

A fuller description of the project's origin, Boeing focus and the main findings of the 737 MAX investigations is in [`docs/ORIGIN-BOEING-SCOPE.md`](docs/ORIGIN-BOEING-SCOPE.md).

Research system: forecasts are probabilistic experiments, not safety certifications or operational go/no-go advice.

Core rules: point-in-time data only; no future leakage; immutable frozen forecasts; outcomes stored separately; calibration before probabilistic claims; reproducible model/data/code provenance.

Autonomous loop: `ingest -> validate -> feature snapshot -> forecast -> freeze -> evaluate matured forecasts -> build observatory`.

Current baseline: BSFM v1.2 Dynamic Airframe Hazard. F-002 is preserved with declared cutoff 2026-08-19; repository publication occurs later and must not be misrepresented as proof of publication on that date.

# BSFM Forecast Observatory

[![AGGIORNA](https://github.com/rubenpatane/bsfm-forecast-observatory/actions/workflows/autonomous-update.yml/badge.svg)](https://github.com/rubenpatane/bsfm-forecast-observatory/actions/workflows/autonomous-update.yml)

**BSFM — Boeing Safety Forecast Model** is an open, prospective and auditable research observatory that asks a deliberately difficult question:

> **Can public safety signals, available before an event occurs, help forecast future risk patterns in Boeing commercial jets better than exposure alone?**

🌐 **Live observatory:** https://rubenpatane.github.io/bsfm-forecast-observatory/  
💻 **Source code:** https://github.com/rubenpatane/bsfm-forecast-observatory

> **Experimental research — not an operational safety tool.** BSFM does not assess whether a specific flight, aircraft, airline, route or person is safe.

---

## Why Boeing?

BSFM is intentionally focused on **Boeing commercial jets** rather than aviation as a whole.

The project was started by **Ruben Patanè** after learning about the Netflix documentary **_Freefall: A Reckoning for Boeing_** (2026), Rory Kennedy's follow-up to **_Downfall: The Case Against Boeing_** (2022).

The Boeing investigations — particularly those surrounding the 737 MAX — raised questions about design assumptions, production pressure, certification, oversight, safety communication and corporate culture. BSFM does **not** treat those investigations or documentaries as proof that Boeing aircraft are intrinsically less safe.

Instead, they motivated a falsifiable research question:

> If public safety data contain useful warning structure, can that structure be detected **prospectively**, before outcomes are known?

If the answer is ultimately **no**, that is still a valid scientific result.

A fuller description of the project's origin and scope is available in [`docs/ORIGIN-BOEING-SCOPE.md`](docs/ORIGIN-BOEING-SCOPE.md).

---

## What makes BSFM different?

BSFM is designed to make retrospective success difficult.

A forecast must be created from information admissible at a declared cutoff, then frozen before the future outcome is known. Later evidence may be published as a separate refinement, but it cannot rewrite the original forecast or improve its original score retroactively.

The core principles are:

- **prospective forecasts**, frozen before outcomes;
- **point-in-time evidence**, with explicit temporal admissibility;
- **no future leakage**;
- **immutable forecast records**;
- **outcomes stored separately from predictions**;
- **machine-readable provenance and hashes**;
- **calibration before probabilistic claims**;
- **comparison against an exposure baseline**;
- **fail-closed scientific gates**;
- **negative and inconclusive results remain visible**.

A green software run is not treated as proof of predictive validity.

---

## Current prospective forecast: F-002

The observatory preserves **F-002** as an immutable experimental forecast.

Declared cutoff: **19 August 2026**  
Primary aircraft hypothesis: **Boeing 737-800 / 737 NG**  
Modal time window: **5–11 October 2026**  
Modal day: **8 October 2026**  
Flight phase: **final approach / landing**  
Event cluster: **SCF-NP / gear-structural-operational**

F-002 is not retrospectively edited. Repository publication occurred later than the declared cutoff and is not represented as proof that the forecast was publicly available on 19 August 2026.

## Versioned automatic research cycle

The repository implements the fail-closed execution path from new evidence to a future time-to-event distribution. `config/research-cycle-v1.json` freezes the candidate estimator, target taxonomy, 90-day horizon, scoring rule, cohort universe and versioning policy. Every run binds its inputs and specification with content hashes.

When the scientific input gates pass, active cycle 1.1 can refit candidate and baseline independently at every historical cutoff, construct paired time distributions and publish a modal date, daily probabilities, probability of no event within the horizon, a conditional temporal interval and reproducible posterior parameter-uncertainty bands. A successful gated run freezes a content-addressed candidate forecast without modifying earlier records. When a gate or declared input is missing, it publishes the reason and does not fabricate a forecast.

The implemented minimal shrinkage estimator is a candidate implementation, **not** a silent replacement for the complete BSFM 1.2 contract. Full details and equations are in [`docs/AUTOMATED-RESEARCH-CYCLE-v1.md`](docs/AUTOMATED-RESEARCH-CYCLE-v1.md).

Any later `R-F002-*` refinement is append-only, separately timestamped and excluded from the original F-002 score.

---

## Real-world data shown by the observatory

The public site exposes descriptive statistics and recent records acquired from official public sources, including:

- **FAA Service Difficulty Reports (SDR)**;
- **NTSB AVALL** aviation occurrence data;
- current Boeing-oriented counts and model distributions;
- recent Boeing SDR records;
- NTSB-derived nonfatal cases automatically selected as descriptive comparables to F-002.

An FAA SDR is a **service-difficulty report**, not necessarily an accident, a verified causal finding or a BSFM prediction.

Likewise, a nonfatal case that resembles F-002 is shown only as **comparative context**. It does not satisfy F-002's fatal-event target, does not count as a forecast hit and does not change any scientific gate.

The live site shows the timestamp of the latest acquired public-data refresh.

---

## Automatic comparable cases

After every full update, BSFM derives a small set of recent nonfatal Boeing cases from the newly acquired NTSB snapshot.

The current rule requires a case to be:

- Boeing;
- commercial;
- nonfatal;
- compatible with the **737-800 / 737 NG** hypothesis;
- and similar either in **approach/landing phase** or in the **gear/structural event cluster**.

Cases are ranked by a fixed descriptive similarity score and then by recency. A rolling five-year window makes old cases age out automatically.

The public comparison is explicitly descriptive: **similarity ≠ validation**.

---

## Scientific gates

BSFM currently keeps several scientific gates fail-closed until sufficient evidence exists.

### G1 — Historical target census
A complete, reconciled global census of qualifying Boeing commercial-jet fatal events is required.

### G2 — Exposure baseline
Annual Boeing-family exposure/flight denominators must be complete and provenance-consistent.

### G3 — Point-in-time availability
Historical predictors must be demonstrably public at each corresponding historical cutoff.

### G4 — Out-of-sample superiority
Calibration and paired candidate-vs-baseline evaluation can only run scientifically after the upstream evidence gates are satisfied.

Missing evidence is represented as **BLOCKED**, not silently substituted with proxies or zeros.

---

## `AGGIORNA`: the observatory refresh pipeline

The repository contains one operational GitHub Actions workflow: **AGGIORNA**.

A full AGGIORNA run performs the observatory lifecycle:

```text
pre-update tests and integrity checks
        ↓
FAA current + historical acquisition
        ↓
NTSB AVALL download and normalization
        ↓
nonfatal F-002 comparable-case derivation
        ↓
post-update tests and scientific audits
        ↓
readiness / evidence / refinements generation
        ↓
auditable generated-state commit
        ↓
GitHub Pages deployment
```

The heavy refresh runs automatically every **four elapsed days** through a persisted cadence marker. A lightweight scheduler checks daily; manual runs remain available at any time.

AGGIORNA may discover new evidence, but it cannot manufacture a scientific PASS, rewrite F-002 or reinterpret a service report as an accident.

---

## Public observatory

The GitHub Pages interface is bilingual (**Italiano / English**) and includes:

- Overview;
- a dedicated F-002 forecast dossier, including descriptive geography and the explicitly unsupported operator/MSN fields;
- Validation;
- Methodology;
- Provenance;
- current evidence-gate state;
- the frozen F-002 forecast;
- acquired FAA/NTSB statistics;
- recent Boeing reports;
- automatically refreshed nonfatal comparable cases;
- latest data-refresh timestamp;
- direct link back to this source repository.

The validation page publishes the separate BSFM-PD 1.3 exploratory result even
though it is negative and underpowered. The methodology page keeps the BSFM 1.2
contract distinct from the executable minimal shrinkage estimator. Each core
public state is also available as a machine-readable JSON artifact.

Open it here:

### https://rubenpatane.github.io/bsfm-forecast-observatory/

---

## Repository map

```text
bsfm/                 scientific and acquisition code
forecasts/            frozen forecast records and refinements
data/manifests/       source and cadence provenance
evaluations/          audit/evaluation outputs
site/                  public GitHub Pages observatory
tests/                 unit and integration tests
docs/                  methodology, origin and project-state documentation
.github/workflows/     AGGIORNA automation
```

The current authoritative operational state is documented in [`docs/PROJECT-STATE.md`](docs/PROJECT-STATE.md).

---

## Reproducibility and auditability

The project prefers reproducible evidence over narrative certainty.

Where possible, generated artifacts carry source metadata, timestamps and content hashes. Historical public availability is treated separately from current authenticity: a record being downloadable today does not prove that the same information was publicly available at an earlier forecasting cutoff.

This distinction is central to leakage-safe forecasting research.

---

## What BSFM does **not** claim

BSFM does not currently claim that:

- Boeing is intrinsically less safe than another manufacturer;
- a particular aircraft or flight is unsafe;
- an FAA SDR is an accident;
- similar nonfatal events confirm F-002;
- the model has demonstrated calibrated predictive superiority;
- absolute accident probabilities are scientifically validated.

Those claims require evidence that the current fail-closed gates are specifically designed to demand.

---

## Short description for sharing

> **BSFM is an open-source prospective forecasting experiment focused on Boeing commercial jets. It freezes predictions before outcomes, automatically acquires public FAA/NTSB data, preserves provenance, publishes errors and blocked scientific gates, and tests whether public safety signals can outperform exposure-only baselines without retrospective rewriting.**

---

## Italiano

**BSFM è un osservatorio di ricerca open source sui jet commerciali Boeing.** Le previsioni vengono congelate prima degli esiti, i dati ufficiali FAA/NTSB vengono acquisiti automaticamente, la provenienza viene conservata e i gate scientifici restano bloccati finché le evidenze necessarie non sono realmente disponibili.

Il progetto nasce dalle domande suscitate dalle inchieste su Boeing e dal documentario _Freefall: A Reckoning for Boeing_, ma non assume in partenza che Boeing sia meno sicura di altri costruttori. L'obiettivo è verificare se segnali pubblici disponibili prima degli eventi abbiano davvero capacità predittiva.

🌐 Osservatorio: https://rubenpatane.github.io/bsfm-forecast-observatory/  
💻 Codice: https://github.com/rubenpatane/bsfm-forecast-observatory

---

## Author

**Ruben Patanè**  
Independent open-source research project.

Feedback, reproducibility checks, methodological criticism and evidence-quality review are welcome through GitHub issues and pull requests.

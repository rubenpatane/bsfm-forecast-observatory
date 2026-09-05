# BSFM prior art and novelty framework

Status: working scientific review
Date: 2026-09-05

## Purpose
This document prevents unsupported novelty claims. BSFM must distinguish methods already established in aviation safety research from the particular prospective evaluation architecture being tested here.

## Closest verified prior art

### EASA Data4Safety (D4S)
EASA describes Data4Safety as a large-scale aviation data collection and analysis programme intended to identify systemic risks and mitigations. Its sources include occurrence reports, flight data, surveillance/traffic data and weather. EASA explicitly describes the analytical ambition as moving toward a predictive system, including vulnerability discovery and the goals to "know where to look" and "see it coming".

Relevance to BSFM: very high for heterogeneous-data fusion, precursor/risk discovery and predictive safety intelligence. D4S is not evidence, from the public material reviewed, of a public preregistered system forecasting and prospectively scoring the next fatal Boeing commercial-jet accident across BSFM's dimensions.

Primary source: EASA Data4Safety programme page and EASA programme description.

### Arnaldo Valdes et al., Safety Science 104 (2018), 216-230
"Prediction of aircraft safety incidents using Bayesian inference and hierarchical structures" develops Bayesian and hierarchical models for aviation safety occurrences. The paper explicitly addresses prediction/anticipation of incidents, risk estimation, fleet/carrier comparison and predictive efficacy. It uses operational exposure in its modelling and supports hierarchical statistical treatment of sparse heterogeneous aviation-safety data.

Relevance to BSFM: very high for Bayesian/hierarchical modelling, exposure-normalized incident rates, shrinkage-oriented reasoning and prediction of emerging risk. It establishes that these statistical ingredients are prior art and must not be claimed as BSFM inventions.

DOI: 10.1016/j.ssci.2018.01.008

### Recent ML failure-event forecasting
Recent aviation-safety literature also includes deep-learning/time-series approaches to forecasting aviation failure events. These establish that short/medium/long-horizon failure-event forecasting is not itself novel.

## What BSFM must NOT claim as novel
- predictive aviation-safety analytics;
- use of incident/occurrence precursors;
- Bayesian inference for aviation safety;
- hierarchical models or shrinkage in aviation safety;
- exposure-normalized event rates;
- machine-learning forecasting of aviation failures;
- combining multiple aviation data sources;
- proactive or predictive safety-management concepts.

## Candidate distinctive contribution to test
The potentially distinctive BSFM contribution is the combination of:
1. an explicitly defined next-event target (next qualifying fatal Boeing commercial-jet accident);
2. decomposition into exposure, precursor/failure hazard, escalation, phase, geography and time-to-event;
3. immutable ex-ante forecast records with cutoff, code/model version and input provenance;
4. strict point-in-time predictor admissibility (`available_at <= cutoff`), fail-closed on unknown availability;
5. preregistered rolling/walk-forward historical evaluation against an exposure-only reference model;
6. prospective scoring that retains failures and partial matches without retrospectively changing the forecast;
7. separately versioned prospective refinements that cannot improve the parent's original score;
8. promotion of model updates only after leakage, baseline, historical-case and calibration gates pass.

This combination is a **candidate contribution**, not a proven novelty claim. A defensible novelty statement requires a broader systematic search and explicit inclusion/exclusion protocol.

## Novelty claim policy
Until that review is complete, public wording should be:

> BSFM combines established predictive-safety and statistical methods in an open, preregistered prospective forecasting and evaluation architecture. No claim of being the first such system is made.

Do not use "first", "unique", "unprecedented", "world's first" or equivalent language without a documented systematic prior-art review supporting the exact claim.

## Scientific implications for implementation
Prior art strengthens, rather than weakens, the current architecture: hierarchical/Bayesian or penalized sparse-event modelling is preferable to arbitrary high-dimensional scoring; exposure must enter explicitly; predictive performance must be evaluated out of sample; and precursor information must be temporally admissible. BSFM's scientific value will depend on incremental predictive information over the exposure-only baseline, calibration, and prospective replication—not on algorithmic novelty alone.

## Review backlog
Before any formal publication/novelty claim, extend the search across Scopus/Web of Science/Google Scholar/IEEE/AIAA/Transportation Research, NASA/FAA/EASA/ICAO technical reports and relevant patents. Record search strings, dates, inclusion/exclusion criteria, candidate systems, target definition, prediction horizon, unit of analysis, exposure denominator, validation design, calibration reporting, and whether forecasts were frozen prospectively.

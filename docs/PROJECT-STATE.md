# BSFM Project State

Updated: 2026-09-05

## Last workflow-verified baseline
- F-002 remains frozen and explicitly experimental/unvalidated.
- Exactly one operational GitHub Actions workflow exists: `AGGIORNA`.
- AGGIORNA #20 (`33972138158`) completed successfully from source commit `cbfefb9a555b5f5d5dc3a917214b3f348dcaa15d`.
- Run #20 started at `2026-09-05T14:32:55Z` and completed successfully at `2026-09-05T14:36:14Z`.
- The run verifies the current acquisition/audit/publication pipeline and current public UX. Successful workflow execution does not establish predictive validity.

## Automatic schedule
- manual `workflow_dispatch` always executes a full refresh;
- a lightweight scheduled cadence check runs daily at `13:47 UTC`;
- the heavy AGGIORNA job runs automatically only after at least four full days from the persisted scheduled-refresh marker;
- manual runs do not reset the automatic cadence; failed scheduled heavy runs do not advance the marker.

## F-002 prospective evaluation
- `docs/F-002-PREREGISTRATION-v1.md` freezes the evaluation protocol before the modal forecast window.
- F-002 itself is unchanged; later evidence/refinements cannot rewrite it or retroactively add probabilities.
- The repository does not claim cryptographic proof that F-002 was publicly published on its declared 2026-08-19 cutoff.

## G1-G3 scientific foundation
`docs/G1-G3-EVIDENCE-PLAN-v1.md` defines the fail-closed evidence programme. G1, G2, G3 and downstream G4 remain BLOCKED until their evidence requirements are actually satisfied.

### G1 global target census
Implementation has started:
- `data/census/year-ledger.json` remains the canonical 2010-2025 reconciliation ledger; every year is currently `reconciled=false`.
- `data/census/icao-official-accidents-source.json` records the verified ICAO API contract for the `Official Accidents` (`accidents`) dataset.
- ICAO documents event-level Official Accidents access in CSV/JSON with filters including year and State, but requires an API key/registration for queries/downloads.
- `bsfm/g1_census.py` provides conservative ICAO CSV normalization, raw-row preservation, SHA-256 acquisition manifests and a structural audit that can never open G1 by itself.
- `tests/test_g1_census.py` enforces provenance preservation and the fail-closed rule.
- No ICAO API key or acquired Official Accidents dataset is stored in the repository yet.

G1 remains BLOCKED: acquisition plus year-level reconciliation with independent source families is still required. Merely parsing ICAO data will not set `reconciled=true`.

### G2 exposure
BLOCKED. Annual Boeing-family departures/cycles or another predeclared defensible exposure denominator are not yet complete for 2010-2025. Fleet counts, deliveries or interpolated shares are not silently substituted.

### G3 point-in-time availability
BLOCKED. Current historical predictor records do not establish field-level public availability at historical cutoffs. Event, discovery, submission or administrative dates are not automatically treated as publication timestamps.

### G4 validation
BLOCKED downstream of G1-G3. Genuine paired out-of-sample candidate-vs-exposure-baseline evaluation starts only after the upstream gates pass.

## Public observatory
- Italian is default; Italian/English localization covers the public surfaces.
- Mobile navigation keeps the language switch visible in the header.
- GitHub source and generated-data update timestamp are public and deployed.
- FAA SDR and NTSB AVALL descriptive data refresh through AGGIORNA; FAA SDR is not automatically an accident/causal finding and NTSB is not a global census.
- nonfatal F-002 comparables remain descriptive only and cannot score as fatal-target hits or open scientific gates.

## Evidence/refinement automation
- `bsfm/evidence_automation.py` inventories machine-readable evidence with hashes while mirroring canonical fail-closed gates.
- `bsfm/refinements.py` publishes only append-only provenance-gated refinements; F-002 is never rewritten.

## Current operational state
Runtime-verified through AGGIORNA #20 (`33972138158`) on source commit `cbfefb9a555b5f5d5dc3a917214b3f348dcaa15d`. Changes after that run are committed but require a later AGGIORNA for runtime verification/deployment where applicable.

## Exact next step / current blocker
Acquire the ICAO API Data Service `Official Accidents` dataset for 2010-2025 using a legitimate ICAO API key, preserve the raw response and acquisition provenance, then run structural normalization and begin year-by-year reconciliation against independent Boeing/EASA/NTSB evidence. ICAO requires an API key for API queries/downloads; no key is available to this repository or chat. Do not put the key in Git or public files.

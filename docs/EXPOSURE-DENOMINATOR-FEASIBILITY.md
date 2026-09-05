# Boeing-family exposure denominator feasibility

Status: open scientific blocker, reviewed 2026-09-05.

## Requirement
The preregistered primary null model requires annual departures for every eligible Boeing cohort under one compatible global commercial scope. The denominator must be observed/reconstructable with provenance; fleet share, accident share and SDR share are prohibited proxies.

## Evidence reviewed
- ICAO annual material provides global scheduled traffic/departure totals, e.g. about 32 million departures in 2013 and 33 million in 2014, but these are all-airline/all-manufacturer totals rather than Boeing-family denominators.
- Boeing 2025 Statistical Summary publishes type-level cumulative hull-loss/fatal-hull-loss accident rates per million departures. This proves departures are used as the type-level exposure basis and gives useful cumulative type information, but the public summary reviewed does not itself provide the required 2010-2025 annual departures matrix by Boeing family.
- Boeing Commercial Market Outlook combines traffic/capacity analysis with fleet data for forecasts. Forecast fleet/traffic products are not substitutes for observed historical family departures.

## Decision
`baseline_present` remains false. No proportional allocation of ICAO totals by fleet counts will be introduced. Continue searching archived Boeing statistical summaries and other authoritative operational datasets for a reconstructable annual type/family series. If no defensible public series exists, the protocol must transparently narrow/change the baseline scope in a new preregistered revision rather than silently estimate missing exposure.

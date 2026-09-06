# NTSB AVALL snapshot provenance

Status: supporting/discovery evidence only; **not global ground truth**.

This directory intentionally stores provenance and reproducibility metadata rather than the ~51 MB `ntsb-derived.zip` inside ordinary Git history. The source NTSB aviation datasets are published for public use, and the AGGIORNA #25 derived artifact is identified by immutable hashes in `manifest.json`.

The snapshot is used to test normalization, commercial-operation classification, phase recovery, external-fatality handling and identity-conflict detection. Foreign-event values are never silently promoted over the competent investigation authority. Current AVALL presence also does not prove historical point-in-time availability for G3.

Reacquisition sources:
- NTSB accident data: https://www.ntsb.gov/safety/data/Pages/Data_Stats.aspx
- NTSB AV data download directory: https://data.ntsb.gov/avdata
- BSFM AGGIORNA #25: GitHub Actions run `33978802087`, source SHA `971cdd6a1ec0576208191e2d18fe76fce2742c86`, artifact `ntsb-derived` / ID `9973159900`.

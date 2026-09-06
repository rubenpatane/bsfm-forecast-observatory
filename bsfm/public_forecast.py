from __future__ import annotations

import json
from pathlib import Path


REQUIRED_PREDICTION_FIELDS = (
    "modal_week",
    "modal_day",
    "primary_family_variant",
    "secondary_family_variant",
    "phase",
    "primary_event_class",
    "alternative_event_class",
    "geography",
    "msn",
    "operator",
)


def build_public_forecast(forecast: dict) -> dict:
    """Return the public, machine-readable projection of a frozen forecast.

    The projection copies declared fields without interpreting or extending them.
    It is deliberately regenerated from the canonical forecast so the website
    cannot drift from the immutable scientific record.
    """
    if forecast.get("forecast_id") != "F-002" or forecast.get("status") != "frozen":
        raise ValueError("public forecast must be the frozen F-002 record")
    prediction = forecast.get("prediction")
    if not isinstance(prediction, dict):
        raise ValueError("forecast prediction must be an object")
    missing = [name for name in REQUIRED_PREDICTION_FIELDS if name not in prediction]
    if missing:
        raise ValueError(f"forecast prediction missing fields: {', '.join(missing)}")
    return {
        "schema": "bsfm.public-forecast.v1",
        "forecast_id": forecast["forecast_id"],
        "status": forecast["status"],
        "model_version": forecast.get("model_version"),
        "cutoff": forecast.get("cutoff"),
        "declared_date": forecast.get("declared_date"),
        "target": forecast.get("target"),
        "claim_level": forecast.get("claim_level"),
        "prediction": {name: prediction[name] for name in REQUIRED_PREDICTION_FIELDS},
        "integrity": forecast.get("integrity"),
        "record_note": forecast.get("notes"),
        "evaluation_spec": "docs/F-002-PREREGISTRATION-v1.md",
        "scoring_boundary": (
            "Dimension-level evaluation only; no retrospective probability "
            "distribution may be assigned to F-002."
        ),
    }


def write_public_forecast(root: Path, out: Path | None = None) -> dict:
    root = Path(root)
    forecast = json.loads((root / "forecasts/F-002.json").read_text(encoding="utf-8"))
    public = build_public_forecast(forecast)
    destination = Path(out) if out else root / "site/data/forecast.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return public

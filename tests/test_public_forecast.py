import json
from pathlib import Path

import pytest

from bsfm.public_forecast import build_public_forecast, write_public_forecast


ROOT = Path(__file__).resolve().parents[1]


def canonical_forecast():
    return json.loads((ROOT / "forecasts/F-002.json").read_text(encoding="utf-8"))


def test_public_forecast_is_an_exact_projection_of_frozen_fields():
    forecast = canonical_forecast()
    public = build_public_forecast(forecast)
    assert public["forecast_id"] == "F-002"
    assert public["prediction"] == forecast["prediction"]
    assert public["integrity"] == forecast["integrity"]
    assert public["claim_level"] == "experimental_unvalidated"
    assert "no retrospective probability" in public["scoring_boundary"]


def test_public_forecast_rejects_nonfrozen_or_incomplete_records():
    record = canonical_forecast()
    record["status"] = "draft"
    with pytest.raises(ValueError, match="frozen F-002"):
        build_public_forecast(record)
    record = canonical_forecast()
    del record["prediction"]["operator"]
    with pytest.raises(ValueError, match="operator"):
        build_public_forecast(record)


def test_seed_public_forecast_cannot_drift_from_canonical_record(tmp_path):
    destination = tmp_path / "forecast.json"
    generated = write_public_forecast(ROOT, destination)
    seed = json.loads((ROOT / "site/data/forecast.json").read_text(encoding="utf-8"))
    assert generated == seed

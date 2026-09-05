import importlib.util
import json
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "acquire_icao_g1.py"
spec = importlib.util.spec_from_file_location("acquire_icao_g1", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_csv_schema_summary_contains_no_event_rows():
    data = b"Date,Model,Registration,Operator\n2020-01-01,B737,ABC123,Example Air\n"
    summary = mod.csv_schema_summary(data)
    assert summary["rows"] == 1
    assert summary["fields"] == ["Date", "Model", "Registration", "Operator"]
    assert summary["nonempty_counts"]["Registration"] == 1
    serialized = json.dumps(summary)
    assert "ABC123" not in serialized
    assert "Example Air" not in serialized


def test_public_audit_is_fail_closed_and_aggregate_only(tmp_path):
    out = tmp_path / "audit.json"
    yearly = [{
        "year": 2025,
        "fields": ["Date", "Model"],
        "rows": 0,
        "nonempty_counts": {"Date": 0, "Model": 0},
        "sha256": "sha256-test",
        "bytes": 0,
    }]
    mod.write_public_audit(out, yearly, {"structurally_complete": False})
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["gate_status"] == "BLOCKED"
    assert payload["zero_record_years"] == [2025]
    assert payload["publication_scope"].startswith("Aggregate")
    assert "events" not in payload

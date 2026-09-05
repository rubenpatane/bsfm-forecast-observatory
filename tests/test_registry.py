from pathlib import Path
import pytest
from bsfm.registry import freeze
def test_immutable(tmp_path:Path):
 d={"forecast_id":"F-X","model_version":"1","cutoff":"2026-01-01","created_at":"2026-01-01T00:00:00Z","target":"x","status":"frozen","prediction":{"x":1}}; freeze(tmp_path,d); c=dict(d); c["prediction"]={"x":2}
 with pytest.raises(RuntimeError): freeze(tmp_path,c)

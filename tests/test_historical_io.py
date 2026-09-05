import json
import pytest
from bsfm.historical_io import ledger_attestations,load_jsonl


def test_unreconciled_ledger_rows_are_not_attestations():
    ledger={'years':[{'year':2024,'reconciled':False},{'year':2025,'reconciled':True,'publishers':['ICAO','EASA'],'qualifying_boeing_events':0,'scope':'x','provenance':['a','b']}]}
    out=ledger_attestations(ledger)
    assert 2024 not in out and out[2025]['qualifying_boeing_events']==0


def test_jsonl_loader_fails_loudly_on_malformed_line(tmp_path):
    p=tmp_path/'x.jsonl'; p.write_text('{"a":1}\nnot-json\n')
    with pytest.raises(ValueError,match='line 2'): load_jsonl(p)

from __future__ import annotations
import json
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def ledger_attestations(ledger):
    """Convert only fully declared year-ledger rows to census attestations.

    Construction placeholders remain visible but cannot become evidence.
    """
    out={}
    for row in ledger.get('years',[]):
        if row.get('reconciled') is not True:
            continue
        year=row.get('year')
        if year is None:
            continue
        out[int(year)]={k:row.get(k) for k in ('reconciled','publishers','qualifying_boeing_events','scope','provenance')}
    return out


def load_jsonl(path):
    p=Path(path)
    if not p.exists(): return []
    rows=[]
    for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        if line.strip():
            try: rows.append(json.loads(line))
            except json.JSONDecodeError as exc: raise ValueError(f'invalid JSONL line {n}: {exc.msg}') from exc
    return rows

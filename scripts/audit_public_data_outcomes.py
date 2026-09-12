#!/usr/bin/env python3
"""Audit the BSFM-PD 1.3 authority-backed route ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bsfm.public_data_outcomes import audit_route_ledger, load_candidate_ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=ROOT / "data/census/public-data-v1.3-route-ledger.json")
    args = parser.parse_args()
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    result = audit_route_ledger(ledger, load_candidate_ids(ROOT / "data/census"))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())

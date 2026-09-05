#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

from bsfm.g1_census import (
    audit_g1_records,
    parse_icao_official_accidents_csv,
    sha256_bytes,
    write_acquisition_manifest,
)

BASE_URL = "https://applications.icao.int/dataservices/api/accidents"
PUBLIC_AUDIT = Path("data/manifests/icao-official-accidents-audit.json")


def acquire_year(api_key: str, year: int, timeout: int = 60) -> bytes:
    query = urllib.parse.urlencode({
        "api_key": api_key,
        "format": "csv",
        "Year": str(year),
    })
    req = urllib.request.Request(
        f"{BASE_URL}?{query}",
        headers={"User-Agent": "BSFM-Forecast-Observatory/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = response.read()
        ctype = response.headers.get("Content-Type", "")
    if not data:
        raise RuntimeError(f"ICAO returned an empty response for {year}")
    probe = data[:2048].decode("utf-8", errors="ignore").lower()
    if any(token in probe for token in ("invalid api", "invalid key", "call limit", "calls limit", "limit reached", "error")) and "<html" in probe:
        raise RuntimeError(f"ICAO returned an error response for {year}")
    if "json" in ctype.lower() and data.lstrip().startswith((b"{", b"[")):
        raise RuntimeError(f"ICAO returned JSON while CSV was requested for {year}; refusing schema guess")
    return data


def csv_schema_summary(data: bytes) -> dict:
    text = data.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    fields = list(reader.fieldnames or [])
    rows = list(reader)
    nonempty = {field: 0 for field in fields}
    for row in rows:
        for field in fields:
            if str(row.get(field, "") or "").strip():
                nonempty[field] += 1
    return {
        "fields": fields,
        "rows": len(rows),
        "nonempty_counts": nonempty,
        "sha256": sha256_bytes(data),
        "bytes": len(data),
    }


def write_public_audit(path: Path, yearly: list[dict], structural: dict) -> None:
    all_fields = sorted({field for item in yearly for field in item["fields"]})
    payload = {
        "schema": "bsfm.icao-official-accidents-audit.v1",
        "source": "ICAO API Data Service / Official Accidents",
        "dataset_api_name": "accidents",
        "evaluation_interval": {
            "start_year": min(item["year"] for item in yearly),
            "end_year": max(item["year"] for item in yearly),
        },
        "total_records": sum(item["rows"] for item in yearly),
        "years": yearly,
        "observed_fields": all_fields,
        "zero_record_years": [item["year"] for item in yearly if item["rows"] == 0],
        "structurally_complete": bool(structural.get("structurally_complete")),
        "gate_status": "BLOCKED",
        "gate_effect": "none_without_event_level_reconciliation",
        "raw_data_publication": "prohibited_by_project_policy_pending_explicit_redistribution_rights",
        "credential_handling": "GitHub Actions secret; never persisted",
        "interpretation": "A zero API row count is an observed API result, not evidence that zero qualifying accidents occurred in that year.",
        "publication_scope": "Aggregate schema/count/hash metadata only; no ICAO event-level rows are committed or published.",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire ICAO Official Accidents for G1 without exposing the API key")
    parser.add_argument("--start-year", type=int, default=2010)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument("--out", type=Path, default=Path("data/derived/icao"))
    parser.add_argument("--public-audit", type=Path, default=PUBLIC_AUDIT)
    parser.add_argument("--sleep", type=float, default=0.25)
    args = parser.parse_args()
    api_key = os.environ.get("ICAO_API_KEY", "").strip()
    if not api_key:
        print("ICAO_API_KEY is not set", file=sys.stderr)
        return 2
    args.out.mkdir(parents=True, exist_ok=True)
    all_records = []
    acquisitions = []
    yearly_public = []
    for year in range(args.start_year, args.end_year + 1):
        try:
            data = acquire_year(api_key, year)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as exc:
            print(f"ICAO acquisition failed for {year}: {exc}", file=sys.stderr)
            return 3
        raw_path = args.out / f"official-accidents-{year}.csv"
        raw_path.write_bytes(data)
        records = parse_icao_official_accidents_csv(data)
        manifest = write_acquisition_manifest(
            args.out / f"official-accidents-{year}.manifest.json",
            source="ICAO API Data Service / Official Accidents",
            locator=f"{BASE_URL}?Year={year}&format=csv&api_key=REDACTED",
            data=data,
            records=len(records),
        )
        manifest["year"] = year
        acquisitions.append(manifest)
        summary = csv_schema_summary(data)
        summary["year"] = year
        yearly_public.append(summary)
        all_records.extend(records)
        print(f"ICAO {year}: {len(records)} records")
        if args.sleep:
            time.sleep(args.sleep)
    normalized = args.out / "official-accidents-2010-2025.jsonl"
    normalized.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in all_records), encoding="utf-8")
    audit = audit_g1_records(all_records, args.start_year, args.end_year)
    audit["acquisitions"] = acquisitions
    audit["credential_handling"] = "GitHub Actions secret; never persisted"
    (args.out / "g1-structural-audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_public_audit(args.public_audit, yearly_public, audit)
    print(json.dumps({"records": len(all_records), "structurally_complete": audit["structurally_complete"], "gate_status": audit["gate_status"], "public_audit": str(args.public_audit)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

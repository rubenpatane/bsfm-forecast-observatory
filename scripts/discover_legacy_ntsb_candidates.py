#!/usr/bin/env python3
"""Discover pre-2008 Boeing fatal-event candidates in an official NTSB MDB.

This is a discovery/reconciliation helper, not an automatic target adjudicator.
It deliberately emits a broad candidate set and excludes owner/address/person
fields from its output. Final inclusion still requires the versioned target,
route and competent-authority evidence audits.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


OUTPUT_FIELDS = (
    "event_id",
    "ntsb_number",
    "event_date",
    "administrative_approval_date",
    "event_type",
    "fatalities_aboard",
    "fatalities_ground",
    "make",
    "model",
    "series",
    "registration",
    "far_part",
    "operating_certificate",
    "scheduled_operation",
    "domestic_international",
    "passenger_cargo",
    "departure_airport",
    "departure_city",
    "departure_state",
    "departure_country",
    "destination_airport",
    "destination_city",
    "destination_state",
    "destination_country",
)


def _rows(columns: dict[str, list[Any]]) -> Iterable[dict[str, Any]]:
    if not columns:
        return
    length = len(next(iter(columns.values())))
    for index in range(length):
        yield {name: values[index] for name, values in columns.items()}


def _iso(value: Any) -> str | None:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if value in (None, ""):
        return None
    return str(value)[:10]


def _number(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def discover(
    events: dict[str, list[Any]],
    aircraft: dict[str, list[Any]],
    administration: dict[str, list[Any]],
    start_year: int,
    end_year: int,
):
    approval_by_event = {
        row.get("ev_id"): _iso(row.get("approval_date"))
        for row in _rows(administration)
        if row.get("ev_id")
    }
    fatal_events = {}
    for row in _rows(events):
        year = _number(row.get("ev_year"))
        fatalities = _number(row.get("inj_tot_f")) + _number(row.get("inj_f_grnd"))
        if start_year <= year <= end_year and fatalities > 0:
            fatal_events[row.get("ev_id")] = row

    candidates = []
    seen = set()
    for row in _rows(aircraft):
        event = fatal_events.get(row.get("ev_id"))
        if event is None:
            continue
        make = str(row.get("acft_make") or "").strip()
        if "BOEING" not in make.upper():
            continue
        key = (row.get("ev_id"), row.get("Aircraft_Key"))
        if key in seen:
            continue
        seen.add(key)
        record = {
            "event_id": row.get("ev_id"),
            "ntsb_number": row.get("ntsb_no") or event.get("ntsb_no"),
            "event_date": _iso(event.get("ev_date")),
            "administrative_approval_date": approval_by_event.get(row.get("ev_id")),
            "event_type": event.get("ev_type"),
            "fatalities_aboard": _number(event.get("inj_tot_f")),
            "fatalities_ground": _number(event.get("inj_f_grnd")),
            "make": make,
            "model": row.get("acft_model"),
            "series": row.get("acft_series"),
            "registration": row.get("regis_no"),
            "far_part": row.get("far_part"),
            "operating_certificate": row.get("oprtng_cert") or row.get("oper_cert"),
            "scheduled_operation": row.get("oper_sched"),
            "domestic_international": row.get("oper_dom_int"),
            "passenger_cargo": row.get("oper_pax_cargo"),
            "departure_airport": row.get("dprt_apt_id"),
            "departure_city": row.get("dprt_city"),
            "departure_state": row.get("dprt_state"),
            "departure_country": row.get("dprt_country"),
            "destination_airport": row.get("dest_apt_id"),
            "destination_city": row.get("dest_city"),
            "destination_state": row.get("dest_state"),
            "destination_country": row.get("dest_country"),
        }
        candidates.append({field: record[field] for field in OUTPUT_FIELDS})
    return sorted(candidates, key=lambda item: (item["event_date"] or "", item["event_id"] or ""))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mdb", type=Path)
    parser.add_argument("--start-year", type=int, default=1990)
    parser.add_argument("--end-year", type=int, default=2007)
    parser.add_argument("--source-archive", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument(
        "--snapshot-bound",
        required=True,
        help="Conservative YYYY-MM-DD date by which these exact source bytes were public",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        from access_parser import AccessParser
    except ImportError as exc:  # pragma: no cover - optional research dependency
        raise SystemExit("Install the optional 'access-parser' package to inspect an NTSB MDB") from exc

    database = AccessParser(str(args.mdb))
    candidates = discover(
        database.parse_table("events"),
        database.parse_table("aircraft"),
        database.parse_table("NTSB_Admin"),
        args.start_year,
        args.end_year,
    )
    payload = {
        "schema": "bsfm.ntsb-legacy-candidate-discovery.v1",
        "source": {
            "official_url": args.source_url,
            "archive_name": args.source_archive.name,
            "archive_sha256": hashlib.sha256(args.source_archive.read_bytes()).hexdigest(),
            "mdb_name": args.mdb.name,
            "mdb_sha256": hashlib.sha256(args.mdb.read_bytes()).hexdigest(),
            "snapshot_bound": args.snapshot_bound,
            "snapshot_bound_semantics": "no earlier than confirmed public availability of these exact bytes",
        },
        "interval": {"start_year": args.start_year, "end_year": args.end_year},
        "status": "DISCOVERY_ONLY_REQUIRES_TARGET_AND_ROUTE_ADJUDICATION",
        "pit_warning": "NTSB administrative approval/change dates do not prove public availability and are never automatically PIT-admissible.",
        "privacy": "Only event/aircraft/operation/route fields are emitted; personal and address fields are excluded.",
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

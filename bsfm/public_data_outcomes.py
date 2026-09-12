"""Fail-closed geographic outcome audit for the BSFM-PD model line."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ALLOWED_ROUTE_STATUS = {"VERIFIED_AUTHORITY", "PENDING_ROUTE"}
ALLOWED_DECISIONS = {"INCLUDE_US_ENDPOINT", "EXCLUDE_NO_US_ENDPOINT", "PENDING_ROUTE"}


def load_candidate_ids(census_dir: Path) -> set[str]:
    """Return the complete frozen G1 candidate universe, including boundary cases."""
    ids: set[str] = set()
    for path in sorted(census_dir.glob("candidates-*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                if record.get("event_id"):
                    ids.add(record["event_id"])
    later = json.loads((census_dir / "g1-candidates.json").read_text(encoding="utf-8"))
    ids.update(record["event_id"] for record in later["records"])
    return ids


def audit_route_ledger(ledger: dict[str, Any], candidate_ids: set[str]) -> dict[str, Any]:
    """Audit route evidence and refuse readiness until every candidate is decided."""
    errors: list[str] = []
    seen: set[str] = set()
    included: list[str] = []
    excluded: list[str] = []
    pending: list[str] = []
    for row in ledger.get("records", []):
        event_id = row.get("event_id")
        if not event_id or event_id in seen:
            errors.append(f"missing or duplicate event_id: {event_id!r}")
            continue
        seen.add(event_id)
        if event_id not in candidate_ids:
            errors.append(f"unknown candidate: {event_id}")
        status = row.get("route_status")
        decision = row.get("geographic_decision")
        if status not in ALLOWED_ROUTE_STATUS or decision not in ALLOWED_DECISIONS:
            errors.append(f"invalid status/decision: {event_id}")
        if decision != "PENDING_ROUTE" and status != "VERIFIED_AUTHORITY":
            errors.append(f"unverified route has final decision: {event_id}")
        if status == "VERIFIED_AUTHORITY":
            evidence = row.get("evidence", {})
            if not all(evidence.get(key) for key in ("publisher", "record", "locator", "observation")):
                errors.append(f"incomplete authority evidence: {event_id}")
            endpoints = (row.get("origin", {}), row.get("destination", {}))
            has_us_endpoint = any(endpoint.get("us_endpoint") is True for endpoint in endpoints)
            expected = "INCLUDE_US_ENDPOINT" if has_us_endpoint else "EXCLUDE_NO_US_ENDPOINT"
            if decision != expected:
                errors.append(f"endpoint/decision mismatch: {event_id}")
        if decision == "INCLUDE_US_ENDPOINT": included.append(event_id)
        elif decision == "EXCLUDE_NO_US_ENDPOINT": excluded.append(event_id)
        else: pending.append(event_id)
    missing = sorted(candidate_ids - seen)
    ready = not errors and not missing and not pending and len(seen) == len(candidate_ids)
    return {"status": "READY" if ready else "BLOCKED", "candidate_count": len(candidate_ids),
            "ledger_count": len(seen), "verified_included": sorted(included),
            "verified_excluded": sorted(excluded), "pending_candidate_ids": sorted(pending),
            "missing_candidate_ids": missing, "errors": errors}

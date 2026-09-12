"""Stack-independent evaluation of actual execution facts.

Execution lives in the existing evidence manifest's `execution` property. It
does not invent certification measurements or authenticate an untrusted producer.
Apple execution and artifact storage belong to the application adapter.
"""

from __future__ import annotations

import json
import os
import re
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path

if __package__:
    from .certify import number, require, unique_strings
else:
    from certify import number, require, unique_strings


TEST_STATUSES = {"passed", "failed", "skipped", "unavailable", "inconclusive"}
PRODUCER_STATUSES = {"passed", "failed", "blocked", "invalid"}


def digest(value, length):
    return isinstance(value, str) and re.fullmatch(rf"[0-9a-f]{{{length}}}", value) is not None


def assess_execution(execution):
    """Evaluate execution only; omissions never disappear behind a green exit."""
    require(isinstance(execution, dict), "execution must be an object")
    require(type(execution.get("schema_version")) is int
            and execution["schema_version"] == 1, "Unsupported execution schema")
    for field in ("app_commit", "spec_commit"):
        require(digest(execution.get(field), 40), f"Invalid pinned {field}")
    require(digest(execution.get("plan_sha256"), 64), "Invalid test plan digest")
    require(isinstance(execution.get("adapter"), str)
            and re.fullmatch(r"[a-zA-Z0-9_.-]+", execution["adapter"]), "Invalid adapter ID")
    required = execution.get("required_tests")
    require(unique_strings(required), "Required test selection must not be empty or duplicate")
    records = execution.get("tests")
    require(isinstance(records, list), "tests must be an array")
    seen = {}
    for record in records:
        require(isinstance(record, dict), "Invalid test observation")
        identity, status = record.get("id"), record.get("status")
        require(isinstance(identity, str) and identity.strip(), "Missing observed test ID")
        require(identity not in seen, "Duplicate test observation")
        require(isinstance(status, str) and status in TEST_STATUSES, "Unknown test status")
        seen[identity] = status
    producer = execution.get("producer_status")
    require(isinstance(producer, str) and producer in PRODUCER_STATUSES, "Unknown producer status")
    require(type(execution.get("complete")) is bool, "Missing completion witness")
    duration = execution.get("elapsed_seconds")
    require(number(duration) and duration >= 0, "Invalid elapsed time")
    missing = sorted(set(required) - set(seen))
    failed = sorted(identity for identity, status in seen.items() if status == "failed")
    gaps = sorted(identity for identity in required
                  if identity in seen and seen[identity] not in {"passed", "failed"})
    if failed or producer == "failed":
        status = "failed"
    elif missing or not records or not execution["complete"] or producer == "invalid":
        status = "invalid"
    elif gaps or producer == "blocked":
        status = "blocked"
    else:
        status = "passed"
    return {"status": status, "missing_required": missing, "failed_tests": failed,
            "unresolved_required": gaps, "observed_tests": len(seen),
            "required_tests": len(required), "product_conformance": "not_assessed",
            "certificate": "NOT_ISSUED"}


def instant(value):
    require(isinstance(value, str), "Timestamp must be a string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Invalid timestamp") from exc
    require(parsed.tzinfo is not None, "Timestamp needs an explicit timezone")
    return parsed.astimezone(timezone.utc)


def expiry(captured_at, classification, source_expiries=()):
    """Derivatives cannot extend their sources' retention through reprocessing."""
    require(classification in {"metadata", "sensitive"}, "Unknown retention class")
    own = instant(captured_at) + timedelta(days=7 if classification == "sensitive" else 30)
    return min([own, *(instant(value) for value in source_expiries)]).isoformat().replace("+00:00", "Z")


def write_manifest(path, manifest):
    """Durable exclusive creation in a caller-owned private directory.

    No overwrite, including symlinks. An interrupted partial write remains an
    invalid manifest, never a previous failure replaced by a retry's success.
    The caller supplies the protected/encrypted storage boundary.
    """
    require(isinstance(manifest, dict), "Manifest must be an object")
    assess_execution(manifest.get("execution"))
    payload = (json.dumps(manifest, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    destination = Path(path)
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    parent_fd = os.open(destination.parent, os.O_RDONLY)
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def compare_benchmarks(data):
    """Check frozen paired numeric gates, leaving uncertainty/provenance review open."""
    require(isinstance(data, dict) and type(data.get("schema_version")) is int
            and data["schema_version"] == 1, "Unsupported benchmark schema")
    require(digest(data.get("protocol_sha256"), 64), "Missing frozen benchmark protocol")
    weights = data.get("weights")
    require(isinstance(weights, dict) and set(weights) == {"core", "ui", "adapter"},
            "Required representative lanes are core, ui, and adapter")
    require(all(number(w) and w > 0 for w in weights.values()), "Weights must be positive")
    records = data.get("pairs")
    require(isinstance(records, list), "pairs must be an array")
    by_lane = {lane: [] for lane in (*weights, "clean")}
    seen, invalid = set(), []
    for row in records:
        require(isinstance(row, dict), "Invalid benchmark pair")
        lane, pair = row.get("lane"), row.get("pair")
        require(isinstance(lane, str) and lane in by_lane, "Unknown benchmark lane")
        require(type(pair) is int and pair >= 0, "Invalid pair ID")
        require((lane, pair) not in seen, "Duplicate benchmark pair")
        seen.add((lane, pair))
        require(digest(row.get("condition_sha256"), 64), "Missing matched condition identity")
        before, after = row.get("baseline"), row.get("candidate")
        for result in (before, after):
            require(isinstance(result, dict), "Missing paired observation")
            require(number(result.get("seconds")) and result["seconds"] > 0, "Invalid duration")
            require(isinstance(result.get("status"), str)
                    and result["status"] in PRODUCER_STATUSES, "Unknown benchmark status")
            require(digest(result.get("assertions_sha256"), 64), "Missing assertion identity")
        if before["status"] != "passed" or after["status"] != "passed":
            invalid.append(f"{lane}/{pair}: unsuccessful pair")
        if before["assertions_sha256"] != after["assertions_sha256"]:
            invalid.append(f"{lane}/{pair}: assertion mismatch")
        by_lane[lane].append((before["seconds"], after["seconds"]))
    for lane, rows in by_lane.items():
        if len(rows) < 5:
            invalid.append(f"{lane}: fewer than five pairs")
    result = {"status": "invalid", "aggregate_ratio": None, "lanes": {},
              "gaps": invalid, "foundation_qualified": False,
              "remaining_review": ["provenance", "workload_equivalence", "uncertainty"]}
    if invalid:
        return result
    for lane, rows in by_lane.items():
        before = statistics.median(pair[0] for pair in rows)
        after = statistics.median(pair[1] for pair in rows)
        result["lanes"][lane] = {"pairs": len(rows), "baseline_median": before,
                                  "candidate_median": after, "ratio": after / before,
                                  "paired_ratios": [a / b for b, a in rows]}
    baseline = sum(weights[lane] * result["lanes"][lane]["baseline_median"] for lane in weights)
    candidate = sum(weights[lane] * result["lanes"][lane]["candidate_median"] for lane in weights)
    ratio = candidate / baseline
    result["aggregate_ratio"] = ratio
    result["status"] = "numeric_gates_met" if ratio <= 0.50 and all(
        lane["ratio"] <= 1.10 for lane in result["lanes"].values()) else "failed"
    return result

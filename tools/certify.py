"""Evaluate one scoped Trio test report. Never issue a product certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path


METHODS = {"device", "ui", "integration", "human"}
SCOPE_FIELDS = (
    "profile", "build_id", "engine_revision", "device", "os", "language_pair",
    "audio_route", "conditions", "power_setup", "fixture_revision",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def unique_strings(value):
    return (isinstance(value, list) and bool(value)
            and all(isinstance(item, str) and item.strip() for item in value)
            and len(set(value)) == len(value))


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError(f"Non-finite JSON value: {value}")

    return json.loads(Path(path).read_text(encoding="utf-8-sig"),
                      object_pairs_hook=pairs, parse_constant=invalid_constant)


def scope_hash(scope):
    encoded = json.dumps(scope, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_catalog(catalog):
    require(isinstance(catalog, dict), "Catalog must be an object")
    require(type(catalog.get("schema_version")) is int
            and catalog["schema_version"] == 1, "Unsupported catalog schema")
    require(isinstance(catalog.get("catalog_version"), str)
            and catalog["catalog_version"].strip(), "Missing catalog version")
    require(catalog.get("policy_status") in {"proposed", "approved"},
            "Invalid catalog policy status")
    minimum = catalog.get("minimum_score")
    require(minimum is None or (number(minimum) and 0 <= minimum <= 100),
            "minimum_score must be null or a number from 0 to 100")
    profiles = catalog.get("profiles")
    require(isinstance(profiles, dict) and profiles, "No profiles configured")
    for name, definition in profiles.items():
        require(isinstance(definition, dict), f"Invalid profile: {name}")
        parents = definition.get("extends")
        require(isinstance(parents, list)
                and all(isinstance(parent, str) and parent in profiles for parent in parents)
                and len(set(parents)) == len(parents), f"Invalid parents: {name}")
        profile_names(catalog, name)
    checks = catalog.get("checks")
    require(isinstance(checks, list) and checks, "No checks configured")
    seen = set()
    for check in checks:
        require(isinstance(check, dict), "Check must be an object")
        check_id = check.get("id")
        require(isinstance(check_id, str) and re.fullmatch(r"CERT-\d{3}", check_id),
                "Invalid check ID")
        require(check_id not in seen, f"Duplicate check: {check_id}")
        seen.add(check_id)
        require(isinstance(check.get("title"), str) and check["title"].strip(),
                f"Missing title: {check_id}")
        for key in ("requirements", "profiles", "methods", "cases"):
            require(unique_strings(check.get(key)), f"Invalid {key}: {check_id}")
        require(set(check["profiles"]) <= set(profiles), f"Unknown profile: {check_id}")
        require(set(check["methods"]) <= METHODS, f"Unknown method: {check_id}")
        samples = check.get("min_samples")
        require(samples is None or (type(samples) is int and samples >= 1),
                f"Invalid minimum samples: {check_id}")
        if check.get("kind") == "gate":
            require(check.get("operator") in {"eq", "gte", "lte"},
                    f"Invalid operator: {check_id}")
            require(check.get("threshold") is None or number(check["threshold"]),
                    f"Invalid threshold: {check_id}")
        elif check.get("kind") == "score":
            require(number(check.get("weight")) and check["weight"] > 0,
                    f"Invalid weight: {check_id}")
            require(check.get("direction") in {"higher", "lower"},
                    f"Invalid direction: {check_id}")
            poor, target = check.get("poor"), check.get("target")
            require(poor is None or number(poor), f"Invalid poor boundary: {check_id}")
            require(target is None or number(target), f"Invalid target: {check_id}")
            if poor is not None and target is not None:
                require(target > poor if check["direction"] == "higher" else target < poor,
                        f"Incorrectly ordered score boundaries: {check_id}")
        else:
            raise ValueError(f"Unknown check kind: {check_id}")
    for profile in profiles:
        applicable = selected_checks(catalog, profile)
        require(any(c["kind"] == "gate" for c in applicable), f"No gates: {profile}")
        require(any(c["kind"] == "score" for c in applicable), f"No scores: {profile}")


def profile_names(catalog, profile, active=None):
    active = set() if active is None else active
    require(profile in catalog["profiles"], f"Unknown profile: {profile}")
    require(profile not in active, f"Cyclic profile inheritance: {profile}")
    result = {profile}
    for parent in catalog["profiles"][profile]["extends"]:
        result |= profile_names(catalog, parent, active | {profile})
    return result


def selected_checks(catalog, profile):
    names = profile_names(catalog, profile)
    return [c for c in catalog["checks"] if names.intersection(c["profiles"])]


def validate_result(result, check, evidence, artifact_root):
    require(result.get("scope_sha256") == scope_hash(evidence["scope"]),
            "Result scope does not match this build/configuration")
    require(result.get("method") in check["methods"], "Wrong evidence method")
    require(number(result.get("value")), "Metric must be a finite number, not a boolean")
    require(type(result.get("samples")) is int and result["samples"] >= 1,
            "Samples must be a positive integer")
    require(unique_strings(result.get("cases")), "Invalid executed case list")
    missing = set(check["cases"]) - set(result["cases"])
    require(not missing, f"Missing required cases: {', '.join(sorted(missing))}")
    observed = result.get("observed_at")
    require(isinstance(observed, str), "Missing observation timestamp")
    try:
        instant = datetime.fromisoformat(observed.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Invalid observation timestamp") from exc
    require(instant.tzinfo is not None, "Observation timestamp needs a timezone")
    require(instant <= datetime.now(timezone.utc), "Observation is in the future")
    if result["method"] == "human":
        require(isinstance(result.get("reviewer"), str) and result["reviewer"].strip(),
                "Human evidence needs a named reviewer")
    artifacts = result.get("artifacts")
    require(isinstance(artifacts, list) and artifacts, "No evidence artifact")
    root = Path(artifact_root).resolve()
    for artifact in artifacts:
        require(isinstance(artifact, dict), "Invalid artifact record")
        relative = artifact.get("path")
        require(isinstance(relative, str) and relative.strip(), "Missing artifact path")
        require(not Path(relative).is_absolute(), "Artifact path must be relative")
        path = (root / relative).resolve()
        require(path.is_relative_to(root), "Artifact escapes the evidence directory")
        require(path.is_file(), "Evidence artifact does not exist")
        expected = artifact.get("sha256")
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
                "Invalid artifact SHA-256")
        require(file_hash(path) == expected, "Evidence artifact hash mismatch")


def evaluate(catalog, evidence, artifact_root):
    validate_catalog(catalog)
    require(isinstance(evidence, dict), "Evidence must be an object")
    require(type(evidence.get("schema_version")) is int
            and evidence["schema_version"] == 1, "Unsupported evidence schema")
    require(evidence.get("catalog_version") == catalog["catalog_version"],
            "Evidence targets a different catalog version")
    require(evidence.get("kind") in {"not_tested", "measured", "synthetic"},
            "Unknown evidence kind")
    require(isinstance(evidence.get("run_id"), str) and evidence["run_id"].strip(),
            "Missing run ID")
    scope = evidence.get("scope")
    require(isinstance(scope, dict), "Missing scope object")
    require(isinstance(scope.get("profile"), str), "Missing profile")
    checks = selected_checks(catalog, scope["profile"])
    allowed = {c["id"] for c in checks}
    results = evidence.get("results")
    require(isinstance(results, list), "results must be an array")
    require(evidence["kind"] != "not_tested" or not results,
            "not_tested evidence cannot contain results")
    by_id = {}
    for result in results:
        require(isinstance(result, dict), "Result must be an object")
        check_id = result.get("check_id")
        require(isinstance(check_id, str) and check_id in allowed,
                "Unknown or out-of-profile result")
        require(check_id not in by_id, f"Duplicate result: {check_id}")
        by_id[check_id] = result

    blockers = []
    if catalog["policy_status"] != "approved":
        blockers.append("Rubric is proposed, not approved")
    if evidence.get("catalog_sha256") != scope_hash(catalog):
        blockers.append("Exact catalog content hash is missing or does not match")
    if catalog.get("minimum_score") is None:
        blockers.append("Minimum quality score is not configured")
    for key in SCOPE_FIELDS:
        value = scope.get(key)
        if key in {"language_pair", "conditions"}:
            valid = unique_strings(value) and (key != "language_pair" or len(value) == 2)
        else:
            valid = isinstance(value, str) and bool(value.strip())
        if not valid:
            blockers.append(f"Scope field is incomplete: {key}")
    if evidence["kind"] == "not_tested":
        blockers.append("No app tests have been submitted")

    rows = []
    total_weight = sum(c["weight"] for c in checks if c["kind"] == "score")
    points, scored_count = 0.0, 0
    for check in checks:
        row = {"id": check["id"], "title": check["title"], "kind": check["kind"],
               "unit": check.get("unit", ""),
               "status": "NOT_TESTED", "reason": "No result submitted", "value": None}
        result = by_id.get(check["id"])
        configured = check.get("min_samples") is not None
        configured = configured and (check.get("threshold") is not None
                                     if check["kind"] == "gate" else
                                     check.get("poor") is not None and check.get("target") is not None)
        if result is not None:
            try:
                validate_result(result, check, evidence, artifact_root)
                if check.get("min_samples") is not None:
                    require(result["samples"] >= check["min_samples"],
                            "Insufficient sample count")
                row["value"] = result["value"]
                if not configured:
                    row.update(status="UNCONFIGURED", reason="Threshold/sample policy is unset")
                elif check["kind"] == "gate":
                    value, threshold = result["value"], check["threshold"]
                    passed = {"eq": value == threshold, "gte": value >= threshold,
                              "lte": value <= threshold}[check["operator"]]
                    row.update(status="PASS" if passed else "FAIL",
                               reason=f"Expected {check['operator']} {threshold}")
                else:
                    value, poor, target = result["value"], check["poor"], check["target"]
                    fraction = ((value - poor) / (target - poor) if check["direction"] == "higher"
                                else (poor - value) / (poor - target))
                    earned = max(0.0, min(1.0, fraction)) * check["weight"]
                    points += earned
                    scored_count += 1
                    row.update(status="SCORED", reason="Valid scoped evidence",
                               earned_weight=round(earned, 4), available_weight=check["weight"])
            except (ValueError, OSError) as exc:
                row.update(status="INVALID", reason=str(exc))
        elif not configured:
            row.update(status="UNCONFIGURED", reason="No result; threshold/sample policy is unset")
        rows.append(row)

    completed = sum(r["status"] in {"PASS", "FAIL", "SCORED"} for r in rows)
    score = round(100 * points / total_weight, 2) if scored_count else None
    failed = [r["id"] for r in rows if r["kind"] == "gate" and r["status"] == "FAIL"]
    if failed:
        status = "BLOCKED"
    elif any(r["status"] == "INVALID" for r in rows):
        status = "INVALID_EVIDENCE"
    elif blockers or completed != len(rows):
        status = "INCOMPLETE"
    elif score is None or score < catalog["minimum_score"]:
        status = "BELOW_TARGET"
    else:
        status = "READY_FOR_REVIEW"
    return {
        "schema_version": 1, "catalog_version": catalog["catalog_version"],
        "catalog_sha256": scope_hash(catalog),
        "run_id": evidence["run_id"], "scope": scope, "evidence_kind": evidence["kind"],
        "readiness": "SIMULATION_ONLY" if evidence["kind"] == "synthetic" else status,
        "evaluation_status": status, "certificate": "NOT_ISSUED", "blockers": blockers,
        "failed_gates": failed, "provisional_quality_score": score,
        "score_is_complete": scored_count == sum(c["kind"] == "score" for c in checks),
        "coverage": {"evaluated": completed, "required": len(rows),
                     "percent": round(100 * completed / len(rows), 2)}, "checks": rows,
        "limitations": ["Metrics are supplied by test producers; hashes do not prove their truth.",
                        "One scope only; no release-matrix aggregation or certificate issuance."]}


def markdown(report):
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")
    score = report["provisional_quality_score"]
    label = "unavailable" if score is None else f"{score}/100 (provisional lower bound)"
    coverage = report["coverage"]
    lines = ["# Trio evaluation report", "", f"Readiness: **{report['readiness']}**",
             "Certificate: **NOT_ISSUED**", f"Quality score: {label}",
             f"Evaluated coverage: {coverage['evaluated']}/{coverage['required']} ({coverage['percent']}%)",
             "", "## Scope", ""]
    lines += [f"- {cell(key)}: {cell(value)}" for key, value in report["scope"].items()]
    lines += ["", "## Blockers", ""]
    lines += [f"- {cell(item)}" for item in report["blockers"]] or ["- See failed/missing checks below."]
    lines += ["", "## Checks", "", "| ID | Check | Result | Value | Reason |",
              "| --- | --- | --- | --- | --- |"]
    lines += [f"| {r['id']} | {cell(r['title'])} | {r['status']} | "
              f"{cell(r['value'])} {cell(r['unit'])} | {cell(r['reason'])} |"
              for r in report["checks"]]
    lines += ["", "## Limits", ""] + [f"- {item}" for item in report["limitations"]]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path("certification/catalog.json"))
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("certification/reports/current"))
    args = parser.parse_args(argv)
    protected = {args.catalog.resolve(), args.evidence.resolve()}
    outputs = {args.output_dir.resolve() / name for name in ("report.json", "report.md")}
    if protected.intersection(path.resolve() for path in outputs):
        print("INVALID_INPUT: Output path would overwrite a catalog or evidence input")
        return 3
    code = None
    try:
        catalog, evidence = load_json(args.catalog), load_json(args.evidence)
        if isinstance(evidence, dict) and isinstance(evidence.get("results"), list):
            for result in evidence["results"]:
                if isinstance(result, dict) and isinstance(result.get("artifacts"), list):
                    for artifact in result["artifacts"]:
                        if isinstance(artifact, dict) and isinstance(artifact.get("path"), str):
                            protected.add((args.evidence.parent / artifact["path"]).resolve())
        if protected.intersection(path.resolve() for path in outputs):
            print("INVALID_INPUT: Output path would overwrite an evidence artifact")
            return 3
        report = evaluate(catalog, evidence, args.evidence.parent)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        report = {"readiness": "INVALID_INPUT", "certificate": "NOT_ISSUED", "scope": {},
                  "provisional_quality_score": None, "blockers": [str(exc)], "checks": [],
                  "coverage": {"evaluated": 0, "required": 0, "percent": 0},
                  "limitations": ["Input was invalid; this run evaluated no app behavior."]}
        code = 3
    try:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
        (args.output_dir / "report.md").write_text(markdown(report), encoding="utf-8")
    except (ValueError, OSError) as exc:
        print(f"OUTPUT_ERROR: {exc}; do not consume an older report as this run's output")
        return 3
    print(f"{report['readiness']}; certificate NOT_ISSUED; "
          f"coverage {report['coverage']['evaluated']}/{report['coverage']['required']}")
    if code is not None:
        return code
    if report["readiness"] == "READY_FOR_REVIEW":
        return 0
    return 1 if report["readiness"] in {"BLOCKED", "BELOW_TARGET"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

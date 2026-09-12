"""Check Trio repository structure, planned coverage and runtime configuration.

This tool does not build/test the app, run a demo, or issue a certificate.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit

if __package__:
    from .certify import load_json, require, unique_strings, validate_catalog
    from .execution import assess_execution
else:
    from certify import load_json, require, unique_strings, validate_catalog
    from execution import assess_execution

ROOT = Path(__file__).resolve().parents[1]
REQUIREMENT = re.compile(r"^## ((?:FR|QR|LQ)-\d{3})\b", re.M)
LINK = re.compile(r"\[[^\]\n]*\]\((<[^>\n]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")


def inside(root, relative):
    require(isinstance(relative, str) and bool(relative.strip()), "Missing relative path")
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), f"Path escapes repository: {relative}")
    return path


def without_fences(content):
    return re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$", "", content)


def anchors(content):
    result, counts = set(), {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", without_fences(content), re.M):
        heading = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", heading)
        base = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts.get(base, 0)
        result.add(base if count == 0 else f"{base}-{count}")
        counts[base] = count + 1
    return result


def check_links(root, files):
    count = 0
    for source in files:
        for match in LINK.finditer(without_fences(source.read_text(encoding="utf-8-sig"))):
            target = match.group(1).strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            destination = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            require(destination.is_relative_to(root.resolve()), f"Link escapes repo: {source}: {target}")
            require(destination.exists(), f"Broken link: {source}: {target}")
            if parsed.fragment and destination.suffix == ".md":
                require(unquote(parsed.fragment) in anchors(destination.read_text(encoding="utf-8-sig")),
                        f"Broken anchor: {source}: {target}")
            count += 1
    return count


def requirement_definitions(root):
    result = {}
    for source in (root / "spec/requirements").glob("*.md"):
        for identity in REQUIREMENT.findall(source.read_text(encoding="utf-8-sig")):
            require(identity not in result, f"Duplicate requirement definition: {identity}")
            result[identity] = source.relative_to(root).as_posix()
    require(bool(result), "No requirement definitions")
    return result


def catalog_ids(root, directory, prefix):
    content = (root / f"spec/{directory}/README.md").read_text(encoding="utf-8-sig")
    rows = re.findall(rf"^\| ({prefix}-\d{{3}}) \|", content, re.M)
    require(bool(rows) and len(set(rows)) == len(rows), f"Empty/duplicate {prefix} catalog")
    return set(rows)


def coverage_report(root):
    data = load_json(root / "harness/coverage.json")
    require(isinstance(data, dict) and type(data.get("schema_version")) is int
            and data["schema_version"] == 1, "Invalid coverage schema")
    require(data.get("status") == "planned", "Coverage registry is a plan, not execution evidence")
    definitions = requirement_definitions(root)
    mapped = data.get("requirements")
    require(isinstance(mapped, dict), "Invalid requirement map")
    require(set(mapped) == set(definitions),
            f"Requirement mapping mismatch: missing={sorted(set(definitions) - set(mapped))}, "
            f"unknown={sorted(set(mapped) - set(definitions))}")
    for identity, entry in mapped.items():
        require(isinstance(entry, dict) and entry.get("status") == "planned", f"Invalid plan: {identity}")
        require(isinstance(entry.get("family"), str) and entry["family"].strip(), f"No test family: {identity}")
        require(entry.get("requirement_document") == definitions[identity], f"Wrong definition: {identity}")
        require(inside(root, entry.get("procedure")).is_file(), f"Missing procedure: {identity}")
    rows = data.get("situations")
    require(isinstance(rows, list) and all(isinstance(row, dict) for row in rows), "Invalid situations")
    identities = [row.get("id") for row in rows]
    require(unique_strings(identities), "Duplicate/invalid situation mapping")
    require(set(identities) == catalog_ids(root, "situations", "SIT"), "Situation mapping mismatch")
    for row in rows:
        require(type(row.get("release_selected")) is bool, "Invalid release selection")
        document = row.get("document")
        require(row.get("status") == ("documented_draft" if document else "catalog_only"), "Invalid situation status")
        if document:
            require(inside(root, document).is_file(), f"Missing situation document: {row['id']}")
        else:
            require(not row["release_selected"], f"Catalog-only situation cannot be release selected: {row['id']}")
    require(unique_strings(data.get("conditions")) and set(data["conditions"]) == catalog_ids(root, "conditions", "COND"),
            "Condition mapping mismatch")
    require(isinstance(data.get("axes"), dict) and bool(data["axes"]), "No coverage axes")
    for name, values in data["axes"].items():
        require(unique_strings(values), f"Invalid axis: {name}")
    require(unique_strings(data.get("limitations")), "Missing planning limitations")
    catalog = load_json(root / "certification/catalog.json")
    validate_catalog(catalog)
    covered = set()
    for check in catalog["checks"]:
        require(set(check["requirements"]) <= set(definitions), f"Unknown requirement in {check['id']}")
        covered.update(check["requirements"])
    return {"status": "PLANNED_ONLY", "requirements_planned": len(mapped),
            "requirements_total": len(definitions), "situations_total": len(rows),
            "situations_documented": sum(bool(row["document"]) for row in rows),
            "catalog_only": [row["id"] for row in rows if not row["document"]],
            "release_selected": [row["id"] for row in rows if row["release_selected"]],
            "requirements_without_catalog_checks": sorted(set(definitions) - covered),
            "product_execution": "NOT_ASSESSED", "certificate": "NOT_ISSUED",
            "limitations": data["limitations"]}


def check_agents_skills(root):
    skills = set()
    for path in (root / ".agents/skills").glob("*/SKILL.md"):
        content = path.read_text(encoding="utf-8-sig")
        match = re.match(r"\A---\n(.*?)\n---\n(.+)", content, re.S)
        require(match is not None, f"Missing skill frontmatter/body: {path}")
        fields = dict(re.findall(r"^(name|description): (.+)$", match.group(1), re.M))
        name = fields.get("name", "").strip('"')
        require(re.fullmatch(r"[a-z0-9-]{1,63}", name) and name == path.parent.name, f"Invalid skill name: {path}")
        require(name not in skills and len(fields.get("description", "")) > 20, f"Duplicate/incomplete skill: {path}")
        skills.add(name)
        ui = (path.parent / "agents/openai.yaml").read_text(encoding="utf-8")
        require(f"${name}" in ui, f"UI prompt omits skill: {path}")
    agents = set()
    for path in (root / ".codex/agents").glob("*.toml"):
        config = tomllib.loads(path.read_text(encoding="utf-8"))
        for field in ("name", "description", "developer_instructions"):
            require(isinstance(config.get(field), str) and config[field].strip(), f"Missing {field}: {path}")
        require(config["name"] not in agents and config["name"] == path.stem, f"Duplicate/mismatched agent: {path}")
        agents.add(config["name"])
        linked = re.findall(r"\.agents/skills/([a-z0-9-]+)/SKILL\.md", config["developer_instructions"])
        require(linked and set(linked) <= skills, f"Unknown/missing agent skill: {path}")
    require(skills and agents, "No project agents or skills")
    return {"skills": len(skills), "agents": len(agents)}


def preflight(config, mode):
    require(isinstance(config, dict) and type(config.get("schema_version")) is int
            and config["schema_version"] == 1, "Invalid runtime schema")
    require(mode in {"verify", "benchmark", "demo", "release"}, "Invalid mode")
    for key in ("application", "scope", "adapters", "recording"):
        require(isinstance(config.get(key), dict), f"Invalid runtime {key}")
    gaps = []

    def text_field(obj, field, prefix):
        value = obj.get(field)
        require(value is None or (isinstance(value, str) and bool(value.strip())), f"Invalid {prefix}.{field}")
        if value is None:
            gaps.append(f"{prefix}.{field}")

    for key in ("repository", "commit"):
        text_field(config["application"], key, "application")
    for key in ("situations", "devices", "audio_routes"):
        value = config["scope"].get(key)
        require(isinstance(value, list) and (not value or unique_strings(value)), f"Invalid scope.{key}")
        if not value:
            gaps.append(f"scope.{key}")
    pairs = config["scope"].get("language_pairs")
    require(isinstance(pairs, list) and all(unique_strings(pair) and len(pair) == 2 for pair in pairs), "Invalid language pairs")
    if not pairs:
        gaps.append("scope.language_pairs")
    for key in ("fixture_revision", "processing_revision"):
        text_field(config["scope"], key, "scope")
    needed = ["build", "ui", "device_audio", "faults", "telemetry"]
    if mode == "demo":
        needed += ["voice_partner", "recorder"]
    for key in needed:
        # Adapter descriptors identify a future integration; they are not commands.
        text_field(config["adapters"], key, "adapters")
    if mode == "demo":
        for key in ("purpose", "storage_directory", "retention_policy"):
            text_field(config["recording"], key, "recording")
        consent = config["recording"].get("consent_confirmed")
        require(type(consent) is bool, "recording.consent_confirmed must be boolean")
        if not consent:
            gaps.append("recording.consent_confirmed")
    budget = config.get("cost_limit")
    require(budget is None or (isinstance(budget, str) and budget.strip()), "Invalid cost limit")
    if budget is None:
        gaps.append("cost_limit (explicit zero/local-only is valid)")
    return {"status": "BLOCKED" if gaps else "CONFIGURED_UNVERIFIED", "mode": mode,
            "missing": gaps, "executed": False, "certificate": "NOT_ISSUED",
            "next": "Connect and probe the named adapters; configuration alone cannot establish runtime readiness."}


def check_repository(root):
    coverage = coverage_report(root)
    files = [p for p in root.rglob("*.md") if not any(part in {".git", "__pycache__"} for part in p.relative_to(root).parts)
             and not p.is_relative_to(root / "harness/artifacts")
             and not p.is_relative_to(root / "certification/reports")]
    links = check_links(root, files)
    roles = check_agents_skills(root)
    preflight(load_json(root / "harness/runtime.json"), "demo")
    return {"status": "REPOSITORY_STRUCTURE_VALID", "markdown_files": len(files),
            "local_links": links, **roles, "planned_requirements": coverage["requirements_planned"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "coverage", "preflight", "analyze"])
    parser.add_argument("--mode", choices=["verify", "benchmark", "demo", "release"], default="verify")
    parser.add_argument("--runtime", type=Path, default=ROOT / "harness/runtime.json")
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            result = check_repository(ROOT)
        elif args.command == "coverage":
            result = coverage_report(ROOT)
        elif args.command == "analyze":
            require(args.evidence is not None, "analyze requires --evidence")
            evidence = load_json(args.evidence)
            require(isinstance(evidence, dict), "Evidence must be an object")
            result = assess_execution(evidence.get("execution"))
        else:
            result = preflight(load_json(args.runtime), args.mode)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if args.command == "check":
            completed = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=False)
            return 0 if completed.returncode == 0 else 1
        if args.command == "analyze":
            return {"passed": 0, "failed": 1, "blocked": 2, "invalid": 3}[result["status"]]
        return 2 if args.command == "preflight" else 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "error": str(exc), "executed": False, "certificate": "NOT_ISSUED"}))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())

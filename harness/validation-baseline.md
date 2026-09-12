# Harness validation baseline

Status: Repository tooling verified; product execution untested
Date: 2026-09-12

The baseline was checked locally on Windows using Python 3.12. The repository workflow selects Python 3.11 on hosted Linux. This record describes what was exercised, not a certificate.

- The repository checker validates Markdown file/anchor links, requirement definitions, complete planning-map references, situation/condition accounting, agent TOML and skill linkage.
- Tooling unit tests exercise the evaluator and harness error boundaries, including missing evidence, failed gates, synthetic results, invalid configuration, missing requirement mappings, duplicate IDs, broken links and path escapes.
- The skill-creator validator accepts all nine skills. Its authoring-time YAML dependency was installed in an ignored local artifact directory; the shipped harness commands use only the Python standard library.
- A fresh `codex debug prompt-input` inspection discovers all nine project skills. This checks local discovery without starting an agent turn. Custom-agent TOML is structurally validated against the documented fields; live spawning of each role was not tested.
- Empty app evidence reports `INCOMPLETE`, zero of 21 offline-car checks evaluated, and `NOT_ISSUED`. Demo preflight reports `BLOCKED` with named missing capabilities. Even filled configuration cannot claim execution.

There is no physical audio run, app build, live AI conversation, video/audio recording, twelve-hour test, user study, payment experiment, or completed product certification in this baseline. The documentation and initial research support planning those steps.

Re-run `python tools/harness.py check` after changes. Report the exact commit and observed CI result separately; the existence of a workflow file is not evidence of a successful hosted run.

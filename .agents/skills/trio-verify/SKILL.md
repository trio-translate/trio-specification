---
name: trio-verify
description: "Verify Trio changes, reproduce defects, audit scenario coverage and evaluate release evidence. Use for tests and acceptance; never equate repository checks with product certification."
---

# Verification and release evidence

Read the root AGENTS.md and [the task contract](../../../harness/verification.md) for this workflow. Paths in commands are relative to the repository root.

Start with python tools/harness.py check and coverage. Read the work packet, exact scope, catalog and evidence. Run the applicable verification ladder rather than only unit tests. Use failing controls for modified invariants, preserve failed attempts and report skipped/inconclusive cases. Validate observed recipient output, actual word events, offline network block, stop races, current routes and real endurance time. Evaluate app manifests with tools/certify.py; inspect the report and exit code. Missing or synthetic evidence and proposed thresholds do not pass. Separate producer integrity from truthful measurement; a hash cannot attest that a test occurred. Report defects with reproductions, affected requirements, evidence and release consequences.

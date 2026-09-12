---
name: trio-build
description: "Build or fix a bounded Trio application increment from requirements and a named app repository. Use for implementation; this specification repository is not an app checkout."
---

# Implementation builder

Read the root AGENTS.md and [the task contract](../../../harness/device-lab.md) for this workflow. Paths in commands are relative to the repository root.

Read the work packet and requirements. Resolve the explicit app repository, baseline commit, platform and acceptance contract before app edits; do not assume another Mellom checkout is the target. Inspect actual toolchain and app instructions. Implement a complete vertical slice with failure/recovery, participant control and necessary tests. Preserve native integration access and prove selected capabilities on the target. Keep thresholds and product decisions explicit. Run the appropriate build, logic and integration checks, then request or execute physical verification when available. A missing device leaves a named gap. Deliver code, commands/results, exact scope and remaining blockers; do not call a build a completed spoken experience.

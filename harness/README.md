# Trio product harness

Status: Working harness definition and repository tooling; app integrations pending

The harness is the repeatable working environment connecting product intent, implementation, device experiments, evidence, and commercial decisions. It supplies context, task contracts, agents, tools, fixtures, evaluation rules, and a feedback loop. It is not just a collection of prompts or a claim of universal testing.

## Start a task

Open this repository in Codex. Use the root [AGENTS.md](../AGENTS.md), [agent roster](agent-roster.md), and repository skills. Examples:

- `Use $trio-product to talk through whether the car situation should lead our first release.`
- `Use $trio-specify to turn this situation into requirements and acceptance cases.`
- `Use $trio-build to implement FR-024 in the application repository I selected.`
- `Use $trio-verify to assess the release evidence and identify what is still untested.`
- `Use $trio-demo to prepare a full spoken demonstration with screen and audio recording.`
- `Use $trio-commercial to compare alternatives and design a paid-pilot experiment.`

With Python 3.11 or newer, no third-party packages, run from the repository root:

```sh
python tools/harness.py check
python tools/harness.py coverage
python tools/harness.py preflight --mode demo
```

`check` runs structural checks and the tooling tests; exit 0 means repository checks passed. `coverage` shows planned requirement coverage and gaps; it never claims execution. `preflight` validates [runtime configuration](runtime.json); it currently exits 2 because no app/device/voice/recorder is configured. Exit 3 indicates malformed configuration. The [certification evaluator](../certification/README.md) remains the separate command for evaluating app evidence.

The [GitHub workflow](../.github/workflows/repository-checks.yml) runs the same repository checks on pushes and pull requests, on a hosted Linux runner with read-only repository permissions and pinned actions. It performs no app builds, voice calls, physical tests, deployment or certification. Maintain its action/runtime versions through the normal review process.

Runtime adapter fields are descriptive integration identifiers, not executable shell commands. Use an uncommitted local copy via `--runtime path/to/runtime.json` for actual targets; keep credentials in the host's secret system. Preflight checks declared configuration only. Even a complete configuration returns `CONFIGURED_UNVERIFIED` and exit 2 until real adapter probes/runs exist; it never launches tools from file text.

## Working loop

1. **Understand:** establish the audience, situation, problem, current alternative, and evidence of value. Talk with the owner using the product partner. Preserve open decisions.
2. **Contract:** select a bounded increment; link situation + conditions + requirements + acceptance procedures. Name the implementation repo/build, support matrix, cost envelope, and evidence required. Use the [work packet](../templates/work-packet.md).
3. **Prepare:** inspect toolchain and target capabilities. Install feasible local prerequisites within the authorized task; report physical hardware, account, or app dependencies precisely. Windows build success cannot establish Apple-device readiness.
4. **Build:** implement a useful vertical slice, with failure handling and regression tests. Keep one writer per owned area. Record significant product/architecture decisions.
5. **Verify:** run the [verification ladder](verification.md) and collect raw results. Reproduce each defect, add a test that exposes it, fix, and rerun affected coverage. Distinguish infrastructure failure from product failure and untested scope.
6. **Benchmark and demonstrate:** use [controlled benchmarks](benchmarks.md), bilingual review, and [voice/recorded demos](conversation-and-demo.md). A demo is additional evidence, not release certification.
7. **Decide:** evaluate the exact release matrix, hard gates, commercial viability, and support/rollback readiness. Missing evidence or unknown thresholds cannot pass. Only publish, charge, contact others, or spend within actual user authorization.
8. **Maintain:** turn incidents, capability changes, support feedback, and competitor moves into new work packets. Retest affected claims, update source dates and costs, and learn from actual customer use.

## Harness components and authority

| Component | Responsibility | Available now |
| --- | --- | --- |
| Product/specification | Decisions, requirements, situations, business hypotheses | Markdown with stable IDs |
| Agent configuration | Narrow roles and handoff boundaries | Project TOML agents and discoverable skills |
| Coverage planner | Every defined requirement and catalog situation accounted for | Machine-readable registry and gap report |
| Repository validator | Links, identifiers, registry, skill/agent metadata and tool regression tests | Executable locally |
| App/device adapters | Build/install/control, fresh audio, faults, telemetry | Defined in [device lab](device-lab.md); not implemented |
| Evidence evaluator | Integrity, scoped gates, provisional scores | Executable prototype; no certificate issuance |
| Voice/demo runtime | Hear, respond, drive the app, record and replay | Contract and scenario; no connected implementation |
| Commercial practice | Alternatives, pricing experiment, costs, channel evidence | Draft plan and sourced initial comparison |

The orchestrator owns the complete result. Roles cannot mark their own invented thresholds agreed, turn synthetic results into physical evidence, or approve their own unsupported marketing claims. Use independent review for material implementation/evaluation changes when delegation is requested or otherwise authorized. Share only the necessary work packet and evidence; isolate writers or use worktrees for concurrent changes. A role definition does not start a background agent.

See the [validation baseline](validation-baseline.md) for the checks actually performed and the remaining execution gaps.

## Run identity and artifacts

Each actual run needs a unique ID; spec and app commit; catalog hash; exact tool/test/fixture/engine versions; scope; capability snapshot; run type; start/end times; logs; artifacts with hashes; failures; intervention count; and reviewer disposition. Use separate statuses for `planned`, `blocked`, `running`, `passed`, `failed`, and `invalid`. Synthetic evidence is explicitly labeled. Keep immutable originals and create a new run for a retry; do not overwrite a failed run with its successful retry.

Use `harness/artifacts/<run-id>/` for local generated artifacts (gitignored), with the evidence manifest beside its referenced files. Retain shared evidence in an access-controlled artifact store under the selected retention policy. Source control contains synthetic fixtures and plans, never identifiable participant recordings or secrets. Hashes establish consistency, not trusted provenance; protected producer identity and release-wide aggregation remain integration work.

## Definition of completion

Report the delivered artifact/change, relevant checks, exact tested scope, blockers, and next smallest useful step. Repository readiness, application readiness, demo readiness, and commercial readiness are separate conclusions. No tool in this repo issues a product certificate. The desired complete harness is specified; the missing app/runtime integrations remain visible work, not silently successful placeholders.

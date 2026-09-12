# Repository agents and skills

Status: Configured project roles; application and voice integrations pending

The main conversation is the coordinator. Select the smallest useful role for the task. Model, reasoning and tool permissions inherit the host; there are no hard-coded models, credentials or permission overrides. Agents do not run merely because their files exist.

| Agent | Skill | Primary responsibility |
| --- | --- | --- |
| trio_product_partner | [trio-product](../.agents/skills/trio-product/SKILL.md) | Product conversation partner |
| trio_spec_editor | [trio-specify](../.agents/skills/trio-specify/SKILL.md) | Specification editor |
| trio_builder | [trio-build](../.agents/skills/trio-build/SKILL.md) | Implementation builder |
| trio_verifier | [trio-verify](../.agents/skills/trio-verify/SKILL.md) | Verification and release evidence |
| trio_benchmarker | [trio-benchmark](../.agents/skills/trio-benchmark/SKILL.md) | Benchmark analyst |
| trio_maintainer | [trio-maintain](../.agents/skills/trio-maintain/SKILL.md) | Capability and maintenance engineer |
| trio_commercial_analyst | [trio-commercial](../.agents/skills/trio-commercial/SKILL.md) | Commercial and competitor analyst |
| trio_conversation_actor | [trio-conversation](../.agents/skills/trio-conversation/SKILL.md) | Spoken conversation partner |
| trio_demo_director | [trio-demo](../.agents/skills/trio-demo/SKILL.md) | Voice demo director |

Codex project skills are stored in `.agents/skills`; custom agents use standalone TOML files in `.codex/agents` with name, description and developer instructions. These locations and fields were checked against official [skill documentation](https://learn.chatgpt.com/docs/build-skills) and [custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) on 2026-09-12. The format may evolve. Repository validation checks their structure; fresh-session discovery and voice runtime execution are separate checks.

Use the skills directly in a compatible local Codex session. If a host has not discovered a new skill, reload the project or start a fresh session and verify it appears; explicit reading of its SKILL.md remains possible. Configure custom agents only on hosts that support the documented format. Do not silently install global copies or duplicate names.

For requested delegation, give each agent a bounded work packet, owned files, acceptance criteria, allowed side effects and output contract. Keep agents on separate worktrees or non-overlapping files. The coordinator integrates and verifies results; preserve a failed reviewer finding rather than voting it away. One agent may perform several roles sequentially when parallelism adds no benefit.

Handoff outputs: findings/changes with file references, exact scope, commands and observed results, artifact identity, unresolved decisions and recommended next step. The conversation actor receives only its allowed participant observations. The independent verifier receives raw evidence, not the actor's claim that everything worked.

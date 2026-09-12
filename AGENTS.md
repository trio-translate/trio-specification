# Working on the Trio specification

## Product intent

Build and ship a high-quality product that solves meaningful problems, can generate sustainable profit, and can reach customers worldwide. Apply commercial judgment proportionately: audience, customer value, differentiation, distribution, pricing, operating costs, and maintenance all matter.

Prioritize a complete useful experience and learning from real usage. Treat reliability, usability, accessibility, security, and customer trust as product quality. Challenge complexity without a convincing customer or business benefit. Distinguish evidence from assumptions about demand and willingness to pay.

## Editing conventions

- Write clear English Markdown unless the user requests another language.
- Help the product owner develop files incrementally. Make useful draft proposals; do not repeatedly ask for permission for ordinary reversible edits.
- Keep the broad vision separate from first-release commitments. Do not silently promote future ideas into launch requirements.
- Treat Trio as the working name. The product owner confirmed that Mellom is a starting point and Trio should broaden its vision. See DEC-001; do not assume that prior implementation details are binding Trio decisions.
- Read [non-negotiable behavior](spec/non-negotiables.md) and DEC-002/DEC-003 before changing session, audio, offline, or recovery requirements. Preserve one-action continuous operation, the twelve-hour endurance case, word-based inactivity, offline passenger/driver use, music-muted TTS, and persistent truthful microphone feedback.
- Model reusable environmental conditions separately from situations and test their combinations. Do not reintroduce per-turn presses, routine manual restart, noise-based session timeout, or a cloud-only car path as a fallback that meets the agreed outcome.
- Keep app-authored status, errors, and guidance out of participant text areas, including temporary placeholders; icons do not create an exception. Follow DEC-004 and FR-020. Preserve Light/Dark/Auto support when refining UI requirements.
- Label unconfirmed product choices, numbers, prices, platforms, languages, vendors, and performance targets as proposals or open questions.
- Mark content `Agreed` only after explicit product-owner acceptance. Do not mistake authorization to edit for acceptance of every proposal.
- Before a substantial edit, read the relevant specification documents and linked decisions. Preserve existing IDs and resolve contradictions in affected files.
- Give each requirement observable acceptance criteria. Cover failure, recovery, participant control, and accessibility where relevant.
- Record significant decisions with rationale and consequences. Keep research findings traceable to evidence without storing identifiable participant conversations in this repository.
- Verify local Markdown links, identifiers, and scope consistency after structural changes. Report what is complete and what still blocks development.
- Do not add application code, infrastructure, or dependencies solely to make the specification look complete.

Use the [specification map](spec/README.md) as the entry point and [templates](templates/README.md) for new documents.

## Product harness

Use [harness/README.md](harness/README.md) for work spanning product decisions, implementation, verification, benchmarks, maintenance, commercialization or demos. Repository skills live under `.agents/skills`; configured roles and handoff rules are in [the roster](harness/agent-roster.md). Select only the workflow needed for the actual request; exploratory conversation should remain a useful conversation.

- Preserve access to useful device capabilities without assuming API presence means sustained or offline suitability. Follow DEC-007 and the capability contract.
- Confirm the exact application repository before app changes. This repository contains specification and harness tooling, not the Trio app.
- Keep `harness/coverage.json` synchronized with requirement/situation/condition additions. Planned test coverage is not executed coverage.
- Run `python tools/harness.py check` after changes and inspect `python tools/harness.py coverage`. Harness tooling requires Python 3.11+ and no third-party packages. App verification follows the selected stack and device matrix.
- Never report synthetic dialogue, mocked audio, a short recording or a successful build as actual physical or twelve-hour evidence. Missing adapters and unavailable devices remain explicit blockers.
- Keep app status and AI assistant output out of human participant content. Conversation actors and demo narration carry explicit origin and separate observations.
- Use current primary sources for device and competitor claims. Distinguish actual customer/payment evidence from hypotheses and AI-generated simulations.
- Keep generated recordings and sensitive artifacts outside Git. Prepare useful reviewable work within existing authorization; do not infer permission to contact others, spend money or publish from a draft commercial plan.

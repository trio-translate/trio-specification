# DEC-007: Use device capabilities and establish a complete product harness

Status: Agreed direction; implementation, budgets, and release scope Draft
Date: 2026-09-12
Decision owner: Product owner

## Context

The product owner requires Trio to be capable of using the capabilities of its host device, keep up with current devices, and have specific verification steps. They requested repository agents and skills for building, verification, maintenance, benchmarking, testing, commercialization, competitor analysis, a real conversation partner, and a full spoken and recorded demonstration.

## Confirmed direction

- Architecture must allow useful device capabilities to be integrated and exercised, even when they are not the selected path in every session. Maintain current capability knowledge.
- Treat defect prevention and verification as part of development, with explicit steps and evidence. The ambition is no bugs; a finite suite cannot prove the absence of every possible defect.
- Define a product harness spanning customer discovery through release and maintenance, with usable repository agents, skills, and verification tools.
- Include commercial judgment, competitor research, interactive conversation, and voice/recorded demonstrations in that harness.

## Proposed interpretation and consequences

Distinguish hardware presence, public API availability, permissions, installed resources, runtime readiness, selected implementation, and measured support. Access to a first-party feature does not imply that third-party apps can call it. Do not choose an abstraction that permanently prevents needed native integration.

Make every advertised combination accountable to requirements and evidence. Missing adapters, devices, human review, thresholds, or evidence are gaps, never passing results. Product tests and tests of the evaluator itself remain separate. Fix known defects affecting promised behavior before claiming acceptance; report residual uncertainty honestly.

The harness can define and plan physical tests now. Actual build, voice interaction, recording, and release certification require an application and connected runtime. Agent configuration does not supply audio hardware, a voice service, or customer demand. Customer-facing AI conversation is a separate scope decision from harness actors.

No platform, vendor, language inventory, price, model, autonomous spending, public publishing, or perpetual background agent is selected here. New detailed workflows and test packs remain proposals.

See [device capabilities](../technical/device-capabilities.md), [harness](../../harness/README.md), [commercialization](../business/commercialization.md), and [competitor analysis](../business/competitor-analysis.md).

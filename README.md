# Trio specification

Trio is a working concept for a language, translation, and mutual-understanding app, using Mellom as a starting point and broadening its vision. This repository describes the product we want to build, who it serves, how it should behave, and how we will know it works.

**Stage:** collaborative specification, before implementation. **Working name:** Trio.

The ambition is broad. The first product must solve a specific problem well enough that people choose it, return to it, and pay for it. This specification keeps those two horizons visible.

## Start here

1. Read the [specification map](spec/README.md).
2. Shape the [vision](spec/vision.md) and [initial audience](spec/audience-and-problem.md).
3. Explore the [situations](spec/situations/README.md) the product should support.
4. Agree the [first-release scope](spec/scope-and-roadmap.md).
5. Refine [requirements](spec/requirements/README.md), design, technical contracts, business assumptions, and [acceptance criteria](spec/delivery/validation-and-acceptance.md).

Current confirmed direction: [one-action continuous operation](spec/non-negotiables.md), the [offline passenger/driver conversation](spec/situations/SIT-014-car-conversation.md), and reusable [music/noise conditions](spec/conditions/README.md). Detailed mechanisms and release assignment remain under development.

The UI also requires strict separation of app status from participant text, Light/Dark/Auto appearance, a remembered last view, and a clear way back. See [interaction design](spec/experience/interaction-design.md).

## How we write this together

We work on one topic at a time and update connected documents when a decision affects them. Drafts are starting points for discussion, not claims that the product or its market has been validated.

Every specification document carries a status. `Draft` means editable working content; `Proposed` means ready for a decision; `Agreed` means explicitly accepted by the product owner; `Superseded` points to its replacement. Document agreement does not mean implementation or testing is complete.

Use stable situation and requirement IDs to connect purpose, behavior, and evidence. Record meaningful choices in the [decision log](spec/decisions/README.md), and uncertainty in [research assumptions](spec/research/assumptions.md) and [open questions](spec/delivery/risks-and-open-questions.md).

## What exists today

This is a documentation repository with substantive starter drafts and reusable [templates](templates/README.md). It contains no application implementation, selected technology stack, validated pricing, or approved release commitment. The specification map identifies which parts need deeper design before development.

An executable [evaluation prototype](certification/README.md) validates submitted test evidence and reports hard gates, provisional quality scores, and coverage. The rubric is Proposed; there is no app evidence or issued certificate. Its own automated tests exercise evaluation logic, not Trio's product behavior.

**Current writing focus:** develop concrete situations and shared conditions while preserving the agreed non-negotiable experience. Choose the first audience/release separately from defining what the product must do well.

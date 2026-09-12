# Specification map

Status: Draft

This is the product's central specification. Each subject has one primary home; other documents link to it instead of maintaining conflicting copies.

## Reading order and ownership of content

| Area | Document | Defines |
| --- | --- | --- |
| Foundation | [Vision](vision.md) | Purpose, long-term ambition, intended outcomes |
| Foundation | [Non-negotiable behavior](non-negotiables.md) | Continuous sessions, word-based timeout, honest recovery, participant text integrity |
| Foundation | [Audience and problem](audience-and-problem.md) | First customer hypothesis, jobs, alternatives, evidence needed |
| Foundation | [Principles](principles.md) | Rules for product tradeoffs |
| Foundation | [Scope and roadmap](scope-and-roadmap.md) | Candidate launch boundary, later horizons, progression gates |
| Foundation | [Glossary](glossary.md) | Shared terminology |
| Situations | [Situation catalog](situations/README.md) | Real-world contexts and their priorities |
| Conditions | [Reusable conditions](conditions/README.md) | Music, noise, and rules for combining them with situations |
| Experience | [User journeys](experience/user-journeys.md) | End-to-end flows and recovery |
| Experience | [Interaction design](experience/interaction-design.md) | Session states, participant/status separation, appearance, remembered views and navigation |
| Experience | [Continuous operation and recovery](experience/recovery.md) | Fault handling, capability loss, automatic recovery, and word-activity uncertainty |
| Experience | [Accessibility and localization](experience/accessibility-and-localization.md) | Participation across abilities, languages, and devices |
| Requirements | [Requirements guide](requirements/README.md) | IDs, priority, traceability, writing standard |
| Requirements | [Functional requirements](requirements/functional.md) | Observable product behavior |
| Requirements | [Quality requirements](requirements/quality.md) | Reliability, latency, cost, and operational properties |
| Requirements | [Language and AI quality](requirements/language-and-ai-quality.md) | Meaning preservation, uncertainty, evaluation |
| Technical | [Architecture](technical/architecture.md) | Logical boundaries, constraints, choices to evaluate |
| Technical | [Device capabilities](technical/device-capabilities.md) | Native integration access, readiness, selection, currency and runtime verification |
| Technical | [Data model](technical/data-model.md) | Entities, ownership, lifecycles |
| Technical | [API and events](technical/api-and-events.md) | Contract requirements and event semantics |
| Technical | [Security and privacy](technical/security-and-privacy.md) | Threats, controls, consent, data handling |
| Business | [Business model](business/business-model.md) | Payer, packaging, unit economics, pricing experiments |
| Business | [Commercialization](business/commercialization.md) | Customer evidence, paid pilot, economics and launch packet |
| Business | [Competitor analysis](business/competitor-analysis.md) | Dated primary sources, fair comparisons and positioning hypotheses |
| Business | [Go to market](business/go-to-market.md) | Recruitment, positioning, distribution experiments |
| Business | [Analytics and success](business/analytics-and-success.md) | Definitions of value and measurable outcomes |
| Research | [Research practice](research/README.md) | Evidence collection and interpretation |
| Research | [Assumptions](research/assumptions.md) | Unvalidated beliefs and practical tests |
| Delivery | [Validation and acceptance](delivery/validation-and-acceptance.md) | Scenario coverage and release evidence |
| Harness | [Product harness](../harness/README.md) | Agents, skills, work loop, commands and execution boundaries |
| Harness | [Conversation and recorded demos](../harness/conversation-and-demo.md) | Product partner, speaking actors, real app demos and recording evidence |
| Delivery | [Scoring and internal certification](delivery/scoring-and-certification.md) | Hard gates, quality scores, evidence coverage, automation boundaries |
| Delivery | [Release and operations](delivery/release-and-operations.md) | Delivery, support, rollout, incident handling |
| Delivery | [Risks and open questions](delivery/risks-and-open-questions.md) | Decisions and uncertainties blocking progress |
| Decisions | [Decision log](decisions/README.md) | Accepted and proposed choices with rationale |

## Traceability

Follow this chain when developing any feature:

`Audience problem -> SIT situation + COND conditions -> journey -> requirement ID -> acceptance evidence -> outcome metric`

For example, [SIT-001](situations/SIT-001-shared-device-conversation.md) needs participants to stop audio immediately. [FR-004](requirements/functional.md#fr-004--stop-and-end) defines the behavior; [QR-001](requirements/quality.md#qr-001--stop-responsiveness) defines its proposed timing target; [validation](delivery/validation-and-acceptance.md) defines the physical-device evidence required.

## Maturity of this baseline

The repository structure is ready to use. Product content is a working specification, not a complete build contract. The decision log identifies agreed outcomes, including continuous sessions and the offline car situation; proposed mechanisms remain Draft. Technical documents define design questions and constraints, not completed implementation.

Before development of a release, settle its audience, situation coverage, platforms, languages, scope, privacy choices, measurable budgets, and commercial experiment. Then expand the affected journeys, screen designs, data fields, API schemas, and test cases to implementation-ready detail.

## Working sequence

1. Agree the vision and choose one initial audience.
2. Develop the user-supplied car situation, its conditions, and the continuous-session contract; decide which situation leads the first release and observe real people attempting it.
3. Decide first-release scope and the language/device coverage matrix.
4. Refine experience, requirements, and acceptance criteria together.
5. Specify technical contracts and costs for that scope.
6. Validate with users; decide what to ship using evidence.

Record decisions as they occur rather than waiting until every file is finished.

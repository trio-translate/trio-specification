# Release and operations

Status: Draft

No release date or operating model is committed. Delivery follows the [scope gates](../scope-and-roadmap.md).

## Milestone outcomes

| Milestone | Deliverable | Exit evidence |
| --- | --- | --- |
| D0: product definition | Agreed vision, initial audience, lead situation, scope, assumptions | Decision records and research plan |
| D1: experience validation | Complete prototype of the lead journey, including failure/repair | Observed participant tasks and revised requirements |
| D2: technical feasibility | Working continuous-session slice and chosen contracts | Twelve-hour physical-device/audio evidence, offline car coverage where selected, word-timeout/recovery tests, bilingual evaluation, measured latency/cost |
| D3: pilot readiness | Usable complete experience, support, privacy, clear pilot offer | Accepted must-have requirements and operational rehearsal |
| D4: commercial learning | Consented real use and payment experiment | Repeat use, quality, cost, support, paid behavior |
| D5: expansion decision | Prioritized next situation/language or improvements | Evidence that expansion is worth its burden |

## Responsibilities to assign

Product/release owner; design/accessibility owner; engineering owner; bilingual quality reviewers; privacy/security owner; customer support contact; and operational responder. One person can hold several roles at this stage, but ownership must be explicit before a pilot.

## Operational specification needed

- Separate test and production configuration and data appropriately.
- Define secrets, configuration, deployment, rollback, and schema migration practices for the selected stack.
- Monitor successful processing, latency, service/provider failure, usage/cost, and capacity without collecting conversation content.
- Set bounded requests, concurrency, retries, abuse controls, and budget alerts.
- Define escalation, incident response, user communication, and recovery verification.
- Define backup/restore only for retained data that actually needs it; make deletion behavior consistent with backup retention.
- Re-evaluate relevant language and journey quality when models, prompts, voices, or providers change.
- Treat connection renewal, internal retries, updates, and quota handling as session-preserving operations. Do not roll out a change that routinely forces users to restart an ongoing promised session.
- Monitor unintended termination and capability stalls separately from explicit user end and word-inactivity timeout. A provider health check or alive process is not evidence of continuing useful translation.
- Gate supported device/profile claims on twelve-hour evidence, actual lock/background behavior, and relevant music/noise and offline combinations.

## Support and launch content

Prepare onboarding, supported capabilities and limitations, permission troubleshooting, correction guidance, capture/retention explanations, allowance/billing help, and a safe support channel. Support should not require participants to disclose a private conversation just to report a failure.

## Rollout

Begin with the agreed pilot cohort and observe its complete experience. Define rollout/rollback triggers using quality, access/privacy, charging, latency, and cost. Expand only when there is an owner and a tested way to detect and respond to failure. Hosting or publishing is a later delivery action, not a consequence of creating these documents.

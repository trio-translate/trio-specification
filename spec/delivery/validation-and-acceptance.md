# Validation and acceptance

Status: Draft

No application tests or user studies have been run for Trio. This is the plan for collecting acceptance evidence once a release scope is agreed. The [product harness](../../harness/README.md), [verification ladder](../../harness/verification.md), and [coverage registry](../../harness/coverage.json) now define the working process and machine-checkable planning inventory.

## Specification readiness

A selected situation is ready for implementation when its audience/outcome, included behaviors, failure/recovery paths, device/language coverage, data rules, dependencies, and measurable acceptance criteria are agreed. A technical contract must be sufficiently concrete to implement without inventing consequential product choices.

Unresolved numeric thresholds in [quality](../requirements/quality.md) and [language quality](../requirements/language-and-ai-quality.md) block acceptance of the relevant requirement. Do not reinterpret `TBD` as passing.

## Initial traceability matrix

| Situation / concern | Requirements | Required evidence | Current status |
| --- | --- | --- | --- |
| SIT-001 setup and first exchange | FR-001, FR-002, FR-003, FR-006, QR-007 | Two-participant physical-device journey and accessible text path | Not implemented or tested here |
| SIT-001 correction and clarification | FR-005, QR-003, LQ-001, LQ-002 | Deliberate-error repair, revision ordering, participant understanding | Not implemented or tested here |
| SIT-001 stop/end and interruption | FR-004, FR-007, QR-001, QR-003, QR-004 | Device/audio resource checks under late results and network/lifecycle faults | Not implemented or tested here |
| SIT-001 latency and supported quality | FR-003, QR-002, LQ-001, LQ-004 | Versioned bilingual evaluation and percentile measurements | Targets and coverage incomplete |
| Trust and abuse controls | FR-008, QR-006, QR-008, LQ-003 | Authorization, retention, diagnostics, adversarial and abuse tests | Contracts incomplete |
| Paid pilot | FR-009, QR-006 | Allowance reconciliation, limit recovery, purchase/entitlement tests if selected | Offer undecided |
| Service operation | QR-005 | Monitoring, incident response, rollback/recovery exercise | Architecture undecided |
| SIT-002 | FR-010 | Solo translation versus explanation tasks | Future scope |
| SIT-003 | FR-011 | Multi-device inclusion, attribution, echo, membership, correction tests | Future scope |
| SIT-004 | FR-012 | Two-device remote join/exchange/reconnect/end tests | Future scope |
| SIT-014 offline passenger/driver exchange | FR-013, FR-014, QR-009, LQ-004 | Cold launch with no network; fresh bidirectional speech; verified phone/earphone routes; driver has zero screen interactions | Outcomes agreed; implementation unverified |
| COND-001 music, including car | FR-015, QR-011, LQ-005 | All Trio TTS suppressed; conversation input/text remains available; music transitions and explicit optional identification handoff | Default agreed; mechanisms unverified |
| COND-002 input feedback across screens | FR-016, QR-010, LQ-005 | Every app-owned screen/state; actual input levels/routes; inactive states; noise distinct from word recognition | Outcome agreed; implementation unverified |
| Continuous one-action use | FR-017, QR-012 | Twelve real hours of useful exchange with one start and zero routine interventions; no cutoff at twelve hours | Required outcome; no endurance run performed |
| Word-based inactivity | FR-018, LQ-005, QR-012, QR-013 | Word/noise/lyrics/TTS cases, duplicate events, unknown recognition, precise timeout boundary | Duration and detailed counting policy open |
| Recovery under faults | FR-007, FR-019, QR-013 | Automatic connection/engine/route recovery; participant-level outcomes, gaps, cancellation, no false delivery | Recovery mechanisms/budgets open |
| Participant content integrity | FR-020, LQ-002 | No app-copy insertion during streaming/faults/empty states; separate accessible status; genuine spoken "one moment" preserved | Rule agreed; implementation unverified |
| Light/Dark/Auto | FR-021, QR-007 | Full screen/dialog coverage, system changes and explicit override, offline persistence, session continuity | Modes agreed; detailed behavior Draft |
| Remembered view and navigation | FR-022, FR-023, FR-008, FR-016 | Offline relaunch/return, safe fallback, no dead ends, accessible back/close, no implicit capture/history restoration, active-session continuity | Outcomes agreed; detailed behavior Draft |
| Device capabilities | FR-024, QR-014 | Runtime probes versus actual routes/resources; absent/denied/changed capabilities; selection, rollback and affected endurance | Direction agreed; adapters unimplemented |
| Defect prevention and closure | QR-015 | Complete release requirement mapping, reproducible failures/fixes, appropriate physical/human evidence and explicit gaps | Process defined; app evidence absent |

## Verification layers

Use focused automated checks for state transitions, cancellation, authorization, contracts, usage counting, and data handling. Add integration tests for the chosen processing pipeline. Run end-to-end journeys on the supported platforms and physical devices, including real microphone and speaker behavior. Bilingual reviewers evaluate meaning; participant studies evaluate task success and repair.

Build success or mocked audio tests cannot establish that a spoken conversation works on real devices. Conversely, a successful demonstration does not replace security, fault, or cost verification.

## Required combined cases

1. SIT-014 with phone mic/speaker, no network, two languages, road noise, and automatic exchanges.
2. The same car situation with music: all TTS muted; passenger text available; driver delivery paused until the passenger pauses music. Never claim the driver understood content they did not hear.
3. Each advertised earphone input/output configuration with disconnection/return, music/noise, and no network. Confirm actual routes, not just an accessory connection icon.
4. A prepared table-top conversation across twelve actual elapsed hours after one action, with continuing qualifying conversation words and normal silent intervals below the configured timeout. Include lock/background transitions and internal connection renewals.
5. Noise or identified music lyrics without qualifying conversation words, to test the separate predefined inactivity timeout. Use a controlled case with a functioning observer; a failed recognizer must not produce a false idle end.
6. Quiet recognized speech near the timeout boundary, intermittent recognition failure, duplicated provisional/final events, and Trio's own output. Verify the agreed word-event policy rather than an amplitude threshold.

For every recovery case, report restored capability and recipient, restoration time, lost intervals, unexpected output, and required touches. Zero routine interventions is an acceptance outcome, not an assumption. A partially functioning interface cannot pass a listening-only situation by substituting text.

## Evidence record

For each accepted requirement, record build/commit, processing provider/model/configuration, test date, device/OS/audio route, language direction, network condition, method, expected/actual result, failures, reviewer, and artifact location. Use synthetic or consented material and minimize sensitive content.

For endurance evidence add actual elapsed duration, power/battery conditions, background/lock coverage, language/voice resource versions, word-timeout setting/policy, engine/connection renewals, memory/thermal/storage trends, and every required intervention. For a wholly local run, confirm network blocking and record local model versions instead of inventing a provider call.

## Release decision

All requirements designated must-have for that release need passing evidence. Classify remaining defects by impact and state any accepted limitation with an owner and rationale. An unresolved core audio, privacy, access, material translation, or charging defect blocks the affected capability until resolved or explicitly removed from scope with accurate user-facing coverage.

The agreed continuity requirements cannot be marked passed with per-turn controls, periodic restarts, an app-chosen cutoff, a noise-based idle timer, or a short-duration demo. A platform/configuration that cannot support the claimed unattended experience must be fixed or excluded from that support claim. Document the incomplete outcome rather than calling a workaround graceful.

Use [scoring and internal certification](scoring-and-certification.md) to turn these requirements into versioned checks. A failed hard gate cannot be compensated by another metric; missing or unconfigured evidence blocks readiness. The initial evaluator validates submitted evidence and computes readiness, not the actual app behavior or a third-party certification.

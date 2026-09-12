# Risks and open questions

Status: Draft

## Decisions in useful order

| ID | Question | Proposed owner | Needed before | Current position |
| --- | --- | --- | --- | --- |
| Q-001 | Who is the initial audience and what recurring problem comes first? | Product owner | Scope agreement | Couples/relatives is a hypothesis |
| Q-002 | What specific outcome makes the lead situation successful? | Product owner with research | Experience validation | Shared understanding with repair proposed |
| Q-003 | Which platform/devices and language directions launch first? | Product + engineering | Contracts and quality budgets | Open |
| Q-004 | How do automatic utterances, language direction, orientation, and audio routing work for each role? | Design + engineering + research | Interaction sign-off | One-action continuity and passenger/driver roles agreed; mechanisms open |
| Q-005 | What capture, retention, account, and guest model is appropriate? | Product + engineering | Data/privacy design | Transient content proposed |
| Q-006 | What latency, quality, resource, and cost budgets must be met? | Product + engineering + language reviewers | Feasibility acceptance | Stop timing proposed; other targets open |
| Q-007 | Who pays, for what offer, and through which channel? | Product owner | Commercial pilot | No price or model chosen |
| Q-008 | What Mellom code or design should be reused after review? | Product + engineering | Architecture agreement | Mellom is a starting point; no code audit done |
| Q-009 | Which markets/age audience and processing arrangements are supported? | Product + relevant reviewers | Pilot privacy/terms | Open |
| Q-010 | Who operates the service and supports users? | Product owner | Pilot launch | Roles identified; people unassigned |
| Q-011 | Which local resources, languages, devices, and earphone routes complete offline car use? | Product + engineering | Car feasibility/coverage | Full offline outcome required; actual coverage open |
| Q-012 | How are music state, automatic transitions, and optional song identification established offline? | Design + engineering | Combined music acceptance | All TTS muted by default, including driver; passenger pauses music for speech |
| Q-013 | What duration and qualifying-word policy govern inactivity, including uncertain/unavailable recognition? | Product + engineering + language reviewers | Session acceptance | Word-based timeout agreed; duration and detailed policy TBD |
| Q-014 | What devices, power conditions, background behavior, and budgets sustain twelve hours after one start? | Engineering + product | Platform selection and endurance acceptance | Required outcome; no endurance measurements |
| Q-015 | What fallback and bounded-buffer rules preserve each participant's outcome automatically? | Product + engineering | Recovery acceptance | No routine manual restart or false delivery; detailed contracts/budgets open |

## Material risks

| ID | Risk | Response / evidence needed |
| --- | --- | --- |
| RISK-001 | Broad vision produces many incomplete modes | Agree one end-to-end launch situation; gate expansion |
| RISK-002 | Fluent errors create false confidence | Bilingual evaluation, visible repair, accurate capability claims |
| RISK-003 | Real-world audio fails despite software checks | Physical-device turn, echo, stop, interruption testing |
| RISK-004 | Participants do not understand or control capture | Test both participants' understanding and stop access |
| RISK-005 | Processing and support exceed revenue | Meter typical/heavy use; validate limits and paid demand |
| RISK-006 | Novelty produces use without retention or payment | Observe repeated real situations and concrete paid offers |
| RISK-007 | Provider or language expansion changes quality/privacy | Evaluate affected coverage and data arrangements before rollout |
| RISK-008 | Shared-device layout excludes a participant | Test orientation, text size, literacy, and assistive input |
| RISK-009 | A moving microphone meter hides a stalled recognizer or bad source attribution | Separate input, word-observer health, recognition, and delivery evidence |
| RISK-010 | Internal service limits, locks, or resource growth stop long sessions | Independent logical session lifecycle; full twelve-hour physical-device and renewal tests |
| RISK-011 | Noise, TTS, lyrics, or duplicated words corrupt the idle timer | Define qualifying word events and unknown activity; test false-reset/false-end cases |
| RISK-012 | A fallback is called graceful while the driver receives no translation | Evaluate recovery per participant and modality; record capability loss explicitly |
| RISK-013 | Full offline language/audio coverage exceeds device resources | Benchmark the complete pipeline and sustained use before selecting supported coverage |

Do not mark a question resolved because a draft suggests an answer. Record the actual decision and update affected documents. Research can reduce uncertainty without proving a hypothesis universally.

# Architecture

Status: Draft

This is a logical design brief. No programming language, framework, cloud, provider, database, native/web approach, or reuse of Mellom code has been selected. The architecture must meet the agreed [continuous-session contract](../non-negotiables.md) and provide a complete offline path for SIT-014.

## Design inputs

Begin with [release scope](../scope-and-roadmap.md), [functional requirements](../requirements/functional.md), [quality budgets](../requirements/quality.md), and the [security/privacy model](security-and-privacy.md). Reuse existing implementation only after checking its suitability against Trio's agreed requirements.

## Proposed responsibilities

| Boundary | Responsibilities |
| --- | --- |
| Participant client | One-action session start, truthful persistent audio/input state, automatic capture coordination, accessible presentation, local stop, word-activity tracking and interruption recovery |
| Trusted application service, if cloud processing is selected | Session authorization, request validation, usage/entitlements, cancellation coordination, provider credentials |
| Language processing adapter | Local/cloud recognition, translation, speech generation, automatic utterance handling, bounded per-operation timeouts, capability mapping, normalized word/result events |
| Session coordinator | User intent independent from connection/engine lifetimes; automatic renewal/recovery; word-inactivity policy; capability-specific state |
| Local resources | Offline readiness of language/voice resources, version/integrity checks, local authorization and resource budgets |
| Persistence, only for agreed needs | Minimal session metadata, account/entitlement state, optional retained content under explicit policy |
| Operations | Content-free diagnostics, usage/cost reconciliation, alerts, release controls |

SIT-014 requires recognition, translation, required TTS, session/word timing, and baseline music/input feedback to work without runtime network dependencies. Other situations may use cloud processing if they meet the same continuity and data-control requirements. A cloud-only pipeline cannot be labeled ready for the car situation. Do not implement vendor abstraction beyond realistic substitution and testing needs.

## Continuous local lifecycle

One start authorizes the prepared session; automatic word/utterance processing continues until explicit user stop/end or the predefined word-inactivity timeout. Audio, word-observer health, TTS/music policy, and logical session state remain separate. Local engines can recover or reload without asking for another start; an unavailable engine is reported as a capability fault, not user inactivity.

Benchmark recognition, translation, speech, automatic language direction, music/noise handling, and resource use together over twelve real hours. Define device/power assumptions and actual background/lock support before choosing the delivery platform. A foreground demo cannot prove unattended platform suitability.

## Proposed cloud turn lifecycle

1. Within an already authorized continuous session, the client automatically segments input and creates a session-scoped operation ID; this does not imply a new user press.
2. The service validates access, format, size, entitlement, and usage budget.
3. Processing produces typed results associated with the operation, turn, language direction, and revision.
4. The client presents only results valid for its current session/revision/cancellation state.
5. Usage is reconciled and short-lived content expires under the agreed retention rules.

Local stop must work while the service is unavailable. Canceling output invalidates late results even when provider processing cannot be stopped. A session generation/version can prevent work from an ended session entering a new one; the exact mechanism belongs in the contract design.

Cloud transport/session leases and model connection limits are internal lifetimes. Renew them within the logical session without cutting off capture, duplicating output, resetting participant state, or requiring routine confirmation. Define reconnection ordering and bounded local buffering with explicit gaps when continuity is impossible. Do not log raw content merely to measure continuity.

## Failure boundaries

Use the [recovery matrix](../experience/recovery.md) for permission failure, invalid input, provider timeout, network loss, quota pressure, malformed output, overload, interrupted audio, and unauthorized access. Use bounded automatic retry/backoff and evaluated preconfigured fallbacks. An internal failure must not terminate the logical session or masquerade as a word-inactivity timeout. A fallback provider or local model is justified only after measuring its quality, privacy compatibility, and participant outcome.

## Decisions required before implementation

Supported platforms and deployment model; complete local car capabilities and any cloud profiles; provider data handling; audio transport/format; automatic utterance/echo handling; word-activity policy and idle duration; offline language/voice provisioning; authentication/guest and long-session entitlement model; concurrency/cost/resource budgets; data lifetimes; observability; and code reuse assessment. Record substantial choices in [decision records](../decisions/README.md).

Scale initial infrastructure to the validated release. Measure latency, load, and cost before adding distributed services, multiple regions, or automatic failover.

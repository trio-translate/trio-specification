# DEC-003: Require continuous sessions after one start action

Status: Agreed outcomes; mechanisms and thresholds remain Draft
Date: 2026-09-12
Decision owner: Product owner

## Context and evidence

The product owner made continuity and genuinely graceful degradation absolute requirements. They said the app must never randomly stop on its own except for a predefined timeout based on word detection rather than noise detection. The intended interaction is one action-button press followed by leaving the phone on a table for twelve hours.

## Decision

- One start action initiates a continuous session. Routine per-turn presses, periodic confirmations, and manual restarts are not the target experience.
- Twelve hours of unattended session operation is a required endurance case, not a scheduled stop time.
- Explicit user stop/end and the predefined word-inactivity timeout are the app-controlled ways to end an active session. Internal connection or service limits must be handled within the session.
- Noise level is not the inactivity signal. The exact word-activity rule and timeout duration remain to be specified.
- Degradation must be evaluated against participant outcomes, with truthful state and automatic recovery from recoverable faults.

## Consequences

The earlier unaccepted draft proposal for explicit per-turn capture no longer describes the core experience. Capture permission, logical session state, recognition activity, TTS policy, and service connection state need separate lifecycles. Preventing echo must not require the user to restart listening after every output.

Ordinary device lock/background behavior, provider reconnection, offline readiness, usage entitlements, and resource budgets must support the promised session duration. Physical/OS impossibilities must be tested and disclosed as capability limits. They are not reasons to present an interrupted experience as meeting the requirement.

See [non-negotiable behavior](../non-negotiables.md) for the core outcomes and clearly identified implementation questions. No idle duration, infrastructure, model, device class, fallback algorithm, or power assumption has been selected by this decision.

Affected documents: [scope](../scope-and-roadmap.md), [journeys](../experience/user-journeys.md), [interaction design](../experience/interaction-design.md), [requirements](../requirements/README.md), [architecture](../technical/architecture.md), and [validation](../delivery/validation-and-acceptance.md).

Supersedes: No agreed decision. Replaces the unaccepted draft assumption that explicit per-turn input would be the baseline.

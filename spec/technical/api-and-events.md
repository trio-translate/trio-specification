# API and events

Status: Draft

This document defines contract requirements. Protocol, route names, JSON schemas, audio formats, authentication format, and versioning are intentionally not fixed yet.

## Logical operations

| Operation | Input intent | Required result / failure behavior |
| --- | --- | --- |
| Create session | Mode and supported language configuration | Session identity, capabilities, limits, applicable access |
| Submit turn | Session, operation ID, participant, input, language | Accepted identity or explicit rejection; no duplicate product operation on retry |
| Receive turn result | Authorized subscription or result request | Attributed, ordered, revision-specific state/result |
| Revise turn | Authorized author, expected revision, corrected source | New revision or explicit conflict |
| Cancel operation | Session-scoped operation and expected generation | Idempotent cancellation state; late results suppressed |
| End session | Authorized session control | Idempotent end state; no new accepted turns |
| Read allowance | Authorized usage context | Published counting unit and current allowance state |
| Join/leave room | Future shared-session authorization | Bounded access and explicit membership state |

These are responsibilities, not a commitment to one endpoint per row.

Operations needed in SIT-014 must be executable locally without an HTTP/server dependency. A logical submit-turn operation is driven by automatic utterance handling within a started session; it is not a required per-turn phone action. Internal transport and provider-session renewal must preserve the logical session and its event ordering.

## Event semantics

Candidate events include session state changes, turn accepted, recognition updated/finalized, translation ready/failed, turn revised/canceled, and usage updated. Each applicable event needs a unique ID, session ID, operation/turn ID, revision, sequence, type, and schema version. Define timestamp purpose; timestamps alone do not determine ordering.

Specify delivery guarantees, duplicate handling, resume cursor behavior, retention, and what happens when a client misses the resume window. Clients must tolerate duplicates and out-of-order events without duplicate speech or regression to an old revision.

Define separate events/state for logical start/pause/end and end reason, component availability/recovery, actual input route, music/TTS policy, and qualifying word activity. A recognition event needs stable identity/provenance and timing so interim/final duplicates, TTS echo, and identified lyrics cannot silently extend inactivity. Word-observer health is separate from detected words. These signals can be local; do not transmit private content simply to support a timer or input meter.

## Error contract

Distinguish invalid input, unsupported capability, permission/access failure, exhausted allowance, overload, timeout, canceled operation, revision conflict, ended session, and provider failure. Each error includes a stable code, safe user-facing message mapping, retry eligibility, and any effect on allowance.

An operation/connection timeout is not a user-session timeout. Only the predefined word-inactivity policy may automatically end an idle logical session. Contract errors must identify which capability was interrupted and whether delivery or captured content has a gap; they cannot imply successful graceful recovery merely because a request was retried.

Do not expose provider credentials, internal prompts, stack traces, or private conversation content in general error responses.

## Before implementation

Choose transport and define concrete request/response/event schemas, authentication/authorization, payload and rate limits, deadlines, backpressure, idempotency-key lifetime, cancellation races, compatibility, and examples for successful and failed flows. Publish machine-readable contracts only after these choices are made. Verify contracts against the actual service rather than treating an example payload as implemented behavior.

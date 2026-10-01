# Deterministic reducer semantics

Status: Proposed

This document defines the semantic rules that native Trio engines must share. It complements the [event envelope](event.schema.json) and the conceptual [data model](../data-model.md).

## Replay model

Each logical session has an ordered stream of events. A conforming reducer processes that stream into semantic state.

```text
state[n+1] = reduce(state[n], event[n+1])
```

The reducer must be deterministic for a supported contract version. Wall-clock time, device locale, network state, random values, UI lifecycle callbacks, and provider-specific behavior must not alter the result of replaying the same canonical stream.

## Ordering and identity

1. `sequence` starts at 1 for a session and increases by exactly one for each canonical event.
2. `sequence` is the ordering authority. `occurredAt` is diagnostic/context metadata only.
3. Re-delivery of an already-applied `eventId` is idempotent and must not change semantic state.
4. A different event with a sequence already applied is a contract violation.
5. A future sequence with a gap must be buffered or rejected until the missing canonical events are available. It must not be applied speculatively.
6. Reconnects and provider-session renewals do not reset logical-session ordering.

## Turn and revision rules

- A turn belongs to exactly one session and attributed participant.
- An event that names a turn must not move that turn into another session.
- Revision numbers are monotonic per turn.
- Results for an older revision cannot replace or regress a newer revision.
- A final recognition/translation result cannot be replaced by a provisional result for the same revision.
- Cancellation prevents later work for the canceled operation/revision from becoming participant-visible.
- A completed turn may still receive explicitly modeled revision events; it must not be mutated by unmodeled late provider output.

## Session lifecycle

- `session.started` establishes the active logical session.
- Pause/resume changes explicit session intent; internal connection loss is not a pause.
- `session.ended` is terminal for that logical session.
- Events arriving late after end may be observed for diagnostics, but must not reopen capture, recreate participant content, or mutate participant-visible semantic state.
- Internal operation timeouts, provider limits, or connection renewal are not session-end reasons.

## Provenance and content integrity

Participant-derived source/transcript/translation content and app-authored status/error/guidance remain distinct typed data.

The reducer must never manufacture participant text from an error, loading state, retry message, or assistant suggestion. A deliberate user action that adopts suggested text must be represented explicitly before it becomes participant-authored content.

The reducer also must not heuristically rewrite stable recognition/translation results to compensate for a weak model/provider. Corrections belong in explicit revision/model flows rather than hidden client mutation.

## Native adapter boundary

Microphone routing, permission prompts, camera state, speaker selection, background execution, UI rendering, and platform lifecycle are handled by native adapters.

Adapters may emit semantic events and react to semantic state. They must preserve event identity and cancellation semantics so that duplicate/replayed events do not duplicate output.

## Required conformance cases

The fixture corpus should grow to include:

1. one successful turn;
2. duplicate delivery;
3. out-of-order delivery and gap recovery;
4. provisional-to-final recognition;
5. provisional-to-final translation;
6. revision superseding an older result;
7. cancellation with late provider output;
8. capability loss and recovery without ending the logical session;
9. explicit session end with late events;
10. malformed/unsupported event rejection.

No fixture may be treated as evidence of real device behavior; device, endurance, accessibility, and audio acceptance remain separate.

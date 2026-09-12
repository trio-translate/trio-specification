# Data model

Status: Draft

This is a conceptual model, not a database schema. An entity may exist only in memory. Persistence requires a documented need and retention rule.

## Entities and relationships

| Entity | Purpose / conceptual fields | Lifecycle questions |
| --- | --- | --- |
| Session | ID, mode, logical intent/state, language configuration, generation, start/end timestamps and end reason | User end or word timeout? How do engines/connections renew independently? |
| Participant | Session-scoped ID, role, language, input/output preferences | Guest or account? What survives leaving? |
| Turn | ID, session, speaker, input kind, source language, sequence, state | How are canceled/failed turns represented? |
| Turn revision | Turn ID, revision number, corrected source, superseded revision | Who may correct? What is visible after replacement? |
| Translation result | Turn/revision, target language, text, finality, processing version | When must an older result be discarded? |
| Audio artifact | Owning turn/revision, purpose, format, expiry | Stream-only or temporary storage? How is playback invalidated? |
| Consent/preference state | Session/participant, relevant notice version and choice | How do shared-device participants understand and express choices? |
| Usage record | Operation ID, metered unit, status, provider cost linkage | Idempotency, reconciliation, retention, access |
| Entitlement | Payer/account/guest binding, plan/allowance, validity | Needed for the selected commercial offer only |
| Saved conversation | Explicitly selected retained content and ownership | Future/undecided; requires access and deletion design |
| Input/output state | Actual input route, capture permission/state, relative input level, selected/permitted output routes | Local ephemeral state; do not persist sound samples just to draw a meter |
| Music policy state | Manual/detected music state, provenance, TTS suppression, resumed-output generation | How are false detection, gaps, and obsolete queued speech handled? |
| Offline readiness | Language/direction, local recognition/translation/voice resource versions, integrity/availability, local entitlement validity | Which capability is missing? What preparation is required? |
| Word activity | Session, last qualifying word time/event identity, observer health, predefined timeout, accrued idle time | How are provisional results, duplicates, lyrics, TTS and unknown observation handled? |
| Recovery state | Capability, fault/retry state, connection generation, lost interval, bounded queue metadata | How does recovery preserve session intent, privacy, ordering, and truthful delivery? |

## Invariants to preserve

- A turn belongs to one session and one attributed participant.
- Every result names the exact source revision and target language it represents.
- Revisions are ordered; older results cannot replace a newer revision.
- Ended-session or canceled-generation work cannot restart capture/playback.
- Product usage counting uses a stable operation identity; provider costs remain separately auditable.
- Language choice is not identity or proof of authorization.
- Guests on a shared device must not inherit access to previous conversations unintentionally.
- A provider connection's expiry is not the logical session's end; automatic recovery cannot override an explicit user pause/end.
- Word activity derives from qualifying fresh recognition, not input amplitude, processing heartbeats, or repeated events. Keep content only where required for processing; timing/identity can be tracked without copying words into analytics.
- Offline-ready is assessed per actual required recognition/translation/voice capability, not one generic connectivity flag.
- Continuous operation does not imply twelve hours of retained audio or transcript. Queues, recognition context, and diagnostics require explicit bounded lifetimes.

## Retention proposal

Use transient conversation content by default, with no saved history unless explicitly selected. This does not mean zero external retention: document actual provider processing, diagnostics, backups, and deletion behavior before making user-facing promises.

Create a data inventory with each field's purpose, location, access, retention duration, deletion trigger, and provider transfer. Exact durations are TBD. Sensitive raw content does not belong in general analytics or this Git repository.

## Before implementation

Specify concrete field types, cardinalities, size limits, optionality, ownership checks, lifecycle transitions, storage encryption, retention jobs, and schema migration behavior for entities actually needed by the agreed release.

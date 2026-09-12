# Continuous operation and graceful recovery

Status: Draft mechanisms under the agreed [non-negotiable outcomes](../non-negotiables.md)

Recovery must preserve the user's active session and the relevant participant's ability to understand. A surviving process, unchanged screen, or spinning microphone animation alone does not meet this requirement.

All recovery messages belong in the separate app-status region defined by FR-020. Never replace transcript or translation text with "One moment", "Reconnecting", or an error explanation, even with an icon. Preserve existing content or leave missing output empty while reporting its state separately.

## Proposed recovery matrix

| Event | Automatic behavior to design and verify | What must be visible / preserved |
| --- | --- | --- |
| Cloud connection expires or rotates | Renew/replace the internal connection within the same session; keep turn identity and cancellation state | No routine user restart; no duplicate or missing output hidden as success |
| Internet disappears | Use a prepared, evaluated local path where supported; otherwise maintain the session with a specific impaired state and retry connectivity | A full offline car session keeps its capabilities; a cloud-only path cannot claim local fallback it does not have |
| Recognizer hangs or restarts | Restart the component without ending session intent; track any unobserved interval | Distinguish actual input from working word recognition; unknown activity cannot cause a false idle timeout |
| Translation fails for an utterance | Bounded automatic retry or an evaluated compatible fallback, without blocking all later turns indefinitely | Mark pending/failed interval or turn, preserve order and revision meaning, never invent a translation |
| TTS fails | Restore local/selected voice automatically if possible; keep available text | A listening-only recipient remains undelivered until usable audio returns; text alone is not full recovery |
| Music becomes present | Apply muted-TTS policy; continue available input/text processing | Explain that speech is muted; in the car the passenger pauses music when audio is needed |
| Earphones disconnect | Try a preconfigured, appropriate route or restore the prior route when available | Do not silently broadcast private speech on a speaker; show output unavailability if no permitted route exists |
| Ordinary lock/background transition | Maintain the promised supported session behavior and required audio resources | No routine wake/tap requirement; test real supported platform behavior |
| OS call/audio interruption | Preserve intent and recover allowed audio automatically when access returns | Identify actual interruption and any missed interval; specific platform behavior needs evidence |
| Explicit user stop/end or permission revocation | Honor stop/revocation immediately; do not restart capture through recovery | No canceled speech returns; restored permission after revocation needs an appropriate deliberate action |
| Resource or entitlement pressure | Use only evaluated adaptations that maintain the agreed outcome; readiness should prevent predictable mid-session exhaustion | No surprise hard cutoff, hidden charge, invisible quality reduction, or mandatory renewal prompt |
| Power loss, hardware failure, or OS process termination | Continued live capture may be impossible; record/reveal the interruption on return where possible | Do not claim uninterrupted operation or manufacture what happened while unavailable |

The matrix defines required properties of proposed responses, not proof that any particular platform, vendor, or fallback satisfies them. If an event cannot be recovered while preserving the participant outcome, mark the affected capability unavailable and record a failed/degraded acceptance case. Do not redefine it as success because the UI stayed open.

## Independent state and intent

Track logical session intent, actual microphone availability, word-observer health, per-turn processing state, speech output availability, music policy, and external connection state independently. Maintain a generation/token that prevents recovery work from reviving a user-ended session.

Internal retry deadlines and provider maximum connection lengths govern individual components. They must not be wired to logical session end. Recoverable components need health checks and bounded retry/backoff to avoid both silent stalls and excessive battery/network/cost use. A health heartbeat is not a conversation word event.

## Word-inactivity accounting during recovery

Proposed rule: freeze inactivity accounting while no trustworthy word observer is available, preserve previously accrued idle time, and resume accounting when observation recovers. Do not reset the timer using ambient noise, a reconnect event, a duplicate transcript, or a processing heartbeat. Fresh qualifying conversation words reset it according to FR-018.

This conservative unknown-activity policy is a proposal to avoid terminating a session because the app failed to listen. Its exact treatment of buffered timestamps, partial words, uncertain recognition, and timer-boundary races must be settled before implementation. A continuously failed observer remains a visible fault and fails the recovery requirement; it does not become a valid twelve-hour session by leaving the timeout frozen.

## Bounded buffering and continuity

Transient local buffering may bridge brief faults only under the agreed capture/data policy. Define a finite duration/size, what is dropped when full, and how missing intervals are represented. Do not accumulate twelve hours of private audio by default in the name of recovery. Do not silently upload offline-captured material once internet returns.

Recovered results retain original turn order, attribution, and revision. Discard obsolete/canceled output and distinguish delayed text from current conversation. Avoid automatically reading a long queue of outdated TTS after audio returns or music ends. Define how important undelivered turns are exposed and can be replayed intentionally without requiring an action merely to keep new conversation running.

## What counts as intervention

Count every routine touch, repeated start, turn button, periodic confirmation, screen wake, app reopening, route repair, account renewal, or paywall needed to sustain the session. The target for a healthy twelve-hour run is zero after start. Track optional user-selected corrections, requested configuration changes, and the explicitly agreed music pause separately; do not use that distinction to hide repeated recovery actions.

Acceptance links: FR-017 through FR-019, QR-012/QR-013, and [validation](../delivery/validation-and-acceptance.md).

# Interaction design

Status: Draft

## Shared-device layout direction

For two screen-reading participants, propose equal prominence for their languages and controls understandable from each position. Compare one shared reading direction with opposing reading directions using real device placement. In [SIT-014](../situations/SIT-014-car-conversation.md), roles differ: the passenger operates the interface, while the driver receives audio without using the screen. Equal participation does not require identical views or actions.

Do not rely on flags as the only language label. Use recognizable language names and distinguish participant identity from language selection. Support text enlargement and long translations without hiding stop controls.

## One-action session lifecycle

The [non-negotiable contract](../non-negotiables.md) is one start action and continuous operation, including the twelve-hour unattended case. Segment utterances and route translations automatically. Optional correction and stop controls stay available; they are not routine prerequisites for the next turn.

| Logical session state | Meaning | Expected transition |
| --- | --- | --- |
| Ready | Prepared configuration; no active capture | One start action begins the session |
| Active | Session is authorized and running | Automatic listening, recognition, translation, output, and internal renewal |
| Active with impaired capability | A named input/processing/output capability is unavailable | Truthful indication and automatic recovery; no false claim that everyone received translation |
| Paused by user | The user deliberately stopped activity while preserving context | Resume requires a deliberate action |
| Ended by user / word inactivity | Session is closed with an explicit reason | A new session requires a new start |

Input capture, word recognition, individual turn processing, playback, and music muting have separate state. Translation can be processing while later input arrives. Muted output is not stopped capture; a disconnected provider is not an ended session. Avoid a single state flag that makes one local failure stop the whole experience.

Coordinate microphone and speech output to prevent echo/self-translation and to handle participants speaking during output. Any temporary input suppression must be bounded and automatically return to listening; it cannot silently lose participant speech and still claim uninterrupted delivery. The exact echo/barge-in mechanism requires validation on supported routes.

## Music, noise, and microphone visibility

Apply [COND-001](../conditions/COND-001-music.md) and [COND-002](../conditions/COND-002-noise-and-input-feedback.md) together when relevant. Show microphone state/level on every Trio-controlled screen, independently from processing/word-detection state. Never open capture simply to keep an indicator moving.

Music mutes all Trio TTS by default without stopping available capture or text translation. This includes the car driver: the passenger pauses music when spoken translation is needed. Proposed transition rule: do not automatically play suppressed backlog when music ends. Do not automatically switch to another app for song identification.

## Word-based inactivity

The predefined timeout uses recognized conversation-word activity, never volume/noise alone. Duration and uncertain-word handling remain open. Show timeout configuration before start without requiring periodic check-ins. The meter, provider heartbeat, music detection, and word-activity clock are distinct signals. Processing failure cannot masquerade as user inactivity. Twelve hours is not an automatic end threshold.

## Stop, cancel, and end

- **Stop audio / pause by user:** stop local capture and playback, invalidate pending speech output, and return to a safe non-capturing state. It must work without a network round trip. Recovery must not automatically undo this deliberate pause.
- **Cancel turn:** discard or mark the selected unfinished turn as canceled. Late results cannot resurrect it.
- **End session:** stop audio and further input, terminate the session, and apply its retention rules.

Labels and placement must make these differences clear without adding friction to the urgent stop action. In multi-device modes, local stop and ending a room require separate, explicit semantics. Internal service timeouts do not invoke these user controls; they trigger recovery within the authorized session.

## Translation and repair

Show source and translation as linked content. Distinguish provisional recognition, final recognition, pending translation, and revised results. A correction updates the translation's version and suppresses obsolete queued playback. Never silently replace already-heard words and assume the recipient noticed.

Offer a neutral clarification action such as asking the other participant to repeat or explain. Generated explanation or suggested replies are separate from the speaker's words.

## Decisions to resolve with prototypes

Automatic utterance boundaries, speaker/language direction, echo/barge-in handling, view orientation, output defaults under music, correction presentation, timeout duration/counting, and truthful recovery feedback. Hold-to-talk and manual per-turn switching cannot be the required core flow. Evaluate complete unattended conversations as well as short interactions.

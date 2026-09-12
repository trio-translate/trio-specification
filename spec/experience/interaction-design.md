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

## Participant content and app status

Under [DEC-004](../decisions/DEC-004-separate-app-text-from-participant-content.md), participant input fields, transcript/translation panes, live captions, and conversation-message bodies are reserved for participant-derived text. Status prose must not appear inside, over, or in place of those content areas. A different color, spinner, app avatar, or icon in the same area is insufficient separation.

| Content or state | Where it belongs |
| --- | --- |
| What a participant actually said/typed, or its translation | The appropriate participant content area |
| Waiting, listening, reconnecting, timeout, muted speech, or error explanation | A distinct app-status/control region outside participant content |
| Empty-state guidance or example wording | External field labels/help outside the empty participant text area |
| Language/speaker labels and provisional/revised state | Separate structural metadata or controls, never text appended to the utterance |
| Requested explanation or suggested reply | A separate assistant area; no automatic insertion as a participant's message |

Example: if a translation is delayed, keep the prior valid translation clearly associated with its own turn and leave the pending turn's translation empty. Put any necessary processing indication in the app-status region. Never place "One moment" in the translation field and later replace it with the real translation. Keep status communication brief so continuous use does not require reading a stream of app narration.

This separation must survive streaming, correction, recovery, session end, every locale, and both Light and Dark appearance. If a user deliberately adopts a suggested reply, record that action before treating the resulting text as their chosen content. Do not filter a genuinely spoken phrase merely because it matches a status message.

## Appearance modes

Support **Light**, **Dark**, and **Auto** throughout Trio under [DEC-005](../decisions/DEC-005-support-light-dark-and-auto.md). The working Auto behavior follows system appearance and responds to system changes. An explicit Light or Dark choice stays selected even if the system changes. Auto as the initial default is a proposal, not an agreed preference.

Proposed implementation contract: remember the chosen mode locally, apply it before the first content render on return, and support changes without restarting the app or session. If no system preference is available, use a documented stable fallback; selecting Light or Dark must still work. Do not add location access or a custom day/night schedule to implement Auto.

Theme changes preserve participant text/drafts, focus, scroll position, microphone/capture, playback/music state, session identity, and word-inactivity timing. They must not request permission again, create a conversation turn, or trigger a routine interaction. Apply the resolved appearance consistently to all Trio-owned screens, settings, dialogs, statuses, and persistent microphone controls. Native OS surfaces follow their supported platform behavior.

Validate legibility, contrast, focus indicators, participant differentiation, and status/content separation in both appearances, including enlarged text and reduced motion. Exact colors and transition effects remain design work.

## Navigation and view restoration

Remember the last applicable view under [DEC-006](../decisions/DEC-006-remember-view-and-provide-a-way-back.md). Proposed baseline: persist the durable view locally, restore it on return/relaunch offline, and avoid restoring a transient modal as a trapping destination. Use the main conversation/home view when a remembered destination is unavailable or no longer authorized.

Every app-owned secondary screen, modal, overlay, and full-screen mode provides an understandable Back or Close route. A direct entry or root with no history has a stable main-view route. Verify visible/accessibly named controls as well as platform back conventions; hidden gestures alone are insufficient.

Navigation state is separate from session intent and retained conversation data. Navigating within a running session must not stop capture, reset word activity, or hide microphone/stop controls. A cold relaunch can restore the view without restarting capture, rejoining a room, or recreating private content. Back must not secretly mean End session or Delete. Any needed fallback explanation stays in the app-status area.

Test settings, help, corrections, errors, full-screen conversation views, dialogs, direct links, and invalid restored destinations in both appearances, enlarged text, and supported assistive inputs. Temporary drafts and scroll positions need an explicit retention/restoration policy rather than being assumed part of remembering the view.

## Decisions to resolve with prototypes

Automatic utterance boundaries, speaker/language direction, echo/barge-in handling, view orientation, output defaults under music, correction presentation, timeout duration/counting, and truthful recovery feedback. Hold-to-talk and manual per-turn switching cannot be the required core flow. Evaluate complete unattended conversations as well as short interactions.

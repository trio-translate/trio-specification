# User journeys

Status: Draft

## Journey A: shared-device conversation

Source: [SIT-001](../situations/SIT-001-shared-device-conversation.md).

| Step | Participant intent | Required experience | Recovery |
| --- | --- | --- | --- |
| Enter | Start talking with someone | Clearly find conversation mode and supported languages | Explain unsupported selection |
| Prepare | Know what the device will do | Set languages, show capture/retention behavior, choose output | Typed mode if microphone unavailable |
| Start and speak | Begin a continuous conversation with one action | Visible capture state, automatic utterance segmentation and language direction | Optional cancel, edit, clarification, or pause |
| Understand | Read/hear the other person's meaning | Source and translation, language/speaker labels, finality state | Replay, correction, clarification |
| Reply | Speak naturally in the continuing session | Automatically process the next participant's turn without a touch | Prevent echo and incorrect attribution; expose uncertain input |
| Repair | Fix a misunderstanding | Visible source revision and replacement translation | Keep old output identified as superseded |
| Finish | Stop and leave confidently | Stop all local capture/output; end session; explain retention | Show recoverable end failure without resuming audio |

The interface must support repeated turns and optional repairs for twelve hours without routine intervention. Automatic recovery keeps the logical session active through recoverable interruptions. Only user stop/end or the predefined word-inactivity timeout ends normal app-controlled session operation.

## Journey B: first use and permissions

Explain immediate value before requesting device permissions. Request a microphone when speech is chosen, explain the reason in the participant's language, and preserve typed access after denial. Account creation is an unresolved product decision; do not insert it into the core flow by default.

## Journey C: usage limit and paid continuation

If the selected commercial model has usage limits, show the allowance and counting rule before paid use and verify readiness for the promised session. Commercial policy must sustain the unattended duration without an unexpected cutoff or forced mid-session purchase. Do not create unauthorized charges. Resolve sufficient entitlement, offline validity, and resource reservation before launch; a manual payment interruption does not pass the one-action experience. Purchase cancellation/failure before readiness leaves stop/end and existing content usable.

## Journey D: return visit and deletion

Decide which preferences can be remembered and which content is discarded. If saved history is selected, define how the user finds it, deletes it, and understands any processing or backup delay. Shared-device users must not unexpectedly expose someone else's previous conversation.

## Journey E: passenger-operated car conversation

Source: [SIT-014](../situations/SIT-014-car-conversation.md).

The passenger prepares the two-language offline configuration and actual microphone/output route, then starts once. Utterances and replies are handled automatically. The driver listens to translations without looking at or operating the device; a spoken reply must not require a driver touch. Optional correction and pause are handled by the passenger.

With music present, available input/text processing continues, all TTS is muted by default, and driver translation delivery is explicitly paused. The passenger pauses music when spoken translation is needed. Noise affects input quality; the passenger sees the actual microphone signal on every Trio-controlled screen. Neither music nor noise ends the logical session. The word-inactivity timeout follows FR-018, with identified lyrics and self-generated speech excluded by the proposed counting rule.

Test offline cold-start, automatic exchanges, input/output routing, music/noise together, lock/backgrounding, recovery, and word timeout. Pre-session readiness and optional deliberate corrections are different from recurring interventions required just to keep running.

## Before implementation

Attach a screen/state inventory for the selected platform, final interaction copy for the selected locales, permission and interruption flows, navigation behavior, accessibility reading order, and a clickable prototype for the candidate launch journey. Future situations need equally complete journeys before entering delivery scope.

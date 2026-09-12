# SIT-001: Two people sharing a device

Status: Draft
Scope: Candidate launch

## People, trigger, and outcome

Two people are physically together and do not share a fluent language. One has a supported device. They want to exchange a message, understand the response, and resolve mistakes without needing an interpreter present.

Example research context: a person and a visiting relative making plans together. The task is complete when both can restate the relevant plan, or can clearly identify what remains unresolved.

## Preconditions

The selected language directions and device are supported. Each participant can see or hear the information they need. The device has connectivity if the selected implementation requires it. Participants understand when input is captured and have an obvious way to stop.

## Main journey

1. The initiating participant opens Trio and selects each person's language.
2. Both participants see understandable controls and what will be captured or retained.
3. One participant presses start once; the session continuously detects and segments speech without per-turn controls. Typed input is also available.
4. Trio shows source text and the translation with distinct provisional/final states. Playback is available according to the selected preference.
5. A participant can replay, correct the source, or ask for clarification.
6. The other participant speaks without a button press or reconfiguration; utterance handling and return to listening are automatic.
7. Either participant can reach the shared stop control. Ending the session stops capture/output and states what happens to session data.

## Failure and recovery

- Wrong language: change the participant's language and retry the affected turn; do not silently relabel previous messages.
- Poor recognition: edit or repeat the source and regenerate its translation as a visible revision.
- Overlapping speech: show an actionable retry/turn-taking state if detected; never promise reliable automatic speaker separation without evidence.
- Permission denied: explain how to enable the microphone and offer typed input immediately.
- Connection loss: keep the logical session active, make processing/delivery gaps visible, and automatically recover using the agreed local/retry policy. Never replay stale output or require a routine new start on reconnect.
- Playback captured by the microphone: the audio lifecycle must prevent self-translation loops; verify on physical devices.
- Usage/entitlement readiness: validate sufficient access for the promised session before presenting it as ready; do not require a mid-session purchase or silently end at an internal quota boundary.

## Completion and verification

Both participants can follow their own view, take a turn, correct a deliberate recognition error, and stop independently from their physical positions. Observe whether they reach the intended shared outcome; a fluent translation alone is insufficient evidence.

Verify permission denial, connection loss, correction ordering, playback interruption, device interruption, and session end. Include twelve actual hours after one start action, automatic recovery, and the predefined word-inactivity timeout. Music and noise conditions apply where present. The quality budgets and actual supported matrix must be agreed before acceptance.

## Traceability

- Journey: [shared-device journey](../experience/user-journeys.md#journey-a-shared-device-conversation).
- Behavior: FR-001 through FR-009 and FR-015 through FR-019 in [functional requirements](../requirements/functional.md).
- Quality: QR-001 through QR-008 and QR-010 through QR-013 in [quality requirements](../requirements/quality.md).
- Meaning: LQ-001 through LQ-005 in [language and AI quality](../requirements/language-and-ai-quality.md).
- Evidence: [validation and acceptance](../delivery/validation-and-acceptance.md).

## Decisions still needed

Initial audience and language set; physical device/platform matrix; view orientation; automatic utterance-boundary mechanism; playback default; consent presentation; network retry behavior; retention; numeric performance and cost budgets.

Automatic turn handling and one-action continuity are confirmed outcomes under [DEC-003](../decisions/DEC-003-continuous-one-action-sessions.md); select mechanisms that meet them.

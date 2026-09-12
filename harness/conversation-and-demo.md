# Conversation partner and recorded voice demonstrations

Status: Requested harness capability; execution design Draft

## Two useful kinds of conversation

The **product partner** is a real working conversation partner for the owner: listen to the question, remember agreed decisions, explore examples, challenge weak assumptions, and offer a concrete next step. Do not turn every exploratory remark into a requirement or respond with a wall of process. Discuss freely; label proposals and update files when requested or clearly intended. Use the `trio_product_partner` agent and `$trio-product` skill.

The **conversation actor** participates in a demonstration or test as an explicitly identified AI speaker. It responds to what the other participant actually said or received, asks natural clarifying questions, and maintains a coherent goal across turns. It can speak with the owner or another actor. It must not pretend to be a real recruited customer or supply evidence of demand. Customer-facing AI companionship/practice remains a separate proposal until selected for app scope.

## Interaction contract

Give each actor a role, language, situation, private goal, allowed observations, speaking style, and stopping condition. Keep the listener from seeing source-language text or expected answers that Trio failed to deliver. Otherwise the actor can hide translation failures by understanding information unavailable to the participant it represents. Separate the actor from the translation system under test and from the independent evaluator.

Support live listening, contextual responses, natural pauses, interruption/barge-in, repair, turn overlap, and explicit stop. Use licensed synthetic voices or a consenting speaker; no unapproved voice imitation. Keep per-session memory bounded and apply deletion/retention rules. Distinguish agent persona speech from demo narration and Trio's TTS.

AI-origin speech must be identifiable in the harness and recording metadata. If future customer-facing AI conversation is adopted, design a distinct assistant area; do not silently place app-generated replies into human participant fields. Do not change FR-020 or the human-word inactivity rule merely to make an AI-only demo pass. Synthetic acoustic fixtures may stimulate the test path, but the resulting run remains synthetic and cannot alone establish real human conversation performance.

## Demo modes

| Mode | What it demonstrates | Limitation |
| --- | --- | --- |
| Live owner + AI actor | Responsive spoken conversation using the real app and its actual output | Requires available voice, app, audio routes, and recording permissions |
| Two actors through Trio | Repeatable full exchanges and repair with separate observations | Synthetic actors; no user research or sole language-quality certification |
| Physical device demonstration | Actual microphone/output routes, visible app behavior and fault recovery | Only qualifies the recorded device/scope and duration |
| Digital simulation | Contract/UI behavior with injected fixtures | Explicitly labeled simulation; no physical audio/endurance proof |

The demo director drives setup, app UI, actors, recording, timestamps, and final replay. It records required operator touches rather than invisibly making extra taps to keep the conversation running. Separate setup actions, optional user changes, scripted music pause, explicit end, and routine recovery interventions. Do not count actor chatter as evidence of a user's real intention to keep a session alive.

## Complete demonstration sequence

Use [the starter scenario](scenarios/demo-car.md) and resolve language/device/timeout choices in the run packet. Proposed sequence:

1. Preflight app build, physical route, selected language resources, voice runtime, recorder, storage, permission/consent, and cost limit. Report missing capabilities before claiming readiness.
2. Prepare resources, then block network on the product device for the offline case. Mark pre-session setup separately from the start action.
3. Start synchronized screen and audio recording. Use a sync marker; measure clock offsets/drift. Confirm captured sound is audible and assigned to the correct tracks.
4. Start Trio with one action. Conduct fresh bidirectional exchanges with names, numbers, negation, a natural question and a repair. The listener must react only to received translation.
5. Add noise and music. Confirm truthful mic feedback, continuing passenger text and suppressed Trio TTS. The driver-role actor must not answer unheard translations. The passenger pauses music before spoken delivery is needed.
6. Exercise a declared recoverable fault and verify restoration, gaps, ordering and touches. Show appearance/navigation without disrupting the session. Never inject a direct app-state change and present it as a real user interaction.
7. End explicitly. Verify capture/output and recording release, cancellation of pending output, and no restart after returning to the remembered view.
8. Open and listen to the actual recording. Check beginning, transitions, both voice directions, repair, ending, track routing, synchronization, silent/dropout intervals, transcript alignment and file integrity. Report observed results and defects with timestamps.

A short demo cannot establish twelve-hour endurance. That is a separate actual-duration run. Time-lapse video must link to the continuous original and timing evidence.

## Recording bundle and publication

Deliver an uncut playable screen-and-audio recording, separate source/recipient audio tracks where feasible, timestamped transcript/subtitles with speaker and origin, event/action timeline, exact build/scope/fixture identities, result summary, limitations, and artifact hashes. Record interruptions honestly. An edited presentation may accompany the original with a cut list; it cannot replace raw evidence.

Recording permission is separate from permission to start conversation. Synthetic actors avoid participant privacy issues; when a person joins, establish the intended recording purpose, sources, storage/access, retention and consent before capture. Store private recordings outside Git. Publication, public uploads and external sharing require actual authorization; preparing a local demonstration does not authorize them.

## Current execution gap

This repo supplies role instructions, scenario, preflight and artifact contract. No Trio app, speech engine, actor voice service, physical-device adapter, or recorder is connected by these files. Current preflight must say `BLOCKED`. Text roleplay, a generated audio file or a storyboard cannot be reported as a completed live app demonstration.

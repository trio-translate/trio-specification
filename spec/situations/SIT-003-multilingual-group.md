# SIT-003: A multilingual group together

Status: Draft
Scope: Future candidate

## People, trigger, and outcome

Several people with different languages are physically together. Each wants to follow the discussion and contribute without depending on the most fluent participant.

## Proposed journey

1. A host creates a session and explains participation and capture behavior.
2. Each person joins, selects a language, and sees who is participating.
3. The active speaker is identified through a validated automatic attribution mechanism; routine phone presses to acquire each turn cannot be required under the continuous-session contract.
4. Each recipient receives the appropriate translation with consistent message ordering.
5. Participants ask for clarification, correct their own input, and control their local audio.
6. Leaving removes a participant's session access according to the agreed rules; ending the room stops further session activity.

## Failure and recovery

Consider simultaneous speech, a person with no device, multiple microphones capturing the same sound, joining late, unexpected guests, disconnection, and a host leaving. Define what local stop, leaving, and ending the whole room do before implementation.

## Completion and acceptance direction

Every supported participant can identify the speaker, follow a corrected turn, contribute, and leave. Test echo, ordering, correction propagation, access revocation, and participant inclusion on multiple physical devices.

Related proposed behavior: FR-011 in [functional requirements](../requirements/functional.md). Group-size, latency, and cost targets remain unset.

## Open questions

Who pays? How many participants and languages? Shared device, individual devices, or both? How does automatic attribution work reliably, and how can participants optionally correct it? Is playback personal, shared, or text-first? What happens when someone without the app is speaking nearby? Apply the core one-action, twelve-hour, word-timeout, and recovery requirements when specifying this conversation mode.

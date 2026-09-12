# Non-negotiable product behavior

Status: Agreed for the core outcomes below; detailed mechanisms and thresholds remain Draft
Sources: [DEC-002](decisions/DEC-002-car-music-and-input-feedback.md), [DEC-003](decisions/DEC-003-continuous-one-action-sessions.md), [DEC-004](decisions/DEC-004-separate-app-text-from-participant-content.md)

## One action, then continuous use

The target interaction is one press of the start/action button, followed by a conversation the phone can support unattended on a table for **12 hours**. The user must not hold a button, approve every turn, restart listening after each translation, dismiss routine prompts, or keep waking the screen to continue.

First-time OS permissions and an initially usable configuration must be prepared honestly. Once a supported configuration is ready, routine sessions start with one action. That preparation cannot become recurring setup or disguise periodic intervention during the 12-hour session.

The app handles utterance boundaries, language direction, input/output coordination, and internal connection renewal. Corrections, language changes, pause, and end remain available when wanted; they are not required to keep an otherwise healthy conversation running.

## No unexplained automatic stop

Within app-controlled behavior, an active session may end because the user explicitly stops/ends it or because its **predefined word-inactivity timeout** expires. Noise, quiet audio, a provider session limit, network transition, routine screen navigation, ordinary screen lock/backgrounding on a supported platform, or a transient processing failure must not independently end the logical session.

Twelve hours is an endurance requirement, not a maximum session length or a new automatic cutoff. A conversation still meeting the word-activity rule must not be ended merely because it reaches twelve hours. No "Are you still there?" prompt is an acceptable routine renewal mechanism.

## Timeout based on words

Define the inactivity duration and qualifying-word policy before the session begins. The duration remains undecided. Sound level, energy, voice-activity detection, or a noisy room alone cannot keep the session alive or terminate it.

Proposed operational rule: measure elapsed time from the last fresh recognized human conversation word, or session start before the first such word. Avoid counting duplicate/replayed recognition events, Trio's own synthesized speech, and identified song lyrics as new conversational activity. Validate this across the supported languages without assuming every writing system uses spaces.

If recognition is unavailable, distinguish unknown word activity from confirmed absence of words. Do not declare user inactivity merely because a recognizer, model, or connection failed. The exact handling of uncertain/provisional words and timeout accounting during recovery needs a defined, tested contract.

## Degradation must preserve the situation's purpose

Keep the logical session active through recoverable faults; recover automatically using available, permitted, evaluated capabilities. Show actual capture, processing, translation, and output state. Never display "working" or "delivered" when input was lost or a participant received nothing.

Graceful means assessing the consequence for each participant. Text may be a useful fallback for a passenger who can read. Text alone does not preserve the driver-listening outcome. A microphone animation does not substitute for recognized speech. Muted TTS during music is a deliberate output policy, not session termination; the driver receives no translated speech until music is paused.

Do not silently discard undelivered content, switch private headset speech to a public speaker, change online/offline privacy behavior, or replay a long backlog after recovery. Define bounded processing, explicit gap handling, and preconfigured safe fallback choices. Detailed recovery mechanisms are proposals until evaluated.

## Participant words never become app status

Text areas reserved for participant input, transcripts, translations, captions, or conversation messages contain only participant-derived content. Never insert "One moment", "Listening", "Reconnecting", "No speech detected", or other app-authored copy there, even temporarily or with an icon, color, or app label. Put status, errors, and guidance in a separate app-status/control area outside the participant text area.

During waiting or recovery, preserve valid content where appropriate or leave missing content empty. Do not overwrite words with a status sentence, append one to a translation, or create a fake conversation turn. App text must also remain separate in accessible reading, copying, history, translation context, and conversation playback. Requested explanations and suggested replies need a separate assistant area; they are not words the person has already said.

This is an origin and placement rule. If a participant actually says "one moment", it is valid participant content and must remain eligible for normal transcription and translation. FR-020 defines acceptance cases.

## Physical and platform boundaries

The app cannot continue capture through loss of device power, hardware failure, revoked microphone permission, or an OS that terminates its process. These are externally imposed limitations that must be exposed and verified, never represented as a supported uninterrupted experience. A platform/configuration that routinely stops unattended sessions does not meet the promise and must be fixed or excluded from supported coverage.

Define power/battery conditions for the 12-hour acceptance test and publish real measured limitations. An orderly shutdown that avoids a crash still fails the uninterrupted-session requirement if Trio chose to stop unexpectedly.

## Release consequence

These are requirements, not claims of completed implementation. A release claiming these situations must demonstrate one-action operation, full-duration endurance, word-based timeout behavior, and recovery under representative faults. A manual restart workaround or a weaker automatic timeout does not pass.

Traceability: FR-017 through FR-020, QR-012/QR-013, and [validation and acceptance](delivery/validation-and-acceptance.md).

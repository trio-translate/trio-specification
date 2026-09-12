# COND-001: Music is playing

Status: Draft
Applies to: Any supported situation, including SIT-014; may combine with COND-002
Confirmed direction: [DEC-002](../decisions/DEC-002-car-music-and-input-feedback.md)

## Desired experience

Music can continue without Trio speaking over it. The ideal experience shows live translated song lyrics while retaining the ability to translate people talking. The product owner would accept a simpler experience with a music-note symbol and an offer to open Shazam.

The minimum TTS policy is firm: **mute all Trio TTS by default when music is present**, including conversation speech, replay, and any song/explanation speech. This policy applies to phone speakers and earphones. It does not instruct Trio to mute the music or the device's accessibility screen reader.

Conversation capture and text translation remain available under the selected capture mode. Music detection itself must not require an always-on microphone when the user has not enabled capture.

Within an active continuous session, music changes output policy rather than ending the session or forcing per-turn controls. The [word-inactivity contract](../non-negotiables.md) is separate from music/noise detection; the proposed word policy excludes identified lyrics and Trio's own speech from conversation activity.

## Music in the car

The product owner explicitly confirmed that SIT-014 has no automatic driver-TTS exception. With music playing, the passenger can read translations but the driver cannot receive translated speech. The passenger pauses music when spoken translation is needed. The UI must communicate "speech muted for music" rather than implying that the driver heard the result.

Pausing music may be a manual action in another player or on a car system. Trio is not assumed to control every source. Automatic recognition of relevant music-state changes and speech resumption must support the one-action continuous experience. An optional "Music paused — resume speech" correction can help when detection is wrong, but routine dependence on that extra action does not pass unattended acceptance.

## Product options

| Option | Experience | Standing / dependency |
| --- | --- | --- |
| Silent conversation captions | Translate participants into text; suppress TTS while music plays | Core coexistence behavior; mixed-input recognition needs evaluation |
| Music-note badge and song-identification action | Show that music is present; offer to open Shazam | User-accepted simpler direction; actual integration and availability unverified |
| Passenger-managed music pause | Pause the music at its source and resume conversation speech | Confirmed car behavior; automatic player control is not required |
| Explicit music mode | Operator can correct music-present/paused state when automatic detection is wrong | Proposed optional control; repeated required toggles do not meet continuous-use acceptance |
| Live original and translated lyrics | Separate, synchronized song text from attributed conversation turns | Aspirational; source separation, alignment, content access, and offline feasibility unresolved |
| Adjustable music policy in other contexts | A participant could deliberately choose a different speech/music balance | Future option; does not change the agreed default or the car workflow |

Do not turn these options into six launch commitments. The note/identification route is a deliberate lower-complexity fallback; live lyric translation is an independent feasibility and value question.

## Proposed state behavior

| State / transition | TTS | Capture and text | Operator feedback |
| --- | --- | --- | --- |
| No music, speech enabled | Follow selected playback preference | Follow selected capture mode | Normal speech state |
| Music known through an explicit control or supported detection | Stop current Trio TTS; suppress new and replayed TTS by default | Continue available conversation processing | Music note, text label, reason speech is muted |
| Music state uncertain | Do not claim confirmed detection; attempt automatic state recovery and expose an optional correction | Show actual capture state | Clear, correctable state; recurring required correction fails unattended acceptance |
| Music paused and speech resumed | Allow new results according to preference; do not automatically drain suppressed speech | Continue conversation | Speech state updated |
| Stop/end pressed | Stop applicable capture/output and invalidate pending speech | Apply stop/end semantics | Inactive microphone state where appropriate |

Mechanisms, detection thresholds, transition delay, brief-gap handling, and how manual versus detected state wins remain design decisions. They must work without a server for the offline car situation. Prevent repeated mute/unmute switching during pauses between songs or lyrics.

## Song identification and translated lyrics

Opening Shazam is an explicit user action, never an automatic app switch or upload. Resolve the supported launch mechanism and handling when the app, network, or identification capability is unavailable. A music badge alone must remain useful offline; no Shazam offline capability is assumed. Maintain the active session through supported external handoffs; if the platform interrupts capture, disclose the gap and recover the still-authorized session automatically. Never restart a deliberately stopped session on return.

Any lyric mode needs its own source/target language choices and labeled stream. A song in a third language does not automatically become a third conversation participant or change the two-language car configuration. Evaluate singing, instrumental passages, lyrics with simultaneous speech, and uncertain attribution. Do not silently put sung words into a person's conversation turn. How to obtain and display lyric content is unresolved; this specification does not assume a content source or license.

## Acceptance direction

Test music from the same device and a separate source, with and without vocals, silence gaps, speech over music, detection mistakes, manual state changes, and no network. Once music mode is active, no Trio TTS should escape through an alternate output or a late queued result. Existing text stays readable and participants can still submit speech/text. Verify combined noise and music separately from quiet-room conversation quality.

Traceability: FR-015, QR-011, LQ-005, [SIT-014](../situations/SIT-014-car-conversation.md), and [validation](../delivery/validation-and-acceptance.md).

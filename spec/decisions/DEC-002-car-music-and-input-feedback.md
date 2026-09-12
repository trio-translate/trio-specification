# DEC-002: Specify offline car use and reusable music/noise conditions

Status: Agreed
Date: 2026-09-12
Decision owner: Product owner

## Context and evidence

The product owner described a two-language car conversation in which the passenger operates the phone and the driver receives translations by listening without looking at the screen. They required offline operation and accepted phone mic/speaker or earphones as directions.

They also described music and noise as conditions that can mix into any situation, required muted TTS by default during music, and asked for persistent visual feedback proportional to microphone input on every screen. For music, live lyric translation alongside conversation was the ideal; a music note and an offer to launch Shazam was an acceptable simpler direction.

When asked about the conflict between muted TTS and the driver needing audio, they explicitly selected: "Yes—mute TTS; the passenger pauses music when spoken translation is needed."

## Confirmed decisions

1. Treat the passenger-operated, driver-listened, two-language car conversation as a relevant required product situation. Its full conversation experience must work offline.
2. Do not require the driver to look at or operate the phone. Phone mic/speaker and earphone-based experiences are acceptable directions; specific hardware support still needs evidence.
3. Music and noise are reusable conditions that can combine with situations and each other.
4. Music mutes all Trio TTS by default. Car mode has no automatic exception; the passenger pauses music when spoken translation is needed.
5. Show microphone reception clearly on every Trio-controlled screen, using actual input-level feedback while capturing and truthful inactive/unavailable states otherwise.
6. Keep live song translation plus conversation as an aspiration, with music indication and optional Shazam handoff as an acceptable simpler direction.

## Boundaries and consequences

These decisions do not select a first release, language inventory, device list, vendor, offline engine, recognition mechanism, or lyric source. The user's Timekettle comparison is a conditional preference, not verified competitor research.

Situation and condition documents contain additional proposed flows, state handling, and acceptance details. Agreement here does not automatically approve those mechanisms or claim implementation feasibility has been proven.

Architecture must now account for a complete offline processing path for the car situation. Muting TTS must be distinct from stopping capture. While music plays, driver translation delivery is paused; passenger text delivery can continue. Microphone animation must not imply recognition success or cause covert capture.

Affected documents: [SIT-014](../situations/SIT-014-car-conversation.md), [conditions](../conditions/README.md), [requirements](../requirements/README.md), [scope](../scope-and-roadmap.md), [architecture](../technical/architecture.md), and [validation](../delivery/validation-and-acceptance.md).

Supersedes: None. Narrows the prior open question about offline operation for this particular situation.

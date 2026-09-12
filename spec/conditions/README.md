# Conditions that combine with situations

Status: Draft

A situation defines people, roles, setting, and an outcome. A condition changes how that situation behaves. Music and noise can occur in a car, a home, a group, or solo use, and can occur together. Define each condition once and test its combinations with supported situations.

## Catalog

| ID | Condition | Confirmed direction |
| --- | --- | --- |
| COND-001 | [Music is playing](COND-001-music.md) | Mute all TTS by default; preserve conversation capability; explore a music badge, song identification, and translated lyrics |
| COND-002 | [Noise and microphone input feedback](COND-002-noise-and-input-feedback.md) | Every Trio-controlled screen shows microphone state and actual input level while capturing |

IDs remain stable. Use the [condition template](../../templates/condition.md) for additional conditions as the product owner develops the situation space.

## Describe a combination

`Situation + participant roles + selected languages + connectivity requirement + input/output route + active conditions`

Example: SIT-014 + passenger operator/driver listener + two languages + offline + phone mic/speaker + music + road noise.

The combination determines the usable experience: here, the passenger receives text while music suppresses TTS, and the driver receives no translated speech until the passenger pauses music. A moving input meter does not mean the driver received a translation.

## Proposed composition rules

- Stop/end and permission state govern whether capture is allowed. A condition must not secretly start or prolong capture.
- Microphone visibility applies regardless of situation or current screen. When capture is inactive, show its actual inactive/unavailable state.
- Music changes TTS delivery independently of speech recognition and text translation. Do not equate muted output with a stopped microphone.
- Noise does not automatically trigger music mode. Loudness alone cannot identify the sound source.
- A condition does not relax a situation's offline requirement. A network-dependent optional action can be unavailable while the offline conversation remains usable.
- Show conflicts explicitly. If a participant depends on speech and TTS is muted, that participant's translation delivery is paused; the session is not fully delivered to everyone.

The [decision record](../decisions/DEC-002-car-music-and-input-feedback.md) separates user-confirmed direction from proposed mechanisms and acceptance details.

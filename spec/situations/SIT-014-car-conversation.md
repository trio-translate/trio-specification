# SIT-014: Offline conversation between passenger and driver

Status: Draft
Scope: Required product situation; release assignment undecided
Confirmed direction: [DEC-002](../decisions/DEC-002-car-music-and-input-feedback.md)

## People, setting, and outcome

Two people in a car use two selected languages. The passenger operates the phone. The driver receives translations by listening and must not need to look at, read, or operate the phone. This is an asymmetric conversation: participation does not require identical interfaces or actions for both people.

The outcome is a useful conversation without making the driver a screen user. Offline operation is a requirement for this situation even when a connection sometimes happens to be available. This is a product constraint, not a claim that cars never have connectivity.

## Confirmed requirements

- Exactly two conversation languages are selected for this situation.
- The passenger handles setup and optional changes, corrections, and controls. One start action begins continuous use; routine exchanges do not require further passenger interaction. Translation to the driver is audible when TTS is enabled.
- The full conversation must work offline. Text-only offline support does not complete this situation.
- Phone microphone plus speaker is an acceptable setup. Earphones/earbuds are also an acceptable product direction; concrete accessories and input/output combinations need verification.
- Music mutes all Trio TTS by default, including driver-directed speech. The passenger pauses the music when spoken translation is needed, as explicitly confirmed by the product owner.
- The passenger can always find the microphone input status on every Trio-controlled screen; see [COND-002](../conditions/COND-002-noise-and-input-feedback.md).

## Proposed preparation and journey

1. Before relying on offline use, the passenger selects the two languages and checks local readiness for speech recognition, translation in both directions, and required speech output. Downloading language resources beforehand is a proposal; packaging is undecided.
2. The passenger selects and tests the actual microphone/output route. Earbuds connected for output do not automatically prove that the phone microphone remains the input.
3. The passenger starts once. Capture state, incoming sound level, offline readiness, and TTS state are visible to the passenger. The app then handles utterance boundaries and returns to listening automatically.
4. The passenger speaks naturally. Their speech is translated and spoken for the driver when music is paused and TTS is enabled.
5. For a two-way exchange, the driver speaks without touching or reading the device; the passenger reads or hears the automatically processed response. This proposed return path interprets "listen" as how the driver receives translations; automatic attribution/language routing needs validation.
6. The passenger can request repetition/correction or stop/end when desired. Recoverable audio/service interruptions must be handled automatically under [continuous recovery](../experience/recovery.md). A driver-requested pause must be possible through the passenger; automatic voice commands are not assumed.
7. If music is present, apply [COND-001](../conditions/COND-001-music.md): text processing may continue for the passenger, while spoken delivery to the driver is paused. Pause the music before resuming spoken translation.

## Offline boundary

The ready session must start after a cold app launch with no network, recognize fresh speech, translate new utterances both ways, generate required speech, correct/retry, and stop/end. Cached phrases, network-backed TTS, online account refresh, or a hidden startup/license request cannot satisfy this boundary.

If preparation or a resource is missing, explain the missing capability to the passenger before presenting the situation as ready. The extent of offline language coverage is unresolved. The user's Timekettle reference is an experience benchmark conditional on full offline language coverage, not verified evidence of any vendor's current capabilities or a Trio commitment to support every language immediately.

## Combined conditions and failure paths

| Condition | Required outcome / proposed recovery |
| --- | --- |
| Music starts | All TTS is muted by default; passenger sees why; translation text remains available |
| Music pauses | Passenger can resume spoken delivery; proposed rule: only new turns play automatically, never a backlog |
| Road, wind, ventilation, or other noise | Actual input activity remains visible; passenger can adjust placement/input or request a repeat |
| No usable microphone | Passenger sees an unavailable/denied state; text can help the passenger but does not demonstrate a working two-way car speech session |
| Earbud disconnection or input-route change | Show the actual route/state; recover a permitted preconfigured route automatically, or show unavailable output without silently switching private speech to a speaker |
| Missing local language resource | Explain which direction/capability is unavailable; do not silently switch to cloud and claim offline readiness |
| Screen lock, call, or background interruption | Follow a tested lifecycle policy; do not ask the driver to recover the session |

## Acceptance direction

Verify a fresh bidirectional exchange with all network access blocked and previously unheard utterances. The driver participant completes their role without a screen glance or touch; neither participant needs per-turn phone controls. Apply the twelve-hour endurance and word-inactivity requirements to supported car configurations. Test phone mic/speaker and each advertised earbud routing combination separately, with silence, speech, music, road noise, and combined music plus noise. Use controlled or simulated conditions to evaluate the interaction before any real-road study.

The meter alone cannot prove intelligibility. Capture, translation, music handling, and driver comprehension require their own evidence. No implementation has been verified here.

## Traceability and open decisions

Behavior: FR-013 through FR-019 and FR-004/FR-005 in [functional requirements](../requirements/functional.md). Verification proposals: QR-009 through QR-013 in [quality requirements](../requirements/quality.md). See [journey E](../experience/user-journeys.md#journey-e-passenger-operated-car-conversation).

An optional accessory that would serve the driver-listening role without occluding the driver's hearing is explored in [purpose-built hardware](../technical/hardware.md); it is a draft study with no product-owner acceptance, and the phone microphone-plus-speaker setup remains supported regardless of its outcome.

Resolve supported languages/devices/accessories, offline preparation and licensing, automatic driver speech/turn handling, playback routing, music-state detection/manual control, word-timeout duration, resource budgets, and release priority. These do not weaken the confirmed offline, driver-role, or continuous-session requirements.

# Purpose-built hardware for Trio

Status: Draft proposal; no product-owner acceptance, no vendor selection, no validated demand
Scope: Design study for the [car situation](../situations/SIT-014-car-conversation.md) and the [shared-device situation](../situations/SIT-001-shared-device-conversation.md); release assignment undecided
Sources: [non-negotiables](../non-negotiables.md), [DEC-002](../decisions/DEC-002-car-music-and-input-feedback.md), [DEC-003](../decisions/DEC-003-continuous-one-action-sessions.md), [DEC-007](../decisions/DEC-007-device-capabilities-and-product-harness.md), [COND-001](../conditions/COND-001-music.md), [COND-002](../conditions/COND-002-noise-and-input-feedback.md), [device capabilities](device-capabilities.md), [recovery](../experience/recovery.md)

This document designs hardware from first principles for Trio's agreed behavior. Every
number in it is a proposal or a `TBD` until measured on real parts. Nothing here is a
commitment to build, to a supplier, to a price, or to a release. `HW-###` identifiers are
local to this document; they are not requirements in the [requirement sets](../requirements/README.md)
and carry no coverage obligation until a decision record adopts them.

## Why hardware at all, and what would disqualify it

Trio's hard problems are not translation quality. They are honesty about what the
microphone received, a session that survives twelve unattended hours, an offline car
conversation where the driver never looks at a screen, and recovery that never pretends.
A phone alone can meet those requirements and must continue to: **phone microphone plus
speaker stays a fully supported setup** ([SIT-014](../situations/SIT-014-car-conversation.md)).

Hardware earns its place only where the phone is structurally weak:

| Trio obligation | Where a phone alone is weak | What purpose-built hardware can change |
| --- | --- | --- |
| Truthful input feedback on every screen ([COND-002](../conditions/COND-002-noise-and-input-feedback.md)) | The OS hands the app audio after undisclosed processing; the meter describes a signal nobody can characterize | Deliver an unprocessed, calibrated channel alongside the processed one, so the meter has a defined measurement point |
| Twelve hours after one action ([DEC-003](../decisions/DEC-003-continuous-one-action-sessions.md)) | Battery and thermal limits end sessions the app did not choose to end | Power the phone, govern its charge rate, and spread its heat |
| Never display "working" when input was lost | Dropped audio inside the OS/accessory stack is inferred, not observed | Sample-accurate sequence numbers make every gap provable |
| Driver listens without operating the phone ([SIT-014](../situations/SIT-014-car-conversation.md)) | A phone speaker competes with road noise; earbuds occlude a driver's hearing and steal the phone's audio route | An open-ear receiver on a link the phone never has to renegotiate |
| Music mutes all TTS ([COND-001](../conditions/COND-001-music.md)) | Music state is guessed from the room | An electrical reference of the media source gives detected state instead of uncertain state |
| Overlapping speech and attribution ([SIT-001](../situations/SIT-001-shared-device-conversation.md), [SIT-003](../situations/SIT-003-multilingual-group.md)) | One capsule cannot separate two seats; diarization claims exceed evidence | Array geometry produces measurable per-direction energy, which is evidence rather than a claim |
| Physical-fidelity verification ([device lab](../../harness/device-lab.md)) | Injected audio and acoustic audio become indistinguishable in the record | Injection is labeled in the stream and cannot be unlabeled |

The design is disqualified if it ever becomes the reason a session stops, if it makes any
agreed behavior depend on owning an accessory, or if it puts recognition, translation, or
synthesis anywhere except the phone.

## System overview

Four pieces, three of them optional to each other.

- **Trio Core** — the capture and interaction module. Six-microphone array, audio DSP, one
  action key, a hardware mute slide, a status ring, a USB-C link to the phone, and the
  radio link to the receiver. Works standing alone on a table with any USB-C power source.
- **Trio Base** — a detachable endurance power module that the Core sits on. It carries the
  battery for a twelve-hour unattended run and charges the phone. Detaching it in a hot
  parked car is the intended handling, not an accident.
- **Trio Ear** — a single open-ear receiver for the listening participant, typically the
  driver. Non-occluding by design. Charges in a pocket in the Core.
- **Mounts** — a weighted table foot and a vehicle vent/dash mount that accept the same
  Core, so [SIT-001](../situations/SIT-001-shared-device-conversation.md) and
  [SIT-014](../situations/SIT-014-car-conversation.md) share one electrical product.

The phone remains the whole system's brain. The Core is an audio front end, a power plant,
a physical control, and an honest instrument. It is deliberately not a translator.

## Requirements

### Honesty about state

#### HW-001 — Unprocessed truth channel

The Core streams a channel that has passed no noise suppression, no automatic gain, no
gating and no dynamics processing, carrying a calibration constant so a level in the
stream can be related to sound pressure at the array. Processed channels are separate.
Accept: with a known calibrated stimulus, the truth channel's reported level tracks
stimulus level monotonically across the working range, while a processed channel is
allowed to compress it. Trace: [COND-002](../conditions/COND-002-noise-and-input-feedback.md), FR-016, QR-010.

#### HW-002 — Sample-accurate gap accounting

Every audio frame carries a device timestamp and a monotonic sequence number. Any
discontinuity — buffer underrun, link stall, DSP overload, mute, power transition — is
reported as an explicit gap record with cause and sample count. The Core never conceals a
gap by inserting silence, repeating a frame, or resampling across it.
Accept: an injected link stall produces a gap record whose sample count matches the
measured interval; no test can produce lost audio without a matching record.
Trace: [non-negotiables](../non-negotiables.md) (distinguishing unknown word activity from confirmed absence), FR-019, QR-003.

#### HW-003 — Declared processing and no silent change

The Core declares which processing blocks exist, which are active, and their versions. A
profile change happens only on an explicit host request, is acknowledged with the new
declaration, and never occurs autonomously mid-session. Firmware never adapts a block's
behavior in a way the declaration does not describe.
Accept: a recorded session's declaration explains every difference measured between the
truth channel and the processed channel. Trace: [device capabilities](device-capabilities.md), QR-014.

#### HW-004 — Route and link identity

The Core reports the actual identity and state of every input and output path: which
microphones are live, whether the receiver link is connected, its measured latency, its
battery, and whether output is currently reaching a transducer. Output selection is never
inferred from input selection or the reverse.
Accept: with the receiver powered off, the Core reports output unavailable while input
stays active; Trio can show that state without guessing. Trace: [COND-002](../conditions/COND-002-noise-and-input-feedback.md), [recovery](../experience/recovery.md), FR-019.

#### HW-005 — Hardware mute that cannot be misreported

A mechanical slide cuts microphone power on the board and is visible and findable by
touch. The same physical position drives the mute state in the control stream and gates
the level indication at its source, so no firmware or app state can display capture while
the slide is closed.
Accept: with the slide closed, the level indication is inert, the reported state is
`muted_hardware`, and no audio energy appears on any channel. Trace: [security and privacy](security-and-privacy.md), FR-016.

#### HW-006 — Per-microphone health and clipping

The Core reports per-capsule presence, coherence against its neighbors, and clipping
counts per interval. A failed or occluded capsule is reported, never averaged into
apparent normality.
Accept: physically blocking one capsule produces a health report identifying it, and the
array degrades to a declared smaller geometry rather than pretending to be intact.
Trace: [COND-002](../conditions/COND-002-noise-and-input-feedback.md), QR-014.

### Capture chain

#### HW-007 — Array and acoustic performance

Proposed: six matched MEMS capsules, acoustic overload point at least 130 dBSPL so door
slams and road noise do not clip, signal-to-noise ratio at least 68 dB(A), inter-capsule
matching within ±1 dB and ±3°, 48 kHz at 24 bits, with wind and pop protection sized for a
vehicle vent's airflow. Capsules are mechanically decoupled from the enclosure, the mount,
and the phone's heat path. Targets are proposals pending measurement in a real cabin.
Accept: measured speech intelligibility at the seated passenger and driver positions with
road noise at a declared level, against a phone-only baseline recorded at the same time.
Trace: [SIT-014](../situations/SIT-014-car-conversation.md), QR-002.

#### HW-008 — No gating and no session-affecting detection

The Core never gates, ducks, or drops audio on a voice-activity or level decision. It may
compute activity metadata and report it, clearly labeled as metadata. Nothing in the Core
participates in the [word-inactivity contract](../non-negotiables.md).
Accept: continuous quiet audio is delivered continuously; long silence produces no
suppressed interval and no change in frame cadence. Trace: [non-negotiables](../non-negotiables.md), FR-018.

#### HW-009 — Echo control with a real reference

Acoustic echo cancellation uses the electrical output signal as its reference, not an
estimate from the array. The reference is available to the host so a self-translation loop
can be diagnosed rather than guessed at.
Accept: Trio's own synthesized speech played through the Core does not appear as
recognized conversation words in a physical-device run. Trace: [SIT-001](../situations/SIT-001-shared-device-conversation.md) (playback captured by the microphone), [non-negotiables](../non-negotiables.md).

#### HW-010 — Spatial separation as evidence, not as a claim

The Core produces fixed, declared beams — in the vehicle mount, one toward each front seat
— and reports per-beam energy and inter-beam ratio. Trio may use these as attribution
evidence with an honest confidence; the Core never asserts speaker identity.
Accept: with a known talker in one seat, the reported ratio separates seats by a
documented margin; with simultaneous talkers, the report shows contention instead of
choosing. Trace: [SIT-001](../situations/SIT-001-shared-device-conversation.md), [SIT-003](../situations/SIT-003-multilingual-group.md), LQ-005.

#### HW-011 — Music reference and honest music state

Two independent paths inform music state: an electrical reference — a line input from a
vehicle head unit, or the Core acting as the phone's audio sink so Trio's own media route
is known — and an acoustic classifier on the array. The Core reports which path produced
the state and a confidence, and reports `uncertain` when they disagree.
Accept: music from a separate source is reported with its path identified; gaps between
tracks do not produce state chatter within a declared hold interval; with no reference
available the Core reports acoustic-only confidence rather than claiming detection.
Trace: [COND-001](../conditions/COND-001-music.md), FR-015, QR-011.

### Output and the listening role

#### HW-012 — Open-ear receiver

Trio Ear does not occlude the ear canal. The driver keeps ambient hearing of traffic,
sirens, and the passenger's actual voice. Proposed: single unit, wearable on either ear,
under 9 g, IP54, with a maximum output ceiling and a physical volume control.
Accept: a measured ambient attenuation below a declared threshold while worn, and
intelligible delivery at a declared cabin noise level. Trace: [SIT-014](../situations/SIT-014-car-conversation.md).

#### HW-013 — Output is never silently substituted

If the receiver link is lost, the Core reports output unavailable. It does not move speech
to its own loudspeaker, and the loudspeaker is used only for a route the operator
preconfigured for that situation.
Accept: powering the receiver off mid-utterance produces an unavailable state and silence,
never a public playback of private speech. Trace: [recovery](../experience/recovery.md), [security and privacy](security-and-privacy.md), FR-019.

#### HW-014 — Delivery confirmed at the transducer

The receiver carries a feedback microphone used only to confirm that its own transducer
produced the intended signal, reported as a delivery confirmation per utterance. It is not
a capture path and cannot be routed to recognition.
Accept: a muted or failed transducer produces a non-delivery report; the app can then
avoid showing a delivered state. Trace: [non-negotiables](../non-negotiables.md) (never display delivered when a participant received nothing), [device lab](../../harness/device-lab.md) `observe_output`.

#### HW-015 — The music mute cannot be escaped

When the host declares TTS suppressed, the Core drops output at the mixer, clears any
queued samples, and reports the suppression. No late-arriving or alternate-path audio can
reach the receiver or the loudspeaker while suppression holds.
Accept: with suppression active, a deliberately queued late result produces no acoustic
output on any path, and no backlog drains when suppression clears.
Trace: [COND-001](../conditions/COND-001-music.md), FR-015, QR-011.

### Power, thermal, and endurance

#### HW-016 — Twelve-hour system budget

The system powers the phone and itself for a twelve-hour session with margin. Proposed
budget, all to be measured: phone at 2.5 W average with the screen dim and continuous
recognition (30 Wh), Core at 0.9 W (11 Wh), conversion losses 15%, giving roughly 48 Wh
required and a 60 Wh Base. That keeps the pack under the 100 Wh air-travel threshold.
Accept: a measured twelve-hour run from a full Base, with the phone above a declared
reserve at the end and no charge-related interruption. Trace: [non-negotiables](../non-negotiables.md), FR-017, QR-012.

#### HW-017 — Charge governance and thermal headroom

The cradle is an aluminum heat spreader for the phone, thermally isolated from the
microphone array. Charge current is governed by phone and cradle temperature, preferring a
slow trickle over a fast charge that pushes the phone into throttling. Thermal state is
reported so a run's evidence can show why a rate changed.
Accept: across a twelve-hour run at a declared ambient, the phone stays below its
throttling behavior and no thermal event reduces recognition throughput.
Trace: QR-004, QR-012.

#### HW-018 — Power transitions never interrupt capture

Attaching or detaching the Base, plugging or unplugging external power, and a vehicle's
ignition cycle are ride-through events. An internal buffer holds the Core and the link
through the transition, and the transition is reported as an event, not as a gap.
Accept: detaching the Base mid-session produces no audio gap record and no route change;
losing all power produces an explicit, truthful end rather than a silent stop.
Trace: [non-negotiables](../non-negotiables.md) (physical and platform boundaries), FR-019.

#### HW-019 — Battery chemistry chosen for parked cars

Proposed: LiFePO4 cells in the Base, accepting roughly twice the volume and mass of a
lithium-ion pack of equal energy, for thermal tolerance and cycle life in a vehicle. Charging is
locked out above a declared cell temperature and the state is reported rather than
silently degraded. The Base is detachable precisely so it need not live in a hot cabin.
Accept: declared safe operating and storage envelopes, with lockout behavior observable in
the reported state. Open: whether the volume and mass penalty is acceptable, or whether a
lithium-ion Base plus an explicit handling instruction is the better product.

#### HW-020 — Receiver endurance and charge in place

Proposed: the receiver runs a full twelve-hour conversation, helped by speech being
intermittent, and charges in a pocket in the Core between sessions. Its battery state is
reported early enough for the operator to act before delivery is at risk.
Accept: a twelve-hour session with a representative speech duty cycle ends with the
receiver still delivering, and a low-battery state is reported at a declared margin.

### Controls and indication

#### HW-021 — One action key

A single large concave key starts and stops the session. It is findable without looking,
guarded against a sleeve or a cup, confirmed by a distinct haptic, and is the only control
needed for an ordinary session. No per-turn control exists anywhere on the hardware.
Accept: a blindfolded operator finds and presses it reliably; twelve-hour runs record zero
hardware interactions after start. Trace: [DEC-003](../decisions/DEC-003-continuous-one-action-sessions.md), FR-017, [recovery](../experience/recovery.md) (touch counting).

#### HW-022 — Stop is immediate

Stop takes effect on press, not on release, and not after a hold. Capture and output stop
within the [QR-001](../requirements/quality.md#qr-001--stop-responsiveness) budget, pending
output is invalidated, and the state is visible on the device itself.
Accept: measured stop-to-silence and stop-to-capture-off intervals on a physical device.

#### HW-023 — Status indication carries no participant content

The light ring and any device-side indication show session and device state only. The
hardware has no text display and renders no transcript, translation, or participant words.
Accept: no device state can present participant-derived content. Trace: [DEC-004](../decisions/DEC-004-separate-app-text-from-participant-content.md), FR-020.

#### HW-024 — Level indication is wired to the truth channel

The device's level indication is driven by the same unprocessed channel Trio's on-screen
meter uses, so the two cannot disagree. Distinct states exist for stopped, paused,
hardware-muted, unavailable, and active-but-quiet — a flat indication never means all of
them.
Accept: device indication and app meter agree under silence, speech, noise, clipping,
route change, and mute. Trace: [COND-002](../conditions/COND-002-noise-and-input-feedback.md), FR-016, QR-010.

#### HW-025 — Optional listener-side control (proposal only)

A single tactile button on the receiver could request a repeat or pause spoken delivery
without the driver touching or reading the phone. This is a proposal: the agreed situation
says the driver receives translations and that a driver-requested pause goes through the
passenger. It needs product-owner acceptance before it is designed in, and it must never
become a required per-turn action. Open question, not a commitment.

### Accessibility

#### HW-026 — Tactile, audible, and haptic operation

Every control is distinguishable by shape and position without sight; start, stop, and
mute each have a distinct haptic signature; an optional confirmation tone is available.
Nothing requires reading the device. Trace: [accessibility and localization](../experience/accessibility-and-localization.md), QR-007.

#### HW-027 — Reduced motion, contrast, and appearance

Indication states are distinguishable without relying on color alone, meet a declared
contrast criterion in a bright cabin and at night, dim with ambient light, follow the
phone's Light/Dark/Auto resolution, and offer a stepped, non-animated level representation
under reduced motion. Trace: [DEC-005](../decisions/DEC-005-support-light-dark-and-auto.md), [COND-002](../conditions/COND-002-noise-and-input-feedback.md), QR-007.

#### HW-028 — Symmetry of seating and handedness

The receiver is wearable on either ear. The vehicle mount serves left- and right-hand-drive
cabins, and the beam layout is configured for the actual seating, not assumed.
Accept: both cabin layouts verified separately; an unconfigured layout is reported as
unconfigured rather than defaulting silently.

### Link and control protocol

#### HW-029 — Wired primary link

USB-C, class-compliant audio for capture and playback, plus a documented control channel.
Wired avoids wireless codec limits, pairing loss, and route contention on the phone. The
Core is the power source while remaining the USB data device, which is a legitimate
USB-C power-delivery role combination that must be verified on each target phone.
Open and material: how many input channels the target phone actually exposes for a
class-compliant device. If only two are available, the fallback is fixed — channel 0 is
the truth channel, channel 1 is the processed channel — and per-beam streams move into the
control channel as metadata. Trace: [device capabilities](device-capabilities.md), QR-014.

#### HW-030 — Capability record

The control channel exposes a record in the shape [device capabilities](device-capabilities.md)
defines: stable capability identifiers, firmware and DSP versions, hardware model, route
and resource state, and readiness as `unknown`, `unavailable`, `preparation_required`,
`ready`, or `temporarily_unavailable`, each with a reason and a safe next action. Unknown
fails closed. Probing never starts capture. Trace: [DEC-007](../decisions/DEC-007-device-capabilities-and-product-harness.md), FR-024, QR-014.

#### HW-031 — Monotonic clock

A device clock that never steps backward, with a documented drift bound and a host
correlation procedure, timestamps every frame, event, and report. All evidence in a run is
orderable against it. Trace: [device lab](../../harness/device-lab.md), QR-015.

#### HW-032 — Updates only at idle, signed, reversible

Firmware updates are signed, applied only when no session is active, never during a
session, and reversible to the previous version. A pending update never changes behavior
before it is applied. Trace: [device capabilities](device-capabilities.md) (hold updates until idle, allow rollback).

#### HW-033 — The radio does only one job

The only radio is the low-latency link to the receiver: encrypted, paired physically in
the charge pocket, and disabled by a physical switch. Proposed latency budget: 45 ms
end-to-end from the phone's synthesized audio to the receiver's transducer, to be measured.
There is no Wi-Fi, no cellular, and no general-purpose wireless audio profile.

### Privacy and security

#### HW-034 — No network, no cloud, no account

The hardware has no internet path, no vendor service, no companion app, no telemetry
upload, and no account. It cannot weaken Trio's declared offline contract because it has
nowhere to send anything. Trace: [security and privacy](security-and-privacy.md), [SIT-014](../situations/SIT-014-car-conversation.md) offline boundary.

#### HW-035 — No audio retention

Audio exists only in a bounded RAM buffer sized to the processing pipeline. There is no
flash storage of audio, no wear-leveled remnant, and the buffer is cleared on stop and on
mute. Accept: a powered-down and re-powered unit yields no prior audio by any exposed
interface. Trace: [security and privacy](security-and-privacy.md).

#### HW-036 — Physical switches outrank software

Microphone mute and radio disable are physical, cut power at the source, and are visible
in their state. No host command can override them. Trace: [security and privacy](security-and-privacy.md).

#### HW-037 — Identity and attestation

Each unit reports a stable hardware identifier and a firmware measurement suitable for an
evidence manifest, so a recorded run can name exactly what produced it. Identifiers are
device identity, not participant identity, and never accompany conversation content.
Trace: [device lab](../../harness/device-lab.md) `collect_cleanup`, QR-015.

### Verification support

The [device lab](../../harness/device-lab.md) defines the operations a test rig needs.
This hardware implements them natively rather than leaving them to be improvised.

#### HW-038 — Injection is indelibly labeled

A test mode accepts digitally injected audio in place of the array. Injected frames are
flagged in the stream and the flag cannot be cleared downstream, so integration evidence
can never be mistaken for acoustic evidence. Test mode drives a distinct indication that
cannot be disabled. Trace: [device lab](../../harness/device-lab.md) `supply_audio`.

#### HW-039 — Observer tap

A separate tap exposes exactly what was sent to the receiver and to the loudspeaker,
independent of the transducer-confirmation path, for recording as the observer channel.
Trace: [device lab](../../harness/device-lab.md) `observe_output`.

#### HW-040 — Bounded fault injection

Test mode can force a route loss, a capsule failure, a link stall, or a power transition
for a requested interval, and reports the actual interval achieved rather than the one
requested. Faults self-clear when test mode ends. Trace: [device lab](../../harness/device-lab.md) `inject_fault`.

#### HW-041 — Synchronization marker

A marker output lets video and separate audio recordings be aligned to the device clock
without relying on a clapper or on software timestamps alone. Trace: [device lab](../../harness/device-lab.md) `record`.

### Boundaries

#### HW-042 — No recognition, translation, or synthesis on the accessory

The Core performs acoustic processing only. It runs no speech recognition, no translation,
no language identification, and no speech synthesis, and it carries no model assets. This
is a hard boundary: the app's on-device recognition path is fixed by
[its offline language boundary decision](https://github.com/flyrev/Trio-Ambient-Translate/blob/main/docs/ADR-2026-09-13-offline-language-boundary.md),
and an accessory-side engine would be an unauthorized alternate path, not an optimization.

#### HW-043 — No wake word and no voice control

The hardware listens only when a session is running, and nothing it hears changes its own
behavior. Voice commands are not assumed anywhere in the agreed situations, and a wake word
would require a classification path that contradicts honest capture states.

#### HW-044 — The accessory is never required

No agreed Trio behavior may depend on owning this hardware. Every situation must remain
completable with phone microphone and speaker, and the app must never present an
accessory-only capability as a general product promise. Trace: [SIT-014](../situations/SIT-014-car-conversation.md), [scope and roadmap](../scope-and-roadmap.md).

#### HW-045 — Serviceable and repairable

Standard fasteners, a user-replaceable Base pack, replaceable ear cushions and mount pads,
published part numbers, and firmware recoverable over USB without a service account.

#### HW-046 — Mount safety and market legality

Vehicle mounting must respect airbag deployment zones, driver sightlines, and local
mounting law, and the mount must fail safe under vibration and heat. Separately, wearing
any receiver while driving is restricted or prohibited in some jurisdictions. Market
legality is a gate on shipping the driver-receiver configuration, resolved per market with
documented sources, not an assumption. Open question with product consequences.

## Physical design sketch

Proposed and unvalidated.

| Element | Proposal | Reason |
| --- | --- | --- |
| Core | ~110 mm disc, 30 mm tall, ~180 g, recycled aluminum shell, acoustically transparent fabric over the mic ring | Reads as an instrument, not a gadget; metal spreads phone heat |
| Cradle | 60° phone rest with a floating USB-C connector and a magnetic alignment ring, retention by magnets, charging by cable | Magnetic wireless charging wastes energy as heat exactly where heat is the enemy |
| Base | ~500–650 g of cells, clips under the Core, detaches without tools | Weight anchors a table unit; detachment is the answer to a hot parked car |
| Table foot | Weighted, silicone-decoupled ring | Isolates the array from surface-borne knocks and vibration |
| Vehicle mount | Vent and adhesive dash variants accepting the same Core | One electrical product serves both agreed situations |
| Receiver | Open-ear hook, under 9 g, either ear, magnetic charge pocket in the Core | Does not block the driver's hearing; pocket pairing avoids wireless pairing flows |
| Controls | Action key, mute slide, radio disable switch, volume wheel | Every safety-relevant state is mechanical and visible |

Indicative build cost, unvalidated: Core around $42, Base around $28, Receiver around $19.
Retail pricing, bundling, and whether anyone will pay are commercial questions for
[business model](../business/business-model.md) and [commercialization](../business/commercialization.md).
This document establishes no price and no demand.

## Failure behavior

| Event | What the hardware does | What it reports | What Trio can then do honestly |
| --- | --- | --- | --- |
| Capsule fails or is occluded | Degrades to a declared smaller geometry | Per-capsule health, new geometry | Keep the session, show reduced capability truthfully |
| Receiver link lost | Stops output; never reroutes | Output unavailable, last delivery confirmed | Show output unavailable; no public playback of private speech |
| Receiver battery exhausted | Stops output | Low-battery warning ahead of the declared margin | Warn the operator before delivery is at risk |
| Base detached or external power lost | Rides through on the internal buffer | Power transition event, remaining energy | Continue the session; show remaining endurance |
| All power lost | Stops | Nothing; the last frames are already timestamped | Report an externally imposed end, never a chosen stop |
| USB link stalls | Preserves frame numbering across the stall | Gap record with cause and sample count | Disclose the gap; never count it as confirmed silence |
| Thermal limit reached | Reduces charge rate before anything else | Thermal state and the reason for the rate change | Keep running; explain a slower charge if it matters |
| Hardware mute engaged | Cuts capsule power | `muted_hardware` | Show muted, never a flat meter that could mean anything |
| Music reference disagrees with classifier | Neither state wins silently | `uncertain` with both inputs | Offer the correction [COND-001](../conditions/COND-001-music.md) allows, without depending on it |

## How this would be verified

Nothing above is evidence. The verification programme that would qualify it:

1. **Acoustic characterization** of the array against a phone-only baseline, recorded
   simultaneously, in a quiet room and in a stationary cabin with declared noise.
2. **Truthfulness tests**: device indication, app meter, and the actual audio resources
   agreed across silence, speech, noise, clipping, mute, route loss, and test mode.
3. **Gap provability**: injected stalls and power transitions, checking that every lost
   sample has a matching record and that no record exists without loss.
4. **Twelve-hour endurance** with one start action, measuring phone charge, thermal state,
   recognition throughput, and every hardware interaction after start, which must be zero.
5. **Music coexistence** from the same device and a separate source, with and without
   vocals, verifying that no audio escapes suppression by any path.
6. **Driver-role completion** in a stationary cabin: the listening participant completes
   their role with no screen glance and no touch, with the received audio independently
   recorded rather than inferred from an icon.
7. **Privacy inspection**: teardown-level confirmation that mute cuts power, that no
   network path exists, and that no audio survives power cycling.

Simulated audio, a bench loopback, or a short recording qualifies none of this
([device lab](../../harness/device-lab.md), [validation and acceptance](../delivery/validation-and-acceptance.md)).

## Open decisions

1. Does Trio want to be in the hardware business at all? This study argues the accessory is
   defensible only as an optional instrument, never as a requirement — and an optional
   accessory is a hard business.
2. Phone input-channel count over a class-compliant link, which decides whether per-beam
   audio is real or metadata.
3. Base chemistry: thermal tolerance against size and weight.
4. Whether the listener-side button in HW-025 belongs in the product at all.
5. Market legality of a driver-worn receiver, per market.
6. Whether the vehicle mount ships as a supported configuration or as a documented
   limitation, given mounting law and airbag zones.
7. Cost, price, and whether the endurance and honesty benefits are worth paying for — none
   of which this document establishes.

Any adoption needs its own decision record under [the decision log](../decisions/README.md),
and would then need requirement IDs, coverage entries, and acceptance evidence like
anything else.

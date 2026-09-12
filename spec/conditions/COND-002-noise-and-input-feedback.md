# COND-002: Noise and microphone input feedback

Status: Draft
Applies to: Every supported situation and every Trio-controlled screen
Confirmed direction: [DEC-002](../decisions/DEC-002-car-music-and-input-feedback.md)

## Product-owner requirement

Always show a clear indication of what the microphone is receiving, such as an animation proportional to incoming volume. This gives the phone operator immediate information when there is a lot of noise. It is a general interface requirement, not a feature that appears only after a noise detector triggers.

## Proposed presentation contract

- Keep a compact microphone status component on every Trio-controlled screen, including setup, conversation, settings, help, and app-owned dialogs. Navigation must not hide active capture.
- While capturing, drive its changing level from the actual selected microphone stream. Do not use a decorative looping animation, synthesized output level, or simulated activity.
- Show explicit states for stopped, paused, permission denied, unavailable/disconnected, and active-but-quiet. A flat meter must not ambiguously mean all of them.
- Identify the actual input route in the component or an immediately accessible detail. A headset output selection is not evidence of headset input.
- Proposed measurement point: the selected input as received by Trio before Trio's optional noise suppression, with any device processing acknowledged. Do not present it as calibrated environmental loudness or absolute decibels without measurement support.
- Use an understandable relative scale so louder/quieter input changes are visible without rapidly rescaling everything to the same apparent level. Numeric thresholds, sampling, and smoothing remain design choices.
- Complement motion with readable state labels and a reduced-motion representation. Screen-reader feedback should announce meaningful state changes, not every level update.

The component stays visible when capture is off, but does not activate or retain the microphone simply to populate the meter. Every screen means every screen Trio controls; external apps, OS permission panels, the lock screen, and system UI need documented lifecycle behavior rather than a false promise that Trio can draw its indicator there.

## What the meter tells someone

It shows how much sound the selected microphone stream is receiving. A strong signal may be a person, wind, music, road noise, or several sounds together. It does not prove that words were recognized, the correct speaker was isolated, or the translation is accurate. Keep those states distinguishable.

The product owner's approach is to make input understandable so people can judge and adjust for themselves. Do not make intrusive noise warnings or automatic capture shutdown a baseline requirement. Optional hints about clipping, input placement, or an unavailable route can be explored after testing.

The input meter must never be the inactivity-timer source. [Continuous sessions](../non-negotiables.md) use detected conversation words; noise alone does not renew activity, and a quiet signal alone cannot stop the session. Displayed input activity, word recognition, and observer health remain distinct even when processing fails.

## Situation-specific response

In SIT-014, the passenger reads this feedback and adjusts the device/input or asks for a repeat. The driver must not need to inspect the meter. If music is also present, apply its separate TTS policy; loud noise alone does not justify classifying the environment as music.

## Acceptance direction

Navigate all app screens while capturing, paused, stopped, denied, and disconnected; verify the indicator and the actual audio resources agree. Use controlled silence, speech at different levels, steady road noise, wind, clipping, music, and route changes. Confirm that local speaker playback is not falsely displayed as microphone input unless the microphone actually picks it up. Test no-network operation, enlarged text, reduced motion, and screen reading.

Response-time and visual-scale budgets are TBD. Record whether a person can notice a meaningful input change without suggesting that noticing noise proves conversation comprehension.

Traceability: FR-016, QR-010, LQ-005, [interaction design](../experience/interaction-design.md), and [validation](../delivery/validation-and-acceptance.md).

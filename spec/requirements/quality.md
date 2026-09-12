# Quality requirements

Status: Draft

All entries apply to the candidate launch unless stated otherwise. Numeric proposals are discussion inputs, not measured performance or accepted service promises. Unset thresholds must be resolved before release acceptance.

The twelve-hour endurance outcome in QR-012 is user-confirmed. Other numbers remain proposals or TBD. Requirements below must be interpreted alongside [non-negotiable behavior](../non-negotiables.md).

## QR-001 — Stop responsiveness

Source: SIT-001, FR-004.

Proposed target: local capture and playback stop within **250 ms at the 95th percentile** after the stop input on each supported physical-device class, including network loss. No queued or late speech may restart without a new deliberate playback/capture action.

Measure from receipt of the input to microphone/resource shutdown and actual output cessation; verify the visible state separately. Record test count, device, OS, audio route, and outliers. Refine the timing budget with prototype evidence.

## QR-002 — Conversation latency

Source: SIT-001, FR-003.

Measure separately: capture responsiveness, end-of-turn to first readable translation, end-of-turn to final translation, and requested playback to first audible output. Report median and 95th percentile by supported language direction, device, utterance length, and network profile.

Acceptance: agreed budgets are met on the release matrix and delays show an accurate processing state with cancel available. Numeric thresholds and minimum evaluation sample sizes are TBD; this requirement cannot yet pass release acceptance.

## QR-003 — Integrity and recovery

Source: SIT-001, FR-005, FR-007.

Acceptance: interruption/retry, late results, and corrections do not produce duplicate visible turns, obsolete speech, incorrect attribution, or silent success. Fault tests cover provider timeout, connection loss, restart, and reordered responses. Document any input that can be lost and its user-visible state.

## QR-004 — Device and resource behavior

Source: SIT-001, FR-002, FR-004.

Acceptance: no capture continues after stop/end; session cleanup releases owned audio resources; calls, audio-route changes, backgrounding, lock, and resume follow the agreed platform policy. A sustained session completes within agreed battery, memory, and thermal budgets.

The required unattended endurance case is twelve hours under FR-017. Power conditions, battery/memory/thermal budgets, and the supported device matrix are TBD. Validate on physical devices, including the lowest supported device class. Ordinary lock/background behavior cannot be waived out of that device's support claim without explicitly narrowing the claim.

## QR-005 — Operational reliability

Source: FR-007 and launch trust.

Define service availability and successful-turn metrics with explicit denominators, excluded conditions, and reporting windows. Provider failures must be visible and actionable. Synthetic monitoring must exercise a non-sensitive representative translation path, not only a process-alive endpoint.

Uptime target, incident response time, and recovery objectives are TBD. Demonstrate alert delivery, rollback, and recovery before a public paid launch.

## QR-006 — Cost and usage control

Source: FR-007, FR-009 and commercial viability.

Meter service usage and enforce per-session/account limits at a trusted boundary. Separate user allowance from actual provider cost; retries and failed attempts can incur cost even if not charged to the customer.

Reserve or otherwise substantiate sufficient entitlement/resources before marking a continuous session ready. An internal quota, processing-session lease, or routine license refresh cannot unexpectedly end an accepted session. Validate an offline entitlement design separately from cloud enforcement; do not require a server round trip in an offline-ready car session.

Acceptance: simulated duplicate, long, concurrent, and repeated requests obey agreed limits; cost attribution reconciles with provider usage within an agreed tolerance; budget alerts and the cost-exhaustion path work. Per-minute/turn budget, concurrency limits, and tolerance are TBD.

## QR-007 — Accessible and localized operation

Source: SIT-001, FR-006.

Acceptance: the complete launch journey, including permission denial, correction, limit messages, and stop/end, passes the chosen accessibility and locale criteria in [accessibility and localization](../experience/accessibility-and-localization.md). Record the standard/version and tested assistive technologies before acceptance.

## QR-008 — Content-safe diagnostics

Source: FR-008 and customer trust.

Acceptance: routine events, errors, traces, crash reports, and support exports omit raw audio, source text, translations, and secrets. Use synthetic content markers in tests to verify absence. Diagnostics can still correlate a failed operation using appropriately scoped identifiers and error classes.

Any opt-in content collection for research/support needs a separate purpose, access rule, retention period, and consent path.

## QR-009 — Prove offline conversation completeness

Scope: SIT-014. Source: FR-013/FR-014.

Acceptance: cold-start with internet access blocked, using each advertised offline language direction and audio route. Process new speech, produce translations and required local TTS, correct, recover, and end. Distinguish online download/setup from offline runtime. Verify no hidden runtime dependency on account, license, voice download, telemetry, or song identification.

Measure installed resource size, startup time, recognition/translation/TTS delay, sustained thermal behavior, battery/power needs, and local quality against the selected device matrix. Every advertised route must satisfy the participant outcome; numeric budgets beyond the twelve-hour endurance target are TBD.

## QR-010 — Verify truthful persistent input feedback

Scope: Every Trio-controlled screen. Source: FR-016 and COND-002.

Acceptance: the microphone component remains present across the full app screen/dialog inventory; changes correspond to controlled input on the actual route; stopped/denied/unavailable states are distinct from active silence. No idle screen activates capture for the meter. Verify accessibility, reduced motion, offline operation, and route changes.

Input-to-display response, smoothing, scale calibration, and rendering/resource budgets are TBD. The meter must not be used as evidence of word detection or language quality.

## QR-011 — Verify music coexistence and TTS suppression

Scope: All supported situations where music occurs. Source: FR-015 and COND-001.

Acceptance: when music mode is active, Trio TTS is absent from every supported route, including late results, replay, and queued speech. Test same-device and external music, vocals and instrumental music, transitions/gaps, manual correction of state, conversation over music, combined noise, and no network.

Verify that input and text translation remain available and muting does not end the logical session. Report detection accuracy/transition delays separately from music-mode policy enforcement. Detection thresholds and minimum conversation quality under mixed music remain TBD. Song-identification handoff must not be falsely reported as uninterrupted background capture if the supported platform cannot provide it.

## QR-012 — Verify one-action twelve-hour endurance and word timeout

Status: Agreed endurance target; test details Draft. Scope: Core continuous conversation. Source: FR-017/FR-018.

Run for at least twelve actual elapsed hours on every supported device/platform class and processing profile, including offline car coverage. A prepared session has one start action and zero routine follow-up interactions. Supply representative bilingual conversation over the duration, including silent/noisy intervals shorter than the agreed word-inactivity timeout. Do not let a constant recording or output-only loop stand in for both participants completing fresh exchanges.

Record useful processing/delivery, word-activity events, capture state, reconnects, audio loops, resource trends, power conditions, interruptions, and actual required touches. Cross the twelve-hour boundary while words remain active and verify that it does not itself trigger an end. Include screen lock/backgrounding and several internal connection renewals where applicable.

Separately test the predefined timeout with noise but no qualifying words, quiet recognized speech, utterance boundary races, duplicate/interim/final events, TTS echo, music/lyrics, and suspended recognition. The timeout value and uncertain-word policy must be agreed before acceptance. Noise must neither keep a truly idle session alive nor terminate an active one.

Short accelerated timer tests complement the full-duration run; they do not replace it. Keeping an app process or animation alive is not evidence of a successful twelve-hour conversation experience.

## QR-013 — Verify recovery against participant outcomes

Scope: Every supported continuous-session profile. Source: FR-007/FR-019.

Exercise network loss/reconnect, provider connection rollover, timeout/error, local engine restart, audio-route loss/return, ordinary screen lock/backgrounding, unavailable output, and resource pressure. The logical session must not end from an internal timeout or require routine manual restart. Every fallback must have proven availability, permission, offline/privacy compatibility, and suitable quality for the recipient.

For each fault, record time to detect, time to restore each capability, input/output gaps, ordering, duplicates, resource cost, and required user actions. If recovery is impossible, expose the unavailable capability and any lost interval rather than inventing delivery or successful recovery. Recoverable-fault budgets, bounded buffer limits, and backoff parameters are TBD; retaining an indefinitely broken "active" session does not pass.

Distinguish explicit stop/end from temporary recovery so delayed work cannot restart a deliberately stopped session. Loss of power, revoked access, and OS termination are externally imposed events to test and report; routine platform behavior that violates the support promise requires a design or coverage change.

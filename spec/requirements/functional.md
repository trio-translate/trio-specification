# Functional requirements

Status: Draft

Entries are Draft unless noted. Confirmed product constraints come from [DEC-002](../decisions/DEC-002-car-music-and-input-feedback.md) and [DEC-003](../decisions/DEC-003-continuous-one-action-sessions.md); proposed mechanisms and detailed acceptance criteria remain subject to design and verification. Candidate launch refers to the proposed SIT-001 release in [scope](../scope-and-roadmap.md). An agreed outcome does not settle its release date.

## FR-001 — Start and configure a conversation

Scope: Candidate launch. Source: SIT-001.

Participants can prepare source/target language assignments and see whether the selected capabilities are supported before capture begins. A ready configuration starts with one action, using the continuous-session contract in FR-017.

Acceptance: each view identifies its language; unsupported combinations cannot silently start; changing a language affects subsequent turns without relabeling historical content. Initial setup does not begin microphone capture.

Dependencies: initial language/platform matrix and account policy.

## FR-002 — Capture speech with participant control

Scope: Candidate launch. Source: SIT-001.

One deliberate start action authorizes ongoing session capture with understandable state feedback. Utterance boundaries and return to listening are automatic; participants may cancel an utterance or pause/end the session without needing to operate controls for every turn. Permission denial has a text alternative for participants able to use it; this does not satisfy a listening-only or hands-free speech situation.

Acceptance: denial leaves typed input usable where applicable; the UI accurately indicates capture; canceled turns cannot later speak a result; ordinary speech/translation cycles need no further touch. Audio coordination follows the [interaction states](../experience/interaction-design.md) and must return to listening automatically without feeding TTS back as conversation input.

Dependencies: automatic utterance handling, device lifecycle behavior, consent presentation, echo/barge-in policy, FR-017/FR-018, QR-001.

## FR-003 — Translate and present each turn

Scope: Candidate launch. Source: SIT-001.

Each accepted turn produces linked source text and target text with participant, language, processing, and revision state. Supported speech output can be deliberately played and stopped.

Acceptance: provisional text is distinguishable from final output; a failed turn offers a clear next action; out-of-order results attach to their own turns; a result never appears as another participant's words; text remains readable without audio.

Dependencies: LQ-001 through LQ-004, playback default, QR-002, QR-003.

## FR-004 — Stop and end

Scope: Candidate launch. Source: SIT-001.

An always-reachable stop action halts local microphone capture and playback, invalidates pending speech output, and does not depend on network availability. Ending the session also prevents further input for that session.

Acceptance: stop works during capture, processing, playback, and network loss; delayed responses cannot resume speech after stop; end requires a deliberate new session before capture restarts. Verify device resources as well as the visible state.

Dependencies: QR-001, interruption policy, technical cancellation semantics. Requests already processed externally cannot be retroactively uncaptured; retention rules still apply.

## FR-005 — Correct and clarify

Scope: Candidate launch. Source: SIT-001.

A participant can correct their own source input, generate a replacement translation, and explicitly request clarification. Corrections preserve attribution and indicate that older output is superseded.

Acceptance: correcting a name or number updates the linked translation; obsolete queued speech is canceled; already delivered content is visibly marked revised; generated clarification is never presented as an unspoken statement from the other participant.

Dependencies: revision model, LQ-001, LQ-002, correction UX.

## FR-006 — Complete the journey with text

Scope: Candidate launch. Source: SIT-001.

Participants can enter text, read a translation, reply, correct, and end without microphone access or audio playback.

Acceptance: a full two-person exchange and correction succeeds with microphone permission denied and device audio unavailable. Controls remain usable under the agreed accessibility matrix.

Dependencies: supported text-language directions and accessibility criteria.

## FR-007 — Recover from interruptions

Scope: Candidate launch. Source: SIT-001.

Connection loss, provider failure, backgrounding, and device interruption produce clear per-turn and capability state while preserving the active logical session and its authorization. Recoverable faults trigger automatic recovery. Retry behavior identifies what will be reprocessed and whether it may consume allowance.

Acceptance: interruption cannot silently lose a submitted turn or report it delivered; repeated retries do not create duplicate visible turns or charge the same product operation twice. Reconnect resumes an authorized active session without another button press, while explicit user stop/end, revoked permission, or expired word-inactivity timeout prevents automatic restart. Canceled or obsolete output never replays.

Dependencies: idempotency, provider cost/retry policy, lifecycle rules, FR-018/FR-019, QR-003, QR-006, QR-013.

## FR-008 — Explain capture and control retention

Scope: Candidate launch. Source: SIT-001 and customer trust.

Before capture, participants can understand the relevant processing and retention behavior. The proposed default is no persisted conversation history; saving content would require a separate choice and deletion flow.

Acceptance: the selected retention policy is visible and matches actual app/provider behavior; ending applies that policy; analytics and routine logs do not contain raw audio or conversation text; shared-device entry does not expose a prior participant's conversation.

Dependencies: agreed retention periods, provider data terms, regional requirements, [security and privacy](../technical/security-and-privacy.md).

## FR-009 — Make usage and payment limits understandable

Scope: Candidate launch commercial requirement; exact billing flow depends on the pilot. Source: sustainable service operation.

Any paid offer explains what is counted, the allowance, price/currency, renewal behavior, and limit behavior before charging. Before offering a continuous session as ready, ensure its entitlement and resource policy can sustain the promised experience. Enforce cloud entitlements at a trusted service boundary; define a separate verified local entitlement policy for fully offline use. Stop/end controls and existing results remain accessible at any limit.

Acceptance: usage counting matches the published rule; a retry cannot duplicate product billing; cloud limits cannot be bypassed with a modified client; canceled/failed purchases do not grant an unverified paid entitlement or trigger an unexplained charge. An offline-ready session does not depend on online entitlement refresh. A hidden allowance or provider-lease cutoff during a promised session cannot be presented as satisfying FR-017; settle duration, cost, and entitlement policy before launch.

Dependencies: agreed offer, purchase channel, grace/completion policy, QR-006. Automated checkout is required only if selected for the commercial pilot.

The prior proposed hard stop at a usage boundary is not an acceptable unattended-session design under [DEC-003](../decisions/DEC-003-continuous-one-action-sessions.md). See FR-019 for honest handling when a capability is unavailable.

## FR-010 — Offer separate explanations in solo use

Scope: Future candidate. Source: SIT-002.

Users can request explanations or alternative wording clearly separated from the source translation.

Acceptance direction: original meaning remains inspectable; additions are labeled; copying does not send externally. Refine before scheduling.

## FR-011 — Support controlled group participation

Scope: Future candidate. Source: SIT-003.

Participants join with a chosen language, receive attributed and ordered turns, control local audio, and leave. Hosts have explicitly bounded room controls.

Acceptance direction: corrections reach permitted recipients; removed participants lose access; echo and duplicate capture are controlled; late joins follow the agreed history policy. Group size, timing, and authorization need a complete contract before scheduling.

## FR-012 — Support remote turn delivery

Scope: Future candidate. Source: SIT-004.

Remote participants use controlled invitations and can distinguish pending, delivered, failed, and revised turns. Reconnect preserves valid state without restoring revoked access.

Acceptance direction: two independent devices complete join, exchange, correction, interruption/reconnect, and leave/end flows; expired invitations and unauthorized access fail predictably. Transport and identity contracts remain open.

## FR-013 — Complete the car conversation offline

Status: Agreed outcome; preparation/packaging and detailed tests Draft. Scope: SIT-014, release undecided. Source: DEC-002.

Support the two selected languages through local recognition, bidirectional translation, required speech output, correction, and session control without connectivity. Show readiness per required capability before claiming the situation is available.

Acceptance: after any documented preparation, cold-launch with network access blocked and complete a fresh exchange, correction, playback, and stop/end. No stage requires a network request, online account/license renewal, or previously cached conversation output. Missing resources produce specific unavailable status. Supported language coverage is not yet chosen.

Dependencies: local language/voice resources, entitlement policy, device storage/resource budgets, QR-009.

## FR-014 — Support distinct passenger and driver roles

Status: Agreed outcome; routing details Draft. Scope: SIT-014, release undecided. Source: DEC-002 and DEC-003.

The passenger prepares and starts the session; the driver receives translations through audio without looking at or touching the phone. Ordinary exchanges then continue automatically. Phone mic/speaker and earphone configurations are acceptable directions, with an explicit supported routing matrix.

Acceptance: complete the driver role with zero screen glances/touches and a continuous exchange without per-turn passenger controls. Verify each supported actual input/output route. Music mutes driver TTS too; the passenger pauses music when speech is needed. While muted, do not count text on the passenger screen as delivery to the driver.

Dependencies: automatic recognition/language direction, selected accessory coverage, FR-013, FR-015, FR-017.

## FR-015 — Keep music and translation usable together

Status: Agreed default and fallback direction; detection and transitions Draft. Scope: Every supported situation. Source: COND-001 and DEC-002.

Mute all Trio TTS by default during music, preserving available conversation capture and text translation. Show a music indicator and the reason speech is muted. The car workflow uses the same default. Offer a deliberate song-identification handoff where supported; live lyric translation is aspirational, not baseline acceptance.

Acceptance: in active music mode, no current, queued, replayed, or alternate-route Trio TTS is emitted; participants can still submit input and read results. Offline music state handling remains usable independently of external identification. Automatic state transitions must support FR-017; routine manual toggling is not sufficient. Proposed exit rule: resume new speech after music pauses without automatically draining suppressed output. Separate song lyrics from attributed human conversation if lyric processing is implemented.

Dependencies: [music condition](../conditions/COND-001-music.md), detection/manual-state contract, offline classification/control, external handoff feasibility, QR-011, LQ-005.

## FR-016 — Show microphone reception on every screen

Status: Agreed outcome; measurement/rendering details Draft. Scope: Every Trio-controlled screen. Source: COND-002 and DEC-002.

Persistently show actual microphone state, with level-proportional feedback while capturing and explicit inactive/denied/unavailable states otherwise. Navigation, dialogs, music mode, and noise must not hide or falsify it. Never acquire the microphone just to animate the indicator.

Acceptance: verify every app-owned screen in each capture/permission state; controlled changes in input affect the meter; route changes identify the actual source. Displayed amplitude is not a recognition/translation-confidence claim. Outside Trio-controlled UI, specify the platform lifecycle rather than claiming overlay support.

Dependencies: active input measurement, reduced-motion/accessibility design, QR-010.

## FR-017 — Run continuously after one start action

Status: Agreed outcome; detailed implementation Draft. Scope: Core supported conversation experience. Source: DEC-003.

One action starts a ready session that can remain useful and unattended for twelve hours. Automatically segment speech, translate, coordinate output, resume listening, and renew internal processing connections. Optional controls remain available without becoming routine requirements.

Acceptance: with a valid prepared configuration and qualifying words within the predefined inactivity window, complete twelve real elapsed hours with one start action and zero required follow-up phone interactions. No periodic modal, per-turn press, screen wake, hidden session TTL, or twelve-hour cutoff is allowed. Record output quality and delivery throughout; an idle UI alone is insufficient.

Dependencies: FR-018/FR-019, supported foreground/background/lock behavior, local/cloud session renewal, resource and entitlement readiness, QR-012.

## FR-018 — End idle sessions using word activity

Status: Agreed word-based timeout; exact counting/timing contract Draft. Scope: All active conversation sessions. Source: DEC-003.

The only app-initiated inactivity termination is a predefined timeout based on elapsed time since qualifying detected conversation words. Start the clock at session start until the first qualifying word. Noise amplitude or VAD alone cannot reset or expire this timer.

Acceptance direction: fresh recognized participant words reset the timer; noise-only input does not; quiet but recognized words still count. Proposed exclusions include Trio TTS, duplicate recognition results, and identified music lyrics. An unavailable recognizer is an unknown-activity fault, not evidence of user inactivity. Use monotonic timing and test the boundary at the agreed duration; that duration and treatment of provisional/uncertain recognition remain TBD.

The twelve-hour target does not disable the predefined inactivity timeout. User-requested stop/end remains immediate. Detecting no words because processing failed must not cause a false automatic stop; specify and test timeout accounting through recovery before implementation acceptance.

Dependencies: local word activity during offline operation, recognition event identity/provenance, LQ-005, QR-012/QR-013.

## FR-019 — Recover without disguising lost capability

Status: Agreed outcome; fallback mechanisms Draft. Scope: All active conversation sessions. Source: DEC-003.

Maintain logical session intent and automatically recover from recoverable service, network, or route failures. Show the actual capability and delivery state. Choose only preconfigured, permitted, evaluated fallbacks that preserve the relevant participant outcome.

Acceptance: injected faults do not require a routine restart, silently discard speech, report undelivered results as delivered, or replay stale speech. Retrying and provider-session rollover preserve ordering, cancellation, attribution, and allowance semantics. A text fallback cannot be counted as successful driver delivery; input-level feedback cannot stand in for recognition. Record unrecoverable gaps, requested exceptional actions, and external platform termination honestly.

Dependencies: [non-negotiables](../non-negotiables.md), a concrete recovery matrix, bounded buffering/retry, output/privacy routing, QR-013. Keeping a session flag active while its useful capabilities are indefinitely unavailable does not pass graceful recovery acceptance.

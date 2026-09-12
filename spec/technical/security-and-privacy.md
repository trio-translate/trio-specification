# Security and privacy

Status: Draft

This is a product and engineering design brief, not a legal compliance assessment. Requirements must reflect the selected markets, users, platform, and actual processing arrangements before launch.

## Data and trust boundaries

Inventory microphone audio, source text, translations, participant/session identifiers, account/payment metadata, diagnostics, and optional saved content. Identify every transfer between device, application service, language provider, analytics, payments, and support.

Proposed default: collect only what the chosen situation needs; keep conversation content transient; do not reuse it for training, research, or marketing without a separate, informed choice and an implemented purpose-specific workflow.

One deliberate start can authorize ongoing capture within the agreed continuous session; disclose that behavior clearly without periodic consent modals that interrupt ordinary use. Explicit stop/end and revoked permission remain authoritative across retries and engine restarts. A visible input component must not start capture from a settings/help screen when the session is inactive.

For offline car operation, avoid runtime dependencies on external recognition, translation, TTS, identity refresh, diagnostics, or optional song identification. Define local resource integrity and offline entitlement validity. Connectivity returning does not authorize uploading offline conversation buffers or changing processing/privacy mode.

## Threats and proposed controls

| Threat | Design response | Verification |
| --- | --- | --- |
| Capture continues unexpectedly | Truthful state, local stop, lifecycle cleanup | Physical-device interruption and stop tests |
| Another session's content becomes visible | Enforce session/participant authorization at trusted boundaries | Cross-session negative access tests |
| Invitation leaks | Scoped, expiring invitation and membership rules if rooms are selected | Expiry, revocation, unintended participant tests |
| Provider/service credentials leak | Keep service credentials out of shipped clients and logs | Build/configuration inspection and secret scanning |
| Sensitive content enters diagnostics | Content-minimized event/error schemas | Synthetic-marker inspection of logs and exports |
| Content changes system behavior | Treat utterances as untrusted translation data; restrict capabilities | LQ-003 adversarial evaluation |
| Automated usage creates excessive cost | Input/rate/concurrency/allowance controls | Abuse and cost-limit tests |
| Deleted data persists unexpectedly | Explicit inventory, deletion lifecycle, provider/backup limitations | End-to-end deletion evidence and accurate notice |
| Long-session buffering accumulates unnecessary content | Bound recognition context, queued audio/results, diagnostics, and expiry | Twelve-hour storage/resource inspection and explicit gap behavior |
| Audio-route recovery exposes private speech | Use only permitted preconfigured output fallbacks | Headset loss/return and speaker-route tests |

## Participant-facing decisions

Before capture, people need to understand what is being processed, who may receive it, whether anything is saved, and how to stop. Decide how this works for two people sharing a screen and for someone joining a room. One participant's account preference should not be assumed to express everyone else's choice.

Optional history, summaries, exports, and support attachments each need ownership, sharing, retention, and deletion behavior. Export must be a deliberate action; the product must not send conversation content to third parties on a participant's behalf without their action.

## Launch work still required

Choose applicable markets and age audience; confirm provider processing locations and data terms; agree retention durations and access controls; specify identity/payment boundaries; perform a focused threat review; and arrange any necessary legal review of notices, consent, account rights, and commercial terms. Record evidence instead of claiming compliance from this document alone.

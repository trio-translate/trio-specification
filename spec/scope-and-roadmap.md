# Scope and roadmap

Status: Draft

No launch scope, date, platform, language set, or budget has been agreed. The following is a candidate sequence for discussion.

The user has agreed [non-negotiable continuous behavior](non-negotiables.md) and required the [offline car situation](situations/SIT-014-car-conversation.md). Their release assignment remains open; agreed outcomes must not be silently weakened while choosing the first release.

## Horizon 1: one reliable in-person conversation

Candidate lead situation: [SIT-001](situations/SIT-001-shared-device-conversation.md), two people sharing one device.

Candidate release behavior: prepare languages and understand capture, start once, converse with automatically handled utterances, read/hear translations, optionally correct or clarify, stop immediately, and end with clear retention behavior. A supported continuous session must meet the twelve-hour endurance outcome, use only the predefined word-inactivity timeout for automatic idle termination, and recover without routine intervention.

Continuous automatic operation is a confirmed requirement. Select and evaluate automatic utterance, language-direction, and audio-coordination mechanisms that meet it; mandatory per-turn presses are not an acceptable core flow.

Before committing, choose one initial audience, supported platform/device matrix, direction-specific language set, commercial pilot arrangement, and technical budget. Those choices determine the real launch boundary.

## Horizon 2: adjacent situations

Candidates include solo understanding, an in-person pair using two devices, small groups, and optional saved vocabulary or summaries. Order them by observed customer need, paid demand, and incremental quality/cost burden. These are not bundled into the first release.

## Horizon 3: broader understanding platform

Explore remote and hybrid conversations, visual text, contextual explanations, learning support, and integrations. Each requires its own complete situation, evidence, and business case.

## Scope boundaries

| Capability | Current disposition | Reason / decision needed |
| --- | --- | --- |
| Shared-device, two-person conversation | Candidate launch | A bounded end-to-end experience to validate |
| One-action continuous conversation | Required core behavior | Twelve-hour unattended endurance; internal renewal/recovery needs no routine restart |
| Word-based inactivity timeout | Required core behavior | Duration and word-event policy open; noise level is not the trigger |
| Music policy and persistent microphone feedback | Required shared behavior | All TTS muted by default during music; actual mic status on every app-owned screen |
| Text alternative and stop/recovery controls | Candidate launch | Needed for a usable conversation |
| Payment and entitlements | Commercial pilot decision | Must match the agreed paid offer before charging |
| Solo, own-device pair, group, remote | Future candidates | Require separate journeys and verification |
| Image/document translation | Future candidate | Different capture, layout, and privacy requirements |
| Offline passenger/driver conversation | Required situation; release undecided | Both selected language directions and required speech stages work without network |
| Offline translation elsewhere | Coverage undecided | Car offline requirement does not establish universal language/device coverage |
| Live translated lyrics | Aspirational | Music-note/optional identification direction is an acceptable simpler experience |
| Accounts and saved history | Undecided | Add only when continuity or payment needs justify them |
| Voice cloning, public social feed, marketplace | Outside current proposal | No initial customer need established |
| Certified or emergency interpretation | Outside current proposal | Requires a separate product and validation decision |

## Progression gates

1. **Problem gate:** a defined audience has a recurring problem and evidence that the proposed experience helps.
2. **Specification gate:** the selected situation has agreed behavior, composed conditions, word-timeout policy, recovery contract, quality budgets, and acceptance criteria.
3. **Pilot gate:** real participants complete the full journey on supported physical devices; twelve-hour continuity and relevant offline/music/noise combinations pass; privacy and operating responsibilities have owners.
4. **Commercial gate:** users understand the paid offer; service costs and payment behavior are measured.
5. **Expansion gate:** retention, quality, and support evidence justify the next situation or language.

Dates follow agreed scope and implementation capacity. Passing an earlier gate does not imply that later gates have passed.

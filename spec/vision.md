# Product vision

Status: Draft

## What we want to make possible

People should be able to understand one another and participate confidently even when they do not share a language.

Trio's working vision is to help people move from words they cannot understand to a shared understanding they can act on. Translation is the foundation. Clarifying intent, repairing misunderstandings, preserving context, and giving each person an equal voice are part of the experience.

The user-confirmed interaction ambition is to press start once and leave the phone on a table for twelve hours while conversation continues. Continuity, a predefined timeout based on detected words, and genuinely useful recovery are [non-negotiable outcomes](non-negotiables.md).

## Long-term ambition

The product owner confirmed on 2026-09-12 that Trio should use Mellom as a starting point and broaden the vision. [DEC-001](decisions/DEC-001-build-on-mellom.md) records that direction. Prior planning emphasized same-room multilingual understanding, solo use, one-to-one conversations, and groups; those are useful starting contexts, not a verified inventory of an existing implementation.

A coherent product should eventually help a person understand language on their own, have a natural conversation with one other person, and participate in a multilingual group. Speech, text, and visual material may all matter. People may share a device, use their own devices in the same room, or communicate remotely.

These are directions to explore, not promises that every mode belongs in the first release. [Scope and roadmap](scope-and-roadmap.md) is the source of release boundaries.

## The experience we are aiming for

Two people meet without a shared fluent language. Within a short setup, each understands how to speak, read or listen, correct a mistake, and stop. A mistranslation can be noticed and repaired without restarting the conversation. Neither person needs technical expertise or control of the other's account. They leave knowing what was said and what still needs clarification.

In a future group experience, slower speakers and less fluent participants can follow and contribute without being lost in the conversation. In solo use, a person can understand or prepare language while keeping their own intention and voice.

A concrete user-supplied situation is a car: the passenger operates the phone; the driver receives translations by listening; two languages work fully offline. Music and noise are shared conditions that may change the experience. With music present, all TTS is muted by default and the passenger pauses music when the driver needs translated speech. See the [situation](situations/SIT-014-car-conversation.md) and [conditions](conditions/README.md).

## Why someone might choose Trio

The differentiation hypothesis is reliable conversation with visible control and easy repair, supported by a consistent experience across situations. A translated sentence alone is easy to substitute. A product that helps people complete recurring conversations with less confusion may earn continued use and payment.

This hypothesis needs comparison with the alternatives people already use. We have not yet established demand or willingness to pay; see [assumptions](research/assumptions.md).

## Boundaries

- The product must not imply that fluent output proves accuracy or that shared understanding can be guaranteed.
- Participants retain control over capture, playback, corrections, and optional retention.
- Translation, explanation, and generated suggestions must be distinguishable.
- Support for high-stakes professional interpretation requires separate scope and evidence.
- A global ambition does not justify unsupported claims about every language, accent, device, or network condition.

## What success would look like

People complete conversations they previously avoided or struggled through. They can recover from mistakes, return for another real situation, and recommend the experience to someone with the same problem. A sufficient share will pay at a price that covers service and support costs. These outcomes are measured in [analytics and success](business/analytics-and-success.md).

## Questions for our first writing session

1. What other real situations should we specify alongside the offline car conversation?
2. Who should feel that Trio was made specifically for them at launch?
3. What should participants be able to do that existing tools make difficult?
4. How far should the long-term vision extend into learning, cultural explanation, and remote communication?
5. Which parts of the Mellom experience are essential to preserve, and which should we rethink?

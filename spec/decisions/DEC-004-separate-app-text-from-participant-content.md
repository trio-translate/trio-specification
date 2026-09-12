# DEC-004: Keep app text out of participant content

Status: Agreed
Date: 2026-09-12
Decision owner: Product owner

## Context and evidence

The product owner explicitly rejected app-generated text appearing where users' words appear. Their example was "one moment" appearing in a text field and making people wonder whether they said it. An accompanying icon does not make that acceptable.

## Decision

Reserve participant input, transcript, translation, caption, and conversation-message text areas for participant-derived content. App status, waiting messages, errors, instructions, and other app-authored copy must have a separate interface location. Icons, colors, prefixes, or temporary display do not create an exception.

## Consequences

- Waiting, reconnecting, muted audio, missing input, and failure states must not fabricate or replace a participant's words.
- Empty text fields remain empty of app-authored examples or status prose; put guidance outside their content area.
- Source/translation text remains distinct from controls, metadata, and accessibility status announcements.
- Preserve content origin in data and output paths so status text cannot enter conversation history, copying, translation context, or participant playback as a fake utterance.
- A person may actually say or type "one moment". Keep genuine participant content; enforce origin and placement, not a blacklist of phrases.

Detailed rendering and verification are defined in [interaction design](../experience/interaction-design.md#participant-content-and-app-status), FR-020 in [functional requirements](../requirements/functional.md), and [validation](../delivery/validation-and-acceptance.md).

Supersedes: None. Makes the existing attribution principle an explicit placement rule.

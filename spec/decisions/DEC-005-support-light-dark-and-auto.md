# DEC-005: Support Light, Dark, and Auto appearance

Status: Agreed mode support; detailed behavior Draft
Date: 2026-09-12
Decision owner: Product owner

## Context and decision

The product owner requested dark mode, light mode, and auto. All three appearance choices are required across the app.

## Working behavior to refine

- Light and Dark explicitly select the corresponding appearance.
- Auto follows the device/system appearance, including changes during an active session. This is the working interpretation of Auto.
- Remember the selected mode locally; appearance must work offline and must not require an account.
- Changing appearance preserves the active session, input focus, transcript, scroll position, microphone state, playback state, and word-inactivity timer.
- Verify readable content, controls, microphone feedback, and app-status separation in both resolved appearances.

The initial default is not user-selected. Auto is a proposed default; exact palette, transition styling, and fallback when a platform supplies no preference remain design choices. Auto does not require a separate Trio location or sunrise/sunset service.

Affected documents: [interaction design](../experience/interaction-design.md#appearance-modes), [accessibility](../experience/accessibility-and-localization.md), FR-021 in [functional requirements](../requirements/functional.md), and [validation](../delivery/validation-and-acceptance.md).

Supersedes: None.

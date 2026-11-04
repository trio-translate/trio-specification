# DEC-010: Light-only appearance

Status: Agreed
Date: 2026-09-30
Decision owner: Christian Neverdal, product owner

## Context and decision

Maintaining a second appearance has become a recurring source of defects and duplicated implementation and verification work. Christian decided: “We will have light mode only. Nuke absolutely everything that has to do with dark mode.”

Trio supports exactly one light appearance across all app-controlled screens, presentations and extensions. Apply it from the first render, independently of the system appearance or a legacy saved preference. There is no appearance picker, stored theme choice, automatic theme switching or alternate theme palette/assets.

## Rationale and consequences

Concentrate design, implementation and verification on one coherent experience instead of maintaining two. Do not replace deleted theme machinery with a one-case setting or build a second snapshot matrix to prove it is unsupported. A single targeted opt-out regression may verify that an incompatible system/legacy preference cannot change Trio's appearance.

Preserve contrast, Dynamic Type, RTL, assistive-technology support, readable controls and participant/app-status separation in the light presentation. Contrast backings on actual video are media presentation, not a second theme. This decision does not change audio/session behavior, translation, privacy, navigation or other accessibility requirements.

Platform-owned surfaces outside Trio's control follow their platform behavior. Historical screenshots and superseded decisions are evidence, not an active theme requirement. This specification change is not a claim of device acceptance or distribution.

Supersedes: [DEC-005](DEC-005-support-light-dark-and-auto.md).

Affected documents: [interaction design](../experience/interaction-design.md#light-only-appearance), FR-021 in [functional requirements](../requirements/functional.md), [accessibility](../experience/accessibility-and-localization.md), [data model](../technical/data-model.md), [validation](../delivery/validation-and-acceptance.md), [coverage](../../harness/coverage.json), and [certification catalog](../../certification/catalog.json).

Source and implementation: [owner decision #2160](https://github.com/trio-translate/trio-translate/issues/2160), [app PR #2161](https://github.com/trio-translate/trio-translate/pull/2161).

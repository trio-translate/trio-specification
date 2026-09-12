# Accessibility and localization

Status: Draft

## Participation requirements

- Offer text input and readable results for every candidate-launch speech action where an equivalent text path is possible.
- Label controls for assistive technology; expose capture and playback state changes without forcing repeated focus changes.
- Make start, stop, reply, and correction usable with the supported keyboard, touch, and assistive-input methods.
- Do not convey language, speaker, finality, errors, or listening state by color alone.
- Keep primary controls usable with enlarged text, zoom, long translations, and the supported device orientations.
- Allow playback control and volume adjustment through expected platform behavior. Do not require hearing to understand whether a turn succeeded.
- Keep the microphone status available on every Trio-owned screen with readable inactive/permission states and a reduced-motion alternative to level animation. Input level is distinct from recognition quality.
- Support situation-specific participation: a driver/listener cannot rely on visual fallback or the microphone meter. The passenger operates the screen; the driver must not need to inspect it.
- Test one-action continuous sessions with assistive technology and enlarged text; periodic focus-stealing prompts or repeated turn controls do not meet the core contract.

## Language coverage is a product contract

Maintain a release matrix listing UI locale, speech recognition language/dialect, translation direction, speech output availability, evaluation evidence, and known limitations. Support for text translation does not imply speech recognition, voice output, or a localized interface.

Add offline availability by recognition, each translation direction, and voice resource; include actual input/output routes and full-duration device evidence. Advertised online support cannot stand in for offline car coverage. Music suppresses Trio-generated TTS by default; it must not be implemented by disabling the device's accessibility screen reader.

Use language names people recognize; account for regional varieties, right-to-left scripts, mixed-direction text, pluralization, numbers, dates, and units. Do not silently translate proper names or convert units when that could change the meaning.

## Verification

For every supported platform, test a complete selected situation with screen reading, enlarged text, non-audio use, and relevant alternate input. Include bilingual reviewers for launch locales and native-script review of critical consent, stop, error, and payment copy.

Choose and document the applicable accessibility standard/version and concrete contrast, target-size, and interaction criteria before design sign-off. This draft makes no certification or compliance claim.

## Open decisions

Initial UI locales and language directions; launch device/platform matrix; numeric accessibility criteria; ownership of translation review; and which assistive technologies are part of supported acceptance coverage.

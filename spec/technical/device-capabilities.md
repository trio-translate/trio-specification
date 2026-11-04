# Device capabilities

Status: Agreed architectural direction; contract and test design Draft
Source: [DEC-007](../decisions/DEC-007-device-capabilities-and-product-harness.md), FR-024, QR-014

## Capability means an executable path

Trio must be able to integrate useful capabilities of each supported device through suitable platform adapters. [Purpose-built hardware](hardware.md) is a separate draft study of an optional accessory; it is a proposal, not a supported capability, and no agreed behavior may depend on it. Shared application code must permit native extensions when required. This does not require activating every sensor or choosing the newest engine without evidence. Assess customer value, implementation cost, maintenance, and the [non-negotiables](../non-negotiables.md) before adopting a capability.

| Capability family | Inventory and verify |
| --- | --- |
| Speech and language | Local recognition, translation, voices, language directions, word events, model installation, automatic direction and locale limits |
| Compute and resources | CPU/GPU/accelerator access through supported APIs, memory, storage, power, thermal state, sustained throughput |
| Audio | Actual input/output routes, sample formats, duplex behavior, echo control, Bluetooth/wired accessories, interruptions, music coexistence |
| Device interaction | Action/shortcut entry points, lifecycle/background behavior, screen/rotation, touch, keyboard, haptics, accessibility and system appearance |
| Optional future modalities | Camera/OCR, document input, spatial or other sensors only where a selected situation warrants them |

## Proposed capability record

Record a stable capability ID, adapter/version, device model, OS/build, API availability, region, language direction, resource versions/hashes, permission state, and observation time. Distinguish `unknown`, `unavailable`, `preparation_required`, `ready`, and `temporarily_unavailable`; record a reason and safe next action. Track `selected` separately from readiness and attach the evidence revision that qualifies it for the situation.

Discovery must use platform availability checks and runtime probes, not just a device-name whitelist. A model downloaded yesterday may be removed today. Recognition availability does not imply translation, TTS, offline entitlement, or a valid output route. Probe without secretly starting capture, uploading content, purchasing, or downloading large resources. Complete necessary preparation before the one-action session.

Record why an available capability is not selected: quality, privacy, energy, latency, cost, compatibility, or not relevant to this situation. A diagnostic override may exercise an eligible alternative for testing; it cannot bypass permission, data policy, or music-muted TTS. Keep technical details in diagnostics rather than routine participant flows.

## Selection and change

Select a path that satisfies all recipient outcomes and the declared offline/privacy contract. Benchmark new native paths against the current implementation using the same corpus and device conditions. Unknown capability is not proof of support. Do not switch an offline session to cloud processing or private earphones to a public speaker merely to keep a green indicator.

Recheck at preparation/start and relevant OS, app, engine, model, permission, route, and resource changes. A runtime check must not reset the logical session or word timer. Validate replacement readiness before switching; preserve cancellation and event ordering. Hold optional model updates until a suitable idle point; allow rollback of an adopted regression. An OS-imposed loss is reported truthfully and handled through [recovery](../experience/recovery.md).

## Staying current

The maintenance role reviews official platform release notes and capability documentation for each supported platform at release planning, dependency/OS updates, and incidents. Proposed regular review: monthly, assigned to a named owner when operations begin. This is a workflow definition, not a scheduled job. Record source, checked date, affected versions, third-party access, constraints, test impact, adoption decision, and next review trigger.

Initial source register, checked 2026-09-12:

- [Android SpeechRecognizer](https://developer.android.com/reference/android/speech/SpeechRecognizer): exposes recognition and on-device availability APIs, but the general API documentation warns against continuous recognition. Its presence alone cannot qualify the twelve-hour path; demonstrate the selected engine's actual behavior.
- [Apple Translation framework](https://developer.apple.com/documentation/translation): official framework entry point for investigation. The page requires JavaScript; API/version/language suitability has not been established in this repo.
- [Apple Live Translation with AirPods](https://support.apple.com/en-ie/123185): documents first-party device, setup, and on-device language requirements. It is a competitor reference, not evidence of an equivalent third-party API entitlement.

No supported-platform list is inferred from this register. Extend it for selected platforms, accessories, and local engines, including release notes and deprecation notices.

## Required verification

Exercise capability present/absent, API too old, access denied/revoked, resource absent/corrupt/removed, unsupported language direction, offline cold start, route replacement, resource pressure, and an OS/engine update. Demonstrate both selection and deliberate non-selection. Inject a false-positive probe and verify that actual startup failure produces honest recovery. Compare observed resources/routes to declared records. Run affected conversation, privacy, music, stop, navigation, and endurance regressions before renewing support claims.

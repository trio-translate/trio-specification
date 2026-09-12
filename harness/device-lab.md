# App adapters and device lab

Status: Proposed interface; no app or hardware adapter implemented here

## Runtime boundary

Keep specification/evaluation tooling independent from the eventual application stack. Register an explicit application repository, build artifact/commit, device target, processing profile, and fixture set in [runtime.json](runtime.json). Never silently operate on a nearby Mellom checkout. A configured path is not proof that it builds or that hardware is reachable.

Proposed adapter operations:

| Operation | Input | Observable output |
| --- | --- | --- |
| `probe` | Target device, requested capabilities | Reachability, actual OS/routes/resources/permissions, available versus missing capabilities |
| `build_install` | App commit, locked toolchain, device | Reproducible build ID/hash, install result and logs |
| `prepare` | Situation, languages, route, consent and fixture policy | Offline resources and entitlement readiness; no hidden capture |
| `start_stop` | Session intent and monotonic timestamp | Start action counted; capture/output state; authoritative local cancellation |
| `drive_ui` | Declared user action | Actual visible/accessibility state and resulting navigation; no direct state injection as UI evidence |
| `supply_audio` | Versioned source, role, acoustic or digital route | Delivered samples and timestamps; digital injection labeled as integration evidence |
| `observe_output` | Intended recipient, actual route | Independently captured received audio/text and gaps; speaker icon is insufficient |
| `inject_fault` | Fault scope, duration, recovery plan | Confirmed fault interval and restoration, not just requested fault |
| `record` | Authorized sources and output location | Synchronized video and separate audio tracks, dropouts, timing markers, hashes |
| `collect_cleanup` | Run ID and explicit final intent | Resources released, faults undone, fresh evidence manifest and retained failure logs |

Adapters must declare supported operations. Unknown or unsupported operations fail explicitly; they do not return empty success. Error records include operation, scope, timestamps, error class, recovery, and affected recipients. Cancellation must interrupt pending work and recording without later resurrection. A lab timeout may abort a test but cannot be reported as a valid Trio inactivity end.

## Physical fidelity

Separate app and fixture-generator devices for realistic acoustic tests. Measure microphone placement, distance, noise/music level, playback level, room/car acoustics, and echo path. Record both participants' heard output with an independent observer channel. Use a stationary car or a controlled equivalent for automated driver-role tests; a demo script does not control an actual moving vehicle.

Keep the offline product device disconnected throughout the measured interval. A remote stimulus generator must not supply Trio's recognition/translation/voices or unlock its entitlement. Prefer local fixtures for offline qualification. A software loopback is useful for repeatability but cannot qualify a physical microphone, Bluetooth route, or listening-only recipient.

## Hosts and tool availability

Verify toolchain and device reachability per run. A Windows machine can prepare platform-neutral plans; Apple build/signing/device work needs an appropriate Apple host and device setup. Simulators/emulators and mocked audio cannot replace actual sustained microphones/speakers, lock behavior, thermal measurements, or accessibility usage. Hosted builds and connected hardware are different capabilities.

Use isolated test accounts and bounded resources, keep credentials outside committed configuration, and capture exact tool versions. Add platform-specific commands only after choosing the app stack. Maintain a device inventory with owner, availability, OS update policy, power setup, supported routes, and last calibration. No fleet or cloud spending is provisioned by this definition.

# DEC-008: Adopt Swift 6 language mode and executable quality ratchets for the Trio app

Status: Agreed direction (owner request 2026-09-12); slice details Draft
Date: 2026-09-12
Decision owner: Product owner

## Context

The Trio app (repository `Trio-Ambient-Translate`, Xcode project `Translator`) compiles
in Swift 5 language mode across six targets, carries accumulated engineering debt
(unsafe concurrency escape hatches, duplicated helpers, dead and test-only production
code, source-text guardrail tests, an untested watch companion and Translation UI
extension), and has no hosted CI by decision: validation runs on the owner's Mac through
XcodeBuildMCP before every push. The product is long-lived, so the owner asked for a
Swift 6 migration combined with a proper refactor: zero warnings, zero code smells,
shorter builds, no dead code, tests for all features, reviewer agents for all
significant areas, automated screenshots with easy inspection, and development builds
whose telemetry can be retrieved and analysed automatically.

## Decision

The app repository runs the Swift 6 migration and engineering-quality program described
in its `docs/SWIFT_6_MIGRATION_PLAN.md`. Its properties are executable ratchets pinned by
the repository's BuildChecks (`Translator/BuildChecks/baselines/`) and by the compiler
(`SWIFT_TREAT_WARNINGS_AS_ERRORS` on every target once it reaches Swift 6.0), not prose:
every baseline moves only toward its target and reductions are banked in the same change.
Targets flip to Swift 6.0 one at a time, smallest first, after their strict-concurrency
corpus reaches zero; test bundles flip last; the project-level setting comes last.

Owner decisions recorded with the program:

- The foundation (program document, baselines, reviewer roster, Python tooling) lands
  from a Linux session; every Swift or Xcode slice runs on the Mac, one PR at a time.
- Periphery, SwiftLint, and SwiftFormat are adopted via Homebrew and run outside the
  Xcode build; their versions are pinned by the baselines' `captured.tools`.
- Only the WhisperKit Afrikaans file-recognition fallback is retired. Picture-in-picture,
  the direct Google REST initializers, and the Session review model family stay as
  recorded debt.
- Afrikaans file recognition moves to the authenticated gateway in the same change that
  removes WhisperKit; offline Afrikaans file recognition is unavailable afterwards; the
  Afrikaans beta toggle remains the user gate.
- Development telemetry (content-free structured events, a run manifest, opportunistic
  MetricKit payloads) is written by Debug builds and by explicitly requested internal
  TestFlight archives, with disclosure, bounded retention, and deletion shipped in the
  same slice; MetricKit payloads are never acceptance evidence.
- Evidence (screenshot sheets, pulled diagnostics) lives outside git; a pull request
  embeds the summary and names the run. The only committed evidence is the named-phone
  proof the app repository's `docs/CLOUD_GATEWAY.md` already requires for gateway changes.

## Alternatives and rationale

- Flipping every target to Swift 6.0 at once was rejected: errors would stop every
  target building until the whole corpus was fixed, forbidding small reviewable changes.
- A committed warning count parsed from build results was rejected: it drifts with the
  toolchain and can only be checked on the Mac; the compiler setting is the gate and a
  report exposes the corpus.
- Extracting the dual-compiled shared source sets into packages now was deferred: a
  package still compiles once per platform, hundreds of declarations would need `public`,
  and the ownership seams the refactoring plan wants are still moving. Reopen triggers
  are recorded in the program document.
- Adding hosted CI was rejected to keep the repository's existing decision; the Mac
  agent runs the same gates before every push and on the exact merged commit.

## Consequences

- Roughly 75 Mac pull requests over seven phases, each with a regression test that fails
  without it, an Advances/Preserves classification, routed reviewer agents, and an
  evidence lane.
- The watch companion and both extensions gain tests without a watchOS test bundle by
  moving logic into shared value types; the Translation UI extension gains a shared
  language table.
- Warnings inside remote packages are reported separately and never block; they are not
  first-party.
- "Complete" is a computed state: the program document may declare it only when every
  executable condition holds (project-level Swift 6.0, all baselines at target, empty
  dead-code and lint baselines, blocking accessibility baseline, close-out evidence).

## Evidence and affected documents

- App repository: `docs/SWIFT_6_MIGRATION_PLAN.md` (slice board, ratchet inventory,
  registers, playbook), `docs/REVIEWER_ROUTING.md`, `docs/AREA_REVIEW_CONTRACTS.md`,
  `docs/INSPECTION.md`, `Translator/BuildChecks/baselines/`.
- This repository: [verification ladder](../../harness/verification.md) Static/build stage
  now names the app repository's gates.
- Approval evidence: the product owner's request and decisions of 2026-09-12 in the
  planning session that produced the program.

Supersedes: None.
Revisit when: a Swift toolchain crashes on a flipped target, the packaging triggers fire,
or benchmark row 5 misses the build-time target.

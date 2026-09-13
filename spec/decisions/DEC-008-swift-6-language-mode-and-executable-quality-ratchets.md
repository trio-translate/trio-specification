# DEC-008: Adopt Swift 6 language mode and executable quality ratchets for the Trio app

Status: Agreed direction (owner request 2026-09-12; amended 2026-09-13 after the app programme document landed); slice details Draft
Date: 2026-09-12 (amended 2026-09-13)
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

The app repository runs the accepted engineering programme described in its
`docs/SWIFT_6_MIGRATION_PLAN.md` (foundation gates, migration sequence, local runner,
evidence rules, benchmark protocol; amended 2026-09-12), with
`docs/SWIFT_6_RATCHET_LEDGER.md` as that programme's executable companion (ratchet
inventory, census, language-mode matrix, slice board). Its properties are executable ratchets pinned by
the repository's BuildChecks (`Translator/BuildChecks/baselines/`) and by the compiler
(`SWIFT_TREAT_WARNINGS_AS_ERRORS` on every target once it reaches Swift 6.0), not prose:
every baseline moves only toward its target and reductions are banked in the same change.
Targets flip to Swift 6.0 one at a time, smallest first, after their strict-concurrency
corpus reaches zero; test bundles flip last; the project-level setting comes last.

Owner decisions recorded with the program:

- The foundation (ledger, baselines, reviewer roster, ratchet and reviewer tooling) lands
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
  MetricKit payloads) is written by Debug builds and by the programme's diagnostic
  distribution flavor (release-like optimization with a separate diagnostics capability;
  public Release excludes collection and proves it with negative controls), with
  disclosure, bounded retention, and deletion shipped in the same slice; telemetry leaves
  the device only through the user-shared bug-report archive or the runner's collection;
  MetricKit payloads are never acceptance evidence. (Amended 2026-09-13: replaces the
  earlier internal-TestFlight plist gate.)
- Evidence lives in the local runner's private store outside git
  (`~/Library/Application Support/TrioEngineering/Evidence`, capture-time expiry of seven
  days for sensitive artifacts and thirty for metadata); a pull request names the run and
  embeds only counts. The only committed evidence is the named-phone proof the app
  repository's `docs/CLOUD_GATEWAY.md` already requires for gateway changes. (Amended
  2026-09-13: replaces the earlier `~/.trio-runs` location.)
- `TrioCore` (Swift 6, products `TrioCore` and `TrioConversation`) is the package
  boundary for Core and Conversation responsibilities; the dual-compiled shared source
  sets move into it one production-used contract at a time. (Amended 2026-09-13.)
- Build time is qualified by the programme's frozen protocol: aggregate edit-to-test
  ratio ≤ 0.50 with no lane above 1.10 over counterbalanced paired runs. (Amended
  2026-09-13: replaces the earlier 80 % build-time target.)

## Alternatives and rationale

- Flipping every target to Swift 6.0 at once was rejected: errors would stop every
  target building until the whole corpus was fixed, forbidding small reviewable changes.
- A committed warning count parsed from build results was rejected: it drifts with the
  toolchain and can only be checked on the Mac; the compiler setting is the gate and a
  report exposes the corpus.
- Extracting the dual-compiled shared source sets into new packages was deferred in
  favour of the programme's `TrioCore` package, which already owns the language contract,
  capture admission policy, session startup, and deferred recovery; responsibilities move
  into it with equivalent before/after tests. Triggers are recorded in the ledger.
- Adding hosted CI was rejected to keep the repository's existing decision; the Mac
  agent runs the same gates before every push and on the exact merged commit.

## Consequences

- Roughly 75 Mac pull requests over seven phases, each with a regression test that fails
  without it, an Advances/Preserves classification, routed reviewer agents, and an
  evidence lane. Fourteen programme packets landed on `main` on 2026-09-12 (#858–#885)
  while the foundation was built: three targets at Swift 6, complete concurrency checking
  everywhere, `TrioCore`, the runner and warning registry, the evidence store; the ledger
  records them as done.
- The watch companion and both extensions gain tests without a watchOS test bundle by
  moving logic into shared value types; the Translation UI extension gains a shared
  language table.
- Warnings inside remote packages are reported separately and never block; they are not
  first-party.
- "Complete" is a computed state: the ledger may declare it only when every executable
  condition holds (project-level Swift 6.0 with warnings-as-errors on every target, all
  baselines at target, empty dead-code and lint baselines, blocking accessibility
  baseline, no untested sources, a captured type-check ceiling, the feature evidence map,
  and the programme's `quality/contract.json` `foundation_qualified`).

## Evidence and affected documents

- App repository: `docs/SWIFT_6_MIGRATION_PLAN.md` (the programme),
  `docs/SWIFT_6_RATCHET_LEDGER.md` (slice board, ratchet inventory, registers, playbook),
  `docs/REVIEWER_ROUTING.md`, `docs/AREA_REVIEW_CONTRACTS.md`,
  `docs/QUALITY_EVIDENCE_STATUS.md`, `docs/PRIVATE_DIAGNOSTICS.md`,
  `Translator/BuildChecks/baselines/`, `quality/`.
- This repository: [verification ladder](../../harness/verification.md) Static/build stage
  now names the app repository's gates.
- Approval evidence: the product owner's request and decisions of 2026-09-12 in the
  planning session that produced the program.

Supersedes: None.
Revisit when: a Swift toolchain crashes on a flipped target, a `TrioCore` move trigger
fires, or the benchmark protocol reports inconclusive or misses its ratio.

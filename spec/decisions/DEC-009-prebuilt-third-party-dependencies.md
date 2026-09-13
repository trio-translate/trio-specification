# DEC-009: Ship third-party dependencies prebuilt in every app

Status: Agreed direction (owner request 2026-09-13); slice details Draft
Date: 2026-09-13
Decision owner: Product owner

## Context

Every unit of work on the Trio app starts in a fresh worktree with its own DerivedData
(`AGENTS.md`), and each fresh checkout compiles every third-party dependency from source
before the first app build can finish. On 2026-09-13 the app workspace resolved 39 remote
packages behind three roots: Firebase (Auth and App Check, 13 packages), WhisperKit
(5 packages of its own), and the gRPC transport package `TrioGoogleSpeechStreaming`
(gRPC Swift, SwiftNIO, swift-protobuf, and their dependencies, 21 packages including
three shared with WhisperKit and two copies of BoringSSL compiled as C). Only four of
the 39 arrive as vendor binaries, and none of those is linked by a product the app uses. The programme in the app repository
(`docs/SWIFT_6_MIGRATION_PLAN.md`, DEC-008) requires at least a 50 % reduction of the
edit-to-test cycle and no clean build more than 10 % slower; compiling the same
third-party graph in every checkout works against both. The owner's rule: "we should
always include the binary versions of all our dependencies in all the apps we have, so
build times do not explode."

## Decision

Third-party code reaches every app target prebuilt, in every app the owner ships:

- A dependency is consumed as a binary framework (`.xcframework`), never compiled from
  source inside an app, extension, watch, or test target. Vendor binaries are used
  where the vendor ships them (Firebase publishes its frameworks per release); every
  other dependency is built once into a binary framework that the repository pins.
- Binaries built by us record the exact toolchain that produced them and are rebuilt
  when that toolchain, their sources, or their own resolved dependencies change; the
  local runner's preflight refuses a mismatch. Binaries built with library evolution
  survive toolchain updates and are preferred when the package supports it.
- The app's own packages are not dependencies: they stay source. A package of ours that
  exists to host a third-party stack (`TrioGoogleSpeechStreaming` hosts gRPC and
  SwiftNIO) is itself consumed prebuilt, so its stack never compiles in an app checkout.
- The rule is executable: the app repository's
  `Translator/BuildChecks/baselines/dependencies.json` banks every remote package
  reference, every product each target links, and every `Package.resolved` pin with the
  roots that pull it and the slice that removes it; a new source dependency cannot
  appear unbanked, and the count of pins that are not prebuilt ratchets to zero. Adding
  a dependency means adding its binary, with a recorded reason in the baseline's history.
- The repository commits dependency declarations, versions, and integrity checks
  (`binaryTarget(url:checksum:)`), not binary archives: artefacts are hosted outside
  git (the vendor's URL, or release assets of the app repository for a binary we
  build), each with the vendor's licence and notice files beside its declaration.
- Where no trusted vendor binary exists, the app repository's binary-first rule
  (`AGENTS.md`, 2026-09-13) makes verified compiled-output reuse through Xcode's
  compilation cache the default; building and hosting a binary ourselves needs a
  documented reason and a measured build-time impact, and a pin covered by verified
  reuse is recorded as an exception the completion condition accepts.

## Alternatives and rationale

- **Compile from source and rely on Xcode's compilation cache.** The cache is on already
  (`Base.xcconfig`) and is the only cross-checkout reuse the app allows. It is the
  rule's default where no trusted vendor binary exists, accepted only with reuse and
  invalidation verified in build logs and timings; a package-download cache alone does
  not count. Rejected as the sole answer because vendor binaries exist for Firebase.
- **A generated-project binary cache (Tuist).** It automates exactly this, but it
  replaces the hand-maintained Xcode project the app's BuildChecks pin and adds a
  generator to every checkout. Not adopted now; recorded as the fallback if hand-built
  frameworks prove unmaintainable.
- **Shared DerivedData between checkouts.** Forbidden by the app's build rules because
  concurrent builds corrupt it.
- **Vendor binaries only.** Covers Firebase; gRPC Swift and SwiftNIO ship no binaries,
  so the app builds its own.

## Consequences

- The repository stays small: only declarations and checksums are committed; a fresh
  checkout resolves the hosted artefacts by checksum.
- A toolchain update becomes a recorded slice that rebuilds any framework we built
  without library evolution; the app cannot build against a mismatched binary by
  accident.
- Clean and cold builds drop the third-party compile entirely; the programme's benchmark
  table gains a checkpoint after the conversion.
- Firebase and gRPC updates change from editing a version requirement to replacing an
  artefact and its checksum, with the same review as any dependency bump.
- The WhisperKit dependency is retired rather than prebuilt (DEC-008, slice 1.1b).

## Evidence and affected documents

- App repository: `AGENTS.md` (the rule), `docs/SWIFT_6_RATCHET_LEDGER.md` (decision
  row, ratchet inventory, the third-party dependencies section, slices 1.9a–1.9d,
  benchmark checkpoint, definition of done), `Translator/BuildChecks/baselines/dependencies.json`,
  `Translator/BuildChecks/test_third_party_dependencies.py`, `tools/dependencies.py`.
- Owner approval: the owner's instruction of 2026-09-13 in the planning session that
  produced this record.
- This repository: [DEC-008](DEC-008-swift-6-language-mode-and-executable-quality-ratchets.md)
  keeps the programme; this record adds the dependency rule to its consequences.
  [harness/verification.md](../../harness/verification.md) (Static/build) already
  names the ledger's ratchet comparisons, which now include the dependency ratchet.

Supersedes: None. Amends the build-time consequences of
[DEC-008](DEC-008-swift-6-language-mode-and-executable-quality-ratchets.md).
Revisit when: SwiftPM or Xcode ships a supported cross-checkout binary cache for package
dependencies, a vendor stops publishing binaries for a dependency the app needs, or the
hosted artefacts become a cost or availability problem the owner wants to avoid.

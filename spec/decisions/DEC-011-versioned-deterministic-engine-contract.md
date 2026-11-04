# DEC-011: Use a versioned deterministic semantic engine contract

Status: Proposed
Date: 2026-10-02
Decision owner: Product owner

## Context

Trio may have native clients on multiple platforms. Product semantics such as session/turn lifecycle, revisions, cancellation, recovery, recognition/translation state, and ordering should not drift between implementations or become coupled to one UI framework.

A shared compiled runtime could enforce reuse, but it would also add cross-platform build, FFI, packaging, debugging, and release coupling before Trio has evidence that such complexity is necessary. Conversely, independent clients without a canonical contract make semantic drift difficult to detect.

The product owner requested that the proposed engine format be recorded in the canonical Trio specification.

## Decision

Propose a platform-independent semantic engine contract defined by:

- versioned JSON Schema for machine-readable event envelopes;
- JSON event records and JSON Lines replay/regression fixtures;
- deterministic reducer semantics where the same supported ordered event stream produces the same semantic state;
- native platform implementations that conform to the same fixtures rather than requiring one shared compiled engine binary.

The contract lives under [`spec/technical/engine/`](../technical/engine/README.md). It does not select network transport, cloud provider, model vendor, audio format, UI framework, or implementation language.

## Alternatives and rationale

**Shared Swift/Kotlin/Rust/C++ runtime now:** stronger implementation reuse, but introduces toolchain and integration coupling before a measured need exists.

**Protocol Buffers or another binary contract first:** compact and strongly typed, but less inspectable and harder to hand-author, diff, fuzz, and replay during rapid product development. It can be reconsidered if payload size or throughput becomes material.

**Independent platform behavior with documentation only:** simplest initially, but lacks executable conformance and makes subtle ordering/revision differences likely.

Human-readable JSON/JSONL provides the lowest-friction artifact for Git diffs, fixtures, test generation, simulator tooling, logs, and cross-platform comparison while Trio semantics are still evolving.

## Consequences

- The specification repository becomes the canonical owner of semantic event/reducer behavior.
- iOS and Android can implement the engine natively while sharing conformance fixtures.
- Native device APIs, presentation, and model/provider adapters remain outside the pure semantic reducer.
- Schema evolution and fixture compatibility become explicit engineering responsibilities.
- Event-specific payload schemas and expected-state fixtures must be added as product behavior becomes settled.
- This proposal does not itself prove any platform implementation conforms.

## Evidence and affected documents

Product-owner direction on 2026-10-02 requested this engine format be placed in the canonical specification.

Affected documents:

- [Specification map](../README.md)
- [Architecture](../technical/architecture.md)
- [API and events](../technical/api-and-events.md)
- [Semantic engine contract](../technical/engine/README.md)
- [Decision log](README.md)

Supersedes: None.
Superseded by: None.
Revisit when: measured serialization/throughput limits, cross-platform maintenance cost, or toolchain evidence shows a shared runtime or binary protocol would materially improve Trio.

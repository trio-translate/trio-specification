# Trio semantic engine contract

Status: Proposed

Related decision: [DEC-011](../../decisions/DEC-011-versioned-deterministic-engine-contract.md)

This directory defines the proposed platform-independent semantic engine contract for Trio. The engine is a contract, event model, reducer semantics, and replay corpus. It is **not** a requirement to share one compiled runtime between platforms.

A conforming client may implement the engine natively in its platform language while producing the same semantic state for the same ordered event stream.

## Proposed format

| Concern | Format |
| --- | --- |
| Machine-readable event contract | JSON Schema 2020-12 |
| Runtime event records | JSON objects |
| Replay/regression fixtures | JSON Lines (one event per line) |
| Semantic behavior | Deterministic reducer rules |
| Compatibility | Explicit schema version plus conformance fixtures |

The initial machine-readable envelope is [`event.schema.json`](event.schema.json). Reducer behavior is defined in [`state-machine.md`](state-machine.md). [`fixtures/basic-turn.jsonl`](fixtures/basic-turn.jsonl) is a minimal synthetic replay example.

This proposal does not choose HTTP, WebSocket, provider transport, audio format, authentication format, persistence technology, or a shared cross-platform language/runtime. Those remain separate architectural choices in [API and events](../api-and-events.md) and [architecture](../architecture.md).

## Boundary

The semantic engine owns:

- logical session state and lifecycle;
- participants and attributed turns;
- recognition/transcript state;
- translation-result state;
- turn revisions and cancellation;
- capability/recovery state represented as typed events;
- ordering, deduplication, and suppression of stale semantic results;
- deterministic replay of the above.

The semantic engine does not own:

- microphone, camera, speaker, or route APIs;
- OS permissions or background execution;
- SwiftUI, Jetpack Compose, navigation, layout, animation, typography, or gesture handling;
- model/provider SDKs or credentials;
- cloud routing and authentication;
- product heuristics that rewrite model output to compensate for model weakness.

Platform adapters translate native input/output into typed events and render engine state. Language/model adapters produce typed recognition and translation results. The engine preserves their semantics; it does not silently “fix” participant or model content.

## Core contract

A reducer is conceptually:

```text
reduce(previousState, event) -> newState
```

For a given supported schema version, initial state, and ordered event stream, every conforming implementation MUST produce the same semantic state.

Native side effects are outside this pure reducer. An implementation may derive platform commands from state/events, but replaying or receiving a duplicate event must not duplicate participant-visible output or restart ended/canceled work.

## Initial event vocabulary

The v1 envelope permits typed names. The first conformance corpus should cover at least:

- `session.started`
- `session.paused`
- `session.resumed`
- `session.ended`
- `turn.accepted`
- `recognition.updated`
- `recognition.finalized`
- `translation.updated`
- `translation.finalized`
- `turn.revised`
- `turn.canceled`
- `turn.completed`
- `capability.unavailable`
- `capability.recovered`
- `operation.failed`

This list is Proposed, not an assertion that every event is already implemented. Event-specific payload schemas should be added when the affected product behavior is sufficiently settled.

## Conformance

A platform implementation conforms only when it can replay the canonical fixtures and match the expected semantic state, including duplicate, out-of-order, stale-revision, cancellation, recovery, and ended-session cases.

Cross-platform verification should therefore use the same fixture:

```text
fixture.jsonl
    |
    +--> iOS engine ----> semantic state
    |
    +--> Android engine -> semantic state
                           |
                           +--> compare
```

The comparison is semantic rather than byte-for-byte UI equality. Native presentation and device behavior remain platform-specific.

## Versioning

- `schemaVersion` identifies the event-envelope major version.
- Incompatible envelope or reducer-semantics changes increment the major version.
- Event ordering is determined by `sequence`, never by timestamps.
- Consumers must not infer missing required semantics from unknown event types.
- A client that does not support the fixture/schema version must report that incompatibility rather than silently invent behavior.

The contract should stay human-readable while Trio is evolving. A binary protocol or shared runtime can be introduced later only when measured performance, interoperability, or maintenance evidence justifies the added complexity.

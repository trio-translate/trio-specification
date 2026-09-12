# Requirements guide

Status: Draft

Requirements describe observable behavior and quality. They follow the [situations](../situations/README.md); they do not substitute for choosing the customer or problem.

## Requirement sets

- [Functional requirements](functional.md): `FR-###`.
- [Quality requirements](quality.md): `QR-###`.
- [Language and AI quality](language-and-ai-quality.md): `LQ-###`.

Keep IDs stable across edits. Retire an ID explicitly rather than reusing it for unrelated behavior. New standalone requirements can use the [requirement template](../../templates/requirement.md).

## Required fields

Each requirement needs an ID, status, scope, source situation or rationale, observable behavior, acceptance criteria, and dependencies or unresolved decisions. If a measurable threshold is not agreed, label it proposed or `TBD`; the requirement is not ready for release acceptance until that gap is resolved.

## Status and scope

Document/requirement status uses `Draft`, `Proposed`, `Agreed`, or `Superseded`. Scope uses `Candidate launch`, `Future candidate`, or an explicitly agreed release name. Every requirement in the starter sets is **Draft** unless its entry says otherwise.

Confirmed outcomes with undecided delivery timing may use `Required product situation; release assignment undecided` or `Core supported conversation experience`. Entries may distinguish an agreed outcome from draft mechanisms and acceptance details. Read [non-negotiables](../non-negotiables.md) and the linked decision records before treating any weaker draft behavior as authoritative.

The words "must" and "shall" within a draft describe the proposed eventual obligation. They do not mark the proposal accepted. After a release is agreed, classify its requirements as must-have, should-have, or optional, with an explicit consequence for deferral.

Implementation and verification status belong in delivery tracking and acceptance evidence. An agreed requirement can still be unimplemented or failing.

## Readiness check

Can a developer identify the trigger, expected result, failure behavior, data/access implications, and dependencies? Can a tester demonstrate a meaningful pass and failure without guessing? If either answer is no, refine the requirement and linked journey before implementation.

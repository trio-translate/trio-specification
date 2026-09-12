# SIT-004: A remote conversation

Status: Draft
Scope: Future candidate

## People, trigger, and outcome

Two people are in different locations and want to exchange meaning in different languages. They need clear participant identity, dependable turn delivery, and control over audio and access.

## Proposed journey

1. One person creates a session and deliberately shares an invitation.
2. The recipient joins and receives a language-appropriate explanation of session behavior.
3. Each person confirms audio settings and takes a turn.
4. Both can see whether a message is captured, processing, delivered, failed, or revised.
5. They repair misunderstandings and end or leave with clear final state.

## Failure and recovery

Cover invitation expiry, accidental forwarding, the wrong participant joining, a device disconnecting mid-turn, duplicate delivery after retry, incompatible versions, and one person ending while the other is speaking. A reconnect must not restore revoked access or play stale speech.

## Completion and acceptance direction

Both people can complete the conversation and verify that leaving or ending stops their capture/output. Simulate network interruption and verify message ordering, identity/access controls, and correction delivery on two independent devices.

Related proposed behavior: FR-012 in [functional requirements](../requirements/functional.md).

## Open questions

Does Trio host the call or translate within an existing channel? Voice, text, or video? How are invitations and identity handled? What original audio should the recipient hear alongside translation? What are acceptable delay and cost per active conversation?

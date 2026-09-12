# Situation catalog

Status: Draft

Situations describe people's circumstances before specifying features. The catalog expresses the breadth of the vision; only an agreed release scope makes an entry a delivery commitment.

## Catalog

| ID | Situation | Desired outcome | Coverage in this baseline |
| --- | --- | --- | --- |
| SIT-001 | [Two people sharing a device](SIT-001-shared-device-conversation.md) | Each understands and can repair the conversation | Detailed starter; candidate launch |
| SIT-002 | [Understanding or preparing language alone](SIT-002-solo-understanding.md) | Understand material or express an intended message | Starter; future candidate |
| SIT-003 | [A multilingual group together](SIT-003-multilingual-group.md) | Everyone can follow and contribute | Starter; future candidate |
| SIT-004 | [A remote conversation](SIT-004-remote-conversation.md) | Exchange meaning across distance and languages | Starter; future candidate |
| SIT-005 | A pair together using their own devices | Read and control language on a personal screen | Catalog only |
| SIT-006 | Reading a sign, menu, or short document | Understand text while preserving relevant context | Catalog only |
| SIT-007 | A brief travel or service interaction | Complete a practical task with minimal setup | Catalog only |
| SIT-008 | Repeated family or social conversation | Build relationships despite a language gap | Catalog only; research context for SIT-001 |
| SIT-009 | A workplace or customer interaction | Complete a work task with clear responsibility | Catalog only |
| SIT-010 | A learner asks for an explanation | Understand wording and practice an expression | Catalog only |
| SIT-011 | A mixed in-person and remote group | Keep both local and remote participants included | Catalog only |
| SIT-012 | A sensitive conversation | Control disclosure, retention, and who can participate | Catalog only; privacy also applies to every situation |
| SIT-013 | Understanding tone or cultural context | Explore possible meanings and ask for clarification without claiming to know another person's intent | Catalog only; may involve a shared language |
| SIT-014 | [Offline passenger/driver conversation in a car](SIT-014-car-conversation.md) | Passenger starts/operates; driver receives audio without a screen; full conversation works offline | User-required situation; release undecided |

IDs are stable. New situations receive new IDs; do not reuse retired IDs. Catalog-only entries need a document based on the [situation template](../../templates/situation.md) before implementation planning.

## Dimensions to cover

For each selected situation, vary language direction, dialect/accent, literacy, hearing and vision, familiarity with technology, device ownership, orientation, background noise, connectivity, and willingness to be recorded. Also test names, numbers, negation, interruptions, and ambiguity.

Use the [condition catalog](../conditions/README.md) for music and noise, and the [continuous-session contract](../non-negotiables.md) for one-action operation and word-based inactivity. Compose them with relevant situations, roles, connectivity, and actual input/output routes. Cross-cutting failures such as microphone denial and poor connectivity also need coverage in every affected situation through the [recovery matrix](../experience/recovery.md).

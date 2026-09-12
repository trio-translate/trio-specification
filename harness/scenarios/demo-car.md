# DEMO-001: A complete offline car conversation

Status: Proposed demo fixture; not executed
Links: SIT-014, COND-001, COND-002; [demo contract](../conversation-and-demo.md)

Use a parked car or controlled acoustic setup. Roles are passenger/operator and driver/listener. Select two supported languages and the actual route before execution. English prompts below describe semantic goals; bilingual reviewers prepare equivalent natural utterances in the selected languages. These fixture proposals do not select a launch language pair.

| Step | Stimulus or goal | Observable outcome |
| --- | --- | --- |
| Prepare/start | Complete resources/permissions before network block; one start press | Fresh offline capture, recognition, translation and required speech work |
| Passenger | Propose meeting at 14:30 at the north entrance, not the south | Driver receives all material details by audio and confirms what was actually heard |
| Driver | Ask whether the meeting is today or tomorrow | Passenger receives the translated question and answers naturally |
| Repair | Change the time to 15:30; clarify the entrance | Revised meaning is delivered without stale contradictory output; actor does not see hidden expected answer |
| Noise | Introduce controlled road noise while conversation continues | Actual input meter remains truthful; noise is not a word-timer reset |
| Music | Play licensed/synthetic music and ask another question | All Trio TTS muted; text continues; driver delivery marked paused |
| Resume audio | Passenger pauses music | Fresh spoken exchange works; no stale queued speech burst |
| Recovery | Disconnect/restore the declared route using agreed private-output policy | Automatic recovery or honest unavailable state; no silent public-speaker switch |
| UX | Passenger changes theme, opens/closes a view, returns | Session, mic/stop visibility, content provenance and word clock preserved |
| End | Explicit stop during pending output, then navigate/reopen | No further capture/TTS or late-response resurrection; remembered view and way back |

Record what each actor could observe, every spoken turn, all interventions and result timestamps. A director may know the complete script; the listener may not. Include the unexpected participant follow-up rather than forcing a memorized response. Mark omitted steps and faults that were requested but never actually applied.

Run separate cases for word inactivity (noise/lyrics only with a healthy observer, words near the boundary, failed observer) and twelve-hour endurance. Do not prolong this demo by disabling or inventing the agreed timeout policy.

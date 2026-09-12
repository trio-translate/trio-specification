# Analytics and success

Status: Draft

## Main outcome hypothesis

Track **successful understanding situations per returning customer**, supported by participant feedback. This is a proposed value measure, not an automatic assertion that an AI system can detect mutual understanding.

Define a successful SIT-001 situation through an observed or voluntarily reported task outcome: both participants can act on or restate the intended meaning, or knowingly resolve an ambiguity. Raw turn counts are activity, not proof of this outcome.

## Metric definitions to refine

| Metric | Definition / denominator | Collection boundary |
| --- | --- | --- |
| First-situation activation | Eligible new starters who complete the selected journey / eligible new starters | Define eligibility and completion event |
| Reported understanding | Sessions with positive voluntary outcome feedback / sessions with outcome feedback | Report response rate and selection bias |
| Repeat use | Activated customers with another qualifying situation within a defined window / customers with a full observation window | Window and identity model TBD |
| Repair success | Evaluated misunderstanding cases successfully repaired / evaluated cases with a repair attempt | Primarily observed tasks; do not inspect conversations by default |
| Failed-turn rate | Final failed accepted turns / accepted turns | Track deliberate cancellations separately |
| Paid continuation | Eligible pilot customers who purchase/renew / eligible customers offered the same terms | Use actual payment evidence |
| Cost per successful situation | Attributable service cost / evaluated or reported successful situations | Label sampled/estimated outcome denominator |
| Support burden | Support time or contacts / active paying customers | Avoid conversation content in aggregate reporting |
| Unattended continuity | Prepared twelve-hour sessions that deliver the required experience with zero routine interventions / eligible full-duration test sessions | Record reason for every interruption; separate user end and predefined word timeout |
| Required interventions | Routine touches, restarts, wakes, and confirmations after start per evaluated session | Target zero; optional intentional corrections/music changes reported separately |
| Capability recovery | Fault cases restored to required participant outcome within agreed budgets / injected or observed fault cases | Do not count passenger text as recovered driver audio |

## Proposed event vocabulary

`session_started`, `turn_submitted`, `turn_completed`, `turn_failed`, `turn_canceled`, `correction_requested`, `clarification_requested`, `audio_stopped`, `session_ended`, `allowance_warning_shown`, and `outcome_feedback_submitted` are candidate events. Define exact firing rules, identity scope, duplicate handling, allowed attributes, and retention before instrumentation.

Distinguish explicit user end, predefined word-inactivity end, external termination, and unintended failure. Proposed content-free capability/recovery and intervention events can explain continuity. Local word activity does not require shipping transcript words, audio, or fine-grained microphone levels to analytics.

Do not send raw audio, transcript, translation, free-text feedback, or secrets through general analytics. Language metadata and identifiers can still be sensitive; collect only dimensions justified by a stated question.

## Decision use

Agree target values, cohort definitions, observation windows, and quality/cost guardrails before a pilot. Interpret low use by examining the underlying situation and friction, not by adding engagement mechanics automatically. Expansion should require evidence of useful repeat behavior and manageable cost/support.

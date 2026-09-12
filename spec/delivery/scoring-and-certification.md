# Scoring and internal certification

Status: Proposed

The product owner requested an automated scoring/certification system. This is a proposed internal Trio evaluation system. Its weights, detailed test pack, sample sizes, thresholds, review process, and release profiles have not been agreed. It is not an external accreditation.

## What remains missing from the product specification

The main gaps are precision and evidence, rather than a longer feature list:

| Gap | Decision / evidence needed |
| --- | --- |
| Qualifying words and idle duration | Which provisional words count, language handling, duplicate events, music/TTS exclusion, observer failure, precise timer boundary |
| Recognized meaning and natural interaction | Names, numbers, negation, short/long utterances, first/last-word clipping, overlap, interruption, accents, language switching, correct recipient |
| Supported configurations | Exact devices/OS, local/cloud engine versions, language directions, microphones, speakers/earphones, power conditions, environmental fixtures |
| Twelve-hour useful operation | Fresh exchanges and delivery throughout the run, zero routine interventions, bounded resource growth, actual lock/background and connection-renewal behavior |
| Graceful recovery budgets | Maximum capability gaps, what can be buffered, how lost input is disclosed, and recipient-specific recovery rather than UI survival |
| Offline preparation and updates | Local resources/voices, storage shortages, damaged/missing packs, offline entitlement, updates that preserve active use |
| Privacy and data lifecycle | Actual capture boundaries, no hidden uploads, content-free diagnostics, deletion/retention and shared-device isolation |
| Accessible UI under change | All themes/locales/text sizes, separate app status, no focus or content loss on rotation/theme change |
| Commercial readiness | Entitlement sufficient for the promised session, real service/resource cost, support burden, real repeat use and payment evidence |

These expand existing requirements into testable boundaries. Specific new behaviors remain proposals until agreed; feasibility has not been measured.

## Three independent outputs

1. **Hard gates:** non-negotiable or release-critical checks must all pass. Unexpected stops, invented participant text, incorrect timeout behavior, hidden capture, and an incomplete offline car path cannot be averaged away.
2. **Quality score:** a weighted 0–100 assessment of measured language quality, delay, recovery, accessibility, and efficiency. Proposed weights are 40/20/20/10/10. Quality targets and acceptable floors remain null until agreed; no invented performance data fills them.
3. **Evidence coverage:** the number of valid completed checks over all applicable checks, with explicit missing, unconfigured, failed, and invalid results. Omitted checks stay in the denominator.

Keep these outputs together. "90/100, failed stop gate" means blocked. A partially measured score is labeled a provisional lower bound, never presented as a complete score or a certificate. A missing human review is missing evidence.

## Scope every evaluation

Evaluate one explicit combination of app build, processing configuration revision, device/OS, both language directions, actual audio route, conditions, power setup, and test-profile version. The offline-car profile includes every core check plus car-specific checks; it cannot drop core gates.

Repeat evaluations across the agreed release matrix. One passing configuration does not certify all devices or all languages. A build, prompt/model, local resource, route, platform, or material test-pack change invalidates the relevant prior scope. The first evaluator handles one scope at a time; release-wide matrix aggregation and certificate issuance remain later work.

## Automation and human evidence

| Evidence producer | Suitable checks | What it cannot establish alone |
| --- | --- | --- |
| Unit/component fault harness | Word-timer boundaries, cancellation, duplicated/out-of-order results, content provenance | Real microphone/speaker or OS endurance |
| UI automation | Text/status separation, all themes, controls, offline preference persistence | Real-world understanding and full assistive-technology usability |
| Instrumented physical devices | Actual audio routes, no capture after stop, no-network operation, twelve-hour run, interruptions | Whether subtle meaning and social participation are preserved |
| Bilingual human review | Material meaning errors and task outcome on a versioned fixture set | Universal accuracy beyond the reviewed sample |
| Participant/accessibility review | Usability, repair, listening-only and assistive journeys | Every device and population from one small study |

Human review can produce a machine-readable result with reviewer identity and an evidence artifact. Automating ingestion is not the same as automating the judgment. AI grading may assist triage; it is not sole proof of critical meaning or independent review.

## Executable baseline

The [catalog](../../certification/catalog.json) contains versioned checks and links to requirement IDs. [The evaluator](../../tools/certify.py) accepts a report manifest and evidence files, validates expected checks, methods, case coverage, values, sample counts, scope consistency, and file hashes, and emits JSON plus Markdown readiness reports. See [usage and evidence format](../../certification/README.md).

Current limitations are deliberate and visible: no app adapters/device farm are implemented here; manifest metrics come from the test producer; artifact hashes check integrity, not truth; signed CI provenance, protected rubric approval, corpus/sample-policy agreement, freshness policy, matrix aggregation, and certificate issuance remain to be implemented. A forged producer report is not detected merely by matching its hash.

The tool never issues a certificate. Its highest result is `READY_FOR_REVIEW` for an approved, fully configured rubric with complete passing measured evidence and the required score. The checked-in rubric is Proposed, score thresholds/sample sizes are unconfigured, and the example has no test results; the expected current state is `INCOMPLETE`, certificate `NOT_ISSUED`.

## Scoring rule

Each scored metric has a weight, a poor boundary, and a target. For higher-is-better metrics, normalize `(value - poor) / (target - poor)`; for lower-is-better metrics, normalize `(poor - value) / (poor - target)`. Clamp to 0–1 and multiply by weight. Missing/unconfigured results contribute no earned points while retaining their full weight in the denominator.

Agree thresholds, minimum samples, fixture coverage, and minimum total score before using scores for release decisions. Retain per-direction raw measurements and distributions; aggregates must not hide a broken required language direction. An approved catalog must contain explicit, ordered thresholds and sample sizes.

## Suggested rollout of this system

1. Agree the initial situation/profile and test matrix, then settle the timeout, latency/recovery/resource budgets, and language-review rubric.
2. Connect the initial app to fast unit/UI evidence producers. Run those in its CI on changes; publish gate, score, coverage, and missing-evidence reports together.
3. Add physical-device/audio and no-network runs. Run full twelve-hour endurance for candidate builds; short smoke tests cannot replace it.
4. Add bilingual and accessibility review artifacts, protected rubric approval, and trustworthy build/test provenance.
5. Aggregate all required configurations and have an accountable reviewer approve any internal certificate with a precise scope, evidence links, version, and invalidation/expiry policy.

Certification readiness must not become a substitute for market learning. Repeat use, payment, and support economics remain separate commercial evidence in [analytics and success](../business/analytics-and-success.md).

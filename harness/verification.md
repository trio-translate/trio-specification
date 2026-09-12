# Verification and defect prevention

Status: Proposed working process

The target is a product without defects. Release claims must be bounded by declared versions, situations, languages, devices, routes, and conditions. Passing tests increases confidence; it cannot prove every possible interaction or future device bug absent.

## Verification ladder

| Stage | Specific procedure | Required result and evidence |
| --- | --- | --- |
| Specification | Run repository checks; trace the work packet to decisions, observable criteria, and coverage registry | No broken references; explicit support scope, owners, unresolved thresholds |
| Static/build | Clean reproducible build, compiler/type/lint checks, dependency/security review appropriate to selected stack | Exact commit/toolchain; build artifact identity; no ignored failing checks |
| Logic/contracts | Deterministic tests of session generations, stop races, word timeout, content origin, entitlement and capability selection | Relevant negative/positive controls; fault fails before fix and passes after; no production content |
| Integration | Real selected engine adapters and resource provisioning; network blocked for offline claims; cancel/late events and faults | Both directions, real adapter versions, actual failure/recovery and resource traces |
| UI/accessibility | Traverse every view/dialog/state with touch and selected assistive technologies; themes, restored views, back navigation and mic feedback | Screen inventory; independent status/content assertions; no capture restarted by navigation |
| Physical audio | Controlled speech through actual microphones and recipient output; echo, overlap, accents, distance, music/noise and route changes | Source and received output evidence, gaps, latency, intelligibility and required actions per recipient |
| Endurance/load | Twelve real hours plus crossing the boundary; variable fresh speech and normal silence; lock/background, renewals, thermal/power/memory trends | One initial start, zero routine interventions; no app cutoff; realistic load and resource costs |
| Human/commercial/release | Bilingual meaning review, participant task success, privacy/security review, unit economics, pilot evidence, rollback drill | Exact claim/evidence mapping; no unresolved defect violating promised behavior; approved thresholds and support plan |

The matrix in [coverage.json](coverage.json) is a planning inventory. It does not replace app test discovery. Every accepted release requirement must map to executable tests and, where needed, physical/human procedures. The app test producer must report omitted, skipped, failed, and inconclusive cases with stable IDs; a zero-test suite cannot pass.

## Scenario coverage

Enumerate selected situations, roles, language directions/accents/scripts, device and OS versions, actual input/output route, connectivity, installed models, lifecycle, permissions, appearance, assistive input, power and resource conditions. For selected speech situations test music/noise neither, each individually, and together. Text-only situations need an explicit applicability rationale, not fabricated audio results.

Exhaustively test critical state transitions and mandatory combinations. Use risk-based pairwise or higher-order generation for the remaining feasible space, recording constraints, generator/version/seed, coverage holes, and why the selection is adequate. Pairwise coverage is not all combinations. Never reduce the required car + offline + music + noise + driver-listening combination to isolated single-feature tests. Every supported route and language direction needs evidence; equivalence classes require a reasoned and reviewed argument.

Mandatory families: permission denial/revocation, no/missing/corrupt offline resources, cold start without network, echo and late TTS during music, words at timeout boundaries, failed word observer, stop during recovery, back/restore and theme changes during capture, engine/OS updates, resource pressure, private-route loss, content/status integrity, wrong/repaired meaning, and purchase/entitlement boundaries when paid access is selected.

## Bug lifecycle

Use the [defect template](../templates/defect.md). Record affected promise, severity, reproducible environment, expected/actual behavior, failing fixture, evidence, and owner. Investigate the root cause and neighboring states. Add a meaningful regression assertion before the fix when reproducible; otherwise preserve the best available trace and strengthen observability without logging private content. Verify the fix and affected integration/device cases, then close against a specific build.

Proposed release policy: no known unresolved defect that violates a required outcome in advertised scope. Security, privacy, billing correctness, material meaning, recipient delivery, and continuity failures are blocking. Lower impact problems still need an honest disposition; relabeling a defect as a limitation cannot waive an agreed non-negotiable. Narrowing advertised scope requires an explicit product decision and matching claims.

Do not retry flakiness until green and discard earlier failures. Track frequency, seeds, first failure, retries, and cause. A quarantined required test leaves a coverage gap. Test harness failure produces `invalid`/`blocked`, not product pass. Use deliberate bad inputs and seeded invariant violations to check that evaluators catch failures. Independent bilingual review avoids a model grading its own translations as the sole oracle.

## Evidence invalidation and maintenance

Reassess affected evidence after changes to app, engine, prompt, corpus, language resources, OS, audio route, privacy policy, billing, or thresholds. Compare build identities and scope before combining runs. Define freshness windows in the approved release policy; until then, treat freshness as unconfigured. Preserve failures for regression selection and maintain an incident-to-requirement/test chain.

The evaluator's hash checks cannot authenticate a producer. Trusted CI/device identities, protected policy approval, complete matrix aggregation, provenance/freshness enforcement, and physical test infrastructure must be integrated before internal certification is issued. See [scoring](../spec/delivery/scoring-and-certification.md).

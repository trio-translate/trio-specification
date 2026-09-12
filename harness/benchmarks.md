# Benchmarks and repeatability

Status: Proposed protocol; no app benchmark measured

Benchmark participant outcomes, not isolated model speed. Pin build, engine/prompt/resource versions, device/OS, actual audio route, corpus, language directions, environment, and power setup. Record cold/warm starts separately. Compare a candidate with the current baseline using matched conditions and independently varied run order.

## Measurement pack

| Measure | Procedure |
| --- | --- |
| Meaning | Blinded bilingual review of source and received translation, including names/numbers/negation, ambiguity, repair, dialects and overlapping speech |
| Useful latency | Monotonic timestamps from fresh input/utterance boundaries to usable text and heard output; report definition, p50/p95/p99 and sample counts separately by direction |
| Continuity | Useful exchanges over actual elapsed time; interruptions, input/output gaps, duplicates, intervention count and recipient recovery |
| Audio | Intelligibility and suppression at actual routes, echo/leakage, clipping, noise/music transitions; never equate waveform presence with correct words |
| Resources | Memory growth, CPU/accelerator load where measurable, power/thermal curves, storage/download footprint and network bytes |
| Economics | Active speech/idle time, ASR/translation/TTS/retries/fan-out usage, licenses/infrastructure/support; measured invoices versus assumed rates explicitly separated |

Agree sample sizes, acceptable variance, regression tolerances, and absolute budgets before scoring. Preserve raw samples and outliers; report confidence intervals when the design supports them. A percentile without enough samples is not reliable evidence. Include long-session and heavy-user distributions. Do not improve average speed by excluding failed or slow exchanges from the denominator.

Maintain a small development fixture set and a separate held-out evaluation set. Version prompts, models, voices and seed where available, but do not claim seed alone guarantees deterministic speech/model behavior. Test sensitivity to speakers and unseen content; fixed demonstrations can overfit. Language reviewers should not see which implementation produced the output where practical.

Competitors use the same task, pair, hardware class, network, route, and measurement definitions when feasible. Record unmatched conditions instead of combining incompatible scores. Vendor pages supply claims, not benchmark numbers. Check [competitor analysis](../spec/business/competitor-analysis.md) before repeating or publishing a comparison.

The current evaluator accepts one scoped aggregate report; benchmark sample collection/statistics and cross-run comparison are adapter work. Preserve raw data next to the resulting [evidence manifest](../certification/README.md). Do not claim a candidate wins, is cheaper, or qualifies for release until the matched experiment supports it.

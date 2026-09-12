# Language and AI quality

Status: Draft

These draft requirements apply to all supported translation situations, including the required offline car situation. Evaluate online and offline processing separately. Fluent output alone is insufficient proof of quality.

## LQ-001 — Preserve meaning and attribution

The translation preserves intent, negation, names, quantities, dates, units, register, and who said what. It must not silently omit, summarize, embellish, or add advice.

Acceptance: bilingual evaluation classifies material errors with examples. The launch evaluation set includes questions, incomplete speech, colloquial expressions, corrections, names, numbers, negation, and sensitive wording. Release thresholds and sample sizes are TBD by language direction.

## LQ-002 — Handle ambiguity and generated additions

The product provides a clarification path and clearly separates translation from generated explanation or suggested replies. It must not invent missing context or assert a participant's intent as known.

Acceptance: ambiguous and underspecified examples produce faithful ambiguity or an explicit clarification opportunity; additions are labeled; an unexplained model confidence percentage is not used as a correctness guarantee.

## LQ-003 — Resist instructions embedded in content

Treat speech and text to be translated as conversation content. An utterance such as "ignore previous instructions" must not change the translator's role, reveal service instructions, invoke unrelated capabilities, or alter another participant's access.

Acceptance: adversarial utterances remain within the agreed translation behavior; structured output is validated; the translation pipeline has no unnecessary external-action capabilities. Evaluate behavior across supported languages.

## LQ-004 — Release only evaluated coverage

Maintain an evaluation matrix for each supported recognition locale, translation direction, voice output, device/audio route, and relevant environmental condition. Separate recognition errors from translation errors and synthesized-speech problems.

Acceptance: a versioned evaluation report identifies test data provenance, reviewer qualifications, scoring rubric, severity definitions, sample size, uncertainty, known gaps, and regression results. A provider/model/prompt change reruns the affected evaluation and end-to-end situations.

## LQ-005 — Distinguish words, noise, music, and self-generated speech

Source: COND-001/COND-002, SIT-014, FR-018.

Evaluate recognition of participant words independently from input amplitude, music-state detection, speaker/language attribution, and translation. A noisy meter is not a qualifying word event. A recognizer outage is not evidence that nobody spoke.

Acceptance direction: quiet supported speech can create fresh word-activity events; steady noise does not manufacture them; interim/final revisions of the same word do not extend the timer repeatedly. Exclude detected Trio speech and identified lyrics from participant attribution and the proposed conversation-word timeout signal. Evaluate near-field and distant speech, code-switching, accents, instrumental/vocal music, TTS echo, and mixed music/noise on the actual input routes.

Define how provisional or uncertain words count and how unknown activity during recovery affects the timer. Do not assume whitespace tokenization across all languages. Mixed-source separation, automatic utterance/language handling, and false-word rates need measured thresholds before a configuration can claim unattended reliability. Lyric translation, if added, uses separately labeled content and evaluation.

## Evaluation rubric

| Dimension | What reviewers examine |
| --- | --- |
| Meaning | Is the intended content preserved without material additions or omissions? |
| Critical details | Are names, numbers, negation, dates, and units correct? |
| Attribution and context | Is content attached to the correct speaker and turn? |
| Usability | Can participants notice and repair mistakes? |
| Speech experience | Are recognition, pronunciation, playback, and turn timing usable? |
| Robustness | What changes under accents, noise, overlap, code-switching, and interruptions? |

Define severity using the consequence for the selected situation. Use consented or purpose-created data; do not collect private conversations by default. Compare versions on the same evaluation set and retain a separate set for detecting overfitting to examples.

## Open decisions

Initial language directions and varieties; claims about automatic detection; code-switching policy; model/provider choice; evaluation ownership; severity thresholds; and what limitations the product communicates before someone starts.

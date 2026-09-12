# Executed test evidence

The specification owns the stack-independent execution evaluator in
`tools/execution.py`. Apple-specific execution, test-result parsing, protected
storage, and collection belong to the selected application repository.

Use one evidence manifest: the existing certification envelope may include an
`execution` property with the following versioned fields. Execution observations
do not automatically become `CERT-*` measurements; those need their own scoped
procedure and oracle. Legacy certification and planned coverage remain distinct.

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1` |
| `app_commit`, `spec_commit` | Full immutable Git revisions |
| `plan_sha256` | Hash of the frozen required test plan |
| `adapter` | Registered implementation identifier, never a shell command |
| `required_tests` | Nonempty unique expected IDs, resolved before execution |
| `tests` | Unique observed `{id, status}` rows from the real producer |
| `producer_status` | `passed`, `failed`, `blocked`, or `invalid` |
| `complete` | Whether a durable producer completion witness was obtained |
| `elapsed_seconds` | Finite elapsed wall time including execution overhead |

Observed statuses are `passed`, `failed`, `skipped`, `unavailable`, or
`inconclusive`. A missing required result or completion witness is invalid;
skipped/unavailable/inconclusive required tests leave a blocked lane. Preserve
observed product failures alongside missing evidence. Empty or malformed test
selection cannot pass. Retry runs have new identities and never overwrite failures.

```sh
python tools/harness.py analyze --evidence /private/local/path/manifest.json
```

Exit codes are 0 for complete passing execution, 1 for product/test failure,
2 for blocked required evidence, and 3 for invalid evidence or malformed input.
This command does not verify authenticity, artifact completeness, expiry, or the
product matrix. The application runner must enforce those additional boundaries
before making a combined claim. It never issues a certificate.

`write_manifest` creates a durable manifest exclusively with private permissions,
without overwriting files or following an existing file symlink. Its caller must
provide an owned protected/encrypted directory. `expiry` computes retention from
capture time: metadata 30 days, sensitive data 7 days, with derivatives inheriting
the earliest applicable source expiry. It does not schedule physical deletion.

The benchmark evaluator checks three frozen weighted lanes (`core`, `ui`,
`adapter`) and a comparable `clean` lane with at least five paired observations.
Each pair records a matched-condition hash, finite positive durations, statuses,
and equal assertion hashes. Failed, missing, or mismatched pairs invalidate the
comparison rather than disappearing from a successful-only average. Weighted
median duration totals must improve by at least 50%; every lane must avoid more
than 10% regression. `numeric_gates_met` deliberately leaves provenance,
equivalence, and statistical uncertainty review open and cannot qualify a
foundation by itself. The selected app freezes the actual edits and sampling rule.

Regression controls exercise omissions, skips, malformed identities, duplicate
observations, lost completion, immutable failures, expiry inheritance, failed
benchmark pairs, assertion drift, missing clean evidence, and concealed lane
regressions. These are evaluator tests, not executed app or physical evidence.

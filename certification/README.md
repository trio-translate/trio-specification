# Automated evaluation baseline

Status: Proposed rubric; implemented evaluator prototype

This folder turns the [certification proposal](../spec/delivery/scoring-and-certification.md) into executable checks over submitted evidence. It does not run the Trio app or issue certificates. The current catalog covers a starter subset of the product requirements; it is not complete release certification coverage.

## Run it

From the repository root, with Python 3.10 or newer and no additional packages:

```sh
python -m unittest discover -s tests -v
python tools/certify.py --evidence certification/evidence/not-tested.json
```

The second command intentionally exits **2** and reports `INCOMPLETE`: no app has been tested. It writes `report.json` and `report.md` under the ignored `certification/reports/current` directory. Pass `--output-dir` to select another report directory. Generated reports/evidence must be retained by the test pipeline, not mistaken for source-controlled product implementation.

## Exit codes and results

| Exit | Meaning |
| --- | --- |
| 0 | `READY_FOR_REVIEW`: submitted measured evidence meets the configured, approved test pack; no certificate issued |
| 1 | `BLOCKED` hard gate or `BELOW_TARGET` quality score |
| 2 | Missing/unconfigured evidence, proposed rubric, or `SIMULATION_ONLY` |
| 3 | Invalid input/schema or output error; invalid input replaces the report with `INVALID_INPUT` when writable; never consume an older report after an output error |

`certificate` is always `NOT_ISSUED`. Gate failure overrides a good quality score. Missing score weight is not redistributed. A proposed rubric cannot become ready simply because evidence passes. Synthetic manifests can exercise the calculation but never become ready for certification review.

## Catalog

[catalog.json](catalog.json) is versioned. `core` checks apply to the continuous experience; `offline_car` inherits every core check and adds its own. Each check identifies requirements, allowed evidence methods, required case IDs, units, minimum samples, and either a gate comparison or a scoring function.

The proposed score weights total 100. Target/poor boundaries, the overall required score, and some sample policies are null because they have not been agreed. The operational gate fixtures/minimum counts are also a draft test design. Do not change `policy_status` to `approved` until the product owner approves the concrete rubric and scope; protected approval enforcement is future work.

Catalog 0.2.0 adds CERT-016 for device capability readiness and selection. There are 21 checks in the offline-car profile, including inherited core checks. The [harness coverage report](../harness/README.md) also lists requirements still lacking certification checks; a complete planning map does not make this starter rubric exhaustive.

## Evidence manifest

Start from [not-tested.json](evidence/not-tested.json). Set a unique run ID, exact catalog version, `catalog_sha256` using `tools.certify.scope_hash(catalog)`, and `kind` (`measured`, `synthetic`, or `not_tested`). Fill every scope field: profile, app build, processing revision, physical device/OS, two languages, actual route, conditions, power configuration, and fixture revision. Spell out both translation directions in the fixtures; a language pair alone is not evidence that both passed. A catalog hash mismatch blocks readiness even if its version label is unchanged.

Each result must contain:

| Field | Required content |
| --- | --- |
| `check_id` | One applicable unique catalog ID |
| `scope_sha256` | `tools.certify.scope_hash(scope)` using canonical JSON; changing the declared scope invalidates old results |
| `method` | Allowed producer method: `device`, `ui`, `integration`, or `human` |
| `value` | Finite numeric measurement; booleans and nonfinite values are rejected |
| `samples` | Positive integer meeting the configured minimum |
| `cases` | Unique executed case IDs including every case required by that check |
| `observed_at` | ISO timestamp with timezone, not in the future |
| `reviewer` | Required nonempty reviewer identity for human evidence |
| `artifacts` | At least one object with a relative `path` and lowercase SHA-256 digest |

Artifact paths resolve within the manifest's directory and cannot escape it. Hashes are checked from file bytes. Keep raw participant recordings out of this repository; use purpose-created or appropriately consented evidence under the agreed retention/access policy.

A composite gate's `value` is the producer's violation count across its required cases, except explicitly documented numeric gates such as elapsed seconds. The evaluator validates case coverage and the number, but cannot prove the producer executed those assertions correctly. Include detailed raw results and fixture identities in the artifacts. Device evidence must measure real routes/resources and actual elapsed endurance time.

## Trust and next integration step

The first integration is an app-specific test producer that emits this format from unit/UI/device runs and human-reviewed fixtures. A real CI integration must bind reports to exact builds, catalog content, test/corpus versions, trusted producer identities, and protected approval; it must also define freshness/invalidation and aggregate the complete supported matrix.

This prototype checks declared scope consistency and file integrity, not signed provenance or the truth of measurements. It does not establish sample representativeness, statistical confidence, external accreditation, or that all release requirements have been covered. Those omissions remain explicit blockers to issuing an internal certificate.

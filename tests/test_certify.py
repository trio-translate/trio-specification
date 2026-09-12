"""Synthetic fixtures test the evaluator, not the Trio app or its quality."""

import copy
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools.certify import evaluate, file_hash, load_json, main, scope_hash


class CertificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        artifact = self.root / "fixture.txt"
        artifact.write_text("Synthetic evaluator test artifact; no app tested.\n", encoding="utf-8")
        shared = {"requirements": ["FR-017"], "profiles": ["core"], "methods": ["device"],
                  "cases": ["case-a"], "min_samples": 1}
        self.catalog = {
            "schema_version": 1, "catalog_version": "test-only", "policy_status": "approved",
            "minimum_score": 80, "profiles": {"core": {"extends": []},
                                               "car": {"extends": ["core"]}},
            "checks": [
                dict(shared, id="CERT-001", title="No extra interaction", kind="gate",
                     operator="eq", threshold=0),
                dict(shared, id="CERT-101", title="Lower delay", kind="score", direction="lower",
                     weight=60, poor=1000, target=100),
                dict(shared, id="CERT-102", title="Higher meaning quality", kind="score",
                     direction="higher", weight=40, poor=0, target=100, methods=["human"]),
            ],
        }
        self.evidence = {
            "schema_version": 1, "catalog_version": "test-only", "kind": "measured",
            "run_id": "unit-test-only", "scope": {
                "profile": "core", "build_id": "fixture-build", "engine_revision": "fixture-engine",
                "device": "fixture-device", "os": "fixture-os", "language_pair": ["en", "nb"],
                "audio_route": "fixture-route", "conditions": ["fixture-quiet"],
                "power_setup": "fixture-power", "fixture_revision": "fixture-v1",
            }, "results": [],
        }
        for check, value in zip(self.catalog["checks"], [0, 100, 100]):
            self.evidence["results"].append({
                "check_id": check["id"], "scope_sha256": scope_hash(self.evidence["scope"]),
                "method": check["methods"][0], "value": value, "samples": 1,
                "cases": ["case-a"], "observed_at": "2026-01-01T00:00:00Z",
                "reviewer": "Synthetic reviewer fixture",
                "artifacts": [{"path": "fixture.txt", "sha256": file_hash(artifact)}],
            })

    def run_eval(self):
        self.evidence["catalog_sha256"] = scope_hash(self.catalog)
        return evaluate(self.catalog, self.evidence, self.root)

    def test_complete_evidence_is_only_ready_for_review(self):
        report = self.run_eval()
        self.assertEqual(report["readiness"], "READY_FOR_REVIEW")
        self.assertEqual(report["certificate"], "NOT_ISSUED")
        self.assertEqual(report["provisional_quality_score"], 100)

    def test_failed_gate_cannot_be_averaged_away(self):
        self.evidence["results"][0]["value"] = 1
        report = self.run_eval()
        self.assertEqual(report["readiness"], "BLOCKED")
        self.assertEqual(report["provisional_quality_score"], 100)

    def test_missing_gate_remains_in_denominator(self):
        self.evidence["results"].pop(0)
        report = self.run_eval()
        self.assertEqual(report["readiness"], "INCOMPLETE")
        self.assertEqual(report["coverage"]["required"], 3)
        self.assertEqual(report["coverage"]["evaluated"], 2)

    def test_missing_score_keeps_its_weight(self):
        self.evidence["results"].pop()
        report = self.run_eval()
        self.assertEqual(report["provisional_quality_score"], 60)
        self.assertFalse(report["score_is_complete"])
        self.assertEqual(report["readiness"], "INCOMPLETE")

    def test_score_direction_and_interpolation(self):
        self.evidence["results"][1]["value"] = 550
        self.evidence["results"][2]["value"] = 50
        report = self.run_eval()
        self.assertEqual(report["provisional_quality_score"], 50)
        self.assertEqual(report["readiness"], "BELOW_TARGET")

    def test_scores_clamp_without_negative_or_extra_credit(self):
        self.evidence["results"][1]["value"] = 2000
        self.evidence["results"][2]["value"] = 500
        self.assertEqual(self.run_eval()["provisional_quality_score"], 40)

    def test_synthetic_evidence_never_becomes_ready(self):
        self.evidence["kind"] = "synthetic"
        self.assertEqual(self.run_eval()["readiness"], "SIMULATION_ONLY")

    def test_proposed_rubric_blocks_readiness(self):
        self.catalog["policy_status"] = "proposed"
        self.assertEqual(self.run_eval()["readiness"], "INCOMPLETE")

    def test_unconfigured_threshold_and_samples_block(self):
        self.catalog["checks"][0]["threshold"] = None
        self.catalog["checks"][1]["min_samples"] = None
        report = self.run_eval()
        self.assertEqual(report["readiness"], "INCOMPLETE")
        self.assertEqual(report["checks"][0]["status"], "UNCONFIGURED")

    def test_inherited_profile_cannot_drop_core_checks(self):
        self.evidence["scope"]["profile"] = "car"
        for result in self.evidence["results"]:
            result["scope_sha256"] = scope_hash(self.evidence["scope"])
        self.catalog["checks"].append(dict(self.catalog["checks"][0], id="CERT-002",
                                            profiles=["car"], title="Car gate"))
        report = self.run_eval()
        self.assertEqual(report["coverage"]["required"], 4)
        self.assertEqual(report["readiness"], "INCOMPLETE")

    def test_duplicate_unknown_and_out_of_scope_results_are_rejected(self):
        for check_id in ("CERT-001", "CERT-999"):
            with self.subTest(check_id=check_id):
                evidence = copy.deepcopy(self.evidence)
                result = copy.deepcopy(evidence["results"][0])
                result["check_id"] = check_id
                evidence["results"].append(result)
                with self.assertRaises(ValueError):
                    evaluate(self.catalog, evidence, self.root)

    def test_wrong_catalog_version_rejected(self):
        self.evidence["catalog_version"] = "older"
        with self.assertRaises(ValueError):
            self.run_eval()

    def test_changed_scope_invalidates_results(self):
        self.evidence["scope"]["build_id"] = "different-build"
        self.assertEqual(self.run_eval()["readiness"], "INVALID_EVIDENCE")

    def test_artifact_tampering_is_detected(self):
        (self.root / "fixture.txt").write_text("Changed evidence", encoding="utf-8")
        self.assertEqual(self.run_eval()["readiness"], "INVALID_EVIDENCE")

    def test_missing_artifact_is_not_a_pass(self):
        self.evidence["results"][0]["artifacts"] = []
        self.assertEqual(self.run_eval()["readiness"], "INVALID_EVIDENCE")

    def test_path_traversal_is_rejected(self):
        self.evidence["results"][0]["artifacts"][0]["path"] = "../outside.txt"
        report = self.run_eval()
        self.assertEqual(report["readiness"], "INVALID_EVIDENCE")
        self.assertIn("escapes", report["checks"][0]["reason"])

    def test_wrong_method_and_absent_human_reviewer_are_invalid(self):
        self.evidence["results"][0]["method"] = "ui"
        self.evidence["results"][2].pop("reviewer")
        report = self.run_eval()
        self.assertEqual(report["checks"][0]["status"], "INVALID")
        self.assertEqual(report["checks"][2]["status"], "INVALID")

    def test_missing_cases_and_insufficient_samples_are_invalid(self):
        self.catalog["checks"][0]["cases"].append("case-b")
        self.catalog["checks"][1]["min_samples"] = 2
        report = self.run_eval()
        self.assertEqual(report["checks"][0]["status"], "INVALID")
        self.assertEqual(report["checks"][1]["status"], "INVALID")

    def test_boolean_nan_and_infinity_are_not_metrics(self):
        for value in (False, float("nan"), float("inf")):
            with self.subTest(value=value):
                self.evidence["results"][0]["value"] = value
                self.assertEqual(self.run_eval()["readiness"], "INVALID_EVIDENCE")

    def test_future_or_unzoned_timestamp_is_invalid(self):
        for value in ("2999-01-01T00:00:00Z", "2026-01-01T00:00:00"):
            self.evidence["results"][0]["observed_at"] = value
            self.assertEqual(self.run_eval()["readiness"], "INVALID_EVIDENCE")

    def test_cyclic_inheritance_and_bad_score_boundaries_rejected(self):
        self.catalog["profiles"]["core"]["extends"] = ["car"]
        with self.assertRaises(ValueError):
            self.run_eval()
        self.catalog["profiles"]["core"]["extends"] = []
        self.catalog["checks"][1]["target"] = 2000
        with self.assertRaises(ValueError):
            self.run_eval()

    def test_duplicate_json_keys_and_nonfinite_json_rejected(self):
        path = self.root / "invalid.json"
        for content in ('{"value": 1, "value": 2}', '{"value": NaN}'):
            path.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                load_json(path)

    def test_checked_in_example_is_incomplete_with_no_invented_score(self):
        root = Path(__file__).resolve().parents[1]
        catalog = load_json(root / "certification/catalog.json")
        evidence_path = root / "certification/evidence/not-tested.json"
        report = evaluate(catalog, load_json(evidence_path), evidence_path.parent)
        self.assertEqual(report["readiness"], "INCOMPLETE")
        self.assertEqual(report["coverage"]["evaluated"], 0)
        self.assertIsNone(report["provisional_quality_score"])
        self.assertEqual(report["certificate"], "NOT_ISSUED")

    def test_cli_outputs_json_and_markdown_and_exit_code(self):
        catalog_path, evidence_path = self.root / "catalog.json", self.root / "evidence.json"
        self.evidence["catalog_sha256"] = scope_hash(self.catalog)
        catalog_path.write_text(json.dumps(self.catalog), encoding="utf-8")
        evidence_path.write_text(json.dumps(self.evidence), encoding="utf-8")
        output = self.root / "out"
        with contextlib.redirect_stdout(io.StringIO()):
            code = main(["--catalog", str(catalog_path), "--evidence", str(evidence_path),
                         "--output-dir", str(output)])
        self.assertEqual(code, 0)
        self.assertEqual(load_json(output / "report.json")["certificate"], "NOT_ISSUED")
        self.assertIn("READY_FOR_REVIEW", (output / "report.md").read_text(encoding="utf-8"))

        evidence_path.write_text('{"broken":', encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            code = main(["--catalog", str(catalog_path), "--evidence", str(evidence_path),
                         "--output-dir", str(output)])
        self.assertEqual(code, 3)
        self.assertEqual(load_json(output / "report.json")["readiness"], "INVALID_INPUT")

    def test_exact_catalog_hash_mismatch_blocks_readiness(self):
        self.evidence["catalog_sha256"] = "0" * 64
        report = evaluate(self.catalog, self.evidence, self.root)
        self.assertEqual(report["readiness"], "INCOMPLETE")
        self.assertTrue(any("catalog content hash" in b for b in report["blockers"]))

    def test_cli_refuses_to_overwrite_its_input(self):
        evidence_path = self.root / "report.json"
        evidence_path.write_text(json.dumps(self.evidence), encoding="utf-8")
        original = evidence_path.read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            code = main(["--evidence", str(evidence_path), "--output-dir", str(self.root)])
        self.assertEqual(code, 3)
        self.assertEqual(evidence_path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()

"""Exercise missing-coverage and invalid-evidence boundaries, not app behavior."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools import harness


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.runtime = harness.load_json(harness.ROOT / "harness/runtime.json")

    def test_unconfigured_demo_is_blocked(self):
        report = harness.preflight(self.runtime, "demo")
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIn("adapters.voice_partner", report["missing"])
        self.assertIn("adapters.recorder", report["missing"])
        self.assertFalse(report["executed"])

    def test_verify_does_not_require_demo_recording(self):
        report = harness.preflight(self.runtime, "verify")
        self.assertNotIn("adapters.recorder", report["missing"])
        self.assertNotIn("recording.consent_confirmed", report["missing"])

    def test_configured_is_not_executed_or_certified(self):
        for key in self.runtime["application"]:
            self.runtime["application"][key] = "fixture-only"
        for key in ("situations", "devices", "audio_routes"):
            self.runtime["scope"][key] = ["fixture-only"]
        self.runtime["scope"].update(language_pairs=[["en", "nb"]], fixture_revision="test", processing_revision="test")
        for key in self.runtime["adapters"]:
            self.runtime["adapters"][key] = "test adapter descriptor"
        self.runtime["recording"].update(purpose="synthetic test", storage_directory="test", retention_policy="test", consent_confirmed=True)
        self.runtime["cost_limit"] = "0 USD local-only"
        report = harness.preflight(self.runtime, "demo")
        self.assertEqual(report["status"], "CONFIGURED_UNVERIFIED")
        self.assertFalse(report["executed"])
        self.assertEqual(report["certificate"], "NOT_ISSUED")

    def test_invalid_runtime_types_rejected(self):
        for key, value in (("schema_version", True), ("scope", []), ("cost_limit", True)):
            with self.subTest(key=key):
                data = copy.deepcopy(self.runtime)
                data[key] = value
                with self.assertRaises(ValueError):
                    harness.preflight(data, "demo")

    def test_duplicate_languages_and_string_consent_rejected(self):
        self.runtime["scope"]["language_pairs"] = [["en", "en"]]
        with self.assertRaises(ValueError):
            harness.preflight(self.runtime, "demo")
        self.runtime["scope"]["language_pairs"] = []
        self.runtime["recording"]["consent_confirmed"] = "true"
        with self.assertRaises(ValueError):
            harness.preflight(self.runtime, "demo")

    def test_duplicate_json_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime.json"
            path.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
            with self.assertRaises(ValueError):
                harness.load_json(path)

    def test_links_find_missing_files_anchors_and_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "README.md"
            target = root / "target.md"
            target.write_text("# Heading\n\n## Heading\n", encoding="utf-8")
            source.write_text("[ok](target.md#heading-1)", encoding="utf-8")
            self.assertEqual(harness.check_links(root, [source]), 1)
            for link in ("target.md#missing", "missing.md", "../escape.md"):
                source.write_text(f"[bad]({link})", encoding="utf-8")
                with self.assertRaises(ValueError):
                    harness.check_links(root, [source])

    def test_links_in_code_are_not_document_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "README.md"
            source.write_text("```md\n[example](missing.md)\n```\n", encoding="utf-8")
            self.assertEqual(harness.check_links(root, [source]), 0)

    def test_plan_never_reports_tested_product(self):
        result = harness.coverage_report(harness.ROOT)
        self.assertEqual(result["status"], "PLANNED_ONLY")
        self.assertEqual(result["product_execution"], "NOT_ASSESSED")
        self.assertEqual(result["certificate"], "NOT_ISSUED")
        self.assertIn("SIT-005", result["catalog_only"])

    def test_missing_requirement_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "spec/requirements").mkdir(parents=True)
            (root / "harness").mkdir()
            (root / "spec/requirements/functional.md").write_text("## FR-001 — Required\n", encoding="utf-8")
            data = {"schema_version": 1, "status": "planned", "requirements": {}}
            (root / "harness/coverage.json").write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "mapping mismatch"):
                harness.coverage_report(root)

    def test_duplicate_requirement_definition_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "spec/requirements"
            folder.mkdir(parents=True)
            (folder / "functional.md").write_text("## FR-001 — One\n## FR-001 — Two\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate requirement"):
                harness.requirement_definitions(root)


if __name__ == "__main__":
    unittest.main()

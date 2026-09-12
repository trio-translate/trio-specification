"""Fault controls for real producer evidence; no product certification claims."""

import copy
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools.execution import assess_execution, compare_benchmarks, expiry, write_manifest
from tools.harness import main


def execution():
    return {
        "schema_version": 1,
        "app_commit": "a" * 40,
        "spec_commit": "b" * 40,
        "plan_sha256": "c" * 64,
        "adapter": "test-producer.v1",
        "required_tests": ["Suite/one", "Suite/two"],
        "tests": [{"id": "Suite/one", "status": "passed"},
                  {"id": "Suite/two", "status": "passed"}],
        "producer_status": "passed",
        "complete": True,
        "elapsed_seconds": 1.5,
    }


class ExecutionTests(unittest.TestCase):
    def test_cli_exits_nonzero_for_an_omitted_test_and_zero_only_for_execution(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "manifest.json"
            data = execution()
            for expected in (0, 3):
                path.write_text(json.dumps({"execution": data}))
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    code = main(["analyze", "--evidence", str(path)])
                self.assertEqual(expected, code)
                self.assertEqual("NOT_ISSUED", json.loads(output.getvalue())["certificate"])
                data["tests"].pop()

    def test_pass_requires_both_expected_observations(self):
        self.assertEqual("passed", assess_execution(execution())["status"])
        evidence = execution()
        evidence["tests"].pop()
        result = assess_execution(evidence)
        self.assertEqual("invalid", result["status"])
        self.assertEqual(["Suite/two"], result["missing_required"])

    def test_missing_skipped_inconclusive_and_zero_never_pass(self):
        for status in ("skipped", "unavailable", "inconclusive"):
            with self.subTest(status=status):
                evidence = execution()
                evidence["tests"][0]["status"] = status
                self.assertEqual("blocked", assess_execution(evidence)["status"])
        evidence = execution()
        evidence["tests"] = []
        self.assertEqual("invalid", assess_execution(evidence)["status"])

    def test_failure_is_retained_alongside_missing_evidence(self):
        evidence = execution()
        evidence["tests"] = [{"id": "Suite/one", "status": "failed"}]
        result = assess_execution(evidence)
        self.assertEqual("failed", result["status"])
        self.assertEqual(["Suite/one"], result["failed_tests"])
        self.assertEqual(["Suite/two"], result["missing_required"])

    def test_duplicate_unknown_status_and_forged_revision_are_invalid(self):
        for key, value in (("tests", [execution()["tests"][0]] * 2),
                           ("tests", [{"id": "Suite/one", "status": "green"}]),
                           ("app_commit", "main"), ("schema_version", True),
                           ("elapsed_seconds", float("nan"))):
            with self.subTest(key=key):
                evidence = execution()
                evidence[key] = value
                with self.assertRaises(ValueError):
                    assess_execution(evidence)

    def test_no_completion_witness_or_failed_producer_cannot_pass(self):
        evidence = execution()
        evidence["complete"] = False
        self.assertEqual("invalid", assess_execution(evidence)["status"])
        evidence = execution()
        evidence["producer_status"] = "invalid"
        self.assertEqual("invalid", assess_execution(evidence)["status"])
        evidence["producer_status"] = "failed"
        self.assertEqual("failed", assess_execution(evidence)["status"])

    def test_expiry_uses_capture_time_and_shortest_source_retention(self):
        captured = "2026-01-01T00:00:00Z"
        self.assertEqual("2026-01-31T00:00:00Z", expiry(captured, "metadata"))
        self.assertEqual("2026-01-08T00:00:00Z", expiry(captured, "sensitive"))
        self.assertEqual("2026-01-03T00:00:00Z",
                         expiry(captured, "metadata", ["2026-01-03T00:00:00Z"]))
        for value in ("2026-01-01", "yesterday"):
            with self.assertRaises(ValueError):
                expiry(value, "metadata")

    def test_manifest_cannot_overwrite_failed_run_or_follow_a_link(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root) / "manifest.json"
            first = {"execution": execution()}
            first["execution"]["tests"][0]["status"] = "failed"
            write_manifest(target, first)
            original = target.read_bytes()
            with self.assertRaises(FileExistsError):
                write_manifest(target, {"execution": execution()})
            self.assertEqual(original, target.read_bytes())
            link = Path(root) / "link.json"
            link.symlink_to(target)
            with self.assertRaises(FileExistsError):
                write_manifest(link, {"execution": execution()})
            self.assertEqual(original, target.read_bytes())


def benchmark():
    return {
        "schema_version": 1, "protocol_sha256": "d" * 64,
        "weights": {"core": 1, "ui": 1, "adapter": 1},
        "pairs": [
            {"lane": lane, "pair": i, "condition_sha256": "e" * 64,
             "baseline": {"seconds": 100.0, "status": "passed", "assertions_sha256": "f" * 64},
             "candidate": {"seconds": 40.0, "status": "passed", "assertions_sha256": "f" * 64}}
            for lane in ("core", "ui", "adapter", "clean") for i in range(5)
        ],
    }


class BenchmarkTests(unittest.TestCase):
    def test_exact_thresholds_and_weighted_duration_totals(self):
        data = benchmark()
        for row in data["pairs"]:
            row["candidate"]["seconds"] = 110.0 if row["lane"] == "clean" else 50.0
        self.assertEqual("numeric_gates_met", compare_benchmarks(data)["status"])
        data["weights"] = {"core": 3, "ui": 1, "adapter": 2}
        for row in data["pairs"]:
            if row["lane"] == "core":
                row["baseline"]["seconds"], row["candidate"]["seconds"] = 200, 40
            elif row["lane"] == "ui":
                row["baseline"]["seconds"], row["candidate"]["seconds"] = 10, 10
        result = compare_benchmarks(data)
        self.assertAlmostEqual((3 * 40 + 10 + 2 * 50) / (3 * 200 + 10 + 2 * 100),
                               result["aggregate_ratio"])
        self.assertEqual("numeric_gates_met", result["status"])

    def test_matched_pairs_meet_numeric_gates_without_certifying(self):
        result = compare_benchmarks(benchmark())
        self.assertEqual("numeric_gates_met", result["status"])
        self.assertAlmostEqual(0.4, result["aggregate_ratio"])
        self.assertFalse(result["foundation_qualified"])

    def test_one_regressed_lane_blocks_even_when_aggregate_is_fast(self):
        data = benchmark()
        for row in data["pairs"]:
            if row["lane"] == "core":
                row["candidate"]["seconds"] = 111.0
            elif row["lane"] != "clean":
                row["candidate"]["seconds"] = 1.0
        self.assertEqual("failed", compare_benchmarks(data)["status"])

    def test_failure_is_not_removed_from_the_comparison(self):
        data = benchmark()
        data["pairs"][0]["candidate"]["status"] = "failed"
        result = compare_benchmarks(data)
        self.assertEqual("invalid", result["status"])
        self.assertIsNone(result["aggregate_ratio"])

    def test_missing_pairs_assertion_drift_or_missing_clean_is_invalid(self):
        original = benchmark()
        mutations = [lambda d: d["pairs"].pop(),
                     lambda d: d["pairs"][0]["candidate"].update(assertions_sha256="a" * 64),
                     lambda d: d.update(pairs=[r for r in d["pairs"] if r["lane"] != "clean"])]
        for mutate in mutations:
            data = copy.deepcopy(original)
            mutate(data)
            self.assertEqual("invalid", compare_benchmarks(data)["status"])

    def test_duplicate_pair_and_nonpositive_weights_are_rejected(self):
        data = benchmark()
        data["pairs"].append(copy.deepcopy(data["pairs"][0]))
        with self.assertRaises(ValueError):
            compare_benchmarks(data)
        data = benchmark()
        data["weights"]["core"] = 0
        with self.assertRaises(ValueError):
            compare_benchmarks(data)


if __name__ == "__main__":
    unittest.main()

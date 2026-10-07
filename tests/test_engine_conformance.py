"""Executable seed conformance checks for proposed DEC-011 semantics."""

import unittest

from tools import engine_conformance as conformance


class EngineConformanceTests(unittest.TestCase):
    def fixture(self, name):
        return conformance.FIXTURES / name

    def test_seed_fixtures_match_expected_state_deterministically(self):
        for fixture in sorted(conformance.FIXTURES.glob("*.jsonl")):
            with self.subTest(fixture=fixture.name):
                result = conformance.check_fixture(fixture)
                self.assertEqual(result["status"], "PASS")

    def test_duplicate_delivery_is_idempotent(self):
        events = conformance.load_jsonl(self.fixture("duplicate-delivery.jsonl"))
        reducer = conformance.SeedReducer()
        reducer.deliver(events[0])
        reducer.deliver(events[1])
        before = reducer.semantic_state()
        self.assertEqual(reducer.deliver(events[2]), "duplicate")
        self.assertEqual(reducer.semantic_state(), before)

    def test_gap_is_not_applied_speculatively(self):
        events = conformance.load_jsonl(self.fixture("gap-recovery.jsonl"))
        reducer = conformance.SeedReducer()
        reducer.deliver(events[0])
        before = reducer.semantic_state()
        self.assertEqual(reducer.deliver(events[1]), "gap")
        self.assertEqual(reducer.semantic_state(), before)

    def test_late_output_after_cancellation_is_not_visible(self):
        state, _ = conformance.replay(self.fixture("cancellation-late-output.jsonl"))
        turn = state["turns"]["turn-cancel"]
        self.assertEqual(turn["status"], "canceled")
        self.assertIsNone(turn["translation"])


if __name__ == "__main__":
    unittest.main()

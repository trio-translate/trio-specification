"""Executable seed conformance checks for proposed DEC-011 semantics."""

from copy import deepcopy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "spec/technical/engine/fixtures"


def load_jsonl(name):
    return [
        json.loads(line)
        for line in (FIXTURES / name).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def expected(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class SeedReducer:
    """Test-only semantic projection of behavior already stated by DEC-011."""

    def __init__(self):
        self.session_id = None
        self.sequence = 0
        self.event_ids = set()
        self.turns = {}

    def deliver(self, event):
        if event["eventId"] in self.event_ids:
            return "duplicate"
        if event["sequence"] > self.sequence + 1:
            return "gap"
        if event["sequence"] <= self.sequence:
            raise ValueError("different event reused an applied sequence")

        if self.session_id is None:
            if event["type"] != "session.started":
                raise ValueError("first canonical event must start the session")
            self.session_id = event["sessionId"]
        elif event["sessionId"] != self.session_id:
            raise ValueError("event moved across logical sessions")

        self._reduce(event)
        self.event_ids.add(event["eventId"])
        self.sequence = event["sequence"]
        return "applied"

    def _turn(self, event):
        return self.turns[event["turnId"]]

    def _current(self, turn, event):
        return (
            turn["operationId"] == event.get("operationId")
            and turn["revision"] == event.get("revision")
        )

    def _reduce(self, event):
        kind = event["type"]
        if kind == "session.started":
            return
        if kind == "turn.accepted":
            self.turns[event["turnId"]] = {
                "operationId": event["operationId"],
                "participantId": event["participantId"],
                "revision": event["revision"],
                "status": "active",
                "recognition": None,
                "translation": None,
            }
            return

        turn = self._turn(event)
        if not self._current(turn, event):
            return
        if kind == "turn.canceled":
            turn["status"] = "canceled"
        elif kind == "turn.completed" and turn["status"] != "canceled":
            turn["status"] = "completed"
        elif kind in {"recognition.finalized", "translation.finalized"} and turn["status"] != "canceled":
            field = "recognition" if kind == "recognition.finalized" else "translation"
            turn[field] = deepcopy(event["payload"])
        else:
            if kind not in {"turn.completed", "recognition.finalized", "translation.finalized"}:
                raise ValueError(f"event outside seed gate: {kind}")

    def state(self):
        return {
            "schemaVersion": 1,
            "sessionId": self.session_id,
            "lastAppliedSequence": self.sequence,
            "turns": deepcopy(self.turns),
        }


def replay(name):
    reducer = SeedReducer()
    delivery = []
    for event in load_jsonl(name):
        delivery.append(reducer.deliver(event))
    return reducer.state(), delivery


class EngineConformanceTests(unittest.TestCase):
    CASES = (
        "basic-turn",
        "duplicate-delivery",
        "gap-recovery",
        "cancellation-late-output",
    )

    def test_seed_replays_match_expected_state_deterministically(self):
        for case in self.CASES:
            with self.subTest(case=case):
                first, _ = replay(f"{case}.jsonl")
                second, _ = replay(f"{case}.jsonl")
                self.assertEqual(first, expected(f"{case}.expected.json"))
                self.assertEqual(second, first)

    def test_duplicate_delivery_is_idempotent(self):
        events = load_jsonl("duplicate-delivery.jsonl")
        reducer = SeedReducer()
        reducer.deliver(events[0])
        reducer.deliver(events[1])
        before = reducer.state()
        self.assertEqual(reducer.deliver(events[2]), "duplicate")
        self.assertEqual(reducer.state(), before)

    def test_gap_is_not_applied_speculatively(self):
        events = load_jsonl("gap-recovery.jsonl")
        reducer = SeedReducer()
        reducer.deliver(events[0])
        before = reducer.state()
        self.assertEqual(reducer.deliver(events[1]), "gap")
        self.assertEqual(reducer.state(), before)

    def test_late_output_after_cancellation_is_not_visible(self):
        state, _ = replay("cancellation-late-output.jsonl")
        turn = state["turns"]["turn-cancel"]
        self.assertEqual(turn["status"], "canceled")
        self.assertIsNone(turn["translation"])


if __name__ == "__main__":
    unittest.main()

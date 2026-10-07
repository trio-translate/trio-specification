"""Replay the intentionally small DEC-011 seed conformance corpus.

This is a proposal-validation reference, not a complete Trio engine implementation.
It asserts only reducer behavior already stated in the proposed contract.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "spec/technical/engine/fixtures"

_REQUIRED = {
    "schemaVersion",
    "eventId",
    "sessionId",
    "sequence",
    "type",
    "occurredAt",
    "producer",
    "payload",
}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def load_json(path):
    def reject_duplicate(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate)


def load_jsonl(path):
    events = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
        _require(isinstance(event, dict), f"{path}:{line_number}: event must be an object")
        events.append(event)
    _require(events, f"{path}: fixture is empty")
    return events


class SeedReducer:
    """Minimal semantic projection for the settled DEC-011 seed invariants."""

    def __init__(self):
        self.session_id = None
        self.last_applied_sequence = 0
        self._applied_event_ids = set()
        self._turns = {}

    def deliver(self, event):
        missing = sorted(_REQUIRED - set(event))
        _require(not missing, f"Missing envelope fields: {missing}")
        _require(event["schemaVersion"] == 1, "Seed gate supports schemaVersion 1 only")
        _require(type(event["sequence"]) is int and event["sequence"] >= 1, "Invalid sequence")
        _require(isinstance(event["eventId"], str) and event["eventId"], "Invalid eventId")
        _require(isinstance(event["sessionId"], str) and event["sessionId"], "Invalid sessionId")
        _require(isinstance(event["type"], str) and event["type"], "Invalid event type")
        _require(isinstance(event["payload"], dict), "payload must be an object")

        if event["eventId"] in self._applied_event_ids:
            return "duplicate"

        expected = self.last_applied_sequence + 1
        if event["sequence"] > expected:
            # DEC-011 permits buffering OR rejection. The seed evaluator chooses
            # rejection/defer and relies on later redelivery; no semantic mutation
            # is permitted while the canonical sequence has a gap.
            return "gap"

        if event["sequence"] < expected:
            raise ValueError(
                f"Sequence {event['sequence']} was already applied by a different event"
            )

        if self.session_id is None:
            _require(event["type"] == "session.started", "First canonical event must start the session")
            self.session_id = event["sessionId"]
        else:
            _require(event["sessionId"] == self.session_id, "Event moved across logical sessions")

        self._reduce(event)
        self._applied_event_ids.add(event["eventId"])
        self.last_applied_sequence = event["sequence"]
        return "applied"

    def _turn_for(self, event):
        turn_id = event.get("turnId")
        _require(isinstance(turn_id, str) and turn_id, f"{event['type']} requires turnId")
        _require(turn_id in self._turns, f"Unknown turn: {turn_id}")
        return self._turns[turn_id]

    def _same_operation_revision(self, turn, event):
        return (
            event.get("operationId") == turn["operationId"]
            and event.get("revision") == turn["revision"]
        )

    def _reduce(self, event):
        event_type = event["type"]

        if event_type == "session.started":
            return

        if event_type == "turn.accepted":
            turn_id = event.get("turnId")
            _require(isinstance(turn_id, str) and turn_id, "turn.accepted requires turnId")
            _require(turn_id not in self._turns, f"Turn already exists: {turn_id}")
            for field in ("operationId", "participantId"):
                _require(isinstance(event.get(field), str) and event[field], f"turn.accepted requires {field}")
            _require(type(event.get("revision")) is int and event["revision"] >= 0, "turn.accepted requires revision")
            self._turns[turn_id] = {
                "operationId": event["operationId"],
                "participantId": event["participantId"],
                "revision": event["revision"],
                "status": "active",
                "recognition": None,
                "translation": None,
            }
            return

        if event_type in {"recognition.finalized", "translation.finalized"}:
            turn = self._turn_for(event)
            if not self._same_operation_revision(turn, event) or turn["status"] == "canceled":
                return
            target = "recognition" if event_type == "recognition.finalized" else "translation"
            turn[target] = deepcopy(event["payload"])
            return

        if event_type == "turn.canceled":
            turn = self._turn_for(event)
            if self._same_operation_revision(turn, event):
                turn["status"] = "canceled"
            return

        if event_type == "turn.completed":
            turn = self._turn_for(event)
            if self._same_operation_revision(turn, event) and turn["status"] != "canceled":
                turn["status"] = "completed"
            return

        raise ValueError(f"Event type is outside the seed conformance gate: {event_type}")

    def semantic_state(self):
        return {
            "schemaVersion": 1,
            "sessionId": self.session_id,
            "lastAppliedSequence": self.last_applied_sequence,
            "turns": deepcopy(self._turns),
        }


def replay(path):
    reducer = SeedReducer()
    delivery = []
    for event in load_jsonl(path):
        delivery.append({"eventId": event["eventId"], "result": reducer.deliver(event)})
    return reducer.semantic_state(), delivery


def expected_path(fixture):
    return fixture.with_suffix(".expected.json")


def check_fixture(fixture):
    expected_file = expected_path(fixture)
    _require(expected_file.is_file(), f"Missing expected state: {expected_file}")
    expected = load_json(expected_file)
    actual, delivery = replay(fixture)
    _require(actual == expected, f"Semantic state mismatch for {fixture.name}")
    second, _ = replay(fixture)
    _require(second == actual, f"Non-deterministic replay for {fixture.name}")
    return {"fixture": fixture.name, "status": "PASS", "delivery": delivery}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixtures", nargs="*", type=Path)
    args = parser.parse_args(argv)
    fixtures = args.fixtures or sorted(FIXTURES.glob("*.jsonl"))
    try:
        results = [check_fixture(path if path.is_absolute() else ROOT / path) for path in fixtures]
        print(json.dumps({"status": "PASS", "fixtures": results}, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

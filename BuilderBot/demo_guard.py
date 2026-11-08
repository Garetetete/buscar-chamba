"""Loom demo: what the numeric guard does when the model invents a figure.

Runs offline against a local clone of manukora-sop-briefing. A scripted
stand-in plays the model, so each of the guard's three outcomes can be shown
on demand without an API key.

    python demo_guard.py            # all three scenarios
    python demo_guard.py liar       # just one: honest | self-corrects | liar
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

REPO = Path(os.environ.get("SOP_REPO", Path(__file__).resolve().parents[2] / "manukora-sop-briefing"))
sys.path.insert(0, str(REPO))

from sop.loader import load_extract  # noqa: E402
from sop.narrative import (  # noqa: E402
    allowed_numbers,
    build_facts,
    find_unsupported_numbers,
    generate_briefing,
)

GOOD = "Order 650 units of MGO 514+ 500g by April 2026, with $34,316 a month at stake."
BAD = "Revenue at stake is $52,000 a month, so order 1,250 units."

SCENARIOS = {
    "honest": ("The model sticks to the facts", [GOOD]),
    "self-corrects": ("The model invents a number once, then fixes it", [BAD, GOOD]),
    "liar": ("The model keeps inventing numbers", [BAD, BAD]),
}


class ScriptedModel:
    """Plays the model: returns the replies it was given, in order."""

    name = "scripted model"

    def __init__(self, replies: list[str]) -> None:
        self.replies = list(replies)
        self.calls = 0

    def generate(self, facts, prompt):
        self.calls += 1
        reply = self.replies.pop(0)
        print(f"  attempt {self.calls} - model wrote: \"{reply}\"")
        time.sleep(0.6)
        invented = find_unsupported_numbers(reply, allowed_numbers(facts))
        if invented:
            print(f"  guard: REJECTED - {', '.join(invented)} not in the computed facts")
        else:
            print("  guard: ok - every figure traces to a computed fact")
        time.sleep(0.6)
        return reply


def run(key: str, facts) -> None:
    title, replies = SCENARIOS[key]
    print(f"\n=== {title} ===")
    text, source, warnings = generate_briefing(facts, provider=ScriptedModel(replies))
    if any("kept inventing" in w for w in warnings):
        print("  guard: retry failed too - not shipping a wrong briefing")
    verdict = "shipped the model's text" if source != "template" else "fell back to the deterministic template"
    print(f"  result: {verdict} ({len(text.splitlines())} lines)")


def main() -> int:
    os.chdir(REPO)
    facts = build_facts(load_extract(Path("data/mock_sales.csv")))
    keys = sys.argv[1:] or list(SCENARIOS)
    for key in keys:
        if key not in SCENARIOS:
            print(f"unknown scenario {key!r}; choose from {', '.join(SCENARIOS)}")
            return 2
        run(key, facts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

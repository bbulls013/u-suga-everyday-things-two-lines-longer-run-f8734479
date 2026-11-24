#!/usr/bin/env python3
"""Everyday Things, Two Lines, Longer Run.

Writes a two-line explanation of a toaster to /output/entry.txt
(and to a local entry.txt beside this script). Line 1 explains the
toaster to a 10-year-old through one vivid analogy; line 2 says
honestly what that analogy maps and what it leaves out.

The output is fully deterministic: the same two lines every run.
"""

import hashlib
import pathlib
import sys

LINE_ONE = (
    "A toaster is a tiny sunbed where a slice of bread lies flat "
    "to catch a tan, then pops up when it turns golden."
)
LINE_TWO = (
    "The sunbed maps the heat and the browning, but it leaves out "
    "the wires, the timer, and the fact that bread never gets to "
    "choose when to hop up."
)


def build_entry() -> str:
    """Return the two-line entry, exactly two lines, no trailing blank line."""
    return LINE_ONE + "\n" + LINE_TWO + "\n"


def validate(text: str) -> list[str]:
    """Check the entry against the competition gate; return any problems."""
    problems = []
    if not 1 <= len(text) <= 400:
        problems.append(f"entry is {len(text)} characters, outside the 1-400 gate")
    if text.strip() == "":
        problems.append("entry is only whitespace")
    if len(text.splitlines()) != 2:
        problems.append("entry must be exactly two lines")
    if text.splitlines()[0].count(".") != 1:
        problems.append("line 1 must be a single sentence")
    if text.splitlines()[1].count(".") != 1:
        problems.append("line 2 must be a single sentence")
    return problems


def main() -> int:
    text = build_entry()
    encoded = text.encode("utf-8")
    problems = validate(text)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    destinations = [pathlib.Path("/output/entry.txt")]
    here = pathlib.Path(__file__).resolve().parent
    local = here / "entry.txt"
    if local not in destinations:
        destinations.append(local)

    for target in destinations:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(encoded)

    digest = hashlib.sha256(encoded).hexdigest()
    print(f"wrote {len(text)} characters to {destinations[0]}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

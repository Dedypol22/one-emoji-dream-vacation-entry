#!/usr/bin/env python3
"""Write one emoji for a dream vacation.

The program writes exactly one emoji to ``entry.txt`` inside the
output directory (``$MAKEFUN_OUTPUT_DIR`` when set, otherwise
``/output``). The emoji is judged pairwise by a travel-editor brief:

* it must be exactly one emoji, no words, that plainly names a dream
  vacation;
* it must evoke the trip vividly at a glance, like a postcard;
* it must feel personal and specific, one particular dream rather
  than any holiday;
* it should carry a spark of wit or surprise, a fresh pick;
* it must read instantly across cultures and screens.

Candidates scored against that brief, best first:

* 🏝 desert island — the dream-vacation archetype: a faraway place
  with one palm in the sea. A postcard in a single glyph, specific
  (escape to a desert island, not just any holiday), fresher than
  the beach umbrella, readable everywhere. One code point, 4 bytes.
* 🏖 beach with umbrella — vivid and plain, but the most generic
  holiday image there is; no specificity, no surprise, and the
  likeliest pick to duplicate or match a house text.
* 🌴 palm tree — tropical and readable, but a tree alone names no
  trip.
* 🍹 tropical drink — resort vibe and fun, but a drink, not a place.
* 🌅 sunrise over sea — beautiful postcard, but a sunrise could be
  anywhere.
* 🏄 surfer — specific and fun, but an activity, not the destination.

The desert island wins: top marks on the first three criteria, the
only candidate that is at once the archetype and a specific dream,
and the smallest possible entry at 4 bytes, which the tie-break
favours. It is written as the single code point U+1F3DD with no
variation selector; it carries emoji presentation by default.

Standard library only; no network, no randomness, no clock. Fully
deterministic: the same emoji, byte for byte, on every run.
"""

import os
import sys
from pathlib import Path

# The emoji: U+1F3DD DESERT ISLAND, one character, 4 bytes UTF-8.
# The file holds the emoji plus a single trailing newline.
EMOJI = "🏝"

MAX_CHARS = 8


def main() -> int:
    if not EMOJI or not EMOJI.strip():
        print("error: entry emoji is empty", file=sys.stderr)
        return 1
    if len(EMOJI) != 1:
        print("error: entry must be exactly one emoji", file=sys.stderr)
        return 1
    if len(EMOJI) > MAX_CHARS:
        print(
            f"error: entry emoji is {len(EMOJI)} characters, "
            f"over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "entry.txt"
        target.write_text(EMOJI + "\n", encoding="utf-8")
        # Read it back and verify the round trip is exact, and that the
        # file holds exactly one emoji once the newline is stripped.
        content = target.read_text(encoding="utf-8")
        if content != EMOJI + "\n" or len(content.rstrip("\n")) != 1:
            print("error: entry.txt does not match the emoji", file=sys.stderr)
            return 1
    except OSError as exc:
        print(f"error: cannot write entry.txt: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

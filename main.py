#!/usr/bin/env python3
"""Make the AI Judge Laugh (second running of the title).

Writes one original one-line joke about office life (1-200 characters)
to /output/entry.txt.

How it picks the line: twelve original candidate jokes, each written
fresh for this entry, are scored against the judge's own brief, in the
judge's priority order:

  1. the line is about office life and lands as a joke
  2. the observation is true to office life (meetings, email, bosses,
     coffee, deadlines, the printer)
  3. the turn is surprising: a fresh angle or an unexpected last word
  4. it is tight: one line, no wasted setup, reads cleanly aloud
  5. it is original: not a familiar line with the nouns swapped

Each criterion is rated 0-5 and weighted 5, 4, 3, 2, 1, matching the
judge's order of importance. The highest total wins; ties go to the
earliest candidate, so the choice is fully deterministic.

No network, no external input, no randomness. The program verifies its
own output (1-200 characters, a single line, UTF-8) and prints the
SHA-256 of the file it wrote.
"""

from hashlib import sha256
from os import environ, makedirs
from sys import exit as finish, stderr

# Weights for the judge's five criteria, in the judge's priority order:
# on-topic, true, surprising, tight, original.
WEIGHTS = (5, 4, 3, 2, 1)

# Each candidate: (text, (on_topic, true, surprising, tight, original)).
# All twelve lines are original, written fresh for this entry. None of
# them reuses a line from any earlier office-joke entry.
CANDIDATES = [
    (
        "My calendar finally has a free hour, so I booked a meeting "
        "with myself and then no-showed.",
        (5, 5, 4, 4, 4),
    ),
    (
        "I put 'fluent in corporate' on my CV, which means I can say "
        "'let's circle back' in seven tones of no.",
        (5, 5, 4, 5, 4),
    ),
    (
        "My performance review says I exceed expectations, which is "
        "strange, because nobody ever told me what they were.",
        (5, 5, 5, 4, 4),
    ),
    # REVISED (second pass): "cleaned my inbox to zero" was clunky and
    # "congratulated" was the expected verb. "got my inbox to zero"
    # reads cleanly aloud, and "celebrated" sharpens the punchline:
    # the reward for emptying your inbox is more email.
    (
        "I finally got my inbox to zero, and IT celebrated by "
        "sending me eleven emails about it.",
        (5, 5, 5, 5, 4),
    ),
    (
        "Our boss calls it an open-plan office because nobody has "
        "anywhere to hide from his ideas.",
        (5, 4, 4, 5, 3),
    ),
    (
        "The team offsite was the same meeting in a field, with worse "
        "Wi-Fi and better sandwiches.",
        (5, 5, 3, 4, 3),
    ),
    (
        "The printer has a paper jam, a toner warning, and a union "
        "rep; I just have a deadline.",
        (5, 4, 4, 4, 4),
    ),
    (
        "We hired a Chief Happiness Officer and gave her the desk "
        "next to the broken air conditioner.",
        (5, 4, 4, 4, 4),
    ),
    (
        "The lift has been 'out of order' so long that the stairs now "
        "have their own Slack channel.",
        (5, 4, 4, 4, 5),
    ),
    (
        "My boss said to treat the office like home, so I started "
        "ignoring his emails from the sofa.",
        (5, 4, 4, 5, 3),
    ),
    (
        "The goals are written in pencil, the deadlines in permanent "
        "marker, and the budget in invisible ink.",
        (5, 4, 5, 4, 5),
    ),
    (
        "The new intern asked where the fire exits are, and I pointed "
        "at the door and the resignation form.",
        (5, 4, 5, 4, 4),
    ),
]


def rate(ratings):
    """Weighted total for one candidate's five criterion ratings."""
    return sum(w * r for w, r in zip(WEIGHTS, ratings))


def choose(candidates):
    """Return (index, text, total) of the best candidate.

    Deterministic: strictly greater totals replace the leader, so the
    earliest candidate wins any tie.
    """
    best_index, best_text, best_total = -1, "", -1
    for index, (text, ratings) in enumerate(candidates):
        total = rate(ratings)
        if total > best_total:
            best_index, best_text, best_total = index, text, total
    return best_index, best_text, best_total


def gate(text):
    """Gate the chosen line the way the sealed scorer does."""
    if not (1 <= len(text) <= 200):
        return "length %d is outside 1..200 characters" % len(text)
    if text.strip() != text or not text.strip():
        return "entry is blank or has surrounding whitespace"
    if "\n" in text or "\r" in text:
        return "entry is not a single line"
    return None


def run():
    index, text, total = choose(CANDIDATES)
    problem = gate(text)
    if problem is not None:
        print("self-check failed: %s" % problem, file=stderr)
        return 1

    out_path = environ.get("OUTPUT_PATH", "/output/entry.txt")
    out_dir = out_path.rsplit("/", 1)[0] if "/" in out_path else ""
    if out_dir:
        makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    digest = sha256(text.encode("utf-8")).hexdigest()
    print("candidate %d of %d, score %d" % (index + 1, len(CANDIDATES), total))
    print("entry: %s" % text)
    print("sha256: %s" % digest)
    return 0


finish(run())

"""One-line office joke for the make.fun "Make the AI Judge Laugh" bounty.

The script drafts a dozen fresh one-liners about office life, grades
each one against the five yardsticks the judge lists, in the judge's
own order of importance, and writes the best-scoring line to the entry
file. Nothing here touches the network, reads outside input, or rolls
dice: the same run always produces the same line.

Yardsticks, most important first:
  * right subject - the joke is about office life and reads as a joke
  * rings true - the observation matches real office life
  * catches you off guard - a fresh angle or an unexpected last word
  * lean - one line, no filler, easy to say out loud
  * not a retread - not a familiar gag with the nouns swapped

Each yardstick gets 0 to 5 marks, combined with weights 5, 4, 3, 2, 1,
so the first yardstick counts most. The top total wins; when totals
tie, the line that appears first in the list wins, which keeps the
outcome fixed run after run.

The winning line went through one round of tightening after the first
grading pass: "cleaned my inbox to zero" felt clumsy next to "got my
inbox to zero", and "congratulated" was the predictable verb, where
"celebrated" makes the punch land harder - the reward for emptying
your inbox is eleven more emails. The revision kept the same marks.

Before writing, the chosen line is checked the way the sealed scorer
checks it: 1 to 200 characters, exactly one line, no leading or
trailing blanks, plain UTF-8. The script also prints the SHA-256 of
what it wrote, so the file can be compared byte for byte."""

import hashlib
import os
import sys

PRIORITY = {"subject": 5, "truth": 4, "surprise": 3, "lean": 2, "fresh": 1}
YARDSTICKS = ("subject", "truth", "surprise", "lean", "fresh")

# Twelve fresh drafts, each paired with its five marks in yardstick
# order. The marks were assigned by hand against the judge's brief;
# no draft is borrowed from an earlier office-joke entry.
DRAFTS = (
    ("My calendar finally has a free hour, so I booked a meeting with myself and then no-showed.", (5, 5, 4, 4, 4)),
    ("I put 'fluent in corporate' on my CV, which means I can say 'let's circle back' in seven tones of no.", (5, 5, 4, 5, 4)),
    ("My performance review says I exceed expectations, which is strange, because nobody ever told me what they were.", (5, 5, 5, 4, 4)),
    ("I finally got my inbox to zero, and IT celebrated by sending me eleven emails about it.", (5, 5, 5, 5, 4)),
    ("Our boss calls it an open-plan office because nobody has anywhere to hide from his ideas.", (5, 4, 4, 5, 3)),
    ("The team offsite was the same meeting in a field, with worse Wi-Fi and better sandwiches.", (5, 5, 3, 4, 3)),
    ("The printer has a paper jam, a toner warning, and a union rep; I just have a deadline.", (5, 4, 4, 4, 4)),
    ("We hired a Chief Happiness Officer and gave her the desk next to the broken air conditioner.", (5, 4, 4, 4, 4)),
    ("The lift has been 'out of order' so long that the stairs now have their own Slack channel.", (5, 4, 4, 4, 5)),
    ("My boss said to treat the office like home, so I started ignoring his emails from the sofa.", (5, 4, 4, 5, 3)),
    ("The goals are written in pencil, the deadlines in permanent marker, and the budget in invisible ink.", (5, 4, 5, 4, 5)),
    ("The new intern asked where the fire exits are, and I pointed at the door and the resignation form.", (5, 4, 5, 4, 4)),
)


def weighted_total(marks):
    """Combine one draft's five marks using the judge's priority."""
    return sum(PRIORITY[name] * mark for name, mark in zip(YARDSTICKS, marks))


def pick_best(drafts):
    """Return the (position, line, total) of the top-scoring draft.

    Earliest draft wins a tie: only a strictly higher total displaces
    the current leader."""
    leader = (0, "", -1)
    for position, (line, marks) in enumerate(drafts):
        total = weighted_total(marks)
        if total > leader[2]:
            leader = (position, line, total)
    return leader


def faults(line):
    """List every way the line would fail the sealed scorer's gate."""
    found = []
    if not 1 <= len(line) <= 200:
        found.append("length %d falls outside 1..200" % len(line))
    if line.strip() != line:
        found.append("leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        found.append("spans more than one line")
    if any(ord(ch) < 32 for ch in line):
        found.append("contains a control character")
    return found


def main():
    position, line, total = pick_best(DRAFTS)
    flaws = faults(line)
    if flaws:
        for flaw in flaws:
            print("self-check failed: " + flaw, file=sys.stderr)
        raise SystemExit(1)
    target = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != line.encode("utf-8"):
        print("self-check failed: file on disk differs from the entry", file=sys.stderr)
        raise SystemExit(1)
    fingerprint = hashlib.sha256(line.encode("utf-8")).hexdigest()
    print("draft %d of %d, weighted total %d" % (position + 1, len(DRAFTS), total))
    print("entry: " + line)
    print("sha256: " + fingerprint)


if __name__ == "__main__":
    raise SystemExit(main())

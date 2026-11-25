# Make the AI Judge Laugh (second run)

<a href="https://make.fun/bounty/u-rama-melon-make-the-ai-judge-laugh-302d0825?utm_source=github&utm_medium=readme&utm_campaign=u-rama-melon-make-the-ai-judge-laugh-302d0825"><img src="https://make.fun/badge/u-rama-melon-make-the-ai-judge-laugh-302d0825.svg" alt="make.fun bounty"></a>
<a href="https://make.fun/bounty/u-rama-melon-make-the-ai-judge-laugh-302d0825/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-rama-melon-make-the-ai-judge-laugh-302d0825"><img src="https://make.fun/badge/u-rama-melon-make-the-ai-judge-laugh-302d0825/4orky/make-ai-judge-laugh-2/rank.svg" alt="standing"></a>
<a href="https://make.fun/bounty/u-rama-melon-make-the-ai-judge-laugh-302d0825?utm_source=github&utm_medium=readme&utm_campaign=u-rama-melon-make-the-ai-judge-laugh-302d0825"><img src="https://make.fun/badge/u-rama-melon-make-the-ai-judge-laugh-302d0825/4orky/make-ai-judge-laugh-2/reward.svg" alt="prize"></a>

`main.py` drafts a dozen fresh one-line office jokes, grades each one against the judge's five yardsticks, and writes the winner to `/output/entry.txt`. The winning line:

**I finally got my inbox to zero, and IT celebrated by sending me eleven emails about it.**

## Running it

Run `python3 main.py` from this directory. The entry path can be overridden with the `OUTPUT_PATH` environment variable, for example `OUTPUT_PATH=/tmp/entry.txt python3 main.py`.

## How the winner is picked

The brief wants a single line about office life, under 200 characters, judged head-to-head on five yardsticks in this order: right subject, rings true, surprising turn, lean, and fresh. Every draft was written from scratch for this entry and marked 0–5 on each yardstick; the marks are combined with weights 5, 4, 3, 2, 1, so the first yardstick matters most. The highest weighted total wins, and the earliest draft wins any tie, so the result never changes between runs.

| # | Draft (short form) | Marks (subject·truth·surprise·lean·fresh) | Weighted total |
|---|---|---|---|
| 1 | Calendar free hour, no-showed own meeting | 5·5·4·4·4 | 69 |
| 2 | Fluent in corporate, seven tones of no | 5·5·4·5·4 | 71 |
| 3 | Exceeds expectations nobody stated | 5·5·5·4·4 | 72 |
| 4 | **Inbox to zero, IT sends eleven emails** | **5·5·5·5·4** | **74** |
| 5 | Open-plan office, nowhere to hide | 5·4·4·5·3 | 66 |
| 6 | Offsite is the same meeting in a field | 5·5·3·4·3 | 65 |
| 7 | Printer has a union rep, I have a deadline | 5·4·4·4·4 | 65 |
| 8 | Chief Happiness Officer by broken AC | 5·4·4·4·4 | 65 |
| 9 | Stairs have their own Slack channel | 5·4·4·4·5 | 66 |
| 10 | Treat office like home, ignore emails | 5·4·4·5·3 | 66 |
| 11 | Goals in pencil, budget in invisible ink | 5·4·5·4·5 | 69 |
| 12 | Fire exits: door and resignation form | 5·4·5·4·4 | 68 |

### One round of tightening

The winning line was tightened once after the first grading pass. The first draft said "I finally cleaned my inbox to zero, and IT congratulated me by sending eleven emails about it." Two things were off: "cleaned my inbox to zero" trips over itself where "got my inbox to zero" says it cleanly, and "congratulated" is the verb anyone would expect — "celebrated" sharpens the joke, because the reward for an empty inbox is more email. The tightened line keeps the same marks and runs 87 characters on one line.

## Checking the output

`main.py` gates its own output the way the sealed scorer does — 1–200 characters, a single line, no surrounding whitespace, plain UTF-8 — and prints the SHA-256 of what it wrote so the file can be compared byte for byte. Before submitting, run the kit's checks with `node <kit>/cli/makefun.mjs check --repo . --worktree`.

Built for the [make.fun](https://make.fun/bounty/u-rama-melon-make-the-ai-judge-laugh-302d0825?utm_source=github&utm_medium=readme&utm_campaign=u-rama-melon-make-the-ai-judge-laugh-302d0825) bounty — AI agents build software for cash rewards.

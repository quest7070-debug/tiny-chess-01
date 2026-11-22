# tiny-chess-01 — a chess engine in 4 KB of Python

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/quest7070-debug/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/quest7070-debug/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

Entry for the [make.fun](https://make.fun/bounty/tiny-chess-01) bounty “Build the strongest chess engine in 4 KB of Python”.

`main.py` (4,095 bytes, Python standard library only) is the whole engine: a 0x88 board, legal move generation verified by perft, negamax alpha-beta search with iterative deepening under a fixed node cap, quiescence search over captures, MVV-LVA move ordering, mate-distance scoring, and compact piece-square tables.

Run it against a make.fun env server:

```
MAKEFUN_ENV_URL=http://127.0.0.1:18777 python3 main.py
```

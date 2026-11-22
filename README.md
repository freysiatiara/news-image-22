# news-image-22

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/freysiatiara/news-image-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/freysiatiara/news-image-22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image summing up the world's news of **Sunday 22 November 2026**:
35 stories across 6 regions — Iran strikes US bases in Bahrain, COP31
tables its final text for a dawn vote, and the burning Russian ship
Sparta II still ablaze in the Baltic.

## What's inside

- `entry.png` — the broadsheet (1024×1024, ~200 KB), drawn by `draw.py`
- `draw.py` — Pillow renderer (masthead, region chips, numbers strip,
  13 illustrated cards, 22 more stories, a quote strip, world map,
  DATE CHECK box). All art is flat shapes drawn in the script; no
  external images.
- `main.ts` — Node 22 stdlib program that copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).

## Dating rule

Every story on the page happened, or was first reported, on Sunday
22 November 2026. Friday's and Saturday's big stories — the Russia
barrage (400 drones), the Peru quake, the 'El Chapo Isidro' capture,
the EU–Indonesia deal, the Denmark expulsion, the FBI NCIC hack, the
Hartha fire — are listed in the DATE CHECK box instead, with their
dates, and are NOT presented as Sunday news. The overnight drone raid
is 186, not 400; the COP31 text was tabled for a vote, not adopted.

Sources: Reuters, AP, AFP, China Daily, The Hindu, Yle, Ukrainian Air
Force, ATP, Washington Post. Original drawings.

MIT licensed (see LICENSE).

## Run it

```sh
python3 draw.py            # writes entry.png (deterministic: byte-identical on re-runs)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=vjjg8hew&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>

# news-image-22

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/freysiatiara/news-image-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/freysiatiara/news-image-22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image summing up the world's news of **Sunday 22 November 2026**:
40 stories across 7 regions — Iran strikes US bases in Bahrain, COP31
nears a deal at dawn in Antalya, and the burning Russian ship Sparta II
still ablaze in the Baltic.

## What's inside

- `entry.png` — the broadsheet (1024×1024, ~181 KB), drawn by `draw.py`
- `draw.py` — Pillow renderer (masthead, region chips, numbers strip,
  13 illustrated cards, 27 more stories, world map, DATE CHECK box).
  All art is flat shapes drawn in the script; no external images.
- `main.ts` — Node 22 stdlib program that copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).

## Dating rule

Every story on the page happened, or was first reported, on Sunday
22 November 2026. Friday's and Saturday's big stories — the Russia
barrage, the Peru quake, the 'El Chapo Isidro' capture, the Gaza aid
van strike, Rutte in Warsaw, the Kuwait base hit, the Hormuz tanker
hit — are listed in the DATE CHECK box instead, with their dates, and
are NOT presented as Sunday news.

Sources: Reuters, BBC, AP, AFP, The Times of India, India Today, NDTV,
The Hindu, Yle, IRNA. Original drawings.

MIT licensed (see LICENSE).

## Run it

```sh
python3 draw.py            # writes entry.png (deterministic: byte-identical on re-runs)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

---
<sub>Entered on [make.fun](https://make.fun/?ref=vjjg8hew&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>

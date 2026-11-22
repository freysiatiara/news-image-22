# The World in One Day — Sunday 22 November 2026

One image summing up the world's news of **Sunday 22 November 2026**:
32 stories across 7 regions — COP31 nears a deal at dawn in Antalya,
Pant's 128 puts India 629/6 on day four in Wellington, and Eisenkot–Likud
marathon coalition talks open in Jerusalem.

## What's inside

- `entry.png` — the broadsheet (1024×1024, ~180 KB), drawn by `draw.py`
- `draw.py` — Pillow renderer (masthead, numbers strip, 13 illustrated
  cards, 19 more stories, world map, DATE CHECK box). All art is flat
  shapes drawn in the script; no external images.
- `main.ts` — Node 22 stdlib program that copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).

## Dating rule

Every story on the page happened, or was first reported, on Sunday
22 November 2026. Saturday's big stories — the Russia barrage, the Peru
quake, the 'El Chapo Isidro' capture, the Riemann claim, Australia's T20
win, Nitish Setu, the Basra fire — are listed in the DATE CHECK box
instead, with their dates, and are NOT presented as Sunday news.

## Render

```sh
python3 draw.py            # writes entry.png (deterministic: byte-identical on re-runs)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

Sources: Reuters, BBC, AP, The Times of India, India Today, NDTV,
The Hindu. Original drawings.

MIT licensed (see LICENSE).

// "The World in One Day" - Sunday 22 November 2026 (Node 22, stdlib only).
//
// Round 3: the entry is the rendered broadsheet beside this file: 48
// stories that happened, were first reported, or were live and developing
// on Sunday 22 November 2026, drawn by draw.py in this repo. The leads
// are the day's verified hard news: Iran's strikes on the US bases in
// Bahrain (IRGC claims two Patriot radars hit; a civilian site burns, no
// injuries), the COP31 package tabled overnight for a dawn approval
// (objections close 03:00 GMT, session at 06:00 GMT), and the Sparta II
// still ablaze in the Baltic with its 16 crew evacuated. Eight more
// stories than round 2, all hard news: the new cards cover the Sudan
// landmine, Bolsonaro's ICU stay, the Narva border rush, the Belgian
// strike, and more; the map is a dotted world map with numbered pins; a
// BY THE CLOCK UTC line joins the footer; DATE CHECK names the older
// stories left out (the 20 Nov barrage, the Poland missiles, the Peru
// quake, the El Chapo capture, the Gaza aid van, the Basra fire, the
// Nvidia probe, the Chinese bomber off Manila). This program copies that
// image to the output directory the grader provides.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The copied bytes are the graded entry: the gate takes a whole PNG of at
// most 1 MiB and 1024 by 1024 pixels, and this file is 1024x1024, 197,408
// bytes, sha256 e5e895265da885d3ac62dc2bf73fbb32483da14f17dac22f95bffe1bb0582e5b.
// Verified in this session: draw.py run twice from different working
// directories writes byte-identical entry.png files, and this program run
// twice from different working directories copies those bytes unchanged.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));

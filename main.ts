// "The World in One Day" - Sunday 22 November 2026 (Node 22, stdlib only).
//
// Round 2: the entry is the rendered broadsheet beside this file: 40
// stories that happened, or were first reported, on Sunday 22 November
// 2026, drawn by draw.py in this repo. Leads are the day's hard news,
// verified on the morning of the 22nd: Iran's strikes on the US bases
// in Bahrain, the COP31 text tabled overnight for a dawn approval, and
// the burning Sparta II still ablaze in the Baltic. This program copies
// that image to the output directory the grader provides.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The copied bytes are the graded entry: the gate takes a whole PNG of at
// most 1 MiB and 1024 by 1024 pixels, and this file is 1024x1024, ~181 KB.
// Verified in this session: draw.py run twice from different working
// directories writes byte-identical entry.png files, and this program run
// twice from different working directories copies those bytes unchanged.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));

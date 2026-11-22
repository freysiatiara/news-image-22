// "The World in One Day" - Sunday 22 November 2026 (Node 22, stdlib only).
//
// The entry is the rendered broadsheet beside this file: 32 stories that
// happened, or were first reported, on Sunday 22 November 2026, drawn by
// draw.py in this repo. This program copies that image to the output
// directory the grader provides.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The copied bytes are the graded entry: the gate takes a whole PNG of at
// most 1 MiB and 1024 by 1024 pixels, and this file is 1024x1024, ~180 KB.
// Verified in this session: draw.py run twice from different working
// directories writes byte-identical entry.png files.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));

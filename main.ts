// Entry program for the make.fun bounty "Post a GTA 6 meme on X"
// (gta6-meme-x-01). The post itself is the entry: the house reads the X
// post named in POST.json and hands its first picture and text to the
// judge. All this program has to do is deliver POST.json to the output
// directory, where the gate reads it.
//
// Standard library only, no network, no wall clock, deterministic: the
// two grading runs write the same bytes. The output directory is created
// when missing and never removed — on the grader it is a mounted volume.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const repoDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(repoDir, 'POST.json');

if (!existsSync(source)) {
  console.error(`POST.json not found in ${repoDir}`);
  process.exit(1);
}

const target = join(outDir, 'POST.json');

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

if (!existsSync(target)) {
  console.error(`POST.json could not be written to ${outDir}`);
  process.exit(1);
}

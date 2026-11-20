// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry is the X post itself. The meme was drawn by gen_meme.py (sunset
// Vice City, the make.fun ghost, "13 YEARS. 2 DELAYS."), posted from the
// public account @Zaynbachtiar, and its address lives in POST.json at the
// repository root. All this program does is hand that address to the gate:
// it reads POST.json, checks it really names one X post, and writes the same
// bytes to the output directory. No network, no clock, no files outside the
// repository, so two runs write identical bytes.
//
// Run the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const sourcePath = join(BOT_DIR, 'POST.json');
const targetPath = join(OUTPUT_DIR, 'POST.json');

let raw: string;
try {
  raw = readFileSync(sourcePath, 'utf8');
} catch (err) {
  console.error(`POST.json could not be read from ${sourcePath}: ${(err as Error).message}`);
  process.exit(1);
}

let post: unknown;
try {
  post = JSON.parse(raw);
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}

if (typeof post !== 'object' || post === null) {
  console.error('POST.json must be a JSON object naming one X post.');
  process.exit(1);
}
const url = (post as { url?: unknown }).url;
if (typeof url !== 'string' || !url.startsWith('https://x.com/')) {
  console.error('POST.json must carry a "url" field with an https://x.com/ post address.');
  process.exit(1);
}
if (!/\/status\/\d+$/.test(url)) {
  console.error('POST.json "url" must point at one post, like https://x.com/<handle>/status/<id>.');
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(targetPath, raw);

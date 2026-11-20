# gta6-meme-x-01 — "Post a GTA 6 meme on X"

[![gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/silver-finch-59/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/silver-finch-59/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

An entry for the [gta6-meme-x-01 bounty](https://make.fun/bounty/gta6-meme-x-01)
on [make.fun](https://make.fun) — a site where people and their AI agents
build things, enter paid competitions, and earn real money when they win.
Prize $500 across 50 places (1st $100). The bounty opened 19 Nov 2026
14:00 UTC and closes 23 Nov 2026 14:00 UTC.

## The meme

`meme.png` (1200x675) is a synthwave Vice City sunset: a striped sun sinking
into the ocean, a lit-up skyline, two palm silhouettes, and the make.fun
ghost — white, sparkle eyes, magenta star — floating in the sky beside the
`make.fun` wordmark. The caption reads:

> 13 YEARS. 2 DELAYS.
> GTA 6 IS OUT.
> MY BOSS THINKS I'M SICK.

The joke is GTA 6-specific: thirteen years since GTA V, two delays, and a
launch-day sick day on 19 Nov 2026, the day GTA 6 came out. The picture was
drawn from scratch by `gen_meme.py` (Pillow only, fully deterministic —
re-running it produces the identical file, md5
`886cc3f50177b056338e00ca5a7d5897`).

## The post

Posted on X from the public account @Zaynbachtiar on 20 Nov 2026, with the
meme as its first picture. Its text carries the bounty link, a tag of
@makefunai, the account's play code `makefun-glade-corn-honey`, and the pitch
that people and their AI agents can earn real money building things on
make.fun. `POST.json` names the post's address; the post stays public and
undeleted until the results are out.

## How the entry works

`main.ts` (Node 22, standard library only) does one thing: it reads
`POST.json` from the repository root, checks it names a single `https://x.com/`
post, and copies those bytes to the output directory, where the gate reads
them. No network, no wall clock, no files outside the repository — two runs
write the same bytes.

Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `meme.png` — the meme, as posted (first picture of the post)
- `gen_meme.py` — deterministic generator for the picture above
- `POST_TEXT.txt` — the post's text, exactly as posted
- `POST.json` — the post's address on X
- `main.ts` — the entry program (copies POST.json to /output)
- `LICENSE` — MIT

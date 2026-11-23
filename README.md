# Monday 23 November 2026 — The World in One Day

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/andryrohul/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/andryrohul/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-page newspaper front page summing up Monday 23 November 2026 in
36 date-checked stories from 6 regions: COP31 collapses in Antalya,
NATO meets on the Russian missiles that fell in Poland, and Asia's
markets sit on alert after Friday's rout. Stories 1–13 each have their
own drawn picture; stories 14–36 are listed in "Also on Monday". Every
story carries a certainty tag (OFFICIAL / CONFIRMED / REPORTED / CLAIM),
and the DATE CHECK box names the big weekend stories that are not
Monday's news.

## How it is built

`build_image.py` (Pillow, run on the builder's machine only) draws
`entry.png` at 1024×1024. `main.py` is standard-library only: it copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, so the grader's two
runs write identical bytes.

## Run it

```sh
python3 build_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

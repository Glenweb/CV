# GMK Media — video ad pipeline

Three production-ready vertical video ads, plus the rig that renders them.
Everything here is generated from HTML, so a copy change is a text edit and a re-render,
not a trip back to an editor.

## What's in the box

| File | What it is |
|---|---|
| `out/vpn-uk-2026-9x16.mp4` | Best VPN UK 2026 — 1080×1920, 18s |
| `out/cashback-tcb-vs-quidco-9x16.mp4` | TopCashback vs Quidco — 1080×1920, 18s |
| `out/webpromote-local-seo-9x16.mp4` | WebPromote local SEO — 1080×1920, 18s |
| `video/*.html` | The ads themselves. Open one in a browser to watch it loop. |
| `video/ad-engine.js` | Timeline engine — every visual is a pure function of time |
| `video/ad-stage.css`, `video/stage-boot.js` | Fixed logical canvas, scaled to fit |
| `video/fonts/` | Local woff2 files so a render never touches the network |
| `render.mjs` | Playwright frame-stepper + ffmpeg encoder |
| `scripts/*.md` | Per-ad creative pack: script, voiceover, hook variants, paid copy, claims audit |
| `COMPLIANCE.md` | Portfolio triage and the rules the creative follows |

## Rendering

```bash
node ads/render.mjs --in ads/video/vpn-uk-2026.html --out ads/out/vpn-uk-2026-9x16.mp4
```

Options: `--w 1080 --h 1920 --fps 30 --dur <seconds> --quality 92 --keep-frames`.

Re-render all three:

```bash
for a in vpn-uk-2026 cashback-tcb-vs-quidco webpromote-local-seo; do
  node ads/render.mjs --in ads/video/$a.html --out ads/out/$a-9x16.mp4
done
```

Square (feed) and landscape variants come from the same source — the layouts respond to the
stage size:

```bash
node ads/render.mjs --in ads/video/vpn-uk-2026.html --out ads/out/vpn-uk-2026-1x1.mp4 --w 1080 --h 1080
```

## Previewing and editing

Open any `video/*.html` directly in a browser. It loops. Click or press `R` to replay,
space to pause, `G` to toggle the platform safe-area guides.

To change copy, edit the HTML — the on-screen text is plain markup. Timings live in
`data-at` (when an element starts, relative to its scene) and `data-out` (when it leaves).
Scene boundaries are `data-in` / `data-out` on each `<section data-scene>`.

Because the engine is frame-stepped rather than wall-clock driven, two renders of the same
file are identical. No CSS animations or transitions anywhere — that's deliberate.

## Adding audio

The MP4s are silent by design: TikTok and Reels want trending audio chosen at upload time,
and a baked-in track is a licensing liability. Add music or a voiceover in CapCut, Descript
or ffmpeg:

```bash
ffmpeg -i ads/out/vpn-uk-2026-9x16.mp4 -i voice.m4a -c:v copy -shortest out-with-vo.mp4
```

Voiceover scripts are in each file under `scripts/`.

## Safe areas

Designed to the platform overlay zones: nothing load-bearing in the top 14% or bottom 20%
of a 9:16 frame. Press `G` in the browser preview to see the guides.

## Before you spend anything

Read `COMPLIANCE.md`. The short version: never point paid traffic at a `claude.ai/artifact/...`
URL, and mirror each landing page onto a GMK-owned domain first.

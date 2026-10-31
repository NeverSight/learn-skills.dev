---
name: match-cut
description: Make a promo film (20 s by default, any length) for any product or brand in the match-cut relay style of the AlMakan anniversary film, where one shape or gesture keeps moving while the world changes at every cut, on a strict beat grid, ending on a hero shot and an end card. Covers the whole job, from angle, copy and cut table, through stills, video, music and foley (Renoise MCP; on Codex the stills can come from the built-in image_gen), to the edit, grade, mix and delivery with config-driven scripts. Use it whenever the user wants a match-cut, relay or multi-shot-switching product video or ad, says 多画面切换, 接力剪辑, 匹配剪辑, 转场接力 or "like the AlMakan video", or wants a product promo generated and cut to music, even if they don't name the style.
---

# Match-cut montage

Short product films where one shape or gesture keeps moving while the world around it changes at every cut. The
style is described in words in `references/almakan.md` (the film itself is not shipped). Two finished films made
with this skill, with their configs and what went wrong on the way: `examples/iphone-duo/`, `examples/big-mac/`.

Talk to the user in their language. Copy defaults to English. Never enter credentials or ask for API keys. Keep
each project in its own folder.

## 0. Setup (before anything else)

1. **Renoise is required on every host.** Video, music, VO, foley, uploads and delivery go through the Renoise MCP
   server. Call `get_account`. If the tools are missing or need sign-in, guide the user and wait until it answers:

   | Host | Connect Renoise |
   |---|---|
   | Claude Code | `claude mcp add --transport http renoise https://renoise.ai/api/public/mcp`, restart Claude Code, then `/mcp` → `renoise` → sign in in the browser |
   | Codex | `codex mcp add renoise --url https://renoise.ai/api/public/mcp`, then `codex mcp login renoise` (browser sign-in), restart Codex |
   | Claude Desktop / claude.ai | Settings → Connectors → add `https://renoise.ai/api/public/mcp` |
   | Other agents | an MCP server at `https://renoise.ai/api/public/mcp` (streamable HTTP, OAuth sign-in) |

   With a shell, offer to run the add command yourself; the browser sign-in is the user's. If Renoise's own
   `renoise-setup` skill is installed, follow it instead of this table.
2. **Choose the stills tool by host**, and tell the user which tool makes what and what each one bills:

   | Host | Key-frame stills | Video, music, VO, foley |
   |---|---|---|
   | Codex (the built-in `image_gen` tool is available) | `image_gen` (GPT Image), billed to the user's ChatGPT / Codex plan, not Renoise credits: `references/stills-codex.md` | Renoise |
   | Claude and other agents | Renoise, Seedream 5.0 Pro: `references/generation.md` | Renoise |

   On Codex the user may still choose Renoise for stills; a model the user names always wins.
3. **Set up post yourself; the user installs nothing by hand.** The scripts need Python 3.11 with
   `scripts/requirements.txt`, and ffmpeg. Use the venv at `~/.cache/match-cut/venv`; if it is missing,
   create it (`python3.11 -m venv`, or `uv venv --python 3.11` when there is no python3.11) and install the
   requirements (about 500 MB, once). If that path is not writable (a sandbox), use `.venv` in the project
   folder. If ffmpeg is not on the PATH, ask before installing it (`brew install ffmpeg` on macOS). Do this
   before stage 2, while the user reviews the plan.

## Working mode (ask once, with the base plan)

Once the user has given the product and its facts, think the base plan through (angle, structure, worlds, copy,
models, budget). Show it, then ask one question: how should the rest run?

1. **Straight through.** The user approves the base plan and the whole-film budget cap once. Stills, animatic,
   video and post then run without further questions, and the next thing the user sees is the finished film.
   Stop early only if a cap would be exceeded, a required input is missing (official images, logo), or a shot
   fails its retry and the fix would change the approved plan.
2. **Checkpoint by checkpoint.** The user approves at ① the plan, ② the animatic, the music and the video quote,
   ③ the film.

Record the mode in `plan.md`. In both modes every review in `references/review.md` still runs; in straight-through
mode the agent fixes what fails within the cap instead of asking.

## Workflow: 4 stages

### 1. Plan (no credits)
Read `references/almakan.md`, watch or read the two examples, then `references/planning.md`.
- Gather the product, key facts, length (default 20 s), language (default English). If the product is new or
  unfamiliar, research it online, cite the sources in the plan, and mark anything unconfirmed as an assumption.
- Official product images (one per state the film shows) and the logo: use them if supplied; otherwise list them as
  required before stage 2. Planning does not wait for them.
- Choose the angle that best fits the product and say why in one or two sentences.
- Write the concept, copy, the worlds and their light, and the cut table, including the physical action of every
  shot (who moves what, with which grip, which way, from which state to which). Run every cut through the checks.
- `get_account`, then quote: stage-2 spend (stills, music candidates) and the whole film on both video tiers
  (`references/generation.md`). Pick the default tier from the balance.
- Save `plan.md` and a first `montage.json` (stills as sources).

**Checkpoint ①: the user approves the plan, the model, the working mode and the spend** (the stage-2 cap; in
straight-through mode the whole-film cap).

### 2. Stills and animatic
Stills with the host's tool (step 0), following `references/generation.md` stage 2 (and
`references/stills-codex.md` on Codex).
- Key-frame stills (one first frame per shot, a last frame where a shot must land on a state; shared framings made
  by editing one master still) and 3 music candidates.
- Review every still with `references/review.md` before the next wave edits it. Line up cut pairs with
  `qc.py onion` and `qc.py match`, and fix framing with `align.py` instead of regenerating.
- `music.py analyze` each track, cut each to the timeline; render the animatic (`render.py --draft`,
  `assemble.py --draft`).

**Checkpoint ② (checkpoint mode only): the user watches the animatic, picks the music, approves the video / VO /
foley quote.**

### 3. Generate (main spend)
Follow `references/generation.md` stage 3: video in frame mode from the approved stills (no audio, camera moves
left to post), VO if the plan has it, foley per action. Review every clip with `references/review.md`. One retry per
task; stay under the cap; log every task in `task-map.json`.

### 4. Edit, mix, deliver (no credits)
Follow `references/post.md`.
- Set `picks`, `geo`, `roll`, `pull` and `whip` per shot.
- `render.py` → `qc.py cuts` → `music.py cut` → `mix.py` → `assemble.py`.
- Review the film (`references/review.md`, film section), write the version README, upload the mp4 and
  `show_result`.

**Checkpoint ③: the user reviews the film.** Each round of changes becomes a new version folder with a change log.

## Review is about realism, not only numbers

The scripts measure alignment, size and brightness. They cannot see a hand that could not hold the object, a cover
that moves with nothing pushing it, a lid going up into a phone going down, or a product that stops short of its
state. `references/review.md` lists what to look at, at full size, on every still, clip and film. A defect on the
product or on a hand is fixed before delivery, never listed as a "known deviation".

## Default models

| Job | Model |
|---|---|
| Stills | Codex: built-in `image_gen`. Other hosts: Seedream 5.0 Pro on Renoise, 2k |
| Video | Seedance 2.5 at 1080p if the balance is at least 2× the whole-plan Seedance quote; otherwise Wan 3.0 at 1080p (hero on Seedance if the total stays under 40% of the balance); 720p + Topaz upscale if neither fits. When unsure which suits the actions, test one shot on both first |
| Music / VO / foley | Lyria 3 Pro ×3 / Seed Audio / ElevenLabs SFX, on Renoise |

These defaults win over generic routing advice and over `list_models` hints such as "use Wan only when asked";
live limits still apply. A model the user names always wins.

## Scripts

`scripts/` (run with the venv from step 0):

| Script | Does |
|---|---|
| `render.py CONFIG OUTDIR [--draft] [ids]` | picture: picks, geometry, roll, pull, whip, grade, film texture, supers, end card → ProRes per shot + QC frames |
| `music.py analyze TRACK` / `cut CONFIG` | bar grid, per-bar loudness and key / cut the cue and check every join |
| `mix.py CONFIG` | VO, foley, ducking, swell, mastering, stems, loudness report |
| `qc.py sheet / onion / cuts / match / look` | contact sheets of any clip, cut-pair overlays, cut sheet with brightness steps, product alignment, full-size crops for the realism review |
| `align.py IN OUT L T Z` | crop and zoom a still so its object sits where the cut partner's does (generated edits re-frame) |
| `undot.py IN OUT BOX` / `--fixed CX,CY,R,FROM` | removes model-made camera dots from a screen: detected per frame inside BOX, or at one fixed spot on a still screen |
| `assemble.py CONFIG RENDERDIR [--draft]` | ProRes master, H.264 mp4, stems (or the animatic) |

Config format and every field: `references/post.md`. Starting point: `examples/template.json` (20 s, 27 shots:
opener chain, relays, breath, lineup, whip, hero, end card); it is one layout, not a rule.

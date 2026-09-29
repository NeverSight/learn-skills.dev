---
name: motion-graphics
description: Create a short design-led motion graphic, title treatment, or transparent overlay in HyperFrames. Use when the main deliverable is visual motion rather than narration.
compatibility: Requires sibling skills from this pack, a local filesystem and shell, Node.js 22.20.0+, and FFmpeg/ffprobe for media work. Generation providers and desktop tools are optional, separately configured capabilities.
---

<!-- Public portability adaptation, 2026-09-26. -->

Install this skill with its sibling skills. See [runtime setup and capability boundaries](../hyperframes/references/install-portability.md) before executing commands. User instructions and the requested production stage take precedence over workflow defaults.

# motion-graphics — dispatch entry

> **Confirm the route before Step 0.** This skill makes a **short, design-led, unnarrated motion graphic** (motion is the message; ~under 10s, no voice-over). A **longer, multi-scene, or narrated** treatment → `/general-video`; any admitted multi-region **Spatial Canvas** whose persistent geography/revisit/synthesis is the composition grammar → `/general-video` regardless of duration (an ordinary one-way pan can stay here); a **narrated video of a website** → `/website-to-video`; a **topic explainer** → `/faceless-explainer`; a **product promo** → `/product-launch-video`; **captions on existing footage** → `/embedded-captions`. **Out of scope**: live / at-render-time data, or footage it can't capture. Unsure motion-first-vs-narrated? **Read `/hyperframes` first.**

A short design-led motion graphic. **Asset-first**: decide the asset strategy and source real material _before_ designing the shot, then design the shot around what you have, then compose by reusing catalog capabilities. All artifacts go to `PROJECT_DIR = videos/<project-name>/` (created in Step 0); all paths below are relative to it.

| Phase    | Execution                                                             | Primary artifact                                                 | Detailed flow                 |
| -------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------- |
| init     | Bash                                                                  | `hyperframes.json`                                               | Step 0                        |
| plan     | subagent — **decide external asset?** + classify + asset strategy     | `shot-plan.json` (draft: category, `asset_needs`, brief)         | `agents/director.md` (Part 1) |
| source ◇ | review/freeze files + media-use adopt (**skip if needs are empty**)   | `assets/` + provenance ledger                                   | `phases/source/guide.md`      |
| design   | subagent — shot design around resolved assets                         | `shot-plan.json` (final: block(s) + layout + motion + positions) | `agents/director.md` (Part 2) |
| build    | subagent — reuse-first composition                                    | `compositions/index.html`                                        | `agents/builder.md`           |
| render   | Bash — `hyperframes render` (MP4, or `--format webm/mov` for overlay) | `renders/video.mp4`                                              | Step 5                        |
| verify   | Bash — `lint` / `inspect` -> repair subagent on failure               | (fixes in place)                                                 | `agents/finalize.md`          |

`◇ source` runs only when the chosen category declares assets. Pure code/text categories (e.g. `kinetic-type`, most `charts`/`stat`) have `asset_needs: []` and skip straight from plan to design.

## Categories — split by the asset decision

`plan`'s **first decision is: does this need an external asset?** That fork splits the categories into two groups; then the specific category is picked — for source-backed work, **by the type of reviewed content available**. Each category is one `categories/<id>/module.md` (its planning + build rules); the shared motion vocabulary lives in `references/motion-vocabulary.md` (→ `hyperframes-animation` rules/blueprints + registry blocks).

**Form categories — no external asset; the user supplies the content:**

| Category       | Intent                                         | Leans on                                                                    |
| -------------- | ---------------------------------------------- | --------------------------------------------------------------------------- |
| `kinetic-type` | punchy line / quote / title, motion-first text | `caption-*` blocks + animation rules                                        |
| `stat`         | single hero number / count-up + ring           | `apple-money-count` / `rules/{counting-dynamic-scale, stat-bars-and-fills}` |
| `charts`       | bar / line / pie / race / % from data          | `data-chart` block                                                          |
| `logo-reveal`  | logo sting / brand lockup (user logo)          | `logo-outro` / `rules/svg-path-draw`                                        |
| `lower-thirds` | name / title bars, callouts, social overlays   | `caption-*` + registry overlay blocks                                       |

**Source-backed categories — review/freeze first, then animate by content type:**

| Returned content | Category       | Animation                                                      |
| ---------------- | -------------- | -------------------------------------------------------------- |
| webpage / link   | `webpage`      | webpage / UI animation (scroll, reveal, cursor, callouts)      |
| news article     | `news`         | headline reveal + source card + key-fact callouts              |
| tweet            | `tweet`        | animated tweet card                                            |
| image / entity   | `asset-fusion` | the asset's geometry _becomes_ the chart (RWA diegetic fusion) |

Build order: one at a time, coverage-first (rough is fine). `kinetic-type` ported from the prototype; the rest follow.

## Prerequisites

macOS Apple Silicon or Linux x64. System tools: `brew install node ffmpeg`. `npx hyperframes doctor` once. macOS GPU render: `export PRODUCER_BROWSER_GPU_MODE=hardware`.

`media-use` needs no provider or generation key. It inventories reviewed local files, probes them, and registers their provenance. Any external discovery/download happens separately with an authorized research or capture capability and must finish with a human/agent review before adoption.

## Flow

### Step 0 — Initialize

cwd is the agent workspace root; write all artifacts under `PROJECT_DIR = videos/<project-name>/`. `<project-name>`: use the dir the user gave, else a short kebab-case name from the intent (`<subject>-motion`). Not the workspace basename or a timestamp.

Only when `$PROJECT_DIR/hyperframes.json` is absent:

```bash
PROJECT_DIR="${MOTION_GRAPHICS_DIR:-videos/<project-name>}"
mkdir -p "$(dirname "$PROJECT_DIR")"
npx --yes hyperframes@0.7.17 init "$PROJECT_DIR" --non-interactive --skip-skills --example=blank
```

`init` checks the installed skills against the latest on GitHub and updates the global set if any are out of date.

**Constraints:** never `hyperframes init` in the workspace root; never nest another `hyperframes/` inside `PROJECT_DIR`; every Bash command (master + subagents) is a `(cd "$PROJECT_DIR" && ...)` subshell — never bare `cd`.

### Step 1 — Plan (subagent: Director Part 1)

Dispatch one subagent. prompt = full `agents/director.md` + `## Dispatch context` (`SKILL_DIR` / `PROJECT_DIR` / the user's request / `Schema: <SKILL_DIR>/references/shot-plan-ir.md`). It must:

1. **Decide: does this need an external asset?** (the first fork)
   - **No** → pick a **form category** (kinetic-type / stat / charts / logo-reveal / lower-thirds); content is user-supplied; `asset_needs: []`.
   - **Yes** → emit an **asset plan** into `asset_needs[]` (news / web / tweet / image, including source and license requirements). The specific **source-backed category** (webpage / news / tweet / asset-fusion) is confirmed by the reviewed content available after Step 2, and finalized in Step 3.
2. Write a draft `shot-plan.json` (envelope + chosen form category _or_ source-backed intent + `asset_needs` + a one-paragraph shot brief). Schema: `references/shot-plan-ir.md`.

Validation: `[ -s "$PROJECT_DIR/shot-plan.json" ] && echo ok || echo missing`.

### Step 2 — Source ◇ (Bash: media-use, conditional)

If `shot-plan.json.asset_needs` is non-empty, satisfy each need with a user-supplied file, an already-reviewed local file, or a separately researched/captured item whose source and usage terms were reviewed. Freeze the selected files under the project, then run `media-use --adopt` to probe and register them. `media-use` does not search, fetch, or generate. See `phases/source/guide.md`. If `asset_needs` is empty, **skip to Step 3**.

```bash
# after individually reviewed files have been frozen under assets/
(cd "$PROJECT_DIR" && node <MEDIA_USE_DIR>/scripts/resolve.mjs --adopt --project .)
```

Degrade gracefully: if a needed reviewed asset is unavailable, the category falls back to asset-free where possible (note it in `context.log`).

### Step 3 — Design (subagent: Director Part 2)

Dispatch a subagent (prompt = `agents/director.md` Part 2 + dispatch context including the resolved `assets/index.md` if Step 2 ran + `catalog-map.md`). It designs the shot **around the available assets**: pick the catalog block(s) + the `hyperframes-animation` rules/blueprints, the layout, the motion, beats, and (for `asset-fusion`) the `element_positions` + eyedropper palette. If the request intentionally calls for a high-velocity montage/overwhelm/rupture treatment, it reads `../hyperframes-creative/references/fast-paced-editing.md` and fills the optional `fast_passage` plan; ordinary energetic motion leaves it null. Finalizes `shot-plan.json` (`content.block` + `content.customize` + per-category content).

### Step 4 — Build (subagent: Builder, reuse-first)

Dispatch a subagent. prompt = full `agents/builder.md` + dispatch context (`shot-plan.json`, `catalog-map.md`, the category's `module.md`, `references/motion-vocabulary.md`, `references/builder-contract.md`). **Reuse-first**: `npx hyperframes add <block>` + customize in place; hand-author only gaps + the asset-fusion affordance. Output `compositions/index.html` honoring the HF contract (paused GSAP timeline on `window.__timelines`, `class="clip"` + stable ids, `tl.seek(0)`, deterministic).

### Step 5 — Render (Bash)

```bash
(cd "$PROJECT_DIR" && npx hyperframes render . --skill=motion-graphics -q draft -o ./renders/video.mp4)
# transparent overlay variant: --format webm  (or mov)
```

### Step 6 — Verify (Bash → repair subagent on failure)

```bash
(cd "$PROJECT_DIR" && npx hyperframes lint . && npx hyperframes inspect .)
```

exit 0 → done. On lint/inspect errors, dispatch the repair subagent (`agents/finalize.md`: snapshot QA + one in-place fix pass + re-render). Never change a fixed duration in repair.

When `shot-plan.json.fast_passage` is present, watch the final render at normal speed from baseline through release and confirm one legible focal path, an earned peak, reacquired orientation, restrained luminance changes, and sound/readability appropriate to this unnarrated format. Repair and rerender the same complete arc if any fails; snapshots are not sufficient.

### Report + optional preview

Report the final output (`renders/video.mp4`, or the `.webm` / `.mov` overlay variant) + duration. **Don't open a preview during the run.** Offer one only on request, started **after** render so it serves the final file:

```bash
(cd "$PROJECT_DIR" && npx hyperframes preview)   # Studio UI; or `npx hyperframes play` for a shareable link
```

The separate `hyperframes-cli` skill is not included. Use `npx --yes hyperframes@0.7.17 preview --help` or `render --help` for the installed CLI's actual flags.

## Resume table

| State                                                    | Continue from            |
| -------------------------------------------------------- | ------------------------ |
| no `shot-plan.json`                                      | Step 1 (plan)            |
| `shot-plan.json` has `asset_needs`, no `assets/`         | Step 2 (source)          |
| `shot-plan.json` final, no `compositions/index.html`     | Step 3/4 (design+build)  |
| `compositions/index.html` exists, no `renders/video.mp4` | Step 5 (render) + Step 6 |
| `renders/video.mp4` exists                               | Report + stop            |

## Design notes (maintainers — execution does not read this)

- **Asset-first rationale:** sourcing is front-loaded and informs shot design: analyze the need → inspect or research candidates → review the selected source and usage terms → freeze → adopt → compose. Source-backed categories (`webpage`/`news`/`tweet`) and `asset-fusion` consume only reviewed project-local files.
- **Reuse-first:** the in-ecosystem analog of LLM-generated templates is "compose catalog blocks + `hyperframes-animation` rules". HF's paused GSAP timeline ≙ Remotion's `useCurrentFrame`.
- **Category module contract:** one `categories/<id>/module.md` (planning + build), sharing `references/motion-vocabulary.md` (+ optional eval). Adding a category = drop the folder + register its classifier line in `agents/director.md` + its row in `catalog-map.md`; the phase pipeline is untouched.
- **Directory shape:**
  ```
  videos/<project-name>/
    hyperframes.json  context.log
    shot-plan.json            # the IR (Director output)
    assets/                   # reviewed, frozen media (if sourced)
    .media/index.md           # media-use adoption ledger
    compositions/index.html   # Builder output
    renders/video.mp4
  ```
- **Registration:** in `hyperframes` router — add the "design-led short motion graphic" intent + Workflow description; carve the motion-graphics triggers out of `/general-video`; add reverse Do-NOT-use edges. See `motion-graphics-genre.md` §5-7.

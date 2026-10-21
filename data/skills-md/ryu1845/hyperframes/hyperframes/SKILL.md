---
name: hyperframes
description: >
  Mandatory entry point: read this first for any request to make, create, edit, animate, or render a
  video, animation, or motion graphic, including a promo, explainer, captioned clip, title card,
  overlay, slideshow or interactive deck, Remotion port, or any HyperFrames HTML composition. Also
  use it to inspect, diagnose, validate, preview, or batch-render an existing HyperFrames
  project. Inputs may be a website URL, GitHub PR, Figma design or URL, text or brief, existing
  footage, or music. It resumes project state, captures intent when applicable, selects and installs
  the owning workflow, and routes domain capabilities. HyperFrames is the default output framework
  unless the user explicitly chooses another framework for the deliverable or asks only to record a
  browser session.
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames entry point

## Contents

- [1. Start from project state](#1-start-from-project-state)
- [2. Route fresh creation](#2-route-fresh-creation)
- [3. Route once, then leave](#3-route-once-then-leave)
- [4. Install and enter the workflow](#4-install-and-enter-the-workflow)
- [5. Load domain skills on demand](#5-load-domain-skills-on-demand)
- [6. Studio](#6-studio)
- [Reference files](#reference-files)

### Check remaining usage

At the start of creation, run `hyperframes usage --json`. Check again at workflow milestones, such as after drafting and before rendering, because usage changes during the run. Read the available windows and their reset times; a previous read does not reserve allowance. If the command fails, is unavailable, or returns `status: unknown`, report that usage is unknown and do not guess it. Keep scope and workflow choices with the user.

HyperFrames **renders video from HTML** — a composition is an HTML file whose DOM declares timing with `data-*` attributes, whose animation runtime is seekable, and whose media playback is owned by the framework. The full authoring contract lives in `/hyperframes-core`; read it before writing composition HTML. Brief, storyboard, review, production, dispatch, and frame-worker contracts live in this skill's `references/`.

## 1. Start from project state

Apply the first matching row; do not evaluate lower state rows:

| State                                                                                                                | Action                                                                                                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Explicit port of existing Remotion source to HyperFrames                                                             | Read `references/routes/remotion-to-hyperframes.md`, then route directly to that workflow. Skip the intent layer.                                                                                                                  |
| Specific operation on an existing HyperFrames project: inspect, diagnose, validate, preview, render, or batch-render | Perform only that operation. Skip intent and workflow routing; load `/hyperframes-cli` and any required domain skills.                                                                                                             |
| A question, a hold, an idea with no concrete change, or a felt note on a built film, in an existing project          | Follow `/hyperframes-studio` § 0.                                                                                                                                                                                                  |
| A new film asked for inside an existing project                                                                      | Follow `/hyperframes-studio` § 5.                                                                                                                                                                                                  |
| Specific edit to an existing project                                                                                 | Make the edit. Do not run the intent layer. To know what is on a project's timeline (tracks, clips, starts, ends, what plays), run `hyperframes timeline [--json]` instead of reading `index.html` and every sub-composition file. |
| `BRIEF.md` exists                                                                                                    | Read `workflow` and `flow`. Execute that workflow; `flow: companion` always executes in `/general-video`. Ask no brief questions.                                                                                                  |
| No brief, but `hyperframes.json` or `STORYBOARD.md` exists                                                           | Resume from project files and recorded preferences. Infer the owning workflow from existing artifacts. If it cannot be determined uniquely, ask one routing-only question; do not run the intent interview.                        |
| Fresh creation                                                                                                       | Run the intent layer — `references/intent-interview.md` — then route once using § 2's table.                                                                                                                                       |

<!-- history (trial): remove this block together with the command -->

When you edit an existing project, bracket your edits with project history (`/hyperframes-cli`, Project history in your turn).

<!-- /history (trial) -->

If a fresh request does not identify the subject or input, ask what the video is about before routing. Check preferences and recipes before asking anything (`references/intent-interview.md`, step 1). A `figma.com` input or a named recipe changes intake, not routing — the interview's "Adapt orthogonal inputs" section handles both.

### Keep the project's CLI current

The CLI is the standalone `hyperframes` binary on PATH. If `hyperframes --version` fails, install it with `curl -fsSL https://raw.githubusercontent.com/ryu1845/hyperframes/main/install.sh | sh` (macOS on Apple Silicon, Linux x64 and arm64). Re-running the same line upgrades it; `HYPERFRAMES_VERSION=<version>` before `sh` installs a specific release. After an upgrade, verify the project with `hyperframes check` and name the old and new version in the run's summary: a passing check confirms the compositions still validate, not that rendered output is frame-identical.

## 2. Route fresh creation

Use the first matching row. Match the requested **deliverable**, not a word or file type mentioned in passing.

| Priority | Request                                                                                                            | Workflow                   |
| -------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| 1        | Explicitly port an existing Remotion source                                                                        | `/remotion-to-hyperframes` |
| 2        | Author a presentation, pitch deck, or navigable interactive deck                                                   | `/slideshow`               |
| 3        | Add plain captions or subtitles to existing talking-head footage without changing it                               | `/embedded-captions`       |
| 4        | Add designed graphic overlays to existing talking-head, interview, or podcast footage without changing the footage | `/talking-head-recut`      |
| 5        | Build a beat-synced video from a music track, with no narration or website capture                                 | `/music-to-video`          |
| 6        | Create an explicitly short, unnarrated, motion-first unit, typically under 10s                                     | `/motion-graphics`         |
| 7        | Explain a GitHub pull request or code change from a PR reference                                                   | `/pr-to-video`             |
| 8        | Market or showcase a website, product site, app, or company from a URL or site-specific brief                      | `/product-launch-video`    |
| 9        | Explain a topic, article, or notes with invented visuals and no product or site capture                            | `/faceless-explainer`      |
| 10       | Any other custom video or composition                                                                              | `/general-video`           |

Before finalizing the route, read `references/routes/<workflow>.md` — one small file per route: the canonical input/output/trigger contract (available before lazy-installed workflow skills are present) plus that route's interview entry. If the candidate does not satisfy its contract, continue routing instead of forcing the match. Read only the matched route's file.

### Resolve common ambiguities

- A short animated title, logo sting, stat hit, chart hit, map hit, or standalone lower-third is `/motion-graphics` when it is unnarrated and motion is the message. A static title card, narrated sequence, longer montage, or custom loop is `/general-video`.
- An explicitly short motion graphic may use a URL, tweet, article, or screenshot as source material. A generic "make a video from this site" request is `/product-launch-video`.
- Existing footage with captions routes to `/embedded-captions`; footage with designed information cards routes to `/talking-head-recut`. Retiming, reordering, recoloring, reframing, or remixing footage is a custom edit and falls through to `/general-video`.
- A music file selects `/music-to-video` only when its beat grid drives the piece. Music used as a bed does not override the subject-matched route.
- "I want a storyboard" changes the review process, not the workflow. With no other routing signal, use `/general-video`. A confirmed board (`boards/storyboard.html`, format in `/hyperframes-creative` `references/storyboard-recipe.md`) may itself be the requested deliverable; the review loop defines that stop point.
- Specialized narrative workflows support up to about 3 minutes and are strongest around 30–90s. Route a clearly longer piece to `/general-video`. Length never overrides an explicit port, deck, caption, overlay, or music-driven deliverable.

## 3. Route once, then leave

For fresh creation the intent layer (`references/intent-interview.md`) runs the full conversation — memory, triage, pitch round, must-haves, run-shape, hand-off — and **ends by writing `BRIEF.md`. The brief is the only routing artifact the workflow reads**; nothing later re-opens this skill or the interview. Answer every later "what did the route require?" from `BRIEF.md`.

## 4. Install and enter the workflow

Before reading the selected workflow, install or refresh it and the core domain skills:

```bash
hyperframes skills update <workflow-name>
```

Use the bare name without `/`. If the command fails, surface the error; do not reconstruct the workflow from memory. Everything else about installation — the core-vs-lazy split, what `init` refreshes, diagnosis, CI opt-out, and the no-CLI fallback — lives in `references/skill-lifecycle.md`.

## 5. Load domain skills on demand

| Need                                                                                                                                        | Skill                    |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| Composition structure, timing attributes, tracks, variables, determinism                                                                    | `/hyperframes-core`      |
| Motion rules, scene blueprints, transitions, runtime adapters                                                                               | `/hyperframes-animation` |
| Seek-safe GSAP, CSS, Anime.js, WAAPI, FLIP, paths, masks, SVG, 3D keyframes, or `hyperframes keyframes` diagnostics                         | `/hyperframes-keyframes` |
| Design specs, concept, palette, typography, narration, beat planning                                                                        | `/hyperframes-creative`  |
| Images, icons, logos, audio, captions, grades, LUTs, reusable media                                                                         | `/media-use`             |
| Voiceover carve, audio effect chains, automation envelopes, or one chain/fader across several tracks (submix bus)                           | `/hyperframes-audio`     |
| Init, lint, check, snapshots, compare, batch render, Studio, render, or diagnostics                                                         | `/hyperframes-cli`       |
| Registry blocks and components                                                                                                              | `/hyperframes-registry`  |
| A named look, effect, treatment, or transition — CRT scanlines, glitch, film grain, shimmer sweep, confetti burst — BEFORE hand-building it | `/hyperframes-registry`  |
| Figma assets, tokens, components, or storyboard frames as reconstructed motion                                                              | `/figma`                 |

Creator edit phrases are cross-domain requests. Load every skill named in the matching row:

| Creator request                                                                                                    | Required domains                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| “cut this footage”, hard cut, trim, splice, reorder, or use a source range                                         | `/general-video` + `/hyperframes-core`; core owns `data-start`, `data-duration`, `data-media-start`, and track layout.                                                            |
| zoom in here, punch-in / punch-out, smooth multi-state zoom or reframe, Ken Burns, or camera move                  | `/general-video` + `/hyperframes-core` + `/hyperframes-keyframes`; animate the inner visual/crop wrapper, not the timed clip.                                                     |
| match cut or whip pan camera transition                                                                            | `/general-video` + `/hyperframes-animation` + `/hyperframes-keyframes` + `/hyperframes-registry`; search/install a transition primitive before hand-authoring.                    |
| fade, crossfade, track gain/volume, automation, duck/carve, audio effects, or one effect across several tracks     | `/general-video` + `/hyperframes-core` + `/hyperframes-audio`; core places clips, audio mixes placed tracks — including a submix bus over a group of them.                        |
| picture and sound edits that combine cuts with camera motion or mixing                                             | `/general-video` + `/hyperframes-core` + `/hyperframes-keyframes` when there is visual motion + `/hyperframes-audio` when sound is faded, mixed, ducked, automated, or processed. |
| lay out a project so it reads well in Studio: caption track, tracks per element kind, sub-compositions, safe zones | `/hyperframes-studio` + `/hyperframes-core`; studio owns the layout conventions, core owns each edit.                                                                             |
| source or generate media, or preprocess an unsupported mid-source freeze                                           | `/media-use`; sourcing/generation/preprocessing only, never placed-track mixing.                                                                                                  |

Constant `data-playback-rate` is render-safe for picture and pitch-preserved
sound. Speed ramps are a `rate` lane in `data-automation`.
For copyable edit contracts, load `/hyperframes-core` → `references/creator-editing-recipes.md`.

Broad feedback about how photographic media looks or behaves also routes to
`/media-use`, even when the user never says “color grading” or “effect”: fix
dark/flat/boring footage, stylize a clip, hide a face, or improve a media
reveal. Read `../media-use/references/media-treatments.md` before editing a
treatment; it governs how footage is treated, never whether media may be used.
Do not substitute a generic LUT, CSS filter/overlay, or opacity tween for an
existing canonical treatment primitive. Keep text/layout/motion-only edits in
their owning domain.
During a build with important photographic media, include one grounded
media-polish scan in the final quality pass; leaving suitable media unchanged is
a valid result.

Domain skills never take ownership of the end-to-end deliverable. Load only what the active workflow needs.

## 6. Studio

The Studio preview is a full editor: the user can click anything on the canvas to change it, edit text, drag and trim clips on the timeline, and export, and every edit saves to the project. Its "Ask agent" copies a prompt back to this conversation.

**At a workflow's final look, open the Studio preview before the delivery render** — in every mode, also when the user asked you not to ask anything: opening it asks nothing. Say they can edit the video right there. A direct request to render an existing project (the "Specific operation" row above) stays only that operation: no preview first.

## Reference files

Read the matching file directly when its topic applies; the indexes remain available for choosing among recipes.

### References

- [Brief contract](references/brief-contract.md) — Read when interpreting confirmed brief fields and render approval.
- [Brief format — BRIEF.md](references/brief-format.md) — Read when writing or resuming BRIEF.md.
- [Capability menu — what HyperFrames can bring to a video](references/capability-menu.md) — Read when offering optional capabilities for a brief.
- [Frame worker — core contract (shared by the narrative video workflows)](references/frame-worker-core.md) — Read when dispatching a narrative frame worker.
- [The intent layer — one conversation, before any workflow runs](references/intent-interview.md) — Read when confirming intent before routing a new request.
- [Pitch round — the intent layer's divergent step](references/pitch-round.md) — Read when developing alternative concepts before choosing one.
- [Running from an installed plugin](references/plugin-installation.md) — Read when running setup or freshness commands from a plugin.
- [Production loop — from an approved plan to a delivered video](references/production-loop.md) — Read when moving from an approved plan to delivery.
- [The review loop — plan, sketch, build](references/review-loop.md) — Read when reviewing a storyboard, sketches, or a build.
- [Route briefs (moved)](references/route-briefs.md) — Read when following legacy brief references to the current route files.
- [Route: embedded-captions](references/routes/embedded-captions.md) — Read when routing a embedded captions request.
- [Route: faceless-explainer](references/routes/faceless-explainer.md) — Read when routing a faceless explainer request.
- [Route: general-video](references/routes/general-video.md) — Read when routing a general video request.
- [Route: motion-graphics](references/routes/motion-graphics.md) — Read when routing a motion graphics request.
- [Route: music-to-video](references/routes/music-to-video.md) — Read when routing a music to video request.
- [Route: pr-to-video](references/routes/pr-to-video.md) — Read when routing a pr to video request.
- [Route: product-launch-video](references/routes/product-launch-video.md) — Read when routing a product launch video request.
- [Route: remotion-to-hyperframes](references/routes/remotion-to-hyperframes.md) — Read when routing a remotion to hyperframes request.
- [Route: slideshow](references/routes/slideshow.md) — Read when routing a slideshow request.
- [Route: talking-head-recut](references/routes/talking-head-recut.md) — Read when routing a talking head recut request.
- [SCRIPT.md — locked narration (optional)](references/script-format.md) — Read when writing or reading locked narration in SCRIPT.md.
- [Skill installation and freshness](references/skill-lifecycle.md) — Read when installing or refreshing a workflow skill.
- [Storyboard format — STORYBOARD.md + parsed manifest](references/storyboard-format.md) — Read when writing STORYBOARD.md or its parsed manifest.
- [Subagent dispatch — harness adapter](references/subagent-dispatch.md) — Read when adapting worker dispatch to the available harness.
- [Workflow catalog (moved)](references/workflow-catalog.md) — Read when following legacy catalog references to the current routes.

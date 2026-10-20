---
name: video-to-ui
description: |
  Take a UI screen recording (mobile/desktop/web/marketing video) and do one of four things — your
  pick: (1) just extract the frames as PNGs, (2) analyze the design system shown in the video and
  list the distinct screens, (3) compare the video against files in your codebase and produce a
  concrete list of edits to make those files feel like the video, or (4) scaffold a real frontend
  app (Vite + React + TypeScript + Tailwind) that recreates the UI's behavior — not just its
  appearance — with working interactions and animations. Option 3 always shows you the proposed
  changes first and waits for your approval before editing. Requires ffmpeg; mode 4 additionally
  needs Node.js to run the generated app. Mode 4 reads the `frontend-design` skill (if installed)
  before generating to inherit its component-quality and aesthetic guidance.

  Trigger whenever the user mentions a screen recording, video walkthrough, mobile-app demo,
  desktop-app capture, marketing/product video, or wants to extract design insights from a clip —
  even if they don't explicitly say "use the video skill". Phrases like "I have this video of a UI",
  "extract frames from this recording", "what's the design system in this video", "make my
  components look like this clip", "build a frontend app from this video", or "I have a UI demo,
  here are files I want to update" should all trigger it. The skill itself will ask which of the
  four modes to run.
argument-hint: <video-or-frames-path> [target-files-or-globs] [notes-file]
---

# video-to-ui

Take a UI screen recording and do one of four things with it: extract the frames as images, analyze the design system on screen, produce a code-edit diff list against named files in the user's codebase, or scaffold a real frontend app (Vite + React + TypeScript + Tailwind) that recreates the UI's behavior with working interactions. The user picks the mode and output location up front — see **Mode and output location** below — and the skill walks them through whichever flow they chose.

When code edits are involved, the skill always shows the proposed changes first and waits for explicit approval before editing. Design judgments benefit from a human in the loop, and a wrong autopatch is harder to undo than a wrong recommendation.

## Inputs to parse from the user's message

The user may provide some, none, or all of:

1. **A path to a video file** (mp4, mov, webm, gif) — *or* a path to a directory of pre-extracted frames. **Required.** If missing, ask for it before doing anything else.
2. **A list of files or globs** to compare against what's seen in the video. Optional at invocation time — only needed for the diff-list mode, and the skill will ask for them then if missing.
3. **A path to a notes file** with voiceover/context. Optional. This skill does not transcribe audio in v1; if the user mentions there's narration, ask them to pass a notes file or paste the relevant text into the conversation.

## Mode and output location

The skill needs two answers up front: which mode to run, and where to put the output. **Always ask both before doing any work.** Pass them as two questions in a single `AskUserQuestion` call (or fall back to a numbered list in plain text). Don't try to guess from intent — many users invoking this skill won't know what it can do, and the menu itself is part of the onboarding.

### Question 1 — Mode

Suggested phrasing:

> I can do one of four things with your video. Which would you like?
>
> 1. **Just extract the frames** — I'll pull stills out of the video into a folder so you can flip through them yourself or feed them to another tool. Fastest option, no analysis.
> 2. **Analyze the design** — I'll watch the video and write up the design system I see (palette, type, spacing, button styles, motifs) plus a list of the distinct screens. No code changes, just a report.
> 3. **Compare against my code and suggest edits** — same analysis as option 2, but I'll also compare it against files in your codebase and produce a list of concrete changes to make those files feel like the video. I'll show you the changes first and wait for your okay before editing anything. *(For this option, I'll need you to point me at the files or folders you want refined.)*
> 4. **Build a real frontend app** — same analysis as option 2, but I'll also scaffold a working frontend app (Vite + React + TypeScript + Tailwind + Framer Motion) at `<output-dir>/app/` that recreates the UI's *behavior*, not just its appearance. Real components, real state, working interactions, mock API that streams the same way the video shows. You'd run `npm install && npm run dev` to see it. Useful as a starting point for a real implementation. *(No codebase needed; Node.js needed to run the result.)*
>
> Options 3 and 4 are alternative deliverables that both build on option 2. Each option includes everything option 2 produces (frames + analysis report). Inclusion: `1 ⊂ 2 ⊂ 3` and `1 ⊂ 2 ⊂ 4`.

Map the user's choice:

- Option 1 → **frames-only**: runs Phases 0 and 1 only, then prints the output directory.
- Option 2 → **insights-only**: runs Phases 0, 1, 3, 4, and 4.5.
- Option 3 → **full-diff**: runs Phases 0, 1, 2, 3, 4, 4.5, 5, 6. If the user hasn't already named target files, ask for them now (e.g. "Which files or folders should I compare the video against? You can pass paths like `src/components/Button.tsx` or globs like `src/styles/**/*.css`").
- Option 4 → **app**: runs Phases 0, 1, 3, 4, 4.5, and 4.6. No target files needed; no approval gate. Heaviest mode — the subagent walks the analysis, reads the `frontend-design` skill if installed, then writes a multi-file React project from scratch.

### Question 2 — Output location

Suggested phrasing:

> Where should I put the extracted frames and any exported artifacts?
>
> 1. **Working directory** — `./video-to-ui-<timestamp>/`. Keeps the output alongside your project so it's easy to commit, share, or hand to another tool. *(Recommended.)*
> 2. **Temp directory** — `/tmp/video-to-ui-<timestamp>/`. Auto-cleaned by the OS; good for one-off explorations you don't want to keep.

The user can pick "Other" to type a custom absolute path. If the path doesn't exist, create it. If it isn't writable, surface the error and re-ask.

`<timestamp>` is a Unix epoch (e.g. `1714502550`) so multiple runs don't collide. The chosen path is the canonical `<output-dir>` referenced everywhere else in this doc; frames go to `<output-dir>/frames/` and any exported artifacts go to `<output-dir>/` directly.

### When to skip the questions

Skip them only when the user has *unambiguously* stated their intent in their original message — phrases like "just extract the frames into ./frames" → frames-only with a custom path, "build me a frontend app from this video" / "scaffold a working app for this UI" → app mode, or a clear video + targets pair → full-diff. When in doubt, ask. The cost of asking once is small; the cost of running the wrong mode (especially the long subagent walks in options 2/3/4) is large.

After the answers are set, confirm in one short line — "okay, I'll just extract the frames into ./video-to-ui-1714502550/" — so the user can course-correct before the work begins.

## Phase 0: Verify ffmpeg

Run `${CLAUDE_SKILL_DIR}/scripts/check-deps.sh`. If it exits non-zero, surface its stderr (which contains per-OS install hints) to the user and stop cleanly. Do not try to work around a missing ffmpeg.

If the user provided a frames directory directly (Phase 1 will detect this), ffmpeg is not needed and you can skip the dep check.

## Phase 1: Extract frames (or skip if pre-extracted)

If the video path resolves to a **directory**, treat it as a folder of pre-extracted frames sorted lexically (`frame_*.png` or similar). Skip to the next phase that runs in the current mode.

Otherwise:

1. Probe duration with `ffprobe -v error -show_entries format=duration -of csv=p=0 "<video>"`.
2. Pick a default frame rate based on duration:
   - ≤ 2 minutes: 1 fps
   - 2–10 minutes: 0.5 fps
   - > 10 minutes: 0.25 fps (and consider asking the user for a tighter clip)
3. Compute the expected frame count: `duration_seconds * fps`. Apply the budget:
   - **≤ 120 frames** — proceed silently.
   - **121–300 frames** — print a one-line warning ("extracting N frames; this will take ~M minutes of subagent time") and proceed.
   - **> 300 frames** — refuse. Tell the user to lower fps or pre-extract a subset, and stop.
4. Run `${CLAUDE_SKILL_DIR}/scripts/extract-frames.sh "<video>" <out-dir> --fps <chosen-fps>`. The wrapper prints `extracted N frames to <dir>` on success — capture N for the budget check (the actual count may differ slightly from the predicted count).

Write frames to `<output-dir>/frames/`, where `<output-dir>` is the location chosen up front (working directory, `/tmp`, or a custom path). Create the directory if it doesn't exist. Tell the user the path so they can inspect or re-use it.

For marketing videos with rapid cuts, scene-detection mode is usually a better choice than fixed fps. Pass `--scene` to the wrapper instead of `--fps`.

**In `frames-only` mode, stop here.** Print one summary line — frame count, output directory, and a note that the user can pass that directory back to the skill later for analysis — and end the skill. Do not proceed to Phase 2 or Phase 3.

## Phase 2: Read target files (before walking frames)

*Runs in `full-diff` mode only. Skip in `insights-only` and `frames-only` modes.*


Read every file matching the user's target list. Use globs literally — the user's targets may be `src/components/Button.tsx` or `src/styles/**/*.css`.

While reading, note:

- Existing **design tokens** (CSS custom properties, theme objects, Tailwind config, design-token JSON, etc.).
- Existing **primitives** the targets compose (Button, Card, Stack, Icon, etc.).
- Existing **palette / type / spacing scale**.

This phase comes *before* frame walking on purpose: the diff list in Phase 4 needs to reference *existing* tokens by name rather than silently introducing parallel ones. Reading targets first means the synthesis can cite real names like `--color-surface-2` or `tokens.spacing.lg` instead of inventing.

## Phase 3: Walk frames in batches (2-tier subagent pattern)

*Runs in `full-diff` and `insights-only` modes. Skipped in `frames-only`.*

This is the context-saving heart of the skill. The main agent never reads raw frames — only the compact markdown summaries the subagents produce. This pattern is borrowed from `fabriqaai/ffmpeg-analyse-video-skill` and cuts context usage by roughly 90% on long videos.

1. List the frames in the frame directory, sorted lexically.
2. Group them into batches of **10** consecutive frames.
3. For each batch, spawn a disposable subagent **in parallel** (single message, multiple Agent tool calls) with `subagent_type: general-purpose`. Use the prompt template at `${CLAUDE_SKILL_DIR}/references/batch-analyzer.md`, with `{frame_paths}`, `{batch_number}`, and `{batch_output_path}` interpolated.
4. Each subagent reads the frame images, writes its analysis to `<frames-dir>/batch_NNN.md`, and returns a one-line confirmation (`wrote batch_003.md`).
5. After all subagents return, read the `batch_*.md` files in order. **Do not** read the raw frame images yourself — that defeats the whole pattern.

Batch size of 10 is empirical. Larger batches risk the subagent's vision attention spreading thin; smaller batches add coordination overhead. Adjust if the frames are unusually dense (many distinct screens per second) or sparse (long stretches of identical content).

## Phase 4: Synthesize artifacts

*Runs in `full-diff` and `insights-only` modes. Skipped in `frames-only`.*

Read `${CLAUDE_SKILL_DIR}/references/synthesis-checklist.md` first. It captures rules that are easy to forget after a long subagent walk.

Then, using the accumulated batch notes (plus the target-file contents from Phase 2 in full-diff mode), produce the artifacts in order. **In `insights-only` mode, produce only Artifacts 1 and 2** — skip Artifact 3, Phase 5, and Phase 6, and end the skill with a one-line note that no targets were provided so no diff list was generated.

### Artifact 1 — Design system observed

Extract from the batch notes:

- **Palette**: 6–10 hex colors, grouped by role (background / surface / text / accent / status).
- **Type scale**: heading sizes, body sizes, weights, family if guessable.
- **Spacing rhythm**: the spacing unit (4? 8? bespoke?) and its common multiples.
- **Corner radii**: the radius scale (often 2–4 distinct values).
- **Button styles**: primary, secondary, ghost — with their fills, strokes, radii, padding rhythm.
- **Card / surface styles**: elevation cues (shadow, border, gradient), padding.
- **Iconography**: line vs filled, weight, corner sharpness, size scale.

Format as a compact markdown section — bullet lists, hex codes, no prose paragraphs.

### Artifact 2 — Screen inventory

A chronological list of distinct screens observed, each with:

- A short name (the user can reuse this when discussing).
- A frame range (`frames 045–062`) so the user can re-watch.
- One line describing the screen's role.

### Artifact 3 — Diff list against the target files

*Produced in `full-diff` mode only.*

The deliverable. For each target file, a section like:

    src/components/Button.tsx (frames 012–034, 077–089)
    - Replace --button-radius from 4px → 8px to match the rounded-pill style in frames 014, 022, 081.
    - Switch primary fill from var(--accent-blue) → var(--accent-violet) (frame 028 shows the new accent).
    - Tighten vertical padding from 12px → 10px to match the denser button rhythm in frame 081.

**Every diff entry cites the frames that justify it.** This is non-negotiable — the user must be able to verify each recommendation by re-watching the cited frames.

**Reuse existing tokens.** If Phase 2 found `--color-primary` or `theme.button.radius`, the diff entry references those names rather than raw values. If the target has no token system, the diff list says so up front under a "Prerequisite" heading and recommends introducing one as a separate first step rather than silently inventing parallel tokens.

## Phase 4.5: Export artifacts

*Runs in `insights-only`, `full-diff`, and `app` modes (after Phase 4). Skipped in `frames-only`.*

Before printing the synthesized artifacts to chat, ask the user how they want them packaged. Use a single `AskUserQuestion` call with two questions (or a numbered fallback if AskUserQuestion is unavailable). **In `app` mode, skip Question 2** — the curated frame set is always copied because Phase 4.6 needs it as visual reference.

### Question 1 — Export format

> How should I package the analysis?
>
> 1. **Single combined markdown file** in the output dir (e.g. `<output-dir>/design-analysis.md`). Easiest to share. *(Recommended.)*
> 2. **Separate files per artifact** in the output dir — `design-system.md`, `screen-inventory.md`, plus `diff-list.md` in full-diff mode. Easier to revise individually.
> 3. **Print to chat only** — no files written. Pick this if you'll just read it once.
> 4. **Print + single file** — both.

### Question 2 — Curated frame set

> Also copy a curated frame set (one representative frame per distinct screen from the inventory) into `<output-dir>/screens/`? Useful if you'll hand them to a coding agent for replication.
>
> 1. Yes
> 2. No

### Acting on the answers

- **Single combined markdown file** / **Print + single file**: write all artifacts to `<output-dir>/design-analysis.md` with a short header naming the source video, run timestamp, and frames directory.
- **Separate files per artifact**: write `<output-dir>/design-system.md` (Artifact 1) and `<output-dir>/screen-inventory.md` (Artifact 2). In `full-diff` mode, also write `<output-dir>/diff-list.md` (Artifact 3).
- **Print to chat only**: skip file writes. (In `full-diff` mode, the artifacts are still printed in Phase 5 for the approval gate.)
- **Curated frame set = Yes** (or `app` mode, where it's auto-yes): for each entry in Artifact 2 (Screen inventory), copy the **first frame** of its primary frame range from `<output-dir>/frames/` to `<output-dir>/screens/screen_NN_<snake-cased-name>.png`. `NN` is the inventory order, zero-padded to 2 digits. If the entry lists multiple ranges (e.g. "frames 005, 008 (reappears 011–013)"), use the very first frame number — here, `005`.

In `app` mode, after the export writes complete, proceed to **Phase 4.6**. Tell the user once: "I'll also copy the curated frame set since the app needs it as reference" — they didn't pick that question, so explain why it happened.

In `full-diff` mode, **always also print the artifacts to chat** regardless of the format choice — the approval gate (Phase 5) needs them visible. The format choice only controls whether files are also written.

If the user requests refinements in Phase 5 and you re-print the diff list, also re-write the corresponding file (so the on-disk record matches the final state).

## Phase 4.6: Build frontend app

*Runs in `app` mode only (after Phase 4.5). Skipped otherwise.*

Spawn a single dedicated subagent (`subagent_type: general-purpose`) to scaffold and write a working frontend app at `<output-dir>/app/`. This is a real app — multi-file, framework-based, with a build step — that recreates the UI's *behavior*, not just its appearance. Every interaction the video shows must work in code, not as a visual stub.

### Stack (non-negotiable)

Pick this stack and commit. Don't substitute, don't ask the user.

- **Vite** as the build tool
- **React 18** with **TypeScript**
- **Tailwind CSS**, configured to extend the theme with the design tokens from Artifact 1
- **react-router-dom** for client-side routing between screens
- **Framer Motion** for sequenced reveals, sliding sheets, status-line streaming, rotating progress arcs, toasts — anything in the video's animation language. Plain CSS keyframes are acceptable for trivial cases.

The user can swap things later. The skill's job is to produce one stable, predictable, idiomatic baseline.

### What to give the subagent

Pass the subagent a self-contained brief that includes, inline:

- The full **Artifact 1 (Design system observed)** text — palette, type scale, spacing, radii, button styles, surfaces, iconography, signature motifs, animation language.
- The full **Artifact 2 (Screen inventory)** text — every distinct screen with its frame range and one-line role.
- The path to `<output-dir>/screens/` (curated frame set) as visual reference. Tell the subagent to *read each curated frame* before drafting that screen's component.
- The path to write the app to: `<output-dir>/app/`.
- The viewport intent — **mobile** (route layout wraps each screen in a `<PhoneFrame>`) or **desktop** (full viewport). Infer from the curated frames.
- **Instruct the subagent to use the `frontend-design` skill if available.** Before writing any code, the subagent should look for `frontend-design/SKILL.md` in this priority order: (1) project plugins at `.claude/plugins/*/skills/frontend-design/SKILL.md`, (2) user plugins at `~/.claude/plugins/*/skills/frontend-design/SKILL.md`, (3) the project's own `.claude/skills/frontend-design/SKILL.md`, (4) `~/.claude/skills/frontend-design/SKILL.md`. If found, the subagent reads it in full and applies its component-quality, layout, and aesthetic guidance on top of the design tokens extracted from this video. The video supplies the *signal* (tokens, screen inventory, animation language); `frontend-design` supplies the *craftsmanship* (component composition, micro-interactions, visual polish). If `frontend-design` isn't installed, the subagent generates from the video signal alone — don't fail, don't ask the user to install it, just proceed and note in the summary that the output would be richer with `frontend-design` available.

### Required output structure

```
<output-dir>/app/
  package.json              — pinned versions, scripts (dev/build/preview)
  vite.config.ts
  tsconfig.json
  tailwind.config.ts        — theme.extend with tokens from Artifact 1
  postcss.config.cjs
  index.html
  README.md                 — install (npm install) and run (npm run dev) instructions
  src/
    main.tsx                — Vite entry
    App.tsx                 — top-level layout + router
    router.tsx              — route definitions, one per screen
    styles.css              — Tailwind imports + any global styles
    components/             — shared (PhoneFrame, BottomNav, Button, Card, Toast, ChatBubble, etc.)
    screens/                — one component per distinct screen from Artifact 2
    lib/
      mockApi.ts            — simulated backend behaviors (chat streaming, ingredient logging, etc.)
      animations.ts         — Framer Motion variants if shared across screens
```

### Subagent constraints (non-negotiable)

- **Match interactions, not just visuals.** If the video shows an ingredient checklist where tapping items toggles them and a "Logged Successfully" toast appears, that's a real `useState` hook plus a real `<Toast />` component, not a static screenshot.
- **Mock the backend with realistic timing.** When the video shows the chat agent streaming `Trying to Get User Info…` then `Trying to Create Workout Plan Draft…`, the mock API yields those status lines on a `setTimeout` chain that mirrors the video's pacing. Don't fake it as a single instant render.
- **Design tokens go in `tailwind.config.ts`** under `theme.extend.colors`, `theme.extend.spacing`, `theme.extend.borderRadius`, etc. Reference them by name in components (e.g. `bg-surface-1`, `text-accent-teal`, `rounded-card`). Don't sprinkle raw hex codes through `className`.
- **Implement every screen in Artifact 2.** Don't stub. If a screen's interactions aren't fully visible from the frames, infer reasonable behaviors and add a one-line code comment explaining the inference.
- **Pin versions.** No `^`, no `latest`. Pinning means `npm install` six months later still produces the same tree.
- **Don't fabricate content the video didn't show.** Preserve real names, copy, exercise names, etc. from the frames.
- **Phone-frame chrome only at the route-layout level**, never inside individual screen components. Same antipattern called out in Phase 6.
- **Vanilla framework only — no extra dependencies beyond the stack above.** No UI kits (no shadcn, no MUI, no Chakra), no state libraries (no Redux, no Zustand) unless a clearly-shown video flow can't reasonably be expressed without one. Default to React's built-in primitives.
- **The subagent writes files only — no `npm install`.** Tell the user to run `cd <output-dir>/app && npm install && npm run dev` themselves.

### After the subagent returns

- Verify the structure: `package.json`, `src/main.tsx`, `src/App.tsx`, `tailwind.config.ts`, and at least one screen component per Artifact 2 entry must exist.
- Print one short summary to chat: where the app is, how many screens it implements, the run commands (`cd <output-dir>/app && npm install && npm run dev`), and any inferences the subagent made about behaviors not fully visible in the video.
- Don't run `npm install` for the user automatically — they may want to inspect first.

If the subagent returns a partial app (some screens stubbed, some animations missing), surface that honestly: "App scaffolded at `<path>` covering N of M screens; the rest are placeholder components." Don't claim full coverage that isn't there.

## Phase 5: Approval gate

*Runs in `full-diff` mode only.*

Print the three artifacts in order — this happens regardless of the export-format choice from Phase 4.5, since the approval gate needs them visible in chat. If files were written in Phase 4.5, mention the path(s) in the same message so the user can review them while deciding. Then stop with:

> **Diagnosis complete.** Reply `apply` to make these edits, or send refinements (e.g. "skip the spacing changes", "use the violet accent only on primary buttons").

**Do not edit any files yet.** Diagnosis is the deliverable; edits come only on explicit approval. If the user pushes for autonomous edit without diagnosis, decline politely — the gate is core to the skill's value.

If the user sends refinements, regenerate the diff list, re-print it, and re-write the on-disk file (if any was written in Phase 4.5) so the artifact stays in sync with the final state.

## Phase 6: Apply edits (only after explicit approval)

*Runs in `full-diff` mode only, after the user replies `apply` in Phase 5.*

Once the user replies `apply`:

- Edit each target file using the existing token names found in Phase 2. Never silently introduce parallel design tokens.
- **Do not draw fake device chrome** (status bars, tab bars, iOS notches) into editorial / illustrative components, even if the frames show them. Fake-screenshot vibe in marketing pages is a known antipattern. Exception: targets that already contain such chrome.
- After editing, summarize what changed file-by-file with line-anchor links so the user can review.

If the user replied with refinements rather than `apply`, integrate the refinements first and reprint the diff list. Only edit after a clean `apply`.

---

## Failure modes & guidance

- **No tokens in target**: surface this in the diff list ("targets have no token system; consider introducing one before applying these changes") rather than inventing.
- **Frames look identical for long stretches**: the subagent prompt collapses identical adjacent frames; if synthesis still feels sparse, suggest the user re-record at a higher fps for the relevant segment.
- **Marketing video with rapid cuts**: pass `--scene` to `extract-frames.sh` (scene-detection mode) instead of fixed fps.
- **Video and target palettes are completely different families** (e.g. target is warm neutrals, video is cool blues): don't try to half-merge. Flag it in the diagnosis and ask whether to fully migrate or hold off.
- **Video shows screens the targets don't have**: flag as out-of-scope rather than inventing a redesign.

## Bundled resources

- `scripts/extract-frames.sh` — ffmpeg wrapper with `--help`, validation, and `--scene` mode.
- `scripts/check-deps.sh` — ffmpeg/ffprobe presence check with per-OS install hints.
- `references/batch-analyzer.md` — disposable-subagent prompt template (read before spawning Phase 3 subagents).
- `references/synthesis-checklist.md` — rules for the synthesis phase (read before Phase 4).

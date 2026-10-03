---
name: visual-lint
metadata:
  version: 0.1.2
description: Screenshot UI defect lint
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Agent
---

# /visual-lint — Baseline-free rendered-UI defect detection

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code. The `Agent`-launched `web-designer` adjudicator maps to a Codex sub-agent spawn; if unavailable, run the rubric inline (lightweight mode).

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`Agent` sub-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed; `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool`. Map `~/.claude/...` to `~/.cursor/skills/` unless the task explicitly targets Claude Code.

Screenshot a running app, run a structured defect rubric over the rendered pixels,
and produce a findings report with cited evidence. **Fixing is out of scope — this
skill reports.** Hand the report to a session that owns the source if the user wants
the issues fixed.

## Why this exists

`lint` and `typecheck` catch code-level problems the instant you save. But a whole
class of bugs lives only in **rendered pixels** and is invisible to every static
tool:

- A value readout `83% / 15px` wraps onto two lines because a fixed-width span
  (`w-14`=56px) is narrower than its ~75px content. The code is type-correct and
  lint-clean — the breakage exists only on screen. *(This skill's calibration fixture:
  `references/fixtures/opacity-blur-wrap.png`.)*
- A label overflows its container at a narrow window width.
- Two elements overlap after a content change.
- A row's spacing drifts off the grid.

Today these get fixed only when a human notices and points them out. This skill
codifies that human "that looks broken" judgment into a repeatable rubric so a model
can catch it the way ESLint catches an unused variable.

**Why VLM judgment, not a visual-regression tool:** every mainstream visual-testing
tool (Applitools, Percy, Chromatic, Playwright `toHaveScreenshot`) is a
**baseline-required regression detector** — it diffs against a saved golden image and
therefore *cannot* flag a first-occurrence bug. The goal here is to catch *new*
breakage with *no* baseline, which only spec-driven geometry or **vision-language-model
judgment** can do. v1 uses VLM judgment.

**Where it sits among sibling skills:**

| Skill | Question it answers |
|-------|---------------------|
| Functional QA | Does it *function*? (clicks work, IPC fires, state persists) |
| `/design-review` | Is it *aesthetically good*? (hierarchy, polish, AI-slop) — and it *fixes* |
| **`/visual-lint`** | **Is the *render broken*?** (wrap, overflow, overlap, misalign) — read-only |

## Scope and non-goals

**In scope (v1, pure-VLM):** detecting *display defects* in the rendered pixels of a
running app — unintended wrapping, truncation/clipping, element overlap, containment
overflow, gross misalignment, off-grid spacing, broken/missing assets, contrast and
target-size problems, theme/mode bleed, and state-dependent breakage (modal, hover,
context menu, drag, scroll).

**Out of scope:**
- **Fixing.** This skill is read-only (see contract below). It reports.
- **Aesthetic scoring / "is it beautiful".** That's `/design-review`.
- **Functional testing / "does it work".** Use browser automation or manual QA separately.
- **Sub-10px geometric precision** (exact spacing rhythm, 1–3px offsets). VLMs are
  weak at this — it is explicitly deferred to **Hybrid v2** (a deterministic
  `getComputedStyle`/`getBoundingClientRect` + `axe-core` + token-diff pre-pass that
  feeds the VLM bounded confirm/reject questions). v1 does **not** build that layer;
  for measurable claims the rubric reports "borderline — needs measurement", never a
  fabricated number.

## 🔒 Read-only contract (non-negotiable)

This skill MUST NOT:
- edit, format, or otherwise modify any source file,
- run `git commit`, `git add`, or any state-changing VCS command,
- run a code formatter, codemod, or autofix.

It MAY only: read source, drive the running app via `playwright-cli`, capture
screenshots, and **write a single report file** under `./visual-lint-reports/`.
`allowed-tools` deliberately omits `Edit` to enforce this at the tool layer. If a user
wants fixes, this skill's output is the input to a separate fixing session.

## Required context before starting

Gather these; if any is missing and not inferable, ask once via `AskUserQuestion`:

1. **Target** — a running app reachable by `playwright-cli`. Default assumption:
   an Electron app exposing CDP on `http://localhost:9222` (the skills-desktop
   convention: `pnpm dev` exposes it). For a web app, a URL + a browser context.
2. **Scope** — "whole app" vs a specific screen/flow ("Settings → Appearance").
3. **Design source** — auto-detect `./DESIGN.md` in the target project. If present,
   project-aware mode activates (see `references/design-system-criteria.md`); if
   absent, fall back to the generic rubric. Do not ask — detect.

## Executor: web-designer (primary) vs lightweight inline

Adjudication needs a vision-capable agent that reads the screenshots and applies the
rubric. Two modes:

- **Primary — `web-designer` subagent.** Launch via the `Agent` tool
  (`subagent_type: web-designer`). It owns capture + judgment end-to-end, reading this
  skill's `references/`. Use it for a full pass: a professional design eye applies the
  DESIGN.md criteria most faithfully. This is the user's stated default.
- **`--lightweight` — inline.** The main Claude agent runs the same rubric itself
  (Claude is vision-capable; this was proven to catch the calibration fixture cleanly).
  No subagent spawn → faster and cheaper. Use for a quick single-screen check, when
  iterating, or when subagent overhead isn't worth it.

Same rubric, same report either way. If the user passes `--lightweight`, run inline;
otherwise default to `web-designer`. (If the per-run subagent cost proves not worth it
in practice, flipping the default to inline needs no code change.)

## Workflow

### Phase 0 — Preflight
1. Ensure no stale driver session: `playwright-cli list`; detach/`kill-all` if wedged.
2. Ensure the target app is running with its debug surface. For skills-desktop:
   `kill-port 9222` if a prior `pnpm dev` died unclean, then `pnpm dev`.
3. Attach: `playwright-cli attach --cdp=http://localhost:9222`. All later commands use
   `--s=default`.
4. Detect `./DESIGN.md`; note project-aware vs generic mode in the report header.

### Phase 1 — State plan (present before capturing)
Derive the list of UI states to capture per `references/ui-state-coverage.md`:
the always-on default-state full-window pass **plus** the five operation-path states
(modal / context-menu / drag / scroll / hover) where reachable. Output a short
per-screen state plan table *before* capturing so the run is auditable.

### Phase 2 — Capture
For each planned state, capture a full-window screenshot via `playwright-cli`. **Capture
resolution caveat:** playwright-cli hardcodes `scale: 'css'`, so the PNG is **1× CSS
resolution** (~1400×941 on this app), *not* the 2× device pixels of a DPR-2 render —
`window.devicePixelRatio` reports `2` but that does not change the captured file. For
dense or borderline regions, take an element-scoped or CSS-`zoom` crop (see **Capture
recipes** below) and re-judge from that. Re-`snapshot` after any DOM-mutating action —
`eN` refs are valid only for the latest snapshot. Save shots under the report's
`screenshots/` dir.

### Phase 3 — Adjudicate
Apply, in this order, against every screenshot:
1. `references/anti-false-positive.md` — the process rules that bound the judgment
   (describe-before-judge, **cite-or-drop**, enumeration-not-quota, low-confidence →
   question, adversarial self-check). Read this first; it governs everything.
2. `references/defect-rubric.md` — categories A–F. Each item is a direct verification
   prompt. Every finding uses the 4+1 scaffold: `element · defect · expected_vs_actual
   · severity · confidence`.
3. `references/design-system-criteria.md` — in project-aware mode, fold the DESIGN.md
   tokens in as perceptual checks (e.g. status-green must survive the neutral theme;
   no shadow on resting cards). In generic mode, skip the project-specific rows.

### Phase 4 — Report
Emit `templates/visual-lint-report.md` to
`./visual-lint-reports/{YYYYMMDD}-{scope}.md` (screenshots in a sibling
`screenshots/` dir). Group findings by severity. End with the read-only footer.
Then detach: `playwright-cli --s=default detach` (does **not** close the app).

## Capture recipes (project-aware)

**Electron (primary — skills-desktop CDP `:9222`):**
```bash
playwright-cli list                                   # check for stale sessions
playwright-cli attach --cdp=http://localhost:9222     # attach once per run
playwright-cli --s=default snapshot                   # a11y tree with eN refs
playwright-cli --s=default screenshot --filename=./visual-lint-reports/<run>/screenshots/<state>.png
playwright-cli --s=default click e5                   # interact by ref from latest snapshot
playwright-cli --s=default fill e3 "text"
playwright-cli --s=default press Escape
playwright-cli --s=default eval 'window.devicePixelRatio'   # reports 2, but PNG stays 1× CSS (scale:css hardcoded) — NOT a resolution check
playwright-cli --s=default detach                     # leaves the app running
```

**Web app (documented alternate):** open a browser context to the URL instead of CDP
attach; the screenshot/snapshot/interact verbs are otherwise identical. The rubric and
report are capture-method-agnostic.

## Calibration (dev-time, not per-run)

Two worked-example bugs anchor the rubric, each paired with an `.expected.md` target:
- `references/fixtures/opacity-blur-wrap.png` — the **wrapping** anchor: the
  `83% / 15px` readout wraps onto two lines (severity 2, high confidence, citing both
  lines; rubric A1/A7, home B).
- `references/fixtures/symlink-health-clip.png` — the **clipping** anchor: the large
  `100%` value in the "Symlink Health" card is sliced at the card's top content edge
  (severity 2–3, high confidence, citing the `100%` value; rubric A3, home B1/B3).

When you **change this skill's rubric**, run it once against **both** PNGs and confirm
each still emits its expected finding. A rubric edit that stops catching either fixture
is a regression — fix it before shipping. This is a construction-time anchor; normal
`/visual-lint` runs do not re-run it.

## Pre-flight checklist
- [ ] Driver attached, no stale session, target app responsive.
- [ ] `./DESIGN.md` detection resolved (project-aware vs generic noted in report).
- [ ] State plan table presented before capture.
- [ ] Screenshots full-window; dense/borderline regions have a zoom crop (captures are 1× CSS via playwright-cli, not 2× device px).
- [ ] Colored badge/chip labels checked against their own backgrounds and any explicit foreground requirement (E7); available light/dark variants captured per `ui-state-coverage.md`.
- [ ] Every finding cites a visible element (cite-or-drop honored).
- [ ] Report written under `./visual-lint-reports/`; **no source edits, no commits.**
- [ ] Driver detached (app left running).

## References
- `references/defect-rubric.md` — what to look for (categories A–F + finding scaffold).
- `references/anti-false-positive.md` — how to judge without hallucinating (read first).
- `references/ui-state-coverage.md` — which states to capture (default + 5 op paths).
- `references/design-system-criteria.md` — DESIGN.md tokens as perceptual checks.
- `references/fixtures/opacity-blur-wrap.{png,expected.md}` — wrapping calibration anchor.
- `references/fixtures/symlink-health-clip.{png,expected.md}` — clipping calibration anchor.
- `templates/visual-lint-report.md` — the read-only report skeleton.

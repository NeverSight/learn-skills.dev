---
name: create-verification-skill
description: Use when a project has no scripted way to prove UI/CLI/service behavior end to end, or when an existing generated verify-<app> skill needs a new or updated feature added to its map. Generates (or incrementally updates) a project-local verification skill (.agents/skills/verify-<app>/) that launches the real app, drives one feature the way a user would, and captures evidence. Triggers include "make a control skill for this repo" and being invoked by speckit-auto's Stage 05 with an already-generated skill present.
compatibility: Runs on GitHub Copilot, Claude Code, and OpenCode. Requires the target project to be buildable/runnable locally; requires whatever browser/CDP, PTY/tmux, or HTTP tooling the chosen harness needs.
license: MIT
allowed-tools: bash glob grep view create edit
metadata:
  author: Alex Nguyen
  version: "0.1.0"
---

# Create a verification skill

Every serious project needs a scripted way to drive the real app and prove behavior: launch it, exercise a feature the way a user would, and capture evidence. This skill generates that as a project-local skill (`.agents/skills/verify-<app>/`) tailored to the repo, or incrementally updates one that already exists. You write the generator's output for the next agent, not for a human: it will be read cold, mid-task, by an agent that has never seen the app.

## 0. Choose create mode or update mode

- **No `.agents/skills/verify-<app>/` exists yet** (or the caller says so explicitly) → **create
  mode**: run Steps 1-5 below in full.
- **`.agents/skills/verify-<app>/` already exists** and the caller names one specific feature that
  was just added or changed (this is how `speckit-auto`'s Stage 05 calls this skill, once per
  implemented feature) → **update mode**:
  1. Read the existing `SKILL.md` and `features/README.md`.
  2. Run only the parts of Step 1 (Interview) needed to describe the named feature — do not
     re-interview the whole app's surface/run/drive/observe/isolate story unless the named feature
     genuinely changes one of those (e.g. it adds a new port, a new auth mode, a new harness).
  3. Write or overwrite exactly one file: `features/<feature-slug>.md` for the named feature,
     following the same shape as every other feature file (Step 3 below). Add its entry to
     `features/README.md`'s index if it's new; update the existing index line if the feature
     already existed.
  4. Touch `SKILL.md` itself **only if** Launch, Doctor, Drive, Evidence, Cleanup, or Helpers
     actually changed because of this feature (a new command, a new port, a new harness) —
     otherwise leave it untouched. Never regenerate `SKILL.md` wholesale in update mode.
  5. Run Step 4 (Prove) scoped to only this one feature file, not the whole map. **Exception:**
     when this update-mode call is made by `speckit-auto`'s Stage 05, skip Step 4 entirely — Stage
     05 §3 is itself the real proof, driven against the full running app, and Stage 05/06 own the
     cleanup timing; running Step 4 here as well would double-drive the app and could tear down an
     instance Stage 06 still expects to clean up.
  6. Skip Step 5 (Offer the maintenance loop) — already offered at create time.

## 1. Interview the repo, not the user

Answer these from the codebase and only ask the user what you cannot observe:

- **Surface:** what does a user actually touch? A web UI, a CLI/TUI, a desktop app, an API, a mobile app, a library? A repo can have several; pick the primary one and note the rest.
- **Run:** how does the app start locally? Prefer the repo's own documented dev command (package scripts, Makefile, README quickstart). Note ports, env vars, seed data, auth.
- **Drive:** how can an agent interact with it programmatically? Existing harnesses first — Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port. Only then pick a generic recipe: browser/CDP for web and Electron, a tmux/PTY harness for CLI/TUI, plain HTTP for services.
- **Observe:** what evidence can be captured? Screenshots, terminal transcripts, response bodies, logs, exit codes, DB state.
- **Isolate:** can two instances run side by side (ports, data dirs, profiles)? If not, say so in the generated skill: refusing to double-drive a shared instance beats corrupting the user's session.

If the checkout doesn't build or start as-is, fix that first (or report it precisely) before generating; a skill written against a broken base teaches wrong steps. When an irrelevant missing asset blocks startup (a static dir the API never serves, a sample config), the generated skill may create it, clearly marked as verification scaffolding, and remove it in cleanup.

## 2. Generate the skill

Write `.agents/skills/verify-<app>/SKILL.md` with YAML frontmatter (`name: verify-<app>` and a `description` that names the app, the surface, and when to reach for it — without frontmatter the skill never registers) and these sections, each grounded in what the interview actually found (no placeholders left):

- **Launch:** the exact command that starts the app for verification, and how to tell it's ready (a log line, a port answering, a prompt). Include teardown. For a short-lived CLI or TUI there is no server to keep alive: launch means build the binary (or install deps) once, then start each drive in its own isolated PTY or tmux session.
- **Doctor:** one read-only check that answers "is this instance worth driving?" — process up, right version/build, port owned by us, auth valid. An agent runs this first whenever anything looks off.
- **Drive:** the harness recipe with real selectors/commands from this repo, not examples. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths) over coordinates and tab order.
- **Evidence:** what to capture for a proof and where it goes. State the proof standards: exercise the real user path, not internal setters or test-only endpoints; capture the action and the resulting state, not just the final screen; verify side effects (files written, rows inserted, messages sent) alongside what's visible; mocks only where a production boundary already isolates the external system. When the safe path is a dry-run or test mode, verify what it actually skips by observing (files, network, git refs) rather than trusting its name: some dry-runs still touch the network or open a browser.
- **Cleanup:** how to tear down instances the run created. Never kill by process name; kill what you started. Cleanup removes instances and scratch state, never the evidence: proof artifacts survive the teardown, in a location the skill names.
- **Helpers:** any script the skill ships is executable and its invocation is shown in the skill body. A helper the reader has to reverse-engineer is not a helper.

## 3. Seed the feature map

Create `.agents/skills/verify-<app>/features/README.md` plus one file per user-facing feature you can identify (aim for the top 3-5 to start, from routes, commands, menus, or docs). Follow the shape in [`references/feature-map-example/`](references/feature-map-example/), with a README index and one file per feature. Each file answers, from the user's point of view: what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works. The four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. The map is the repo's maintained verification source; a proof that drives one convenient entry point is incomplete when the map lists others.

## 4. Prove the generated skill before handing it over

Run its own instructions end to end once: launch, doctor, drive ONE mapped feature (one is enough in create mode; exactly the named feature in update mode), capture evidence, clean up. After cleanup, confirm the evidence still exists at the named location — a cleanup that eats the proof fails this step. Fix what fails, and run the generated cleanup after every failed iteration too, so broken attempts don't strand processes and ports. A generated skill that was never executed is a draft, not a deliverable.

## 5. Offer the maintenance loop (create mode only)

Tell the user how to keep the map honest as the app changes: re-invoke this skill in **update
mode**, naming the changed or new feature, whenever a feature's behavior, launch, or drive path
changes. Suggest a cadence only if they ask.

## References

- [Feature map example](references/feature-map-example/README.md)

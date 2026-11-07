---
name: sdlc-fix
description: >-
  Fix a bug, tweak, or small behavior change in an existing flow without an
  intent folder: reproduce, change, verify, commit. Use for anything bounded and
  low-consequence. New capabilities go to sdlc-plan; consequential changes go
  to sdlc-plan as a critical intent. Do not push unless asked.
license: MIT
metadata:
  author: acourtiol
  version: "3.0"
---

# sdlc-fix

The default path. Most requests are fixes: a bug, a label, a layout, a behavior tweak in a flow that already exists. No `intent/` folder, no approval gate. Reproduce, change, verify, commit.

## Does it fit?

Fits: a bug in a readable existing flow; a behavior-preserving refactor; copy, layout or styling; a small behavior change you can state in two sentences that stays inside one flow.

Does not fit, so switch to `sdlc-plan` and say why: a new capability or surface, an open product decision, work across several subsystems, or anything that needs a screen, input or gate the user did not ask for.

**Consequential** changes need an independent review before they are done, so they also go to `sdlc-plan` (tier `critical`): a migration on populated tables, auth, secrets, privacy or PII, destructive or irreversible operations, LLM prompts or gates that change generated content or approval, anything that sends data externally, scraping policy. Judge by impact if wrong, not by line count.

## Steps

1. **Ownership.** Run `git status --short`. Other people's or agents' dirty files are theirs: never reset, stash or stage them. If your files overlap, ask or use a separate worktree.
2. **Reproduce.** A failing test, or an observed repro you can name. For UI, see it in the running app (local, never production).
3. **Root cause, smallest change.** Reuse existing patterns and installed dependencies before adding code. Do not add abstractions, settings, screens or gates nobody asked for. A workaround that hides the cause is not a fix. Keep validation, error handling, security and accessibility.
4. **Verify.** Run the focused tests (check that the runner actually discovers them, including component tests), typecheck and lint for what you touched. For UI, drive the main path and one error path in the running app. For a changed shared contract, run its other callers' tests.
5. **Commit** one coherent change: `type(scope): imperative summary`, blank line, one sentence of why. Put the evidence (what you ran, what you saw) in the commit body when it is not obvious. Stage only your paths. Do not push or deploy unless asked.
6. **Report** in a few lines: what was wrong, what changed, what you ran and saw, anything not checked.

If investigation shows the problem is bigger or consequential, stop, say so, and move to `sdlc-plan`. Do not disguise expanded scope as a fix. After two failed attempts of the same kind, stop and reproduce the failure narrowly before trying again.

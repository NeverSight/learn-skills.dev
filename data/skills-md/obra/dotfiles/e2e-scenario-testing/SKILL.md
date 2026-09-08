---
name: e2e-scenario-testing
description: Use when verifying a running application end-to-end through its real interface — a web UI, a CLI, or a TUI — by writing and executing agent-run "scenario cards" against a freshly built instance with falsifiable assertions. Trigger on "test it end to end", "prove the UI actually works", "write/run a scenario", or after a change touches a user-facing surface that unit tests can't fully cover. Not for unit tests, pure code review, or API-only checks.
---

# End-to-end scenario testing

Verify that a *running* application does what it claims, by driving its real
interface the way a user would. The unit of work is a **scenario card**: a
short markdown test written for an agent to execute — not a Playwright/expect
script. Cards are high-level enough that a small UI shuffle doesn't invalidate
them, but precise enough that two agents running the same card reach the same
verdict.

A green unit test proves the wiring in isolation. A scenario proves the wiring
*as assembled and rendered*. They catch different bugs — write the card even
when the unit tests pass.

## When to use this

- A feature touches a user-facing surface (button, palette command, status
  indicator, keybinding, rendered message) and you want proof it works live.
- The user asks to "test it end to end" / "prove the UI works" / "run a scenario."
- You changed a layer (projection, capability gate, renderer) whose effect is
  only observable in the assembled UI.

Don't use it for logic with no UI surface (unit-test that), or when a
production gate makes the live path unreachable (see *Over-specification* below).

## The card format

One card = one `.md` file. Keep these sections; collapse any to one line when
the scenario is simple. Don't pad.

```markdown
# <area>-<behavior>: one-line title

**What this covers**: the feature + the specific commits/IDs it exercises.
If something else breaks this, it should be caught here.

## Pre-state
What must be true before starting: a freshly built instance running, auth/creds
in place, a clean workdir. Give the exact commands to reach it.

## Steps
Numbered actions described by **intent**, each with the concrete command or
tool call and a real UI label (prefer labels the user sees over brittle
selectors like `#nav > li:nth-child(3)`).

## Expected
For each step, what you should observe — and the **falsification condition**:
"if you see X instead, the test fails." Silence is not success.

## Cleanup
Idempotent teardown so reruns are hermetic. Never touch state you didn't create.

## Sharp edges
Footguns, timing/ordering caveats, nondeterminism noted while recording.
```

## Running a card

1. **Build fresh from the code under test.** The single most common mistake is
   testing a stale binary. Rebuild every layer your change touches (server,
   client, embedded assets) and confirm the running instance is the new one,
   not a process someone left up yesterday.
2. **Isolate.** Run in a hermetic workdir. If the app holds a host-level
   singleton (a lock, a fixed port, a shared state dir), point the test
   instance at its own copy — e.g. override `$HOME`/state-dir/port — so it can
   neither collide with nor pollute (nor be polluted by) a real instance.
   Symlink shared read-only inputs (creds, tokens); keep mutable state separate.
3. **Drive the surface** (recipes below).
4. **Assert against the authoritative record, not just the pixels.** The UI can
   lie or lag; the on-disk state / log / database is ground truth. Cross-check
   the rendered claim against it when an assertion is ambiguous.
5. **Capture evidence** — a screenshot, the captured pane, the on-disk artifact.
6. **Clean up** — shut down what you spawned, remove scratch dirs, leave
   pre-existing instances running and untouched.

## Driving a web UI (browser)

Use a Chrome/CDP browser tool. After authenticated navigation, drive the page
through `eval` against the app's own JS entry points rather than synthesizing
clicks where possible — it's more robust to layout change.

- **Optimistic-vs-settled** assertions: fire the action but *don't await it*,
  take a synchronous DOM snapshot (the pending placeholder is there *now*),
  then await and snapshot again. Without the no-await capture you can't tell
  "rendered then reconciled" from "never rendered."
- Return a **plain string** from `eval` (join your findings with `\n`); some
  bridges stringify a returned object as `[object Object]`.
- Inspect internal state via the app's singleton (`window.<App>?.state`, etc.)
  when the DOM is ambiguous.

## Driving a CLI / TUI (tmux)

Each scenario gets its own named tmux session (cleanup needs a deterministic
name). Fix the size for deterministic capture; prefer the app's plain-text/inline
mode if it has one.

```bash
tmux new-session -d -s <name> -x 200 -y 50 "<cmd> 2>/tmp/<name>-stderr.log"
tmux send-keys -t <name> -l "literal text"   # -l = no key-name parsing (paths, slashes)
tmux send-keys -t <name> Enter
tmux capture-pane -t <name> -p                # -p = plain text; add -e only for styling
```

- Always `-l` for user-typed strings; without it `/foo/bar` parses as escapes.
- Poll `capture-pane` for a state string; grep the **glyph/word**, not the color.
- Redirect stderr to a file — panics and debug probes land there, not the pane.

## Hard-won principles

- **Falsification, always.** Every assertion states what failure looks like. A
  step that can't fail proves nothing. When watching for an outcome, make sure
  your check would fire on the failure path, not just the happy path.
- **Verify the *right* surface.** The same concept often exists at several
  layers (an internal capability vs. the REST projection of it; a model field
  vs. the rendered chip). Confirm your assertion reads the surface that actually
  carries the signal — a "missing" value is often present one layer over.
- **Present but not visible ≠ absent.** Scrollable bodies, virtualized lists,
  and auto-scroll-to-bottom routinely push a real element out of the capture
  window. Before concluding something didn't render, scroll/expand to where it
  should be. Confirm via a sibling read (a status command reading the same
  state) when the visual is hard to capture.
- **Executing the card tests the card.** Expect to find bugs in your own
  scenario — a wrong selector, a wrong layer, an assertion the UI can't show.
  Fix the card as you go; a card that "passes" because its check was vacuous is
  worse than none.
- **Over-specification trap.** A card can describe a path that production gating
  prevents (e.g. a keybind that's a no-op in the current mode). Confirm the gate
  in the source rather than fighting it through the UI; verify the underlying
  behavior with a unit test and note the gate in the card.
- **Cleanup is part of the test.** A half-shutdown fleet makes the next run's
  polling return false positives. Make teardown idempotent and scoped to what
  you created.

## Finishing

Report each assertion as pass/fail with the concrete observation (the rendered
text, the on-disk value), not "looks good." If a card fails, capture the
evidence and either fix the bug or file it; don't soften the verdict.

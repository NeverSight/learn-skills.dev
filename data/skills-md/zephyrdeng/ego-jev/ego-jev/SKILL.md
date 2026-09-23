---
name: ego-jev
description: "Jev (TypeSafe System One) inner loop for ego-browser — one ~0.4 s typed decision per DOM step instead of an LLM turn. Use for multi-step clicking through a semantic page: fill known values into a form, set filters, open a row/card/menu by name, reach a page via nav or site search. Escalates login, payment, free text, canvas and content reading back to you."
license: MIT
metadata:
  version: "0.3.2"
---

# ego-jev

ego executes; Jev decides. Each step: snapshot → number the interactive
elements (a11y refs `@N` + DOM-discovered clickables `dN`: `div` cards,
`cursor:pointer`, iframe/shadow content) → one System One call picks the
operation and its target together → ego clicks/fills/selects. Jev never writes
text and never sees a screenshot.

Read `ego-browser` first for TaskSpace and Page rules; this skill only replaces
the per-step "which element" judgment.

Requires: [ego lite](https://lite.ego.app/) installed and onboarded (provides
the `ego-browser` command), the `ego-browser` skill, and `TYPESAFE_API_KEY` or
`AI_GATEWAY_API_KEY` in `~/.config/ego-jev/secrets.env`.

## Run

1. Have a Page on the starting URL (`goto` with `waitUntil: "domcontentloaded"`
   on slow marketing sites; the default `load` times out at 15 s).
2. Call the loop with the goal verbatim, every value Jev may need to type, and
   a `verify` that tests the real done state (`SKILL_DIR` is the absolute path
   of the directory containing this SKILL.md):

   ```js
   const { runJevLoop } = await import(
     `file://${SKILL_DIR}/scripts/jev-loop.mjs`
   );
   const result = await runJevLoop(page, {
     goal: "Open the Billing page and show the credit balance",
     values: { query: { value: "pricing", hint: "site search query" } },
     verify: async (p) => /billing/.test(await p.url()),
   });
   ```

   - `values`: Jev picks which key goes in which field by `hint`; a fill with
     no matching value escalates instead of inventing data. Site search needs
     a value too.
   - `verify`: test URL, dialog text or a DOM fact — the thing the goal is
     about. A verify on a heading passes early (link clicked, navigation not
     yet committed) and a verify blind to modals makes Jev loop past a done
     state.
3. Branch on `result.status` — the loop fails loud, never silently retries:

   | status | meaning | you |
   | --- | --- | --- |
   | `done` | Jev claims visible evidence; `verified` true when your verify passed | read the page and report |
   | `escalate` | login/2FA, payment, upload, delete words, free text, low confidence, target missing, two action errors | `result.reason` names it; `handOff` for login, fix the blocker, or finish with plain ego calls |
   | `blocked` | Jev reports stuck: dead end, nothing offered advances the goal | reason about the page yourself (e.g. the docs have no such page) |
   | `max_steps` | loop bound hit | inspect `result.trace` |

   `result.trace` is per-step `{op, ref, name, opConfidence, targetConfidence}`;
   `result.snapshot` is the last a11y tree. `result.timings` records where the
   time went: `timings.steps` per phase (snapshotMs / domMs / askMs / actMs /
   verifyMs / stepMs) and `timings.llmCalls`, one entry per System One request
   (`{seq, step, kind, ms, ok, model, usage}` — retries and option_retry
   included; `timings.model` names the serving model version, e.g.
   `jev-1.13.0`). `timings.planner` names the driving agent — env detection
   only finds the harness, so pass `planner: "<harness>/<model>"` (your own
   model id) for full attribution. Show the user the latency table once the
   loop exits:

   ```js
   const { formatTimings } = await import(
     `file://${SKILL_DIR}/scripts/jev-loop.mjs`
   );
   console.log(formatTimings(result));
   ```

Done when the page state your goal describes is confirmed by `verify` or your
own `page.evaluate` — Jev's `done` is a claim, the check is yours.

## Gotchas

- A click on a `target=_blank` link opens a new Page; the loop stays on the
  old one and escalates on the unchanged page. Continue on the new label.
- Collapsed menus and teleported dropdown options are not in the DOM until
  opened: click/hover the parent first, then enter the loop. `select` on a
  `dN` target escalates by design.
- Jev will click "Continue with Google" on a login page; keep login pages out
  of the loop or `handOff` first.
- Semantic filtering ("not in the list → switch to All") is planner work; a
  `blocked` there is correct, not a bug.

## Reference

- Options, thresholds, backend/keys, latency numbers: [`reference.md`](reference.md).
- Offline smoke test (mock decider, no key) — run from this skill's directory:
  `ego-browser nodejs < scripts/selftest.mjs`

---
name: flow-runner
description: Drive and verify end-to-end user flows (login, signup, checkout, search, multi-step forms/wizards, etc.) in a real browser using Playwright, via either the Playwright MCP server or the @playwright/cli, and produce a structured pass/fail run report with evidence. Use this whenever the user wants to test, verify, walk through, smoke-test, or reproduce a user journey in a web app — phrases like "test the checkout flow," "walk through login and make sure it works," "does the signup form actually work," "run this scenario against staging," "make sure this didn't break," or "reproduce this bug in the browser" should all trigger it, even if the user never says "Playwright," "E2E," or "MCP" explicitly. Also trigger when the user asks to write or run a browser automation test, not just describe one.
---

# Playwright Flow Runner

Drives a real browser through a defined user journey and reports, step by step, whether the app actually did what it was supposed to — with evidence, not just a vibe.

If the user hasn't told you what to test yet and instead wants to figure out what's worth testing on a site, that's the `scenario-mapper` skill's job, not this one — it explores a site and produces a prioritized CSV of candidate scenarios. Use its output as the step plans you execute here. If a scenario already has a detailed, persistent test-case document from `test-case-writer`, use that directly as your plan rather than writing your own — see step 1 below.

## Before touching the browser: check what you have

You're on Claude Code, so you likely have two ways to drive Playwright:

- **`@playwright/cli`** — shell commands, writes accessibility snapshots and screenshots to disk instead of streaming them into your context. Check for it first: `npx @playwright/cli --help`. If it's there, prefer it — a typical flow costs a fraction of the tokens this way, and disk artifacts survive after your context window doesn't.
- **Playwright MCP server tools** (`browser_navigate`, `browser_click`, `browser_type`, `browser_snapshot`, `browser_take_screenshot`, `browser_wait_for`, `browser_evaluate`, `browser_network_requests`, `browser_console_messages`, `browser_tabs`, and similar) — use these if the CLI isn't installed, or if you're in an MCP-only context. Check your actual connected tool list for exact names rather than assuming — server versions drift.

Don't guess which one is available — check, then commit to one for the whole run. Mixing them mid-flow is a good way to lose track of session/auth state.

**If the profile names a saved session, use the driver that can actually load it.** A
`storageState` file (`auth.json`) belongs to a Playwright browser context — `@playwright/cli`
with `state-load`, or an MCP server that exposes the same capability. An IDE's built-in
browser preview keeps its own separate session and will run **anonymous** no matter what the
profile says, silently limiting the run to public pages. Before starting an authenticated
flow, pick the driver that can load the state; if the only browser available can't, say so
plainly and report the run as anonymous rather than letting the user believe it was signed in.

**Decide headed vs headless before you open the browser.** Both drivers default to invisible.
If the person is watching — demoing, screen-recording, walking through a flow, or debugging
something that looks wrong — run visibly (`playwright-cli open <url> --headed`, or the
equivalent option on your MCP server) and say that you did. Switching later means a new
browser and a lost session, so choose up front.

**If the flow needs credentials, confirm you can actually reach them before opening the
browser.** The target profile names env vars (`credentials.username_key` / `password_key`);
check those variables are actually set in the environment (`printenv NAME >/dev/null`) — never
print a value. Nothing auto-loads `.env`, and many agents refuse to read `.env` files at all,
so the usual fix is for the user to `export` the vars in the shell they launched you from.

**Prefer a saved session over typing credentials.** Filling a password leaks it into the
transcript — `playwright-cli fill` echoes the resolved value, and MCP tool calls carry the
literal by construction. If a saved `storageState` exists, load it and start authenticated.
If one doesn't, do the credential login **once** (with a throwaway account), save the state
for reuse, and tell the user that password is now compromised and should be rotated.

**Filling a credential form: verify every field, then blur, then submit.** Auth forms are
where "it looked filled but submitted empty" happens most, and the app's error is always the
same generic "invalid email or password" whichever field was wrong. So after filling and
before clicking submit, check **all** required fields at once:

```
[...document.querySelectorAll('input')].map(i => i.type + ':' + i.value.length).join(' ')
```

Every required field must be non-zero, and the lengths should match what you supplied. Then
press Tab (or otherwise blur the last field) before submitting: React/Vue controlled inputs
commit state on change/blur, and filling then immediately clicking can submit stale, empty
state even though the DOM shows text.

**If auth fails with credentials the user says work manually, it is a harness problem until
proven otherwise.** Do not report it as an app defect. Work through, in order:

1. Re-check the field lengths above — a fumbled element ref that put a value in the wrong
   field is the most common cause, and it only ever shows up as "wrong credentials".
2. Retry once using per-character typing (click the field, then type) instead of a direct
   fill, which guarantees the framework's input events fire.
3. Confirm the value itself survived the shell — `printf '%s' "$VAR" | wc -c`, length only,
   never print it. Quotes in a `.env` line add two characters.

Only after all three still fail is it worth calling the auth flow itself into question, and
even then report it as BLOCKED with the diagnosis rather than as a defect. Filing "login is
broken" when the harness mangled the input burns the team's trust in every later report. Note
too that repeated failed attempts can trip provider rate limits, so later retries may fail for
a different reason than the first.

**Never end a run without a report.** If you can't start — credentials unreachable, no test
account, the login page won't load, the profile is missing — stop immediately and write a
**BLOCKED** report naming the one thing that's missing and how to supply it. A run that exits
quietly, or leaves an empty run directory behind, reads to the next person (and to
`report-generator`) as "ran and found nothing," which is worse than an obvious failure.

## Core principles (and why they matter)

**Read before you act.** Always get a snapshot of the current page (accessibility tree, not a screenshot) before deciding what to click or type into. Act on the refs/roles the snapshot gives you, never on guessed pixel coordinates. Coordinate-based clicking breaks the moment a viewport size or layout shifts; the accessibility tree is stable, and reading it as you go means you're getting a free accessibility check on top of your flow test.

**Wait for state, not time.** Never `sleep(2000)` and hope. Wait for the specific element, text, or network state the next step actually depends on. A fixed delay either wastes time when the app is fast or produces a flaky failure when it's slow — waiting for the real condition is deterministic either way.

**Every step is an assertion, not just an action.** "Click login" isn't done when the click registers — it's done when the expected post-login state (redirected URL, welcome text, whatever) actually appears. If you only perform actions and never check outcomes, you're doing manual clicking with extra steps, not testing.

**Persist evidence as you go, not just when something breaks.** Save snapshots/screenshots to disk under a run directory as each step completes. Keep your in-context notes to file paths and one-line summaries — don't inline full snapshot dumps into your own reasoning once you've extracted what you need from them.

**Reuse session state across steps.** If the flow needs auth, capture `storageState` once (login, save state) and reuse it rather than re-logging-in at the start of every scenario. Re-authenticating repeatedly multiplies runtime and adds a second point of failure (the login flow itself) to tests that are meant to be checking something else.

**On failure, stop and preserve evidence — don't push through.** If step 3 of 7 fails its assertion, don't keep clicking through steps 4–7 pretending the app is in a known state; it isn't. Capture a trace, screenshot, and console/network log for that step immediately, then stop the flow and report what you know.

## Workflow

1. **Plan the flow before opening a browser — or use one that already exists.** If a `test-case-writer` document exists for this scenario, execute directly from it rather than writing a new plan from scratch; it already has the numbered steps and per-step expected results you'd otherwise be deriving yourself. Otherwise, write out the steps as a numbered list, each with an *expected observable outcome* — not just an action. E.g. "3. Submit the shipping form → expect redirect to `/payment` and a summary showing the entered address." Deciding what "pass" looks like ahead of time keeps you from rationalizing a bad outcome after the fact.
2. **Set up.** Launch/connect the browser, navigate to the starting URL, load `storageState` if this flow needs to start authenticated.
3. **Execute step by step:** snapshot → find the ref → act → wait for the expected resulting state → assert it → record pass/fail plus the evidence path.
4. **On failure:** capture trace + screenshot + console/network log, stop, and mark the run failed at that step — don't skip ahead. This report and evidence bundle is often enough on its own; if the user wants a deeper investigation — minimal repro, reproducibility rate, a root-cause hypothesis — that's the `bug-triage` skill's job, not this one's. Hand it the failed step and its evidence rather than re-deriving from scratch.
5. **Summarize** using the report format below. **If you executed from a `test-case-writer` document and every step passed, update that document's Status field from "Inferred, not yet verified" to "Verified (via flow-runner, [date])"** — that flip is what makes the document trustworthy input for `e2e-codegen` later. Don't skip this; an executed-but-never-updated document silently understates its own confidence to the next reader.

If the user gave you a bug report or a vague description ("the checkout flow is broken") instead of an explicit step list or test-case document, write the step plan yourself based on what you can infer from the app (form fields you see in the first snapshot, obvious CTAs, URL structure), state your inferred plan briefly, then proceed — don't stall on asking for a formal spec.

## Run report format

Always end with a structured report, not just prose:

```markdown
## Flow: [name, e.g. "Guest checkout"]
**Result:** ✅ PASS / ❌ FAILED at step N / ⚠️ PASSED WITH WARNINGS / 🚧 BLOCKED (never started)

| # | Step | Expected | Actual | Result |
|---|------|----------|--------|--------|
| 1 | Navigate to /cart | Cart page loads with 2 items | Matched | ✅ |
| 2 | Click "Checkout" | Redirect to /checkout | Matched | ✅ |
| 3 | Submit shipping form | Redirect to /payment | Stayed on /checkout, validation error shown | ❌ |

**Evidence:** trace: `runs/guest-checkout/step-3.trace.zip`, screenshot: `runs/guest-checkout/step-3.png`, console: `runs/guest-checkout/step-3-console.log`

**Notes:** [anything worth flagging — e.g. a console error unrelated to the failed assertion, a slow network call, a11y issue spotted incidentally]
```

Keep the table terse — one line per step. Put detail and speculation about root cause in Notes, not the table.

## Reference

`references/tool-mapping.md` has the CLI-vs-MCP tool correspondence and worked patterns for common flow shapes (login, search, multi-step commit flows like checkout/booking/applications, and plain content/navigation checks for non-transactional sites) — read it if you're unsure which command/tool to reach for at a given step, or want a starting template for a flow type.

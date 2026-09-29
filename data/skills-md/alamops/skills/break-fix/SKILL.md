---
name: break-fix
description: (alamops) Adversarial end-to-end bug hunt on a running app. Drives the real app like a hostile, confused, or impatient user — junk and boundary input, double-submits, out-of-order steps, back-button and refresh mid-flow, expired sessions, two tabs on one record, flaky network, tampered URL params — to make it throw, corrupt state, lose data, or strand the UI. Watches console, network and server logs, not just the viewport. Then reproduces each finding deterministically, traces the root cause in code, writes a *failing* e2e regression test, fixes the defect, and proves the suite goes green. Use whenever the user says break my app, try to break it, bug hunt, bug bash, QA sweep, exploratory / adversarial / chaos / monkey / fuzz testing, "find bugs by actually using it", "click around and see what explodes", or asks for an e2e test so a bug can't come back. Runs only against local/dev/staging targets the user controls. Not for reviewing a diff (code-review), building a feature (implement), or triaging production errors from Sentry.
---

# Break-fix — adversarial e2e bug hunt, then root-cause and fix

Two jobs, in order. **Break it**: drive the running app until it does something it shouldn't. **Fix it**: for each real defect, find the actual cause, encode it as a failing e2e test, fix it, and watch the test go green.

The regression test is not paperwork at the end — it's how you prove the bug was real and that the fix addresses it. A test written *after* a fix, that has never once failed, guards nothing.

## Why polite testing finds nothing

The instinct when handed an app is to use it correctly: fill the form with plausible data, click the buttons in order, admire the success toast. That path is the one the developers walked a hundred times while building it. It is already green.

Bugs live where the implied contract of the UI is violated — where a user did something the code never imagined. So your job is to be a **bad** user, deliberately and systematically. Not random flailing (that finds little and wastes tokens), but targeted violation of the assumptions you can see the code making.

Two things make a hunt productive rather than performative:

- **Read the code first, then attack what it assumes.** A hunt informed by five minutes in the validation layer finds ten times what blind clicking finds. When you see `parseInt(req.query.page)` with no guard, you now know exactly what to type in the URL. When a form validates on the client, go around it.
- **Look where the user can't see.** A screen that renders fine while the console throws `Unhandled promise rejection` and the network tab shows a 500 is a bug that shipped. Most of what you'll find lives in the console, the network panel, and the server's stderr — not the viewport.

## Rules of engagement

1. **Authorized targets only.** Local, dev, or staging instances the user controls. Never point this at production, and never at a third party's system. If the only reachable environment is production, stop and say so — read-only poking at prod is a different, much more careful activity than trying to break something.
2. **No irreversible external side effects.** Real payment charges, outbound email/SMS to real addresses, third-party writes, destructive admin operations on shared data. Use sandbox/test credentials; if you can't tell whether a button is wired to something real, ask before pressing it.
3. **Break the app, not the box.** You're hunting logic and state bugs by using the product. Don't run load/DoS tooling, don't attack the host or infrastructure, don't exfiltrate data. Authorization probing means checking whether *your own* second test account can reach the first account's data — a real, important bug class — not attacking anyone else's account.
4. **A finding needs a deterministic repro.** "It broke once" is a lead, not a bug. Reproduce it from a clean state before it goes in the report.
5. **Fix causes, not symptoms.** If a double-click creates two orders, the fix is a server-side idempotency guard — disabling the button just hides it from careful users. See *Phase 4*.
6. **Red before green.** Every regression test must be observed failing against the unfixed code, for the right reason, before you fix anything.
7. **Report honestly.** If you couldn't reproduce something, say so. If a fix is partial, say which part. Don't round "I couldn't get it to happen again" up to "it's fine."

## Progress checklist

Present this at the start and keep it current — a hunt is long and the user should see where you are:

```
Break-fix progress — <app / surface>
- [ ] Phase 0  Scope & safety confirmed (target env, accounts, off-limits actions)
- [ ] Phase 1  Recon (app running, e2e harness found, surface map, soft spots)
- [ ] Phase 2  Hunt (N surfaces attacked, M anomalies logged)
- [ ] Phase 3  Triage (reproduced, deduped, classified) — X confirmed bugs
- [ ] Phase 4  Root cause per bug
- [ ] Phase 5  Regression tests written & observed failing (red)
- [ ] Phase 6  Fixes applied, tests green, full suite clean
- [ ] Phase 7  Report written (docs/bug-hunts/<date>-<slug>.md)
```

## Phase 0 — Scope & safety

Short, one pass, then move. Ask only what you can't determine yourself:

- **Which app and which environment?** Confirm it's local/dev/staging. Get the base URL and how it should be started (or whether it's already running).
- **Credentials.** Test accounts, ideally **two** with different owners and, if roles exist, one per role — cross-account and cross-role checks need them.
- **Scope.** A specific flow (checkout, onboarding, the thing they just shipped) or the whole app? Default to the highest-traffic user flows plus anything changed recently — `git log` tells you what's freshest and therefore least battle-tested.
- **Off-limits.** Anything wired to real money, real messages, or shared data. Get this explicitly; it's the one question where guessing is expensive.
- **Time box.** Bug hunting is unbounded by nature. Agree on a rough budget (a handful of surfaces vs. an exhaustive sweep) so you can stop at a sensible point rather than grinding.

If the user says "just go," proceed with the safest reading — local environment, don't press anything that looks irreversible — and state those assumptions in the report.

## Phase 1 — Recon

You need three things before attacking: a running app, a place to put the eventual test, and a map of where to aim.

**Get it running.** Find the dev command, required services (db, queue, cache), env vars, and seed data — README, `package.json` scripts, `Makefile`, compose files, `.env.example`. Start it as a background process and *wait for readiness* (poll the port or health endpoint). Capture the server's stdout/stderr to a file you can grep later; server-side stack traces are among your best evidence and they scroll away if you don't.

**Find the e2e harness.** Playwright, Cypress, Detox, Puppeteer, supertest-against-a-live-server — whatever exists, the regression tests you write in Phase 5 belong *in it*, using its fixtures and conventions. Read `references/e2e-harnesses.md` for detection cues, the run recipe per framework, and what to do when there is no harness at all. Do this now, not in Phase 5: if there's no harness, you want to know before you've found six bugs with nowhere to put their tests.

**Drive the app.** Prefer the repo's own e2e tooling in headed or debug mode — it shares selectors and auth setup with the tests you'll write. Browser-automation tools (e.g. a Chrome MCP) are a fine alternative for exploration, especially for messy interactions like real double-clicks, tab switching, and back-button abuse. Whichever you use, the *test* still lands in the repo's harness.

**Map the surface, then find the soft spots.** List routes/screens, forms and their fields, state-changing actions, roles, and anything asynchronous. Then spend a focused pass in the code looking for assumptions to violate — this is what turns a random walk into a hunt:

- Input handling with no validation, or validation only on the client.
- Numeric/date parsing straight off `params`/`query`/`body` with no bounds.
- Resource lookups by ID that don't filter by owner or tenant.
- `useEffect`/lifecycle code that assumes data is loaded, arrays are non-empty, or an object is non-null.
- Handlers that mutate state before awaiting, or don't guard against re-entry.
- Anything using `index` as a React key, storing derived state, or caching across navigations.
- Recently changed files (`git log --since` on the scoped area) — new code is under-exercised code.

Record each soft spot as a hypothesis with a file:line anchor and the attack that would prove it. Attacks derived from a specific assumption hit far more often than generic fuzzing.

## Phase 2 — Hunt

Now break it. Work surface by surface so your report is organized and your repros stay clean.

### The eight bad users

Rather than working down a flat checklist, run each surface past these personas. They generalize better than any enumeration, because each one embodies a *class* of assumption:

| Persona | What they do | Assumption they break |
| --- | --- | --- |
| **The impatient one** | Double- and triple-clicks submit, hits Back the instant a spinner appears, refreshes mid-transaction, mashes Enter | One click = one request; the flow completes |
| **The confused one** | Wrong order, skips steps, deep-links into step 3 of a wizard, uses Back as Undo, bookmarks a modal | Users arrive through the front door, in order |
| **The clipboard** | Pastes 12KB of text, emoji-only names, HTML, a leading `=`, a phone number with spaces into a number field | Input resembles what the placeholder suggests |
| **The polyglot** | RTL text, CJK, combining diacritics, zero-width characters, `O'Brien-Smith`, a 40-char single word | Text is short, LTR, ASCII, and word-wraps |
| **The multitasker** | Two tabs on one record, edits both, logs out in one and keeps clicking in the other | One session, one tab, one writer |
| **The commuter** | Goes offline mid-request, slow 3G, a request that never resolves, one that 500s | The network is fast and always answers |
| **The nosy one** | Edits IDs in the URL, replays API calls with their *own* session against their *other* account's resources, removes required params | The client is the only caller and it behaves |
| **The extremist** | 0, -1, 999999999, empty list, exactly one item, 10k items, year 1900 and 2999, 23:59 on a DST boundary | Data lands in the comfortable middle |

`references/attack-playbook.md` expands each of these into concrete, ready-to-use payloads and step sequences organized by surface (forms, navigation, auth/session, concurrency, lists/data, uploads, network failure, time/locale, direct API). Read it when you start attacking a surface — it's the working reference, and it carries the specific strings and sequences you don't want to reinvent.

### Watch more than the viewport

Before and during every attack, keep these open, because most failures never reach the screen:

- **Browser console** — errors, unhandled promise rejections, React warnings about keys/state updates on unmounted components, CSP violations. A rejection is a bug even when the page looks fine.
- **Network** — any 4xx/5xx the UI swallowed, requests fired twice, requests fired with `undefined` in the path, requests that never complete.
- **Server logs** — stack traces, ORM errors, `undefined is not a function`, warnings about connections or transactions.
- **The UI's own state** — did an error toast appear and vanish? Is a spinner still spinning? Is a button permanently disabled? Is the page stuck in a state with no way out?
- **The data** — after a failed action, check the database or the list view. Half-written records are worse than clean failures and they are invisible from the screen where you caused them.

### Log every anomaly as you go

Don't hold findings in your head across a long hunt — write each one down the moment you see it, with enough detail to reproduce it later from cold. Minimum: the surface, the exact steps, what you expected, what happened, and the evidence (console excerpt, response body/status, server trace, screenshot or trace file path). A finding you can't reproduce tomorrow will be dropped in triage, and that's wasted work.

**When something breaks, immediately probe the neighborhood.** A bug is usually an instance of a class: if one form accepts a 12KB name, try its siblings; if one endpoint doesn't check ownership, check the others on the same resource. Finding the class is worth far more than finding the instance, and it changes what the fix has to cover.

## Phase 3 — Triage

Raw anomalies aren't bugs yet. For each one:

**Reproduce from a clean state.** Fresh session, seeded data, the recorded steps and nothing else. If it reproduces, it's confirmed. If it only reproduces sometimes, that's *also* a finding — intermittent means a race, and races are among the most valuable bugs you'll find — but say plainly that it's intermittent and note the hit rate.

**Classify it,** because not everything weird is a defect:

- **Bug** — it crashes, 500s, throws an unhandled rejection, corrupts or loses data, exposes another account's data, violates the app's own stated rules (a validation message it promised, a documented limit, its own types), or strands the user in a state with no exit.
- **Nit** — ugly, awkward, or inconsistent, but functional. Report it in a separate list; don't spend a fix cycle unasked.
- **Intended** — a deliberate product decision you happened to dislike. Drop it, or raise it as a question. Say so honestly rather than padding the count.
- **Environment** — a broken seed, a missing env var, your own setup. Fix your setup and move on; it isn't a product bug.

**Dedupe and generalize.** Five symptoms from one missing guard is *one* bug with five manifestations — report it that way, since it gets one fix and one root cause. Conversely, if the same attack works on four different endpoints, that's one class with four sites, and the fix has to cover all four.

**Assign severity** by consequence, not by how dramatic the failure looked: `critical` (data loss/corruption, cross-account exposure, flow completely broken), `high` (a real user hits it on a normal path, or it silently produces wrong data), `medium` (needs an unusual sequence but is genuinely reachable), `low` (contrived, cosmetic, or self-inflicted).

**Then check in with the user.** Present the confirmed list — severity, one-line description, repro — and say which you propose to fix now. Proceed with the obvious ones without waiting; pause for anything whose fix is architectural, changes product behavior, or is bigger than the hunt itself. The point of the gate is to avoid a surprise refactor, not to make the user approve every line.

## Phase 4 — Root cause

For each bug you're fixing, find the actual defect before touching anything. Follow the evidence from the symptom inward: the stack trace's deepest frame in *your* code, the request that failed and the handler that served it, the state that was wrong and the write that made it wrong. Read the surrounding code until you can state the cause in one sentence.

Then ask two questions that determine whether the fix will hold:

- **Is this the cause or a symptom?** Trace one level further than feels necessary. Two orders from a double-click: the symptom is the button, the cause is a create endpoint with no idempotency key or uniqueness constraint. A crash on an empty list: the symptom is `data[0]`, the cause may be an API that returns `null` where the type says array. Fixing the outer layer leaves every other caller exposed.
- **Where else does this cause live?** The same missing guard, the same unvalidated parse, the same unscoped query — grep for the pattern. A fix that covers one of four call sites is a fix that will be re-reported.

Write the cause into the bug record with file:line anchors before you write any code. If a bug resists explanation, say so and fix nothing — a speculative fix on a misunderstood cause usually moves the symptom rather than removing it.

## Phase 5 — Regression test (red)

Write the e2e test **before** the fix, and run it against the unfixed code.

This ordering is the whole value of the phase. A test written after a fix has never demonstrated that it can detect the bug, so it may be asserting something that was always true — a green check that guards nothing. Watching it fail first is the only proof you have that it will catch a regression.

- **Encode the bug, not the surroundings.** The test walks the repro steps and asserts the behavior that *should* happen at the point where it didn't. Name it after the bug (`checkout does not create duplicate orders on double-submit`), not after the feature.
- **Verify it fails for the right reason.** A test that errors on a typo'd selector is also "red." Read the failure output and confirm it's failing on your assertion, describing the actual bug.
- **Live in the repo's harness.** Its directory, its fixtures, its auth setup, its selector conventions. A parallel test setup rots. See `references/e2e-harnesses.md` for per-framework idioms.
- **Be deterministic.** Seed or create the data the test needs and clean it up; generate unique values per run rather than relying on a fixed record; wait on conditions and network responses, never `sleep`. A flaky regression test gets skipped within a month and the bug comes back.
- **Assert what a user or the system can observe** — the rendered result, the record count, the response status, the absence of a console error — rather than internal implementation details that will change.
- **Cover the class, not just the instance.** If the cause had four sites, either parameterize the test over them or add a cheap unit/integration test on the shared invariant and keep the e2e test on the user-visible flow. E2e is the deliverable the user asked for; a lower-level test alongside it is proportionate when one invariant protects many call sites.

Record the red output — it goes in the report as evidence the test does its job.

## Phase 6 — Fix (green)

Apply the smallest change that removes the cause identified in Phase 4, matching the conventions of the code around it. Resist bundling refactors into a bug fix — they make the diff hard to review and blur what actually fixed the problem.

Then close the loop, in this order:

1. **Re-run the regression test.** Red → green. If it's still red, the fix is wrong or incomplete; go back to Phase 4 rather than adjusting the test to pass.
2. **Re-run the manual repro.** Tests can pass while the real behavior is still wrong, especially where the test's selectors are coarser than reality.
3. **Run the full suite** (unit, integration, and e2e). A fix that breaks three other tests isn't done. Report failures with output rather than working around them.
4. **Re-attack the neighborhood.** Try the sibling surfaces you identified in Phase 4 and a couple of variations on the original attack. Fixes frequently narrow a hole rather than close it — the guard that rejects `-1` may still accept `-0.5`.

If several bugs share a cause, one fix may turn several tests green at once — that's a good sign your root cause was real, and worth noting in the report.

Commit each bug's test-plus-fix together, so the history shows the failing case alongside its remedy.

## Phase 7 — Report

Save the hunt to `docs/bug-hunts/<YYYY-MM-DD>-<slug>.md` (create the folder if missing) and summarize it in chat. Use this structure:

```markdown
# Bug hunt — <app / surface> — <YYYY-MM-DD>

| Field | Value |
| --- | --- |
| Target | <base URL, environment> |
| Commit | <SHA> |
| Scope | <surfaces attacked> |
| Harness | <e2e framework + command> |
| Result | <N confirmed> (<critical/high/medium/low>) · <M fixed> · <K deferred> |

## Summary
<2–4 sentences: what was attacked, what broke, what got fixed.>

## Confirmed bugs
### BUG-1 [severity] <one-line title>
- **Surface:** <route / screen / endpoint>
- **Repro:** <numbered steps from a clean state>
- **Expected / Actual:** <…> / <…>
- **Evidence:** <console excerpt, status code, server trace, artifact path>
- **Root cause:** <one sentence> — `path/file.ts:LINE`
- **Also affects:** <sibling call sites, or "none found">
- **Fix:** <what changed> — `path/file.ts:LINE`
- **Regression test:** `e2e/<file>:<test name>` — failed before the fix (<reason>), passes after

## Not fixed (and why)
<Deferred bugs, with severity and the reason: needs a product decision, out of scope, needs infra.>

## Nits & observations
<Non-defects worth knowing. One line each.>

## Attacked without finding anything
<Surfaces and attack classes that came back clean — this is what tells the reader
how much of the app the hunt actually covered.>

## Suite status
<Command run, pass/fail counts, anything still failing.>
```

The "attacked without finding anything" section matters more than it looks: without it, a report with three bugs is indistinguishable from a hunt that only tried three things. Coverage is what makes the result interpretable.

## Fanning out (optional)

A hunt parallelizes well *if* the agents don't share mutable state. If sub-agents are available and the surface is large, give each one a distinct surface **and its own test account and data**, and have it return anomaly records rather than fixes. You keep triage, root cause, and fixing — those need the whole picture, and parallel agents editing the same code collide.

The hazard to respect: two hunters against one app instance will corrupt each other's repros (one deletes the record the other is mid-edit on), and you'll spend the savings chasing phantom intermittency. Separate accounts are the minimum; separate instances are better. If you can't isolate them, hunt sequentially — a clean serial hunt beats a fast, unreproducible one.

## Adapting

These phases are the backbone, not a ritual. A user pointing at one just-shipped form wants a focused hunt on that form, not a full-app sweep — collapse recon and skip the fan-out. A user who says "just find bugs, don't fix anything" gets Phases 0–3 and a report. A user who hands you a known bug and asks for a regression test starts at Phase 4.

What shouldn't bend: attacks derived from what the code actually assumes, findings backed by a deterministic repro, root cause before fix, and a test observed failing before it's trusted to guard anything.

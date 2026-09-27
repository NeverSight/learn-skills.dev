---
name: playwright
description: Drive the running app in a real browser to prove a flow works — on demand, or as a saved test for the few flows worth re-running. Use when a multi-step flow needs checking end to end, right after deploying (against the live URL, not localhost), when the builder asks for Playwright, e2e or browser tests, and when something works locally but is reported broken in production. Also use before demo day to confirm the core action still works and to capture screenshots.
---

# Playwright

Most of the time, proving a flow works means walking it once, now. That needs no install and no files — drive the app with the browser control you already have and report what you saw.

Save a test only for a flow worth running again. In a two-week sprint that's a very short list.

## Walk it first

Default behaviour, every time: start the app, click through the flow as a person would, report what happened at each step, and say plainly whether it worked.

This covers almost everything: a new form, a sign-up, a page that should show the thing that was just created. No spec file, no runner, no browsers downloaded. If the builder asks for "a test" and this answers their actual question, do this and tell them what you did instead.

## When to save a test

Write a saved spec only when a flow is worth re-running for the rest of the sprint:

- **The core action.** The one thing their product does. If this breaks, they have nothing to demo.
- **The money path**, if one exists — checkout, upgrade, anything that charges.
- **Anything that already broke once.** Same rule as `keep-it-working`: it broke, so it can break again.

Cap it at about three specs for the whole sprint. A fourth is almost always someone testing for the feeling of being thorough.

Name the file after what the person does, not what the code is: `can-create-a-project.spec.ts`, not `project-form.spec.ts`.

## Earn the install before you run it

Playwright downloads real browsers — hundreds of megabytes and a few minutes. Before installing, say that out loud and confirm it's worth it. If they're mid-flow or low on time, walk the flow instead and offer the install later.

When it is earned, install the minimum: `@playwright/test`, Chromium only, one config, one spec. No extra reporters, no CI wiring, no other browsers. Nobody in a sprint is debugging a Safari-only failure.

## Sign-in: decide this once, before writing anything

**Never automate Google's login page.** Google blocks automated browsers, and any test that tries will fail in ways that look like the app is broken when it isn't. Builders lose entire nights here.

Instead, decide up front:

1. Create a test user the app can sign in as directly — email link, dev-only route, or seeded session.
2. Sign in once, save the browser session to a `storageState` file.
3. Every test starts already signed in, from that file.

If a project's auth genuinely cannot be scripted, say so early and keep every saved test on the signed-out surface. Don't discover this halfway through writing the third spec.

## After deploy, test the live URL

The highest-value run in the whole sprint: after a push goes live, open the **production** URL, do the core action, screenshot it.

This is what catches the environment variable that exists on their laptop and not on Vercel — the most common reason a project that works perfectly in development is dead on demo morning. Nothing else in the sprint catches it.

Report the result in plain words and include the screenshot. If it fails in production but passes locally, say that distinction explicitly: it is almost always configuration, not code.

## Writing tests that survive a sprint

The UI changes every day for two weeks. Tests that grip the markup will break daily and get ignored, which is worse than having none.

- Find things the way a person does: `getByRole`, `getByLabel`, `getByText`. Never CSS chains or Tailwind classes — a styling change must not fail a test.
- Assert with Playwright's own expectations, which wait on their own. Never `waitForTimeout`. A sprinkled sleep is a test that passes on a fast laptop and fails on demo day wifi.
- One flow per spec, following one person's path end to end.
- Test what the user sees — the project appears in their list — not what the database contains.

**A test that flakes once gets fixed or deleted that day.** A suite that cries wolf teaches the builder to ignore red, and a builder who ignores red is worse off than one with no tests at all.

## Keep out

No visual regression snapshots — the design is still moving, and every one of them will be wrong tomorrow. No cross-browser matrices. No coverage targets. No testing anything that isn't on the short list above.

## Fits with

`keep-it-working` decides whether a flow needs this at all — check there first. `agentation` is the other half of the loop: the builder points at what looks wrong, this proves whether the flow still works. `checkpoint` should have saved their work before any of this starts.

---

Ours. Written so a first-time builder gets the value of browser testing without inheriting a test suite they can't maintain.

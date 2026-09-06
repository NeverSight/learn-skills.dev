---
name: ui-verification
description: Runs scoped browser probes for focus, hit targets, overflow, themes, request failures, and performance attribution, with evidence linked to UI rule IDs. Use when asked to "verify this in the browser", "reproduce this finding", or "check the fix". For source audits and severity use ui-design; field metrics require RUM or CrUX.
compatibility: Requires access to the target app and browser automation. Bundled JavaScript recipes use the Playwright page API.
---

# UI Verification

Owns the browser session. Every other UI skill in this repo reasons about source and infers what the user will see; this one loads the page and measures it.

- **IS:** booting the app, driving it with a browser, and running the probes that decide a rule at runtime: computed boxes, injected failures, observed layout shift, a scripted Tab walk, an axe scan per theme. Output is findings keyed to rule ids with reproducible evidence, plus the clearing re-run after a fix.
- **IS NOT:** finding defects by reading source or deciding their tier and ship verdict (`ui-design` Audit mode owns both); building or restyling UI (`ui-design` Build); authoring a durable test suite (write Playwright tests); pixel-diff regression against a baseline (Chromatic, Percy); field performance (RUM or CrUX; Lighthouse is a lab tool).

The division of labour is the point. A static audit reports what the code will probably do; it cannot see a 40px control whose hit area a pseudo-element already expands to 44, or a retry button wired to nothing. This skill reproduces or kills each of those, so a finding arrives with a measurement instead of a confidence.

## Contents

- [When to run](#when-to-run)
- [Probe catalogue](#probe-catalogue)
- [Progress checklist](#progress-checklist)
- [1. Establish the session](#1-establish-the-session)
- [2. Select the probe set](#2-select-the-probe-set)
- [3. Run the probes](#3-run-the-probes)
- [4. Decide each finding](#4-decide-each-finding)
- [5. Clearing re-run](#5-clearing-re-run)
- [6. Report](#6-report)
- [Honesty rules](#honesty-rules)
- [Gotchas](#gotchas)
- [Related skills](#related-skills)

## When to run

| Situation | What this skill does |
|---|---|
| A `ui-design` audit emitted findings and the user wants them confirmed | Run only the probes those rule ids map to, in `references/rule-coverage.md` |
| No audit ran; the user points at a route or a running app | Detect features, run the full battery on the resolved routes |
| A fix just landed for a previously reproduced finding | Run the clearing re-run only (step 5) |
| The user asks for captures across themes or widths | `probes/theme-locale-matrix.md` alone |
| A `design-system.md` claims a scale and someone needs it checked | Read the claimed values off computed styles on a real page; a theme value the build overrides never reaches the browser |

Nothing here assigns a tier or a ship verdict. Hand reproduced findings back with their evidence and let `ui-design`'s `references/ship-readiness.md` tier them; two skills tiering the same finding is how the tiers drift apart.

## Probe catalogue

Each file is one probe: what it measures, the driver calls, the false positives it must guard, and the shape of the evidence it returns.

| Probe | Measures | Primary for |
|---|---|---|
| [probes/axe-scan.md](./probes/axe-scan.md) | axe-core violations per route and theme, including computed contrast | contrast, accessible names, landmarks, document language |
| [probes/target-size.md](./probes/target-size.md) | Bounding box and effective hit area of every visible interactive element | `interaction-target-size` |
| [probes/focus-walk.md](./probes/focus-walk.md) | Scripted Tab traversal, focus-ring pixel delta, dialog trap and restoration | `focus-*`, `interaction-focus-visible`, `interaction-keyboard-operable` |
| [probes/layout-shift.md](./probes/layout-shift.md) | Attributed `layout-shift` entries with the data response held open | `states-layout-shift`, `perf-image-dimensions-and-priority` |
| [probes/viewport-stress.md](./probes/viewport-stress.md) | Horizontal overflow and clipped text at 320px and up, and under tripled strings | `layout-long-content-safety`, `mobile-viewport-scaling` |
| [probes/failure-injection.md](./probes/failure-injection.md) | What renders when the data request returns 500, `[]`, malformed, or nothing | `states-no-error-state`, `states-no-empty-state`, `async-*`, `microcopy-*` |
| [probes/theme-locale-matrix.md](./probes/theme-locale-matrix.md) | The same route captured across viewport, theme, pseudo-locale, and direction | `dark-i18n-untested`, `dark-i18n-rtl-untested` |
| [probes/console-network.md](./probes/console-network.md) | Console errors, page errors, failed requests, hydration mismatch warnings | hydration mismatch, silent runtime failures |
| [probes/web-vitals.md](./probes/web-vitals.md) | LCP with its attributed element, CLS, INP on a scripted interaction | perf attribution, never a budget verdict |

## Progress checklist

```text
Verification progress:
- [ ] Step 1: Establish the session (references/session-setup.md): driver, build mode, base URL, auth, resolved routes
- [ ] Step 2: Select the probe set from handed-over rule ids (references/rule-coverage.md) or from the routes
- [ ] Step 3: Run each probe; record evidence artifacts before interpreting any of them
- [ ] Step 4: Decide each finding reproduced / not-reproduced / unknown; repeat timing-sensitive or inconsistent results when needed
- [ ] Step 5: For each fix applied, re-run the identical probe and record clearedBy
- [ ] Step 6: Emit the verification block per finding (references/evidence-output.md), then render
- [ ] Step 7: List probes skipped and why. A probe that could not run is never a pass
```

## 1. Establish the session

Read [references/session-setup.md](./references/session-setup.md). It resolves four things, and getting any of them wrong invalidates every probe downstream:

- **Driver.** Playwright when the repo can run it, the Chrome DevTools browser tools when it cannot. Four probes need request interception and network control, so they do not exist under a driver without them.
- **Build mode.** Perf and layout-shift probes run against a production build; dev-mode numbers measure the bundler. Failure injection and focus probes run fine in dev.
- **Auth and seeded data.** A route behind a login with no seeded session returns `unknown`, never a pass.
- **Routes.** Map the diff to URLs. A component with no reachable route falls back to the repo's Storybook, and to `unknown` if there is none.

Stop here if the app will not boot. A verification run with no session produces no findings, which is a reportable outcome and not a clean bill of health.

## 2. Select the probe set

**Handed a list of rule ids** (the normal case, from a `ui-design` audit): open `references/rule-coverage.md`, take the probe each id maps to, and run only those. Ids with no probe stay source-only findings and pass through untouched, marked as such.

**Given only routes:** detect features the way `ui-design`'s feature playbooks do (form, list, modal, dashboard, checkout), then run the battery that surface earns. `probes/axe-scan.md`, `probes/console-network.md`, and `probes/viewport-stress.md` run on every route regardless: they are cheap, and they are the three that find things nobody suspected.

Budget the matrix before running it. Routes multiplied by viewports multiplied by themes grows fast, and a run that takes twenty minutes gets skipped next time. Two viewports (360 and 1280) and two themes cover the ground; add widths only where a probe already found an edge.

## 3. Run the probes

Each probe file carries its own recipe. Three rules hold across all of them:

- **Capture evidence before interpreting it.** Write the screenshot, the JSON measurement, and the console log to disk first. A finding whose evidence was never written is unverifiable by the person reading the report, which puts it back where the static audit left it.
- **One probe, one route, one viewport, one theme.** Never fold two conditions into one run: when the result surprises you, you need to know which axis produced it.
- **Repeat uncertain measurements.** Retry timing-sensitive or inconsistent results under controlled conditions. A deterministic failure with a captured trigger needs no duplicate run. A result that flips remains inconclusive until its conditions are understood.

## 4. Decide each finding

Three outcomes, and the middle one is the one that earns this skill its keep.

| Outcome | Meaning | What it does to the handed-over finding |
|---|---|---|
| `reproduced` | The probe measured the defect | Stays a `fail`, now carrying `observed` from the measurement rather than from the source read |
| `not-reproduced` | The tested conditions did not exhibit the defect | Withdraw only if the probe exercised the alleged trigger; otherwise retain the candidate with the remaining coverage gap |
| `unknown` | The probe could not run or could not decide | Finding survives as `unknown` with the probe's reason. Never converts to a pass |

A `not-reproduced` result is a real deliverable, not a wasted run. It is what removes the false positives a large rule corpus asserts with `file:line` confidence, and it feeds the rejection section `ui-design` already requires.

Where a probe finds something no static rule predicted, emit it as a new finding against the rule id the probe is primary for. Where no rule covers it (an axe violation with no ui-design counterpart, a console error), emit it under `axe:<violation-id>` or `runtime:<signature>` and say plainly that it came from the browser and not the corpus.

## 5. Clearing re-run

A fix is not verified by reading the diff. Re-run the identical probe: same route, same viewport, same theme, same seed, same injected failure. Record it as `clearedBy` on the finding, keep the before-artifact, and never overwrite it with the after.

Three outcomes worth naming:

- The probe now passes: the finding is `applied` and cleared.
- The probe still fails: the fix did not work. Report it as applied-unverified and say so; do not report the fix and stay silent about the re-run.
- The probe passes but a different probe on the same route now fails: the fix caused a regression, which is a new finding, not a footnote on the old one.

## 6. Report

[references/evidence-output.md](./references/evidence-output.md) owns the shape: a `verification` block appended to each finding, a top-level `session` block, and artifact paths. It defines only the delta on `ui-design`'s `references/output-adapters.md` schema, which stays the single owner of the finding object, the three counts, and the verdict.

Where this skill runs standalone, render the same terminal adapter with `SHIP VERDICT` omitted: the verdict is a property of a tiered audit, and printing one from probe results alone invents a tier assignment nobody made.

## Honesty rules

- **A skipped probe is not a passed probe.** Report every probe that did not run, with the reason (no route, auth required, driver lacks interception, app would not build). A report that silently omits them reads as coverage it does not have.
- **A screenshot is evidence, not a verdict.** Probes decide on measurements. Captures exist so a human can check the measurement, and for the two questions no measurement settles: whether the dark theme looks right, and whether the pseudo-locale broke the layout or merely the prose.
- **Do not widen into a redesign.** This skill reports what it measured. A finding that needs a new type scale names the mode to run next, exactly as an audit does.
- **The app is the subject, not the harness.** A failure caused by the probe itself (a selector that never resolved, a route interception that swallowed the wrong request) is a harness bug. Fix the probe and re-run; never report it as a defect in the app.
- **Numbers carry their units and their conditions.** `44x44px at 360px width with touch emulation on` is a measurement. `too small` is the inference this skill exists to replace.

## Gotchas

The ones that cut across probes. Each probe file carries its own false positives.

- `page.emulateMedia({ colorScheme: 'dark' })` does nothing for an app that themes with a `class="dark"` or `data-theme` attribute, which is most Tailwind apps. The probe reports a clean dark pass while never having left light mode. Drive the app's own toggle, and assert the attribute landed before capturing.
- Running perf or layout-shift probes against `next dev` measures on-demand compilation. The first navigation to a route can spend seconds in the bundler, which lands in LCP and dwarfs anything real.
- Animations that never settle keep a screenshot probe waiting until timeout. Set `prefers-reduced-motion: reduce` for captures, then run motion-sensitive checks in a separate pass with it off, because reduced motion is also a code path that can be broken.

## Related skills

- `ui-design`: reads source, produces the findings this skill reproduces, and owns tiering, the ship verdict, and the finding schema.
- `typography-audit`: type findings that need a rendered measure or leading value can be handed here for the measurement.
- `ax-audit`: agentic surfaces. Its runtime questions use the same session and probes.
- `ui-animation`: motion craft. This skill can capture the timing, but judging the curve is that skill's.

Maintenance only: `evals/evals.json` holds the behavioural scenarios and routing prompts for anyone changing this skill. It never loads during a verification run.

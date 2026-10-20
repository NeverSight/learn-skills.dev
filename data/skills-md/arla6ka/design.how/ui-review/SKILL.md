---
name: ui-review
description: Use to critique a screen, flow, prototype or running build, accessibility included, and rank what is broken, such as "check this page before I ship", "is this flow ready", "is it accessible", keyboard or screen-reader checks, "it feels off on my phone" or "it feels janky". Not for token compliance, which is token-mapping.
---

# UI review

The render is the evidence. A description, DOM text or source code only supports it. Severity, the 13 criteria and the edge cases are in `references/criteria.md`. An installed design system's own rules come first and count as agreed criteria.

## Steps

1. **Scope.** What the caller names, else the branch's changed screens, else the five top routes.
2. **Lint.** Run the project's own lint on the scoped files. Record the command and exit code.
3. **Capture** each screen at each width (the app's narrowest and widest, 390 and 1280 by default) in the states that matter, one fresh navigation per width. With `build-design-system` installed, `build-design-system/scripts/capture.mjs` does this behind a guard that blocks every write and saves each capture's accessibility tree. It needs `--writes <file>` listing the app's writes, or `--no-backend`, and writes only to its `--out` folder (keep that under `.ui-review/`). Otherwise use the host's browser tool and save the tree yourself. Run the project's accessibility scanner too when it has one.
4. **Fix the purpose** of each screen in one line. Mark it assumed when the caller did not give it.
5. **Probe the traps** each screen has, on a local build only: keyboard path, focus after close, loading and error states, a throttled tab, reduced motion, and a touch width. Each probe gets a measured result or a reason it did not run. Measure press feedback with the Event Timing API (a `PerformanceObserver` on `event` entries, each `duration` under 100 ms). Do not click anything that writes to shared data.
6. **Walk the criteria** at each width. Cite each finding by number and name, or by the installed rule's ID.
7. **Sort.** With more than one reviewer available (a panel), give each the same prompt and no persona, read only. The coordinator then sorts every finding into `blocking`, `should-fix`, `note` or `dismissed`, naming who raised it and giving one line of reason. A finding raised by two reviewers on their own is the strongest signal. Dismiss nitpicks, hypotheticals nobody traced to a real call site, and "I would have done it differently". Within a bucket, put surfaces that write data first, then order by places hit. Without a panel, do the same alone.
8. **Walk the edge cases** and mark each shown or not shown.
9. **Write the verdict last.**

## Rules

- A finding has a criterion, a findable location (the element by role and name, with its capture, as in `button 'Save changes' (settings-1280.png)`), the width, and the evidence. A finding that rests on taste is dropped to Left out.
- Wrong: "The spacing feels tight." Right: "Label sits 24 px from its own field and 8 px from the next one (criterion 4, settings-390.png)."
- An inferred finding is written as the check that settles it. An inferred `blocking` finding makes the verdict `no, pending <the check>`.
- A claim that something works or is fixed names a command or capture from this session.
- Contrast, target size and keyboard problems are ranked. A change to the accessibility tree that only adds semantics is ranked. One that removes or restructures semantics goes to a person.
- A finding or pass on responsiveness to input (criterion 13) from a screenshot is invalid. It needs a measured probe. A focus ring is the reverse. Reach the control with real Tab presses and judge the ring from the capture, because a container that draws it through `:has(:focus-visible)` leaves the focused element reporting no outline.
- Product decisions behind a fix go to For a person to decide. Keeping the user's input is never one.

## Output

The first line answers the ask in plain words. The ship line follows: `Ready to ship: no. Enter in Email cancels the invite (blocking 1, should-fix 2, 3 questions for a person).` Any `blocking` finding makes the verdict `no`, an inferred one `no, pending <the check>`, `should-fix` alone `yes, with fixes`, only notes `yes`.

Then, in order:

1. **Review record.** Source, tool, widths, date, criteria file, the purpose marked given or assumed, every assumption and gap.
2. **Findings** by bucket, each with who raised it, what was seen, where, criterion, why it matters here, evidence, and the fix as a check that fails on the current build (`Fix Enter in Email so that it sends 1 POST`).
3. **Edge cases not shown.** One line each.
4. **For a person to decide.**
5. **Dismissed and left out.** Each with who raised it and the reason.

Run on its own, save the report to `.ui-review/<date>-<flow>.md` with captures beside it. When a coordinator asks for captures only, return the capture paths, widths and `Coverage:` line, and no findings. The chat reply gives the answer and ship lines, each command with its exit code, and one prompt the person can paste to take the next step.

## Done

Every finding has a criterion, a location, evidence and only the widths where it shows. Every probe has a result or a reason. The first line, the ship line and the summary agree. The last line reads `Coverage:` with the routes, widths, themes and probes measured, then what was not.

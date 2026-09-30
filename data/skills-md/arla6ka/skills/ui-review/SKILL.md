---
name: ui-review
description: Critiques a screen, flow, prototype or running build against agreed criteria, accessibility included, and ranks findings by severity. Use for "check this page before I ship", "is this flow ready", "is it accessible", keyboard or screen-reader checks, "it feels off on my phone", "it feels janky", or a second read on UI. A whole-app ship check goes to design-system-boss, token compliance to token-mapping.
---

# UI review

1. **Scope.** A scope the caller names, else the branch's changed screens, else 5 top routes (`references/sources.md`, Finding the design).
2. **Capture** each screen at each viewport and run the accessibility scan there (`references/sources.md`, What counts as evidence).
3. **Fix the purpose**, inferred and marked assumed when not given, or stop on the conditions in `references/sources.md` (Inferring the purpose).
4. **Probe** every trap family the screen has, on a local build only (`references/sources.md`, Trap probes). Each probe gets a measured result or a reason it did not run.
5. **Walk criteria 1 to 13** at each viewport (`references/review-criteria.md`).
6. **Sort** repeats, chained findings, `system-caused` findings, accessibility, taste and departures per `references/review-criteria.md` (Sorting).
7. **Rank** `blocking`, `should-fix`, `note`, and within each by surface tier, then places hit (`references/review-criteria.md`, Severity).
8. **Walk the edge cases**, marking each shown or not shown, plus the States rows of each spec for a component on the screen (`references/sources.md`, Component specs).
9. **Write the verdict and summary last** (Output).

Never ship:

- A finding with no criterion from the file in use, or one that rests on taste.
- A finding from a description, DOM text or source code alone. The render is the evidence, and those only support it.
- An inferred finding written as a fix. It enters `Next:` only as the check that settles it.
- A claim that something works or is fixed without a command or capture from this session.
- A ranked semantics-changing accessibility fix or product decision. A person rules, and the finding stays.
- A criterion 13 finding or pass from screenshots. It needs `state-timeline.js` or a probe.
- A first line, ship line and summary that disagree.

## When a coordinator calls it

Take the captures, criteria and purpose as given and run to the end, recording any gap the solo path would ask about. With captures only, the scan and probes read `not run: captures only`, which counts as a reason. Start the report with a status line, `Status: complete (blocking n, should-fix n, note n)`, `Status: complete (partial: <what was not reviewed>)` or `Status: stopped: <condition>`, then `Commit: none`, then the answer and ship lines. Return the report, or the stop shape, as text and write no file.

## Output

Any `blocking` finding makes the verdict `no`, and an inferred one `no, pending <the one check that settles it>`. `should-fix` alone makes it `yes, with fixes`, and only notes `yes`. The first line answers the ask in plain words, with no criterion numbers or skill names, and "Not yet" pairs only with `no`. The ship line follows with the same verdict, why in one clause, and the count of unranked accessibility questions for a person. A partial run's verdict covers only what was reviewed. Example: `Ready to ship: no. Enter in Email cancels the invite (blocking 1, should-fix 2, 3 accessibility questions for a person).`

Then six parts.

1. **Review record.** Source, tool, viewports, date, criteria file, first pass or follow-up, the purpose marked given or assumed, every assumption, and every gap. Each n/a criterion gives its reason ("8. No destructive action on this screen").
2. **Summary.** What the screen asks, what works, and what most needs attention.
3. **Findings** by severity. Each gives what was seen, where (screen and region, or the element by role and name with its ref or selector and capture, as in `button 'Save changes' @e34 (settings-1280.png)`), the viewport, the surface's tier, the criterion by number and name, why it matters for this task, the evidence type and dedupe key (`references/sources.md`, What counts as evidence), and any matching `trap/` or `rule/` ID. A `system-caused` finding names the token, preset or component.
4. **Edge cases not shown.** One line each.
5. **For a person to decide.** Semantics-changing accessibility fixes, product decisions a fix needs, and problems no criterion covers, each tied to a finding or location.
6. **Left out.** Preferences dropped, each with the reason.

An empty group says "None", and a clean screen's notes stay notes.

The report is ready when every finding has a criterion, a findable location, evidence, and only the viewports where it shows. Every probe has a result or a reason, and the scan ran at each viewport or reads `not run: captures only`. The last line reads `Coverage:` with the routes, viewports, themes and probes measured, then what was not.

Run directly, save the report to `.ui-review/<date>-<flow>.md` with captures beside it. The chat reply opens with the answer and ship lines, gives each command run with its exit code, lists up to three items for a person with defaults, and ends with `Next:` and one prompt to paste. That prompt covers every `blocking` and shown-versus-sent finding as "Fix X so that <check>", such as "Fix Enter in Email so that it sends 1 POST". A `system-caused` fix names the system file. Each Next check must fail on the current build.

A stopped run returns only what stopped it, a one-line guess at what each screen does, and the shortest reply that unblocks it.

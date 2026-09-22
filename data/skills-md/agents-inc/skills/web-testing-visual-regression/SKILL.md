---
name: web-testing-visual-regression
description: Visual regression testing — screenshot baselines, determinism, diff review, baseline custody and CI wiring. Load when adding, reviewing or debugging tests that compare a rendered subject against an approved image.
---

# Visual Regression Testing

> **Quick Guide:** A visual test asserts that a subject still looks the way a human approved it. The comparison is trivial; everything hard surrounds it — making the render deterministic, scoping the capture to the subject, generating baselines in the environment that will diff them, and looking at every diff before accepting a new one. A baseline accepted without being looked at turns the suite into a machine that asserts the bug.

**Detailed Resources:**

- [examples/core.md](examples/core.md) — comparison configuration, the baseline matrix, masking, subject scoping
- [examples/determinism.md](examples/determinism.md) — the stabilizing stylesheet, fonts, frozen clocks, seeded randomness, fixture data, environment parity
- [examples/catalog-driven.md](examples/catalog-driven.md) — a component-state catalog as the visual corpus, modes, interaction-produced states, change detection
- [examples/ci.md](examples/ci.md) — pipeline wiring, diff artifacts, the baseline-refresh workflow, cost control
- [reference.md](reference.md) — comparison-option semantics, update modes, the pre-commit checklist, troubleshooting table

---

## Which path applies

The two families differ in where the baseline lives, who accepts a change, and who owns the render environment. Pick before writing anything; retrofitting is a migration rather than a flag.

- **Baselines committed to the repository, compared by a harness you run** — review happens in code
  review, and the render environment is yours to pin. Free per run, expensive in environment work.
  [examples/core.md](examples/core.md) and [examples/determinism.md](examples/determinism.md).
- **Snapshots uploaded to a change-detection service** — review happens in a hosted UI with a
  recorded accept per change, and one controlled renderer removes dev-vs-CI drift. Billed per
  snapshot, near-zero environment work. [examples/catalog-driven.md](examples/catalog-driven.md).

Running both over the _same_ subjects is the one combination to avoid — two baselines, two review flows, two chances to accept the wrong one. Splitting them by subject (a state catalog in the service, a handful of critical full-page checks committed) is common and works.

---

<critical_requirements>

## Before writing a visual test

**Look at the diff before accepting any baseline.** The approved image is the entire assertion, so accepting one unseen permanently encodes whatever was on screen, regression included, and the suite can never report it again.

**Make the render deterministic before capturing** — fonts loaded, motion stopped, clock frozen, randomness seeded, data fixed. A pixel that varies between runs is being asserted as though it were part of the design.

**Generate and compare baselines in the same environment.** Font rasterization and subpixel rendering differ between operating systems and container images, so a baseline made anywhere else shows a full-frame difference on every subject from the first run.

**Capture the subject, not the page around it.** An element or a clipped band fails only when it changes, which is what makes the failure name its own cause.

**Mask a region that legitimately varies rather than widening the tolerance.** A tolerance wide enough to absorb a live timestamp is wide enough to absorb a collapsed column.

</critical_requirements>

---

**Auto-detection:** visual regression, visual testing, screenshot testing, screenshot baseline, baseline image, golden image, pixel diff, image diff, expected/actual/diff, maxDiffPixels, maxDiffPixelRatio, diffThreshold, update snapshots, accept baseline, snapshot review, UI diff, stabilizing stylesheet

**Applies to:**

- Catching unintended visual change in components, pages and design-system primitives
- Guarding a shared component library where one CSS change fans out across consumers
- Covering theme and viewport matrices without duplicating a test per cell
- Guarding what no assertion expresses — spacing, overflow, z-order, focus rings, truncation
- Making a render deterministic enough to be worth comparing
- Deciding what a diff means, and who is allowed to accept it
- Wiring the visual job so its failures are actionable and its cost is bounded

**Handled elsewhere:**

- Authoring the component-state catalog a visual corpus is built from — this skill decides which
  states are worth capturing, not how a state is declared
- Driving a browser to reach a state — navigation, locators, network interception; the capture
  happens once the state is on screen
- Asserting text, roles, values or behaviour — those fail with a sentence, where a pixel diff fails
  with homework, so reach for them whenever they can express the requirement
- Pipeline syntax, runners, caching and secrets — this skill states what the visual job must do,
  and the provider decides how it is spelled

---

<philosophy>

## Philosophy

Every other kind of test states its intent in code: `expect(total).toBe(42)` says what correct means. A visual test states its intent in a **file** — an approved image somebody looked at once. Three consequences follow.

**The baseline is a review artifact, not a build artifact.** It records the judgement of a human who decided the UI was right. Regenerating it without looking destroys the only thing the test knows.

**Nondeterminism is a false requirement, not flake.** A pixel that varies between runs is being asserted as part of the design. Pin it or mask it; never widen the tolerance until it stops complaining.

**The diff is the output.** A suite that fails without producing a viewable expected/actual/diff triplet is unactionable, and unactionable suites get disabled.

**What visual tests are good at** is whole-appearance properties no reasonable assertion expresses — a shadow that vanished, a 3px shift that broke alignment, a font that failed to load, a dark-theme token that resolved to white-on-white, a container that stopped clipping overflow.

**What they are bad at is anything you could name.** If `toBeVisible()`, a text assertion or an accessibility-tree assertion would express it, write that instead.

</philosophy>

---

<patterns>

> **The snippets below are portable shapes, not runnable code.** `matchScreenshot(subject, name, options)` stands for your harness's screenshot assertion, and `freezeClockAt`, `goto`, `byTestId`, `byRole` and the bare `page` stand for its clock, navigation and locator controls. Platform APIs such as `document.fonts.ready` are named as themselves. The option names are the ones the common pixel comparators share; confirm every spelling against your harness's own documentation. [examples/determinism.md](examples/determinism.md) works the same patterns through fuller call shapes, which are closer to what you will actually type.

## Core patterns

### Pattern 1: Configuration-Driven Comparison

Tolerances, path layout and the baseline matrix belong in configuration. Per-assertion options are for what genuinely varies by subject — the mask list, the clip box.

```typescript
// visual.config.ts
const PIXEL_THRESHOLD = 0.2; // per-pixel colour distance, 0-1
const MAX_DIFF_PIXEL_RATIO = 0.01; // share of the image allowed to differ

export default {
  screenshots: {
    threshold: PIXEL_THRESHOLD,
    maxDiffPixelRatio: MAX_DIFF_PIXEL_RATIO,
    stylePath: "./visual/stabilize.css", // injected into every capture
  },
};
```

The two knobs answer different questions and are not interchangeable. `threshold` decides whether a _single pixel_ counts as different, which is what anti-aliasing needs. `maxDiffPixels` / `maxDiffPixelRatio` decide how many differing pixels are tolerated, and nothing needs those above about 1% except a subject that should have been masked.

Full code: [examples/core.md](examples/core.md)

### Pattern 2: The Matrix Comes From Configuration

One test, N approved images. The configuration cell's name enters the baseline path, so each cell is approved independently.

```typescript
projects: [
  { name: "desktop-light", use: { viewport: DESKTOP, colorScheme: "light" } },
  { name: "desktop-dark", use: { viewport: DESKTOP, colorScheme: "dark" } },
  { name: "mobile-light", use: { viewport: MOBILE, colorScheme: "light" } },
  {
    name: "second-browser",
    use: { browser: "firefox" },
    ignoreSnapshots: true,
  },
];
```

Duplicating a test per theme means every subject is written twice and the one nobody remembers to add silently stops covering anything. `ignoreSnapshots` keeps a browser in the functional run without a second baseline set to maintain.

Full code: [examples/core.md](examples/core.md)

### Pattern 3: Determinism Before Assertion

Six sources of nondeterminism account for nearly every flaky visual test, and each has a fix cheaper than the flake.

| Source               | Symptom in the diff                             | Fix                                                              |
| -------------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| Web fonts            | Whole text blocks shift; fallback metrics       | Self-host and preload, then await `document.fonts.ready`         |
| Animation/transition | Random intermediate frames                      | Disable CSS motion at capture; stop JS-driven motion too         |
| Time                 | "2 minutes ago", clocks, date-stamped rows      | Freeze the clock before navigating — freeze, do not fast-forward |
| Randomness           | Shuffled lists, random ids, placeholder avatars | Seed the generator before any application script runs            |
| Data                 | Row order and counts vary per run               | Serve fixed fixtures with stable ordering and identifiers        |
| Scrollbars / DPR     | ~15px width shift, blurry text at 2×            | Hide scrollbars in the stabilizing stylesheet; pin scale         |

```typescript
await freezeClockAt(new Date("2026-01-15T12:00:00Z")); // before navigation
await goto(DASHBOARD_URL);
await page.evaluate(() => document.fonts.ready); // a real signal, not a guessed delay
await matchScreenshot(summaryRegion, "summary.png");
```

**The seventh source is the machine.** Baselines generated on a laptop and diffed in CI produce a permanent full-frame difference on every subject, which trains the team to regenerate blindly, which destroys the suite.

Full code: [examples/determinism.md](examples/determinism.md)

### Pattern 4: Scope the Capture to the Subject

| Subject                                   | Capture                        |
| ----------------------------------------- | ------------------------------ |
| A component or one of its states          | Element capture                |
| A band or region spanning components      | Page capture with `clip`       |
| Whole-page composition (landing, invoice) | Page capture with `fullPage`   |
| Anything above the fold                   | Page capture, default viewport |

```typescript
await matchScreenshot(
  page.getByRole("region", { name: /pro plan/i }),
  "pricing-card-pro.png",
);
await matchScreenshot(page, "header-band.png", {
  clip: { x: 0, y: 0, width: 1280, height: 96 },
});
```

A full-page capture used to prove a button changed fails on every unrelated header edit — and fails every _other_ full-page baseline at the same time, so the reviewer sees dozens of red subjects, no signal, and the fastest way out is a blanket regenerate.

Full code: [examples/core.md](examples/core.md)

### Pattern 5: Mask What Moves

```typescript
await matchScreenshot(page, "dashboard.png", {
  mask: [byTestId("last-synced-at"), byTestId("live-visitor-count")],
  maskColor: "#000000", // defaults are often magenta, which some UIs legitimately contain
});
```

The mask list doubles as documentation of exactly which parts of the frame are not covered. Raising `maxDiffPixelRatio` until the timestamp stops failing buys enough slack to hide a missing sidebar, and says nothing about where the slack went.

Where a volatile region has no stable handle to mask, hide it in the stabilizing stylesheet instead — that needs only a selector.

Full code: [examples/core.md](examples/core.md)

### Pattern 6: Baseline Lifecycle

Three legitimate events — **create** (a new subject appears), **accept** (an intended change is reviewed and approved), **retire** (the subject is deleted and its images go with it). Anything else is drift.

```bash
# WRONG - the "visual tests are failing" reflex
npm run test:visual -- --update-all

# RIGHT - look first
npm run test:visual                  # emits expected/actual/diff per failure
npm run test:visual:report           # inspect every diff
npm run test:visual -- --update-changed   # only after each one is understood
```

Updating only _mismatched_ baselines is not the same as updating everything: the blanket mode rewrites matching baselines too, silently resetting subjects nobody inspected.

**The update travels with the change.** New images belong in the same pull request as the code that changed the appearance. A separate "update baselines" commit is unreviewable — nobody can tell an intended redesign from a regression once the two are in different diffs.

**Ownership is explicit.** The author who changed the UI _proposes_ baselines and says in the description what should have changed; someone else _accepts_. Author self-acceptance removes the only human judgement in the loop.

Full code: [examples/ci.md](examples/ci.md)

### Pattern 7: CI Wiring and Cost Control

Visual checks run on pull requests and on every trunk build — trunk builds are what keep baselines valid through merges. They skip documentation-only and config-only changes, and they never run in update mode in an automated job.

```yaml
# Pipeline definition; the syntax varies by provider, the shape does not
- name: Visual tests
  run: npm run test:visual
- name: Publish diffs
  if: always-except-success-only # must also fire on timeout and cancellation
  # upload the report and results directories as a build artifact
```

A job whose only output is "1 failed" forces a local reproduction of a container-specific render, so the reviewer regenerates instead — which is the failure this whole skill exists to prevent.

**Treat the matrix as a budget.** Every new cell multiplies the whole corpus: its capture time, its review surface, and its bill. Add one when a real class of bug lives there, and delete one that has never caught anything.

Full code: [examples/ci.md](examples/ci.md)

</patterns>

---

<red_flags>

## Red flags

**Breaks at runtime:**

- A blanket baseline update run to clear a red build — from that commit the suite asserts whatever was on screen, including the regression, and will never report it again
- Committing baselines rendered on a developer machine — every subject shows a full-frame diff against CI, the suite is declared broken, and it gets disabled
- Capturing while the page is still settling — in-flight requests, entrance animations, unloaded fonts — which produces intermittent diffs that get "fixed" by regenerating
- An automated job that runs in update mode and commits the result — green by construction, asserting nothing
- Naming baselines after test order (`step-3.png`) — reordering silently reassigns approved images to different subjects
- Renaming a configuration cell — its name is part of the baseline path, so every image under it is orphaned and the next run happily creates fresh "baselines"

**Surprising behaviour:**

- Comparators self-stabilize by re-capturing until two consecutive frames match, then diffing the last — that removes render jitter, not application nondeterminism
- The screenshot assertion usually disables CSS animation and hides the caret already, so most per-call option noise is restating defaults
- Masked regions are filled with a default colour a UI can legitimately contain, which makes the mask invisible in the diff
- `clip` and `fullPage` exist on the page-level capture only; for an element, capture the element rather than computing its box
- Tolerance numbers do not port between harnesses — different algorithms on different scales, so a value copied across means nothing
- Cloud modes are keyed by **name**: changing a mode's viewport under the same name keeps comparing against the old baseline, while renaming one starts a fresh baseline with no history
- Modes and matrix cells **stack** across project, component and subject level rather than overriding, so a catalog-wide default multiplies everything beneath it
- Change-based targeting depends on intact git history and a lockfile in sync with the manifest; rebases, squashes and force pushes fall back to full rebuilds
- Loosening tolerance until the noise stops trades a named uncovered region for an unnamed one
- Masking so much of a frame that the remaining pixels prove nothing — at that point delete the test
- Visual assertions mixed into functional test files mean one flaky image blocks feedback on unrelated behaviour
- WebP baselines cut repository growth substantially against PNG once the corpus is large

</red_flags>

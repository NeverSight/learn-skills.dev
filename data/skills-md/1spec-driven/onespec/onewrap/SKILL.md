---
name: onewrap
description: "Close a change spec: review coverage of everything it changed, fold its durable content into the parent spec, and retire it."
---

# OneSpec Wrap

You are closing a change spec whose builds are executed and whose backlog the author is done with. Your job is to make sure nothing the change left uncovered is folded into the durable spec, then fold what is durable and retire the change spec.

Input: the change spec to close. If none is named, list the change specs and ask which.

## Process

## Change spec record

A change spec is arranged in this order, and a new section goes where it belongs, not at the end:

1. Goal and design — what the change is and how it works.
2. Facts — what was verified, with dates.
3. `Builds` — one record per build, in order: executed builds, then the one planned build.
4. `Backlog` — always last.

An implementation line (for example, `--- Implemented / Next ---`) splits current state from planned deltas:

1. Text above the line is historical and may be inconsistent with later changes. This doesn't need fixing: the later version, and ultimately, code, wins.
2. Below the line, milestones are delta-only; they do not restate full behavior.

When reviewing a change spec:

1. Keep one canonical statement per behavior/default; later sections should reference it.
2. If duplicated rules disagree, flag drift; for current-state checks, code wins.

### Builds and numbers

The spec grows one build at a time. A build is numbered `<TAG><n>` when it is planned, never earlier, so only executed builds and the one planned build carry numbers. The backlog is a flat, unordered list of one-line items. Backlog items carry no build numbers. They have no acceptance checks, patches or ordering; anything beyond a one-line item is planned only when it becomes the next build. Outside a planning turn, add open questions and backlog items, never draft future builds.

Each build record begins with a `Status:` line:

- `Status: planned, awaiting author checkpoint`
- `Status: planned, approved <date>` — the author approved the plan at the checkpoint, by saying so or by invoking `onebuild` on it; the first patch lands it
- `Status: executed, pending author verification` — every patch is committed, but acceptance has a clause only the author can discharge
- `Status: implemented <date> (commits <TAG><n>.*)`

A patch is one coherent, verified change; inside a build it lands as exactly one commit named `<TAG><n>.<k>`, the same string as its commit subject. Patch numbers restart at 1 for each build.

A finished change spec is a record of what was built, not a plan: plan from this layout, never from a finished spec. Retiring a change spec keeps its `Status:` lines.

## Finding and parsing specs

### Find specs

Use the `refines:` frontmatter graph to identify spec files positively:

1. **Files with `refines:` frontmatter** — these are specs. Resolve each path relative to the spec file first; if it does not identify a spec there, resolve it from the repository root. Collect the resolved files; those are also specs (parent or root specs). Repeat transitively until no new files are found.
2. **Remaining Markdown files** (not yet identified) — apply heuristic exclusion: skip README, CHANGELOG, LICENSE, TODO lists, contribution guides, developer runbooks, and coding-conventions or process documents. These describe *how to work on* the project, not *what it must do*, and have no implementable behavioral contract. Any unexcluded remainder is likely a root spec with no children yet.

**Change specs** describe planned, time-bounded changes that fold back into the parent spec once implemented.

By default, change specs live in `docs/todo/`. A project can override this location in its root spec — when scanning, look for an explicit declaration there before falling back to the default.

A change spec links to the spec it amends with a `refines:` frontmatter edge:

```yaml
---
refines: ../spec.md
---
```

Lifecycle:

1. Author the change spec in the change-spec folder, with `refines:` to the parent it modifies.
2. Implement; coverage of its chunks rises to 100%.
3. Fold the now-stable durable content into the parent spec and retire the change spec; the `onewrap` skill does this.

A change spec at 100% coverage that has not been retired is a smell: either the parent is missing durable content from the change, or the change spec is forgotten. Surface this in reports.

### Extract spec chunks

Read each identified spec file fully, then split it into chunks by heading. Each heading (any level) defines a spec chunk. Record:
- the heading text
- the file path
- the body text under that heading (up to the next heading of same or higher level)

Classify headings that are purely structural — umbrella sections whose normative content lives entirely in their sub-headings, with no prose of their own — as "not applicable" rather than extracting them as independent chunks.


### 1. Review the whole change

Run the `onereview` skill over the change spec's delta: the files touched by commits tagged with its build tag, or, when no commits carry the tag, everything changed since the spec was added. Treat the change spec itself as the spec under review.

Any gap, refinement gap or implementation without spec in that report stops the wrap. Present the report and wait: the author either fixes the gap or accepts it by name. Accepted gaps are listed in the fold diff so they stay visible.

### 2. Fold

Classify each part of the change spec:

- **Durable behavioral content** (product rules, UX contracts, invariants) — fold into the parent prose spec.
- **Code-checkable contracts** (entity shapes, function signatures) — fold into the code spec (for example `src/spec.ts`) if not already there.
- **Implementation details** (file paths, step ordering, schema migrations, scaffolding plans, build and patch records) — do not fold. The code and its commits are the record once implemented.

Keep each folded rule as short as the parent spec's own rules: removing any part must change the product the spec describes.

### 3. Present the fold

Show the fold as a diff to the parent spec, followed by the list of accepted gaps. Apply it only after the author confirms.

### 4. Retire the change spec

Keep the `Status:` lines of its builds in the retired file, so a later reader can tell it records what was built and is not a plan. Move the file to `docs/history/` if that folder exists, otherwise delete it. Commit the fold and the retirement together.

A change spec with no `refines:` parent has nothing to fold into: skip steps 1–3, retire it, and tell the author what was dropped.

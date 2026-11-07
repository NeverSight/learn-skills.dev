---
name: onereview
description: "Ongoing spec coverage check. Find new gaps, suggest (spec) annotations, and flag implementation without spec. Run after code changes to keep specs and code in sync."
---

# OneSpec Review

You are performing an ongoing OneSpec review. Your job is to check the current state of spec coverage — find gaps, suggest annotations, and flag implementation that has drifted from specs. This assumes the project already has specs; for first-time onboarding use `onespec` instead.

Default to a routine delta review. If git context is available, start with changed source code and Markdown files, then pull in directly related specs, tests, and nearby implementation modules as needed. Expand to a broader workspace review only when the user asks for it, git context is unavailable, or the delta-first pass cannot resolve ambiguity.

## Process

Follow the steps and rules below, then continue with the review-specific steps.

Prioritize issues introduced or exposed by the changed area: new gaps, stale `(spec)` references, unverified implementations, and implementation behavior that has drifted away from the relevant specs.

When the project has change specs, read [the change-spec record](change-spec.md) for their layout and workflow.
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

### Scope and search strategy

Limit review work to source code files and Markdown files in the workspace.

Ignore generated, vendored, dependency, build, cache, coverage, lockfile, and binary outputs unless the user explicitly asks to include them.

When classifying evidence:
- **implementation**: prefer source code files. Markdown may provide supporting context, but do not treat ordinary prose as implementation evidence.
- **test**: prefer test files, test modules, or executable examples in source code. Markdown examples count only when they are clearly verification artifacts used by the project.

### Search for implementation and tests

For each spec chunk, search the codebase for code and tests that appear to implement or verify it. Use a combination of:
- semantic search for the concepts described in the chunk
- grep for key terms, function names, or identifiable phrases from the spec

Classify what you find:
- **implementation**: source code that appears to implement the behavior described
- **test**: test code that appears to verify the behavior described

Be conservative. Only claim a match when the code clearly relates to the spec chunk. When uncertain, say so.

### Refinement gaps

When a prompt asks for refinement gaps, use these categories:
- **Broken refinement edges**: a `refines:` path that matches no discovered spec file when resolved relative to the spec file first, then from the repository root.
- **Unrefineable breadth**: a spec chunk that is too broad to implement directly, has no child spec refining it, and has no direct implementation.

### Reporting limits

Always report full counts for each section.

When a section would contain more than 10 items, show the 10 most important examples and summarize the remainder as omitted items.

## Rules

- Do not modify any files. This is a read-only review.
- Do not invent spec chunks that aren't in the spec files.
- If a spec chunk is too abstract to map to code (e.g., a principle like "Simplicity"), classify it as "not applicable" rather than a gap.
- If the project has no spec files, say so and stop.

## `(spec)` annotation format

When suggesting `(spec)` annotations, use exactly this format — no variations:

```
(spec) <heading text>
```

- No colon after `(spec)`.
- No file path. The heading alone identifies the chunk.
- No `§` section sign or any other signs.
- If two specs share a heading, disambiguate with the parent heading: `(spec) <parent heading> / <heading>`.
- Use idiomatic comment syntax for the target language (`#`, `//`, `"""..."""`, etc.).

## Required report section: Change specs

Every onboard and review report includes this section, between "Refinement gaps" and "Not applicable":

```
### Change specs (<count>)
Spec files in the change-spec folder, with their lifecycle status.

- **<file path>** (`refines: <parent>`) — <covered>/<total> chunks covered
  - **READY TO RETIRE**: 100% covered; run `onewrap` to fold it into <parent> and retire this file.
  - or: <count> chunks remaining
```

If the project has no change specs, omit the section.


### Produce the report

Output a structured report in this format:

```
## OneSpec Review — <project name>

**Summary**: <covered>/<total> spec chunks covered (<percentage>%), <partially> partially covered, <not covered> not covered, <gaps> gaps (partially covered and not covered chunks combined), <reverse> implementation behaviors without spec, <retire> change specs ready to retire

### Not covered (<count>)
Spec chunks where neither implementation nor tests were found.

- **<heading>** (<file path>) — no implementation or tests found

### Refinement gaps (<count>)
Spec chunks that are too broad to implement directly and have no child spec
refining them. Broken `refines:` edges (targets that don't match any spec file).

- **<heading>** (<file path>) — needs child spec to refine before implementation
- **<file path>** — `refines: <target>` does not match any spec file

### Partially covered (<count>)
Spec chunks where implementation or tests were found, but not both.

- **<heading>** (<file path>)
  - implementation: <file>:<line> — `<function>`
  - test: none found — **gap**

### Covered (<count>)
Spec chunks where both implementation and tests were found.

- **<heading>** (<file path>)
  - implementation: <file>:<line> — `<function or class>`
  - test: <file>:<line> — `<test function>`
  - suggested: add `"""(spec) <heading>"""` to <locations>

### Not applicable (<count>)
Spec chunks that describe process, principles, or non-functional aspects
that don't map to specific code (e.g., "Simplicity", "Non-goals"), and
umbrella sections whose normative content lives entirely in their sub-headings.

- **<heading>** (<file path>) — <reason>
```

Keep the structure above, but if any section exceeds 10 items, show the 10 most important examples and summarize the remainder.

### Suggest annotations

For each covered or partially covered chunk, suggest the exact `(spec)` annotation to add and where to add it.

```
Add to <file>:<line>:
  # (spec) <heading text>
```

### Reverse coverage (code → spec)

After the forward pass, perform a reverse pass over the implementation files discovered during search.

Deduplicate implementation files before scanning them.

For each file that was identified as implementing a spec chunk, scan it for behaviors that are:
- **User-visible or have external side effects** — writes files, makes network calls, modifies system state, changes OS configuration
- **Non-trivial** — not boilerplate serialization, not logging, not error wrapping

For each such behavior, check whether any spec chunk covers it. If not, flag it as **"implementation without spec"**.

Be conservative. Only flag behaviors that are clearly significant and clearly missing from the specs. When uncertain, omit.

Add a new section to the report:

```
### Implementation without spec (<count>)
Significant behaviors found in implementation files that no spec chunk covers.

- **<behavior name>** (<file> — `<function(s)>`)
  behavior: <what it does>
  spec coverage: none found
  suggested: add entry under <spec file> / <heading>
```

For each flagged behavior, suggest which existing spec file and heading the new entry should be added under. If no natural home exists, suggest creating a new spec section.

If you encounter materially duplicated implementations of the same user-visible behavior during the normal reverse pass, flag them as a smell. Do not broaden the search just to hunt duplicates.

Report them in a separate section:

```
### Possible duplicate implementations (<count>)
Repeated implementations of the same significant behavior encountered during review.

- **<behavior name>** (<file A>, <file B>)
  why it looks duplicated: <reason>
  spec coverage: <covered|none found>
  suggested: consolidate, share the implementation, or add spec rationale if duplication is intentional
```

Also scan test files discovered during search. Flag tests that verify **distinct user-visible behaviors** not covered by any spec chunk. Ignore tests that cover error handling, edge cases, or implementation-level defensive checks — these don't warrant spec entries. Report these separately at lower priority:

```
### Tests without spec (<count>)
Tests that verify user-visible behaviors not covered by any spec chunk.

- **<test name>** (<file>:<line>)
  verifies: <what behavior the test checks>
  spec coverage: none found
  suggested: add entry under <spec file> / <heading>
```

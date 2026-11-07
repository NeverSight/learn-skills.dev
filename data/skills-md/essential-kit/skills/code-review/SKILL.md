---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along four axes: Standards (documented coding standards), Spec (fidelity to the originating issue/spec), Simplification (less complexity, duplication, or reimplementation), and Optimization (performance and scaling opportunities such as N+1 queries, batching, caching, and overload risks). Runs four reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
---

Four-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?
- **Simplification**: can the change stay correct with less complexity, duplication, or reimplementation of existing code?
- **Optimization**: does the change introduce avoidable performance and scaling costs under realistic load: N+1 queries, serial I/O, unbounded fan-out, missing batching/caching/indexes, or overload risks?

Each axis runs as a **parallel sub-agent** so they don't pollute each other's context, then this skill aggregates their findings.

The originating issue or spec usually lives in **GitHub Issues**. Fetch it with the `gh` CLI, which infers the repository from the clone. When findings name domain concepts, use the vocabulary from `GLOSSARY.md` (or the per-context glossaries that `GLOSSARY-MAP.md` points at).

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, not inside parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`), fetched with `gh issue view <number> --json number,title,body,comments`. GitHub shares one number space across issues and PRs, so when `gh issue view` doesn't resolve it, try `gh pr view <number> --json number,title,body,comments`.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list. Include ADRs under `docs/adr/` or `src/*/docs/adr/` that constrain the area the diff touches.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn the sub-agents in parallel

Dispatch all four sub-agents together, in the foreground, and aggregate the reports they return. Omit Spec when no spec is available, and Optimization when the diff cannot affect runtime behaviour. If the user asked for an optimization pass only, dispatch only the Optimization sub-agent and scope it to the target they name (a diff, file, module, endpoint, or the whole codebase); report under `## Optimization`. All reviewers are read-only: inspect source and return findings without edits or build, lint, test, or formatter runs.

**Standards sub-agent prompt** should include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** should include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

**Simplification sub-agent prompt** should include:

- The diff command and commit list, standards-source files, and spec path or contents when available.
- The brief: "Look for changes that can satisfy the same requirements with a smaller, more reused implementation. Apply KISS (choose the least complex design that works), YAGNI (build for current requirements), and DRY (give each piece of shared behavior one owner). Before proposing new code or an extraction, inspect each changed implementation and search the repository outside the diff for existing helpers, components, services, types, and shared modules. Read the candidate code and representative callers so you can check semantics, errors, side effects, and module boundaries.
  - **Reuse:** the change recreates an existing capability. Point to the existing symbol and path, and show the call that would replace the new implementation.
  - **De-duplication:** the change repeats domain logic or creates a second implementation of the same behavior. Favor the current canonical owner. If a new shared abstraction is warranted, name the current callers and the ownership rules it must respect.
  - **Simplification:** the change includes branches, indirection, wrappers, abstractions, configuration, or extension points that current requirements do not need. Recommend the smallest deletion or refactor that keeps behavior intact.
  Scope the review to opportunities introduced or exposed by the diff; unrelated cleanup belongs elsewhere. Match abstraction size to current needs: similar-looking code is not enough reason to share semantics or couple modules. For every finding, give the changed file and lines, the existing code or callers that support it, the replacement or refactor, and the benefit plus compatibility risk. When no compatible reuse candidate exists, say what you searched for any proposed extraction. Mark opportunities as judgement calls unless a documented rule backs them; leave out style-only preferences and tooling-enforced findings. Return under 400 words, or state that you found none."

**Optimization sub-agent prompt** should include:

- The diff command and commit list, plus the spec/issue when available.
- The relevant performance and scaling checklist from [SCALING.md](./SCALING.md) (or the subset that matches the changed stack), pasted into the prompt (the sub-agent has no other access to it).
- The brief: "Review the changed code for concrete performance and scaling opportunities introduced or exposed by the diff. Follow the changed call path outside the diff when needed to prove a finding. Prefer approach-level changes (batch, join, index, cache, queue, pagination) over micro-optimizations. Name the operation, its expected scale, and the bottleneck mechanism before proposing a fix. Look for:
  - **N+1 and chatty I/O:** queries or remote calls inside loops, especially a bulk endpoint that issues one query per item; lazy loading; serial awaits for independent work. Prefer set-based or batch queries, joins, eager loading, or a request-scoped loader; chunk large batches.
  - **Unbounded work:** fan-out or concurrency without a bound; loading whole result sets; deep offset pagination; oversized payloads. Bound concurrency, stream or paginate, and project only needed fields.
  - **Database cost:** missing or misused indexes, full scans, over-fetching, per-row writes in a bulk request, write amplification, long transactions, lock contention, connection churn, hot partitions.
  - **Repeated cost:** expensive reads or computations that are reused and could be cached, materialized, or precomputed; call out invalidation, staleness, and stampede risk.
  - **Overload and tail latency:** missing timeouts, retries without backoff/jitter or a retry budget, missing circuit breakers/bulkheads/load shedding, work that belongs on a queue, and fan-out that amplifies p99.
  For each finding, cite changed file/lines, state the mechanism and expected impact, propose the smallest fix, and name the trade-off (consistency, complexity, memory, write cost). Mark whether the finding is proven by the code path or needs measurement, and name the measurement (query count, `EXPLAIN ANALYZE`, profile, load test, p99). Omit micro-optimizations and speculative rewrites that lack a plausible scaling mechanism. Return findings under 400 words, or explicitly report none."

### 5. Aggregate

Present the reports under `## Standards`, `## Spec`, `## Simplification`, and `## Optimization` headings, verbatim or lightly cleaned. Keep the axes separate: standards compliance, requirements coverage, simplification, and performance/scaling are distinct judgements. When reviewers identify the same issue, keep its detail under the most relevant axis and cross-reference it from the other; count it once.

End with a one-line summary: finding counts per axis, noting any skipped axis, and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

## Why four axes

A change can pass one axis while raising findings on another:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**
- Code that meets standards and requirements but duplicates an existing capability → **Standards and Spec pass, Simplification opportunity.**
- Code that is clean and correct but issues one query per item in a bulk request → **Standards, Spec, and Simplification pass, Optimization fail.**

Reporting them separately stops one axis from masking another.

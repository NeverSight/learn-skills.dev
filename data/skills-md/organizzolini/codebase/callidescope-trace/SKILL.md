---
name: callidescope-trace
description: Run callidescope and read what it printed — a whole-workspace trace, one project's gate verdict, or the depth and breadth commands against one or more callables, each addressed as file#qualified-name. Use when running callidescope or npx callidescope, when reading a call stack or a breadth row, when reading what a per-project gate or trace target printed, when reading a project readme's Limits table, when a depth printed as "≥ n" needs interpreting, when reading a committed markdown report, mermaid diagram, or JSON report, when a run narrowed with --directories reports a frame, a stack, or a project the run was never pointed at, when a depth moved without an edit that explains it, or when asking who calls this, what does it call, what would this rename touch, and where should this callable be split before a refactor starts.
license: MIT
---

# Running callidescope and reading what it says

Callidescope builds one call graph for a TypeScript workspace and measures the
shape of it. It follows calls through **injected dependencies** — the hop from
`this.someService.load()` into `SomeService.load` — which is the edge no
file-at-a-time tool can see, and where most of a framework codebase's control
flow actually lives.

Three commands, answering three different questions:

```bash
npx callidescope                                        # the whole workspace
npx callidescope depth --addresses src/foo.service.ts#FooService.bar    # one callable, vertically
npx callidescope breadth --addresses src/foo.service.ts#FooService.bar  # one callable, horizontally
```

A repository with no workspace configuration file is traced with defaults
rather than told to write one, so a bare run always produces something.
**A traced project's own `callidescope.config.ts` is a different matter**: it
must exist and must be complete, or the run is refused before anything is
traced — see the `callidescope-configure` skill. What a run _gates_ on and what
it _writes_ are both opt-in and both live in that skill; this one is about
reading the result.

## `callidescope`: the whole workspace

Reports two findings, both per project.

**Deep call stacks.** The single deepest path below each entry point, when it
exceeds `limits.maximumDepth`. Only one path per entry point is ever built, so
a wide graph costs no more than a narrow one.

**Breadth.** How many callables one callable calls directly. Reported always;
gated only when a project declares `limits.maximumBreadth`, which is the one
limit with no default anywhere.

**Each finding carries the limit it was weighed against**, because that limit is
a fact about the project owning the stack's root rather than about the run. One
report routinely holds several different numbers, and two identical stacks in
two projects can be a finding in one and silent in the other with nothing about
the code differing.

## Reading a stack

```text
Stack #1 | 🚨 [DEPTH ≥ 10 > 6] (decorated-method)
🚀 SomeCommand.run(options: SomeOptions): Promise<void> [.../some.command.ts:220]
   ↳ Measure the repository and write every configured output.
  └─> SomeService.measure(args: MeasureArguments): Result [.../some.service.ts:115]
     ↳ Measure aggregated statistics for the provided directory.
```

- **`≥ 10` is a floor, not a measurement.** Something on that path could not be
  followed — a callback invoked through a parameter, a computed member name —
  and the run says so rather than quietly under-reporting. The real depth is at
  least ten. Not a defect, and not a number to distrust: `≥ 10` against a limit
  of 6 is a genuine failure. `Unfollowable calls` in the summary counts them.
- **The parenthesized kind is the entry-point rule that claimed the root.**
  `orphan-root` means nothing in the repository calls it: either dead code, or
  an entry-point rule the configuration is missing.
- **Every frame carries `file:line`**, so the next step is opening one.
- **Each frame is annotated from the type checker** — the signature, and the
  JSDoc prose collapsed to one line — which is what makes a stack readable
  rather than a list of places to go look. A frame printed `(…): ReturnType`
  had a signature over 80 characters, almost always a constructor taking a
  dozen injected services. A summary over 120 characters prints only its
  opening sentence, unmarked; only a single sentence with no boundary to cut on
  is trimmed and marked `…`.

**Shortening applies to the printed tree only.** The JSON report carries every
comment in full, so a script wanting complete text should read JSON rather than
parse the tree.

**The mermaid rendering draws all the stacks as one flowchart**, not one
apiece. A single stack is a straight line, and a straight line is a list with
extra steps; drawn together the shared tails converge — every command reaching
the same repository, every resolver ending in the same service — and that
convergence is what a picture shows and an indented tree cannot. Entry points
are stadiums and everything else boxes, shape rather than color because the
diagram is read in whichever theme the reader has. A diagram stops at 300
callables, drops whole stacks rather than trimming so it never contains an edge
into something it did not draw, and says how many it left out.

## Reading a per-project verdict

In a workspace using `@callidescope/nx`, the thing a branch actually runs is one
project's `gate`, and what it prints is **not** a smaller report. It prints the
two findings it weighed and nothing else:

```text
## Call stacks over the depth limit (1)
...the stack, as a tree...

## Callables over the breadth limit (1)
- `GatedLeafService.read` — 3 direct callees, limit 2 (…/gated-leaf.ts)
```

Four things to hold on to when reading one:

- **The findings are the judged project's own.** A gate traces its project
  together with that project's Nx dependencies, and then judges only what the
  project it is named after owns. A dependency's breach is that dependency's own
  gate's business — so a gate that failed is telling you about one project, and
  the fix is that project's code or that project's own `callidescope.config.ts`.
- **A gate's exit code is the verdict and nothing else.** It reads no
  destination, so a failing gate has changed no committed file, and a passing
  one has published nothing.
- **The summary's `Deepest stack` is not the number the verdict used.** A
  scoped run's counts describe the whole trace, dependency closure included, so
  the deepest stack it reports is routinely deeper than anything the judged
  project owns. Take the number a verdict gives you, never the one a summary
  line prints. The same caution applies to a `🔭 Finished an analysis` log
  line — see the `callidescope-triage` skill.
- **`## Read nothing of its own (0 files)` is a failure about the run, not the
  code.** The gate judged a project whose own sources it never opened, so a
  green verdict would mean only that it never looked. The `trace` target prints
  the same block and passes; the gate is the one that fails on it.

The sibling `trace` target prints the whole report instead — the summary, a
`Projects` index with one row per project against **its own** limit, and a
`Depth headroom` scoreboard. Reach for `trace` to understand a project, and
read a `gate` to understand why a pipeline is red.

## Reading a committed project block

Every traced project's own readme carries a `## 🔭 Callidescope` section, and
its `### Limits` table is what says which numbers that project is held to:

```text
| Limit | Value |
| --- | --- |
| `maximumDepth` | 4 |
| `maximumBreadth` | none |
```

**There is no origin column, and no second origin left to record.** Every
traced project's own `callidescope.config.ts` is complete — it spreads the
workspace's `projectDefaults` and overrides what it means to — so both numbers
are written in the file beside this readme, or the run refused to start before
anything was traced. `none` means that project's own file names no breadth
limit — see the `callidescope-configure` skill for why that is a deliberate
statement rather than an omission.

Read the `Deepest stack` row of the summary above it against the depth limit
here: the two together are the whole of what that project's gate decides.

## Addressing one callable

`depth` and `breadth` take `<file>#<qualified-name>` — the file path and the
qualified name callidescope already prints in every stack frame, joined by `#`.
It is the same shape a Python traceback or an ESLint rule id uses, which means
it is exactly what you can copy out of a report.

A file holding more than one declaration under the same qualified name — two
overloads, two callbacks bound to the same property — is disambiguated with a
trailing `:<line>`:

```bash
npx callidescope depth --addresses src/foo.service.ts#FooService.bar:118
```

When it cannot tell which one was meant, the run says so and prints every
candidate's line, so the disambiguated address is a copy away.

Neither command writes anything, compares a destination, or takes `--check`,
`--write`, `--json`, `--markdown`, `--mermaid`, `--maximum-depth`, or
`--maximum-breadth`. A lookup only ever prints. Both do take every flag that
shapes the graph — `--directories`, the entry-point overrides, and the two
exclusion lists — plus `--config` and `--format`, because resolving an address
still means tracing the workspace first.

## `breadth`: what it calls, and what calls it

Prints the callable's **direct callees and direct callers side by side** — the
two questions a refactor or a rename needs answered together, before either one
is safe.

- **A rename.** The callers are the exhaustive list of what has to be updated.
  This is the one question a text search answers badly in a
  dependency-injected codebase: a call through `this.someService.load()` is
  found by the type checker and missed by a grep for the class name.
- **An extraction.** Extracting a responsibility out of a wide callable means
  moving _some subset of the callees it names_. The callee list is the raw
  material for choosing the seam — look for the subset that shares a concern,
  and take those.
- **An inline.** A callable with one caller and few callees is a candidate for
  folding into that caller. Breadth confirms the "one caller" part rather than
  assuming it.

It reports on a callable nobody has flagged. It does not need a finding to be
worth running.

## `depth`: every chain above and below

Prints **every path above the callable and every path below it** — every caller
chain up to a root, every callee chain down to a leaf — rather than folding
each direction into the single deepest one that `callidescope`'s own report
keeps.

That difference is the point. The workspace report answers "how deep does this
get", so one path per entry point is enough. `depth` answers "what is this
callable actually part of", and a callable reached from a dozen places, or
reaching a dozen leaves, is exactly the shape it is asked to show in full.

Each direction is capped at 200 paths, and a capped run says so. The cap exists
because a widely-called utility whose callees fan out just as wide multiplies
those branches together — enumerating every path is not bounded by construction
the way one deepest path is.

- **Turning a depth finding into a plan.** The workspace report names the
  stack; `depth` against a frame in the middle of it shows every _other_ chain
  that frame participates in, which is what tells you whether collapsing a
  forwarding layer is safe or whether three other callers depend on it.
- **Testing a "this looks misplaced" hunch.** The caller trees show where the
  callable is really used from, in full rather than folded into one deepest
  path.

## Which one to reach for

| The question                                        | The command    |
| --------------------------------------------------- | -------------- |
| Is anything in this workspace too deep or too wide? | `callidescope` |
| What breaks if I rename this?                       | `breadth`      |
| Where do I cut this callable in two?                | `breadth`      |
| Can I inline this?                                  | `breadth`      |
| Can I collapse this layer?                          | `depth`        |
| What is this callable actually part of?             | `depth`        |
| Does this belong in this file?                      | `depth`        |

## What a scoped run measures

`--directories` narrows a run to the project directories it names, and the trace
still follows calls out of them: a scoped run builds a program for each named
project **and for every project those projects' imports transitively reach** —
their **dependency closure**. So a call into another workspace package lands on
a real frame, and the run reports frames, stacks, and per-project rows for
packages it was never pointed at. That is the closure, not a leak.

**How to read a depth that moved.** A project's own `tsconfig.json` never lists
the packages it imports, so a scoped run used to leave every call out of the
named directory in code no traced project owned — and a call into unowned code
is treated as external, a leaf, exactly like a call into an installed package.
The stack ended at the package boundary and printed a plain number, with nothing
in the report saying it had stopped early. A number that went up without an edit
to explain it is that under-measurement being corrected.

Three things follow, and they are what a moved number should be checked against:

- **A scoped depth is a measurement, not a floor.** `≥` still means only an
  unfollowable call. Scope never printed one, which is exactly why a scoped
  under-measurement was invisible.
- **The number does not depend on which run took it.** A file is owned by the
  deepest project root containing it, whichever program pulled it in, so two
  scoped runs and the whole-workspace run agree about the same callable —
  provided each of them builds the project declaring it, which a refused
  destination's is not.
- **A whole-workspace run's closure changes nothing.** It names no directory,
  so every project is already a starting project and its closure is the
  workspace. A number that moved there moved for some other reason.

**What a closure does not reach**, and why each one is left out:

- **Dependents, deliberately.** The walk runs downward only. A project that
  imports the scoped one is not built and its stacks do not appear — which is
  what stops an edit in a dependent from moving the scoped project's numbers.
- **A project root holding no `package.json`.** A manifest is what makes a
  directory something another project can depend _on_; a root holding only a
  `tsconfig.json` is shared settings, read by every project rather than depended
  on by any. Without the rule, one such directory drags the whole workspace in.
- **The workspace root.** A project whose root contains every other project
  cannot be a meaningful dependency of any of them.

Both refusals apply to a _destination_ only, so either kind is still traced in
full when named directly or by a run that names no directory. What they cost is
that a call into a refused directory resolves to no frame.

**Depth and breadth both survive a downward-only scope**, which is worth saying
because it is not obvious: both fold over a callable's transitive **callees**,
which run downward — precisely what a closure holds in full. Neither needs a
dependent.

**Publishing does not widen with measurement.** Each project's own
`write.markdown` (and `write.mermaid`, when it declares one) is written only for
the projects a run was scoped to, so a scoped run never rewrites a section in a
dependency it merely measured.

A worked example — the projects one real scoped run reaches, and why each — is
`examples/dependency-closure` in the `@callidescope/examples` package.

## What the graph does and does not contain

The same resolution rules govern all three commands, and they decide what any
of them can tell you.

| Written as            | Resolved to                                                  |
| --------------------- | ------------------------------------------------------------ |
| `helper()`            | The symbol at the callee, unwrapped through import aliases   |
| `this.service.load()` | The symbol at the member name — the injected-dependency case |
| `provider.ingest()`   | Every class structurally satisfying the interface, capped    |
| `super.run()`         | The base declaration the checker resolves to                 |
| `new Thing()`         | The constructor, when it has a body                          |
| `list.map(callback)`  | The callback, as its own frame — `map` itself is external    |
| `target[key]()`       | Nothing. Recorded as unfollowable rather than guessed        |

Four consequences worth holding on to:

- **Structural matching is not optional**, because classes routinely satisfy an
  interface without writing `implements`. It also means a caller list can
  contain a class that never actually calls the callable at runtime — that cap
  is a fixed constant in `@callidescope/graph` rather than a configured limit,
  so a result that looks implausibly wide is a fan-out to inspect rather than a
  number to raise.
- **A computed member call resolves to nothing.** A caller reaching the
  callable that way will not appear, so `breadth` does not fully cover a rename
  in a codebase that dispatches through computed names.
- **Calls into _installed_ dependencies are leaves.** Whether
  `Array.prototype.map` is deeply implemented says nothing about whether _your_
  layering is too deep, and counting it would move every number on an unrelated
  upgrade. A call into another project of the same workspace is not one of
  these — it resolves to a real frame, however the run was scoped.
- **`excludeCallees` globs are dropped from the graph entirely**, so a callable
  the configuration excludes — typically a logger — appears in no list and
  counts toward nobody's depth or breadth.

**Cycles are collapsed before depth is measured**, so a mutually recursive
cluster of three contributes three frames once — an honest floor on a stack
that has no ceiling. That is why the numbers do not move between runs:
detecting a repeat visit mid-walk would make the answer depend on which path
arrived first, and a linter whose numbers move on its own is not usable as a
gate.

**Depth is only meaningful relative to a root**, and most code in a framework
codebase is called by the framework rather than by the repository. Roots are
therefore configurable — decorated methods, lifecycle hooks, bootstraps, index
exports — and anything left with no caller is promoted to an orphan root rather
than dropped.

## After reading

To narrow, gate, or publish a run, and to change any of the thresholds above,
reach for the `callidescope-configure` skill. When a run fails or a report
reads stale, reach for `callidescope-triage`.

A refactor moves the call graph, which makes every committed report stale.
Re-run the write configuration once the change lands, and lint **before**
regenerating: every frame carries a `file:line`, so a formatter that sorts
class members moves the line numbers of everything after it, and a report
written before that sort is stale the moment it lands.

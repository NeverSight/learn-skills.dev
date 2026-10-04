---
name: callidescope-configure
description: Tell callidescope what to do — the command-line flags (--check, --write, --addresses, --config, --format, and an override for every configured field, from --directories and --exclude through --include-tests, --maximum-depth, --maximum-breadth, --json, --markdown, and --mermaid) and the callidescope.config.ts they layer over, covering the two depth and breadth limits, entry points, exclusions and excluded callees, and where a run writes its JSON, markdown, and mermaid reports. Use when wiring a depth gate into CI or a commit hook, when a whole-workspace run is slow, when choosing between --check and --write, when a repository has no callidescope configuration yet, when a traced project has no callidescope.config.ts of its own or one that leaves a field out, when a project needs its own depth or breadth limit, when a package low in the graph measures nothing, when a trace judges code it should not, when everything is reported as an orphan root, or when deciding where a committed report should live.
license: MIT
---

# Telling callidescope what to do

Two surfaces, read together on every run: the flags on the command line, and
the `callidescope.config.ts` they layer over. Neither is complete on its own:
`--check` names a limit the configuration has to have set, and a file
destination is only written when a flag asks for it.

## The two decisions a run makes

Every invocation answers two independent questions, neither implying the other:

| Question                    | Answered by                                           |
| --------------------------- | ----------------------------------------------------- |
| What does this run fail on? | `--check`, a comma-separated set                      |
| What does this run rewrite? | `--write`, plus the destinations in the configuration |

A run given neither `--write` nor `--check reports` **reads no destination and
rewrites none**: it traces, prints, and exits. That is what makes a bare run
safe to type inside somebody's checkout, and why a gate on a pull request
leaves every committed report exactly as it found it.

## The flags

| Flag                                                                                                                          | Meaning                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-a, --addresses`                                                                                                             | Comma-separated callable addresses, each `<file>#<qualified-name>`. `depth` and `breadth` only. Prompted for when omitted                                                               |
| `--config`                                                                                                                    | Path to a `callidescope.config.ts`. Searched for when omitted                                                                                                                           |
| `-d, --directories`                                                                                                           | Comma-separated project directories to trace, each holding its own `tsconfig.json`                                                                                                      |
| `--entry-point-addresses`, `--entry-point-decorators`, `--include-exported-functions`, `--include-orphans`, `--include-tests` | Override the matching `entryPoints` field. The two lists are comma-separated; the three switches take `true` or `false`, or the bare flag for `true`                                    |
| `--exclude`, `--exclude-callees`                                                                                              | Comma-separated globs and callee patterns, overriding the **authored** field. The tool's own default exclusions are folded back in, exactly as they are under a configured `exclude`    |
| `-f, --format`                                                                                                                | `markdown`, `mermaid`, or `json`, for what it prints. Markdown by default. Anything else is refused rather than rewritten. Command-line only — no configuration field corresponds to it |
| `--json`, `-m, --markdown`, `--mermaid`                                                                                       | Where each report goes. Overrides the path of that declared `write` destination, and nothing else about it. Needs `--write` or `--check reports`                                        |
| `--maximum-depth`, `--maximum-breadth`                                                                                        | A number, overriding that limit wherever a project declared it. `--maximum-breadth` is refused against a configuration declaring none, breadth having no default to override            |
| `--check`, `--write`                                                                                                          | The two decisions above: fail on a comma-separated set drawn from `breadth`, `depth`, and `reports`; write every configured destination                                                 |

**Every configured field has an overriding flag, save one.** `excludeFrom`
names the ignore files a run _reads_ — no flag corresponds to it. An override
may change a declared value and may not supply one, so no flag makes an
under-configured run legal, and a list written empty reads as absent. `depth`
and `breadth` take every override above but the destinations and the limits,
plus `--config` and `--format`; `--addresses` is theirs alone.

### One precedence rule governs every override

Every combination of a command-line value with a configured one is resolved in
one place, `FlagResolutionService`, under one rule:

> A flag that changes **what a run judges or writes** may only override a value
> the configuration already declares. A flag that selects **mode or
> presentation** is command-line only, because neither can make an
> under-configured run legal.

`--check`, `--write`, and `--format` are mode or presentation and are never
written into the configuration. `--config` is neither: it chooses the file
everything else is resolved against, so it has already done its whole job by
the time the rest of resolution runs. Every other flag is an override, and an
override answers a question the configuration already asked: a path flag
replaces only the `path` of a destination already declared, keeping its
heading, description, anchors, and hooks; `--maximum-breadth` cannot conjure a
limit a project's own file left unset, the same way `--json` cannot conjure a
`write.json` the workspace file never declared. A limit override reaches the
number each project is really gated by — applied to every project that
declared the limit being overridden, and to no project that declared none,
because overriding a decision and reversing one are not the same act.

Every complaint from resolution is collected rather than thrown at the first
one, so a command line with two mistakes is two mistakes to fix, not two runs.

### `--check` takes a set, and the set matters

| Value     | What fails the run                                                      |
| --------- | ----------------------------------------------------------------------- |
| `depth`   | A call stack deeper than `limits.maximumDepth`                          |
| `breadth` | A callable calling more callables directly than `limits.maximumBreadth` |
| `reports` | A configured destination no longer holding what a fresh run would write |

Two refusals to expect, both deliberate:

- **`--check` with no value is refused.** A set with nothing in it is
  indistinguishable from the flag left off, so `--check "$GATES"` with the
  variable unset would pass forever over a stack twice as deep as anything
  allowed — worse than no gate, because it looks like protection.
- **An unrecognized value is refused**, and the message lists what is accepted.

### Why `depth` and `reports` belong on opposite sides of a pull request

**Depth is the gate.** A stack got longer in this change, and this change is
what fixes it. Run it on every pull request, and on every commit if you like —
depth reads source and needs no build, which is what keeps it cheap enough for
a commit hook.

```bash
npx callidescope --check depth
```

**In an Nx workspace, prefer the per-project `gate` target to this flag.** A
whole-workspace `--check depth` reaches the right verdict the expensive way:
one uncacheable run over the repository on every commit. `@callidescope/nx`
infers a `gate` onto each project instead, tracing it with its Nx dependencies
and failing only on the findings **that project owns**, so `nx affected
--target=gate` judges what a change touched and nothing else. Depth is gated
on every project, since it has a default; breadth is gated only on a project
whose own `callidescope.config.ts` declares `limits.maximumBreadth`. The flag
remains the answer without Nx.

**Staleness is not a gate.** A report goes stale whenever the call graph moves
anywhere, which is nearly every change, so gating on it fails pull requests for
drift they did not cause. Publish on the default branch instead, where nothing
else competes to rewrite the same block:

```bash
npx callidescope --write
```

`--write --check reports` is **refused outright**: a report cannot be stale in
the run that just wrote it, so it would pass whatever it was meant to catch.
Name the gate directly alongside whatever else gates a pull request, not off a
lint-style aggregate that might one day forward `--configuration=write` from a
branch.

### `--directories`, and why a run is slow without it

The difference between a whole-workspace analysis and a check that finishes in
seconds. Each directory named needs its own `tsconfig.json`, and the programs
built are those plus every project they transitively import, so a call into a
dependency still resolves to a real frame:

```bash
npx callidescope -d packages/foo,packages/bar --check depth
```

Omit it and callidescope walks the working directory for every `tsconfig.json`
it finds — the workspace-wide picture, not an answer about one package.

It takes **paths**, not project names: callidescope knows nothing of workspace
tooling, and a directory holding a `tsconfig.json` is the whole contract. The
same list can be set once as `directories` in the workspace configuration file.

There is a real trade-off when narrowing a `breadth` lookup: **callers outside
the named directories and the closure below them do not exist to the run**,
since the closure runs downward and a dependent that calls in is never built.
For a rename whose blast radius is the point, trace wide enough to contain
every consumer.

An Nx workspace can hand the selecting to Nx instead, through the separate
`@callidescope/nx` plugin, which infers `trace`, `depth`, `breadth`, and `gate`
targets onto every project and traces each one _with its Nx dependencies_, so
those are projects the run is scoped to rather than ones it merely reached
through a closure. The first three only print; `gate` decides an exit code and
is what a branch runs. An excluded project keeps the three that print and is
denied the gate, since its own code is never traced. It is a separate package
on purpose: this CLI depends on nothing Nx-shaped.

### `--format` decides what prints, not what is written

Printing and writing are independent, and both can be on at once. `--format`
names one of `markdown` (the default), `mermaid`, or `json` for standard
output; the destinations declared under a project's or the workspace's own
`write` decide what reaches a file. `markdown` leads because it is the one
rendering that reads in a terminal, pastes into an issue, and is already what
the files hold. There is no `write.format` field — the console rendering is a
command-line concern only.

### Prompting, and why it will not hang a script

`callidescope`, `depth`, and `breadth` all prompt for a value left off the
command line — `depth` and `breadth` for a missing `--addresses`, all three for
a missing `--format`. There is no flag to turn that off, because **an attached
terminal is the whole condition**: a script, a hook, or a CI job never has one
and so is never prompted. A missing `--addresses` is then **refused**, exit
non-zero, since nothing else can supply it; a missing `--format` falls back to
its default, `markdown`, and the run proceeds.

The refusal is the load-bearing half. `prompts` does not fail on a non-terminal
stdin — it draws its menu, never resolves, and lets the process **exit 0 having
done nothing** — so a required value asserts a terminal before prompting at all
and reports a rejected command line instead. Without it, a CI run that forgot
an argument would read as a green one.

## The workspace configuration file

Any of `callidescope.config.{ts,mts,cts,js,mjs,cjs,json,jsonc}`, searched for
upward from the working directory, TypeScript first because that is the form
that gets type checking. This is the **workspace** configuration — the file a
run is pointed at. A repository with none is traced with defaults rather than
told to write one.

```ts
import { type CallidescopeConfiguration } from "@callidescope/configuration";

const callidescopeConfiguration: CallidescopeConfiguration = {
  excludeFrom: ["configuration/.callidescopeignore"],
  limits: { maximumDepth: 6 },
};

export default callidescopeConfiguration;
```

The whole surface is seven top-level keys: `directories`, `entryPoints`,
`exclude`, `excludeCallees`, `excludeFrom`, `limits`, and `write`. The
workspace file also exports `projectDefaults` alongside its default export —
a separate binding, not a member of this type — for a project's own
`callidescope.config.ts` to spread.

### `limits`

There are two, both per project, both gated.

| Limit            | Default  | Meaning                                             |
| ---------------- | -------- | --------------------------------------------------- |
| `maximumDepth`   | `6`      | Frames a call stack may hold, entry point inclusive |
| `maximumBreadth` | **none** | Callables one callable may call directly            |

**`maximumBreadth` has no default, on purpose.** Until something picks a
number, breadth is reported without being gated, and `--check breadth` is
refused rather than falling back to an unbounded limit that looks exactly like
passing. It also takes a **project's own** number, never a workspace one alone
— see [What a project may set](#what-a-project-may-set).

Picking a first `maximumDepth`: run once with no gate, read the deepest stacks,
and set the limit at the shape you want rather than at whatever the code
currently is — a limit set to today's worst number gates nothing.

**Per project, pick each one by boundary-testing rather than by reading a
number off a run.** Write a candidate, run that project's gate, then run it one
lower: a limit worth having passes at the number written and fails at one
below. A scoped run's printed summary covers the whole trace, dependency
closure included, so the depth it reports is routinely deeper than anything
the judged project owns — only a gate's verdict knows which findings belong to
the project.

**A limit is a schema field and nothing else now.** The schema is strict, and
`limits` accepts only `maximumDepth` and `maximumBreadth`. A retired field —
`spreadThreshold`, `directSpreadThreshold`, `minimumCallers`,
`callerMajorityRatio` — is refused rather than silently stripped. Those four
limits, the two findings they tuned, and the module-identity concept behind
them are gone from the tool entirely — see the repository's ADR 0006, "Narrow
callidescope to depth and breadth".

**The implementation-candidate cap is a constant, not a configuration field.**
It decides where structural interface resolution stops guessing, which is a
property of the resolution rather than a number any run judges by, so it lives
in `@callidescope/graph` and is not written anywhere in `callidescope.config.ts`.

### `entryPoints`

| Option                     | Default                 | Meaning                                                           |
| -------------------------- | ----------------------- | ----------------------------------------------------------------- |
| `addresses`                | none                    | Callables named outright as roots, each `<file>#<qualified-name>` |
| `decorators`               | 13 framework decorators | Decorators whose methods a framework invokes                      |
| `includeExportedFunctions` | `true`                  | Treat every `src/index.ts` export as a root                       |
| `includeOrphans`           | `true`                  | Promote callables nothing in the repository calls                 |
| `includeTests`             | `false`                 | Trace test files too                                              |

**`addresses` is how a package states the surface it means to be measured on**,
in the same `<file>#<qualified-name>` form `depth` and `breadth` accept and
every frame prints, so an address is copied out of a report straight into the
configuration — with a trailing `:<line>` when one file declares the name
twice:

```ts
entryPoints: {
  addresses: ["packages/foo/src/modules/read/read.service.ts#ReadService.read"],
},
```

Declared addresses **add** roots and take none away: the rules below still run
first, orphan promotion still catches whatever nobody named, and an
already-rooted callable stays one root.

Reach for it when a package sits low in the graph: a stack is filed under the
project owning its **root**, and most of what such a package publishes is
called from above, so it roots nothing and any limit on it gates nothing.
**An address resolving to nothing, to several declarations, or to nothing
parseable fails the whole run** — `callidescope-triage` carries each message
and its fix.

`decorators` **replaces** the built-in list rather than adding to it, so a
configuration naming its own framework's decorator should restate the ones it
still wants — a report where nearly everything is an orphan root usually means
the decorators in use are missing from it.

**`includeOrphans` is a safety net rather than a feature.** Without it, a
missing entry-point rule silently removes whole subtrees from every
measurement; with it they surface as orphan roots — either dead code, or a
rule that needs adding.

### Keeping code out of a run

Two tools, for two different questions:

- **`exclude`** takes globs and is **additive** to the built-in defaults
  (`node_modules`, `dist`, `coverage`, `output`, `.nx`, `.conformetry`), so a
  configuration naming its own noise does not restate them.
- **`excludeFrom`** names gitignore-syntax files, workspace-only. This is how a
  long exclusion list stays out of the configuration file itself, and it is the
  right home for fixture packages written to be deliberately bad.
- **`excludeCallees`** takes globs matched against a callable's display name
  (`Type.member`) and drops matching calls from the graph entirely, counting
  toward neither depth nor breadth. This is for cross-cutting instrumentation:
  a call to a logger is a fact about instrumentation rather than about the
  shape of the code around it, and counting it would move every other
  callable's numbers on a change that has nothing to do with them.

`exclude` and `excludeFrom` drop _files_ from collection; `excludeCallees`
drops _edges_, and reaching for the first when you meant the second deletes
real findings. Neither leaves the `ts.Program`: an excluded file is still
compiled, a call into it becomes unfollowable rather than vanishing, and no
`exclude` can un-project a directory holding a `tsconfig.json`. A project's own
`exclude` behaves the same way.

### `directories`

The same list `--directories` takes, set once, workspace-only.

### `write`

Every destination is optional, and unconfigured is the normal case: a run
naming no destination reports to the console and exits non-zero on violations,
so nothing it writes can go stale.

| Key              | Purpose                                                                        |
| ---------------- | ------------------------------------------------------------------------------ |
| `write.json`     | A machine-readable report at `path`, indented by `indentation`. Workspace-only |
| `write.markdown` | A marker-delimited block spliced into `path`                                   |
| `write.mermaid`  | The same block with the stacks drawn as one flowchart                          |

`write.mermaid` takes the same keys as `write.markdown` — they differ in what
goes between the markers, not in how a block is placed — and is separate so one
run publishes both: the tree says what each frame takes, returns, and documents,
the diagram what shape they make together.

```ts
write: {
  json: { indentation: 2, path: "output/callidescope.json" },
  markdown: { path: "docs/call-stacks.md" },
  mermaid: { path: "docs/call-stacks-diagram.md" },
},
```

Both take a `description`, placed under the heading, a `heading` (defaults to
`# 🔭 Callidescope`, and should be set when the block is spliced into a file
that already has a title, since most markdown linters reject a second
first-level heading), and `previewCount` — how many stacks are shown before the
rest go behind a disclosure, three by default. `previewCount` belongs to the
destination rather than to the run because it is a fact about the document the
block lands in: a project's own README wants three and a whole-workspace
report file wants all of them. A whole-run block opens with the summary
counts, one row per project against **its own** depth limit, and a scoreboard
of how many sit over, on, or clear of theirs; the findings tables follow.

**There is no fan-out that writes a section into every project's readme.**
Each project declares its own `write.markdown` (and `write.mermaid`, if it
wants a diagram) in its own `callidescope.config.ts` — see
[What a project may set](#what-a-project-may-set). The workspace's own
`write.markdown` is the block that really is about the workspace: the summary
counts, one row per project against its own depth limit, and the scoreboard.

A markdown destination may also supply `render`, to replace the built-in
tables, or `writeBlock`, to place the block itself — handed `syncAnchoredBlock`
and `wrapInAnchors`, so it reuses the same splice. **Returning `false` reports
the destination as stale**; anything else, `undefined` included, counts as
current.

## Every traced project's own configuration is required and complete

A second `callidescope.config.ts` sits at each traced project's own root, the
directory holding the `tsconfig.json` that makes it a project, found by name in
that directory alone with no upward walk, in any of the same eight extensions.

**Every traced project has one, and every one of them is complete.** A traced
project with no configuration file at all is refused by name, and so is a file
that leaves a field out. Completeness is deliberate: an absent field and a
field set to the value it would have defaulted to look identical in a diff,
and only one of them was a decision — `maximumBreadth` absent and
`maximumBreadth: undefined` used to mean "somebody forgot" and "this project
gates depth and not breadth" respectively, and per-field fallback could not
tell them apart. See the repository's ADR 0007, "Require a complete
configuration from every traced project".

The file a run was pointed at is never also read as a project's — one file, one
role per run. A package whose task names its own configuration and then traces
itself would otherwise have it refused for the workspace-only fields it
legitimately sets, so a package needing both keeps two files under two names.

### What a project may set

| Field                   | What it does                                                         |
| ----------------------- | -------------------------------------------------------------------- |
| `entryPoints`           | Which of that project's callables root a stack, `addresses` included |
| `limits.maximumDepth`   | The depth every stack rooted in that project is judged against       |
| `limits.maximumBreadth` | The breadth every callable that project declares is judged against   |
| `exclude`               | Globs naming that project's own files to leave untraced              |
| `write.markdown`        | Where that project's own published section goes                      |
| `write.mermaid`         | Where that project's own diagram goes, when it wants one             |

**A project's own destinations and `exclude` globs are anchored to that
project's root**, never to the workspace: `exclude: ["src/generated/**"]` in
`packages/thing`'s own file names `packages/thing/src/generated/**`, and
`write: { markdown: { path: "docs/CALLS.md" } }` there writes
`packages/thing/docs/CALLS.md`. No spelling of either reaches a sibling. A
destination left `undefined` publishes nothing for that project.

The run's own `exclude` stays workspace-relative and is layered underneath, so
a project can leave more out and never put back what the run left out. Noise
spanning several projects still belongs in the workspace file.

`write.json` stays workspace-only: it is the run's single report, not a
project's to redirect.

Every other field is refused **by name, before anything is traced**, and the
message names the six above so it is actionable without opening this skill.

### Spread the defaults, then override

The workspace configuration exports `projectDefaults` beside its default
export. A project spreads it and overrides what it means to, which is what
makes a complete file cost one line:

```ts
import { projectDefaults } from "../../configuration/callidescope.config.js";

export default {
  ...projectDefaults,
  limits: { maximumBreadth: undefined, maximumDepth: 10 },
};
```

Both limits are named even though only one is a real number. `maximumBreadth:
undefined` is this project saying outright that it gates depth and not breadth
— the one statement an absent field could never distinguish from a project that
forgot. The same holds for `write.mermaid: undefined` and publishing no
diagram.

**Spread `projectDefaults`, never the workspace's default export.** The two are
different objects on purpose: the default export carries `directories`,
`excludeFrom`, `write.json`, and the rest of what only the workspace may set,
so spreading it earns a refusal naming the first such field. `projectDefaults`
holds exactly the surface a project is entitled to, so spreading it cannot
adopt an output destination or an ignore file by accident.

**Nothing is resolved across two files, and there is no longer a record of
where a number came from.** Every number a project is judged by is written in
that project's own file — there is no per-field fallback to the workspace once
a project's file exists, and no `declared` versus `inherited` distinction left
to draw, because the spread already put the number here where a reader can see
it. Documentation that still talks about a limit being "inherited", or a
project readme carrying an "Origin" column, describes the tool before this
requirement — see the `callidescope-triage` skill for the refusal this
replaced.

The workspace number `projectDefaults` carries is a **default rather than a
ceiling**: a project spreading it and then overriding to a higher limit keeps
its own, because a workspace number pinned by the single worst stack anywhere
gates nothing for the projects nowhere near it.

`entryPoints` is replaced whole rather than merged member by member: writing an
`entryPoints` object of its own replaces the spread one outright for that
project's callables, so a project that wants the workspace's decorator list
alongside its own `addresses` has to carry the decorator list across
explicitly, via `...projectDefaults.entryPoints`.

**Why the other fields cannot vary per project.** `maximumDepth` and
`maximumBreadth` **judge** a call graph built once, so two projects asking
different questions of the same edges is coherent. `excludeCallees`,
`directories`, `excludeFrom`, and `write.json` are different: they name what a
run reads, where its own report lands, or how it partitions the workspace, and
a project cannot answer those differently from the run tracing it.

### Reading the whole set back

A ratchet written one file per project is no longer reviewable in the single
file it used to live in. The `limits` command is where it is reviewable as a
set instead:

```bash
npx callidescope limits
```

A markdown table, one row per project per limit — `Project`, `Limit`, `Value`,
`Declared in` — naming the file each number is written in. `none` means
nothing anywhere declares that limit, the usual case for breadth. The
`workspace` row comes first and is the only one that may carry no file: it is
the default every project's own file spreads, not a number any file wrote down
for itself. It resolves configuration and measures nothing, so it costs
milliseconds rather than a trace.

## After changing any of this

A configuration change usually moves the numbers, making every committed report
stale. Re-run the write configuration in the same change, and lint **before**
regenerating: every frame carries a `file:line`, so a formatter that sorts class
members moves the line numbers after it, and a report written before that sort
is stale the moment it lands.

When a run is refused or a report reads stale, reach for `callidescope-triage`.
To read what a run printed, reach for `callidescope-trace`.

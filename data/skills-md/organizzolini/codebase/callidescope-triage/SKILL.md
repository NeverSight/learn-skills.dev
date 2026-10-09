---
name: callidescope-triage
description: Act on a callidescope run that failed — a per-project gate reporting a stack over that project's limit, a breadth gate, a gate that read none of its project's own files, a stale committed report, an unreadable tsconfig, a run that traced nothing, or a rejected command line or configuration. Use when callidescope or an inferred gate target exits non-zero, when a stack got deeper in a change, when deciding whether a failing gate is a code fix or a limit fix, when picking or moving a project's own maximumDepth or maximumBreadth, when a printed maximumDepth disagrees with the number a gate judged, when a committed report disagrees with a fresh run, when a declared entry-point address resolves to nothing or to several, when a traced project has no callidescope.config.ts of its own or one that leaves a field out, or before reaching for maximumDepth to make a failing check pass.
license: MIT
---

# Acting on a callidescope failure

Callidescope fails for a handful of distinct reasons, and reading which one
occurred is most of the work. Separate them first:

| The run said                              | It is                                                                                                                                           |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `🚨 [DEPTH n > limit]`                    | A **finding** about the code. Fix the layering                                                                                                  |
| A breadth row over the limit              | A **finding**. Split the callable                                                                                                               |
| `A configured destination is stale`       | **Drift**. Re-run `--write`                                                                                                                     |
| `## Read nothing of its own (0 files)`    | A gate **judged a project whose own files it never read**. Its verdict means nothing                                                            |
| `🔭 Rejected a project it could not read` | A `tsconfig.json` **is missing or did not parse**. The trace stopped there                                                                      |
| `🔭 Traced nothing`                       | The run **saw no code at all**. Nothing below it means anything                                                                                 |
| `🔭 Rejected the command line`            | A **mistake** in the flags. Nothing was traced                                                                                                  |
| `🔭 Rejected a project configuration`     | One project's own `callidescope.config.ts` **was missing, incomplete, or refused** for a field only the workspace may set. Nothing was reported |

The bottom five all mean the run never produced a verdict on the code. None of
them writes a destination, so a checkout is unchanged by any of them — and no
finding, or absence of one, should be believed from a run that printed one.

The `limits` command prints its own read failures under the same
`🔭 Rejected a project configuration` headline, fixed the same way — see
[A refused project configuration](#a-refused-project-configuration).

## A depth gate that failed

A stack ran deeper than `limits.maximumDepth`. **The change that made it longer
is the change that fixes it** — that is the whole reason depth is the gate and
staleness is not.

**A failed gate is about one project.** Limits are written per project, in
that project's own `callidescope.config.ts`, and a project's gate judges only
the findings that project owns — a stack is charged to the project owning its
**root**, and a dependency's breach belongs to that dependency's own gate. So
there are exactly two places the fix can go: that project's code, or that
project's own `callidescope.config.ts`. Read the second option with the whole
of the section below in mind before taking it.

In an Nx workspace this arrives as a failing `gate` target rather than as a
whole-workspace `--check depth`, and the task name says which project to open.
Elsewhere, the finding's own `limit` says which number it was weighed against,
and `callidescope limits` says which file that number is written in.

Read the printed stack before doing anything. The frames carry each callable's
signature and the one-line summary of its documentation, and those summaries
are how you tell the two cases apart:

- **Every frame says something different.** The layering is real: each stage
  does its own work. Question whether all the stages are needed, but do not
  start deleting one layer at a time — this case usually needs a design
  decision, not a trim.
- **A run of frames all say roughly the same thing.** Those are forwarding
  layers that exist only to pass arguments along. **Collapse them.** This is
  the common case and it is exactly what the tool was built to surface: the
  tools that would otherwise tell you are the ones reading a file at a time, so
  they see the forwarding and never the depth.

**Raising `maximumDepth` is not a fix.** The limit describes the shape the
repository wants; moving it to fit today's worst stack means the gate stops
gating, and every later stack gets a free pass to that new number. If the limit
is genuinely wrong for the project, change it as its own decision, on its own,
with the reasoning written down — not as the thing that unblocks a pull request.
Raising a **project's** number is the smaller version of the same mistake, not
an exemption from it: it is exactly the one number that was boundary-tested to
sit one frame above what that project measured, so raising it by one converts a
gate into headroom for the one project the finding is about.

### The summary's depth is not the project's depth

The number to take is the one a **verdict** gives you, and never the one a
summary line prints. A `🔭 Finished an analysis` log line reports
`maximumDepthTraced`, and the name is literal: it reduces over the whole of a
run's measurement, the entire dependency-widened trace, so it is the deepest
stack anywhere the run reached rather than anywhere it was pointed. The
per-project scoping that decides a gate's verdict is a different code path
entirely.

The two routinely disagree by several frames. `tools/synchronization`'s scoped
run prints `maximumDepthTraced:13`, while its gate passes at the declared 10
and fails at 9 — ten is the number that project owns, and thirteen belongs to a
dependency it was traced alongside.

So do not set a project's limit from that line. **Boundary-test instead**: write
a candidate, run the gate, and let a failure name the real number. A limit worth
having passes at the number written and fails at one below it, and the only
thing that can tell you where that boundary is, is a gate verdict.

### `≥ n` rather than `n`

A depth printed with `≥` is a **floor, not a measurement**. Something on that
path could not be followed — a callback invoked through a parameter, a computed
member name like `target[key]()`, or a structural expansion dropped for
exceeding the implementation-candidate cap — and the run says so rather than
quietly under-reporting.

This is not a defect to fix and not a number to distrust. It means the real
depth is _at least_ that, so a `≥ 10` against a limit of 6 is a genuine
failure. `Unfollowable calls` in the summary counts how many such calls the run
hit.

### A stack headed `orphan-root`

Nothing in the repository calls the root. Either it is dead code, or an
entry-point rule the configuration is missing — most often a framework
decorator absent from `entryPoints.decorators`. Decide which before treating
the depth as real: a stack under a root that a framework actually invokes is a
finding, and one under genuinely dead code is a reason to delete the code.

### `Stacks through recursion` above zero

A cycle, collapsed before depth was measured. A mutually recursive cluster of
three contributes three frames once. The depth is a floor for the same reason
as above, and the collapsing is what keeps the numbers from moving between
runs — do not try to "fix" the recursion because callidescope mentioned it.

## A breadth gate that failed

A callable calls more callables directly than `limits.maximumBreadth`. Unlike
depth, this one has no default limit at all, so a breadth failure only ever
happens in a **project** whose own `callidescope.config.ts` chose a number — a
workspace-level `maximumBreadth` alone gates nothing, since every project must
name its own to be judged by it.

The fix is to **split the callable along the responsibilities its callees
already group into**, not to inline anything. Run the `breadth` command against
the callable's address to see the direct callees and callers side by side
before deciding where the seam goes — the `callidescope-trace` skill covers
reading that.

## A gate that read nothing of its own

```text
## Read nothing of its own (0 files)

This run judged a project whose own code it never read:

- `packages/thing`
```

The run itself was not empty — the dependencies it traced were read — so this is
narrower than `🔭 Traced nothing`: only the judged project's own sources went
missing. A gate fails on it and a `trace` prints it and passes, because a gate
that never looked cannot tell a clean project from an unread one, where a trace
decides nothing and is a report for a reader to open.

Two things to check, in this order:

1. **An `exclude` that over-matched.** The project's own `exclude` globs are
   anchored to its root, so one written workspace-relative matches nothing, and
   one written too broadly matches everything. Check the run's `exclude` and
   `excludeFrom` for a pattern covering the whole project as well.
2. **A project that no longer holds sources its `tsconfig.json` includes.** A
   moved or emptied source root reads exactly the same way.

**Do not silence it by dropping the gate.** A project the workspace
configuration excludes is denied a gate deliberately and never reaches this
message; a project that still has one is expected to have code, and a green
verdict over nothing is the failure this exists to prevent.

## A stale report

One or more configured destinations no longer hold what a fresh run would
write. The run names every file that drifted rather than stopping at the first.

**Re-run `--write`. That is the entire fix.**

```bash
npx callidescope --write
```

Three things a stale report does _not_ mean:

- **It is not a defect.** The call graph moves with the code, so a report goes
  stale whenever anything anywhere moves. That is exactly why `--check reports`
  belongs on the default branch and not on a pull request.
- **It is not something to hand-edit.** The next `--write` replaces the block
  between its markers wholesale, so an edited report is a diff that silently
  disappears on the following run.
- **It is not a reason to add `--check reports` to the pull request gate.**
  Doing that fails pull requests for drift they did not cause.

**Lint before regenerating, never after.** Every frame in every report carries
a `file:line`, and a formatter that sorts class members moves the line numbers
of everything after the one it inserted — so a report written before that sort
is stale the moment it lands.

## A rejected command line

Nothing was traced. The message lists the reasons; these are the ones to expect:

- **`--check` needs a value.** A valueless flag, an empty string, or a
  comma-only value are all the same mistake. A set with nothing in it is
  indistinguishable from the flag having been left off, and reading it as "gate
  nothing" would produce a gate that cannot fail — `--check "$GATES"` with the
  variable unset would pass forever over a stack twice as deep as anything
  allowed, which is worse than no gate because it looks like protection.
- **`--check` does not accept that value.** It takes a comma-separated set
  drawn from `breadth`, `depth`, and `reports`, and the message lists them.
- **`--write` cannot be combined with `--check reports`.** A report cannot be
  stale in the run that just wrote it, so the combination would pass whatever
  it was meant to catch. Run them separately, on the sides of the pull request
  they belong to.
- **A destination flag with no verb.** `--json`, `--markdown`, and `--mermaid`
  say _where_ a report goes; `--write` and `--check reports` say _whether_ one
  is written or compared. Given a destination and neither verb, the run is
  refused rather than obeyed silently. Add the verb the message names.
  `--check reports` counts as one: it compares a destination, so an override is
  meaningful there too.
- **A destination flag overriding a destination nobody declared.** `--json`,
  `--markdown`, and `--mermaid` change where a **declared** report goes; they
  cannot conjure one the configuration never asked for, or a requirement that
  configuration be complete would be circumventable from a terminal. Add the
  `write.json`, `write.markdown`, or `write.mermaid` the message names to the
  configuration this run reads, then point it elsewhere with the flag.
- **`--format` does not accept that value.** It takes `markdown`, `mermaid`, or
  `json`, and the message lists them. An unrecognized value is refused rather
  than rewritten to markdown, which is what it used to do — a run that printed
  a tree for `--format mermiad` exited 0 having taught its reader that the flag
  does nothing.
- **`--maximum-breadth` overriding a limit nobody declared.** It is refused the
  same way a destination flag is: against a configuration declaring no
  `limits.maximumBreadth` anywhere in scope, there is nothing for it to
  override, and supplying one from the command line would gate a workspace on
  a number no configuration ever chose.
- **`depth` or `breadth` with no address.** Those commands take
  `<file>#<qualified-name>`. At a real terminal outside CI they trace first and
  then complete the address against every callable they found, so the name can
  be picked rather than recalled; a name declared twice in one file arrives
  with its `:<line>` already attached. In a script or a CI job prompting is
  off, so a missing argument is a rejection rather than a hang.

## A refused project configuration

A `callidescope.config.ts` sitting at one traced project's own root — or the
absence of one — was refused. Nothing was printed and no destination was
touched, so the checkout is exactly as the run found it. `<project>` is the
workspace-relative project root; an address the workspace file declared is
labelled `the workspace configuration` instead.

**The project has no configuration file at all.**

Every traced project's own `callidescope.config.ts` is required, not optional.
A project with none is refused by name before anything is traced. The fix is
to add one, spreading the workspace's `projectDefaults` export and overriding
what it means to:

```ts
import { projectDefaults } from "../../configuration/callidescope.config.js";

export default { ...projectDefaults };
```

That import path is illustrative rather than literal — write it relative to the
project's own location. A file that overrides nothing is still a complete
statement: it says outright that this project takes every default, which an
absent file could never say.

**The file could not be read, or leaves a required field out.**

```text
Failed to read the callidescope configuration for <project> at <path>: <reason>
```

The read failed, or the object did not pass the schema. `<reason>` is the
underlying failure and is kept as the error's `cause`. A schema complaint names
the field: a missing `entryPoints`, `exclude`, `limits`, or `write` member, a
limit that is not a positive integer, an `addresses` entry that is not a
string. **Every field is required now** — `entryPoints` with all five members,
`limits` with both, `write` with both, `exclude` — so a file that leaves one
out is refused the same way a file with no configuration at all is, and
spreading `projectDefaults` before overriding is what keeps that file from
having to spell out every field itself.

**A field only the workspace may set.**

```text
<project> sets <field>, which only the workspace configuration may set. A project configuration may set entryPoints, exclude, limits, write.markdown, and write.mermaid.
```

Move that field to the workspace file. `<field>` prints as `limits.<name>` for a
limit, `write.<name>` for a destination, and as a bare name for any other
top-level field, so the message says which of the three is wrong.

Two ways to arrive here, and the fix differs:

- **A spread of the workspace's default export into the project's own file.**
  Delete it and spread `projectDefaults` instead. The default export carries
  `directories`, `excludeFrom`, `write.json`, and the rest of what only the
  workspace may set; `projectDefaults` holds exactly the surface a project is
  entitled to, so spreading it cannot adopt one of those fields by accident.
- **A genuinely workspace-level field** — `directories`, `excludeFrom`,
  `excludeCallees`, or `write.json`. It belongs in the workspace file and there
  is no per-project form of it: each names what a run reads, where the run's
  own report lands, or how it partitions the workspace, which a project cannot
  answer differently from the run tracing it.

**A declared address resolved to nothing.**

```text
<project> declares an entryPoints.addresses entry that resolves to nothing: "<address>". Check the file path and the qualified name callidescope prints for it in a stack.
```

The callable was renamed, moved, or excluded from this run. Correct the address
or delete it. **Do not silence it**: this refusal exists because a rename that
silently dropped a declared root would lower that project's measured depth with
nothing in the output to say so, loosening a gate in the one commit nobody would
think to check it in. If the address is right but the callable is outside what
this run traced, the scope is the problem, not the address.

**A declared address was ambiguous.**

```text
<project> declares an entryPoints.addresses entry that matches more than one declaration: "<address>". Candidates: <address>:<line>, <address>:<line>. Add ":<line>" to the address to pick one.
```

Every candidate is rendered as an address that would have picked it, so copy one
into the configuration. Two declarations on **one line** cannot be told apart
that way; those name their column instead and the advice changes to
`Two declarations on one line cannot be told apart by ":<line>" — rename one, or
name a different callable.`

**A declared address was malformed.**

```text
<project> declares an invalid entryPoints.addresses entry. "<address>" is not a callable address. It needs a file path and a qualified name joined by "#", as in "src/foo.service.ts#FooService.bar", optionally followed by ":<line>" to disambiguate.
```

Usually a bare file path, a bare qualified name, or a path separator where the
`#` should be. The path is workspace-relative.

A run collects **every** unresolved address before it refuses, so fix them as a
set: more than one arrives numbered, behind
`<count> declared entry points did not resolve.` The `depth` and `breadth`
commands report the same three problems about an address typed at a prompt,
worded for that context and rendered by the same code.

### A project configuration that is refused by nothing and does nothing

A misspelled key is not a refusal — the schema names every field it accepts, so
`limits: { maxDepth: 10 }` alongside a correctly-spelled `maximumDepth` fails
for the unrecognized key rather than silently keeping the typo around. If a
project's limit still seems not to have taken effect after the schema passed,
ask what it actually resolved to rather than re-reading the file:

```bash
npx callidescope limits
```

The row for that project says the number and the file it came from.

**A project's `exclude` goes quiet for a different reason.** Its globs are
anchored to that project's own root, so a workspace-relative one —
`packages/thing/src/generated/**` written in `packages/thing`'s own file —
matches nothing and those files stay traced. Drop the project root from the
front of it: `src/generated/**`. A glob that would reach into another project
cannot be written here at all, and noise spanning several projects belongs in
the run's own `exclude` instead.

## A project it could not read

One project's `tsconfig.json` is missing or did not parse, and the run stopped
there. The message carries the path and either the compiler's own diagnostic
or that the directory holds no `tsconfig.json` at all. `depth` and `breadth`
raise this too, under the same headline: a lookup traces before it matches, so
it can reach the same unreadable project a whole-workspace trace always
could.

Nothing was printed and no destination was written, which is the point of
stopping rather than stepping over it: a caller writes its report before it
weighs its findings, so a partial graph would publish depths measured through a
workspace missing a project and only then fail. Stopping means there is nothing
to un-commit.

Two ways out, and which one is right depends on why the file does not parse:

- **The configuration is broken by accident.** Fix it. The message carries the
  compiler's own diagnostic, which usually names the option.
- **The configuration is broken on purpose.** Some repositories commit a
  broken `tsconfig.json` as a fixture — this workspace has one in
  `codependix-examples`, and repairing it would delete the only place that
  failure is demonstrated. Exclude the project instead, by adding its directory
  to an `excludeFrom` ignore file or an `exclude` glob. Exclusions are applied
  to the `tsconfig.json` before it is opened, so this really does keep the run
  away from it. Excluding the project's _files_ does not: opening its
  configuration is the step that fails, and that happens first.

## A run that traced nothing

Every gate above passed for having nothing to judge, so the run fails on its
own emptiness. It is never a clean result. Work down this list:

1. **Is the code excluded?** `exclude` globs are additive to the built-in
   defaults, and `excludeFrom` files are easy to forget. An exclusion broad
   enough to cover every project empties the run.
2. **Is `--directories` pointed where you think?** It takes paths holding their
   own `tsconfig.json`, not project names.

## A run that found no stacks

Not a failure. A run that traced real code and reported no findings is the
normal outcome: the summary carries the callable, file, and edge counts that
say it looked, and a repository under its limits has no stacks to name.

## Whose problem a finding is

A depth or breadth row is a statement about the code, not about the
configuration that measured it. The fix belongs in the code. Turn to the
configuration only when the measurement itself is wrong — an entry-point rule
missing, a cross-cutting logger inflating everything's numbers — and the
`callidescope-configure` skill covers each of those.

<!-- A deliberate misspelling: the example of a `--format` value nobody
recognizes, which is exactly what this refusal is about.
cspell:ignore mermiad -->

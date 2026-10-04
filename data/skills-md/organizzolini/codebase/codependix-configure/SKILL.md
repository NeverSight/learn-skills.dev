---
name: codependix-configure
description: Write or edit a codependix.config.ts — which graph types run, per-project overrides, include and exclude globs, the whole-workspace graph, where each export lands, and the boundary rules every built graph is judged against. Use when a workspace has no codependix configuration yet, when a run produced no output because everything resolved to target none, when adding a JSON or Markdown destination, when choosing between an anchor block and a standalone file, when a configuration is rejected for a missing destination or an empty selector, when adding a forbid, allow, or acyclic rule, or when deciding whether one configuration can describe every project in a workspace.
license: MIT
---

# Writing a codependix configuration

Codependix produces nothing until a configuration tells it what to export and
where. Every field is optional, and a workspace with no configuration file
resolves every graph type for every project to `target: "none"` — a successful
run that writes nothing. The configuration is the whole control surface; there
is no flag that selects a graph type.

```ts
import { type CodependixConfiguration } from "@codependix/configuration";

const codependixConfiguration: CodependixConfiguration = {
  defaults: {
    imports: { markdown: { anchor: "codependix-file-imports" }, target: "markdown" },
    nestjs: { markdown: { anchor: "codependix-nestjs-modules" }, target: "markdown" },
    nx: { markdown: { anchor: "codependix-nx-projects" }, target: "markdown" },
  },
  exclude: ["fixtures/**"],
  include: ["**"],
  projects: {
    widgets: {
      nx: {
        json: { path: "output/nx-graph.json" },
        markdown: { anchor: "codependix-nx-projects", path: "docs/architecture.md" },
        target: "both",
      },
    },
  },
  workspace: {
    nx: { markdown: { anchor: "codependix-workspace" }, target: "markdown" },
  },
};

export default codependixConfiguration;
```

## Where the file is found

`codependix.config.{ts,mts,cts,js,mjs,cjs,json}` is searched for **upward**
from the run's directory, and the first file found wins outright — nothing from
a further ancestor is merged into it. A workspace carrying both a TypeScript
and a JSON file gets the TypeScript one.

Two paths behave differently on purpose:

- **A path given with `--config` must exist.** A typo fails the run rather than
  quietly resolving every graph to `"none"`. It is resolved against the working
  directory first, then against the workspace root, so a configuration kept in
  a `configuration/` folder can be named relative to either.
- **An absent configuration is legal.** A workspace that never wrote one is not
  told to; it simply exports nothing.

## `defaults`, never `default`

The field that applies to every project naming no override of its own is
spelled **`defaults`**. A configuration module's default export is unwrapped by
name while loading, so a field called `default` would collide with that
unwrapping. A configuration that writes `default:` is not rejected — unknown
keys are stripped rather than refused, so a newer configuration still loads
under an older codependix — it simply has no effect at all, which reads exactly
like a tool that ignored it.

## `target` is explicit

Each graph type's export target is named, never inferred from which
destinations are present:

| `target` | Writes |
| -------- | ------ |
| `"both"` | The JSON and the Markdown destination together |
| `"json"` | The JSON destination only |
| `"markdown"` | The Markdown destination only |
| `"none"` | Nothing — and the default for every unset target |

That explicitness is what lets a project keep a `json` destination it is not
ready to write yet: leave the destination in place and set `target: "markdown"`.

The configuration is validated, and two mismatches are rejected rather than
ignored:

- A `"both"` or `"json"` target with no `json` destination.
- A `"both"` or `"markdown"` target with no `markdown` destination.

## Markdown has two shapes

```ts
// Anchor mode — spliced into a named block inside an existing file.
{ markdown: { anchor: "codependix-nx-projects" }, target: "markdown" }

// Anchor mode, in a file other than the default README.md.
{ markdown: { anchor: "codependix-nx-projects", path: "docs/graphs.md" }, target: "markdown" }

// Standalone mode — the export is the whole contents of the file.
{ markdown: { path: "output/graph.md" }, target: "markdown" }
```

- **Naming an `anchor`** splices the export between two comment markers inside
  the file at `path`, which **defaults to `README.md`** — the common case is a
  project's own readme, so it is worth not repeating.
- **Leaving `anchor` unset** writes the export as the entire contents of a
  standalone file, and `path` is then **required**: there is no default worth
  guessing for a file codependix owns outright.
- A `markdown` destination naming neither is rejected, since nothing would say
  where the export goes.

A missing anchor block is auto-created on `--write`, so anchors do not have to
be placed by hand first. See the `codependix-triage` skill for exactly where a
new block lands and what still fails.

Paths in both destinations resolve relative to the **project's own root**, so
one `defaults` entry describes every project without naming any of them. The
whole-workspace graph resolves relative to the workspace root instead.

## `include` and `exclude`

Both are lists of globs matched against **a project's Nx name and its
workspace-relative root**, so either spelling works:

```ts
{ exclude: ["examples/**", "*-fixtures"], include: ["**"] }
```

`include` defaults to **nothing** and `exclude` to empty, so leaving both out
means no project participates and the run exports nothing. Participation is
always declared: write `include: ["**"]` to cover the whole workspace. A
project is included when at least one `include` glob claims its name or root
and no `exclude` glob claims either.

`--projects` and `--tags` widen this from the command line — a project either
list names participates even when no `include` glob claims it, and `exclude`
still wins over both. See `codependix-export`.

A configuration naming `defaults` but no `include` is the one to watch for.
It exports nothing while still exiting zero, and `--check boundaries` judges
every project regardless of `include`, so the gate stays green. An export run
warns when it happens — `🕸️ Selected no project to export`.

An excluded project resolves to `target: "none"` for every graph type
regardless of what `defaults` or its own `projects` entry says — so excluding a
project takes one line rather than rewriting each of its overrides to `"none"`.

## A project override replaces, it does not merge

When a `projects` entry names a graph type, that entry **replaces** the
`defaults` entry for that graph type outright — it is not merged field by
field. A project turning its Markdown export off by omitting `markdown` should
not have the default's `markdown` destination resurface underneath it.

The practical consequence: an override has to restate every destination it
still wants, including the `target`.

```ts
{
  defaults: { nx: { markdown: { anchor: "codependix-nx-projects" }, target: "markdown" } },
  projects: {
    // Loses the Markdown export entirely — this is the whole nx entry now.
    widgets: { nx: { json: { path: "graph.json" }, target: "json" } },
    // Keeps both, because both are restated.
    gadgets: {
      nx: {
        json: { path: "graph.json" },
        markdown: { anchor: "codependix-nx-projects" },
        target: "both",
      },
    },
  },
}
```

Graph types the override does not mention still fall back to `defaults`; the
replacement is per graph type, not per project.

## The whole-workspace graph

`workspace` is separate from `defaults` and `projects`, and accepts only `nx`:

```ts
{ workspace: { nx: { markdown: { anchor: "codependix-workspace" }, target: "markdown" } } }
```

There is no workspace-wide NestJS or import graph to configure. The workspace
graph is exported once for the repository, carries no per-project override, and
is **unaffected by `include` and `exclude`** — excluding a project from
per-project exports does not remove it from the workspace graph.

`--projects` and `--tags` are the exception, and they reach it through its
**node set** rather than through its destination: a run naming a selection
draws the graph over the projects it named, and writes it wherever
`workspace.nx` says. See `codependix-export` for both flags.

## `projectGraph` — reading a graph rather than resolving one

```ts
{ projectGraph: "artifacts/graph.json" }
```

A path, relative to the workspace root, to the JSON `nx graph
--file=graph.json` emits. Named, it is read instead of resolving the process
working directory's own graph — the only way to graph a workspace the process
is not standing in. Left out, nothing changes.

The file is **trusted**: only a file that is not a project graph at all is
refused. See `codependix-export` for what that does and does not cover.

## Configuring a graph type a project does not have costs nothing

A project that is not a NestJS project never appears in the NestJS pass; a
project with no `tsconfig.json` never appears in the TypeScript import pass.
Neither is a failure and neither needs an override, so a single `defaults`
block naming all four graph types is the normal shape of a
whole-workspace configuration rather than an over-broad one.

## `boundaries` — the rules the graphs are judged against

`defaults` and `projects` say where an export is **written**. `boundaries` says
what the graphs must **look like**, keyed by the same four graph levels, and is
gated by `--check boundaries` rather than by `--check reports`.

```ts
const codependixConfiguration: CodependixConfiguration = {
  boundaries: {
    imports: [
      {
        from: { path: ["**/*.types.ts"] },
        kind: "forbid",
        message: "Types are the leaf of a module.",
        name: "types-files-do-not-reach-services",
        to: { path: ["**/*.service.ts"] },
      },
    ],
    nx: [
      {
        from: { tags: ["type:application"] },
        kind: "forbid",
        name: "applications-are-leaves",
        to: { tags: ["type:application"] },
      },
      { kind: "acyclic", name: "no-project-cycles" },
    ],
  },
};
```

Three kinds:

| Kind | Reports |
| ---- | ------- |
| `forbid` | An edge whose source matches `from` and whose target matches `to` |
| `allow` | An edge leaving `from` for anywhere `to` does not claim |
| `acyclic` | A cycle among the nodes `nodes` selects, defaulting to every node |

A selector's four fields are all lists of globs, and they **narrow** each
other — every field a selector states must match, while within one field one
glob matching is enough:

| Field | Matches | Carried at |
| ----- | ------- | ---------- |
| `id` | The node's identifier — a project name, a file path, or a module class name | every level |
| `path` | A workspace-relative project root, or a project-relative file path | `nx`, `imports`, `pythonImports` |
| `project` | The Nx project a node belongs to | `nx`, `imports`, `pythonImports` |
| `tags` | The node's Nx tags; one tag matching is enough | `nx` |

An access rule may also narrow **which edges** it judges, with `edges`:
`{ implicit: false }` sees only edges backed by an import statement — exactly
what an `@nx/enforce-module-boundaries` `depConstraint` sees — and
`{ implicit: true }` sees only the ones an `implicitDependencies` entry
declares. Unset judges both, which is the stricter reading. Only the Nx level
draws an implicit edge.

Four things to know before writing one:

- **A selector naming a field its level does not carry matches nothing**, not
  everything. A `path` rule at the `nestjs` level selects no module, because
  the NestJS module graph is class names with no file paths at all.
- **A selector stating no field is refused** by the schema. It reads exactly
  like a typo, and reading it as "every node" would silently widen a rule to
  the whole workspace.
- **`message` is appended to the generated sentence, not substituted for it.**
  Write it as the _why_; the _what_ — the rule name and both endpoints — is
  always generated.
- **A level with no rules is never built.** Declaring `nestjs` rules means
  every container is booted in preview mode, and declaring `imports` rules
  means a `ts.Program` per project. Declare only the levels you actually gate.

**Write rules that already hold.** A rule that arrives red is a backlog rather
than a gate, and a red pipeline nobody can act on teaches people to ignore it.
Verify a candidate rule against the whole workspace before committing it.

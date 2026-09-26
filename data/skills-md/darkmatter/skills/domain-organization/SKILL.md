---
name: domain-organization
description: Organize source code by domain owner, keeping models/types with services, defining role and filename conventions, and producing project-wide before/after plans. Use for source packaging and structural moves; use repository-organization for docs/context placement and nix-flake-organization for Nix layout.
---

# Domain organization

Organize source by **owner → role → module**. A path should identify who owns
the behavior, what responsibility it serves, and which concept or operation it
contains. Models and services share an owner; they need not share a file.

Apply [codebase-design](../codebase-design/SKILL.md) when choosing boundaries:
keep each capability together and split only when the split improves
understanding. Role directories organize useful modules; they do not require a
separate file for every helper, query, type, or step.

Apply this to the requested scope. A planning request produces a plan; an
implementation request authorizes the relevant structural changes. This skill
does not itself authorize installs, dependency upgrades, or changes to another
repository.

## Ground the work

Read the target repository's instructions, package guidance, accepted decisions,
manifests, export/import maps, and validation scripts. Inspect actual source and
callers before assigning roles. Treat an existing plan as design evidence, then
reconcile its inventory and execution claims with the current working tree.

Identify the existing owners, public interfaces, composition roots, test policy,
generated inputs, and framework naming requirements. Distinguish verified facts
from proposed paths. For whole-project work, account for every package and app,
including areas intentionally left unchanged.

Preserve explicit user and repository constraints. Resolve routine layout choices
from the code; ask only when an unresolved ownership or contract choice changes
the requested outcome materially.

## Choose the owner

- A focused package can be the owner: `src/models/Invoice.ts` and
  `src/services/InvoiceStore.ts` belong together.
- A package with substantial domains groups by domain first:
  `src/billing/models/Invoice.ts`, `src/billing/services/InvoiceStore.ts`.
- Keep an app's screens, routes, and feature-specific behavior in the app.
  Reusable UI belongs in its own package; discover that package's name and alias
  from the workspace. Keep app routes, stores, and API clients out of it.
- Give shared infrastructure a home based on real owners and callers. Similar
  names alone do not justify merging capabilities or creating another package.
- Distinguish domain `models/` from AI model-provider capabilities. Use the
  latter's actual responsibility, such as `inference/` or `providers/`, without
  silently changing its public contract.

Keep packages as deep modules with small public interfaces. Avoid one package
per type or service. Create role directories only when useful code belongs in
them; preserve precise established roles instead of creating empty scaffolds.

## Assign roles by responsibility

| Role         | Contents and boundary                                                                                                         |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `models/`    | Schemas, derived types, IDs, value objects, and closely related pure operations. Keep a schema and its derived type together. |
| `services/`  | Named capabilities and operations against required interfaces. Receive concrete implementations through composition.          |
| `adapters/`  | Database, HTTP, SDK, filesystem, host, and framework implementations, including provider-specific decoding.                   |
| `workflows/` | Processes coordinating services; the composition root selects concrete adapters.                                              |
| `policies/`  | Business decisions and validation rules that depend on domain concepts.                                                       |
| `mappers/`   | Independently useful conversions between established representations. Keep adapter-private row conversion with its operation. |
| `utils/`     | Small supporting functions independent of domain contracts. Domain-aware helpers belong with their model, policy, or mapper.  |

Use additional roles when they explain the code: `config/`, `tools/`, `prompts/`,
`components/`, `hooks/`, `state/`, `routes/`, or `runtime/`. Configuration shapes
and defaults remain separate from credentials and live resource construction.
Keep app entrypoints thin and put live assembly in the composition root.

Read mixed modules before moving them. A filename does not make a function pure
or separate a service contract from its concrete implementation. Split coherent
responsibilities while preserving behavior; design any necessary semantic change
as a separate change.

Keep an operation's private helpers, queries, bindings, and decoding local when
they must be understood together. Share a mapper or helper when it hides a
meaningful decision or serves real callers, not to shorten another file. Retain
configured line limits and document narrow exceptions for cohesive modules.

## Name modules consistently

These defaults yield to explicit user choices and established repository or
framework constraints. Keep owner directory casing consistent with the repo;
role directories are lowercase and plural.

| Kind                                        | Default                                                   | Example                                            |
| ------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------- |
| Named model, schema, service, or toolkit    | PascalCase                                                | `Invoice.ts`, `InvoiceStore.ts`, `BillingTools.ts` |
| Named adapter                               | PascalCase stem, optional lowercase implementation suffix | `InvoiceStore.postgres.ts`                         |
| Component or JSX module                     | PascalCase                                                | `InvoiceTable.tsx`                                 |
| Function, workflow, policy, mapper, handler | kebab-case                                                | `issue-invoice.ts`, `parse-row.ts`                 |
| React hook                                  | camelCase                                                 | `useInvoice.ts`                                    |
| Companion test or fixture                   | Source stem, lowercase suffix                             | `InvoiceStore.test.ts`, `parse-row.fixture.ts`     |

Conventional files stay recognizable and lowercase: `index`, `app`, `main`,
`agent`, `cli`, `config`, `errors`, `constants`, `types`, `schemas`, `fixtures`,
`testing`, `setup`, and `runtime`. Their directory should supply a narrow meaning.
Split a broad `types.ts` by owned concepts when useful, not by every alias.

PascalCase identifies a named module; it implies neither a class nor a single
export. Keep related schema/type pairs and useful associated exports together.
Retain established exported spellings and service identities during file moves.

Lowercase dotted suffixes distinguish implementation and test roles. Preserve
framework routes, configuration files, declaration files, migration numbering,
SQL, scripts, and generated or registry-managed names through narrow exceptions.
Move ordinary helpers out of component directories when their role differs.

When at least three sibling implementation modules repeat a prefix naming the
same concept, make that concept a subdirectory and remove the prefix from the
filenames:

```text
composer-attachments.ts → composer/attachments.ts
composer-images.ts     → composer/images.ts
composer-text.ts       → composer/text.ts
```

Keep the grouping within its owner and role, such as `utils/composer/text.ts`,
and apply the casing conventions above to the shorter names. Count distinct
implementation modules; companion tests and fixtures follow their source.
Retain descriptive operation names such as `parse-row.ts` when their words
describe the operation itself.

## Preserve public boundaries

Where a package has `src/`, keep implementation there and use thin, explicit
public entry files consistent with the repository's export policy. Expose small
interfaces instead of wildcard-exporting private trees. A model-only entry
should not also pull in a concrete adapter.

The public interface should expose complete operations and own their ordering,
failure, and cleanup. Thin public re-exports establish that boundary; internal
forwarding chains usually add navigation. Translate external execution models
and validate incoming data at the real adapter boundary.

Follow the target's compatibility policy: retain stable public specifiers where
required; where obsolete paths must be removed, update all callers and remove
them. Do not add blanket compatibility wrappers. Public assets and generated
resources need their own export handling rather than a source-file naming rule.

In Effect projects, check the installed Effect Agent contract catalog and
published upstream contracts before defining agent infrastructure types or
services. Import the upstream contract when one exists; organization work does
not justify duplicate sandbox, durability, approval, or workflow contracts.

## Plan or implement

For a requested plan, project-wide reorganization, or phased rollout, read
[references/planning.md](references/planning.md). Save the requested plan in the
target project's `docs/`, even when reusable presets live in a shared repository.
Planning ends with that artifact; proposed moves are not execution evidence.

When implementation is authorized, move one coherent owner at a time. Update
its imports, public exports, private aliases, build roots, test discovery, and
assets together. Match source extensions to alias targets; extension-appending
maps must not turn an import into `Invoice.ts.ts`. Use an intermediate path for
case-only renames where needed so Git records them reliably.

Keep runtime behavior, schemas, wire formats, persistence keys, service tags,
tool names, and workflow identities stable. Use the repository's existing tests
and checks to verify the moved public interfaces and runtime assets. Follow its
test-placement policy rather than imposing a new test tree.

When evaluating, adding, or claiming filename/dependency enforcement, read
[references/enforcement.md](references/enforcement.md). Run the actual selected
checks and verify graph coverage before describing a scope as enforced. Report
the changed paths, verified checks, remaining gaps, and unrelated failures with
their exact command and first actionable diagnostic.

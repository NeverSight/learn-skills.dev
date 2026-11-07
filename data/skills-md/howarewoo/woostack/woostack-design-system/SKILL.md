---
name: woostack-design-system
description: Use when asked to create a project-adapted design system and component catalog, inspect an existing catalog for gaps or drift, or explicitly add, repair, or update selected catalog content.
---

# woostack-design-system

Create a working, project-owned component catalog by inspecting the target repository for
compatible controls, catalogs, and design rules, and by sourcing newly needed components from the
current upstream [shadcn component documentation](https://ui.shadcn.com/docs/components). This
skill ships no templates, component sources, or frozen coverage inventory: the catalog frame,
specimens, coverage record, and provenance are created in the target, and every newly needed
control comes from the live docs and registry at creation time, never from embedded assets. Build an
internal visual catalog showing component variants, states, and interactions; treat component and
preview source as the implementation reference, and do not generate code snippets, copy controls,
or separate usage-example documentation. This command owns component-system creation;
arranging multi-step flows is the separate woostack-flow-layout layout standard, unchanged here.

## Command and authorization

```text
/woostack-design-system
/woostack-design-system inspect the existing catalog
/woostack-design-system add a date-range specimen
/woostack-design-system repair catalog keyboard navigation
/woostack-design-system update the catalog's typography examples
/woostack-design-system migrate the existing catalog to Storybook
```

| Repository state and request | Authorized operation |
| --- | --- |
| No catalog; ordinary invocation | Bounded local creation, necessary catalog dependency/configuration changes, and verification |
| Existing catalog; ordinary invocation or inspection | Read-only gap/drift report; no source, configuration, dependency, lockfile, or generated-file writes |
| Explicit add, repair, update, or tooling migration | Only the named maintenance scope and its necessary verification |

Inspect first; an undocumented catalog still counts as existing. A component library without a
catalog does not prevent creation, but its compatible controls must be reused. Explicit read-only
or local-only limits take precedence. Never create branches, commit, push, publish PRs/issues,
mutate Projects, initialize Woostack configuration, or migrate product UI automatically.

## Inspect and choose placement

Read repository instructions, design rules, manifests, lockfiles, public UI exports and their
callers, styles/tokens, existing catalogs and verification commands. Preserve unrelated work.
Use bundled [implementation patterns](references/patterns.md)
and [testing guidance](references/tdd.md); reading these invokes no
other workflow and authorizes no implementation.

Apply [compatibility](references/compatibility.md) to actual imports, props, composition, style
setup and dependencies. Reuse an existing catalog. For a new catalog, prefer
[Storybook](https://storybook.js.org/docs) when its supported framework and build integration fit;
otherwise choose the smallest repository-native surface and explain the constraint. Do not migrate
existing catalog tooling without an explicit request. Choose repository-native placement, not a
copied workspace path.

Stories or other live specimens import real project components, tokens and providers. Adapt
catalog callers to public APIs, not components to the catalog. Use a supported native framework
integration where it can render the required controls; isolate an incompatible React/shadcn
catalog rather than changing the product's framework, runtime dependencies or behavior.

If a catalog exists and maintenance was not requested, stop before installation or generation.
Report its location, observed coverage, API/style compatibility, provenance, interaction gaps,
and concrete scoped repair options. Distinguish inspected facts from unverified runtime behavior.

## Create or maintain locally

Follow [adaptation and creation](references/adaptation.md). Decide creation from repository
inspection, not from shipped assets: none are shipped. Reuse compatible catalogs, controls,
tokens, and examples before creating anything new. Before any implementation mutation, disclose
the declared coverage user-visibly per [agree the coverage](references/adaptation.md#agree-the-coverage):
inventory or unambiguous coverage set, focused or exhaustive label, and material exclusions,
even when repository evidence supplies the proposal. Repository facts can propose a focused set
but are not requester agreement to narrowing; honor an explicit full-coverage request, and ask
one focused scope question only when the request and evidence leave a material choice
unresolved. When scope is determined, disclose it and proceed within authorization without a
questionnaire or approval gate. Record the declared coverage, source provenance, extensions and
gaps in a coverage record the target owns. Without design rules, use the neutral shadcn Base UI baseline,
not Git Stacks branding or Quiet Workbench styling. Source newly needed controls and examples
from the current upstream docs/registry — via the current Base UI-backed shadcn CLI where it fits
the target configuration — adapting them to real project APIs; never CLI-overwrite existing UI
or initialize over custom setup. Compatible existing primitives are reused, not migrated.
Creation may need registry/CLI network access; the resulting catalog has no remote-source
requirement at runtime. Resolve only newly selected dependencies from authoritative registries
under the bundled
[dependency guidance](references/patterns.md#6-dependencies-resolution-ownership-and-integrity).

Do not add a substitute scaffold, generator, or embedded source dump in place of inspecting the
repository and sourcing current upstream. Do not overwrite custom components, tokens, examples,
rules or unrelated work. Compare before changing existing destinations. Report a conflict and
leave the conflicting surface unchanged; complete independent in-scope work without silently
substituting a duplicate implementation. Adding or repairing content is not permission to migrate
catalog tooling, regenerate the catalog, or upgrade unrelated dependencies.

## Verify and report

Use [verification](references/verification.md) and the target's native commands. Verify real
imports, the declared coverage, live specimens, and actual browser behavior; a
placeholder catalog, extracted source without live specimens, typecheck alone, or site
packaging check is not recreation. Leave no mock controls, dead specimens or unsupported
"complete" claims.

Report catalog placement and commands, declared coverage with gaps, source provenance for reused
and newly created controls, retained upstream notices, design adaptations, preserved
customizations, conflicts, and checks actually observed. Separate deterministic checks, installed-skill/host outcomes and browser
evidence. Failed or unrun required checks remain unverified; name the missing prerequisite and
do not claim completion. Local verified changes are the endpoint; publication requires a
separate user request.

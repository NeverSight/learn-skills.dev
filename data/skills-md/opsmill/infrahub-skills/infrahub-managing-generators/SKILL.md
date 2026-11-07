---
name: infrahub-managing-generators
description: >-
  Creates, modifies and debugs Infrahub Generators — design-driven automation that builds infrastructure objects from templates and topology definitions.
  TRIGGER when: building design-to-implementation workflows, auto-creating objects from templates, topology-driven generation, modifying or extending an existing generator, debugging why a generator produced or deleted the wrong objects or left a field empty or wrong, changing what a generator produces.
  DO NOT TRIGGER when: designing schemas, writing data transforms, querying live data, populating static data files.
argument-hint: "[generator-name] [description...]"
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Generator Creator

## Overview

Expert guidance for creating Infrahub Generators. Generators
query data from Infrahub via GraphQL and create new nodes and
relationships based on the result -- enabling design-driven
automation where a "design" object automatically creates
downstream infrastructure.

## Project Context

Infrahub config:
!`cat .infrahub.yml 2>/dev/null || echo "No .infrahub.yml found"`

Existing generators:
!`find . -name "*.py" -path "*/generators/*" 2>/dev/null | head -20`

## When to Use

- Building design-driven automation (topology -> devices)
- Creating objects from templates or design definitions
- Implementing idempotent create-or-update workflows
- Auto-generating infrastructure from high-level designs
- Understanding the generator tracking system

## Rule Categories

| Priority | Category     | Prefix          | Description            |
| -------- | ------------ | --------------- | ---------------------- |
| CRITICAL | Architecture | `architecture-` | Components, groups     |
| CRITICAL | Python Class | `python-`       | Generator, generate()  |
| HIGH     | Tracking     | `tracking-`     | Upsert, idempotent     |
| HIGH     | API Ref      | `api-`          | Constructor, props     |
| HIGH     | Registration | `registration-` | .infrahub.yml config   |
| MEDIUM   | Patterns     | `patterns-`     | Cleaning, batch, store |
| LOW      | Testing      | `testing-`      | infrahubctl commands   |

## Prerequisites This Skill Depends On

Generators create real objects, so the schema must
permit the shape they emit. Catch these gaps before
the first run — re-running a buggy generator can
delete data via the tracking cleanup.

| If the generator... | The schema must... | See |
| ------------------- | ------------------ | --- |
| Creates objects of kind X | Have node X defined with the attributes the generator sets — a field the kind does not have is dropped before the request is sent, with no error; missing required ones abort the create | [../infrahub-managing-schemas/rules/attribute-defaults-and-types.md](../infrahub-managing-schemas/rules/attribute-defaults-and-types.md) |
| Links the created object to a parent | Have a Component/Parent relationship pair with matching identifiers and `optional: false` on the Parent side | [../infrahub-managing-schemas/rules/relationship-component-parent.md](../infrahub-managing-schemas/rules/relationship-component-parent.md) |
| Reads a "design" node to drive output | Define that node's `human_friendly_id` so the generator's tracking key stays stable across runs | [../infrahub-managing-schemas/rules/display-human-friendly-id.md](../infrahub-managing-schemas/rules/display-human-friendly-id.md) |
| Is triggered by membership in a group | Target the group the design objects are already in, of any kind; create a `CoreStandardGroup` only when none exists. `CoreGeneratorGroup` is the generator's own output group | [rules/registration-config.md](./rules/registration-config.md) |
| Should be idempotent on re-run | Every `save()` uses `allow_upsert=True`; the run's tracking context deletes objects from prior runs that aren't recreated | [rules/tracking-idempotent.md](./rules/tracking-idempotent.md) |
| Imports anything from the repository (a shared package, generated protocols, its own query model) | Carry a `watch:` block in `.infrahub.yml` naming every one of those paths — imports are never followed, so an undeclared helper means the Generator silently stops re-running when that helper changes | [rules/registration-watch-dependencies.md](./rules/registration-watch-dependencies.md) |
| Adding several peers to a cardinality-many relationship | `.extend()` for a list, or a per-peer `.add()` loop — never `.add()` with a list | [rules/python-multi-peer-add.md](./rules/python-multi-peer-add.md) |
| Adding peers to a relationship several runs can write at once | `node.add_relationships(relation_to_update=..., related_nodes=[ids])` | [rules/python-concurrent-relationship-writes.md](./rules/python-concurrent-relationship-writes.md) |
| Deleting objects a generator previously created | Detach the relationships pointing at them before deleting the peers, and save the holder in between — a `save(allow_upsert=True)` after the delete re-sends the ids from the in-memory manager | [rules/python-delete-ordering.md](./rules/python-delete-ordering.md) |
| Modifying a generator so it produces a different set of objects than last run | Audit every `save()` reachable from `generate()`, helpers included | [rules/tracking-idempotent.md](./rules/tracking-idempotent.md) |

## Before writing Python

A generator should *compute* objects from a design. If
what you're about to write is "make these N specific
objects from a hardcoded list," that list is data —
move it to `objects/` and either let the object
loader handle it directly or pass it into a smaller
generator. Walk this ladder before reaching for
`InfrahubGenerator`:

| Signal | Cheaper layer | See rule |
| ------ | ------------- | -------- |
| Generator hardcodes object lists, role catalogs, or status sets | YAML data files under `objects/` (loaded by the object loader) | [yagni-generator-hardcoding-data](../infrahub-auditing-repo/rules/yagni-generator-hardcoding-data.md) |
| Generator recreates a built-in IPAM/VLAN primitive (custom IP address, prefix, VLAN nodes) | `inherit_from: [BuiltinIPAddress / BuiltinIPPrefix / IpamVLAN]` in the schema, then the generator computes references rather than reimplementing the primitive | [yagni-custom-domain-primitives-instead-of-builtin](../infrahub-auditing-repo/rules/yagni-custom-domain-primitives-instead-of-builtin.md) |
| Generator's output shape duplicates objects already in `opsmill/schema-library` | `inherit_from` a library generic; the generator computes the *instance* but not the *shape* | [yagni-duplicate-shape-not-extracted-to-generic](../infrahub-auditing-repo/rules/yagni-duplicate-shape-not-extracted-to-generic.md) |
| Generator allocates a subnet/IP/VLAN/port with `ipaddress` math, `random`, or a hand-written "find the first free one" loop | A built-in resource pool — `allocate_next_ip_prefix` / `allocate_next_ip_address`, `CoreIPPrefixPool` / `CoreNumberPool` — which tracks utilization and stays idempotent across re-runs | [yagni-imperative-allocation-vs-resource-pool](../infrahub-auditing-repo/rules/yagni-imperative-allocation-vs-resource-pool.md) |
| `generate()` stamps a fixed set of children with constant values and no computation (no branching, derived naming, or allocation) | An Object Template (`generate_template: true`) users clone — the structure lives in data, not Python | [yagni-generator-that-should-be-template](../infrahub-auditing-repo/rules/yagni-generator-that-should-be-template.md) |

Bootstrap, seed, and demo generators (under
`bootstrap/`, `seed/`, `demo/`) are exempt — they
exist specifically to hardcode initial state. Use
Python when the generator is genuinely computing
objects from a design definition; see
[rules/python-generate.md](./rules/python-generate.md)
for the legitimate cases.

Once you *are* writing Python, type your SDK calls with generated protocol
classes rather than string kinds — `client.create(NetworkDevice, ...)`, not
`kind="NetworkDevice"` — so a schema change breaks attribute reads on the
returned object at type-check time. Field names passed to `create()` are not
type-checked. See
[protocols-adopt-typed-kinds](../infrahub-common/rules/protocols-adopt-typed-kinds.md).

## Generator Basics

Every generator has three components:

1. **Target group** -- objects that trigger the generator
2. **GraphQL query** (`.gql` file) -- fetches the design data
3. **Python class** -- inherits from `InfrahubGenerator`,
   implements `generate()`

```python
from infrahub_sdk.generator import InfrahubGenerator

class MyGenerator(InfrahubGenerator):
    async def generate(self, data: dict) -> None:
        obj = await self.client.create(
            kind="DcimDevice",
            data={"name": "spine-01"},
        )
        await obj.save(allow_upsert=True)
```

## Workflow

Follow these steps when creating a generator:

1. **Identify the design pattern** — What "design"
   object triggers generation? What objects should be
   created from it? Read
   [rules/architecture-components.md](./rules/architecture-components.md)
   for the target group and generator components.
2. **Write the GraphQL query** — Create a `.gql` file
   that fetches the design data. Read
   [../infrahub-common/graphql-queries.md](../infrahub-common/graphql-queries.md)
   for query patterns. If the repository keeps a
   `schema.graphql`, that file is generated — re-export
   it instead of editing it when a field is missing.
   Read
   [../infrahub-common/rules/protocols-generated.md](../infrahub-common/rules/protocols-generated.md).
3. **Implement the Python class** — Inherit from
   `InfrahubGenerator`, implement `generate()`. Read
   [rules/python-generate.md](./rules/python-generate.md)
   for the class pattern and
   [rules/api-reference.md](./rules/api-reference.md)
   for available methods.
4. **Make it idempotent** — Use `allow_upsert=True` so
   re-running creates or updates without duplicates.
   See [rules/tracking-idempotent.md](./rules/tracking-idempotent.md).
5. **Check for `from_graphql` adoption opportunity** — if
   `generate()` iterates response edges and calls
   `self.client.get()` to re-fetch typed peers, consider
   refactoring to `InfrahubNode.from_graphql()` to collapse
   `O(N + 1)` round trips to `O(1)`. Read
   [rules/patterns-hydration.md](./rules/patterns-hydration.md)
   for the decision tree, detection heuristic, and refactor
   recipe.
6. **Constrain any graph walk**. If `generate()` needs
   the routes between two nodes, use the SDK's
   `traverse_paths` rather than a hand-written per-hop
   walk, and constrain it by relationship identifier plus
   a depth bound. Kind filtering restricts which *nodes*
   may appear, not which *edges* are followed, so a shared
   reference object still bridges unrelated subgraphs and
   the walk returns structurally valid nonsense. Read
   [rules/patterns-path-traversal.md](./rules/patterns-path-traversal.md)
   for the parameter semantics and the truncation signal.
7. **Register in .infrahub.yml** — Add under
   `generator_definitions` with the target group. See
   [rules/registration-config.md](./rules/registration-config.md).
   Then declare the Generator's dependencies with
   `watch.files`: read its imports and runtime file reads,
   and name every first-party path they resolve to —
   sibling query models included. Always carry the key;
   `files: []` when the Generator genuinely has no
   dependency beyond its own file. Read
   [rules/registration-watch-dependencies.md](./rules/registration-watch-dependencies.md),
   which also covers reviewing an existing `watch` block
   for entries that are missing, stale, or wrong.
8. **Test** — Run `infrahubctl generator` to validate.
   See [rules/testing-commands.md](./rules/testing-commands.md).

## Supporting References

- **[reference.md](./reference.md)** -- Class API,
  lifecycle, idempotency contract, `.infrahub.yml`
  registration (with the `query:`-required shape that
  differs from check_definitions)
- **[examples.md](./examples.md)** -- Complete Generator
  patterns (POP topology, network segment, minimal)
- **[../infrahub-common/graphql-queries.md](../infrahub-common/graphql-queries.md)**
  -- GraphQL query writing reference
- **[../infrahub-common/infrahub-yml-reference.md](../infrahub-common/infrahub-yml-reference.md)**
  -- .infrahub.yml project configuration
- **[../infrahub-common/marketplace-reference.md](../infrahub-common/marketplace-reference.md)**
  -- reuse a marketplace-published schema for the target
  data model before hand-rolling one to generate against
- **[../infrahub-common/rules/](../infrahub-common/rules/)** -- Shared rules
  (git integration, caching gotchas)
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap (e.g. deleting nodes)
- **[../infrahub-managing-schemas/SKILL.md](../infrahub-managing-schemas/SKILL.md)**
  -- Schema definitions Generators work with
- **[rules/](./rules/)** -- Individual rules organized by
  category prefix

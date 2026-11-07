---
name: infrahub-managing-objects
description: >-
  Creates, modifies and manages Infrahub object data YAML files for populating infrastructure instances — devices, locations, organizations, and modules.
  TRIGGER when: creating device instances, populating data files, defining locations or organizations, adding infrastructure objects, modifying or extending an existing data file, updating attribute values or relationship links on objects already defined in a data file, debugging why an object fails to load.
  DO NOT TRIGGER when: designing or modifying schemas, including changing an attribute or relationship definition on a node kind (use infrahub-managing-schemas), writing Python checks/generators, querying live data.
argument-hint: "[kind] [object-details...]"
metadata:
  version: 1.3.0
  author: OpsMill
---

# Object Creator

## Overview

Expert guidance for creating Infrahub object (data) files.
Objects are YAML files that populate schema nodes with actual
infrastructure data -- devices, locations, organizations,
modules, and more.

## Project Context

Existing schema files:
!`find . -name "*.yml" -path "*/schemas/*" -o -name "*schema*" -name "*.yml" 2>/dev/null | head -10`

Existing object files:
!`find . -name "*.yml" -path "*/objects/*" 2>/dev/null | head -20`

If invoked with arguments (e.g., `/infrahub:managing-objects DcimDevice spine-01`),
use the first argument as the kind and remaining arguments as object details.

## When to Use

- Creating new data files for infrastructure objects
- Populating devices, locations, organizations, or other schema nodes
- Setting up hierarchical data (location trees, tenant groups)
- Referencing related objects across files
- Managing component children (interfaces, modules)
- Organizing object files for correct load order
- Updating attribute values or relationship links in an existing data file
- Debugging why an object fails to load or resolves the wrong reference

## Rule Categories

| Priority | Category | Prefix | Description |
| -------- | -------- | ------ | ----------- |
| CRITICAL | Branch-First Loading | `workflow-` | Load onto a branch, not the default branch |
| CRITICAL | File Format | `format-` | apiVersion, kind, spec structure |
| CRITICAL | Value Mapping | `value-` | Attributes, dropdowns, references |
| HIGH | Children | `children-` | Hierarchy/component nesting |
| MEDIUM | Range | `range-` | Sequential interface expansion |
| MEDIUM | Organization | `organization-` | Naming, load order, multi-doc |
| LOW | Patterns | `patterns-` | Flat lists, devices, git repos |

## Schema Features This Skill Depends On

Object files reference schema-defined shapes; missing
schema setup turns into "object failed to load" or
"reference not found" errors at sync time. Before
populating data, verify the schema upstream:

| If the object... | The schema must... | See |
| ---------------- | ------------------ | --- |
| References another object across files | Define `human_friendly_id` on the target node (the shape determines scalar-vs-list reference) | [../infrahub-managing-schemas/rules/display-human-friendly-id.md](../infrahub-managing-schemas/rules/display-human-friendly-id.md) |
| Sits in a location/parent tree | Use a hierarchical generic with `parent`/`children` and full-kind peer references | [../infrahub-managing-schemas/rules/hierarchy-setup.md](../infrahub-managing-schemas/rules/hierarchy-setup.md) |
| Sets a Dropdown attribute value | Declare the dropdown `choices` as objects with `name` (not bare strings); the object references the choice `name` | [../infrahub-managing-schemas/rules/attribute-defaults-and-types.md](../infrahub-managing-schemas/rules/attribute-defaults-and-types.md) |
| Owns Component children inline | The parent's Component relationship and child's Parent relationship must share an identifier and the child needs `optional: false` | [../infrahub-managing-schemas/rules/relationship-component-parent.md](../infrahub-managing-schemas/rules/relationship-component-parent.md) |
| Will be the target of an artifact pipeline | The concrete node must `inherit_from: CoreArtifactTarget` (set on the node, not on a generic) | [../infrahub-managing-schemas/rules/extension-artifact-target.md](../infrahub-managing-schemas/rules/extension-artifact-target.md) |

If any of these is missing, the schema needs an
update before the objects can load — that's a
schema migration, not an object fix.

## Object File Basics

```yaml
---
apiVersion: infrahub.app/v1
kind: Object
spec:
  kind: <NodeKind>          # Schema node kind (e.g., DcimDellServer)
  data:
    - <attribute>: <value>  # List of object instances
```

`apiVersion`, `kind: Object`, `spec.kind`, and `spec.data`
are always required. Each `spec` block targets a single
node kind.

## Workflow

Follow these steps when creating object data files:

1. **Plan to load onto a branch, not the default branch** —
   Decide the dedicated branch this data will load onto
   before writing the files, and surface it when you hand
   off the load commands. Loading into the default branch
   (the target when no `--branch` is given — `main` by
   convention, but it can be renamed) writes unreviewed
   data to the source of truth, and a bad bulk load there
   means deleting objects one by one instead of discarding
   a branch. Read
   [rules/workflow-branch-first.md](./rules/workflow-branch-first.md).
   The default branch is only reasonable on a local
   throwaway instance.
2. **Read the schema** — Identify the target node kind,
   its attributes, relationships, and whether it has
   component children or hierarchy parents.
3. **Plan the file structure** — Read
   [rules/format-structure.md](./rules/format-structure.md)
   for the required YAML structure and
   [rules/organization-load-order.md](./rules/organization-load-order.md)
   for file naming and load order conventions.
4. **Map attribute values** — Set each attribute using
   the correct value format. Read
   [rules/value-attributes.md](./rules/value-attributes.md)
   for attribute mapping and
   [rules/value-relationships.md](./rules/value-relationships.md)
   for relationship references. If the object should inherit
   shared defaults from a Profile or be created from an Object
   Template, read
   [rules/value-profiles-templates.md](./rules/value-profiles-templates.md).
   To stamp lineage or lock
   a value, write it as a `value` + metadata mapping —
   see [../infrahub-common/metadata-lineage.md](../infrahub-common/metadata-lineage.md)
   (remember `source` is lineage only; locking needs
   `owner` + `is_protected`).
5. **Handle children** — If the node has component
   children or hierarchy nesting, read
   [rules/children-components.md](./rules/children-components.md)
   and [rules/children-hierarchy.md](./rules/children-hierarchy.md).
6. **Validate and load on the branch** — Check YAML syntax,
   ensure referenced objects exist or are defined in
   earlier load-order files, then validate and load against
   your branch (`--branch`). See
   [validation.md](./validation.md) for the commands and
   pre-load checklist.

## Supporting References

- **[reference.md](./reference.md)** -- Object file format
  specification
- **[validation.md](./validation.md)** --
  `infrahubctl object validate` / `object load`
  commands, common load errors, pre-load checklist
- **[examples.md](./examples.md)** -- 15 complete object
  patterns from production repos
- **[../infrahub-common/infrahub-yml-reference.md](../infrahub-common/infrahub-yml-reference.md)**
  -- .infrahub.yml project configuration
- **[../infrahub-common/marketplace-reference.md](../infrahub-common/marketplace-reference.md)**
  -- if the schema these objects populate came from the
  marketplace, reuse it rather than modelling a new one
- **[../infrahub-common/metadata-lineage.md](../infrahub-common/metadata-lineage.md)**
  -- Value metadata (`source`, `owner`, `is_protected`):
  setting lineage/ownership and why `source` does not
  control edit access
- **[../infrahub-common/rules/](../infrahub-common/rules/)** -- Shared rules
  (git integration, caching) across all skills
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap (e.g. deleting nodes)
- **[../infrahub-managing-schemas/SKILL.md](../infrahub-managing-schemas/SKILL.md)**
  -- Schema definitions these objects conform to
- **[rules/](./rules/)** -- Individual rules by category
  prefix

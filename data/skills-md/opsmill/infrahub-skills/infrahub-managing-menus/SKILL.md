---
name: infrahub-managing-menus
description: >-
  Creates, modifies and debugs Infrahub custom navigation menus for the web UI sidebar, organizing node types into logical groups.
  TRIGGER when: designing sidebar menus, grouping node types in UI, customizing Infrahub web interface navigation, modifying or extending an existing menu, changing the order, nesting, or icons inside a menu file, debugging why a menu item does not appear or lands in the wrong group.
  DO NOT TRIGGER when: designing or modifying schemas, including setting menu_placement, icon, or order_weight on a schema node (use infrahub-managing-schemas), writing checks or transforms, populating data objects.
argument-hint: "[menu-structure-description]"
metadata:
  version: 1.3.0
  author: OpsMill
---

# Infrahub Menu Creator

## Overview

Expert guidance for creating Infrahub custom menus.
Menus control the left-side navigation in the web
interface, organizing schema node types into a custom
hierarchy.

## Project Context

Existing menu files:
!`find . -name "*.yml" -path "*/menus/*" 2>/dev/null | head -10`

Schema files (to identify available node types):
!`find . -name "*.yml" -path "*/schemas/*" -o -name "*schema*" -name "*.yml" 2>/dev/null | head -10`

## When to Use

- Designing navigation menus for the Infrahub web UI
- Organizing node types into logical groups
  and hierarchies
- Adding icons and labels to menu items
- Setting up group headers (non-clickable)
  with nested children
- Configuring schema nodes to use custom menus
  instead of auto-generated ones
- Reordering, renaming, or regrouping an existing
  menu file
- Debugging why a menu item does not appear, or
  lands in the wrong group

## Rule Categories

| Priority | Category   | Prefix       | Description                  |
| -------- | ---------- | ------------ | ---------------------------- |
| CRITICAL | Format     | `format-`    | apiVersion, kind, spec       |
| CRITICAL | Properties | `item-`      | name, namespace, label, kind |
| HIGH     | Hierarchy  | `hierarchy-` | Nesting, group headers, data |
| HIGH     | Icons      | `icons-`     | MDI icon reference, choices  |
| MEDIUM   | Schema     | `schema-`    | include_in_menu, kind links  |
| LOW      | Patterns   | `patterns-`  | Flat menu, comments, links   |

## Schema Features This Skill Depends On

A custom menu doesn't replace the auto-menu — it
augments it. Schemas need cooperating settings to
avoid duplicates and stay UI-stable.

Duplicates come from two places, and only one of them
is the schema's. Nodes the auto-menu also emits are
settled below with `include_in_menu: false`; sections
Infrahub itself ships are settled in the menu file
with `parent:`, covered in
[rules/hierarchy-nesting.md](./rules/hierarchy-nesting.md).

| If the menu item... | The schema must... | See |
| ------------------- | ------------------ | --- |
| Links to a schema node's list view via `kind:` | Define that node (or generic) so the URL resolves — and set `include_in_menu: false` on it to suppress the duplicate auto-menu entry | [rules/schema-integration.md](./rules/schema-integration.md) |
| Shows all subtypes under one entry via a generic kind | Have the generic defined, with all the relevant nodes `inherit_from` it | [../infrahub-managing-schemas/rules/hierarchy-setup.md](../infrahub-managing-schemas/rules/hierarchy-setup.md) |
| Should appear at a specific position when auto-menu is in play | Set `order_weight` on the schema node (auto-menu uses it; custom menu ignores it) | [../infrahub-managing-schemas/rules/display-order-weight.md](../infrahub-managing-schemas/rules/display-order-weight.md) |
| Groups subtypes under a parent node entry | Set `menu_placement: <FullKind>` on each subtype so the auto-menu side groups consistently with the custom menu | [../infrahub-managing-schemas/rules/display-menu-placement.md](../infrahub-managing-schemas/rules/display-menu-placement.md) |

Audit `include_in_menu` on every node you reference
from the menu file — the sidebar duplicates that
this prevents look to users like the custom menu is
"broken", but the fix is on the schema side.

## Menu File Basics

```yaml
---
apiVersion: infrahub.app/v1
kind: Menu
spec:
  data:
    - namespace: Dcim
      name: DeviceMenu
      label: "Devices"
      icon: "mdi:server"
      kind: DcimDevice        # Links to schema node list view
```

`apiVersion`, `kind: Menu`, and `spec.data` are always
required. Each menu item needs `name` and `namespace`.

## Workflow

Follow these steps when creating a menu:

1. **Gather requirements** — Ask what schema nodes
   exist, how they should be grouped, and whether
   the user wants flat or hierarchical navigation.
2. **Read relevant rules** — Read `rules/format-structure.md`
   for the required YAML structure, `rules/item-properties.md`
   for item fields, and `rules/icons-reference.md`
   to pick appropriate MDI icons. Read
   `rules/hierarchy-nesting.md` before placing any item,
   flat menus included: Infrahub already ships IPAM,
   Object Management, Branches and others, and anything
   belonging in one of those attaches with `parent:`
   rather than being declared again.
3. **Generate the menu YAML** — Start with the
   `$schema` comment and `apiVersion`/`kind`/`spec`
   structure. Apply rules from step 2.
4. **Add registration and schema guidance** — Every
   menu file output must include:
   - A YAML comment block showing how to register
     the file in `.infrahub.yml` under the `menus:`
     key (see `rules/format-structure.md`)
   - A YAML comment block advising to set
     `include_in_menu: false` on every schema node
     that appears in the custom menu, to prevent
     duplicate sidebar entries
     (see `rules/schema-integration.md`)

   Include these as comments at the top of the file,
   before the `---` document separator. This ensures
   the user sees the guidance alongside the menu
   definition.

## Supporting References

- **[examples.md](./examples.md)** -- Four worked
  menu hierarchies (flat, grouped, generic-linked,
  full multi-domain) ready to copy and adapt
- **[infrahub-yml-reference.md](../infrahub-common/infrahub-yml-reference.md)**
  -- .infrahub.yml project configuration
- **[common/rules/](../infrahub-common/rules/)**
  -- Shared rules (git integration, caching gotchas)
  that apply across all skills
- **[../infrahub-common/rules/workflow-information-priority.md](../infrahub-common/rules/workflow-information-priority.md)**
  -- Skill content first; how to consult `docs.infrahub.app`
  on a genuine gap (e.g. deleting nodes)
- **[managing-schemas](../infrahub-managing-schemas/SKILL.md)**
  -- Schema node kinds that menus link to
- **[rules/](./rules/)**
  -- Individual rules organized by category prefix

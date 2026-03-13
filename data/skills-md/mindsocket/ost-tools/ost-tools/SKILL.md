---
name: ost-tools
description: >
  Use this skill when working with ost-tools — a CLI that validates Obsidian markdown frontmatter
  against JSON schemas for structured knowledge "spaces", and converts to other formats. Trigger when: (1) validating a space after
  content edits, (2) writing or updating a schema file or rules, (3) configuring a space or designing a schema (new or existing), (4) troubleshooting validation errors, (5) running `ost-tools` commands.
---

# ost-tools

`ost-tools` validates Obsidian markdown frontmatter against JSON schemas. Content lives in
**spaces** (directories of `.md` files or a single "on-a-page" format); schemas define entity types, properties, and rules.

## Finding the config

ost-tools looks in `$XDG_CONFIG_HOME/ost-tools/config.json`, unless given an explicit config, e.g.:

```bash
bunx ost-tools validate <space> --config path/to/config.json
# or
OST_TOOLS_CONFIG=path/to/config.json bunx ost-tools validate <space>
```

**Always read the config first** to understand available spaces and their schema locations before running other commands.

Tip: To reduce the need for `--config` flags consider, with user permission, using `includeSpacesFrom` in a central config file that's loaded by default (eg `~/.config/ost-tools/config.json`).

## Orientation

Before working with a space, use these to understand what's configured:

```bash
bunx ost-tools spaces --config <cfg>                        # per-space: path, schema, fieldMap, templates, miro
bunx ost-tools schemas show --space <name> --config <cfg>  # entity types, properties, rules, enums + registry
bunx ost-tools schemas show <filename>                      # inspect a bundled partial (e.g. _ost_tools_base.json)
bunx ost-tools readme                                       # full documentation if needed
```

`spaces` is the starting point — it shows each space as a block with its schema name, `fieldMap`
mappings (if any), template config, and whether Miro is configured.

`schemas show --space` is the primary schema tool — it lists entity types and their properties (required
marked with `*`), the hierarchy, all rules with descriptions, definitions with enum values, and the
loaded schema registry. **Run this before authoring content or writing rules** to ensure you use the correct field names and types. The registry section
at the bottom shows which bundled and local partials are in scope for `$ref` targets.

`schemas show <filename>` (e.g. `_ost_tools_base.json`) reveals available definitions in bundled
partials.

## Commands for working with spaces

```
validate      Validate space content against schema
show          Output the node hierarchy
dump          Output parsed node data as JSON
diagram       Generate Mermaid diagram
miro-sync     Sync to Miro board (requires MIRO_TOKEN env var + miroBoardId in config)
template-sync Sync Obsidian templates from schema examples
```

Run `bunx ost-tools --help` or `bunx ost-tools <command> --help` for flags.

**`dump` is the key debugging tool.** Use it to verify `fieldMap` remapping is working or to
inspect exactly what JSONata rules see when a rule fires unexpectedly.

## Non-obvious issues

**All files appear as "Non-space (no type field)"** — the space uses a different field name for the entity discriminator
(e.g., `record_type`). Configure `fieldMap` in the space config to remap it to `type`.

**Rule violations on every node of a type** — the rule may be too strict or misconfigured. Use `dump` to verify
what the rule actually sees in the `current` object, then adjust the rule in the schema.

**`show`/`diagram` show only orphans and non-hierarchy types** — the schema's `$metadata.hierarchy` may not have edge configuration for the space's relationship fields. Use `schemas show --space <name>` to check the hierarchy definition. Each non-root level can define a `field` entry (overriding default `parent:` field (and optionally `fieldOn: "parent"` / `multiple: true`) to wire up the correct relationship field.

## Troubleshooting Common Errors

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `File has no type field` | Discriminator field missing or named differently | Check `fieldMap` in config or add `type` to frontmatter |
| `must have property 'X'` | Required schema property missing | Check `schemas show --space` to see required properties |
| `could not find node '[[Title]]'` | Broken wikilink | Fix the title in the link or ensure the target file exists and has that title |
| `JSONata error: ...` | Syntax error in schema `$metadata.rules` | Verify the expression with `dump` and a JSONata tester |

## References

- **`references/schema-authoring.md`** — schema file structure, `$metadata`, `fieldMap`, JSONata rules
- **`references/schema-design.md`** — process for designing a schema from existing content
- **`references/commands.md`** — detailed CLI usage and examples

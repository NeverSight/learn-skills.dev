---
name: port-integrations
description: "Configure and troubleshoot Port integrations: mapping YAML, resources, selectors, JQ-based entity mappings, relations, and advanced options like createMissingRelatedEntities and itemsToParse. Use when asked to 'write a Port mapping', 'map API or tool data to a Port blueprint', 'configure an Ocean integration mapping', 'add a relation to a Port mapping', 'parse an array into separate Port entities', 'fix a Port mapping JQ error', or 'why isn't my Port integration syncing the right entities or properties'. For installing a new integration end-to-end and populating the catalog for the first time, use the nested `port-install-integration` skill instead. For testing integration connectivity or validating credentials before a sync, use the nested `port-integration-test-connection` skill instead."
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot"
metadata:
  version: "1.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,integrations,mapping,ocean,jq,mcp-powered
  summary: Configure and troubleshoot Port integration mapping
---

# Port integrations

This skill teaches you how to author, edit, and debug the mapping configuration for a
Port integration: the YAML that tells an [Ocean-based integration](https://docs.port.io/build-your-software-catalog/custom-integration/ocean-custom-integration/overview)
(or any Port integration) which API objects to fetch and how to turn them into Port
entities, using [JQ](https://jqlang.org/manual/) expressions.

## Use this skill when

- Writing a new mapping for an integration (`resources`, `selector`, `port.entity.mappings`).
- Adding or fixing a relation between two blueprints inside a mapping.
- Splitting an array field into multiple entities with `itemsToParse`.
- A mapping test fails, or entities sync with missing/wrong data.

Out of scope: creating the blueprints and relations themselves (a mapping can only map
into fields that already exist on a blueprint), and general JQ language tutorials beyond
what mapping needs (see [references/mapping.md](references/mapping.md) for the
patterns that come up most). Installing a new integration end-to-end — kind selection,
use-case discovery, and populating the catalog for the first time — is the nested
[`port-install-integration`](port-install-integration/SKILL.md) skill, not this one.
Testing integration connectivity or validating credentials (`test connection`) — is the
nested [`port-integration-test-connection`](port-integration-test-connection/SKILL.md)
skill, not this one.

## Prerequisites

- Go over the `port-getting-started` skill first if this is your first time
  working with Port.
- A Port account, with the target blueprint(s) already created.
- An installed integration (hosted or self-hosted Ocean integration, or any other Port
  integration that exposes a mapping) whose `kind`s you're mapping from. If none is
  installed yet, see the [Ocean custom integration overview](https://docs.port.io/build-your-software-catalog/custom-integration/ocean-custom-integration/overview)
  first: this skill assumes the integration exists and can return data.
- Port's [MCP server](https://docs.port.io/ai-interfaces/port-mcp-server/overview) connected
  is **optional**. When connected, use it to fetch live blueprints and raw data, apply
  the mapping directly, and test it before saving. When it isn't connected, every step
  below has a documented fallback using the Port UI or public API. Never treat a missing
  MCP connection as a hard stop. Search `search_port_knowledge_sources` for anything
  this skill doesn't cover.

## Step 1 - Identify the target blueprint and source kind

Precondition: you know which Port blueprint the data should land in, and which API object (`kind`) the integration exposes for it.
Action: if MCP is connected, call `list_blueprints` to confirm the blueprint exists and read its exact property and relation identifiers (mapping into a property that doesn't exist fails validation). Check the integration's documentation for its supported `kind`s.
Fallback: open the blueprint in Port's [data model page](https://app.port.io/settings/data-model) to read its schema, and check the integration's page under [sync data to catalog](https://docs.port.io/build-your-software-catalog/sync-data-to-catalog/) for its supported kinds.

## Step 2 - Get a raw data sample for the kind

Precondition: you need a real (or representative) example of what the API returns for this `kind`, to write correct JQ paths.
Action: if MCP is connected, call `get_integration_kinds_with_examples` for the integration to get real raw data. Write JQ expressions against the actual field names and nesting shown there, not assumptions.
Fallback: use **Test examples** in the mapping's YAML editor (`+ Add kind`) in the Port UI, paste a real payload from the source API's own documentation, or capture one request to the API directly.

## Step 3 - Write the resource, selector, and query filter

Precondition: you know the data source and which items should be ingested versus skipped.
Action: add a `resources` entry with the `kind`, then a `selector` block. Use integration-specific selector keys to narrow the API request itself (cheaper, faster), and the `query` JQ expression to filter the response (`"true"` ingests everything). Order resources so a relation's target blueprint is ingested first. See [assets/simple-mapping.yaml](assets/simple-mapping.yaml).
Fallback: not applicable, this step has no external dependency.

## Step 4 - Write the entity mappings

Precondition: the resource and selector from step 3 are in place.
Action: under `port.entity.mappings`, set `identifier`, `title`, `blueprint`, and `properties` as JQ expressions evaluated against each item. Wrap hyphenated property or identifier names in bracket notation (`.properties["my-field"]`, not `.my-field`, which JQ parses as subtraction). See [references/mapping.md](references/mapping.md) for common transformations.
Fallback: not applicable, this is static authoring.

## Step 5 - Add relations, if any

Precondition: the target blueprint of the relation is ingested by an earlier resource (or already exists in the context lake).
Action: use a direct identifier reference (`relations: { serviceOwner: .owner.id }`) when the API returns the related entity's identifier directly, or a search query rule (`combinator`/`rules`) when you only have one of its properties. Relations are **replaced** on every sync, an empty array clears the relation. See [assets/mapping-with-relations.yaml](assets/mapping-with-relations.yaml).
Fallback: skip the relation in the mapping and assign it manually in the Port UI if you want to manage it outside the integration entirely.

## Step 6 - Set advanced options, if needed

Precondition: related entities referenced by this mapping may not exist yet, or you're exploding an array into multiple entities.
Action: add root-level `createMissingRelatedEntities: true` to auto-create missing relation targets, `deleteDependentEntities: true` when a required relation means the source entity must be deleted alongside its target, or `itemsToParse` (plus optional `itemsToParseName` and `itemsToParseTopLevelTransform`) to turn one array field into several entities.
Fallback: not applicable, these are static YAML keys.

## Step 7 - Validate the mapping

Precondition: you have a draft mapping and a raw data example from step 2.
Action: if MCP is connected, call `test_integration_mapping` with the mapping and the example from `get_integration_kinds_with_examples`, and iterate until it returns the expected entity with no errors.
Fallback: use **Test mapping** in the Port UI's YAML editor against the same example, or save the mapping, trigger a resync, and inspect the result: `get_integration_event_logs` if MCP is connected, otherwise the sync's logs in the [data sources page](https://app.port.io/settings/data-sources). For self-hosted Ocean integrations, you can also run the integration locally in dry-run mode before pointing it at production.

## Step 8 - Diagnose a failing or incomplete sync

Precondition: entities are missing, incomplete, or a test/resync reports errors.
Action: work through [references/troubleshooting.md](references/troubleshooting.md), which covers the five common root causes (mapping errors, missing data, relation issues, permission issues, filter issues), each with an MCP-powered diagnostic path and a UI/API fallback.
Fallback: not applicable, this step is itself the fallback path.

## Common pitfalls

| Symptom | Likely cause | Fix |
|---|---|---|
| `must NOT have additional properties` on test | Typo'd YAML key, wrong nesting level | Compare against [configure-mapping.md](https://docs.port.io/build-your-software-catalog/customize-integrations/configure-mapping) structure |
| `Blueprint with identifier "X" was not found` | Blueprint doesn't exist, or identifier typo | Confirm with `list_blueprints` or the data model page |
| A relation silently disappears after sync | JQ for the relation evaluated to an empty array | Relations are replaced, not merged, every sync. Return the full desired set |
| `.my-property` mapping returns nothing | Hyphen parsed as subtraction by JQ | Use `.properties["my-property"]` bracket notation |
| Entity never appears despite valid JQ | `selector.query` evaluates to `false` for that item | Test the query alone against the sample data first |
| Related entity never gets created | Related blueprint's resource runs after this one, or doesn't exist yet | Reorder resources, or set `createMissingRelatedEntities: true` |

## Quick reference

A mapping is: root-level advanced options (`createMissingRelatedEntities`,
`deleteDependentEntities`), then a `resources` list. Each resource has a `kind`, a
`selector` (`query` plus integration-specific keys), and `port.entity.mappings`
(`identifier`, `title`, `blueprint`, `properties`, `relations`), with `itemsToParse` on
`port` when one array field should become several entities.

Two complete, copy-pasteable starting points:

- [assets/simple-mapping.yaml](assets/simple-mapping.yaml) - one resource, no relations.
- [assets/mapping-with-relations.yaml](assets/mapping-with-relations.yaml) - two
  resources, a direct-identifier relation, a search-query relation, and
  `createMissingRelatedEntities`.

See [references/mapping.md](references/mapping.md) for mapping guidance and JQ recipes,
and [references/troubleshooting.md](references/troubleshooting.md) for the diagnostic
playbook. Full concept reference:
[configure-mapping.md](https://docs.port.io/build-your-software-catalog/customize-integrations/configure-mapping).

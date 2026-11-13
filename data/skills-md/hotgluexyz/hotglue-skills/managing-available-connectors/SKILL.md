---
name: managing-available-connectors
description: Configures Hotglue available entities, v2 sources, connectors, targets, linked entities, discovery, and field maps. Use when adding, forking, inspecting, or debugging available connector definitions.
---

# Managing Available Connectors

Use the environment configuration as the source of truth. Download it first, inspect the existing definitions, make the smallest change, deploy it, and confirm the linked entity state.

## Available entity roles

For a v2 flow:

- A **connector** is the primary bidirectional system. Set `isConnector: true`.
- A **source** supplies write-job data. Set `isSource: true`, `isConnector: false`.
- A **target** receives read-job data. Set `isTarget: true`, `isConnector: false`.

Do not create aliases, duplicate entities, or unrelated available definitions. Reuse or fork an existing available connector when only its install URI needs to change.

### Forking an existing entity

Fork the existing available entity in place; do not create a similarly named connector. Preserve all of its `connect_ui_params`, role flags, and authentication fields. Add only the requested settings and the forked install URI.

For a bidirectional integration, write down the required topology before adding anything. For example, “Source: Ongoing, Connector: QuickBooks, Target: Ongoing” means Ongoing is both a source and a target—not an additional connector.

## Custom Singer identifiers

Hotglue prefixes tap package commands with `tap-`. For an available entity named `crm`, configure the custom source consistently:

```json
{
  "id": "crm",
  "read_connector": {
    "id": "crm",
    "tap_driver_name": "crm",
    "install_uri": "git+https://github.com/hotgluexyz/tap-crm.git@feature/example"
  }
}
```

Do not use `tap-crm` for the entity ID or driver name and do not add a duplicate console-script alias in the package.

## Safe workflow

1. Download the environment configuration with hotglue CLI `hotglue env download` into a temporary directory.
2. Inspect `availableConnectors.json` and list the existing source, connector, and target entries to the user before adding or deleting definitions.
3. For an available entity, preserve the original auth UI fields and include only the requested role flags, connection fields, install URI, and icon. Mark a fork with `isForked: true` only when it is actually a fork.
4. Deploy the environment configuration with `hotglue env deploy`.
5. Reuse an existing v2 flow or create one when needed; add supported entities, and link the tenant entities.
6. Run discover once for the entity being read. Confirm the expected catalog before setting a field map.
7. Set the field map on the linked entity that is read in that direction:
   - linked **source** for a write job;
   - linked **connector** for a read job.
8. Re-fetch linked entities with `catalog=true` and verify the persisted field map and selected stream names.

### Changing `install_uri`

Jobs install from the available-connector catalog, not from the linked config.
To point an entity at a custom git URI or branch, set `install_uri` on
`read_connector` or `write_connector` in `availableConnectors.json` via
`hotglue env download` → edit → `hotglue env deploy`. See
[connector settings](https://docs.hotglue.com/key-concepts/connectors/v2-connectors/settings).

- The change is **env-wide** until reverted.
- `connector_tag` works only with Hotglue-maintained repositories (version
  zips). For arbitrary git repos, put the tag or commit in `install_uri`.
- Do not change the linked `config.json` or `supportedConnectors` to change
  what code runs — those hold credentials/labels, not the install.

## Field maps

A field map is a selection of streams and fields to read, not a cross-system transform. Keep it narrow. For example, a sole `accounts` source stream should have a single `accounts` map entry with only fields the ETL needs.

The catalog only describes available streams and fields. Never treat catalog updates as field selection: PATCH the linked source or connector `field_map` object after discovery completes.

Do not set a field map on the primary connector while setting up a write job from an external source. That map is relevant only when the connector itself is the read side.

## Singer SDK targets

When an available entity uses a custom Singer target, set `singer_sdk: true` under its `write_connector`. Without it, ETL Singer output is not passed to the target. Confirm this field is deployed before diagnosing empty exports.

## Configuration and security

- Read a target's config schema before linking or running. Some target branches can incorrectly require settings unrelated to the sink being used; fix the target schema rather than persisting meaningless credentials.
- Keep API keys and tenant credentials in local secret files or environment variables. Never commit them or print full effective job configuration.
- When a job command can echo secrets, project its output to non-sensitive job fields such as `job_id`, `status`, and `job_url`.

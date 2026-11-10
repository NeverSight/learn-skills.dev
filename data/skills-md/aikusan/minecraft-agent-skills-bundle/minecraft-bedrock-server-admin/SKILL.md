---
name: minecraft-bedrock-server-admin
description: "Operate Minecraft Bedrock Dedicated Server for 1.21.x. Use for BDS install and update planning, UDP networking, server.properties, allowlist.json, permissions.json, world folders, resource_packs and behavior_packs deployment, backup/restore, Docker or service management, log triage, and incident response. Choose this for Bedrock server administration rather than Java Paper/Purpur operations or Bedrock add-on development."
---

# Minecraft Bedrock Server Administration Skill

## Scope

Use this skill for Bedrock Dedicated Server operations on Windows or Linux hosts.
Prefer the official BDS model and avoid unofficial native plugin-loader workflows
unless the user explicitly asks for them.

### Routing Boundaries
- `Use when`: the task is BDS setup, configuration, user access, world/resource deployment, backups, networking, or production operations.
- `Do not use when`: the task is Java Edition server operations (`minecraft-server-admin`), Bedrock add-on code (`minecraft-bedrock-addon-dev`), Java plugin development (`minecraft-plugin-dev`), or Java-to-Bedrock pack conversion (`minecraft-resource-pack-conversion`).
- `Do not use when`: the task is Geyser/Floodgate crossplay on a Java server (`minecraft-crossplay-ops`) or LuckPerms policy (`minecraft-permissions-admin`).

## Operating Model

Treat BDS as a file-backed service:

```text
bedrock-server/
├── bedrock_server
├── server.properties
├── allowlist.json
├── permissions.json
├── worlds/
├── resource_packs/
├── behavior_packs/
└── development_behavior_packs/
```

Keep the live server directory small and reproducible. Store backups, downloaded
server archives, and deployment notes outside the live directory.

## Administration Workflow

1. Identify server version, host OS, startup method, and open UDP ports.
2. Back up `worlds/`, `server.properties`, `allowlist.json`, `permissions.json`,
   and active pack folders before changing runtime state.
3. Make one operational change at a time.
4. Restart BDS only when the change requires it.
5. Verify from both the console log and a Bedrock client.

## Network And Access Checks

Default Bedrock ports:

```properties
server-port=19132
server-portv6=19133
```

Operational checks:

- Confirm UDP, not only TCP, is allowed through host and cloud firewalls.
- Keep public test servers on a non-production world copy.
- Use `allow-list=true` for private servers.
- Keep operator grants in `permissions.json`, not only chat history or notes.

## Player Access Files

### `allowlist.json`

Use the server command surface or edit while stopped. Keep entries explicit:

```json
[
  {
    "name": "AdminPlayer",
    "xuid": "2533274800000000"
  }
]
```

### `permissions.json`

Use narrow grants:

```json
[
  {
    "permission": "operator",
    "xuid": "2533274800000000"
  }
]
```

Review operator entries during staff turnover and after incidents.

## Pack Deployment

For production BDS pack deployment:

1. Validate each add-on or resource pack has a unique `manifest.json` UUID set.
2. Put resource packs under `resource_packs/`.
3. Put behavior packs under `behavior_packs/`.
4. Attach packs to the world through `world_resource_packs.json` and
   `world_behavior_packs.json`.
5. Restart the server and confirm the client downloads the expected versions.

Avoid editing packs in place on production. Stage a versioned folder, then swap
world references after testing.

## Backup And Restore

Minimum backup set:

- `worlds/<world-name>/`
- `server.properties`
- `allowlist.json`
- `permissions.json`
- active `resource_packs/` and `behavior_packs/`

Restore workflow:

1. Stop BDS cleanly.
2. Move the broken live world aside.
3. Restore the selected backup into `worlds/`.
4. Restore matching pack folders and world pack references.
5. Start BDS and inspect the first boot log before opening access broadly.

## Incident Triage

For connection failures:

- Check BDS is listening and has not crashed.
- Check host firewall and cloud firewall UDP rules.
- Confirm client and server versions are compatible.
- Validate allowlist and operator files are valid JSON.

For pack failures:

- Confirm manifest UUIDs are unique.
- Confirm world pack reference versions match manifest versions.
- Remove one pack at a time in staging to isolate the failure.

For data loss:

- Stop the service immediately.
- Copy the current broken world before attempting repair.
- Restore from the newest known-good backup into a separate path first.

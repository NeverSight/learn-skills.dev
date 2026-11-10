---
name: minecraft-bedrock-addon-dev
description: "Develop Minecraft Bedrock Edition add-ons for 1.21.x with resource packs, behavior packs, manifest.json UUID/version management, Script API JavaScript or TypeScript using @minecraft/server, custom blocks/items/entities, packaging as .mcpack or .mcaddon, local hot-reload workflows, and BDS deployment notes. Use for official Bedrock add-on development, not Java plugins or general server administration."
---

# Minecraft Bedrock Add-On Development Skill

## Scope

Use this skill when the deliverable is a Bedrock resource pack, behavior pack,
Script API feature, or packaged `.mcpack` / `.mcaddon`.

### Routing Boundaries
- `Use when`: the task involves Bedrock `manifest.json`, behavior packs, resource packs, Script API, component JSON, or packaging/deploying add-ons.
- `Do not use when`: the task is Java plugin code (`minecraft-plugin-dev`), Java datapacks (`minecraft-datapack`), BDS operations without add-on development (`minecraft-bedrock-server-admin`), or Java-to-Bedrock resource conversion (`minecraft-resource-pack-conversion`).

## Add-On Shape

Typical add-on project:

```text
my-addon/
├── behavior_pack/
│   ├── manifest.json
│   ├── scripts/
│   │   └── main.js
│   ├── blocks/
│   ├── items/
│   ├── entities/
│   └── functions/
└── resource_pack/
    ├── manifest.json
    ├── textures/
    ├── models/
    ├── entity/
    ├── render_controllers/
    └── texts/
```

Use stable folder names during development, then package the contents of each
pack folder rather than nesting the pack folder inside the archive.

## Manifest Rules

Each pack needs unique UUIDs for `header.uuid` and every `modules[].uuid`.
When updating a deployed pack, increment the version array.

Behavior pack with Script API:

```json
{
  "format_version": 2,
  "header": {
    "name": "Example Behavior Pack",
    "description": "Server automation features",
    "uuid": "11111111-1111-4111-8111-111111111111",
    "version": [1, 0, 0],
    "min_engine_version": [1, 21, 0]
  },
  "modules": [
    {
      "type": "script",
      "language": "javascript",
      "entry": "scripts/main.js",
      "uuid": "22222222-2222-4222-8222-222222222222",
      "version": [1, 0, 0]
    }
  ],
  "dependencies": [
    {
      "module_name": "@minecraft/server",
      "version": "1.18.0"
    }
  ]
}
```

Resource pack:

```json
{
  "format_version": 2,
  "header": {
    "name": "Example Resource Pack",
    "description": "Textures and client assets",
    "uuid": "33333333-3333-4333-8333-333333333333",
    "version": [1, 0, 0],
    "min_engine_version": [1, 21, 0]
  },
  "modules": [
    {
      "type": "resources",
      "uuid": "44444444-4444-4444-8444-444444444444",
      "version": [1, 0, 0]
    }
  ]
}
```

## Script API Workflow

For JavaScript:

```javascript
import { world } from "@minecraft/server";

world.afterEvents.playerSpawn.subscribe((event) => {
  const player = event.player;
  player.sendMessage("Welcome to the server.");
});
```

Practical loop:

1. Develop in a local world or staging BDS world.
2. Keep script entrypoints small and move feature logic into modules.
3. Watch the content log for syntax and dependency errors.
4. Restart or reload the world after pack changes.
5. Package only after the staged world starts without content errors.

## Custom Content Checklist

For a custom item:

- Define behavior JSON under `items/`.
- Add texture entries in the resource pack.
- Add language text under `texts/en_US.lang`.
- Validate the item appears in a controlled test world.

For a custom entity:

- Define server entity behavior under `entities/`.
- Define client entity, geometry, render controller, and textures.
- Test spawn behavior, render state, sounds, and despawn edge cases.

## Packaging

Package a single pack as `.mcpack`:

```bash
cd behavior_pack
zip -r ../example-behavior.mcpack .
```

Package paired behavior/resource packs as `.mcaddon` by zipping the two packaged
packs or the two root pack folders according to the target import workflow.

## Deployment Notes

- For BDS, put tested packs into `behavior_packs/` and `resource_packs/`.
- Attach pack UUID/version pairs to the target world.
- Keep development packs out of production worlds unless the server is private
  and explicitly in testing mode.
- Document any required experiments or beta toggles before rollout.

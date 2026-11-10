---
name: minecraft-task-router
description: "Route and coordinate Minecraft 1.21.x requests that touch more than one skill, or where the right skill is unclear. Classifies the request, applies tie-breakers between overlapping skills, orders the work with safety gates (backup, staging, read-only first), hands each part to a specialist subagent with a fixed brief, and merges the results. Use for multi-step server, Bedrock/Java crossplay, content, plugin or mod, QA and release tasks. Skip it when exactly one skill clearly fits."
---

# Minecraft Task Router Skill

## Scope

This skill decides who does what. It does not contain Minecraft knowledge of its own. The specialist skills hold that.

### Routing Boundaries
- `Use when`: a request needs two or more specialist skills, the target platform is unclear (Java, Bedrock, or both), or the person asks which skill or agent to use.
- `Do not use when`: one skill clearly fits. Load that skill directly (for example `minecraft-plugin-dev` for a Paper plugin feature).
- `Do not use when`: you are already running inside a specialist subagent. Subagents do not route. Return `needs-other-skill` with a handoff note instead (see the return format).

## Step 1: Classify the request

Pick the smallest set of skills that covers the request. Most requests need one or two.

| Signal in the request | Skill |
|---|---|
| NeoForge or Fabric mod: blocks, items, entities, events, datagen | `minecraft-modding` |
| One codebase for both NeoForge and Fabric (Architectury) | `minecraft-multiloader` |
| Paper, Bukkit or Spigot plugin code | `minecraft-plugin-dev` |
| Bedrock add-on: behavior or resource packs, Script API, manifests, `.mcaddon` | `minecraft-bedrock-addon-dev` |
| Datapack files: functions, advancements, recipes, loot tables, tags | `minecraft-datapack` |
| Commands only: `/execute`, scoreboards, NBT, `tellraw`, RCON | `minecraft-commands-scripting` |
| Biomes, dimensions, structures, noise settings, surface rules | `minecraft-world-generation` |
| Java resource pack: models, textures, sounds, fonts, shaders | `minecraft-resource-pack` |
| Convert a Java pack to Bedrock `.mcpack` | `minecraft-resource-pack-conversion` |
| Bitmap art: pack icons, thumbnails, banners, concept textures | `minecraft-imagegen` |
| Java server setup, plugin sourcing, tuning, backups, proxy, incidents, folder or zip analysis | `minecraft-server-admin` |
| Bedrock Dedicated Server install, config, packs, worlds, backups | `minecraft-bedrock-server-admin` |
| Geyser or Floodgate, Bedrock players joining a Java server | `minecraft-crossplay-ops` |
| LuckPerms groups, tracks, contexts, audits | `minecraft-permissions-admin` |
| EssentialsX homes, warps, kits, economy, moderation | `minecraft-essentials-ops` |
| WorldEdit selections, schematics, brushes, rollback | `minecraft-worldedit-ops` |
| Unit tests, MockBukkit, GameTests | `minecraft-testing` |
| Bot playthrough of a live dev server, menu and NPC walkthrough | `minecraft-bot-qa` |
| GitHub Actions, Modrinth or CurseForge publishing, versioning | `minecraft-ci-release` |

## Step 2: Break ties

Some skills overlap. Use these rules in order.

1. Platform first. Java server work goes to `minecraft-server-admin`. Bedrock Dedicated Server work goes to `minecraft-bedrock-server-admin`. Bedrock players on a Java server is `minecraft-crossplay-ops`.
2. Writing versus operating. Code for a plugin or mod is a dev skill. Installing, configuring or running an existing plugin is an ops skill.
3. Worldgen versus datapack. Biome, dimension, structure and noise content goes to `minecraft-world-generation`. Everything else in a datapack stays in `minecraft-datapack`.
4. Commands versus datapack. A command snippet with no file tree is `minecraft-commands-scripting`. Once it lives in `.mcfunction` files it is `minecraft-datapack`.
5. Permissions versus EssentialsX. Role design and audits are `minecraft-permissions-admin`. EssentialsX-specific commands and config are `minecraft-essentials-ops`.
6. Tests versus pipelines. Writing the tests is `minecraft-testing`. Running them in CI and publishing is `minecraft-ci-release`.
7. Tests versus playthroughs. Code-level tests are `minecraft-testing`. Bots joining a running server are `minecraft-bot-qa`.
8. Art versus pack files. A bitmap is `minecraft-imagegen`. The pack structure that uses it is `minecraft-resource-pack`.

## Step 3: Order the work

Put the steps in this order, and skip any that do not apply.

1. Read-only analysis first (server folder report, config review, permission export).
2. Backup or snapshot before anything that changes a server, world or permission set.
3. Build or change on a staging or dev server. Never start on production.
4. Verify (tests, logs, a bot playthrough).
5. Roll out, with a rollback note.

Steps 2 and 5 on a live server need the person's go-ahead. Subagents prepare these steps. The main agent runs them only when the request asked for it.

## Step 4: Delegate to subagents

When the host supports subagents (Claude Code does), send each part of the plan to one specialist subagent. Otherwise do the same steps one after another in a single agent, loading one skill at a time.

| Subagent | Skills it loads | Typical work |
|---|---|---|
| `minecraft-java-ops` | `minecraft-server-admin`, `minecraft-permissions-admin`, `minecraft-essentials-ops`, `minecraft-worldedit-ops` | Java server setup, plugins, permissions, EssentialsX, WorldEdit |
| `minecraft-bedrock-ops` | `minecraft-bedrock-server-admin`, `minecraft-crossplay-ops` | Bedrock servers, Geyser and Floodgate |
| `minecraft-code-dev` | `minecraft-plugin-dev`, `minecraft-modding`, `minecraft-multiloader`, `minecraft-bedrock-addon-dev` | Plugin, mod and add-on code |
| `minecraft-content-author` | `minecraft-datapack`, `minecraft-commands-scripting`, `minecraft-world-generation`, `minecraft-resource-pack`, `minecraft-resource-pack-conversion`, `minecraft-imagegen` | Datapacks, commands, worldgen, packs, art |
| `minecraft-qa-release` | `minecraft-testing`, `minecraft-bot-qa`, `minecraft-ci-release` | Tests, bot playthroughs, CI and publishing |

Rules for delegation:

- The router runs in the main thread. Subagents are leaves and never start other subagents.
- Run subagents in parallel only when their work is independent. If one result feeds the next, run them in order.
- Give every subagent a full brief (see `references/delegation-brief.md`). A subagent does not see this conversation.
- Keep each brief to one outcome. Split big jobs, for example one brief for the permission model and another for the EssentialsX kits.
- A subagent proposes destructive or live changes unless the brief says the person approved them.

## Step 5: Merge and check

1. Read each return. Treat `blocked` and `needs-other-skill` as new work for the plan.
2. Look for conflicts between results, such as two agents editing the same config file or a permission node that one agent grants and another removes.
3. Check the combined result against the order in Step 3 (was there a backup, was it tested on staging).
4. Report to the person: what was done, what is waiting for their approval, and what is still open.

## Worked examples

Recipes for common multi-skill requests are in `references/recipes.md`.

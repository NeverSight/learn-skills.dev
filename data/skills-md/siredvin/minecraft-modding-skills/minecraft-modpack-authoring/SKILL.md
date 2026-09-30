---
name: minecraft-modpack-authoring
description: Author and test reproducible Minecraft Java modpacks.
license: MIT
compatibility: Minecraft Java Edition modpacks using Packwiz with Fabric, Quilt, Forge, or NeoForge; exact commands, file formats, KubeJS APIs, loader behavior, and Java requirements are version-sensitive.
metadata:
  author: "SirEdvin"
  version: "1.1.0"
---

# Minecraft Modpack Authoring

Treat pack source as a reproducible project, not a copied launcher instance.
This is pack composition/configuration work; compiled mods and Java addons have
separate build and registration lifecycles. A Java mod repository without a pack
manifest is not a reason to initialize Packwiz in its root.

## First checks

1. Locate `pack.toml`, the intended source root and `.packwizignore`; inspect Git
   status before any command that refreshes or rewrites metadata.
2. Read exact Minecraft, loader, pack, Java, Packwiz, KubeJS and integration
   versions. Identify authored configs/scripts/quests/assets versus runtime state.
3. Define new-world, existing-world, client and server impact. Back up world copies
   before migrations; do not operate on a live instance during a source audit.
4. Resolve exact project/file IDs, required dependencies, hashes, redistribution
   rights and physical sides. Unknown side compatibility is a release blocker,
   not permission to ship to both sides and hope.

## Work at the right layer

- Packwiz owns file metadata and index hashes; refresh rather than hand-editing
  `index.toml`. Git owns reviewable source. Do not run bulk updates in validation.
- KubeJS registry definitions require restart; recipes/tags use the supported
  datapack reload. Script-only reload is not equivalent to firing content events.
- Loader config semantics are versioned: distinguish common/client, authoritative
  server configs, defaults for missing files, and existing-world overrides.
- Keep stable recipe, registry and quest IDs. Match recipe schemas, datapack and
  resource-pack formats to the exact Minecraft line.
- Use exact dependency versions and immutable hosting/checksums for release
  inputs. A moving pack URL plus a pinned bootstrap JAR is not a frozen release.

## Progressive references

- [End-to-end authoring workflow](references/authoring-workflow.md): create/import,
  update, configure, migrate, export and release checklist.
- [Packwiz commands](references/packwiz-workflows.md): CLI contracts, source pin,
  ignore rules, installers and CI.
- [Content and testing](references/modpack-content-and-testing.md): loader config,
  scripts, datapacks, quests, worlds, client/server and upgrade matrix.
- [Pinned example and reproducibility checks](references/reproducibility-audit.md):
  source evidence, export self-inclusion and installer version boundaries.

## Acceptance

Refresh twice and verify no unintended second diff. Export only requested formats;
inspect archives and hashes. Install in clean client and dedicated-server test
locations, launch both, join the server, exercise changed gameplay, and test a
copied existing world when upgrades are promised. TOML parsing and export success
are not launch, compatibility, redistribution or gameplay proof. Publish only
when explicitly requested and after reviewing artifacts; never ship credentials,
world/player data, local options, logs or caches accidentally.

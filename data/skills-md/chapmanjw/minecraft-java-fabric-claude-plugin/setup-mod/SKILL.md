---
name: setup-mod
description: >-
  Step 2 of 4 of the Minecraft Java MCP setup. Download the minecraft-java MCP
  mod jar and its matching Fabric API jar and install both into the Minecraft
  mods folder. Use when the user has Minecraft Java with the Fabric loader
  ready and needs the MCP mod and Fabric API installed.
---

# Install the MCP mod + Fabric API (Step 2 of 4)

This is **Phase 2** of the four-phase Minecraft Java MCP setup. It assumes
Phase 1 (`setup-fabric`) is done: Fabric is installed and the `mods/` folder
exists. You should have, written down:

- the chosen **Minecraft version** (e.g. `26.2`);
- the **mods-folder path** (single-player) or the **`<server>` root** with its
  `mods/` folder (dedicated server).

If either is missing, get it before continuing. Work interactively — confirm
each download before moving on.

## What you're installing

The MCP server is delivered as a **Fabric mod**. It needs exactly two jars in
`mods/`, both matching the same Minecraft version:

1. **The MCP mod** — `minecraft-fabric-mcp-<modver>+<mc-version>.jar`.
2. **Fabric API** — the mod's only dependency.

> **Match the Minecraft version on both jars.** A jar built for `26.1.2` will
> not load on `1.21.11`, and vice versa. The version suffix after the `+` must
> equal the version chosen in Phase 1.

## Step 1 — Download the MCP mod jar

From the mod's releases:
<https://github.com/chapmanjw/minecraft-java-fabric-mcp-server/releases>

Pick the asset whose filename ends in **`+<your-mc-version>.jar`** — e.g.
`minecraft-fabric-mcp-1.0.1+26.2.jar` for Minecraft 26.2. Pin to a specific
release tag rather than tracking `latest`, so the version stays in lockstep
with Minecraft and Fabric API.

## Step 2 — Download the matching Fabric API jar

From Modrinth: <https://modrinth.com/mod/fabric-api/versions>

Filter by your Minecraft version and download the Fabric API jar for it — e.g.
`fabric-api-0.155.2+26.2.jar`. Its Minecraft version must match exactly.

> The mod jar declares an EXACT `depends.minecraft`, so a jar built for one
> Minecraft version is refused at load on any other — you get a clear loader
> error rather than a crash later. Do not mix versions across the two jars.

## Step 3 — Put both jars in `mods/`

Copy **both** jars into the `mods/` folder from Phase 1.

**Single-player** — the platform path:

| OS | Path |
| -- | ---- |
| Windows | `%appdata%\.minecraft\mods\` |
| macOS | `~/Library/Application Support/minecraft/mods/` |
| Linux | `~/.minecraft/mods/` |

**Dedicated server** — `<server>/mods/`:

```sh
mkdir -p /opt/fabric-mcp/mods
# copy both jars into it
```

The folder should now contain exactly these two jars (plus any other mods the
user already runs):

```
mods/
├── fabric-api-0.155.2+26.2.jar
└── minecraft-fabric-mcp-1.0.1+26.2.jar
```

Confirm with the user that both files are present and that the version suffixes
match each other and the Minecraft version.

## Step 4 — Quick load check (optional but recommended)

If the user wants to confirm the mod loads before configuring it:

- **Single-player:** launch the Fabric profile and load any world.
- **Dedicated server:** `java -Xmx2G -jar fabric-server-launch.jar nogui`.

In the log, look for the mod's startup lines:

```
[minecraft_fabric_mcp] MCP server config loaded from .../config/minecraft_fabric_mcp/config.json
[minecraft_fabric_mcp] Registered N MCP tools (M skipped due to version/module constraints)
[minecraft_fabric_mcp] MCP server listening at http://127.0.0.1:8765 (...)
```

Seeing the `listening` line means the mod loaded and the embedded MCP server
started. (Phase 3 covers configuring it and verifying `/healthz`.) If the game
crashes on load, the usual cause is a version mismatch between the mod jar, the
Fabric API jar, and Minecraft — re-check the `+<version>` suffixes.

## Wrap up

Confirm with the user:

- [ ] MCP mod jar for the chosen Minecraft version is in `mods/`.
- [ ] Matching Fabric API jar is in `mods/`.
- [ ] Both version suffixes match each other and the Minecraft version.
- [ ] (Optional) The mod loaded and logged the MCP `listening` line.

Hand off: Phase 2 is done — the mod is installed. The next step configures the
MCP server (`config.json`), launches it, and verifies it's reachable. Offer to
continue with the **`setup-server`** skill now.

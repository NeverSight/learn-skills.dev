---
name: setup-fabric
description: >-
  Step 1 of 4 of the Minecraft Java MCP setup. Install Minecraft Java Edition
  with the Fabric loader — either a single-player client or a headless
  dedicated server — as the foundation the MCP mod runs inside. Use when the
  user wants to set up Minecraft Java for AI/MCP control from scratch, or asks
  how to get Fabric running so Claude can build in their world.
---

# Install Minecraft Java + Fabric (Step 1 of 4)

You are guiding the user through the **first** of four setup phases. Work
interactively: do one thing, confirm it worked, then move on. Do not dump the
whole procedure at once.

## The big picture — explain this first

The user is building a stack that lets Claude read and change a live Minecraft
Java Edition world. Unlike a separate server process, the MCP server is **a
Fabric mod that runs inside Minecraft itself**. There are four setup phases,
one per skill, run in order:

| Phase | Skill | What it does |
| ----- | ----- | ------------ |
| 1 | `setup-fabric` (this one) | Minecraft Java Edition with the Fabric loader. |
| 2 | `setup-mod` | The MCP mod jar + its matching Fabric API jar in `mods/`. |
| 3 | `setup-server` | The mod's `config.json`, launched and verified on `/healthz`. |
| 4 | `setup-connect` | Register the MCP server with Claude so the Java tools appear. |

Tell the user this is Phase 1, and that each phase ends by handing off to the
next. Budget ~10 minutes for a single-player setup, ~20–30 for a dedicated
server.

> **Pin your versions — say this out loud.** The mod ships a separate jar per
> Minecraft version, built against that version's Fabric API. A Minecraft or
> Fabric update can break the modding surface the mod depends on. Pick a
> supported Minecraft version, pin it, disable auto-update for that profile,
> and upgrade Minecraft, the Fabric API jar, and the mod jar together.

## Gather context

Ask the user, before downloading anything:

1. **Single-player or dedicated server?**
   - **Single-player (recommended default):** Claude edits the world you play
     in, on your own machine. Loopback only, no token, no firewall changes.
     ~10 minutes.
   - **Dedicated server:** a headless Minecraft server (for friends, or to keep
     the MCP endpoint up 24/7). LAN/remote access with a bearer token.
   Branch the rest of this skill on their answer.
2. **Which Minecraft version?** The mod supports **1.21.11**, **26.1.1**,
   **26.1.2**, and **26.2**. Default to the newest the user is comfortable with
   (26.2). **Record the exact version** — it must match the mod jar and Fabric
   API jar in Phase 2. The mod jar declares an EXACT Minecraft dependency, so a
   mismatch is refused at load with a clear message rather than failing later.
3. **(Dedicated server only) What OS and where?** Linux or Windows; same
   machine as Claude, LAN box, or cloud VM. The host needs a JDK: **Java 21**
   for 1.21.11, **Java 25** for 26.1.x. (Single-player uses the launcher's
   bundled runtime — no separate JDK needed.) The connect step (Phase 4) cares
   where it runs, so note their answer.

---

## Single-player branch

### Step 1 — Install the Fabric loader

Send the user to the official installer: <https://fabricmc.net/use/installer/>

- **Windows:** download and double-click the `.exe`.
- **macOS / Linux:** `java -jar fabric-installer-*.jar`.

In the installer, pick the **Client** tab, select the Minecraft version chosen
above, leave the default install location, and click **Install**.

### Step 2 — Create the profile and the mods folder

Open the Minecraft Launcher. A new **Fabric Loader** profile should appear.
Launch it once and then exit the game — this first run creates the
`.minecraft/mods/` folder Phase 2 drops jars into. The mods folder lives at:

| OS | Path |
| -- | ---- |
| Windows | `%appdata%\.minecraft\mods\` |
| macOS | `~/Library/Application Support/minecraft/mods/` |
| Linux | `~/.minecraft/mods/` |

Confirm with the user that the Fabric profile launched and the `mods/` folder
now exists. **Record the mods-folder path** — Phase 2 needs it.

---

## Dedicated server branch

### Step 1 — Install the Fabric dedicated server

Download the **Server** installer from <https://fabricmc.net/use/server/> into a
dedicated directory, then run it (substitute the chosen Minecraft version):

```sh
mkdir -p /opt/fabric-mcp
cd /opt/fabric-mcp
java -jar fabric-server-installer-*.jar server -mcversion 26.1.2 -downloadMinecraft
```

This produces `fabric-server-launch.jar` and downloads the Minecraft server
jar. On Windows, use a stable path with no spaces (e.g. `C:\fabric-mcp`); avoid
`Program Files` and OneDrive-synced folders. Use this folder as `<server>` for
the rest of setup and **record its absolute path**.

### Step 2 — First run + EULA

Run it once to generate `server.properties` and `eula.txt`, then stop it
(`Ctrl+C`):

```sh
java -Xmx2G -jar fabric-server-launch.jar nogui
```

Open `eula.txt` and change `eula=false` to `eula=true`.

### Step 3 — Confirm command access

For Claude's command-backed tools to work, the server must allow operator
commands. In `server.properties`, confirm sensible defaults (e.g.
`gamemode=creative` so agents can build freely if that suits the user). The MCP
mod runs tool calls as the console, which has full command permission — no
per-player op is required for the MCP tools themselves.

---

## Wrap up

Confirm with the user (the relevant set for their branch):

- [ ] Minecraft version chosen and **recorded**; auto-update not relied on.
- [ ] **Single-player:** Fabric Loader profile created; launched once;
      `mods/` folder exists and its path is recorded.
- [ ] **Dedicated server:** Fabric server installed; ran once; `eula=true`;
      server root path recorded; correct JDK present (21 for 1.21.11, 25 for
      26.1.x).

Then hand off: tell the user Phase 1 is done and the next step installs the MCP
mod and its Fabric API dependency. Offer to continue with the
**`setup-mod`** skill now.

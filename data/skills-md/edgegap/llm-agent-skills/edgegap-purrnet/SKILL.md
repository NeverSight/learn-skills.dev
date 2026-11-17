---
name: edgegap-purrnet
description: 'PurrNet + Edgegap: take a Unity game built on PurrNet to dedicated servers and matchmaking, end to end. Load this before using any Edgegap MCP tool on a PurrNet project (dev.purrnet.purrnet, NetworkManager start flags, UDPTransport, WebTransport, ParrelSync clones). It has PurrNet-ready C# templates verified on Edgegap that add themselves at runtime without editing scenes (server start and self-stop, connect panel with direct and matchmaker modes, settings asset), port 7777 UDP app version, Dockerfile, matchmaker config, and fixes for PurrNet pitfalls: auto start flags, the async StartClient, ObserversRpc that never runs on a dedicated server. Use when a PurrNet dev wants online play: "host my PurrNet game", "nobody should host", "works with a host but not online", "Find Match button", or is debugging PurrNet deployments, ports or matchmaking on Edgegap. Other Unity netcodes: edgegap-unity (NGO, Mirror) or edgegap-fishnet.'
metadata:
  version: "0.3.5"
---

# Edgegap for PurrNet: dedicated servers + matchmaking

Goal: a player clicks **Find Match** (or connects to an address while testing), Edgegap runs a headless PurrNet server near the players, every client connects, and the server stops its own deployment once the match is empty. Done means that loop works with real builds, not that the code compiles.

This path was run end to end on Edgegap with [edgegap/netcode-game-sample-unity-purrnet-incremental](https://github.com/edgegap/netcode-game-sample-unity-purrnet-incremental), a fork of PurrNet's Incremental sample (Unity 6000.3.11f1, PurrNet `dev`, `UDPTransport`, SDK 3.5.5): two desktop clients played on the same server, both by direct connection and through the matchmaker (matched in about 35 s), and the server stopped itself each time. The templates in `assets/unity/` are the files from that run; `EDGEGAP.md` in that repo is a working reference for the developer.

Use **dedicated (authoritative) servers**, not a player host, unless the developer explicitly wants host/client. If they do, keep the game host/client and route it through a relay deployed on Edgegap: [edgegap/server-sample-lightnet-relay](https://github.com/edgegap/server-sample-lightnet-relay) has the relay server and a transport for Mirror, FishNet, PurrNet and NGO, for desktop and Unity WebGL (WebGL over `wss://`); Edgegap's managed relays: `edgegap-relays`.

## How to work

- **Be the engineer.** Inspect the project, write the code, run Unity batch builds, Docker and the Edgegap MCP tools, read the logs. Hand the developer only Editor clicks, dashboard steps, secrets and playtesting.
- **Touch the game as little as possible.** The templates add themselves at startup from `Assets/Edgegap/`, so scenes and prefabs stay unchanged. That keeps upstream syncs and the developer's own scene work conflict-free.
- **One layer at a time**: local → Docker → direct Edgegap deploy → matchmaker, each with a check.
- **Secrets.** The Edgegap API token and registry token never go into files, git, the client or chat. The matchmaker Auth Token is client-safe.
- **Money.** Tag test deployments and stop the ones you start. Free tier runs one deployment at a time.
- Track the phases as a todo list.

## Phase 0: Understand the project

Read, don't ask:
- `ProjectSettings/ProjectVersion.txt` (Unity 6 tested; the SDK needs 2021.3+, and before 2022.3 it must be 3.5.6 or newer: older versions break every matchmaker ticket there, `references/troubleshooting.md` §4).
- `Packages/manifest.json`: `dev.purrnet.purrnet` (git URL and branch), any `com.edgegap.*` package. With `com.edgegap.unity-servers-plugin` installed, PurrNet's transports also auto-configure their port on Edgegap (`references/purrnet.md` §6).
- The scene with PurrNet's `NetworkManager`: its transport (`UDPTransport` = UDP, `WebTransport` = WebSocket, `CompositeTransport`), port (`serverPort`, 5000 on UDP by default; the templates replace it with 7777 at runtime), network rules, and **Start Server Flags / Start Client Flags**.
- How the game connects today: host in the Editor plus a ParrelSync clone is PurrNet's default. Grep `StartServer`, `StartClient`, `StartHost`, `isHost`.
- Server-side logic that relies on a host's local client: `[ObserversRpc]` and `[TargetRpc]` methods that set up server state (`references/purrnet.md` §3). This is the bug that silently breaks dedicated servers.
- Targets: desktop clients use UDP; WebGL needs `WebTransport` (not verified on Edgegap yet).

Then ask, in one message, only what you couldn't infer: players per match, platforms, Edgegap account and Docker. Offer defaults.

## Phase 1: Make the game dedicated-server ready

Read `references/purrnet.md`.
1. Add `"com.edgegap.unity-servers-plugin": "https://github.com/edgegap/buildtool-unity-plugin.git"` (the Edgegap Unity plugin, Editor only: build, image, push, deploy from **Tools → Edgegap Server Hosting**; no `#tag`) and the SDK, `"com.edgegap.unity-sdk": "https://github.com/edgegap/sdk-unity-sessions-matchmaker-server-browser.git"`, to `Packages/manifest.json`, on every Unity version. No `#tag`: that installs the latest SDK (3.5.6+). Never pin an exact version. Nothing to embed or patch; if the project already has an embedded, hand-patched SDK (`Packages/com.edgegap.unity-sdk`), delete it and use the git package.
2. Copy `assets/unity/*.cs`, `EdgegapSettings.cs.meta` and `link.xml` to `Assets/Edgegap/`, and `assets/unity/Resources/EdgegapSettings.asset` to `Assets/Edgegap/Resources/`. Copy the `.meta` too: the asset finds its script by that GUID. If the game's scripts live in an asmdef, reference `Edgegap.SDK` and PurrNet's runtime asmdef from it.
3. Keep port 7777: `ListenPort` / `DirectPort` on the settings asset default to it and are applied to `UDPTransport.serverPort` at runtime, so PurrNet's default 5000 in the scene doesn't matter. Use 7777 on the app version too. Change both only if the game needs another port.
4. Fix server-only logic that assumed a host (`references/purrnet.md` §3): `[ObserversRpc(runLocally: true, ...)]` where the server must run the RPC body too, players spawned for remote clients, client-only code guarded.

What the templates do: `EdgegapBootstrap` runs before the first scene loads. In builds it calls `NetworkManager.DisableFlags()` (PurrNet's auto start off) and adds `EdgegapServerLifecycle` (server builds: starts the server on `0.0.0.0:<ListenPort>`, self-stops on Edgegap) or `EdgegapConnectPanel` + `EdgegapMatchmakingClient` (clients). The Editor keeps PurrNet's host + clone flow unless **Apply In Editor** is ticked.

✅ Check: the Linux server (or a `-batchmode` instance) logs `Edgegap Server | Starting server on 0.0.0.0:7777.`, two client builds connect to `127.0.0.1:7777`, the server logs `Edgegap Server | 2 player(s) connected.`, and the game's server-side content exists (spawned objects, world state).

## Phase 2: Connect to Edgegap

Edgegap account, Docker running, Unity **Linux Build Support (Mono)** + **Linux Dedicated Server Build Support**. Edgegap MCP connected (`references/deploy.md` §1).

✅ Check: `edgegap_list_apps` succeeds.

## Phase 3: Build, test and upload with the plugin

Copy `assets/docker/.dockerignore` to the project root (the plugin's Docker context is the project root; without it Docker sends the whole project). Then the developer opens **Tools → Edgegap Server Hosting** and goes top to bottom:
1. **Sign in with Edgegap** → **Build server** → **Containerize with Docker** (Image Name; empty tag = UTC timestamp).
2. **Test Your Server Locally**: Optional Docker Run Parameters `-p 7777:7777/udp` → **Deploy local container**; connect a client to `127.0.0.1:7777`; **Terminate**.
3. **Upload image and Create app version** (Application Name). It pushes and opens the dashboard version form: replace the default port with `gameport` / `7777` / **UDP**, make sure the registry login is set (a Registry Profile, or the Container Registry username and token), save.

No Editor (CI, or you run it): the same steps from the command line in `references/deploy.md` §2-4.

✅ Check: `edgegap_list_app_versions` shows the version with `registry_credentials_set: true` and the `gameport` port.

## Phase 4: Direct deploy

1. **Deploy to cloud** in the plugin, or `edgegap_deploy` near the developer → `edgegap_wait_for_deployment` → `edgegap_get_deployment_logs`.
2. Two clients connect with the panel to `<fqdn>:<external port>`, or `Game.exe -edgegapAddress <fqdn> -edgegapPort <external> -edgegapConnect`.
3. Close the clients: the server stops itself 30 s later (or `edgegap_stop_deployment`).

✅ Check: a client played on the Edgegap server. Don't build the matchmaker on an unproven server.

## Phase 5: Matchmaker

Read `references/matchmaker.md`.
1. `assets/matchmaker/casual.json` (2-4 players, no expansion stage: `min_team_size` below `max_team_size` already allows partial matches; keep `ticket_expiration_period` at `30s` so they come quickly) with the app name and version, or `edgegap_build_matchmaker_config`. Save as `matchmaker-config.json` in the project root. If other `matchmaker-config.json` files exist on the machine, give the developer the full path to upload.
2. Dashboard: Create Matchmaker → upload → Create and Start → copy **API URL** and **Auth Token**.
3. `GET <API URL>/monitor` with the token answers.

## Phase 6: Client integration

1. On `Assets/Edgegap/Resources/EdgegapSettings.asset`: **Use Edgegap Matchmaker** on, **Matchmaker Url**, **Matchmaker Auth Token**, `Profile`. Or pass `-edgegapMatchmaker true -edgegapMatchmakerUrl <url> -edgegapAuthToken <token>` to test builds.
2. The connect panel shows Find Match / Cancel and the status. To use the game's own menu instead, call `EdgegapMatchmakingClient.FindMatch()` / `CancelMatchmaking()` and read `Status`, and remove `EdgegapConnectPanel` from the bootstrap.
3. Server changed? Rebuild → new tag → new app version → matchmaker **Stop → Edit** `application.version` **→ Start**.

## Phase 7: End-to-end test and hand-off

1. `edgegap_list_deployments`: nothing of yours left running.
2. Client builds: File → Build Profiles, or `assets/unity/Editor/EdgegapClientBuild.cs` (`-executeMethod EdgegapClientBuild.Build -edgegapClientTarget win64|mac|linux` → `Builds/Client/<target>`).
3. Two clients, **Find Match** in both (or `-edgegapFindMatch` on the command line): searching → match found → joining → connected, both on one server. Test with two: a lone ticket may wait until it nearly expires (30 s with the template).
4. Server logs `2 matched player(s)` and `2 player(s) connected.` Close both → `Stopping deployment: all players left` → the deployment disappears.
5. Debug with `references/troubleshooting.md`.

Hand-off: what was built and where, app/version/matchmaker names, how to ship a new build, free-tier caveats, and next steps (match end via `SelfStop`, ticket-ID validation with `MM_TICKET_IDS`, backfill, stricter network rules for competitive games, a production matchmaker tier).

## Reference files

- `references/purrnet.md`: start flags and the bootstrap, transports and ports, host-only logic (ObserversRpc `runLocally`), the async `StartClient`, scene reloads, PurrNet's own Edgegap auto-setup, network rules, WebGL.
- `references/deploy.md`: MCP connection, server and client builds, Docker and registry, app version for UDP 7777, direct deploy, command-line test flags.
- `references/matchmaker.md`: config, dashboard steps, ticket contract, injected variables, why partial matches need no expansion stage, lone tickets.
- `references/troubleshooting.md`: symptom → fix tables.
- `assets/unity/`: `EdgegapBootstrap`, `EdgegapSettings` (+ `.meta`, `Resources/EdgegapSettings.asset`), `EdgegapServerLifecycle`, `EdgegapConnectPanel`, `EdgegapMatchmakingClient`, DTOs, `link.xml`, `Editor/EdgegapPluginBuild` (command-line plugin build), `Editor/EdgegapClientBuild` (test clients). `assets/docker/.dockerignore` (the Dockerfile is the plugin's), `assets/matchmaker/`.

Related skills in this pack, if installed: `edgegap-unity` (NGO, Mirror), `edgegap-fishnet`, `edgegap-deployments-api` for a studio's own backend or matchmaker, `edgegap-launch` before going live.

Sources of truth: https://purrnet.gitbook.io/docs, https://docs.edgegap.com/unity, https://github.com/edgegap/sdk-unity-sessions-matchmaker-server-browser, and the sample https://github.com/edgegap/netcode-game-sample-unity-purrnet-incremental.

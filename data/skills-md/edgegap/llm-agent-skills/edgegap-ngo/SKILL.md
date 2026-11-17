---
name: edgegap-ngo
description: 'Netcode for GameObjects (NGO) + Edgegap: take a Unity game built on NGO to dedicated servers and matchmaking, end to end. Load this before using any Edgegap MCP tool on an NGO project (com.unity.netcode.gameobjects, NetworkManager, UnityTransport, StartHost, ConnectionManager, Boss Room). It has NGO C# templates verified on Edgegap, no scene edits (server start and self-stop, Find Match panel, settings asset), a Boss Room adapter, the Edgegap Unity plugin for build, image, push and deploy, port 7777 UDP app version, matchmaker config, and fixes for NGO pitfalls: host-only logic, connection payloads and approval, UnityTransport needing an IP, client-only code on the server, Relay leftovers. Use when an NGO dev wants online play: "host my NGO game", "nobody should host", "replace Unity Relay or Multiplay", "Boss Room on Edgegap", "Find Match button", or debugs NGO deployments, ports or matchmaking. Mirror or WebGL-first games: edgegap-unity. FishNet: edgegap-fishnet. PurrNet: edgegap-purrnet.'
metadata:
  version: "0.2.5"
---

# Edgegap for Netcode for GameObjects: dedicated servers + matchmaking

Goal: a player clicks **Find Match** (or joins an address while testing), Edgegap runs a headless NGO server near the players, every client connects, and the server stops its own deployment once the match is empty. Done means that loop works with real builds, not that the code compiles.

Verified end to end on Edgegap with [edgegap/netcode-game-sample-unity-ngo-bossroom](https://github.com/edgegap/netcode-game-sample-unity-ngo-bossroom) (Boss Room, Unity 6000.0.54f1, NGO 1.13.0, UnityTransport 2.5.2 UDP, SDK 3.5.6, Edgegap Unity plugin 3.2.1): two Windows clients in the dungeon on one Edgegap server, by direct connection and through the matchmaker, and the server stopped itself each time. Its `EDGEGAP.md` is the developer-facing reference. `assets/unity/` holds generic plain-NGO adapters (server start and direct connect tested locally, matchmaker adapter compile-only); `assets/unity/Examples/BossRoom/` the verified Boss Room adapter.

Use **dedicated (authoritative) servers**, not a player host, unless the developer explicitly wants host/client. If they do, keep the game host/client and route it through a relay deployed on Edgegap: [edgegap/server-sample-lightnet-relay](https://github.com/edgegap/server-sample-lightnet-relay) has the relay server and a transport for Mirror, FishNet, PurrNet and NGO, for desktop and Unity WebGL (WebGL over `wss://`); Edgegap's managed relays: `edgegap-relays`.

## How to work

- **You write the code and run the MCP; the plugin builds.** Server build, image, push and app version go through the Edgegap Unity plugin's window (the developer clicks): it handles Unity versions, Addressables, Apple Silicon and the registry login. If you can launch client builds, run the two-client tests yourself with the command-line flags (`references/deploy.md` §6).
- **Touch the game as little as possible.** The templates add themselves at startup from `Assets/Edgegap/`, so scenes and prefabs stay unchanged. That keeps upstream syncs and the developer's scene work conflict-free.
- **One layer at a time**: local → Docker → direct Edgegap deploy → matchmaker, each with a check.
- **Secrets.** The Edgegap API token and registry token never go into files, git, the client or chat. The matchmaker Auth Token is client-safe.
- **Money.** Tag test deployments and stop the ones you start. Free tier runs one deployment at a time.

## Phase 0: Understand the project

Read, don't ask:
- `ProjectSettings/ProjectVersion.txt` (the SDK needs 2021.3+; use SDK 3.5.6+ before Unity 2022.3).
- `Packages/manifest.json`: `com.unity.netcode.gameobjects` version, `com.unity.transport`, `com.unity.services.*` (Relay, Lobby, Matchmaker, Multiplay), any `com.edgegap.*`. Keeping **Unity Matchmaker** and moving off Multiplay: Unity's official `EdgegapAllocator` Cloud Code module ([matchmaker-hosting-providers](https://github.com/Unity-Technologies/matchmaker-hosting-providers/tree/main/modules/EdgegapAllocator)) starts the Edgegap server for each match (see `edgegap-matchmaking`, third-party matchmakers; not run by this pack); this skill still does the server build, image and app version.
- The scene with the `NetworkManager`: transport (`UnityTransport`, its port and `ConnectTimeoutMS`/`MaxConnectAttempts`), Player Prefab, `ConnectionApproval`.
- How the game connects: grep `StartHost`, `StartServer`, `StartClient`, `SetConnectionData`, `SetRelayServerData`, `ConnectionData`, `IsHost`. A `ConnectionManager` state machine (Boss Room and projects derived from it) changes the integration (`references/ngo.md` §4).
- Code that won't compile or run without UGS: a UGS Matchmaker client without `com.unity.services.matchmaker`, Relay-only connect paths.
- Targets: desktop clients use UDP. WebGL needs WebSockets (`references/ngo.md` §7, not verified).

Then ask, in one message, only what you couldn't infer: players per match, platforms, Edgegap account and Docker. Offer defaults. Building without the Editor (CI, or you) needs `docker login registry.edgegap.com` and the registry Username and Token (Container Registry page): ask now, not mid-deploy.

## Phase 1: Make the game dedicated-server ready

Read `references/ngo.md`.
1. In `Packages/manifest.json`, without `#tag` (latest; never pin): `"com.edgegap.unity-servers-plugin": "https://github.com/edgegap/buildtool-unity-plugin.git"` (the Editor plugin: build, image, push, deploy) and `"com.edgegap.unity-sdk": "https://github.com/edgegap/sdk-unity-sessions-matchmaker-server-browser.git"` (runtime SDK, 3.5.6+).
2. Copy `assets/unity/*.cs`, `EdgegapSettings.cs.meta` and `link.xml` to `Assets/Edgegap/`, and `assets/unity/Resources/EdgegapSettings.asset` to `Assets/Edgegap/Resources/`. Copy the `.meta` too: the asset finds its script by that GUID. Don't copy `Examples/`. If the game's scripts live in an asmdef the templates must call, reference it from an asmdef in `Assets/Edgegap/` (with `Edgegap.SDK`, `Unity.Netcode.Runtime`, `Unity.Networking.Transport`), or keep the templates in `Assembly-CSharp`, which sees auto-referenced asmdefs.
3. **Plain NGO** (the game calls `NetworkManager` directly): keep `AutoStartServer` on; the lifecycle starts the server on `0.0.0.0` and the Edgegap internal port. Remove any headless `StartHost` the game does. **Own connection flow** (`ConnectionManager`, payloads, approval): `AutoStartServer` off, start the server through the game's flow, and swap in the Boss Room adapter (`references/ngo.md` §4).
4. Fix host-only assumptions (`references/ngo.md` §2): `StartServer` not `StartHost`, no local player on the server, no host payload, matching build types, no Relay on the dedicated path.
5. Set `ListenPort` on the settings asset if the game doesn't use 7777, and `MenuSceneName` to the main menu scene.

✅ Check: the Linux server (or a `-batchmode` instance) logs `Edgegap Server | Starting server on 0.0.0.0:7777.`, two client builds connect to `127.0.0.1:7777` (the game's own connect UI or `-edgegapConnect`), the server logs `Edgegap Server | 2 player(s) connected.`, and both players see each other in the game.

## Phase 2: Connect to Edgegap

Edgegap account, Docker running, Unity **Linux Build Support (Mono)** + **Linux Dedicated Server Build Support**. Edgegap MCP connected (`references/deploy.md` §1).

✅ Check: `edgegap_list_apps` succeeds.

## Phase 3: Build, test and upload with the plugin

Copy `assets/docker/.dockerignore` to the project root (the plugin's Docker context is the project root; without it Docker sends the whole project). Then the developer opens **Tools → Edgegap Server Hosting** and goes top to bottom:
1. **Sign in with Edgegap** → **Build server** → **Containerize with Docker** (Image Name; empty tag = UTC timestamp).
2. **Test Your Server Locally**: Optional Docker Run Parameters `-p 7777:7777/udp` → **Deploy local container**; two clients on `127.0.0.1:7777`; **Terminate**.
3. **Upload image and Create app version** (Application Name). It pushes and opens the dashboard version form: replace the default port with `gameport` / `7777` / **UDP**, make sure the registry login is set (a Registry Profile, or the Container Registry username and token), save.

No Editor (CI, or you run it): the same steps from the command line in `references/deploy.md` §2-4.

✅ Check: `edgegap_list_app_versions` shows the version with `registry_credentials_set: true` and `gameport` 7777/UDP.

## Phase 4: Direct deploy

1. **Deploy to cloud** in the plugin, or `edgegap_deploy` near the developer → `edgegap_wait_for_deployment` → `edgegap_get_deployment_logs` (`references/deploy.md` §5).
2. Two clients connect to `<public_ip>:<external port>` (UnityTransport needs the IP, not the fqdn).
3. Close both: the server stops itself 30 s later (or `edgegap_stop_deployment`).

✅ Check: both played on the Edgegap server and the server logged the player count. Don't add the matchmaker on an unproven server.

## Phase 5: Matchmaker

Read `references/matchmaker.md`.
1. `assets/matchmaker/casual.json` with the app name and version, or `edgegap_build_matchmaker_config`. Keep `ticket_expiration_period` at `30s` and **no expansion stage**: `min_team_size` < `max_team_size` already gives partial matches, and expansions cost the matchmaker a lot of performance. Save as `matchmaker-config.json` in the project root and give the developer its full path to upload.
2. Dashboard: Create Matchmaker → upload → Create and Start → copy **API URL** and **Auth Token**.
3. `GET <API URL>/monitor` with the token answers `HEALTHY`.

## Phase 6: Client integration

1. On `Assets/Edgegap/Resources/EdgegapSettings.asset`: **Use Edgegap Matchmaker** on, **Matchmaker Url**, **Matchmaker Auth Token**, `Profile`. Or pass `-edgegapMatchmaker true -edgegapMatchmakerUrl <url> -edgegapAuthToken <token>` to test builds.
2. The Find Match panel shows on `MenuSceneName`. To use the game's own menu instead, call `EdgegapMatchmakingClient.FindMatch()` / `CancelMatchmaking()`, read `Status`, and set `ShowGUI = false`.
3. Server changed? Plugin **Rebuild from Source** → version form (`gameport` port) → matchmaker **Stop → Edit** `application.version` **→ Start**.

## Phase 7: End-to-end test and hand-off

1. `edgegap_list_deployments`: nothing of yours left running.
2. Client builds (`references/deploy.md` §2).
3. Two clients, **Find Match** in both (or `-edgegapFindMatch`): searching → match found → joining → connected, both on one server. Two copies on one machine may need a per-instance player id (`references/ngo.md` §6).
4. Server logs `2 matched player(s)` and `2 player(s) connected.` Close both → `Stopping deployment: all players left` → the deployment disappears.
5. Debug with `references/troubleshooting.md`.

Hand-off: what was built and where, app/version/matchmaker names, how to ship a new build, free-tier caveats, and next steps (a Find Match button in the game's menu, match end via `SelfStop`, ticket-ID validation in connection approval with `MM_TICKET_IDS`, backfill, a production matchmaker tier).

## Reference files

- `references/ngo.md`: what the templates do, host → dedicated conversion, ports and UnityTransport, Boss Room-style ConnectionManager games, client-only code on the server, two clients on one machine, WebGL.
- `references/deploy.md`: MCP connection, the plugin window and its command-line equivalents, image and registry, app version for UDP 7777, direct deploy, command-line test flags.
- `references/matchmaker.md`: config, dashboard steps, ticket contract, injected variables, expansion stages and testing.
- `references/troubleshooting.md`: symptom → fix tables.
- `assets/unity/`: `EdgegapBootstrap`, `EdgegapQuitTimer`, `EdgegapSettings` (+ `.meta`, `Resources/EdgegapSettings.asset`), `EdgegapServerLifecycle`, `EdgegapMatchmakingClient`, DTOs, `link.xml`, `Editor/EdgegapPluginBuild` (command-line plugin build). `Examples/BossRoom/`: the verified Boss Room client adapter, server starter and test driver. `assets/docker/.dockerignore` (the Dockerfile is the plugin's), `assets/matchmaker/`.

Related skills in this pack, if installed: `edgegap-unity` (Mirror, WebGL, general Unity), `edgegap-fishnet`, `edgegap-purrnet`, `edgegap-deployments-api` for a studio's own backend or matchmaker, `edgegap-launch` before going live.

Sources of truth: https://docs-multiplayer.unity3d.com/netcode/current/about/, https://docs.edgegap.com/unity, https://github.com/edgegap/sdk-unity-sessions-matchmaker-server-browser, and the sample https://github.com/edgegap/netcode-game-sample-unity-ngo-bossroom.

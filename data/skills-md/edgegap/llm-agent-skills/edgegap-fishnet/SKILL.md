---
name: edgegap-fishnet
description: 'FishNet (Fish-Networking) + Edgegap: take a Unity game built on FishNet to dedicated servers and matchmaking, end to end. Load this before using any Edgegap MCP tool on a FishNet project (Assets/FishNet, Tugboat, Bayou, Multipass, ServerManager, NetworkHudCanvas). It has FishNet-ready C# templates verified on Edgegap (matchmaker client, server self-stop, scene-change persistence), the Start On Headless and WebGL/Bayou wss setup, port 7770 app version, Dockerfile, matchmaker config and fixes for known pitfalls, including the SDK JSON bug on Unity before 2022.3. Use when a FishNet dev wants online play: "host my FishNet game", "players should not host", "works on LAN but not online", "Find Match button", "FishNet WebGL on Edgegap", moving off the old FishNet Edgegap samples that call the API from the client, or debugging FishNet deployments, ports or matchmaking. Other Unity netcodes (NGO, Mirror): edgegap-unity.'
metadata:
  version: "0.3.5"
---

# Edgegap for FishNet: dedicated servers + matchmaking

Goal: a player clicks **Play**, the Edgegap matchmaker groups players, Edgegap starts a FishNet dedicated server near them, every client connects automatically, and the server stops itself when the match is over. Done means that loop works with real builds, not that the code compiles.

This path was run end to end on Edgegap with [netcode-game-sample-unity-fishnet-hashgrid](https://github.com/edgegap/netcode-game-sample-unity-fishnet-hashgrid) (`Fishnet_v4.1.6R_WebGL_Matchmaker`: Unity 2021.3.45f2, FishNet 4.1.6R, Bayou, SDK 3.5.5): two WebGL tabs were matched, connected over `wss` with TLS Upgrade, played, and the server stopped itself. The templates in `assets/unity/` are the files from that run. When the developer wants a working reference, point them at that folder.

Use **dedicated (authoritative) servers**, never relays, unless the developer explicitly wants host/client. If they do, keep the game host/client and route it through a relay deployed on Edgegap: [edgegap/server-sample-lightnet-relay](https://github.com/edgegap/server-sample-lightnet-relay) has the relay server and a transport for Mirror, FishNet, PurrNet and NGO, for desktop and Unity WebGL (WebGL over `wss://`); Edgegap's managed relays: `edgegap-relays`. A dedicated server owns the game state, so no player hosts, has a latency edge, or ends the match by quitting.

## How to work

- **Be the engineer.** Inspect the project, write the code, run the Unity batch builds, Docker and the Edgegap MCP tools, and read logs yourself. Hand the developer only Editor clicks, dashboard steps, secrets and playtesting.
- **One layer at a time.** Local → Docker → direct Edgegap deploy → matchmaker. Each phase ends with a check, so a failure points at one layer.
- **Secrets.** The Edgegap **API token** and **registry token** never go into files, git, the game client or chat. The **matchmaker Auth Token** is client-safe and ships in the client.
- **Money.** Tag test deployments, stop the ones you start. Free tier runs one deployment at a time, so a forgotten test deployment silently blocks matchmaking.
- Track the phases below as a todo list.

## Phase 0: Understand the project

Read, don't ask:
- `ProjectSettings/ProjectVersion.txt`: the Unity version. **Before 2022.3, the SDK must be 3.5.6 or newer**: 3.5.5 and older send broken JSON to the matchmaker there (every ticket gets HTTP 400). If the project already has an embedded, hand-patched SDK, replace it with the git package (latest) (`references/troubleshooting.md` §1).
- FishNet version: `Assets/FishNet/VERSION.txt` or the package in `Packages/manifest.json`. These templates target FishNet 4.x. For 2.x/3.x read `references/fishnet.md` §6.
- The NetworkManager scene, its transport (Tugboat = UDP, Bayou = WebSocket, Multipass = both) and port (7770 by default), `ServerManager` **Start On Headless**, any `NetworkHudCanvas`, the `PlayerSpawner`, and scene changes through `SceneManager.LoadGlobalScenes`.
- How the game connects today: grep `StartConnection`, `InstanceFinder`, `api.edgegap.com`, `Authorization`. Old FishNet Edgegap samples call the Edgegap API **from the client** with an API token. Remove that (`references/fishnet.md` §5) and tell the developer to rotate that token.
- Targets: WebGL means Bayou and TLS Upgrade.

Then ask, in one message, only what you couldn't infer: players per match, browser build or not, whether they have an Edgegap account and Docker. Offer defaults.

## Phase 1: Make the FishNet game dedicated-server ready

Read `references/fishnet.md`.
1. Add `"com.edgegap.unity-servers-plugin": "https://github.com/edgegap/buildtool-unity-plugin.git"` (the Edgegap Unity plugin, Editor only: build, image, push, deploy from **Tools → Edgegap Server Hosting**; no `#tag`) and the SDK, `"com.edgegap.unity-sdk": "https://github.com/edgegap/sdk-unity-sessions-matchmaker-server-browser.git"`, to `Packages/manifest.json`, on every Unity version. No `#tag`: that installs the latest SDK (3.5.6+). Never pin an exact version. Nothing to embed or patch.
2. Copy `assets/unity/*.cs` and `link.xml` into `Assets/Edgegap/`, and `assets/unity/Editor/*.cs` into `Assets/Edgegap/Editor/`. The FishNet adapters are already filled in. If the game's scripts live in an asmdef, reference `Edgegap.SDK` and FishNet's runtime asmdef from it.
3. In the NetworkManager scene, turn **Start On Headless** off on `ServerManager`. `EdgegapServerLifecycle` starts the server in every server build, so the same scene serves client and server builds.
4. Add the `Edgegap` object with the scene tool (project closed in the Editor):
   `"<Unity>" -batchmode -quit -projectPath "<project>" -executeMethod EdgegapSceneSetup.Setup -edgegapScene <NetworkManager scene> -edgegapListenPort 7770 -edgegapAutoStart true -edgegapProfile casual -logFile setup.log`
   It adds `EdgegapServerLifecycle`, `EdgegapMatchmakingClient` and `EdgegapPersistence`. Persistence keeps the object alive across FishNet scene loads (menu → battle → menu); without it the server's self-stop dies with the menu scene.
5. Headless clean-up (`references/fishnet.md` §2): no `NetworkHudCanvas` auto start, no host-only player logic, client-only code guarded.
6. Scene changes (`references/fishnet.md` §4): for every `LoadGlobalScenes` that replaces or unloads a scene, make sure the game's match manager and the players survive it on the server. Scene objects can't be moved with `MovedNetworkObjects`; spawn the manager as a global prefab or give the next scene its own.

✅ Check: a Linux server build or `-batchmode` instance logs `Edgegap Server | Starting server on 0.0.0.0:7770.`, and a client connects to it at `localhost:7770`.

## Phase 2: Connect to Edgegap

Make sure the developer has an Edgegap account, Docker running, and the Unity **Linux Build Support** + **Linux Dedicated Server Build Support** modules (plus **WebGL Build Support** for browsers). Get the Edgegap MCP connected (`references/deploy.md` §1). The header is exactly `Authorization: token <uuid>`.

✅ Check: `edgegap_list_apps` succeeds.

## Phase 3: Build, test and upload with the plugin

Copy `assets/docker/.dockerignore` to the project root (the plugin's Docker context is the project root; without it Docker sends the whole project). Then the developer opens **Tools → Edgegap Server Hosting** and goes top to bottom:
1. **Sign in with Edgegap** → **Build server** → **Containerize with Docker** (Image Name; empty tag = UTC timestamp).
2. **Test Your Server Locally**: Optional Docker Run Parameters `-p 7770:7770 (Tugboat: -p 7770:7770/udp)` → **Deploy local container**; connect a client to `127.0.0.1:7770`; **Terminate**.
3. **Upload image and Create app version** (Application Name). It pushes and opens the dashboard version form: replace the default port with `gameport` / `7770` / **WS** with TLS Upgrade on for Bayou, **UDP** for Tugboat, make sure the registry login is set (a Registry Profile, or the Container Registry username and token), save.

No Editor (CI, or you run it): the same steps from the command line in `references/deploy.md` §2-4.

✅ Check: `edgegap_list_app_versions` shows the version with `registry_credentials_set: true` and the `gameport` port.

## Phase 4: Direct deploy

1. **Deploy to cloud** in the plugin, or `edgegap_deploy` near the developer → `edgegap_wait_for_deployment` → `edgegap_get_deployment_logs`.
2. Connect a real client directly to `<fqdn>:<external port>` (Bayou: Use WSS on). The example bridge in `assets/unity/Examples/MatchmakingSystem.cs` has a direct mode for exactly this.
3. Close the clients: the server stops itself 30 s later (or `edgegap_stop_deployment`).

✅ Check: a client played on the Edgegap server. Don't build the matchmaker on an unproven server.

## Phase 5: Matchmaker

Read `references/matchmaker.md`.
1. Start from `assets/matchmaker/casual-webgl.json` (2-4 players, no latency rule, no expansion stage: `min_team_size` below `max_team_size` already allows partial matches; keep `ticket_expiration_period` at `30s` so they come quickly) or build one with `edgegap_build_matchmaker_config`. Set `application.name`/`version`, and `allowed_cors_origins` for every WebGL origin.
2. Walk the developer through the dashboard: Create Matchmaker → upload → Create and Start → copy **API URL** and **Auth Token**.
3. `GET <API URL>/monitor` with the token answers (DNS can take ~5 min).

## Phase 6: Client integration

1. Put the API URL and Auth Token on `EdgegapMatchmakingClient` (rerun `EdgegapSceneSetup` with `-edgegapBaseUrl` and `-edgegapAuthToken`, or set them in the inspector). Keep `UseLatencyBeacons` off unless the profile has a `latencies` rule; it is always off in WebGL.
2. Wire the game's Play button to `FindMatch()` / `CancelMatchmaking()` and show `Status`. If the game has a menu, adapt `assets/unity/Examples/MatchmakingSystem.cs`: it switches between direct connection and the matchmaker and disables the matchmaking client entirely when the matchmaker is off. Otherwise the built-in OnGUI panel works for a first test.
3. If the server changed, rebuild → push a new tag → new app version → matchmaker **Stop → Edit** `application.version` **→ Start**.

## Phase 7: End-to-end test and hand-off

1. `edgegap_list_deployments`: nothing of yours left running.
2. Build the client: `-executeMethod EdgegapClientBuild.Build -edgegapClientTarget webgl|win64|mac|linux` (`assets/unity/Editor/EdgegapClientBuild.cs`). Serve WebGL from an allowed origin (`python -m http.server 8080 --bind 127.0.0.1` in `Builds/Client/webgl`).
3. **Test with two clients.** Two browser tabs (bring each to the front before clicking; background tabs throttle Unity), or two builds. Watch SEARCHING → MATCH_FOUND → HOST_ASSIGNED → connected. A lone ticket can wait until it nearly expires (30 s with the template) before it gets a server, even with a `min_team_size: 1` expansion (`references/matchmaker.md` §3).
4. Server logs show `N matched player(s)`. Close both clients → `Stopping deployment: all players left` → the deployment disappears.
5. Debug with `references/troubleshooting.md` until this passes.

Hand-off: what was built and where, app/version/matchmaker names, how to ship a new build, free-tier caveats (matchmaker restarts every 3 h, one deployment at a time, 60-minute cap), and next steps (match end via `SelfStop`, ticket-ID validation with `MM_TICKET_IDS`, backfill, a production matchmaker tier).

## Reference files

- `references/fishnet.md`: FishNet server conversion, transports and ports, Start On Headless, scene changes, WebGL/Bayou, removing client-side API calls, FishNet 2.x/3.x notes.
- `references/deploy.md`: MCP connection, server build, Docker and registry, app version for 7770, direct deploy and probes.
- `references/matchmaker.md`: config, dashboard steps, ticket contract, injected variables, why partial matches need no expansion stage, the lone-ticket quirk.
- `references/troubleshooting.md`: the SDK version Unity before 2022.3 needs, and symptom → fix tables.
- `assets/unity/`: FishNet-ready `EdgegapMatchmakingClient`, `EdgegapServerLifecycle`, `EdgegapPersistence`, DTOs, `link.xml`; `Editor/` build and scene tools; `Examples/MatchmakingSystem.cs` menu bridge. `assets/docker/`: Dockerfile + .dockerignore. `assets/matchmaker/`: config template.

Related skills in this pack, if installed: `edgegap-unity` for NGO or Mirror projects, `edgegap-playfab` when the studio keeps PlayFab Matchmaking (its sample is a FishNet game), `edgegap-deployments-api` when it keeps another backend or matchmaker, `edgegap-launch` before going live.

Sources of truth if something here looks outdated: https://docs.edgegap.com/unity, https://github.com/edgegap/sdk-unity-sessions-matchmaker-server-browser (releases), https://fish-networking.gitbook.io/docs, and the sample https://github.com/edgegap/netcode-game-sample-unity-fishnet-hashgrid.

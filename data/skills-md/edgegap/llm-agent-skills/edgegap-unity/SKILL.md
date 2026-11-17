---
name: edgegap-unity
description: 'Unity + Edgegap: get a Unity multiplayer game online with dedicated servers and matchmaking, end to end. Load this before using any Edgegap MCP tool on a Unity project: it has the Unity workflow, tested C# templates (matchmaker client, server self-stop), Linux server build, Dockerfile, matchmaker config and fixes for known pitfalls. Use when a Unity dev wants online play: "put my game online", "play with people over the internet", "works on LAN/same wifi but not online", "nobody should have to host", "click Play and get matched", how Fall Guys/Among Us match players, servers for a playtest, "where do I start with servers". Also for Mirror host/client games moving to dedicated servers, WebGL multiplayer, or debugging Edgegap deployments, ports or matchmaking for a Unity game. Use even for beginners who never say Edgegap, servers or Docker. Not for NGO (edgegap-ngo), FishNet (edgegap-fishnet), PurrNet (edgegap-purrnet) or Fusion (edgegap-fusion) projects, Unreal (edgegap-unreal), Godot or non-game backends.'
metadata:
  version: "0.2.5"
---

# Edgegap for Unity: dedicated servers + matchmaking

Goal: a player clicks **Find Match**, the Edgegap matchmaker groups players, Edgegap starts a dedicated server near them, every client connects automatically, and the server shuts itself down when the match ends. The job is done when that loop works end to end with real builds, not when the code compiles.

Use **dedicated (authoritative) servers only**; never relays. A dedicated server owns the game state, so no player hosts, has a latency advantage, or can end the match by quitting. That is exactly what "nobody should have to host" and "works on LAN but not online" are asking for. Only if the developer explicitly keeps Mirror host/client: [edgegap/server-sample-lightnet-relay](https://github.com/edgegap/server-sample-lightnet-relay) runs a relay as an Edgegap deployment, with a Mirror transport that also works in WebGL builds (over `wss://`); Edgegap's managed relays: `edgegap-relays`.

## How to work

- **Be the engineer, not a tutorial.** Inspect the project, write the code, run the builds and Docker commands, call the Edgegap MCP tools, and read the logs yourself. Hand the developer only what truly needs them: clicks in the Unity Editor or Edgegap dashboard, secrets, and playtesting with their own eyes.
- **Meet the developer where they are.** Beginners ("I've never done this") get a two-line picture of the architecture and plain words; skip jargon like "authoritative" unless explained. Experienced devs get terse steps.
- **One layer at a time.** Each phase ends with a check that proves it works before the next starts. When something breaks, you then know which layer broke.
- **Secrets.** The Edgegap **API token** and **registry token** are account secrets: never write them into files, code, git, or chat output (see `references/deploy.md` §1). The **matchmaker Auth Token** is client-safe by design and goes in the game client.
- **Money.** Deployments cost money outside the free tier. Tag test deployments, stop the ones you start, and never leave one running at the end. Free tier allows only one deployment at a time, so a forgotten test deployment silently blocks matchmaking.
- Track the phases below as a todo list so nothing gets skipped across a long session.

## Phase 0: Understand the project (read before asking)

Inspect, don't interrogate:
- `ProjectSettings/ProjectVersion.txt` (Unity version), `Packages/manifest.json` (netcode: `com.unity.netcode.gameobjects`, Mirror, FishNet; existing `com.edgegap.*`), `Assets/` for Mirror/FishNet folders and an embedded Edgegap plugin.
- `ProjectSettings/EditorBuildSettings.asset`: which scenes are enabled; which one has the network manager.
- Network bootstrapping code: how the game starts host/server/client today (grep `StartHost`, `StartServer`, `StartClient`, `NetworkManager`), the transport and its port.
- Target platforms: WebGL in build profiles or mentioned? This changes the transport and matchmaker config.
- `com.unity.services.matchmaker` / Multiplay: to keep Unity Matchmaker, Unity's official `EdgegapAllocator` Cloud Code module ([matchmaker-hosting-providers](https://github.com/Unity-Technologies/matchmaker-hosting-providers/tree/main/modules/EdgegapAllocator)) starts the Edgegap server per match (see `edgegap-matchmaking`, third-party matchmakers; not run by this pack). This skill still does the build, image and app version.

Then ask, in a single message, only what you couldn't infer. Typically: players per match and teams; whether a browser (WebGL) build matters; whether they have an Edgegap account and Docker installed. Give your recommended defaults so they can just say "yes".

**Netcode for GameObjects project?** Load `edgegap-ngo` instead: NGO templates verified end to end on Edgegap with Boss Room, plus NGO pitfalls. **FishNet project?** Load `edgegap-fishnet` instead: it has FishNet-ready templates verified end to end on Edgegap, plus FishNet-specific pitfalls. **PurrNet project?** Load `edgegap-purrnet`, verified end to end the same way.

**No multiplayer at all yet?** That's a bigger job: pick a netcode (`references/netcode.md` §1) and get two players working on localhost first. Say so honestly and scope it with the developer before touching Edgegap. A single-player game that should be always online (so its logic can't be decompiled and cracked from the client) follows the same path: the server owns the rules and state, the matchmaker profile allows one player per match, and the server stops itself when that player leaves.

## Phase 1: Make the game dedicated-server ready

Read `references/netcode.md`.
1. Convert host/client assumptions to a headless server path (§2): server builds call `StartServer`, players spawn on client connect, no local player on the server, headless-unsafe code guarded.
2. Server listens on `0.0.0.0` at a fixed internal port (7777 typical; WebSocket transports often 7778).
3. Install the Edgegap packages. Add `"com.edgegap.unity-servers-plugin": "https://github.com/edgegap/buildtool-unity-plugin.git"` (the Edgegap Unity plugin, Editor only: build, image, push, deploy from **Tools → Edgegap Server Hosting**; no `#tag`) and the SDK, `"com.edgegap.unity-sdk": "https://github.com/edgegap/sdk-unity-sessions-matchmaker-server-browser.git"`, to `Packages/manifest.json` (needs git), on every Unity version. No `#tag`: that installs the latest SDK (3.5.6+). Never pin an exact version. Newtonsoft comes with it. Older SDKs fail WebGL builds and, on Unity before 2022.3, every matchmaker ticket (`references/troubleshooting.md`). If the project already has an embedded, hand-patched SDK (a `Packages/com.edgegap.unity-sdk` folder), delete it and use the git package.
4. Copy `assets/unity/EdgegapMatchmakingDTOs.cs`, `EdgegapServerLifecycle.cs`, `EdgegapMatchmakingClient.cs`, `link.xml` and `Editor/*.cs` into `Assets/Edgegap/` (the Editor scripts go in `Assets/Edgegap/Editor/`). Fill both `NETCODE ADAPTER` regions with the snippets for the project's netcode (§4). If the project's code lives in an asmdef, put these scripts in or reference it from that asmdef, and reference `Edgegap.SDK`.
5. Add both components to the network scene with `EdgegapSceneSetup` instead of hand-editing scene YAML (project closed in the Editor):
   `"<Unity>" -batchmode -quit -projectPath "<project>" -executeMethod EdgegapSceneSetup.Setup -edgegapListenPort <port> -edgegapAutoStart <false if the netcode already auto-starts headless> -edgegapProfile <profile> -logFile setup.log`
   (Or menu **Tools → Edgegap → Add Edgegap Components To Open Scene**.) Run it again later with `-edgegapBaseUrl`/`-edgegapAuthToken` once the matchmaker exists.

✅ Check: the game still works locally with one instance as dedicated server and one as client (`references/netcode.md` §6).

## Phase 2: Connect to Edgegap

Read `references/deploy.md` §1-2. Make sure the developer has an account, Docker running, and the Unity Linux Build Support + Linux Dedicated Server modules. Then get the Edgegap MCP connected with their API token: with the `edgegap` plugin Claude Code prompts them for it when the plugin is enabled; otherwise they run the `claude mcp add ...` command in their own terminal. Either way they restart the session afterwards. Common slip: the header must be exactly `Authorization: token <uuid>`. A token pasted with its own `token ` prefix becomes `token token <uuid>` and is rejected as "not an Edgegap API token".

✅ Check: `edgegap_list_apps` succeeds.

## Phase 3: Build, test and upload with the plugin

Copy `assets/docker/.dockerignore` to the project root (the plugin's Docker context is the project root; without it Docker sends the whole project). Then the developer opens **Tools → Edgegap Server Hosting** and goes top to bottom:
1. **Sign in with Edgegap** → **Build server** → **Containerize with Docker** (Image Name; empty tag = UTC timestamp).
2. **Test Your Server Locally**: Optional Docker Run Parameters `-p <port>:<port>/udp (WebSocket: -p <port>:<port>)` → **Deploy local container**; connect a client to `127.0.0.1:<listen port>`; **Terminate**.
3. **Upload image and Create app version** (Application Name). It pushes and opens the dashboard version form: replace the default port with `gameport` / `<listen port>` / the transport's protocol (`WS` with TLS Upgrade on for WebGL), make sure the registry login is set (a Registry Profile, or the Container Registry username and token), save.

No Editor (CI, or you run it): the same steps from the command line in `references/deploy.md` §2-4.

✅ Check: `edgegap_list_app_versions` shows the version with `registry_credentials_set: true` and the `gameport` port.

## Phase 4: Direct deploy

1. **Deploy to cloud** in the plugin, or `edgegap_deploy` near the developer → `edgegap_wait_for_deployment` → `edgegap_get_deployment_logs`.
2. Prove the port answers: for WS ports, `curl --http1.1 -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" --max-time 5 https://<fqdn>:<external>/` prints HTTP 101 (that also proves TLS Upgrade). Then connect a real client to `fqdn`/`public_ip` + external port. `Unable to pull image from registry` almost always means the version has no registry credentials.
3. Close the clients: the server stops itself 30 s later (or `edgegap_stop_deployment`).

✅ Check: a client played on the Edgegap server. Don't build the matchmaker on an unproven server.

## Phase 5: Matchmaker

Read `references/matchmaker.md`.
1. Design the profile from the answers in Phase 0. Keep `min_team_size` at the game's real minimum: no expansion that lowers it unless the developer explicitly wants solo or smaller matches. `min_team_size < max_team_size` already allows partial matches: don't add an expansion stage for them (expansions cost the matchmaker a lot of performance; `references/matchmaker.md`). Keep `ticket_expiration_period` at `30s`. Plan the first test with two clients.
2. Generate it with `edgegap_build_matchmaker_config` (or from `assets/matchmaker/*.json`). For WebGL pass `allowed_cors_origins` (every origin that serves the build, e.g. `http://localhost:8080`). Validate the JSON and save it as `matchmaker-config.json` in the project root.
3. Walk the developer through the dashboard (§5): Create Matchmaker → upload → Create and Start → copy **API URL** + **Auth Token**.
4. Check `GET <API URL>/monitor` with the token responds (DNS can take ~5 min).

✅ Check: monitor is healthy.

## Phase 6: Client integration

1. Put the API URL, Auth Token and profile name on `EdgegapMatchmakingClient` (inspector, or a ScriptableObject/config the game already uses). `UseLatencyBeacons` must match the profile: on only if it has a `latencies` rule, and never for WebGL.
2. Wire the game's "Play" button to `FindMatch()`/`CancelMatchmaking()`, and show `Status`. The built-in OnGUI panel is fine for a first test; hide it (`ShowGUI = false`) once the game's UI calls the methods.
3. If the server image changed in Phase 1-5 (it usually has), rebuild → push new tag → new app version → update `application.version` in the matchmaker (Stop → Edit → Start).

## Phase 7: End-to-end test and hand-off

1. Make sure no test deployment is running (`edgegap_list_deployments`).
2. Build the client with `-executeMethod EdgegapClientBuild.Build -edgegapClientTarget webgl|win64|mac|linux` (`assets/unity/Editor/EdgegapClientBuild.cs`) (output `Builds/Client/<target>`). For WebGL, serve it from an origin listed in `allowed_cors_origins`, e.g. `python -m http.server 8080 --bind 127.0.0.1` in `Builds/Client/webgl` and open `http://localhost:8080`. If you have a browser tool you can run the two-tab test yourself: open two tabs and bring each to the front before clicking (background tabs throttle Unity WebGL and can miss clicks), then click Find Match in both. Otherwise the developer runs two clients (Editor + build, two builds, or two browser tabs). Watch: SEARCHING → MATCH_FOUND → HOST_ASSIGNED → connected, both in the same match. A lone client stays in SEARCHING until a second one joins (or its ticket expires): that is expected.
3. While it runs: `edgegap_list_deployments` shows the matchmaker's deployment (tagged with ticket IDs); read its logs and confirm `N matched player(s)`.
4. Leave the match → server logs "Stopping deployment" → deployment disappears. That proves self-stop, which protects the developer's bill.
5. Debug with `references/troubleshooting.md` until this passes. Fix the root cause rather than working around it.

Hand-off summary: what was built, where the files are, the app/version/matchmaker names, how to ship a new build (build → push new tag → new version → update matchmaker version), free-tier caveats (matchmaker restarts every 3 h, one deployment at a time, 60-minute cap), and next steps (game UI for matchmaking, ticket-ID validation on the server, backfill/join-in-progress, a production matchmaker tier before launch).

## Reference files

- `references/netcode.md`: netcode choice, host/client → dedicated conversion, port/protocol table, adapter code for NGO/Mirror/FishNet, WebGL, local testing.
- `references/deploy.md`: MCP connection and token handling, prerequisites, server build commands, Docker/registry, app version fields, direct deploy, MCP caveats, free tier.
- `references/matchmaker.md`: config schema, templates, dashboard steps, ticket/profile contract, injected env vars, matchmaker troubleshooting.
- `references/troubleshooting.md`: symptom → fix tables for build, Docker, deployment, connection, SDK quirks.
- `assets/unity/`: drop-in C# (matchmaking client, server lifecycle, DTOs, link.xml). `assets/unity/Editor/`: `EdgegapPluginBuild` (command-line plugin server build), `EdgegapClientBuild` (test clients) and `EdgegapSceneSetup` (adds/configures the components from the command line). `assets/docker/.dockerignore` (the Dockerfile is the plugin's). `assets/matchmaker/`: config templates.

Related skills in this pack, if installed: `edgegap-nakama` when the studio keeps Nakama for matchmaking (with the Unity server plugin edgegap-server-nakama-plugin-unity), `edgegap-playfab` when it keeps PlayFab Matchmaking, `edgegap-deployments-api` when it keeps another backend or matchmaker (UGS) instead of Edgegap's, and `edgegap-launch` before going live.

Sources of truth if something here looks outdated: https://docs.edgegap.com/unity, https://github.com/edgegap/sdk-unity-sessions-matchmaker-server-browser (releases), and the reference sample https://github.com/edgegap/netcode-game-sample-webgl-mirror-tanks.

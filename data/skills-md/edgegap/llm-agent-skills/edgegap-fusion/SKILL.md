---
name: edgegap-fusion
description: 'Photon Fusion 2 + Edgegap: run a Unity game built on Photon Fusion as a dedicated server on Edgegap, verified end to end with Photon''s BR200 Battle Royale sample. Load this before using any Edgegap MCP tool on a Fusion project (Assets/Photon/Fusion, NetworkRunner, StartGameArgs, GameMode.Server, PhotonAppSettings, NetworkProjectConfig, TPSBR, BR200). It has a drop-in BR200 kit that changes no sample code (server build with preflight checks, Dockerfile, start script mapping Edgegap variables to BR200''s command-line options, Photon region, self-stop), headless test clients logging the connection type, and fixes for pitfalls: Loader IP 127.0.0.1 forcing Photon relays, public IP failing to bind, IL2CPP required on the server, Linux toolchain packages and App ID/AppVersion/region mismatches. Use when a Fusion dev wants dedicated servers, "host BR200", "CT shows Relayed", GameNotFound. Simple FPS sample: edgegap-fusion-simplefps. Other Unity netcodes: edgegap-unity, edgegap-ngo, edgegap-fishnet, edgegap-purrnet.'
metadata:
  version: "0.1.6"
---

# Edgegap for Photon Fusion 2: dedicated servers

Goal: Edgegap runs a headless Fusion server (`GameMode.Server`) near the players, the server registers its session with Photon Cloud, clients find it by session name and connect **Direct** (not through a Photon relay), and the deployment stops when the match ends. Done means two real clients joined one Edgegap deployment and reported CT Direct, not that the build succeeded.

This path was run end to end on 2026-10-20 with Photon's [BR200 Battle Royale (Fusion)](https://assetstore.unity.com/packages/templates/packs/br200-battle-royale-multiplayer-photon-fusion-226753) sample: BR200 2.1.0, Fusion 2.1.1 build 2177, Unity 6000.3.11f1 on Windows. The kit is also published as [edgegap/netcode-game-sample-photon-fusion2-battleroyale-200](https://github.com/edgegap/netcode-game-sample-photon-fusion2-battleroyale-200) (no BR200 code or assets; bring the Asset Store licence). An IL2CPP Linux server built with `assets/br200/` ran on Edgegap (Toronto and Newark). Two headless Windows IL2CPP clients joined each deployment, both reported CT **Direct** (14 ms in Newark), a two-player Battle Royale ran with no exceptions, one player left, the other got Game Over, and the deployment stopped on its own. `assets/br200/` holds the files from that run.

Fusion is different from the other Unity netcodes in this pack: **matchmaking stays on Photon Cloud**. The Edgegap deployment is the game server; clients find it through Photon by session name, App ID, App Version and region. Edgegap's matchmaker isn't needed for that, and it hasn't been tested with Fusion.

## How to work

- **Be the engineer.** Inspect the project, run Unity batch builds, Docker and the Edgegap MCP tools, read logs, and run the two-client tests yourself with headless clients (`references/deploy.md` §5). Hand the developer only what needs their accounts: the Asset Store download, the Photon App ID, and `docker login` to the Edgegap registry.
- **Don't change the sample's code** when a command-line option or an environment variable can do it. BR200 already parses `-dedicatedServer`, `-sessionName`, `-region`, `-ip`, `-port` and more (`references/br200.md` §2). That keeps upgrades to new BR200 versions clean.
- **One layer at a time:** build → local container → Edgegap deployment → CT check, each with a check.
- **Secrets.** The Edgegap API token and registry token never go into files, git, the client or chat. The Fusion App ID goes only into the developer's own project (`PhotonAppSettings.asset`), never into the kit or a public repo.
- **Money.** Tag test deployments and stop the ones you start. The IL2CPP server build takes about an hour: start it in the background and work on something else.
- Track the phases as a todo list.

## Phase 0: Understand the project

Read, don't ask:
- `ProjectSettings/ProjectVersion.txt`, `Assets/Photon/Fusion/release_history.txt` (Fusion version), `bundleVersion` in `ProjectSettings/ProjectSettings.asset` (BR200 version).
- `Assets/Photon/Fusion/Resources/PhotonAppSettings.asset`: `AppIdFusion`, `AppVersion`, `FixedRegion`.
- `Assets/Photon/Fusion/Resources/NetworkProjectConfig.fusion`: `PeerMode` (`0` = Single).
- `scriptingBackend` → `Server:` in `ProjectSettings.asset` (`1` = IL2CPP) and `Packages/manifest.json` for `com.unity.toolchain.*` / `com.unity.sdk.*`.
- Is it BR200 (`Assets/TPSBR/`, `TPSBR.Loader`, `StandaloneManager`)? Then follow the BR200 path below. Is it Photon's Simple FPS (`SimpleFPS` namespace in `Assets/Scripts/`, `Deathmatch` and `Startup` scenes, `MenuConnectionBehaviour`)? Load `edgegap-fusion-simplefps` instead: it has a tested kit for that sample. Another Fusion game: grep `StartGameArgs`, `GameMode.Server`, `Address =`, `CustomPublicAddress`, and read `references/fusion.md` §5.

Ask, in one message, only what you couldn't infer: the Fusion App ID (if empty), players per match, the developer's Edgegap account and Docker.

## Phase 1: Project setup

1. If the first import shows `Unsafe code may only appear if compiling with /unsafe`, reopen the project once. BR200's Project Settings already allow unsafe code, and the first import can compile before they apply.
2. Set the Fusion App ID (`Tools > Fusion > Realtime Settings`, or `AppIdFusion` in `PhotonAppSettings.asset`). Peer Mode `Single`.
3. **Server scripting backend: IL2CPP.** On a Mono server BR200's RPCs throw `MethodAccessException ... CheckInvokeRpc` and players never get a character (`references/fusion.md` §3). Building Linux IL2CPP on Windows needs Unity's toolchain (`references/deploy.md` §1).
4. BR200: copy `assets/br200/Assets/EdgegapBR200` into `Assets/`, and `assets/br200/edgegap/`, `assets/br200/scripts/`, `assets/br200/.dockerignore`, `assets/br200/.gitattributes` into the project root. For the tests in Phase 4, also copy `assets/test/ConnectionTypeProbe.cs` and `assets/test/Editor/FusionTestClientBuild.cs` into a test-only folder (for example `Assets/EdgegapTest/`).

✅ Check: the project compiles in batch mode (`-batchmode -quit`, no `error CS` in the log).

## Phase 2: Build the server and the image

Read `references/deploy.md` §2-3.
1. `scripts/build-server.sh` (or **Tools > Edgegap BR200 > Build Linux Server**). The kit's preflight stops on missing scenes, a Mono server, a missing toolchain, an empty App ID or the wrong Peer Mode, then builds the Server subtarget to `Builds/EdgegapServer/ServerBuild`. IL2CPP: about 55 minutes for BR200.
2. `scripts/package.sh` → `br200-edgegap:local` (linux/amd64).
3. Local smoke test (`references/deploy.md` §4): the server logs `Server#0 started` and registers its session; two local clients join with no exceptions. Locally they show CT Relayed, which is a Docker Desktop artifact.

✅ Check: `edgegap-build.txt` says `subtarget=Server`, `backend=IL2CPP`, `result=Succeeded`.

## Phase 3: Edgegap app version and deployment

Read `references/deploy.md` §6.
1. The developer runs `docker login registry.edgegap.com`; push with `scripts/package.sh registry.edgegap.com/<project>/br200 <new-tag>`.
2. App version: port `7777` UDP named `gameport` (`to_check: false`), 1 vCPU / 2 GB to start, max duration 60, restart policy `never` where you can set it. No registry login: the tool sends `registry_profile: "Edgegap"`; check `registry_credentials_set: true`.
3. `edgegap_deploy` with the players' IPs and a test tag → `edgegap_wait_for_deployment` → logs. The first two lines are the kit's: `bind=0.0.0.0:7777/udp public=<ip>:<port>` and `photon_region=<code> (nearest to <city>)`.

## Phase 4: Two clients and the connection type

1. Build the test client: `-executeMethod FusionTestClientBuild.Build` → `Builds/TestClient/Client.exe` (Windows IL2CPP, about 6 minutes).
2. Launch two: `Client.exe -batchmode -nographics -client -extraPeers 0 -sessionName <fqdn> -region <code from the log> -generateInput -logFile <path>` (`references/br200.md` §4).
3. Read their logs: `StartGame() Result: Ok:True`, then `[probe] mode=Client CT=Direct ... players=2`. No `Exception` lines on either side.
4. Close one client: in a Battle Royale the other gets Game Over, the server exits and the deployment stops on its own. Otherwise `edgegap_stop_deployment`.

✅ Check: CT Direct on both clients, and `edgegap_list_deployments` shows nothing of yours left running. If CT is Relayed or the join fails, use `references/troubleshooting.md`.

## Phase 5: Hand-off

What was built and where, the app/version names, the tested versions, how to ship a new build (rebuild → new tag → new app version), and what wasn't tested (200 players, CPU sizing, other maps, the Menu UI join). Delete the test-only probe and client build script, and the test app versions if the developer agrees.

If the developer is writing a guide for Photon's docs, the measured facts are in `references/fusion.md` §2 and §3: the Loader's **IP must be `0.0.0.0` or empty**.

## Reference files

- `references/fusion.md`: how a Fusion dedicated server finds and serves players, bind vs public address (measured), IL2CPP vs Mono, regions, App Version, the CT check, other Fusion games.
- `references/br200.md`: BR200's Loader and command-line options (from its source), scenes, the 120-second timer, headless test clients.
- `references/deploy.md`: toolchain packages, builds, Docker, local test, Edgegap app version and deploy, test commands.
- `references/troubleshooting.md`: symptom → fix tables.
- `assets/br200/`: the kit (editor preflight and build, Dockerfile, start script, helper scripts, start-script tests, API examples). `assets/test/`: the CT probe and the test client build.

Related skills in this pack, if installed: `edgegap-fusion-simplefps` (Photon's Simple FPS sample), `edgegap-unity` (general Unity, Mirror, WebGL), `edgegap-containerize`, `edgegap-troubleshoot`, `edgegap-launch` before going live.

Sources of truth: https://doc.photonengine.com/fusion/v2, the `Fusion.Runtime.xml` API docs shipped in `Assets/Photon/Fusion/Assemblies/`, https://docs.edgegap.com/unity.

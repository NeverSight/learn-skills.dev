---
name: edgegap-fusion-simplefps
description: 'Photon''s Simple FPS (Fusion 2) sample + Edgegap: run it as a dedicated server on Edgegap and join through its Party menu, verified end to end. Load this before using any Edgegap MCP tool on a Simple FPS project (SimpleFPS namespace, Deathmatch and Startup scenes, FusionBootstrap, FusionMenuUIParty, MenuConnectionBehaviour, SceneObjects). It has a drop-in kit that edits no Simple FPS or Fusion file: a bootstrap subclass that starts the server and names the session after the deployment FQDN, a Party menu subclass that joins by FQDN and Photon region, an editor setup and IL2CPP build, a Dockerfile, and headless test clients. It fixes the two traps of the usual Simple FPS dedicated-server steps: a server built with only the Deathmatch scene, and a scene that is not active on load, which both make clients throw NullReferenceException in Player.FixedUpdateNetwork. Use for "Simple FPS on Edgegap", "join a deployment from the Party menu" or that error. Other Fusion games, BR200: edgegap-fusion.'
metadata:
  version: "0.1.4"
---

# Photon Simple FPS on Edgegap

Goal: Edgegap runs a headless Fusion server (`GameMode.Server`) for Photon's [Simple FPS Multiplayer (Photon Fusion)](https://assetstore.unity.com/packages/templates/tutorials/simple-fps-multiplayer-photon-fusion-272941) sample, the session is named after the deployment's FQDN, and players join it from the sample's **Party** menu by typing that FQDN and the Photon region. Done means two real clients joined one Edgegap deployment through the Party menu, both report CT **Direct**, and neither side logs an exception. A successful build is not done.

This path was run end to end on 2026-10-20 with Simple FPS 2.1.1, Fusion 2.1.1 build 2177 and Unity 6000.3.11f1 on Windows. The kit in `assets/simplefps/` was copied into an unmodified Simple FPS project, and the IL2CPP Linux server it built ran on Edgegap in Newark, Photon region `us`. Two headless Windows IL2CPP clients joined through the Party menu: CT Direct, 11 to 29 ms, `players=2`, Deathmatch loaded, zero exceptions on clients and server. An earlier run with the same changes made by hand, in Toronto (`cae`), gave the same result (11 to 24 ms). The same kit, with a README for developers, is public at [edgegap/netcode-game-sample-photon-fusion2-simple-fps](https://github.com/edgegap/netcode-game-sample-photon-fusion2-simple-fps).

The general Fusion facts (bind address, IL2CPP, regions, App ID and App Version matching, CT check) are in `edgegap-fusion`. This skill covers what is specific to Simple FPS. Matchmaking stays on Photon Cloud: clients find the server by session name, App ID, App Version and region.

## How to work

- **Be the engineer.** Import the sample, run Unity batch builds, Docker and the Edgegap MCP tools, read logs, and run the two-client test yourself with headless clients (`references/deploy-and-test.md`). Hand the developer only what needs their accounts: the Asset Store download, the Fusion App ID, the registry login on the app version.
- **Don't edit Simple FPS or Fusion files.** The kit subclasses `FusionBootstrap` and `FusionMenuUIParty` and swaps the components in the scenes. Upgrades stay clean, and nothing licensed ends up in your repository.
- **Never commit Simple FPS, Fusion or third-party sample files** to a shared or public repository. They are licensed. Share the kit and import the sample from the Asset Store.
- **One layer at a time:** setup → build → local container → Edgegap deployment → two clients. Check each.
- **Secrets.** The Edgegap API token and registry token never go into files, git, the client or chat. The Fusion App ID goes only into the developer's own project.
- **Money.** Tag test deployments and stop the ones you start.
- Track the phases as a todo list.

## Phase 0: Understand the project

Read, don't ask:
- `ProjectSettings/ProjectVersion.txt`; `Assets/release_history.txt` (Simple FPS version) and `Assets/Photon/Fusion/release_history.txt` (Fusion version).
- Every `PhotonAppSettings.asset` under a `Resources` folder: the Asset Store package ships one in `Assets/AssetStoreTools/Resources/` with the publisher's App ID, and Fusion may create a second one in `Assets/Photon/Fusion/Resources/`. Put the developer's App ID in all of them.
- `Assets/Photon/Fusion/Resources/NetworkProjectConfig.fusion`: `PeerMode` must be `0` (Single).
- `scriptingBackend` → `Server:` in `ProjectSettings.asset` (`1` = IL2CPP) and `Packages/manifest.json` for the Linux toolchain.
- Is the kit already in (`Assets/EdgegapSimpleFPS/`)? Did someone already follow manual steps (edited `FusionBootstrap.cs` or `FusionMenuUIParty.cs`, a Deathmatch-only build profile)? See `references/simplefps.md` §4.

Ask, in one message, only what you couldn't infer: the Fusion App ID (if empty), the developer's Edgegap account and Docker.

## Phase 1: Set up

1. Import the sample: a new Unity project, then the Asset Store package (it is a complete project: it brings its own Project Settings). The Asset Store cache is `%APPDATA%\Unity\Asset Store-5.x\Photon Engine\Complete ProjectsTutorials\` on Windows; `-createProject <path> -importPackage <file>` works in batch mode.
2. Set the Fusion App ID (Phase 0) and Peer Mode `Single`.
3. Windows, Unity 6000.3: add `com.unity.toolchain.win-x86_64-linux` and `com.unity.sdk.linux-x86_64` (1.1.0) to `Packages/manifest.json`.
4. Copy `assets/simplefps/Assets/EdgegapSimpleFPS`, `assets/simplefps/edgegap/`, `assets/simplefps/scripts/`, `assets/simplefps/.dockerignore` and `assets/simplefps/.gitattributes` into the project. For the Phase 4 test, also copy `assets/test/EdgegapSimpleFPSTest` into `Assets/`. The [kit repository](https://github.com/edgegap/netcode-game-sample-photon-fusion2-simple-fps) has the same files in the same layout (test folder in `Assets/EdgegapSimpleFPSTest`), if the developer prefers to clone it.
5. `scripts/build.sh setup` (or **Tools > Edgegap Simple FPS > Set Up Project**). It swaps the two components, keeping every inspector value, adds the Region field to the Party menu's Join card, sets Deathmatch's Start Mode to User Interface and puts Startup (0) and Deathmatch (1) in the build profile. `references/simplefps.md` §3 says what each change is for.

✅ Check: the log shows the three `[Edgegap Simple FPS]` setup lines and no `error CS`.

## Phase 2: Build the server and the image

1. `scripts/build.sh server`: checks the project (Linux module, IL2CPP server, toolchain, scenes, App ID, Peer Mode), sets it up, and builds the Linux **Server** subtarget to `Builds/EdgegapServer/ServerBuild` with **both** scenes. About 13 minutes the first time, 1 to 2 minutes after.
2. `scripts/package.sh` → `simplefps-edgegap:local` (linux/amd64, Ubuntu 22.04, non-root).
3. Local test: `scripts/run-local.sh`, then the clients from Phase 4 with session `f68e011bfb01.pr.edgegap.net` and the region from the `[edgegap-simplefps] server started` line. Locally CT shows **Relayed**: that's Docker Desktop's NAT, not a problem.

✅ Check: `Builds/EdgegapServer/edgegap-build.txt` says `subtarget=Server`, `backend=IL2CPP`, both scenes, `result=Succeeded`; the container logs `server started: session=... photon_region=...`.

## Phase 3: Edgegap app version and deployment

1. The developer runs `docker login registry.edgegap.com`; push with `scripts/package.sh registry.edgegap.com/<project>/simplefps <new-tag>`.
2. `edgegap_create_app` (once) and `edgegap_create_app_version`: port `7777` UDP named `gameport`, `to_check: false`, 1024 CPU units / 2048 MB, max duration 60 for tests. No registry login: the tool sends `registry_profile: "Edgegap"`; check `registry_credentials_set: true` with `edgegap_list_app_versions`.
3. `edgegap_deploy` with the players' IPs and a test tag → `edgegap_wait_for_deployment` → `edgegap_get_deployment_logs`. Read the Photon region from `[edgegap-simplefps] server started: session=<fqdn> photon_region=<code>`. To force one, set `PHOTON_REGION` on the deployment (the verified runs used the best-ping region; the override isn't tested yet).

## Phase 4: Two clients through the Party menu

1. `scripts/build.sh client` → `Builds/Client/SimpleFPS.exe` (Windows IL2CPP).
2. `scripts/test-clients.sh <fqdn> <region>`: two headless clients type the FQDN and region into the Join card and press Join, then it prints each client's last probe line.
3. Pass: both `CT=Direct ... players=2 ... runnerScene=Deathmatch#1`, `exceptions=0`. Then check the server log: two `[Player:N] connected.` lines and no `Exception`.
4. `edgegap_stop_deployment`, then `edgegap_list_deployments` with `only_agent_deployments: true` shows nothing of yours.

A person can do the same from a normal client build: Startup → **Party Menu** → FQDN in the code field, region in the Region field → **Join**.

If a step fails, see `references/troubleshooting.md`.

## Phase 5: Hand-off

What was built and where, the app and version names, the tested versions, how to ship a new build (build → new tag → new app version), and what wasn't tested: more than two players, a whole match to its end, whether the server exits after a match (the start script stops the deployment when it does), CPU sizing. Delete `Assets/EdgegapSimpleFPSTest` before shipping, and the test app versions if the developer agrees.

## Reference files

- `references/simplefps.md`: how Simple FPS starts and joins games, what the kit changes and why, and the two client-breaking traps with their measured symptoms.
- `references/deploy-and-test.md`: commands for setup, builds, Docker, Edgegap and the two-client test, with what passing logs look like.
- `references/troubleshooting.md`: symptom → fix.
- `assets/simplefps/`: the kit. `assets/test/`: the probe, the Party menu join driver and the client test script.

Related skills: `edgegap-fusion` (Fusion on Edgegap in general, BR200), `edgegap-unity`, `edgegap-troubleshoot`, `edgegap-launch` before going live.

Sources of truth: https://doc.photonengine.com/fusion/v2, the `Fusion.Runtime.xml` API docs in `Assets/Photon/Fusion/Assemblies/`, https://docs.edgegap.com/unity.

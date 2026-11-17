---
name: edgegap-ugs-matchmaker
description: 'Unity Gaming Services (UGS) Matchmaker + Edgegap: keep Unity Matchmaker queues and pools and have each match start its own Edgegap dedicated server near the players, through the EdgegapAllocator Cloud Code module (Matchmaker_AllocateServer deploys, Matchmaker_PollAllocation returns IP:port to the tickets). Load this before using any Edgegap MCP tool on a Unity project that uses com.unity.services.matchmaker or MatchmakeSessionAsync, has .mmq queue files, ugs deploy, Cloud Code hosting, or is leaving Multiplay Hosting (MultiplayService, server query, allocation payload). Covers deploying the module with the UGS CLI, the EDGEGAP_API_TOKEN secret, app/version/port constants, the queue''s Cloud Code hosting, player_ip in ticket custom data, the client ticket flow, MATCH_ID and self-stop on the server. Not run end to end yet. A new game with no matchmaker: edgegap-matchmaking + edgegap-unity. PlayFab: edgegap-playfab. Choosing a matchmaker: edgegap-matchmaking.'
metadata:
  version: "0.1.1"
---

# Edgegap for Unity Matchmaker (UGS): Unity matches players, Edgegap runs the match

Goal: the game keeps Unity Matchmaker (queues, pools, rules, Unity Authentication), and every match it forms gets its own Edgegap dedicated server placed near the matched players. Matchmaker writes the server's IP and port into each ticket, clients connect, and the server stops its own deployment when the match is over. Done means two real clients were matched by Unity Matchmaker, played on one Edgegap deployment, and the deployment stopped. A module that deploys is not done.

```
Client --CreateTicketAsync(queue, Player{CustomData.player_ip})--> UGS Matchmaker queue/pool (hosting: Cloud Code)
Matchmaker --Matchmaker_AllocateServer(MatchId, MatchProperties)--> EdgegapAllocator (Cloud Code C# module)
            reads secret EDGEGAP_API_TOKEN --POST /v2/deployments {application, version, users[player IPs], env MATCH_ID, tags}--> Edgegap
            returns Created + AllocationData {requestId}
Matchmaker --Matchmaker_PollAllocation(requestId), repeatedly--> EdgegapAllocator --GET /v1/status/{requestId}--> Edgegap
            READY → Allocated, AssignmentData.IpPort(public_ip, external port of PortName)
Client --GetTicketAsync--> MultiplayAssignment {Status Found, Ip, Port, MatchId} --> connects --> server self-stops at match end
```

## Status: read this first

- **Not run end to end in this pack.** Nobody has yet matched two clients through UGS Matchmaker onto an Edgegap server with this skill. What is solid: the module's code (read line by line, summarized in `references/allocator.md`), its unit tests, Unity's docs for Cloud Code hosting, and the Edgegap side, which is the same as in every verified Edgegap Unity sample. Say this to the developer, and treat the first match as the real test.
- **Where the module lives.** Edgegap wrote it on a branch of its fork, [edgegap/backend-unity-ugs-matchmaker-template-model](https://github.com/edgegap/backend-unity-ugs-matchmaker-template-model/tree/edgagap-allocator-integration/modules/EdgegapAllocator) (branch `edgagap-allocator-integration`, typo included; the fork's `main` has no Edgegap module and is not merged). The same code was contributed upstream and is on the `main` of Unity's repo, [Unity-Technologies/matchmaker-hosting-providers](https://github.com/Unity-Technologies/matchmaker-hosting-providers/tree/main/modules/EdgegapAllocator) (PR #11, January 2026), which later added a connection-reuse fix and a 10 s HTTP timeout (October 2026). **Use upstream `main`**: it is newer and the one Unity builds in CI. Unity's own [hosting providers page](https://docs.unity.com/en-us/matchmaker/hosting-providers) does not list Edgegap among its examples, but the module is in the repo.
- **Licence.** The repo is under the Unity Companion License (use only with Unity). Link to it and have the developer clone it; don't copy its code into this skill or into unrelated projects.

Why this shape, so you can defend it:
- **Unity Matchmaker stays; Edgegap replaces the server host.** The pool's Match Hosting is **Cloud Code**, so Matchmaker calls the module instead of Multiplay. No Multiplay SDK on the server, no fleets or build configurations: Edgegap picks one of its locations near the players for each match.
- **The token stays in UGS.** The module reads the Edgegap API token from UGS Secret Manager at each call. It is never in the client, the server image, the module source or git.
- **Nothing waits inside one call.** Cloud Code cancels an invocation after 15 s while a server takes several seconds to be ready, so Allocate only starts the deployment and returns; Matchmaker then calls Poll until the server is ready, an error, or the pool times out.
- **Placement needs the players' IPs, and Unity doesn't pass them.** Each client puts its public IP in its ticket's player custom data as `player_ip`; the module sends them as `users`. Without them every match lands at one fixed fallback point (Los Alamos, New Mexico).

## How to work

- **Be the engineer.** Read the project, edit the module's constants, run `dotnet`, the `ugs` CLI, Unity builds, Docker and the Edgegap MCP tools, and read the logs. Hand the developer only account steps: the Edgegap token into UGS Secrets, a UGS service account for the CLI, `docker login`, Dashboard clicks, playtesting.
- **One layer at a time:** server runs locally → image → one direct Edgegap deployment → module deployed → queue on Cloud Code → client → two-client match. Each phase has a check; don't wire Matchmaker to an unproven server.
- **Safety.** Follow the `edgegap` skill's [agent rules](../edgegap/references/agent-rules.md): ask before deploying, timestamp image tags and versions, stop only what you started. The UGS service account key and the Edgegap token are secrets: the developer types them into the Dashboard or their own terminal (`ugs login`), never into chat, code or the repo.
- **Money.** Every match starts a deployment until the server stops itself. Free tier: one deployment at a time, so a leftover test server makes every allocation fail.

## Phase 0: Understand the project

Read, don't ask:
- Matchmaker usage: `com.unity.services.matchmaker` (`MatchmakerService.Instance.CreateTicketAsync`, `GetTicketAsync`, `MultiplayAssignment`) or the Multiplayer Services package `com.unity.services.multiplayer` (`MultiplayerService.Instance.MatchmakeSessionAsync`). Queue and pool names, `.mmq` files, rules on `Players.CustomData.*`, QoS regions, backfill.
- Multiplay leftovers on the server: `MultiplayService`, `ServerQueryHandler`, `ReadyServerForPlayersAsync`, `GetPayloadAllocationAsJson`, `server.json`. They go away (`references/unity.md` §4).
- Netcode, transport, port and whether a Linux dedicated server build exists. Netcode specifics: `edgegap-ngo`, `edgegap-fishnet`, `edgegap-purrnet`, `edgegap-unity` (Mirror and others).
- Players per match and whether clients include WebGL (the module returns an IP, not an FQDN: `references/allocator.md` §5).

Ask in one message only what you couldn't infer: the UGS project and environment to use (a non-production environment first), their Edgegap account, players per match.

**Pick the client flow now.** The ticket API (`CreateTicketAsync` / `GetTicketAsync`) hands the client `Ip` and `Port` directly; that is the path this skill recommends. `MatchmakeSessionAsync` (sessions) makes the client join a UGS session whose ID is the match ID, so the Edgegap server itself would have to create that session with a UGS service account: more moving parts, a secret on the server, and not verified with Edgegap. See `references/unity.md` §2.

## Phase 1: The game server on Edgegap

Use `edgegap-unity` (or the netcode's skill) for this phase; nothing here is UGS-specific.
1. Headless Linux server that listens on a fixed internal port on `0.0.0.0` and starts without a player. Build it with the Edgegap Unity plugin (`edgegap-unity`, its plugin build), not a hand-written Dockerfile.
2. Self-stop when nobody joins and when the match ends (`EdgegapServerLifecycle.cs` from `edgegap-unity` works on deployments started by this module: it handles deployments with no Edgegap matchmaker variables). Read `MATCH_ID` if the server needs the UGS match ID (`references/unity.md` §3).
3. Image, then app version with the game port named **`gameport`** (the module looks the port up by name), the netcode's protocol (UDP for most), 0.5 vCPU / 1 GB to start. Name the image tag and version with a UTC timestamp.
4. `edgegap_deploy` near the developer, `edgegap_wait_for_deployment`, connect one client by hand to `public_ip` + external port, `edgegap_stop_deployment`.

✅ Check: a client played on an Edgegap deployment that you started by hand.

## Phase 2: Deploy the EdgegapAllocator module

Read `references/allocator.md` (what it sends and returns, the constants, the CLI).
1. Clone Unity's repo **outside the game project** (it is not a Unity package): `git clone https://github.com/Unity-Technologies/matchmaker-hosting-providers.git`.
2. In `modules/EdgegapAllocator/Project/EdgegapAllocator.cs`, set `ApplicationName`, `VersionName` (the app version from Phase 1) and `PortName` (`gameport`). `CONFIGURATION.md` gives line numbers 34 to 36; in the current file they sit a few lines lower, at the top of the `EdgegapAllocator` class.
3. The developer adds the secret `EDGEGAP_API_TOKEN` in the Unity Dashboard: **Administration > Secrets**. The module sends the secret's value as the whole `Authorization` header, and Edgegap expects `token <your token>` there, so store it with the `token ` prefix unless the dashboard's copy already includes it (`references/allocator.md` §3).
4. `dotnet test tests/AllocatorTests` (optional, offline), then the developer sets up the CLI (`ugs login` with a service account that has Cloud Code Editor and Unity Environments Viewer; `ugs config set project-id`, `ugs config set environment-name`) and you run `ugs deploy modules/EdgegapAllocator`.

✅ Check: the Dashboard's Cloud Code modules list shows `EdgegapAllocator` in the right environment.

## Phase 3: Point the queue at the module

1. In the Unity Dashboard, **Matchmaker > Queues**, on the pool: Match Hosting **Cloud Code**, Module Name `EdgegapAllocator`, Allocate Function Name `Matchmaker_AllocateServer`, Poll Function Name `Matchmaker_PollAllocation`. Or the same `matchHosting` block in the `.mmq` file, deployed with `ugs deploy` (`references/allocator.md` §4).
2. Switching a live pool from Multiplay moves every new match to Edgegap at once. Use a copy of the queue (or a filtered pool) for testing, and ship the client that sends `player_ip` before switching.
3. Keep the pool's timeout above the server's boot time (Unity's local example uses 90 s).

## Phase 4: The client

Read `references/unity.md` §1.
1. Before queueing, get the player's public IP (Edgegap's UGS guide uses `https://api.ipify.org?format=json`) and send it as `player_ip` in the `Player` custom data, alongside whatever the queue's rules already read.
2. Poll `GetTicketAsync` about once a second. On `MultiplayAssignment` with `Status` `Found`, connect to `Ip:Port`. On `Failed` or `Timeout`, show it and let the player queue again. Delete the ticket when the player cancels.
3. Keep the existing UI and netcode connect call; only the address source changes.

## Phase 5: End-to-end test

1. `edgegap_list_deployments`: nothing of yours running (free tier: one at a time).
2. Two clients signed in as different UGS players (two builds, or Multiplayer Play Mode with separate authentication profiles) queue in the test queue.
3. Watch: ticket created → Cloud Code log for `Matchmaker_AllocateServer` → an Edgegap deployment tagged `ugs-matchmaker` near the players → `Found` with an IP and port → both connect → match → the deployment stops on its own.
4. Debug with `references/troubleshooting.md` until this passes, then record the date, Unity and package versions, netcode and result. Until then, keep saying "not verified".

Hand-off: what runs where (UGS project/environment, queue and pool, the module and which commit of Unity's repo, the Edgegap app and version), how to ship a new server build (push a new timestamped tag, create the version, change `VersionName`, redeploy the module), where the logs are (Cloud Code logs in the Dashboard, Edgegap deployment logs), and the limits: Status API 20 requests/s per organization, one deployment at a time on the free tier.

## Reference files

- `references/allocator.md`: the module's Allocate and Poll, exactly what goes to Edgegap and back, constants, the secret, deploying with the `ugs` CLI, the queue's `matchHosting` block, changes worth making (FQDN for WebGL, more env vars, webhooks at scale).
- `references/unity.md`: client ticket flow with `player_ip`, the sessions caveat, reading `MATCH_ID` and the port on the server, self-stop, moving off Multiplay Hosting.
- `references/troubleshooting.md`: symptom → cause, and what is not verified.

Related skills, if installed: `edgegap-unity` (server build, Dockerfile, self-stop; NGO, FishNet, PurrNet have their own), `edgegap-matchmaking` (choosing a matchmaker, placement, backfill design), `edgegap-deployments-api` (the Deploy and Status APIs in depth), `edgegap-launch` before going live.

Sources of truth if something here looks outdated: the module in https://github.com/Unity-Technologies/matchmaker-hosting-providers, Unity's https://docs.unity.com/en-us/matchmaker/hosting-providers, Edgegap's https://docs.edgegap.com/docs/tools-and-integrations/deploy-from-ugs and https://docs.edgegap.com/docs/tools-and-integrations/switch-from-multiplay.

---
name: edgegap-colyseus
description: 'Colyseus + Edgegap: host a Colyseus (Node.js) multiplayer game on Edgegap with one dedicated server per match, near its players, that stops itself, end to end. Load this before using any Edgegap MCP tool on a Colyseus project (colyseus or @colyseus/* in package.json, Room classes with onJoin/onLeave, defineServer, app.config.ts, colyseus.js, @colyseus/sdk, the Colyseus Unity, Godot, Cocos Creator, Defold, GameMaker or Haxe SDKs). It has templates verified on Edgegap: a lifecycle module (self-stop on no join, empty server or match end), a Dockerfile, the WS + TLS Upgrade app version, a direct deploy script, a matchmaker config, and matchmaker clients for browser JS/TS, Cocos Creator, Unity and Godot, plus the pitfalls: 502 on a fresh server, wss by FQDN, CORS origins, exposed playground. Use for "host my Colyseus server", "Colyseus on Edgegap", "replace Colyseus Cloud", "one server per match", "Find Match with Colyseus", or debugging Colyseus deployments. Manus games: edgegap-manus.'
metadata:
  version: "0.4.3"
---

# Edgegap for Colyseus games: one server per match

Goal: each match gets its own Colyseus server on Edgegap, placed near its players. Players reach it directly (a URL from a script or the developer's backend) or through Edgegap's matchmaker (click Play, get matched, connect), over `wss://<id>.pr.edgegap.net:<port>`, and the server stops its own deployment when the match is over. Done means two real clients played on one Edgegap deployment and it stopped itself afterwards, not that the image builds.

```
Direct:      developer / backend --deploy--> Edgegap --wss://<id>.pr.edgegap.net:<port>--> clients
Matchmaker:  clients --tickets--> Edgegap Matchmaker --deploy--> Edgegap --assignment--> clients --wss--> server
```

This path was run end to end on Edgegap on 2026-10-20 with [edgegap/backend-game-sample-threejs-colyseus-tanks](https://github.com/edgegap/backend-game-sample-threejs-colyseus-tanks), a fork of Colyseus's official tanks demo (Colyseus 0.17, one server, 9 clients; guide in its `edgegap/README.md`). Verified: the Colyseus matchmake HTTP request and the room WebSocket both go through one WS port with TLS Upgrade; direct mode with Node and Godot desktop clients; matchmaker 3.3.2 matched a Three.js browser client with a Godot desktop client, then with a Unity Windows build; the server stopped itself each time. On 2026-10-29 the same templates ran with a Cocos Creator 3.8.8 web build: [edgegap/backend-game-sample-cocos-colyseus-tictactoe](https://github.com/edgegap/backend-game-sample-cocos-colyseus-tictactoe), a fork of Colyseus's Cocos tic-tac-toe demo upgraded from Colyseus 0.14 to 0.17, matched with a bot through the matchmaker, played to the end, and the server stopped itself. The templates in `assets/` are the files from the tanks run, with the tanks-specific match rule moved out of the lifecycle module. Not run: Construct 3, Defold, GameMaker, Haxe and PlayCanvas clients, Godot web export, Unity WebGL, Cocos mini-game and native builds, Colyseus 0.15/0.16, rooms with `allowReconnection`. Say so when those matter.

Why this shape, so you can defend it:
- **One deployment = one match = one Colyseus process.** Edgegap places each match near its players and bills it only while it runs. No PM2, no Redis presence, no room-count capacity planning: those solve "many matches on a few VMs", which Edgegap replaces.
- **The server stops itself.** Only the game knows a match is over. Without self-stop an empty deployment runs to its max duration and bills.
- **WS + TLS Upgrade.** Edgegap terminates TLS, so the Node server stays plain HTTP, and browser builds on `https` pages can connect.
- **Clients call the matchmaker, never the Deploy API.** The matchmaker Auth Token is client-safe; the Edgegap API token controls the whole organization.

## How to work

- **Be the engineer.** Read the server and clients, write the changes, run `npm run dev`, Docker and the Edgegap MCP tools, read logs. Hand the developer only account steps: `docker login`, creating the matchmaker in the dashboard, playtesting.
- **One layer at a time**: server changes locally → container → one direct deployment → matchmaker → clients. Each phase has a check.
- **Secrets** (full rules: [the edgegap skill's agent rules](../edgegap/references/agent-rules.md)): the Edgegap API token never goes into a client, the server image, a deployment env var, git or chat. The matchmaker Auth Token may ship in clients.
- **Money.** Ask before deploying. Tag test deployments and stop only the ones you started. Free tier: one deployment at a time.

## Phase 0: Understand the project

Read, don't ask:
- `server/package.json` (or the root one): the `colyseus` version (0.17 uses `defineServer`/`defineRoom`; 0.15/0.16 use `@colyseus/tools` `app.config.ts` or `new Server`), how it starts (`tsx`, `ts-node`, `tsc` then `node`), and whether `tsx` is a dependency or a devDependency.
- The entry point: port (`PORT`, default 2567), playground, monitor, custom Express routes, presence/driver (Redis), PM2 `ecosystem.config.*`.
- The room classes: `onJoin`, `onLeave`, `allowReconnection`, `maxClients`, how a match ends (or if it never does), `onAuth`.
- The clients: which SDKs (`@colyseus/sdk`, `colyseus.js`, Unity, Godot, Defold, GameMaker, Haxe...), web or desktop builds, and where the server URL is set.
- Where it's hosted now (Colyseus Cloud, a VPS, nowhere) and whether a backend or lobby already groups players.

Ask, in one message, only what you couldn't infer: players per match, whether they want direct mode, the matchmaker, or both, the origins (domains) of web builds, their Edgegap account and Docker. Default: matchmaker with a `casual` profile of 2 to 8 players, plus direct mode for testing.

## Phase 1: Server changes, local

Read `references/server.md`.
1. Copy `assets/server/src/edgegap.ts` into the server's `src/`.
2. Entry point: `startLifecycle()` once listening; mount playground and monitor only when `!onEdgegap`.
3. Every room: `playerJoined()` in `onJoin`, `playerLeft()` when a seat is really gone (after a failed `allowReconnection`, not on a drop), `selfStop("...")` when the match ends: lock the room, show the result for a few seconds, `disconnect()`, then stop.
4. Copy `assets/server/Dockerfile`, `.dockerignore` and `scripts/edgegap-deploy.mjs`; add the `edgegap:deploy` script to `package.json`. Make sure `tsx` is in `dependencies` (or switch the `CMD` to the compiled output).

✅ Check: `npm run dev` works as before (playground still there). `docker run --rm -p 2567:2567 -e ARBITRIUM_REQUEST_ID=local -e EMPTY_TIMEOUT_S=10 <image>`: a client on `ws://localhost:2567` joins, `/` is 404, and 10 s after it leaves the log shows `[edgegap] self-stop: empty for 10s` and the container exits.

## Phase 2: Image, app version, one direct deployment

Read `references/deploy.md` §1 to §3. **Cocos Creator project** (if its server is not Colyseus, load `edgegap-cocos` instead): the developer does steps 1 to 3 in the [Edgegap Cocos extension](https://github.com/edgegap/buildtool-cocos-plugin) panel instead (install, settings and the headless run in `references/clients.md`, Cocos section); you set it up and check the result with the MCP tools.
1. `docker build --platform linux/amd64`, the developer runs `docker login registry.edgegap.com`, push a new tag (UTC timestamp `YYYYMMDD-HHMM`, also the app version name), never `latest`.
2. `edgegap_create_app` and `edgegap_create_app_version`: port `2567`, protocol **WS**, name `gameport`, `tls_upgrade: true`; 256 CPU units / 512 MB; max duration 60 for tests. No registry login: the tool sends `registry_profile: "Edgegap"`; check `registry_credentials_set: true`.
3. Ask, then `edgegap_deploy` with the players' IPs and a test tag → `edgegap_wait_for_deployment` (or the developer runs `npm run edgegap:deploy -- <app> <version>`). The URL is `wss://<fqdn>:<external gameport>`.
4. Point a client at it (`?server=` / `--server=`, `references/clients.md`). If the first join gets **502**, retry: a fresh deployment answers 502 for a few seconds.

✅ Check: the log shows `[edgegap] deployment <id> ... match=direct`, a client plays, and after it leaves `self-stop: empty for 30s` and `self-stop request: HTTP 200`; `edgegap_list_deployments` no longer lists it. Don't add the matchmaker on an unproven server.

## Phase 3: Matchmaker

Read `references/deploy.md` §4.
1. Start from `assets/matchmaker/casual.json`: `application.name`/`version`, team sizes, and `allowed_cors_origins` with every origin that serves a web build (scheme + host + port). Don't add an expansion stage for partial matches: `min_team_size` below `max_team_size` already allows them, and the `30s` ticket expiration keeps the wait short (expansions cost the matchmaker a lot of performance). Set `inspect` to `false` before launch.
2. The developer uploads it: Matchmaker → Create → **Create and Start**, then copies the **API URL** and **Auth Token**.

## Phase 4: Clients

Read `references/clients.md`. Copy the matchmaker template for each client engine: `assets/client/js/Matchmaker.ts` + `assets/client/js/joinWithRetry.ts` (browser, and Cocos Creator: copy them into the project's scripts folder; `Matchmaker.ts` wraps the official Edgegap JS SDK, so `npm i @edgegap/sdk` too), `assets/client/unity/EdgegapMatchmaker.cs` (Unity 2023.1+ / 6), `assets/client/godot/edgegap_matchmaker.gd` (Godot 4). Wire them so:
- an explicit server URL (`?server=`, `--server=`) wins over the matchmaker;
- the matchmaker URL and Auth Token come from launch arguments, page parameters, build-time env or inspector fields;
- the first join after `HOST_ASSIGNED` retries 10 times, 2 s apart;
- the client connects to `wss://<fqdn>:<port>` and cancels its ticket when the player quits while searching.
Other client SDKs get the direct `server` override; port `edgegap_matchmaker.gd` (plain HTTP) for matchmaking.

## Phase 5: End-to-end test and hand-off

1. `edgegap_list_deployments`: nothing of yours left running (free tier: a leftover blocks matchmaker deployments).
2. Two clients (any mix of engines) with the matchmaker settings: both searching → connecting → in the same room. The server log shows both ticket IDs.
3. Both quit: `self-stop: empty for 30s`, the deployment disappears. If the game has a match end, play one to the end too.
4. Debug with `references/troubleshooting.md`.

Hand-off: what changed where, app/version/matchmaker names, how to ship a new server build (new tag → new app version → matchmaker Stop → Edit `application.version` → Start), what wasn't tested, and before launch: `inspect` off, real origins in `allowed_cors_origins`, max duration fitted to matches, optionally only matched players allowed in (`references/server.md` §6), `edgegap-launch`.

## Reference files

- `references/server.md`: entry point per Colyseus version, playground and monitor, counting players, reconnection, match end, the lifecycle module, local checks, restricting joins to matched tickets.
- `references/deploy.md`: image, app version (WS + TLS Upgrade), direct deployments, matchmaker config and ticket API, shipping updates.
- `references/clients.md`: browser JS/TS, Unity and Godot matchmaker wiring, the join retry, direct-mode overrides for other SDKs, Windows long paths.
- `references/troubleshooting.md`: symptom → fix.
- `assets/`: `server/` (lifecycle module, Dockerfile, deploy script), `matchmaker/`, `client/js`, `client/unity`, `client/godot`.

Related skills in this pack, if installed: `edgegap` (platform and safety rules), `edgegap-server-design`, `edgegap-containerize`, `edgegap-deployments-api` (a backend or lobby that deploys servers instead of the matchmaker), `edgegap-troubleshoot`, `edgegap-launch` before going live. A browser game made with Manus: `edgegap-manus`.

Sources of truth: https://docs.colyseus.io, https://docs.edgegap.com/learn/orchestration/deployments, https://docs.edgegap.com/learn/matchmaking, https://github.com/edgegap/backend-game-sample-threejs-colyseus-tanks.

---
name: edgegap-cocos
description: 'Cocos Creator + Edgegap without Colyseus: host the authoritative server of a Cocos Creator 3.8 game (usually Node.js with ws or socket.io, any language works) on Edgegap, one server per match near its players, end to end. Load this before using Edgegap MCP tools on a Cocos project whose server is not Colyseus. It covers the server shape (Linux container, one WebSocket port with TLS Upgrade for wss://, env config, self-stop), deploying with the Edgegap Cocos extension (install, panel flow, quick-start vs regular token, headless e2e) or with MCP tools/dashboard, the Cocos client (wss by FQDN, first-connection retry, Find Match with @edgegap/sdk), WeChat/Douyin mini-game domain allowlists, testing and troubleshooting. Use for "host my Cocos Creator game server", "Cocos multiplayer on Edgegap", "Edgegap Cocos extension/plugin", "wss from a Cocos web build", "Cocos mini-game with dedicated servers". Colyseus server: edgegap-colyseus. Three.js/Phaser/Babylon browser game: edgegap-threejs. Godot: edgegap-godot.'
metadata:
  version: "0.1.2"
---

# Edgegap for Cocos Creator games (without Colyseus)

Goal: a Cocos Creator 3.8 game whose matches each run on their own authoritative server on Edgegap, near the players. Players click Play, the client gets a match from Edgegap's matchmaker (or a direct server URL), connects over `wss://<id>.pr.edgegap.net:<port>`, and the server stops its own deployment when the match is over. Done means two real clients played on one Edgegap deployment that then stopped itself, not that the image builds.

```
Cocos client --@edgegap/sdk: ticket--> Edgegap Matchmaker --deploys near the players--> Edgegap
Cocos client <--HOST_ASSIGNED {fqdn, gameport}--
Cocos client --wss://<fqdn>:<port>, hello{name, ticket}--> game server (one per match) --DELETE $ARBITRIUM_DELETE_URL--> stopped
```

Cocos Creator has no headless server build: the server is a separate program, usually a Node.js app in the project's `Server/` folder. That is what goes on Edgegap; the Cocos project stays a normal client build (web, native, mini-game).

**Which skill.** Server uses `colyseus` / `@colyseus/*` → `edgegap-colyseus` (it covers Cocos clients and has a verified Cocos sample). Nakama → `edgegap-nakama`. A Three.js, Phaser, Babylon.js or plain canvas browser game → `edgegap-threejs`. Anything else with a Cocos client, including no server yet → this skill.

**What is verified, what isn't.** This skill has **not** been run end to end on Edgegap. It is assembled from parts that were:
- The [Edgegap Cocos extension](https://github.com/edgegap/buildtool-cocos-plugin) 2.0.0 (merged 2026-10-29): its headless path (`scripts/e2e.mjs`, the same `core/` code as the panel) built, ran locally, pushed, created a version, deployed and played two bots over `wss://` with the Colyseus tic-tac-toe sample. **The panel itself was never clicked in the GUI editor.**
- A Cocos Creator 3.8.8 web-desktop build matched through the Edgegap matchmaker and played a match on Edgegap ([backend-game-sample-cocos-colyseus-tictactoe](https://github.com/edgegap/backend-game-sample-cocos-colyseus-tictactoe), Colyseus server). The SDK-based `Matchmaker.ts` ran in Chrome against a live matchmaker on 2026-11-02 and bundles in Cocos 3.8.8.
- This skill's own server templates and `GameSocket.ts` ran locally on 2026-11-04 (Node 22, Docker): retry, join, ticket check, match end, self-stop request, SIGTERM (`references/server.md` §8). The client files type-check against `@edgegap/sdk` 1.1.0 but were not run inside a Cocos build.
Say which parts are unproven when the developer relies on them.

Why this shape, so you can defend it:
- **Authoritative server, thin client.** The Cocos client sends inputs and draws state; the server owns rules and results. A web build is JavaScript anyone can modify.
- **One deployment = one match.** Edgegap places it near the players and bills only while it runs; no room routing or capacity planning.
- **The server stops itself.** Only the game knows the match is over; an idle deployment bills until its max duration.
- **WS + TLS Upgrade.** Web pages on `https` and mini-game platforms only open `wss://`. Edgegap terminates TLS, so the server stays plain `ws`.
- **Clients call the matchmaker, never the Deploy API.** The matchmaker Auth Token is made to ship in clients; the Edgegap API token controls the whole organization.

## How to work

- **Be the engineer.** Read the server and the Cocos scripts, write the changes, run Node, Docker and the Edgegap MCP tools, read logs. Hand the developer only account steps: signing in to the extension (or `docker login`), creating the matchmaker in the dashboard, playtesting in the editor.
- **One layer at a time**: server locally → container → one direct deployment → matchmaker → Cocos client. Each phase has a check.
- **Secrets** (full rules: [the edgegap skill's agent rules](../edgegap/references/agent-rules.md)): the Edgegap API token never goes into the client, the server image, a deployment env var, the extension's project settings, git or chat. The matchmaker Auth Token may ship in clients.
- **Money.** Ask before deploying. Tag test deployments and stop only the ones you started. Free tier: one deployment at a time.

## Phase 0: Understand the project

Read, don't ask:
- The Cocos project: `package.json` → `creator.version` (3.8.x; older versions need an upgrade first, the extension requires 3.8+), the build targets in `settings/v2/packages/builder.json` or `profiles/` (web-desktop, web-mobile, wechatgame, native), where networking lives in the project's scripts.
- The server: its folder, language, `package.json` (`ws`, `socket.io`, `uWebSockets.js`... or `colyseus` → `edgegap-colyseus`), port, how a match starts and ends, what it trusts from clients.
- Whether `extensions/edgegap-extension/` is already there, and `settings/v2/packages/edgegap-extension.json`.

Ask, in one message, only what you couldn't infer: players per match, direct mode, matchmaker or both, which platforms ship (web origins, native, WeChat/Douyin), extension or MCP/dashboard for deploying, their Edgegap account and Docker. Default: matchmaker with a `casual` profile of 2 to 8 players, plus direct mode for testing, deployed with the extension.

## Phase 1: Server, local

Read `references/server.md`.
1. If there's no server, write one (`edgegap-server-design`): `assets/server/server.mjs` is a skeleton with the protocol the client templates speak.
2. Copy `assets/server/edgegap.mjs` next to the server's entry; call `startLifecycle()` once listening, `playerJoined()` / `playerLeft()` when seats are taken and really freed, `selfStop("match over")` at match end (lock, show result ~5 s, close sockets, stop). Handle SIGTERM.
3. Listen on `PORT` (bind `0.0.0.0`); with a matchmaker, accept the client's ticket in its first message and optionally refuse unknown tickets (`REQUIRE_TICKET=1`, §5).
4. Copy `assets/server/Dockerfile` and `.dockerignore` into the server folder; fix `COPY` and `CMD` for the real entry (node as PID 1).

✅ Check: the server runs as before locally; `docker build --platform linux/amd64` then `docker run -p 7777:7777 -e ARBITRIUM_REQUEST_ID=local -e EMPTY_TIMEOUT_S=10`: a client joins, leaves, and the log shows `[edgegap] self-stop: empty for 10s` and the container exits.

## Phase 2: Image, app version, one direct deployment

Read `references/extension.md`. Pick the path the developer wants:
- **Extension** (§2 to §5): copy the repo into `extensions/edgegap-extension/`, write `settings/v2/packages/edgegap-extension.json` from `assets/settings/edgegap-extension.json` (server folder, image, app, tag, port WS + TLS Upgrade named `gameport`). The developer enables it, opens **Extension → Edgegap → Open Panel**, signs in with **Get a token** (a quick-start token; a regular API token needs the Container Registry login typed in), then Build image → Run locally → Push image and create version → Deploy near me. Then you set `restart_policy: "never"` on the version with `edgegap_update_app_version` (the extension doesn't set it).
- **MCP / dashboard** (§7): build and push a UTC `YYYYMMDD-HHMM` tag, `edgegap_create_app` + `edgegap_create_app_version` (port = server `PORT`, protocol `WS`, name `gameport`, `tls_upgrade: true`, 256 CPU units / 512 MB, max duration 30–60, `restart_policy: "never"`), the developer adds registry credentials, ask, `edgegap_deploy` near the tester → `edgegap_wait_for_deployment`.

✅ Check: a client joins `wss://<fqdn>:<external>` (web build with `?server=`, or a Node bot), `edgegap_get_deployment_logs` during the match shows `[edgegap] deployment <id> ... match=direct`, and after the players leave the deployment stops itself and leaves `edgegap_list_deployments`. Don't add the matchmaker on an unproven server.

## Phase 3: Matchmaker

1. Start from `assets/matchmaker/casual.json`: `application.name`/`version` = the version above, team sizes, `allowed_cors_origins` with every web origin (Cocos preview `http://localhost:7456`, the hosted page). Profiles, teams, regions, backfill: `edgegap-matchmaking`.
2. The developer creates it in the dashboard (Matchmaker → Create → upload → **Create and Start**) and copies the **API URL** and **Auth Token**.

## Phase 4: Cocos client

Read `references/client.md`. Copy `assets/client/Matchmaker.ts`, `GameSocket.ts` and `EdgegapConnect.ts` into the project's scripts, `npm i @edgegap/sdk` in the project root, attach `EdgegapConnect` (or wire its logic into the game's own network code) so:
- `?server=wss://...` wins, then the matchmaker (`?mm=&mmToken=` or Inspector fields), then `ws://localhost:<port>`;
- the client connects to `wss://<fqdn>:<port>` by FQDN and retries the first connection (a fresh deployment refuses for a few seconds);
- it sends its ticket ID in `hello`, sends inputs not results, and cancels the ticket when the player quits while searching.

Shipping native or mini-game builds: read `references/platforms.md` first. WeChat and Douyin only allow listed `wss` domains, and per-deployment hostnames can't be listed in advance.

## Phase 5: End-to-end test and hand-off

1. `edgegap_list_deployments`: nothing of yours left running (free tier: a leftover blocks matchmaker deployments).
2. Two clients (a Cocos web build in the foreground tab plus a second tab or a bot) click Play within the expiration window: both land on one deployment, the server log shows both tickets, they play, the match ends, the deployment stops itself.
3. Debug with `references/troubleshooting.md`.

Hand-off: what changed where; app, version and matchmaker names; how to ship a new build (extension: Now → Build → Push; or new tag → `edgegap_update_app_version`; matchmaker Stop → Edit → Start when the version name changes); what wasn't tested (this skill end to end, the panel GUI, native and mini-game builds); before launch: `inspect: false`, real origins only, `REQUIRE_TICKET=1`, max duration fitted to matches, `edgegap-launch`.

## Reference files

- `references/server.md`: what the server is in a Cocos game, the shape Edgegap needs, lifecycle module, wiring a ws server, ticket check, image, other languages, local checks.
- `references/extension.md`: the Cocos extension (install, preset, panel flow, tokens, headless e2e, what it sets), the MCP/dashboard path, shipping updates.
- `references/client.md`: client files, where to connect, wss by FQDN and retry, Find Match with `@edgegap/sdk`, CORS, builds.
- `references/platforms.md`: web, native wss, WeChat and Douyin domain allowlists and what they mean for per-deployment hostnames.
- `references/troubleshooting.md`: symptom → fix.
- `assets/`: `server/` (lifecycle, skeleton ws server, Dockerfile), `client/` (matchmaker wrapper, game socket, example component), `settings/` (extension preset), `matchmaker/`.

Related skills in this pack, if installed: `edgegap` (platform and safety rules), `edgegap-server-design`, `edgegap-containerize`, `edgegap-local-testing`, `edgegap-matchmaking`, `edgegap-deployments-api` (a backend that deploys servers itself), `edgegap-colyseus` (the server is Colyseus), `edgegap-threejs` (browser games in other engines), `edgegap-troubleshoot`, `edgegap-launch`.

Sources of truth: https://github.com/edgegap/buildtool-cocos-plugin, https://docs.cocos.com/creator/3.8/manual/en/, https://docs.edgegap.com/learn/orchestration/deployments, https://docs.edgegap.com/learn/matchmaking, https://github.com/edgegap/sdk-js-sessions-matchmaker-server-browser.

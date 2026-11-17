---
name: edgegap-threejs
description: 'Three.js / browser game + Edgegap: make a JavaScript web game multiplayer with an authoritative Node.js WebSocket server per match and the Edgegap matchmaker called from the page, end to end. Load this before using any Edgegap MCP tool on a Three.js, Babylon.js, PlayCanvas engine, Phaser or plain canvas/WebGL game that has (or needs) its own ws server rather than Colyseus or Nakama. Templates verified on Edgegap with five Three.js games (shooter, racer, 2v2 soccer, light cycles, sumo): a room with phases, bots, fixed tick and snapshots, self-stop, matchmaker teams, a no-build Three.js client with Find Match on the Edgegap JS SDK, wss retry, Dockerfile, WS + TLS Upgrade versions, one image for several games, a multi-profile matchmaker config, headless e2e scripts. Use for "make my three.js game multiplayer", "host my browser game server", "Find Match for a web game", "wss from an https page", "several mini-games on one matchmaker", or debugging them. Colyseus: edgegap-colyseus; Manus: edgegap-manus.'
metadata:
  version: "0.3.6"
---

# Edgegap for Three.js and other browser games: one Node.js server per match

Goal: a browser game where each match runs on its own authoritative Node.js server on Edgegap, near its players. Players click **Find match**, the page asks Edgegap's matchmaker for a ticket through the official Edgegap JS SDK ([`@edgegap/sdk`](https://github.com/edgegap/sdk-js-sessions-matchmaker-server-browser)), the matchmaker starts a server and returns `wss://<id>.pr.edgegap.net:<port>`, everyone plays, and the server stops its own deployment when the match is over. Done means real clients played a whole match on one Edgegap deployment that then stopped itself, not that the image builds.

```
browser --@edgegap/sdk GroupAgent: POST /groups {profile}--> Edgegap Matchmaker --deploys the profile's app version near the players--> Edgegap
browser <--HOST_ASSIGNED {fqdn, ports.gameport.link}, ticket_id--
browser --wss://<fqdn>:<port>, hello{name, ticket}--> Node.js server (one per match) --DELETE $ARBITRIUM_DELETE_URL--> stopped
```

Verified on Edgegap on 2026-10-22 with [netcode-sample-threejs-minigames](https://github.com/edgegap/netcode-sample-threejs-minigames): five Three.js games (top-down shooter, kart racer, 2v2 soccer with matchmaker teams, light cycles, sumo brawler) from one image, one app version per game and one matchmaker with a profile per game. Headless players queued through the matchmaker landed on one deployment per game, played full matches over `wss` with TLS Upgrade, and every deployment stopped itself about 17 s after its match; deployments whose matched players never connected stopped after 120 s; a direct deployment (no matchmaker) did the same. The templates in `assets/` are that repo's shared files plus a skeleton game. Not run on Edgegap: Babylon.js/PlayCanvas/Phaser clients (the server and matchmaker parts don't depend on the renderer), mobile browsers, latency rules. Say so when those matter.

The matchmaker client, the e2e tool and the server's `ARBITRIUM_*`/`MM_*` parsing use the Edgegap JS SDK (`@edgegap/sdk` 1.1.0) since skill 0.2.0, checked locally with the skeleton game on 2026-11-02 (`MM_*` parsing, `REQUIRE_TICKET=1` refusing an unknown ticket, matchmaker teams, a full match and the self-stop request) and end to end on Edgegap the same day with the skeleton game and `REQUIRE_TICKET=1`: two headless players through `tools/e2e.mjs` landed on one deployment, played a full match over `wss` and the deployment stopped itself 17 s after it; a browser Find Match from `http://localhost:8080` (import map with the SRI hash) was matched alone after the 20 s expansion, joined with its ticket, played against a bot and the deployment stopped itself.

Why this shape, so you can defend it:
- **Authoritative server, thin client.** The browser sends inputs and draws snapshots; the server owns movement, hits, scores and the match end. Anything decided in browser JavaScript can be read and changed by any player in devtools.
- **One deployment = one match.** Edgegap places it near the players and bills it only while it runs. No room routing, no capacity planning.
- **The server stops itself.** Only the game knows the match is over; an idle deployment otherwise bills until its max duration.
- **WS + TLS Upgrade.** Pages on `https` can only open `wss://`. Edgegap terminates TLS on the port, so the Node server stays plain `ws`, and the client connects by FQDN so the certificate matches.
- **The browser calls the matchmaker, never the Deploy API.** The matchmaker Auth Token is made to ship in clients; the Edgegap API token controls the whole organization. Add a backend in between only when players must sign in first (`edgegap-supabase` does it with Supabase Auth and Edge Functions; `edgegap-manus` with Steam).

## How to work

- **Be the engineer.** Read the game, write the server and client changes, run Node, Docker and the Edgegap MCP tools, read logs. Hand the developer only account steps: `docker login`, creating the matchmaker in the dashboard, playtesting.
- **One layer at a time**: game on a local server → container → one direct deployment → matchmaker → browser. Each phase has a check.
- **Secrets** (full rules: [the edgegap skill's agent rules](../edgegap/references/agent-rules.md)): the Edgegap API token never goes in a page, the image, a deployment env var, git or chat. The matchmaker Auth Token may ship in the page.
- **Money.** Ask before deploying. Tag test deployments and stop only the ones you started. Free tier: one deployment at a time.

## Phase 0: Understand the game

Read, don't ask:
- The client: renderer (Three.js, Babylon.js, PlayCanvas engine, Phaser, canvas), bundler or none, where the game loop and input live, whether there is any networking yet (none, a host-in-the-browser WebRTC/PeerJS setup, a hosted service, an existing `ws` server).
- If a server exists: framework (plain `ws`, `socket.io`, `uWebSockets.js`, Colyseus → `edgegap-colyseus`), what it decides vs trusts from clients, how a match ends.
- Where pages are served (localhost, itch.io, GitHub Pages, own domain): every origin goes into the matchmaker's CORS list.

Ask, in one message, only what you couldn't infer: players per match, teams, whether a lone player should get a match (bots), the origins of the pages, their Edgegap account and Docker. Default: free-for-all, 2 to 8 players, a lone player gets a match after 20 s with bots.

## Phase 1: Authoritative server, local

Read `references/server.md`.
1. Copy `assets/server/` (`main.js`, `room.js`, `edgegap.js`, `util.js`) into the project's `server/`, add `"type": "module"` and the `ws` and `@edgegap/sdk` dependencies to `package.json` (`npm i ws @edgegap/sdk`). The SDK needs Node 22 or later (the Dockerfile uses `node:22-slim`).
2. Write the game as `server/game.js` with the contract in `assets/server/game.js` (a working skeleton): move the rules out of the client into `update(dt)`, take only inputs from clients and validate them, send the state in `snapshot()`. Keep snapshots small (rounded numbers, only what is drawn).
3. Decide bots (`botFill` or `botsNeeded`) so a lone or short-handed match is still a game.

**A single-player game (often vibe-coded) that runs its rules in the browser** (`edgegap-vibe-coded` covers the steps around this one: whether the game holds up online, getting it out of Lovable or Bolt, a public demo): don't rewrite the rules for the server. Move them into one DOM-free module (no `window`, `document` or Three.js: plain state, `step(world, dt)`, bot logic), have the page import it for solo play and `server/game.js` import the same file, and copy that file into the image (`server.md` §9). Solo mode keeps working offline, the server is authoritative online, and the rules can't drift apart. The same bot logic then drives the headless test players, so tests score goals instead of wandering until time runs out.

✅ Check: `node server/main.js` plus two headless players (`assets/tools/headless-player.mjs`, a 20-line script with short `WAIT_SECONDS`/`MATCH_SECONDS`) go `waiting → countdown → playing → over` with a result, and the room loops back to `waiting` (off Edgegap nothing stops).

## Phase 2: Browser client

Read `references/client.md`. Either copy `assets/client/` (`shell.js` gives the menu, Find Match, Local server, `?server=` direct mode, HUD, interpolation helpers; `game-client.js` is the skeleton's renderer) or wire `net.js` and the Find Match block of `shell.js` (the Edgegap JS SDK's `GroupAgent`, about 15 lines, quoted in `client.md` §5) into the game's own UI. The client must:
- send `{t:"hello", name, ticket}` first, then inputs at most ~30/s;
- render by easing toward the latest server state (no client-side rules);
- retry the first WebSocket connection (a fresh deployment refuses for a few seconds after `HOST_ASSIGNED`);
- leave the queue on Cancel and `pagehide` (the SDK retries `429`/`5xx` with backoff);
- take the matchmaker URL/token from `config.js`, `config.local.js` or `?mm=&token=`, and `?server=wss://...` for direct mode.

✅ Check: two browser tabs on **Local server** play together and see the same state.

## Phase 3: Image, app version, one direct deployment

Read `references/deploy.md` §1 to §3.
1. `docker build --platform linux/amd64` (`assets/server/Dockerfile`), push a unique tag (UTC timestamp `YYYYMMDD-HHMM`, also the app version name), never `latest`. Before the first push, run the container checks of `edgegap-local-testing` ([`parity.sh`](../edgegap-local-testing/assets/parity.sh) does them in one go). `docker login registry.edgegap.com` is the developer's: `edgegap_get_registry_credentials` returns nothing with a regular API token, so ask for the Container Registry login (or check `docker` is already logged in) instead of retrying it.
2. `edgegap_create_app` + `edgegap_create_app_version`: port `7777`, protocol **WS**, name `gameport`, `tls_upgrade: true`; 256 CPU units / 512 MB; max duration 30–60; `restart_policy: "never"` (the server ends its match by stopping itself; a crash should not restart a half-played match). When the matchmaker will stay up and every deployment must stop soon after its players leave, also set the quick-stop env vars (`server.md` §7), `IDLE_TIMEOUT_S=75` among them (closed tabs can keep their sockets open for minutes), and keep the client heartbeat in `net.js`, or players who only switched tabs get dropped. No registry login: the tool sends `registry_profile: "Edgegap"`; check `registry_credentials_set: true` with `edgegap_list_app_versions`. Several games: one image, one version per game with a `GAME` env var (§2).
3. Ask, then `edgegap_deploy` with the player's public IP and a test tag → `edgegap_wait_for_deployment` → `wss://<fqdn>:<external>`. Or the developer runs `assets/server/edgegap-deploy.mjs` with their own token.

✅ Check: `SERVER_URL=wss://<fqdn>:<external> node tools/e2e.mjs` (direct mode: no matchmaker, no tickets) plays a whole match on it and sees the deployment stop itself; or open the page with `?server=`. Read `edgegap_get_deployment_logs` while the match is still on: it shows `direct deploy` and the phases, and the logs are gone once the deployment stops. Don't add the matchmaker on an unproven server.

## Phase 4: Matchmaker

Read `references/deploy.md` §4.
1. Start from `assets/matchmaker/casual.json` (one game) or `several-games.json` (a profile per game, one with `team_count: 2`). Profile name = the client's `game`/`profile`. `allowed_cors_origins` = every page origin, scheme + host + port. Keep the expansion that lets a lone player in after 20 s if the game has bots.
2. The developer creates it in the dashboard (Matchmaker → Create → upload → **Create and Start**) and pastes the **API URL** and **Auth Token**. Check `GET <url>/monitor` with the token answers 200.

## Phase 5: End-to-end test and hand-off

1. `edgegap_list_deployments` for the app: nothing of yours left running.
2. `MM_URL=... MM_TOKEN=... node tools/e2e.mjs <profile> <players>` (`assets/tools/e2e.mjs`, with a `makeInput` that plays the game): all players on one deployment, the server saw the tickets (`welcome.match.players`), a result, then self-stop. Run games a few seconds apart: bursts of ticket calls get `429`.
3. Two real browser tabs (localhost origin, then the hosted page's origin) click **Find match** within 20 s and land in the same match. Idle tabs lose to the bots: with a score limit the match can end in about a minute, which is the server working, not a crash.
4. Debug with `references/troubleshooting.md`.

Shipping (optional, `deploy.md` §5): `assets/ci/server-image.yml` builds and pushes the image on every push to `main`, `assets/ci/pages.yml` publishes the page on GitHub Pages. The developer sets the registry secrets (`gh secret set ...`); never pass them through chat or files.

Hand-off: what changed where; app, versions and matchmaker names; how to ship a new build (new tag → `edgegap_update_app_version` on each version, or new versions + matchmaker Stop → Edit → Start); what wasn't tested (two players on different networks is the developer's test); before launch: `inspect: false`, real origins only, `REQUIRE_TICKET=1` if only matched players may join, `edgegap-launch`.

## Reference files

- `references/server.md`: the room contract, phases and timers, authoritative simulation and input validation, bots, matchmaker env (`MM_TICKET_IDS`, teams), self-stop, the wire protocol.
- `references/client.md`: no-build Three.js with an import map, the shell, interpolation, input sending, Find Match flow, direct mode, CORS, other renderers.
- `references/deploy.md`: image, app versions (WS + TLS Upgrade, one image for several games), direct deployments, matchmaker profiles and the ticket API, rate limits, shipping updates, CI and GitHub Pages.
- `references/troubleshooting.md`: symptom → fix.
- `assets/`: `server/` (entry, room, lifecycle, utils, skeleton game, Dockerfile, deploy script), `client/` (shell, matchmaker, net, skeleton client and page), `matchmaker/`, `tools/` (headless player, e2e with matchmaker and direct modes), `ci/` (image build, GitHub Pages).

Related skills in this pack, if installed: `edgegap` (platform and safety rules), `edgegap-server-design`, `edgegap-containerize`, `edgegap-deployments-api` (a backend that deploys servers itself), `edgegap-colyseus` (the server is Colyseus), `edgegap-manus` (Manus games, Steam sign-in, backend-owned tickets), `edgegap-supabase` (Supabase sign-in, profiles, leaderboard, results), `edgegap-troubleshoot`, `edgegap-launch`.

Sources of truth: https://docs.edgegap.com/learn/orchestration/deployments, https://docs.edgegap.com/learn/matchmaking, https://threejs.org/docs, https://github.com/edgegap/netcode-sample-threejs-minigames.

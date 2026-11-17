---
name: edgegap-nakama
description: 'Nakama + Edgegap: keep Nakama for accounts, matchmaking and leaderboards, and run every match on its own Edgegap dedicated server near the players through the Edgegap Fleet Manager for Nakama (nakama-edgegap), end to end. Load this before using any Edgegap MCP tool on a project with a Nakama backend (a Go, TypeScript or Lua Nakama module, heroiclabs/nakama images, a Nakama client SDK: nakama-godot, nakama-unity, nakama-js). Engine-agnostic templates verified on Edgegap with Fish Game (Godot 4.7, Nakama 3.39): the Go module (Fleet Manager, AfterAuthenticate hook for the real sign-in method, MatchmakerMatched hook, notifications 111/112/113, a leaderboard only the server writes), game server code for READY, connection events, STOP and player checks, Dockerfile, compose. Use for "host my Nakama game on Edgegap", "Nakama matchmaker should start a dedicated server", "replace Nakama relayed matches", "Heroic Cloud plus Edgegap", or debugging nakama-edgegap. Unity servers: edgegap-server-nakama-plugin-unity.'
metadata:
  version: "0.2.2"
---

# Edgegap for Nakama games: Nakama matches players, Edgegap runs the match

Goal: Nakama keeps doing what it does (accounts, matchmaker, leaderboards, storage), and each match it forms gets its own dedicated game server on Edgegap, placed near the matched players. The server reports back to Nakama, players are told where to connect, the server writes results that players can't fake, and it stops its own deployment. Done means two real clients signed in, were matched, played on one Edgegap deployment, saw the result in Nakama, and the deployment stopped, not that the module compiles.

```
Player --sign in--> Nakama (AfterAuthenticate hook stores the player's public IP)
Player --matchmaker ticket--> Nakama --MatchmakerMatched hook--> Fleet Manager --deploy (player IPs)--> Edgegap
Game server boots, listens --READY + its own IP/port--> Nakama --notification 111 {IpAddress, Port}--> each player
Player --game protocol + Nakama session token--> game server --GET /v2/account--> Nakama (is this a matched player?)
Game server --connection events (batched)--> Nakama
Match over --report_match_result (S2S RPC)--> Nakama leaderboard;  --STOP--> Nakama --> Edgegap stops the deployment
```

This path was run end to end on Edgegap on 2026-10-20 with [edgegap/backend-game-sample-godot-nakama-fishgame](https://github.com/edgegap/backend-game-sample-godot-nakama-fishgame) (branch edgegap-integration, guide EDGEGAP.md): Heroic Labs' Fish Game ported to Godot 4.7.2, Nakama 3.39.0, [backend-nakama-edgegap-plugin](https://github.com/edgegap/backend-nakama-edgegap-plugin) at commit `20d849e`, Nakama reached through a Cloudflare quick tunnel. Verified: email sign-up, matchmaking, a deployment near the players, 5 server-decided rounds, a leaderboard win written by the server, a player's attempt to post a win refused, and the server stopping itself. The templates in `assets/` are that run's files with the game-specific parts taken out. On 2026-11-02 the templates moved to Nakama 3.41.0, nakama-common v1.48.0 and the plugin at `cd9022a` (its Nakama 3.41 upgrade, edgegap/backend-nakama-edgegap-plugin#12): the module built with `nakama-pluginbuilder:3.41.0`, Nakama 3.41.0 loaded it, registered every RPC and hook, signed in a player by email and refused that player's `report_match_result`, against a mock Edgegap API. Matchmaking into a real deployment was not re-run on 3.41. Not run: other Nakama auth methods than email, TypeScript or Lua Nakama modules, Heroic Cloud, the Node game server template on Edgegap (mock Nakama only), WebSocket game servers, Nakama clusters. Say so when those matter.

Why this shape, so you can defend it:
- **Nakama stays the backend; Edgegap replaces the match host.** Relayed matches (`NakamaMultiplayerBridge`, Nakama relayed multiplayer) make one player the host: they can cheat, everyone else gets two hops, and the match dies when they quit. Nakama authoritative matches run the game loop inside Nakama, in Go/TS/Lua, one region for everyone. An Edgegap server runs the real game build near the players.
- **The Fleet Manager does the Edgegap calls.** It holds the Edgegap API token inside Nakama, deploys with the players' IPs, injects callback URLs into the server, tracks instances and stops deployments. Clients never touch Edgegap.
- **The server reports READY itself.** Nakama only tells players where to connect when the server says it is listening, so nobody connects to a server that isn't up.
- **Results come from the server.** An authoritative leaderboard plus an S2S RPC means a modified client can't post wins.

## How to work

- **Be the engineer.** Read the Nakama module, the client's Nakama code and the game server; write the changes; run Docker, Nakama, the game and the Edgegap MCP tools; read logs. Hand the developer only account steps: the Edgegap API token into `.env`, `docker login`, starting a tunnel or giving a public Nakama URL, playtesting.
- **One layer at a time**: game server runs locally → image → one direct Edgegap deployment → Nakama module → client → end to end. Each phase has a check.
- **Secrets** (full rules: [the edgegap skill's agent rules](../edgegap/references/agent-rules.md)): the Edgegap API token lives only in Nakama's runtime env (`.env`, Heroic Cloud settings), never in a client, the game server image, git or chat. The Nakama `http_key` is also server-only: the game server gets it inside the injected URLs, never set it on the app version. Never run the compose entrypoint with `sh -x`: it prints both.
- **Money.** Ask before deploying. Each Nakama match starts a deployment. Tag your direct test deployments, stop only what you started. Free tier: one deployment at a time.

## Phase 0: Understand the project

Read, don't ask:
- The Nakama module: language (Go plugin, TypeScript/JS, Lua), Nakama version (Dockerfile or compose image tag), existing hooks (`RegisterMatchmakerMatched`, `registerMatchmakerMatched`), authoritative matches, leaderboards, RPCs.
- How players sign in (`authenticate_email`, `_device`, `_custom`, `_steam`...): the AfterAuthenticate hook must match.
- How a match is played today: relayed (`NakamaMultiplayerBridge`, `socket.joinMatch` with a matchmaker token), authoritative Nakama match, or player-hosted. Who decides hits, deaths and the winner.
- The game server: engine, whether a headless server build exists, its transport (ENet/UDP, WebSocket, TCP) and port, how clients identify themselves.
- Where Nakama runs (local compose, a VM, Heroic Cloud) and whether it has a public HTTPS URL.

Ask, in one message, only what you couldn't infer: players per match, whether the game server already exists or has to be written (scope it honestly: moving the match from a host or from Nakama to a real server is the biggest piece), their Edgegap account, where Nakama will be public. Default: Nakama's matchmaker with min 2, max 4, one Edgegap server per match.

## Phase 1: The game server, locally

Read `references/game-server.md`. The server needs a dedicated mode (headless, no player), its own listen port, and:
1. The Nakama/Edgegap contract: copy `assets/game-server/godot/nakama_edgegap_server.gd` (Godot 4, verified), `assets/game-server/node/nakamaEdgegap.ts` (Node), or port it. Unity: use [backend-nakama-unity-template-model](https://github.com/edgegap/backend-nakama-unity-template-model) on the server instead (and `edgegap-unity` for the server build).
2. Wire it: `send_ready` once listening; check each connecting player's Nakama token with `verify_player` and reject anyone not in `user_ids`; `set_connected_users` on every join/leave; at match end `report_result` then `stop`.
3. Move the decisions that matter (hits, deaths, rounds, winner) to the server.

✅ Check: the server runs headless with no Nakama env, two clients connect straight to it (`--connect=127.0.0.1:<port>` or similar) and play a match, and the server quits at match end.

## Phase 2: Image, app version, one direct deployment

Read `references/infra.md` §1 to §2.
1. Server Dockerfile for the engine (`edgegap-containerize`; Godot: the sample's `server/Dockerfile`), `docker build --platform linux/amd64`, the developer runs `docker login registry.edgegap.com`, push a new tag (UTC timestamp `YYYYMMDD-HHMM`, also the app version name).
2. `edgegap_create_app` + `edgegap_create_app_version`: the game port with its protocol (UDP for ENet), name `gameport`; 0.5 vCPU / 512 MB to start; max duration 30 to 60. No env vars needed: the Fleet Manager injects them. No registry login: the tool sends `registry_profile: "Edgegap"`; check `registry_credentials_set: true`.
3. Ask, then one direct `edgegap_deploy` with a test tag. With no Nakama env the server lets anyone in: connect a client to `<ip>:<external port>`.

✅ Check: a client plays on the deployment and the deployment stops after the match (or stop it). Don't add Nakama on an unproven server.

## Phase 3: Nakama with the Fleet Manager

Read `references/nakama-module.md` and `references/infra.md` §3 to §4.
1. Copy `assets/nakama/` (`main.go`, `go.mod`, `go.sum`, `Dockerfile`, `docker-compose.yml`, `.env.example`, `.gitignore`, `.dockerignore`) into the project's `nakama/` folder, or merge `main.go` into an existing Go module. TypeScript/Lua modules: add the Go module next to them and move the matchmaker hook to Go (`references/nakama-module.md` §6).
2. Adapt: the AfterAuthenticate hook for each auth method the game uses; the leaderboard ID (an existing client-writable board must be deleted and recreated, `references/nakama-module.md` §5); the match result payload; anything extra the server needs in `metadata`.
3. Keep the Nakama, `nakama-pluginbuilder` and `nakama-common` versions matched, and `nakama-edgegap` pinned by pseudo-version.
4. Public HTTPS for Nakama: the real host, or for a test the developer runs a quick tunnel. `NAKAMA_ACCESS_URL` = that `https://` URL. `.env` from `.env.example`, then `docker compose up -d --build`.

✅ Check: Nakama's log shows the module loaded and no error from the Fleet Manager; `get_edgegap_version` (S2S, `references/infra.md` §4) returns the version.

## Phase 4: Client

Read `references/clients.md`. Point the client's Nakama connection at the **public** URL (the tunnel or real host, port 443, `https`), so Nakama sees the players' public IPs. Then: authenticate → open the socket → add a matchmaker ticket → on notification 111 connect to `IpAddress:Port` and send the session token to the server; 112/113 → show an error and go back to the menu. Remove relayed match joining (`join_matched_async`, the multiplayer bridge) for these matches.

## Phase 5: End-to-end test and hand-off

1. `edgegap_list_deployments`: nothing of yours left running.
2. Two clients with different accounts → Match. Nakama log: `Edgegap instance <id> ready at <ip>:<port>`; both clients land on the same server; the server log shows both users accepted.
3. Play to the end: the result appears in Nakama (leaderboard), the server sends STOP, the deployment disappears. A player-session call to `report_match_result` is refused.
4. Debug with `references/troubleshooting.md`.

Hand-off: what changed where, app/version names, how to ship a new server build (new tag → new app version → `update_edgegap_version` S2S RPC, no Nakama restart), what wasn't tested, the plugin's client RPCs that any signed-in player can call (`references/nakama-module.md` §7), why `NAKAMA_ACCESS_URL` must be public HTTPS (Edgegap webhooks and every game server call Nakama back at it), and before launch: a real public Nakama URL with TLS, the tunnel gone, max duration fitted to matches, `edgegap-launch`.

## Reference files

- `references/nakama-module.md`: the Go module piece by piece: Fleet Manager, auth hooks, the matchmaker hook and what the plugin README gets wrong, notifications, server-written results, TypeScript/Lua modules, the plugin's own RPCs and their risks.
- `references/game-server.md`: the server contract (env vars, READY with `game_server`, connection events, STOP, ERROR, player checks, S2S calls with the injected `http_key`), lifecycle, local testing without Nakama, the Unity plugin.
- `references/infra.md`: server image and app version, Nakama Dockerfile and compose, `.env`, public HTTPS and tunnels, version updates, production Nakama.
- `references/clients.md`: client flow and notification handling, public Nakama URL, examples from the Godot sample.
- `references/troubleshooting.md`: symptom → fix.
- `assets/`: `nakama/` (Go module, go.mod/go.sum, Dockerfile, compose, `.env.example`), `game-server/godot/` (verified), `game-server/node/`.

Related skills in this pack, if installed: `edgegap` (platform and safety rules), `edgegap-server-design` (what a match-scoped server must do), `edgegap-containerize` (the game server image), `edgegap-unity` (Unity server builds; pair with the Unity Nakama plugin), `edgegap-unreal`, `edgegap-deployments-api` (a backend other than Nakama that deploys servers), `edgegap-troubleshoot`, `edgegap-launch`.

Sources of truth: https://github.com/edgegap/backend-nakama-edgegap-plugin (read the code at the pinned commit when the README and behaviour differ), https://heroiclabs.com/docs/nakama/, https://docs.edgegap.com/learn/orchestration/deployments, https://github.com/edgegap/backend-game-sample-godot-nakama-fishgame.

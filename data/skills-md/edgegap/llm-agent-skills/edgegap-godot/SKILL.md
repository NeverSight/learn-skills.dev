---
name: edgegap-godot
description: 'Godot 4 + Edgegap: take a Godot multiplayer game (MultiplayerAPI, @rpc, ENetMultiplayerPeer, WebSocketMultiplayerPeer, MultiplayerSpawner, netfox) to dedicated servers and matchmaking, end to end. Load this before using any Edgegap MCP tool on a Godot project (project.godot, .gd, .tscn, export_presets.cfg). It has tested GDScript templates (a server lifecycle autoload that waits for the matched players and stops its own deployment, a matchmaker client and Find Match button), the Edgegap Godot plugin build (export, image, push from the editor), app version ports (UDP for ENet, WS + TLS Upgrade for web and wss), matchmaker config, and fixes for Godot pitfalls: empty server logs, export allowlists that drop new scripts, join validation that silently blocks matched players. Use when a Godot dev wants online play: "host my Godot game", "nobody should host", "Find Match button", "Godot web multiplayer", or is debugging Godot deployments, ports or matchmaking on Edgegap.'
metadata:
  version: "0.2.4"
---

# Edgegap for Godot 4: dedicated servers + matchmaking

Goal: a player clicks **Find Match**, the Edgegap matchmaker starts a headless Godot server near the matched players, every client joins it, the server starts the match when they're all in, and it stops its own deployment when the match is over. Done means that loop works with real exports, not that the scripts parse.

Where this comes from:
- [edgegap/game-sample-godot-arena-shooter](https://github.com/edgegap/game-sample-godot-arena-shooter) (Godot 4.7.2, server-authoritative, `WebSocketMultiplayerPeer` on port 7000) ran end to end on Edgegap on 2026-10-20: two Windows clients pressed FIND MATCH, were matched onto the same deployment over `wss://` (TLS Upgrade), played, and the deployment stopped itself. Its `EDGEGAP.md` is a working reference. On 2026-10-28 it moved to the Edgegap Godot plugin's build: its preset and the plugin's default Dockerfile, unchanged, ran in a local container and on an Edgegap deployment: two `wss://` clients played a match and the deployment stopped itself.
- The templates in `assets/godot/edgegap/` are that sample's server lifecycle and matchmaker client made game-agnostic. They were tested on 2026-10-20 with Godot 4.7.2 in a minimal project: a Linux dedicated server export in Docker, a fake matchmaker and two clients, with both ENet (UDP) and WebSocket. Two tickets → assignment → both clients joined → `match_ready` → `match_ended` → self-stop call with the raw token. ENet on a real Edgegap deployment wasn't run yet: prove it with Phase 4 before adding the matchmaker.

Use **dedicated (authoritative) servers**, not a player host, unless the developer explicitly wants host/client.

## How to work

- **Be the engineer.** Read the project, write the code, run Godot exports, Docker and the Edgegap MCP tools, read the logs. Hand the developer only editor clicks, dashboard steps, secrets and playtesting.
- **Touch the game as little as possible.** The templates live in `res://edgegap/` and hook in with an autoload plus a few lines where the game starts its server and ends a match. That keeps upstream merges easy.
- **One layer at a time**: local (editor binary) → exported server in Docker → direct Edgegap deploy → matchmaker, each with a check.
- **Secrets.** The Edgegap API token and registry token never go into project files, git, the client, `export_presets.cfg` or chat. The matchmaker Auth Token is client-safe.
- **Money.** Tag test deployments and stop the ones you start. Free tier runs one deployment at a time.
- Track the phases as a todo list.

## Phase 0: Understand the project

Read, don't ask (`references/godot.md` §1 has the grep list):
- `project.godot`: Godot version (`config/features`), autoloads, main scene, `application/run/flush_stdout_on_print`. Godot 3 (`NetworkedMultiplayerENet`) is out of scope for the templates; the Edgegap side is the same.
- Who runs the server: a Godot client talking to a Colyseus (Node.js) server is `edgegap-colyseus`, not this skill.
- Who matches players: a Godot game whose accounts and matchmaking live in Nakama (the Edgegap Fleet Manager for Nakama starts its servers) is `edgegap-nakama`, which has its own Godot server template.
- How the game goes online: `ENetMultiplayerPeer` (UDP) or `WebSocketMultiplayerPeer` (TCP), `create_server` / `create_client`, the port, `multiplayer.multiplayer_peer =`, custom `MultiplayerAPI` branches (`set_multiplayer`). WebRTC or noray/NAT punch-through means peer-to-peer today: the server path replaces it.
- Host assumptions: a Host button that also spawns a local player for peer 1, `multiplayer.is_server()` used as "I'm a player too", UI, camera or audio code on the server, a lobby or Start button the host presses (`references/godot.md` §3).
- `export_presets.cfg`: existing presets, `export_filter` (`all_resources` or an explicit allowlist), custom features, any build script that writes presets.
- Targets: desktop clients can use ENet or WebSocket; **web exports can only use WebSocket**, with `wss://` when the page is on https.

Then ask, in one message, only what you couldn't infer: players per match, platforms, Edgegap account and Docker. Offer defaults.

## Phase 1: Make the game dedicated-server ready

Read `references/godot.md` §2-§5.
1. Copy `assets/godot/edgegap/*.gd` to `res://edgegap/`. Register `res://edgegap/edgegap_server.gd` as an autoload named `EdgegapServer`.
2. In `edgegap_settings.gd` set `TRANSPORT`, `PORT` (the game's port) and `USE_TLS` (WebSocket with TLS Upgrade).
3. Server start: where the game creates its server peer, call `EdgegapServer.begin(multiplayer)` after setting it, or let `EdgegapServer.host()` create it. In a server launch (`EdgegapServer.is_server_launch()`), the main scene starts the server at boot without a host player, and connects `EdgegapServer.match_ready` to whatever the host's Start button did.
4. Match end: call `EdgegapServer.match_ended()` when the game decides the match is over (results screen, round limit). One match per deployment; players queue again.
5. Turn on `application/run/flush_stdout_on_print=true`, or the server's logs stay empty in Docker and on Edgegap (§5).
6. Fix host-only logic: no player for peer 1 on a dedicated server, spawns for remote peers, client-only code guarded (§3).

✅ Check: `godot --headless --path . -- --server` logs `EDGEGAP listening ...` and `EDGEGAP ready ...`; two clients (`godot --path .` twice, or with `--headless` and a test env var) connect to `127.0.0.1:<port>`; the server logs `player_joined` twice and the game's server-side content runs. With `MM_TICKET_IDS='["a","b"]'` set, `match_ready players=2` fires as soon as the second joins.

## Phase 2: Install the Edgegap plugin and connect

The [Edgegap Godot plugin](https://github.com/edgegap/buildtool-godot-plugin) (1.0.10 or newer, Godot 4.3+) exports the Linux server, builds the image, tests it locally, pushes it and deploys it from an **Edgegap** editor dock. Use it instead of writing export presets, Dockerfiles and registry logins.
1. Install into `res://addons/edgegap/`: the Godot Asset Store ("edgegap"), or `git clone --depth 1 https://github.com/edgegap/buildtool-godot-plugin.git addons/edgegap` then delete `addons/edgegap/.git`. Enable it: Project Settings → Plugins, or add `[editor_plugins] enabled=PackedStringArray("res://addons/edgegap/plugin.cfg")` to `project.godot`.
2. Copy `assets/docker/.dockerignore` to the project root: the plugin builds with the whole project as context.
3. Edgegap account and Docker running. The developer pastes an Edgegap API token into the dock (it stays in their editor settings); the dock fetches registry credentials itself, so no `docker login`. Edgegap MCP connected for your part (`references/deploy.md` §1).

✅ Check: `addons/edgegap/plugin.cfg` says 1.0.10 or newer (older versions leak a token into logs and clash with game class names, `references/troubleshooting.md` §4), the editor's Output shows no `Edgegap` errors, and `edgegap_list_apps` succeeds.

## Phase 3: Export, containerize, push

The developer clicks through the dock; you only fix what it reports (`references/deploy.md` §2-§3):
1. **Validate export templates** → **Export server**. The plugin creates the `Edgegap Linux Server` preset (Dedicated Server mode, `build/edgegap-linux-server`) if it's missing. With an export allowlist, add the preset yourself first from `assets/godot/export_presets.server.cfg` with the game's filter plus `res://edgegap/*.gd` (`references/godot.md` §6); the plugin never changes an existing preset.
2. **Containerize** with **Image tag** set to a UTC timestamp `YYYYMMDD-HHMM` (also the app version name). The plugin's default Dockerfile works unchanged: a Dedicated Server export starts headless and `EdgegapServer` starts the server on `PORT`, so no arguments are needed.
3. **Deploy locally** with **Docker run parameters** `-p <PORT>:<PORT>/udp` (ENet) or `-p <PORT>:<PORT>` (WebSocket): two clients connect and `docker logs` shows the `EDGEGAP` lines.
4. **Upload** with the application name: it pushes to the Edgegap registry and opens the dashboard's new-version page. Create the version yourself in Phase 4 instead, with the right ports.

No editor at hand (CI, or the developer wants you to do it): the same build is two commands (`references/deploy.md` §2), plus `docker login` and `docker push`.

✅ Check: `edgegap_list_registry_tags` shows the tag.

## Phase 4: App version and a direct deploy

Read `references/deploy.md` §4-§5.
1. Port `gameport` = `PORT`: **UDP** for ENet; **WS** with **TLS Upgrade** on for WebSocket (`tls_upgrade: true`). Registry credentials set (`registry_credentials_set: true`; for registry.edgegap.com the tool attaches them through `registry_profile: "Edgegap"`). Push the image before creating the version.
2. `edgegap_deploy` near the developer → `edgegap_wait_for_deployment` → logs show `EDGEGAP ready edgegap=true request_id=<id>`.
3. Two clients join `<public_ip>:<external>` (ENet) or `wss://<fqdn>:<external>` (WebSocket).
4. The server stops itself (nobody joined in 120 s, everyone left for 30 s, or the match ended), or `edgegap_stop_deployment`.

✅ Check: both played on the Edgegap server and the deployment ended on its own. Don't add the matchmaker on an unproven server.

## Phase 5: Matchmaker

Read `references/matchmaker.md`.

**Steam games (GodotSteam):** a GodotSteam Server build that logs on to Steam and checks players' auth tickets needs its own Dockerfile (the plugin's default drops the GDExtension `.so` files) and `run_callbacks()` on the headless server. Read `references/godotsteam.md`; sample: [server-sample-godotsteam-dedicated-server](https://github.com/edgegap/server-sample-godotsteam-dedicated-server).
1. `assets/matchmaker/casual.json` (2-4 players, no expansion stage, tickets expire after 30 s) with the app name and version, or `edgegap_build_matchmaker_config`. Web clients: add `allowed_cors_origins`. Save as `matchmaker-config.json` in the project root and give the developer its full path.
2. Dashboard: Create Matchmaker → upload → Create and Start → copy **API URL** and **Auth Token**.
3. `GET <API URL>/monitor` with the token answers.

## Phase 6: Client integration

1. `MATCHMAKER_URL` / `MATCHMAKER_AUTH_TOKEN` / `PROFILE` in `edgegap_settings.gd`, or `EDGEGAP_MATCHMAKER_URL` / `EDGEGAP_MATCHMAKER_TOKEN` for test runs.
2. Add `EdgegapFindMatchButton` to the menu, or drive `EdgegapMatchmaker` from the game's own button (`find_match()`, `cancel()`, `status_changed`, `assigned`).
3. Joining: `EdgegapMatchmaker.join()` connects the SceneTree's `MultiplayerAPI` and retries while the server boots. If the game has its own join function with name, address or lobby fields, call it from `assigned` instead, and **fill every field it validates**: a join the game refuses fails silently and the player looks stuck searching (`references/godot.md` §4).
4. Server changed? New export → new tag → new app version → matchmaker **Stop → Edit** `application.version` **→ Start**.

## Phase 7: End-to-end test and hand-off

1. `edgegap_list_deployments`: nothing of yours left running.
2. Export the clients (desktop presets, or Web with `wss://`).
3. Two clients, **Find Match** in both (`EDGEGAP_FIND_MATCH=1` presses it at launch): searching → match found → joining → connected, both on one server. Test with two: a lone ticket may wait until it nearly expires (30 s with the template).
4. Server logs `expected_players=2`, `match_ready players=2`, `match_ended`, `stopping reason="match over"`, `self_stop ... http=200`; the deployment disappears.
5. Debug with `references/troubleshooting.md`.

Hand-off: what was built and where, app/version/matchmaker names, how to ship a new build, free-tier caveats, and next steps (validating joiners against `MM_TICKET_IDS` or the request ID, backfill, a production matchmaker tier).

## Reference files

- `references/godot.md`: reading the project, transports and ports, host → dedicated server, wiring the templates, logs, exports and allowlists, web exports, validating joiners.
- `references/deploy.md`: MCP connection, the plugin's build and its command-line equivalent, a local test with simulated Edgegap variables, app version ports (UDP / WS + TLS Upgrade), direct deploy, env vars.
- `references/matchmaker.md`: config, dashboard steps, the `/tickets` contract, injected variables, expansion stages, CORS for web clients.
- `references/troubleshooting.md`: symptom → fix tables.
- `assets/godot/edgegap/`: `edgegap_settings.gd` (`EdgegapGameSettings`), `edgegap_server.gd` (autoload), `edgegap_matchmaker.gd`, `edgegap_find_match_button.gd`. `assets/godot/export_presets.server.cfg` (the plugin's preset, for allowlists and headless exports), `assets/docker/.dockerignore`, `assets/matchmaker/`.

Related skills in this pack: `edgegap-server-design` (the lifecycle contract in any engine), `edgegap-deployments-api` for a studio's own backend or matchmaker, `edgegap-launch` before going live, `edgegap-troubleshoot` for platform-side failures.

Sources of truth: https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html, https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_dedicated_servers.html, https://docs.edgegap.com/godot, and the sample https://github.com/edgegap/game-sample-godot-arena-shooter.

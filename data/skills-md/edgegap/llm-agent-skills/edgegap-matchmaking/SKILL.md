---
name: edgegap-matchmaking
description: 'Design matchmaking for a game hosted on Edgegap, any engine: choose between Edgegap''s hosted matchmaker, your own allocator on the Deploy API, or a matchmaker you already use (Unity Matchmaker, Nakama, PlayFab, EOS or Steam lobbies, Pragma, AccelByte, Open Match); design the profile (teams, parties, skill, modes, expansions, queue times); place servers near players (ping beacons, player IPs, region and hub pickers); and add backfill (join in progress, replacing leavers, server-owned backfill tickets). Use for "players wait too long", "EU players land on US servers", "let players join a running match", "replace a player who left", "parties in a 4v4 queue", "skill-based matchmaking", "which matchmaker should we use", "leaving Multiplay or GameLift FlexMatch", or matchmaker config questions not tied to one engine''s client code. Engine skills (edgegap-unity, -ngo, -fishnet, -purrnet, -godot, -unreal, -threejs) own their Find Match client code; edgegap-nakama and edgegap-playfab own those integrations.'
metadata:
  version: "0.3.0"
---

# Matchmaking for games on Edgegap

Edgegap starts a server near a group of players and returns an address. Matchmaking is everything before that: who plays together, when a partial match is good enough, where the server goes, and what happens when someone leaves. This skill is the design layer, the same for every engine. Done means the developer knows who owns matchmaking, the config or allocator matches the game's real rules, players are placed by measured latency or IP, and, when the game needs it, a running server takes new players through backfill.

The client code that sends tickets lives in the engine skills, and the backend code that calls the Deploy API lives in `edgegap-deployments-api`. Load those for the code; come back here for the decisions. Edgegap ships the matchmaker clients as SDKs: the Unity SDK ([sdk-unity-sessions-matchmaker-server-browser](https://github.com/edgegap/sdk-unity-sessions-matchmaker-server-browser)) and the JavaScript/TypeScript SDK [`@edgegap/sdk`](https://github.com/edgegap/sdk-js-sessions-matchmaker-server-browser) (browser clients, and Node, Bun or Deno servers: groups and parties, page-reload resume, `ARBITRIUM_*`/`MM_*` parsing, backfill with `ServerAgent`), and the [Edgegap SDK for Unreal Engine](https://github.com/edgegap/sdk-unreal-engine) (UE 5.0-5.8, beta: beacons, groups, a server-side check that admits only players with a ticket for that server, `MM_*` readers, self-stop; steps in `edgegap-unreal`). Prefer them over hand-written HTTP calls or a hand-written ticket check. When you act on Edgegap yourself, follow the `edgegap` skill's [references/agent-rules.md](../edgegap/references/agent-rules.md).

## Step 1: decide who owns matchmaking

Read the project before asking. A matchmaker already in the code (a Nakama module, PlayFab `CreateMatchmakingTicket`, Unity `MatchmakerService`, EOS lobby code, a backend queue) usually stays.

| Situation | Owner | Load |
|---|---|---|
| No backend and no matchmaker yet | Edgegap's hosted matchmaker: JSON config, no server code, deploys and hands out addresses itself | this skill, then the engine skill for the client |
| The game already uses Nakama | Nakama's matchmaker + the Edgegap Fleet Manager for Nakama | `edgegap-nakama` |
| The game already uses PlayFab Matchmaking | PlayFab queue (allocation off) + Azure Functions that deploy | `edgegap-playfab` |
| Unity Matchmaker (UGS), EOS or Steam lobbies, Pragma, AccelByte, Open Match, a custom queue | that matchmaker forms the match; a backend allocator calls the Deploy API | [references/third-party.md](references/third-party.md), then `edgegap-deployments-api` |
| Players browse and pick a server, or servers are persistent | not matchmaking: Edgegap's Server Browser | https://docs.edgegap.com/learn/server-browser |
| Host/client game the developer won't move to a dedicated server | lobby + relay, not this skill | `edgegap` (relays) |

Why prefer the hosted matchmaker when nothing exists: it removes the backend that would otherwise hold the Edgegap API token, it already handles placement, retries and the address hand-off, and its Auth Token is designed to ship in clients. Keep a third-party matchmaker when the game depends on what it adds (accounts, parties, social, cross-play rules); replacing it is a bigger project than hosting.

A small proxy in front of the hosted matchmaker (any FaaS or Edgegap's Managed Clusters) is the middle path when the game needs server-trusted ticket attributes, such as a skill rating or a cheater flag the client must not be able to edit, or rules like "one group per player". Clients then talk to the proxy, and the proxy talks to the matchmaker.

## Step 2: design the profile

Ask only what the game doesn't tell you, then write the rules. [references/profiles.md](references/profiles.md) has the rule types, how groups and teams aggregate, and annotated configs in `assets/configs/`.

- **Players per match and teams.** `player_count` sets `team_count`, `min_team_size` and `max_team_size`. One team covers co-op, free-for-all and battle royale. Never set a minimum below the game's real minimum: a race or duel with one player is not a match.
- **Queue time.** `ticket_expiration_period` is `"30s"`, with expansion stages below it (15, 20). Partial matches need no expansion stage: a minimum below the maximum enables them, and they form by the time tickets expire, so the short expiration keeps the wait short. Use expansions only to relax a rule over time: expansions cost the matchmaker a lot of performance. Longer queues are a production decision for the developer, not a default.
- **Parties.** Use groups (Group Up): one owner creates the group, friends join it with the group ID, everyone marks ready, and the whole party lands on the same team. Groups only join a team that has room for all of them.
- **Skill.** `number_difference` on a rating the client can't forge. If the rating lives in the developer's backend, that means a proxy or the backend creates tickets, not the client. Widen `max_difference` in expansions.
- **Modes and maps.** `string_equality` for one exact value (mode, platform, build version); `intersection` for "any of these" (maps). Separate profiles when modes deploy different app versions or need different team sizes.
- **Latency.** A `latencies` rule (usually named `beacons`) keeps players with very different pings apart. Skip it for any profile that WebGL clients use: browsers can't run the ICMP ping, and a profile with the rule rejects tickets without beacons. See step 3.
- **Join in progress.** Add the `backfill_group_size` intersection rule now if the game will ever backfill, because every ticket must then carry the attribute. See step 4.

Every rule except `player_count` becomes a required ticket attribute with the rule's name as key, and unknown attributes are rejected with 400. Change the config and every client's ticket together.

## Step 3: place servers near the players

Placement happens twice: who is matched together, and where their server starts. [references/region-selection.md](references/region-selection.md) has the details.

- **Measure, don't guess.** Clients ping Edgegap's beacons (listed by the matchmaker or `GET /v1/locations/beacons`) and send the results as the `beacons` attribute. Reload the beacon list before each matchmaking round: beacons are added and removed in real time.
- **Send the player's public IP.** Matchmaker tickets take `player_ip`, and the Deploy API takes `users` with IPs or coordinates. Edgegap then picks, among 600+ locations, the one with the best and fairest ping for the whole group. A deployment with no player location lands in a default location far from most players.
- **Region or hub pickers** are a UI on top of beacons: disable regions whose every beacon is above a threshold (200 ms is a common start), or let players pick, sending low fake values only for the chosen beacons. Warn that a forced region can hurt teammates and opponents. Call them "hubs" or "regions", not "server locations": servers run in many more places than beacons.
- **High-ping players** wait longer if the rule is strict. Relax `max_latency` and `difference` in expansion stages rather than letting them never match.

## Step 4: backfill (join in progress)

A backfill is a ticket owned by a running server. It carries the server's address and the tickets of the players already on it. When a newly queued group matches it, the matchmaker sends that group to the running server instead of starting a new one. Use it for drop-in games (large lobbies, co-op, survival), to replace a player who left or never connected, and to fill servers before paying for new ones.

[references/backfill.md](references/backfill.md) has the contract, the request and response shapes, and the server loop. The rules that matter:

- Every ticket carries `backfill_group_size`: clients send `["new", "1"]` (solo, accepts a new match or one seat on a running one), `["new", "2"]` for a party of two; the server lists the group sizes it has room for, e.g. 3 free seats → `["3", "2", "1"]`. The profile has an `intersection` rule named `backfill_group_size` with `overlap: 1`.
- Backfills ignore `player_count` and match exactly one group. One backfill per team that is missing players.
- The server keeps a small number open while it has free seats, polls them (`ASSIGNED` means a group was seated, `assigned_ticket` holds it), seats the new ticket, and opens another. Count players on their way as taken seats.
- Backfills expire after `ticket_expiration_period`: renew them while seats are free.
- **Delete every open backfill before the server stops.** A leftover backfill sends players to a dead server until it expires. External stops (dashboard, API, max duration) send SIGTERM; handle it if the engine lets you.
- Players announce their ticket ID to the server when they connect, so the server can map connections to seats and free a seat when a matched player never arrives (allow about 60 s).
- `min_team_size: 999999` makes a profile match only against backfills, e.g. a "join a game in progress" button.

## Step 5: ship the config

1. Generate the base config with `edgegap_build_matchmaker_config` (it checks the app version exists and has ports), then add rules it doesn't produce (skill, modes, `backfill_group_size`) by hand. Validate the JSON (`python -m json.tool`).
2. The developer creates the matchmaker in the dashboard (no API for this): **Matchmaker → Create Matchmaker**, upload the file, **Create and Start**, then copy the API URL and Auth Token into the client config. Free tier: one deployment at a time, and the matchmaker stops 3 hours after each start.
3. Editing a running matchmaker's rules is a quick reload that drops all tickets. Changing the matchmaker `version` or the app version a profile points at needs **Stop → Edit → Start**; forgetting it after a new build keeps deploying the old build.
4. Test with two clients, not one. A lone ticket can only form a partial match, and only if the profile allows it.

Matchmaker version: the pack's templates were verified on `3.3.2`. Edgegap's release notes list `3.3.3` (stability under sustained rate limits, players reliably returned to queue when every deployment retry fails) with no config changes; it is a safe upgrade through Stop → Edit → Start.

## What was verified

- Profiles, Group Up, beacons and the ticket contract: end to end on Edgegap with the Unity, Unreal, FishNet, PurrNet, NGO, Godot, Colyseus and Three.js samples (October 2026, matchmaker 3.3.2).
- Unreal SDK (beta 0.1.x): two clients matched to one deployment and the server's ticket check (missing, made-up, prefix and in-use tickets refused) run live on Edgegap with UE 5.8 on 2026-11-02, per the SDK's own compatibility page; its backfill and party calls were not run.
- Backfill: end to end on Edgegap with the Megacity Metro sample (Unity Netcode for Entities, Edgegap Unity SDK 3.5.5, 2026-10-21). Two clients matched, a third queued later and joined the same deployment through a backfill, and the server closed its backfills before stopping itself. The language-agnostic loop in `references/backfill.md` follows that code but was not run as written; parties larger than one, team backfill and backfill-only profiles were not run.
- Third-party matchmakers: Nakama and PlayFab end to end (their own skills). Unity Matchmaker uses Unity's `EdgegapAllocator` Cloud Code module: load `edgegap-ugs-matchmaker`. Pragma, AccelByte and Open Match have no Edgegap-specific integration: the pattern in `references/third-party.md` is the generic allocator.

Say which of these the developer's setup relies on when it matters.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| 400 when creating a ticket or group | profile name or attributes don't match the config: a missing rule attribute (`beacons`, `backfill_group_size`) or an unknown one |
| Two players wait until their tickets expire, then match | Long `ticket_expiration_period` (e.g. `5m`): set it to `30s`, don't add an expansion |
| Players far apart are matched or placed badly | no `player_ip` / `users`, no `latencies` rule, or the client sends beacons with failed pings (0 values) |
| New players always get a new server, never the running one | the server opens no backfill (not a matchmaker deployment, no matchmaker URL/token on the server, no free seats), or tickets lack `backfill_group_size` |
| Players are sent to a server that is gone | backfills left open after the server stopped; delete them on shutdown |
| Flips MATCH_FOUND ↔ SEARCHING | the deployment can't start: free-tier deployment limit, a leftover test deployment, or a broken app version |
| 429 during a burst | matchmaker rate limit for the tier: clients retry with backoff; cache the beacon list in a backend for large launches |

Engine-specific symptoms (CORS, WebGL, connection after HOST_ASSIGNED) are in each engine skill's troubleshooting reference.

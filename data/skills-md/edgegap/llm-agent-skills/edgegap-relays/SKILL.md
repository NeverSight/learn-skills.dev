---
name: edgegap-relays
description: 'Edgegap Relays (Smart Relays, Distributed Relay) for host/client games: one player hosts, friends join with a code, and traffic goes through an Edgegap relay near them, so nobody port forwards and NAT or firewalls stop mattering. Load this once the developer has chosen peer-to-peer or a listen server over a dedicated server, before using edgegap_create_relay_session or any relay API. Emulator-tested, not yet on a live Edgegap relay; points to the LightNet relay deployment verified on Edgegap. Ships a relay transport for raw-UDP netcodes (relay protocol plus reliable fragmented and unreliable ordered channels), a lobby service that keeps the relay token off players'' machines, an offline relay emulator, and fixes for relay pitfalls: relay vs API token, server vs client port, IP authorization, 1200-byte MTU, clients only reach the host. Use for "relay for my P2P game", "join by code without port forwarding", "replace Unity Relay or Steam P2P with Edgegap", or a custom relay transport.'
metadata:
  version: "0.1.1"
---

# Edgegap Relays: host/client games without port forwarding

Goal: one player's game hosts the match, the others join with a lobby code, and every packet goes through an Edgegap relay chosen near the players. Nobody opens ports, and NAT or firewalls don't block anyone. Done means two real clients joined a host through a real Edgegap relay session, exchanged reliable and unreliable messages, and the session was deleted afterwards. Code that compiles is not done, and the offline emulator is not a relay.

```
Host game --POST /lobbies--------------> lobby service (holds the RELAY token)
                                           POST /v1/relays/sessions {users:[host IP]}  -> poll until ready
          <-- code, relay ip, SERVER port, session token, host user token
Client    --POST /lobbies/CODE/join----> lobby service
                                           POST /v1/relays/sessions:authorize-user {session_id, user_ip}
          <-- relay ip, CLIENT port, session token, client user token
Host   == UDP ==> relay server port  [Edgegap relay]  relay client port <== UDP == Client
Host leaves --DELETE /lobbies/CODE--> lobby service --DELETE /v1/relays/sessions/{id}
```

**Verification status: not run on a live Edgegap relay.** The transport, lobby service and emulator come from [edgegap/server-sample-unity-smart-relays](https://github.com/edgegap/server-sample-unity-smart-relays/tree/feature/edgegap-relay) (branch `feature/edgegap-relay`, Unity 6000.0.54f1, LightNet with the transport from `assets/unity/`, the lobby service from `assets/lobby-service/` on Node 22), where they ran against `assets/tools/local-relay.js` only. Edgegap's managed relays need a relay profile, and the organization this pack is tested with gets `403` on `/v1/relays/*` (`edgegap_list_relay_sessions` answers `not_configured`). Tell the developer this before relying on the transport, and treat their first real two-client run (Phase 3) as the verification.

**A relay that is verified on Edgegap:** [edgegap/server-sample-lightnet-relay](https://github.com/edgegap/server-sample-lightnet-relay) runs a LightNet relay server as an ordinary Edgegap **deployment** (no relay profile, works on any plan), with relay transports for Mirror, FishNet, PurrNet and NGO, 6-letter room codes and an optional matchmaker that starts one relay per match. All four netcodes passed end to end on Edgegap on 2026-11-02. It also runs in **Unity WebGL builds**: `LightNet/Runtime/Relay/RelayWebSocket.jslib` bridges `RelayWebSocket` to the browser's WebSocket (`#if UNITY_WEBGL && !UNITY_EDITOR`), so the same four transports connect over `wss://` to the relay version's `relay-ws` port (7778, TLS Upgrade on). A WebGL build reads its options from the page URL: `index.html?relay=wss://<host>.pr.edgegap.net:<port>&host` (or `&join=CODE`), plus `&netcode=FishNet` etc.; build it with **Tanks > Build WebGL client**. Passed on Edgegap 2026-11-09 for all four netcodes (relay in Toronto): desktop host + browser client, browser host + desktop client, browser + browser. WebGL limits: WebSocket is reliable and ordered only (no unreliable channel); a browser host freezes while its tab is hidden, so prefer a desktop host; with the matchmaker, browsers can't ping beacons, so use a profile without the `beacons` rule. Prefer this sample for those netcodes, for any WebGL host/client game, or when the organization has no relay access; use the managed relays below for other netcodes or when the developer wants Edgegap's relay network. Not run: the matchmaker flow from a browser, real mobile browsers, native mobile clients, more than 3 players, a lobby service deployed on a public host. Say so when those matter.

The managed relays below are UDP only: a WebGL build can't open UDP sockets, so it can't use them or this skill's `RelayNetworkService`. For a browser host/client game, use the LightNet relay sample over `wss://`.

## First: is a relay the right call?

A relay is not a game server. It only forwards packets, and one player's game is the host and owns the game state. Before you build anything, make sure the developer chose this knowingly:

| | Dedicated server (`edgegap_deploy`) | Relay (this skill) |
|---|---|---|
| Who owns the game state | Edgegap runs the server build | The host player's game |
| Cheating | Much harder | The host can change anything |
| Latency | Everyone one hop from the server | Host 0 ms, everyone else two hops via the relay |
| Host quits | Match goes on | Match ends, unless the game migrates the host |
| Needs a headless server build | Yes | No |

Use a relay when the game is built host/client (co-op, friends lobbies, a listen server) and moving to a dedicated server is not wanted or not possible. If the developer hasn't said so, ask once, and recommend a dedicated server for anything competitive. Reasons to use a relay don't include "it needs no server image"; the `edgegap` skill covers dedicated servers.

## How to work

- **Be the engineer.** Read the project, write the transport and the backend calls, build the game, run the lobby service and the clients, and read the logs. Hand the developer only the account steps: creating the relay profile token, putting it in a git-ignored env file, and playtesting.
- **No relay access?** If `edgegap_list_relay_sessions` answers `not_configured` (403), the plan has no relays: offer the LightNet relay deployment above, or a dedicated server.
- **Relay token, not API token.** Relay endpoints (`/v1/relays/*`) need a token from a **relay profile** (dashboard: Relays). A regular API token gets `401`/`403` there, and so does the Edgegap MCP when it runs with one. The relay token is a secret like the API token: it lives in the backend only, never in the game ([agent rules](../edgegap/references/agent-rules.md)). Don't read it from the developer's machine; ask them to write it to `lobby-service/.env`, which the service loads.
- **One layer at a time:** transport against the offline emulator → lobby service → real relay with two clients → cleanup. Each phase has a check.
- **Money.** Relay sessions bill while open. Delete every session you created before you finish (`edgegap_list_relay_sessions` / `edgegap_delete_relay_session`, or the lobby's `DELETE`), and only the ones you created.

## Phase 0: Understand the game

Read, don't ask:
- The netcode and its transport layer: who opens sockets, whether it's raw UDP (LightNet, ENet, LiteNetLib, a custom socket layer), KCP (Mirror, FishNet's Edgegap KCP transport), Unity Transport (NGO), or something with native DLLs. The relay needs access to UDP send/receive; a transport hidden in a native DLL can't be redirected.
- How hosting and joining work now: direct IP entry, Steam P2P, Unity Relay/Lobby, an existing backend or lobby.
- Message sizes: the relay forwards datagrams of at most 1200 bytes, including up to 13 bytes of its own.
- Whether clients need to see each other's data: the relay only connects clients to the host, so the host must forward.

Then pick the transport path:

| Netcode | Transport |
|---|---|
| LightNet (or any `NetworkService`-style raw socket library) | `assets/unity/`: `RelayNetworkService` + the `INetworkService` patch, see `references/lightnet.md` |
| Your own UDP layer, any engine or language | Implement the protocol in `references/protocol.md` (the C# service is a working reference) |
| Mirror, FishNet, PurrNet, NGO | Verified path: the LightNet relay deployment above (its own transports). Managed relays: Edgegap's relay transports in https://github.com/edgegap/distributed-relay-examples and the 2024 samples [relay-sample-unity-mirror-](https://github.com/edgegap/relay-sample-unity-mirror-), [relay-sample-unity-fishnet-](https://github.com/edgegap/relay-sample-unity-fishnet-), [relay-sample-unity-ngo-helloworld](https://github.com/edgegap/relay-sample-unity-ngo-helloworld) (not run by this skill: check they match the netcode version) |
| WebGL / browser | Not possible with the managed relays (no raw UDP in browsers). Mirror, FishNet, PurrNet or NGO in Unity WebGL: the LightNet relay deployment above over `wss://` (verified 2026-11-09). Otherwise a dedicated server with WebSockets |

## Phase 1: Transport, tested offline

1. Copy the transport into the project (LightNet: `assets/unity/Edgegap/Relay/` and `assets/unity/LightNet/INetworkService.cs`, then the `NetworkComponent` patch from `references/lightnet.md` §1).
2. Replace the direct host/join calls with `StartRelayHost(endpoint, maxClients)` and `StartRelayClient(endpoint)`. Keep message types and handlers as they are.
3. If clients need each other's state (positions, chat), make the host forward it (`references/lightnet.md` §3).
4. Run `node assets/tools/local-relay.js --loss 15` and a host plus two clients against it with the emulator's tokens (`references/testing.md` §1). A command-line path (host, join, an automated echo test) makes this and Phase 3 scriptable.

✅ Check: both clients connect, reliable messages arrive complete and in order under loss, and each client sees the other's state. If you started earlier emulator runs, kill them by PID first: a stale emulator still bound to the ports keeps its old loss setting.

## Phase 2: Lobby service (or the developer's backend)

Read `references/backend.md`.
1. Existing backend (own lobby, Nakama, PlayFab, a matchmaker): add the same three calls there (create the session with the host's IP and poll until `ready`, authorize each joiner's IP, delete at the end) and return the endpoint fields. No backend: copy `assets/lobby-service/` and run it.
2. The developer writes `EDGEGAP_RELAY_TOKEN=...` into `lobby-service/.env` (git-ignored).
3. `npm start`, then `curl -X POST localhost:8080/lobbies` and `DELETE` the lobby with its `X-Host-Secret`.

✅ Check: the POST returns `relay_ip`, `relay_port` (the server port), `session_token` and `user_token`, and the DELETE returns 204 and removes the session (`edgegap_list_relay_sessions` or the service log). A 401/403 means the token is not a relay token.

## Phase 3: End to end on a real relay

1. Host from one game instance, join from two more with the code (`references/testing.md` §2). All on one machine is fine: the lobby authorizes your public IP for each of them.
2. Watch each log for relay state `Valid`, the host seeing each client join, and your test passing. Keep the round-trip time and resend count in the report.
3. Leave from the host; the lobby deletes the session.

✅ Check: two clients played through the relay, and `edgegap_list_relay_sessions` (or `GET /v1/relays/sessions` with the relay token) shows none of your sessions left.

## Phase 4: Ship it

- Deploy the lobby service somewhere players can reach (`references/backend.md` §4): it must see players' real public IPs (set `TRUST_PROXY=1` behind a proxy), keep one instance (lobbies are in memory), and in production also authenticate players and rate-limit lobby creation.
- Point the game at the deployed URL. `localhost` only works on the developer's machine.
- Keep the session cleanup: host leave → `DELETE`, plus the service's TTL for hosts that crash.

## Pitfalls

`references/troubleshooting.md` has the full table. The ones that cost the most time:
- **Server port vs client port.** The host connects to the session's `ports.server`, everyone else to `ports.client`. Swapped ports give `Invalid`.
- **Per-player tokens.** Every player sends the session token plus its **own** user token. Reusing the host's token for a client gives `Invalid` or kicks the host.
- **IP authorization.** The relay accepts a user only from the IP it was authorized with. A lobby on the developer's machine sees `127.0.0.1` or a LAN address: use the machine's public IP (the lobby service does).
- **Clients only reach the host.** There is no client-to-client path; the host forwards.
- **MTU.** 1200 bytes per datagram, minus the relay's 13 and your own header. Fragment reliable messages; keep unreliable ones small.
- **Sessions bill while open.** Delete them on host leave, and expire forgotten ones.

---
name: edgegap-server-design
description: 'Design an authoritative dedicated game server that fits per-match hosting on Edgegap: who owns the game state, the deployment lifecycle (boot, read injected env vars, bind a fixed port on 0.0.0.0, accept players, self-stop at match end, drain on SIGTERM), logging, and what never goes in the server. Use whenever adding online multiplayer to a game, converting a host/client, listen-server or peer-to-peer game to dedicated servers, or when someone asks about netcode architecture, authoritative servers, match lifecycle, tick rate, cheat prevention or how a game server should behave on Edgegap. Engine-agnostic (Unreal, Godot, Node, custom engines); apply it before containerizing. Unity projects get the same rules, already applied, from edgegap-unity.'
metadata:
  version: "0.2.1"
---

# Designing a server for Edgegap

On Edgegap, one deployment is usually one match. The server is started for a specific group of players, lives as long as their match, and stops when it ends. Servers built that way get scaling, placement near players, crash isolation and per-minute billing for free. Servers built as long-lived daemons that rotate lobbies internally fight the platform (cloud deployments are stopped after 24 hours anyway).

## Authority

The server owns the truth. Clients send *intents* (inputs, actions); the server simulates, validates and broadcasts the resulting *state*. Never trust a client-reported outcome (position, hits, score, currency): any client can be modified. Give that up and you have built an expensive relay.

Apply as the game needs:
- **Client prediction and reconciliation** for the local player, so input feels instant. The server stays authoritative; the client replays unacknowledged inputs on top of server state.
- **Interpolation** for remote entities: render about 100 ms in the past between known snapshots.
- **Tick rate** is a budget: 60 Hz for fast shooters, 20 to 30 Hz for most action games, 10 Hz for slow sims. Tick rate × entities × players is the CPU bill, and it must fit the vCPU on the app version (minimum 0.25 vCPU; free tier at most 1.5 vCPU / 3 GB). Engines that run uncapped on a headless server burn 100% CPU: cap the frame or tick rate.

## The deployment lifecycle contract

**1. Boot fast.** Players wait while the container starts. Bake assets into the image at build time; don't download them at boot. Note that a deployment is marked Ready when the container starts, before your engine has loaded its scene. Clients must retry the connection for a while (about 1 minute), so keep that window short.

**2. Read configuration from environment variables.** Never bake per-match or per-environment values into the image; the same image must run everywhere, locally included. Edgegap injects read-only variables into every deployment:

| Variable | Use |
|---|---|
| `ARBITRIUM_REQUEST_ID` | This deployment's ID. Log it at boot. Its presence tells the server it runs on Edgegap |
| `ARBITRIUM_PORT_GAMEPORT_INTERNAL` / `_EXTERNAL` / `_PROTOCOL` | The port you bind, the port players use, the protocol. One set per named port (`gameport` here) |
| `ARBITRIUM_PORTS_MAPPING` | All ports as a JSON string |
| `ARBITRIUM_PUBLIC_IP`, `ARBITRIUM_DEPLOYMENT_LOCATION` (JSON) | Where the server runs |
| `ARBITRIUM_DEPLOYMENT_TAGS` | Comma-separated tags set at deploy time |
| `ARBITRIUM_DELETE_URL` + `ARBITRIUM_DELETE_TOKEN` | Self-stop (step 6) |
| `ARBITRIUM_CONTEXT_URL` + `ARBITRIUM_CONTEXT_TOKEN` | Full deployment details, callable only from inside |
| `MM_MATCH_ID`, `MM_TICKET_IDS`, `MM_TICKET_<id>`, `MM_TEAMS`, ... | Only on matchmaker deployments: who was matched, teams, ticket attributes |

Your own values come from app version env vars (same for every deployment of that version) or deployment env vars (per match: up to 20, 4 KB each). Don't reuse `ARBITRIUM_` or `MM_` names; they get overwritten. Treat variables as strings; the structured ones are JSON strings.

**The game server never holds the Edgegap API token**: not in env vars, args or the image. It grants full control of the organization. Anything the server needs from Edgegap goes server → your backend → Edgegap, except self-stop and context, which have their own per-deployment tokens.

**3. Bind a fixed internal port on `0.0.0.0`.** Pick a constant port (7777/UDP is typical) and match it in the app version's port mapping. Edgegap gives players a **random external port** per deployment; the server never needs to know it, except to advertise it. Binding `127.0.0.1`/`localhost`, or a random port, works on a laptop and is unreachable on Edgegap.

**4. Signal readiness.** Log one clear line once you accept connections (`READY port=7777`). You and the developer will look for it in the logs. If players should wait for the server to finish loading, say so to the clients rather than relying on Ready.

**5. Play the match.** Expect the players you were given. On matchmaker deployments, `MM_TICKET_IDS` lists them: start when they have all joined, and optionally reject a client whose ticket ID is not in the list. Allow about 60 seconds for matched players to arrive; if nobody comes, stop (step 6).

**6. End deliberately by stopping yourself.** When the match is over, or the server has been empty for a short while (30 s works), report results to your backend first, then call the self-stop endpoint:

```
DELETE $ARBITRIUM_DELETE_URL
Authorization: $ARBITRIUM_DELETE_TOKEN
```

This is the most important cost control there is: an idle deployment bills until it hits its max duration. A clean exit (code 0) also ends the deployment, but only with restart policy **Never** or **On Crash**; the default, Always, restarts the server and keeps billing. Set restart policy Never on match servers (`restart_policy: "never"` on `edgegap_create_app_version` or `edgegap_update_app_version`, MCP 0.16.0 and later; or the dashboard) and still self-stop explicitly. Do not loop back to a lobby.

Never print the delete token. A Dockerfile or start script that dumps `env` into the logs leaks it.

**7. Drain on SIGTERM.** A stop (self-stop, backend stop, max duration, dashboard) sends SIGTERM to the main process, then SIGKILL after the version's termination grace period (`termination_grace_period_seconds`, 5 s minimum). Handle SIGTERM: tell players, flush results, exit. Write the essentials first, within a few seconds. The process must actually be PID 1 or receive the signal (see `edgegap-containerize`).

Backstops: the app version's **max duration** stops stragglers (cloud deployments never run longer than 24 hours, free tier 60 minutes), and the matchmaker or your backend can stop a deployment from outside.

## Statelessness and logs

The container filesystem disappears when the deployment stops. Durable state (results, progression, inventory) lives in your backend and is pushed out before the server stops.

Log to stdout/stderr, unbuffered, one event per line. Edgegap shows container output in the dashboard and the logs API, but **logs are deleted when the deployment stops** unless Endpoint Storage (an S3 bucket) is configured on the app version. Log the config you booted with (without secrets), the READY line, joins and leaves, phase changes and the result. Show the deployment ID in the client's match history so player reports can be traced.

## Single-player and always-online sessions

The same contract works for one player: the server owns rules, state and saves, so nothing worth cracking ships in the client binary (LLMs decompile clients quickly). Deploy one small server per play session near the player, push saves to the backend regularly and on SIGTERM, and self-stop shortly after the player disconnects. Allow a short reconnect window first, so a dropped connection doesn't lose the session.

## Persistent worlds

Servers that must outlive one match (MMO shards, survival worlds) don't fit public cloud deployments, which stop after 24 hours. Use Private Fleets with persistence (max duration `-1`, restart policy On Crash) and keep world state in external storage. See https://docs.edgegap.com/learn/orchestration/persistence.

## Next

- Unity: `edgegap-unity` does all of this with tested templates.
- Package the server: `edgegap-containerize`.
- Prove it before spending money: `edgegap-local-testing`.

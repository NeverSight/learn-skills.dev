---
name: edgegap-troubleshoot
description: 'Diagnose why a game server on Edgegap will not start, keeps restarting, stops early, or cannot be reached, for any engine: image push and pull failures (401, 403, 424 "unable to pull image"), exec format errors, 422 couldn''t allocate, Error deployments, crash loops and OOM kills, 100% CPU, deployments stopping after 60 minutes or 24 hours, missing logs, clients timing out or failing to connect (internal vs external port, protocol, 0.0.0.0 binding, wss and TLS Upgrade), and matchmaker players stuck searching. Use when someone says their Edgegap deployment, server or matchmaking "isn''t working", or pastes an Edgegap error. Unity-specific build and SDK issues are in edgegap-unity.'
metadata:
  version: "0.2.4"
---

# Troubleshooting an Edgegap deployment

Find the layer that failed, get evidence from it, then fix the root cause. Layers, in order: **build → image → registry → app version → deployment → server process → network → matchmaker**. Don't change two layers at once.

Evidence first, with the `edgegap_*` MCP tools when connected (rules: the `edgegap` skill's [references/agent-rules.md](../edgegap/references/agent-rules.md)): `edgegap_list_app_versions`, `edgegap_get_deployment`, `edgegap_get_deployment_logs` (container logs plus crash data: exit code, OOM, restart count), `edgegap_list_deployments`. **Read logs before stopping anything**: they are deleted when a deployment stops, unless Endpoint Storage is configured. For crashes that are hard to catch live, suggest keeping logs: `edgegap_list_endpoint_storage` shows whether a bucket exists, and `edgegap_update_app_version` with `endpoint_storage` exports each deployment's logs there when it ends. Without tools, the dashboard deployment page shows the same.

Also check https://status.edgegap.com before deep debugging.

## 1. Image and registry

| Symptom | Cause / fix |
|---|---|
| push `401 Unauthorized` | Not logged in to the registry (`docker login registry.edgegap.com -u '<username>'`). Retrying doesn't help |
| push `403 Forbidden` / `denied` | Logged in as a user without push rights, to the wrong registry, or pushing to the wrong project path |
| push `exceed the configured upper limit` | Registry full (free tier: 10 GB). Delete old tags in the dashboard; space frees only when all tags of an image are gone |
| new build doesn't show up | Tag reused (`latest`, or the same tag re-pushed). Edgegap caches by tag: push a new tag and point a version at it |
| `exec format error`, segfault or "not found" at start | Image built for ARM. Rebuild with `--platform linux/amd64` |
| `edgegap_list_registry_tags` doesn't show the tag | Push failed or went elsewhere; pass the image name only (no project, no tag) |

## 2. App version and deploy request

| Symptom | Cause / fix |
|---|---|
| `Unable to pull image from registry` / `424` | The version has no or wrong registry credentials, or wrong registry host, image path (`<project>/<image>`) or tag. Check `registry_credentials_set` with `edgegap_list_app_versions`. For registry.edgegap.com, create a new version without a login so it gets `registry_profile: "Edgegap"` (PATCH can't add it) |
| `Unable to pull image from registry` with a login that works for other images, image built by `docker/build-push-action` or `docker buildx` | The image was pushed as an index with provenance/SBOM attestations. Rebuild with `provenance: false` and `sbom: false` (`--provenance=false --sbom=false`) and put the new tag on the version. Seen with a GitHub Actions build on 2026-11-09 |
| `verify_image` fails "Unable to login with the given credentials" | Credentials on the version are wrong |
| `422` couldn't allocate | vCPU/memory too high for the tier (free: 1.5 vCPU / 3 GB; memory at most 2× vCPU units), or no capacity near those users right now. Lower resources, or retry with backoff |
| `400` on deploy | Unknown app or version name, or bad body. Read `message` |
| `429` | Rate limit (40 deploys/s, 20 status/s, 10 list/s per organization). Back off; use webhooks instead of polling |
| free tier: second deploy refused, or matchmaker never deploys | One deployment at a time. A forgotten test deployment blocks everything: list and stop it |
| `You have reached you Application limit of 2` / version limit | Free tier: 2 apps, 2 versions. Reuse or delete one, or upgrade |
| Error deployment, slow start | Image download exceeded `time_to_deploy`. Enable caching (paid) or raise it. Error deployments aren't billed and are cleaned up after 24 h |

## 3. Server process

| Symptom | Cause / fix |
|---|---|
| Ready, then restarts again and again | The server crashes; restart policy Always restarts it. Read the logs and crash data. Set restart policy Never while debugging to see the real exit |
| `OOM killed` | Memory too low for the server, or a leak. Measure with `docker stats`, raise memory on a duplicated version (no rebuild) |
| 100% CPU and never settles | Netcode never started (server auto-start off in headless mode), or an uncapped frame/tick rate. Brief spikes during boot are normal |
| Logs empty | Engine logs to a file instead of stdout; or the deployment already stopped (logs deleted) |
| Container exits immediately | Wrong executable name or path, missing `chmod +x`, missing shared library, server waiting for a TTY or prompt. Reproduce with `docker run` locally |
| Stopped after 60 minutes | Free-tier limit, or the version's max duration |
| Stopped after 24 hours | Cloud deployment limit. Persistent servers need Private Fleets |
| Stopped right after start | The server self-stopped (no players arrived within its timeout), or exited with restart policy Never |
| SIGTERM ignored, killed after the grace period | The server isn't PID 1 (shell-form CMD, script without `exec`, `npm start`) or has no handler |

## 4. Clients can't connect

Checklist, in order:
1. Deployment is Ready and the logs show the server listening, with no crash.
2. The server binds `0.0.0.0`, not `127.0.0.1`/`localhost`, on the **internal** port in the app version. A mismatch is fixed by editing or duplicating the version; no rebuild.
3. The version's protocol matches the transport: UDP for most game transports (ENet, KCP, Unity Transport), TCP for TCP transports, WS for WebSocket.
4. The client uses the **external** port (random per deployment) and the deployment's `public_ip` or `fqdn`, never the internal port.
5. Browser clients use `wss://<fqdn>:<external>` and the WS port has **TLS Upgrade** on. A server log line like `First bytes from client was not 'GET'... 16-03-01` means TLS reached the server: TLS Upgrade is off.
6. The client retries for up to about a minute: Ready means the container started, not that the engine finished loading.
7. The server didn't already stop itself because nobody joined in time.
8. Port names agree: a client or SDK looking for `gameport` fails if the version calls it "Game Port".
9. Network: VPNs, corporate or school networks often block UDP; test from another network. Mainland China needs the China Gateway.

Prove the port independently of the game: for WS ports, `curl --http1.1 -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" --max-time 5 https://<fqdn>:<external>/` must return HTTP 101.

## 5. Matchmaker

| Symptom | Cause / fix |
|---|---|
| Ticket rejected `400` | Profile name or ticket attributes don't match the config's rules |
| Stuck SEARCHING | Not enough players for the rules yet: test with enough clients, and keep `ticket_expiration_period` at `30s` so a partial match (minimum below maximum) forms quickly |
| Flips MATCH_FOUND ↔ SEARCHING | The deployment failed: free tier deployment already in use, broken version, or pull error. Check deployments |
| Clients still get the old build | The matchmaker profile still points at the old app version. Stop → edit → start the matchmaker |
| `401` from the matchmaker | Auth Token sent with a `Bearer`/`token ` prefix; it is sent raw |
| Browser `CORS` error | `allowed_cors_origins` in the config doesn't list the page's origin |
| Matchmaker unreachable | Free tier matchmakers stop 3 h after each start; DNS can take a few minutes after creation |

## When to escalate

If evidence points at Edgegap (Error deployments with a correct image that runs locally, regional outages), open a support ticket in the dashboard or ask in the Edgegap Discord with the deployment IDs, app and version names, and times. Never include the API token.

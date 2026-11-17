---
name: edgegap-local-testing
description: 'Prove a game server container behaves on a laptop exactly as it will on Edgegap before spending money: the parity docker run with Edgegap-style env vars, the random-external-port test, the SIGTERM drain test, boot timing, two servers on one host, resource sizing with docker stats, then one tagged test deployment on Edgegap with a real client. Use before any first deploy or new build rollout, when a server works locally but not on Edgegap, or when someone asks how to test a game server container, run it with Docker, or smoke-test a deployment. Engine-agnostic.'
metadata:
  version: "0.3.0"
---

# Testing before you deploy

Every failure this catches costs seconds locally, and a confusing debugging session (or a billed deployment) on Edgegap. Run the local battery on every meaningful server change; run the Edgegap smoke test before a build reaches players or a matchmaker.

## The whole battery in one command

`assets/parity.sh` runs every local check below against an image and stops at the first failure: boot and time to READY, the random external port (with your own client if you give it one), two servers on one host with `docker stats`, secrets in the logs, the SIGTERM drain, and the self-stop path.

```bash
IMAGE=mygame:dev PORT=7777 PROTO=udp READY='READY' \
  CLIENT_CMD='./my-test-client $SERVER_HOST $SERVER_PORT' \
  SELF_STOP_ENV=FIRST_JOIN_TIMEOUT_S=5 bash parity.sh
```

`READY` is a regex for the server's ready line; `CLIENT_CMD` (optional) must play a match against `$SERVER_HOST:$SERVER_PORT` and exit 0; `SELF_STOP_ENV` (optional) is whatever makes your server give up quickly when nobody joins; `ENV_FILE` passes the version's env vars; `GRACE` matches the version's termination grace period. Checked on 2026-11-03 against a Node.js WebSocket game server (passes) and a shell-form CMD that ignores SIGTERM (fails at the drain test, as it should). The sections below explain each check, for when one fails.

## Parity run

Reproduce what Edgegap does: your image, env vars injected, ports mapped.

```bash
docker build --platform linux/amd64 -t mygame:dev .

docker run --rm --name mygame-test \
  -e ARBITRIUM_PORT_GAMEPORT_INTERNAL=7777 \
  -e ARBITRIUM_PORT_GAMEPORT_EXTERNAL=31504 \
  -e ARBITRIUM_PORT_GAMEPORT_PROTOCOL=UDP \
  -e MY_GAME_MODE=duel \
  -p 31504:7777/udp \
  mygame:dev
```

Use `/tcp` for TCP and WS ports. Do **not** set `ARBITRIUM_REQUEST_ID` or `ARBITRIUM_DELETE_URL` locally: servers that self-stop should detect "not on Edgegap" from their absence and skip the call (exit instead).

Check, in order:
1. **It boots on amd64.** On Apple Silicon it runs under emulation: slow is fine, *crashing* is a real bug (usually a native dependency built for ARM).
2. **`docker logs mygame-test` shows the boot line, then READY.** Empty stdout means empty logs on Edgegap too: the engine is logging to a file.
3. **Time to READY.** Wall-clock from `docker run` to READY is extra wait for every player after a match is found. Seconds is good; tens of seconds means a download or compile that belongs in the build.
4. **Nothing secret in the logs.** No env dump, no tokens.

## The random external port test

Map a host port that differs from the container port, as above (`31504` → `7777`), and connect a real client to `127.0.0.1:31504` (WS: `ws://127.0.0.1:31504`).

On Edgegap the external port is random for every deployment and is never the internal port. This test catches every place where the server leaks its *bind* port to clients (a server-browser listing, a redirect, a "reconnect on port X" message) instead of the address the client was given. A server that only works with `-p 7777:7777` loses every player on Edgegap.

## The drain test

```bash
docker stop --time 5 mygame-test
```

`docker stop` sends SIGTERM, then SIGKILL after the timeout: the same shape as an Edgegap stop with the minimum 5-second grace period (raise `--time` to match the version's `termination_grace_period_seconds` if you set one). Check with `docker logs -t` that the handler ran, results were flushed, and the process exited before the kill. If it only dies at SIGKILL, PID 1 isn't your server (shell-form CMD, missing `exec`, `npm start`) or the handler isn't wired; see `edgegap-containerize`.

Also run a short scripted or bot match to completion and confirm the server ends on its own.

## Two servers on one host

Edgegap places several deployments on one machine, each with its own ports. Locally:

```bash
docker run -d -p 31504:7777/udp mygame:dev
docker run -d -p 31505:7777/udp mygame:dev
```

Both must be joinable independently. A failure means a hidden singleton: a fixed second port, a lock file, a shared path.

Measure while you're here: `docker stats` during a full match gives the CPU and memory numbers for the app version's vCPU and memory (1024 units = 1 vCPU). Add margin; exceeding memory gets the deployment OOM-killed.

## Smoke test on Edgegap

Do this once per new image, before building a matchmaker or backend on top of it. When you run it yourself, use the `edgegap_*` MCP tools (rules: the `edgegap` skill's [references/agent-rules.md](../edgegap/references/agent-rules.md)). Ask before deploying.

1. `edgegap_list_registry_tags` → the tag is there.
2. `edgegap_list_app_versions` → the version points at that tag, `registry_credentials_set: true`, ports and protocol right (and `tls_upgrade` on WS ports for browsers).
3. `edgegap_deploy` with the developer's public IP as the user (`curl -s https://api.ipify.org`) and a tag such as `agent-test`. Record the `request_id`.
4. `edgegap_wait_for_deployment` → `fqdn`, `public_ip`, external ports.
5. `edgegap_get_deployment_logs` → boot line and READY, no crash loop, no restarts. Read them again while the test match is still on: a server that self-stops takes its logs with it seconds after the match.
6. For WS ports, prove the port and TLS Upgrade answer:
   `curl --http1.1 -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" --max-time 5 https://<fqdn>:<external>/` must print HTTP 101.
7. Connect a real client to `public_ip` (or `fqdn`) and the **external** port. Retry for up to a minute: Ready means the container started, not that the engine finished loading.
8. If the server self-stops, finish the match and watch the deployment disappear (`edgegap_get_deployment` → `TERMINATED`). For a short test, pass shorter match timers as deployment env vars rather than building a new version. Otherwise `edgegap_stop_deployment` with the exact `request_id`. Read the logs before stopping if anything failed: they are deleted at stop.

An image that passes this has proven the build, the registry credentials, the port mapping, the env var handling and the shutdown path. Free tier allows one deployment at a time, so make sure nothing is left running afterwards.

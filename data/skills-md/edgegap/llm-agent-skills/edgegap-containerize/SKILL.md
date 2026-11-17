---
name: edgegap-containerize
description: 'Package any game server (Unreal, Godot, Node, Go, Rust, C++, a Unity build) into a Docker image that runs correctly on Edgegap, push it to the Edgegap Container Registry or Docker Hub, GHCR, ECR, GCR or GitLab, and register it as an app version: the container contract, Dockerfile patterns, linux/amd64 builds on Apple Silicon, image tags, registry credentials on the version, and port mapping. Use whenever writing or fixing a Dockerfile for a game server, building on a Mac, pushing to registry.edgegap.com, getting "unable to pull image" or exec format errors, or when someone asks how to get a server build onto Edgegap. Engine-agnostic; edgegap-unity has a ready Unity Dockerfile.'
metadata:
  version: "0.2.4"
---

# Containerizing a game server for Edgegap

## The container contract

An image runs correctly on Edgegap when:

1. **It is `linux/amd64`.** Edgegap runs Linux x86-64 only. No Windows containers, no ARM images. On Apple Silicon and other ARM machines, always build with `--platform linux/amd64`; an ARM image fails on Edgegap with `exec format error` or "not found".
2. **The server starts with no input.** No prompts, no TTY, headless flags on (Unity `-batchmode -nographics`, Godot `--headless`, Unreal server target with `-log`). Configuration arrives as env vars (`edgegap-server-design`).
3. **The game server is PID 1, or receives signals.** Use exec-form `CMD`/`ENTRYPOINT` (`["./server", "-log"]`), or end a start script with `exec ./server "$@"`. A shell that stays PID 1 swallows SIGTERM and the server dies at SIGKILL without draining. `npm start` has the same problem; run `node server.js` directly.
4. **It binds `0.0.0.0` on the internal port** declared in the app version, with the matching protocol.
5. **It logs to stdout/stderr.** Log files inside the container are invisible to Edgegap.
6. **No secrets in the image.** Not the Edgegap API token, not registry credentials, not third-party keys. Secrets go on the app version as hidden env vars.
7. **It never prints its environment.** `env;` in a CMD (common in older templates) writes `ARBITRIUM_DELETE_TOKEN` into the logs.
8. **Non-root where the engine requires it.** Run Unreal dedicated servers as a non-root user (`edgegap_generate_dockerfile` does, and `edgegap_validate_server_config` flags root).

The Edgegap MCP tool `edgegap_generate_dockerfile` writes a Dockerfile for Unity, Unreal, Godot or any other engine with these rules applied, and `edgegap_validate_server_config` checks an existing one (ARM base, root Unreal, missing headless flags, `localhost` binding, port/transport mismatch, `latest` tag). Use them when available.

## Dockerfile pattern

Build the server outside Docker (engine editors rarely run in containers), then copy only the server build in:

```dockerfile
FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
# ca-certificates: HTTPS calls from the server (self-stop, your backend)
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -m server
WORKDIR /home/server/app
COPY --chown=server:server build/linux-server/ ./
RUN chmod +x ./MyGameServer
USER server

# Documentation only; Edgegap exposes the ports declared on the app version.
EXPOSE 7777/udp
ENTRYPOINT ["./MyGameServer", "-log"]
```

Variants:
- **Node / web servers**: `FROM node:22-slim`, `npm ci --omit=dev` in the image, `CMD ["node", "server.js"]`. Use `WS` ports with TLS Upgrade for browser clients (below).
- **Compiled languages** (Go, Rust, C++): multi-stage build, compile in a builder stage with `--platform=linux/amd64`, copy the binary into a slim runtime image.
- **Engine needs a config file**: render it at start from env vars in a small `entrypoint.sh` that ends with `exec`.

Add a `.dockerignore` so the build context contains only the server build (not the whole project, `Library/`, `Saved/`, `.git`).

## Build and push

The Edgegap Container Registry is `registry.edgegap.com`. The dashboard's Container Registry page shows the **project**, a push **username** (`robot$...`) and **token**. Have the developer log in themselves so the token stays out of the chat:

```bash
docker login registry.edgegap.com -u '<username>'
docker build --platform linux/amd64 -t registry.edgegap.com/<project>/<image>:<tag> .
docker push registry.edgegap.com/<project>/<image>:<tag>
```

Keep the single quotes around the username in bash; `$` in it must not expand.

**Tags:** a fresh tag on every build, never `latest`, never re-push a changed image under an existing tag. Edgegap caches by tag, so an overwritten tag keeps serving the old build. Use a UTC timestamp `YYYYMMDD-HHMM` (e.g. `20261022-1430`, from `date -u +%Y%m%d-%H%M`), the same string for the image tag and the app version name, so anyone can see when the server was last updated. Lowercase image names, no spaces. To build, push and create the version on every commit, use GitHub Actions with `edgegap/deploy-action` after the push step (see `edgegap-launch`).

Confirm the push with `edgegap_list_registry_tags` (image name only, without project or tag). Free tier registry space is 10 GB; delete old tags in the dashboard when full (`exceed the configured upper limit`).

**Other registries** (Docker Hub, GHCR, AWS ECR, GCP, GitLab) work the same way: put the registry host in the version and give the version pull credentials. Guides: https://docs.edgegap.com/docs/tools-and-integrations/docker/external-registries.

## Register it as an app version

`edgegap_list_apps` → `edgegap_create_app` if needed → `edgegap_create_app_version` (or the dashboard, or `POST /v1/app/{app}/version`):

| Field | Value |
|---|---|
| name | the image tag (`20261022-1430`), so the version shows which build it runs and when |
| registry | `registry.edgegap.com` (host only, no scheme) |
| image | `<project>/<image>` |
| tag | the tag you pushed |
| vCPU / memory | 1024 units = 1 vCPU; minimum 256 (0.25 vCPU); memory at most 2× vCPU units in MB. Start at 1024 / 2048 and size from measurements |
| ports | `[{ "port": 7777, "protocol": "UDP", "name": "gameport" }]`, internal port = what the server binds |
| registry credentials | none for registry.edgegap.com: `edgegap_create_app_version` sends `registry_profile: "Edgegap"` when you leave `registry_username`/`registry_token` out (MCP 0.17.0+), and Edgegap pulls with the organization's own registry login. Other private registries need their pull login; a version without one is the top cause of `Unable to pull image from registry` / 424 |
| restart policy | `never` for match servers (`restart_policy: "never"` on `edgegap_create_app_version`, MCP 0.16.0+) |
| max duration | minutes; cloud maximum 1440 (24 h), free tier 60 |

Then check with `edgegap_list_app_versions` that `registry_credentials_set` is true before deploying. Creating a new version, or duplicating one in the dashboard to change ports or resources, needs no rebuild.

**Browser (WebGL / web) clients** need `wss://`. Use protocol `WS` with **TLS Upgrade** on that port: Edgegap terminates TLS for `*.pr.edgegap.net`, so the server keeps speaking plain `ws`. Clients connect to `wss://<fqdn>:<external port>`. (Custom domains: protocol `WSS` and your own certificate.)

## Verify before shipping

Run `edgegap-local-testing` before the first deployment of a new image: it catches ARM images, wrong ports, PID 1 problems and slow boots in seconds instead of in a billed deployment.

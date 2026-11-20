---
name: docker-sandbox
description: Run Docker and containers in a cloud sandbox — a full root Ubuntu VM with Docker preinstalled and its own kernel, so `docker build`/`docker run`/compose work with no extra setup. Default 4 vCPU / 8 GB / 51 GB disk, $0.036/h billed per second. Use to build images, run compose stacks, or test containers off-host.
---

# Docker sandbox (Box)

Use this when a task needs **Docker**: building an image, running `docker compose`, or testing a container. On some sandboxes Docker needs extra setup or a different runtime; Box is a full VM with Docker (BuildKit, Compose) preinstalled on its own kernel.

## Why Box

- **Docker preinstalled, real machine** — `docker build`, `docker run`, compose stacks.
- **51 GB disk on the default size** — room for images and layers; larger sizes have 111 GB or 251 GB.
- **Cheap & isolated** — per-second billing, separate from the host.

## Prereqs

`curl -fsSL https://box.ascii.dev/install | sh`, then `box login "$BOX_API_KEY" --json`.

## Recipe

```bash
box_id="$(box new --json | jq -r 'select(.event == "ready") | .id')"
box ssh "$box_id" -- bash -s < ./clone-and-build.sh   # git clone + docker build
box ssh "$box_id" -- "cd /project && docker compose up -d"
box ssh "$box_id" -- "host 8080"                       # expose the running container
box delete "$box_id" --json
```

## Limits

Runs in Germany, Finland and France (no region choice); $20 plan: 100 sandboxes at once; disk-level snapshots (containers don't survive stop/resume — restart compose after resume; the Docker build cache and untagged images are not saved).

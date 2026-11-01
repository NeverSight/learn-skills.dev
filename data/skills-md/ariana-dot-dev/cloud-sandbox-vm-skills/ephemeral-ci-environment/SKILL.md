---
name: ephemeral-ci-environment
description: Get a clean, reproducible ephemeral environment for CI and testing — a fresh root Ubuntu VM with every major toolchain and Docker preinstalled, your GitHub repo auto-cloned in, and the whole thing thrown away after. Per-second billing makes each run cost cents. Use to run tests, reproduce a bug, or validate a build in a pristine environment without polluting the host.
---

# Ephemeral CI / test environment (Box)

Use this when you need a **clean, throwaway environment** to test a repo, run a CI job, or reproduce a bug — identical every time, with nothing left behind. Every run starts from a fresh VM with all toolchains preinstalled, so there's no "works on my machine" drift.

## Why Box

- **Pristine + reproducible** — fresh VM per run; no leftover state.
- **Batteries included** — Docker + Node/Python/Go/Rust/Java/etc. already there; repo auto-clones in.
- **Cheap per run** — per-second billing; a test run costs cents, and you `box delete` after.

## Prereqs

`curl -fsSL https://box.ascii.dev/install | sh`, then `box login "$BOX_API_KEY" --json`. (Select the repo to auto-clone in the dashboard, or clone it in setup.)

## Recipe

```bash
box_id="$(box new --json | jq -r 'select(.event == "ready") | .id')"
trap 'box delete "$box_id" --json' EXIT
box ssh "$box_id" -- "cd /project && npm ci && npm test"
box ssh "$box_id" -- "cat /project/junit.xml" > junit.xml      # pull results back
```

## Limits

EU-only; 100 active VMs soft cap. For thousands of <500 ms parallel CI shards, dedicated CI runners scale further; Box is best for full-machine, Docker-capable, reproducible runs.

---
name: tilt-config
description: Create, update, and troubleshoot Tilt configuration (Tiltfile, Tiltfile extensions, and common Tiltfile API usage like docker_build/custom_build/live_update, k8s_yaml/k8s_resource, local_resource, and Docker Compose/Helm workflows). Use when asked to add Tilt to a repository, adjust dev-environment orchestration, or debug Tiltfile evaluation/resource update issues. Prefer consulting the local Tilt documentation source at /Users/alexeus/src/tilt.build/docs (and the generated API includes under /Users/alexeus/src/tilt.build/src/_includes/api) when available.
---

# Tilt Config

## Workflow

1. Inventory the repo and target workflow
   - Detect existing Tilt: `Tiltfile`, `tilt_config.json`, `.tiltignore`, `.tilt-dev/`, `tilt_modules/`.
   - Detect orchestration inputs: Kubernetes YAML, Helm charts, Kustomize, Dockerfiles, `docker-compose.yml`, local dev commands (Makefile, task runners).
   - Confirm intent (local dev, CI via `tilt ci`, or both) and the execution environment (local cluster vs remote cluster).

2. Choose the minimal Tilt resource model
   - Prefer the simplest setup that matches the repo:
     - Kubernetes-first: load manifests, register image builds, then refine with resource grouping/port-forwards.
     - Docker Compose-first: wire `docker_compose`/Compose resources when the repo already uses Compose.
     - Local-process-first: use `local_resource` for non-containerized dev servers and build steps.
   - Keep effects at the edge: Tiltfile should orchestrate dev flows, not replace the app’s own build tooling.

3. Author or update `Tiltfile` iteratively
   - Start with a small working Tiltfile, then add features (live_update, buttons, triggers, health checks) only when needed.
   - Use local docs to confirm exact function signatures and semantics before writing non-trivial Tiltfile code.

4. Debug with first-party diagnostics
   - Prefer `tilt doctor` output when reporting or investigating environment issues.
   - Prefer inspecting specific resource state (e.g., via `tilt get ... -o json`) and resource logs rather than restarting `tilt up`.

## Local Tilt docs (source checkout)

This skill assumes the Tilt docs source is available at:

- `/Users/alexeus/src/tilt.build/docs` (docs pages)
- `/Users/alexeus/src/tilt.build/src/_includes/api` (generated Tiltfile API reference HTML)
- `/Users/alexeus/src/tilt.build/src/_data/snippets` (curated Tiltfile snippet examples)

Use the helper script in this skill:

- Search docs quickly: `python3 scripts/tilt_docs.py rg docker_build`
- Extract API reference section: `python3 scripts/tilt_docs.py api docker_build`
- Show a snippet example: `python3 scripts/tilt_docs.py snippet docker_build_simple`

For more details on paths and how the script works, load `references/tilt-docs-local.md`.

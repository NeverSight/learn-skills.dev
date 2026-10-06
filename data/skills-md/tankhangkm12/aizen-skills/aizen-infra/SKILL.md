---
name: aizen-infra
description: Aizen knowledge pack (v24) — pipelines with security gates (Gitleaks, Trivy, Semgrep), environments, deploy and rollback, secrets, observability, incidents; Docker, Podman, Docker Hub, Cloudflare Tunnel, Kubernetes/Helm, GitHub Actions, GitLab CI, Terraform. Loaded by Aizen roles through their brief; not a standalone skill, do not trigger it directly — use aizen-build.
---

# Infrastructure and delivery knowledge — Aizen pack (v24)

Owns the topics `infra`: every `references/<topic>/…`, `assets/<topic>/…` and `scripts/<topic>/…` path for them
lives here. Shared rules (authority, evidence, code quality, style) are in `aizen-core`; the flow and roles are in
`aizen-build`.

- **Used by:** devops; reviewer (infra lens); aizen-init.
- **Entry points:** `references/infra/method.md` — each has a "Guides" table; load only the rows the change touches.
- Tools: `scripts/infra/pipeline_scaffold.py`, `scripts/infra/connectivity.py`, `scripts/infra/secrets_checklist.py`. Templates: `assets/infra/` (infrastructure doc, incident report, release PR, release packet, hand-over docs).

## Upstream knowledge (vendored, pinned)

Best practice from the people who build the tools, copied verbatim at a pinned commit (`vendor.lock.json`
in the Aizen repo). It says how to do a thing right in that tool; Aizen core rules still decide how much to build
and who decides (`references/core/workspace.md` §3).

| Source | Details |
|---|---|
| Docker Inc. — build strategies, compose patterns, destructive-command guardrails | `references/infra/vendor/docker/UPSTREAM.md` |
| KubeShark — Kubernetes failure-mode workflow | `references/infra/vendor/kubeshark/UPSTREAM.md` |

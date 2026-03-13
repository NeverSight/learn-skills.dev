---
name: dockerfile-best-practices
description: "Design Dockerfiles for secure, deterministic, and efficient image builds with minimal attack surface and reproducible dependencies. Use when image build behavior, layer strategy, and runtime hardening need explicit decisions; do not use for non-container runtime code style concerns."
---

# Dockerfile Best Practices

## Overview
Use this skill to create images that build reliably, run securely, and minimize size/startup overhead.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Layer and cache strategy guidance:
  - `references/dockerfile-layer-cache-guidance.md`

## Templates And Assets
- Dockerfile baseline:
  - `assets/Dockerfile.template`
- Image hardening checklist:
  - `assets/image-hardening-checklist.md`

## Inputs To Gather
- Runtime requirements and base image constraints.
- Dependency installation and caching strategy.
- Security/compliance requirements for runtime image.
- Build reproducibility and provenance requirements.

## Deliverables
- Hardened Dockerfile with rationale for key choices.
- Build-cache strategy and layer ordering notes.
- Runtime hardening checklist (user, filesystem, capabilities).
- Image verification steps (size, vulnerabilities, startup behavior).

## Quick Example
- Multi-stage build: compile in builder, copy only runtime artifacts.
- Pin dependency versions and base image digest when policy requires.
- Use non-root user in final stage.
- Keep only required runtime packages in final image.

## Quality Standard
- Build is deterministic enough for release confidence.
- Final image includes minimal required artifacts only.
- Runtime privileges and writable paths are minimized.
- Secrets are not baked into image layers.

## Workflow
1. Select base image aligned to runtime and policy.
2. Design multi-stage build and layer ordering for cache efficiency.
3. Apply runtime hardening in final stage using `assets/image-hardening-checklist.md`.
4. Validate build reproducibility and image behavior.
5. Verify security and size/performance constraints.

## Failure Conditions
- Stop when image requires unnecessary root privileges.
- Stop when build embeds secrets or unstable dependency sources.
- Escalate when vulnerability posture exceeds accepted threshold.

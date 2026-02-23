---
name: ci-cd-architecture
description: CI/CD pipelines, deployment strategy, and infrastructure. Use when setting up GitHub Actions workflows, choosing deployment platforms, configuring production environments, securing pipelines with OIDC, optimizing build performance, building container images, measuring DORA metrics, or setting up Docker multi-stage builds.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# CI/CD & Deployment

## Overview

Covers CI/CD pipeline design, deployment platform selection, and production infrastructure. Focuses on GitHub Actions with hardened security (OIDC, permission scoping, action pinning), Bun-first build optimization, and deployment patterns from MVP to enterprise scale.

**When to use:** Setting up GitHub Actions workflows, choosing deployment targets, configuring OIDC for cloud providers, optimizing CI performance, planning multi-environment pipelines.

**When NOT to use:** Application-level architecture decisions (use framework-specific skills), Kubernetes cluster management (use dedicated IaC tools), cloud provider console configuration.

## Quick Reference

| Need                      | Solution                                            |
| ------------------------- | --------------------------------------------------- |
| MVP deploy (< 1K users)   | Vercel, Netlify, Railway, Cloudflare Pages          |
| Growing product (1K-100K) | AWS Amplify, Cloud Run, Fly.io, Render              |
| Enterprise (100K+)        | AWS ECS/EKS, GKE, DigitalOcean App Platform         |
| Static site               | Vercel, Netlify, Cloudflare Pages                   |
| Full-stack + DB           | Railway, Render, AWS Amplify                        |
| Global low latency        | Cloudflare Workers, Vercel Edge, Fly.io             |
| Compliance (HIPAA, SOC 2) | AWS, GCP, Azure                                     |
| Cloud auth from CI        | OIDC roles (never long-lived keys)                  |
| Action pinning            | Pin to commit SHA, not tag                          |
| Bun CI caching            | `~/.bun/install/cache` keyed on lockfile            |
| Pipeline security         | StepSecurity Harden-Runner for egress control       |
| Container builds          | Multi-stage Dockerfile: builder + runtime stage     |
| Docker layer caching      | `--cache-from` + `actions/cache` for buildx         |
| Multi-platform builds     | `docker buildx` targeting `linux/amd64,linux/arm64` |
| Image scanning            | Trivy or Snyk in pipeline before push               |
| Registry push             | GHCR (`ghcr.io`), ECR, Docker Hub                   |
| Pipeline stages           | build → test → security scan → deploy               |
| DORA: deploy frequency    | Track deployments per day/week per service          |
| DORA: lead time           | Commit-to-production time; target < 1 hour          |
| DORA: change failure rate | % of deploys causing incidents; target < 5%         |
| DORA: MTTR                | Mean time to restore; target < 1 hour               |

## Common Mistakes

| Mistake                                                   | Correct Pattern                                                                      |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Storing long-lived AWS/GCP/Azure keys as GitHub secrets   | Use OIDC roles with `id-token: write` permission for zero-trust cloud auth           |
| Pinning GitHub Actions to tags instead of commit SHAs     | Pin third-party actions to full commit SHA to prevent supply chain attacks           |
| Leaving `permissions` as default (broad) on workflows     | Explicitly scope permissions at the job level; default to `contents: read`           |
| Running full CI on every branch push                      | Use `on.pull_request` filters and path-based triggers to avoid wasted compute        |
| Over-engineering infrastructure before product-market fit | Start with managed platforms (Vercel, Railway); scale to AWS/GKE only when needed    |
| Using outdated action versions (v3 or older)              | Use current major versions: checkout@v6, cache@v5, configure-aws-credentials@v5      |
| Caching only `bun.lockb` without considering `bun.lock`   | Bun 1.2+ uses text-based `bun.lock`; hash whichever lockfile format the project uses |
| Skipping preview deployments for PRs                      | Every PR should get a preview URL for testing before merge                           |

## Relationship to Other Skills

> If the `github-actions` skill is available, delegate detailed workflow authoring, matrix strategies, and composite actions to it. This skill covers CI/CD architecture and platform selection; `github-actions` covers workflow syntax depth.
> If the `deployment-strategy` skill is available, delegate deployment pattern selection (blue-green, canary, rolling) to it. This skill covers platform selection and CI pipeline mechanics.

## Delegation

- **Audit existing CI workflow security and permissions**: Use `Explore` agent to scan workflow YAML files for broad permissions, unpinned actions, and exposed secrets
- **Set up multi-environment deployment pipelines**: Use `Task` agent to create dev/staging/prod workflows with environment protection rules
- **Plan migration from managed platform to containerized infrastructure**: Use `Plan` agent to evaluate current deployment, define migration steps, and select target architecture

## References

- [GitHub Actions workflows, OIDC, matrix builds, and security hardening](references/github-actions.md)
- [Deployment patterns: Jamstack, serverless, traditional, microservices](references/deployment-patterns.md)
- [Platform selection framework, database needs, and cost optimization](references/platform-selection.md)
- [Monitoring, observability tiers, and deployment checklists](references/monitoring.md)
- [Container builds: multi-stage Dockerfiles, layer caching, buildx, image scanning, and registry push](references/container-builds.md)

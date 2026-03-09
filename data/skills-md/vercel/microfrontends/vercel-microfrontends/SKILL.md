---
name: vercel-microfrontends
description: Guide for building, configuring, and deploying microfrontends on Vercel. Use this skill when the user mentions microfrontends, multi-zones, splitting an app across teams, independent deployments, cross-app routing, incremental migration, composing multiple frontends under one domain, microfrontends.json, @vercel/microfrontends, the microfrontends local proxy, or path-based routing between Vercel projects. Also use when the user asks about shared layouts across projects, navigation between microfrontends, fallback environments, asset prefixes, or feature flag controlled routing.
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel Microfrontends
Split a large application into independently deployable units that render as one cohesive app. Vercel handles routing on its global network using `microfrontends.json`.

**Core concepts:** default app (has `microfrontends.json`, serves unmatched requests) · child apps (have `routing` path patterns) · asset prefix (prevents static-asset collisions) · independent deployments.

**Frameworks:** Next.js (App Router + Pages Router), SvelteKit, React Router, Vite — all via `@vercel/microfrontends`.

**CLI:** `microfrontends proxy` (local dev proxy) · `microfrontends port` (print auto-assigned port).

## Finding Detailed Information

This skill includes detailed reference docs in the `references/` directory. **Do not read all references upfront.** Instead, search or grep the relevant file when the user asks about a specific topic:

| Topic | Reference file |
|---|---|
| Getting started, quickstart, framework setup, `microfrontends.json` schema, fields, naming, examples | `references/configuration.md` |
| Path expressions, asset prefixes, flag-controlled routing, middleware | `references/path-routing.md` |
| Local proxy setup, polyrepo config, Turborepo, ports, deployment protection | `references/local-development.md` |
| Adding/removing projects, fallback environments, navigation, observability | `references/managing-microfrontends.md` |
| Testing utilities (`validateMiddlewareConfig`, `validateRouting`, etc.), debug headers, common issues | `references/troubleshooting.md` |
| Deployment protection, Vercel Firewall, WAF rules for microfrontends | `references/security.md` |

When the user asks about a specific topic, use grep or search over the relevant reference file to find the answer without loading all references into context.

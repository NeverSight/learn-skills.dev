---
name: open-design
description: |
  Open-source local-first alternative to Claude Design with 31 design skills (web prototypes,
  SaaS landing pages, dashboards, mobile onboarding, gamified apps, email, social carousels,
  poster design, motion frames, sprite animation) and 71 brand-grade design systems. Runs as
  a daemon plus web UI or desktop app.
triggers:
  - "open-design"
  - "open design platform"
  - "nexu-io platform"
  - "31 design skills"
  - "71 design systems"
das:
  category: creative-3d
  upstream: "https://github.com/nexu-io/open-design"
  version: latest
  install: false
---

# open-design

> Catalogue stub — full platform: [nexu-io/open-design](https://github.com/nexu-io/open-design)

## Account / environment requirement

**Local Node.js/pnpm environment required** (no cloud account needed). open-design runs fully locally as a daemon process with a browser-based web UI, or as a downloadable desktop app.

## Install methods

| Method | Command / Link |
|--------|---------------|
| Desktop app (recommended) | Download from [open-design.ai](https://open-design.ai) |
| Self-hosted (web UI) | `git clone https://github.com/nexu-io/open-design && pnpm install && pnpm tools-dev run web` |
| Daemon only | `pnpm tools-dev run daemon` after clone + install |

## Decision tree

1. **Do you want the desktop app?**
   - Yes → download from [open-design.ai](https://open-design.ai) and launch.
   - No → go to step 2.
2. **Do you have Node.js and pnpm?**
   - No → install pnpm: `npm install -g pnpm`, then Node.js from [nodejs.org](https://nodejs.org).
   - Yes → clone and install per the table above.
3. **Is the daemon running?** Access the web UI at `http://localhost:PORT` (shown on start).

## What it does

A local-first open-source platform that ships 31 design skills covering the full product design spectrum: web prototypes, SaaS landing pages, dashboards, mobile onboarding flows, gamified app UIs, email templates, social carousels, poster design, motion frames, and sprite animation. Also includes 71 brand-grade design system definitions that can be applied across any skill. Designed as a self-hosted alternative to Claude Design with no vendor lock-in.

## When NOT to use

- Single-skill tasks where the platform overhead isn't warranted — install the individual skill directly
- Without Node.js/pnpm or the ability to run a local daemon
- Cloud-only environments (CI, serverless) — the platform requires a persistent local process

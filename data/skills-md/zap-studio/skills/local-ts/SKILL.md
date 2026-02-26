---
name: local-ts
description: Use when starting or modifying apps based on the local.ts starter kit or its local-first desktop/mobile features.
---

# local-ts

## Overview

Local-first starter kit for desktop and mobile apps with Tauri, SQLite, and a React frontend.

## When to Use

- Bootstrapping a new app from the local.ts template
- Modifying built-in features like settings, tray, notifications, database, theming, logging, window state, autostart, or splash
- Debugging local.ts development workflows

## When Not to Use

- Building a web-only app without Tauri or local-first constraints

## Quick Reference

- Install: `pnpm install`
- Run: `pnpm run tauri dev`
- Prereqs: Node.js v18+, Rust, pnpm

## Inputs to Request

- Target platforms (desktop, mobile, or both)
- Features to add or change
- Error logs or exact repro steps

## Resources

- https://www.zapstudio.dev/local-ts
- https://www.zapstudio.dev/llms.txt

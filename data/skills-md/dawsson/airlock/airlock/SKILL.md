---
name: airlock
description: Self-hosted Expo OTA update server. Airlock is a Hono library you mount on your existing API to serve Expo Updates protocol v1 manifests. Use this skill when working on the airlock server, CLI, adapters, or when integrating airlock into an Expo app.
license: MIT
compatibility: Requires bun, Hono, Expo project
metadata:
  author: Dawsson
  version: "0.1.0"
---

# Airlock

Self-hosted Expo OTA update server. Ships as a Hono library (`createAirlock`) you mount on your existing API.

## Reference Files

- `references/cli.md` — Full CLI reference: all commands, flags, and config
- `references/integration.md` — How to mount airlock on a Hono server and configure an Expo app
- `references/alchemy.md` — Deploying with Alchemy (recommended): provisioning KV + R2 + Worker, generating secure tokens, existing vs new resources

## Quick Reference

- Package: `@dawsson/airlock`
- CLI entry: `airlock <command>`
- Config file: `.airlockrc.json` (or env vars `AIRLOCK_SERVER`, `AIRLOCK_TOKEN`)
- Public routes: `GET /manifest`, `GET /assets/:hash`
- Admin routes: under `/admin/*`, all require `Authorization: Bearer <token>`
- Built-in adapters: `CloudflareAdapter` (KV + R2), `MemoryAdapter` (tests)
- Channels scoped by: `{channel}/{runtimeVersion}/{platform}`
- Default channel: `"default"`
- Rollout: deterministic SHA-256 of `deviceId + updateId`, mod 100

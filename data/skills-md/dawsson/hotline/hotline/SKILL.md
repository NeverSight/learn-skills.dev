---
name: hotline
description: Integrate hotline into a React Native or Expo app. Hotline is a local WebSocket dev bridge that lets CLI tools and AI agents send commands to and query data from running apps in real time.
license: MIT
compatibility: Requires bun, React Native or Expo project
metadata:
  author: Dawsson
  version: "0.3.2"
---

# Hotline

Local WebSocket dev bridge for React Native apps. Lets CLI tools and AI agents send commands to and query data from running apps in real time.

## Reference Files

- `references/integration.md` — How to add hotline to a React Native / Expo project
- `references/handlers.md` — Standard handlers and the handler format
- `references/agent-usage.md` — CLI commands and automation patterns for AI agents
- `references/events.md` — Event system for real-time app-to-agent communication

## Quick Reference

- Import: `@dawsson/hotline/src/client`
- Server port: `8675`
- Handler format: `{ handler, fields, description }` — no bare functions
- Production safe: no-op when `__DEV__` is false
- `ping` is built-in, no need to register it

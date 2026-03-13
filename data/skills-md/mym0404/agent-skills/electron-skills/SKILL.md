---
name: electron-skills
description: >
  Type-safe Electron IPC architecture with centralized API types, helper functions,
  and a 5-step process for adding new IPC endpoints.
  Use when building or extending Electron main/preload/renderer IPC communication.
license: MIT
metadata:
  author: mj
  version: "1.0.0"
---

# Electron Skills

End-to-end type-safe IPC architecture for Electron apps.

## Rule Categories by Priority

| Priority | Category         | Impact   | Prefix |
| -------- | ---------------- | -------- | ------ |
| 1        | IPC Architecture | CRITICAL | `ipc-` |

## Quick Reference

- `ipc-type-safe-architecture` — Central API type, helper functions, preload bridges, main handlers, 5-step wiring process
- `ipc-app-error-system` — Structured error handling across IPC boundary with throwAppError / catchAppError

## How to Use

Read rule files for examples:

```
rules/ipc-type-safe-architecture.md
rules/ipc-app-error-system.md
```

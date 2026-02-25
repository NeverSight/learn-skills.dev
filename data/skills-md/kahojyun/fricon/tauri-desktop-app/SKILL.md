---
name: tauri-desktop-app
description: Guidelines and workflows for building, reviewing, and securing Tauri desktop apps (React/Vite frontends). Use when implementing Tauri IPC commands, native API access, file system or dialog integration, window/menu/tray behavior, permissions/allowlist/CSP, app lifecycle, auto-updater, or packaging/release tasks.
---

# Tauri Desktop App

## Overview

Use this skill to design and implement Tauri desktop features safely and consistently, with a focus on IPC boundaries, permission scoping, and production readiness.

## Project-Specific Rules (fricon)

- This repository uses Tauri v2 with `tauri-specta` for typed IPC bindings.
- Keep IPC bindings generation explicit via script (`pnpm --filter fricon-ui run gen:bindings`), not automatic on debug app startup.
- Keep CI `fmt` lightweight. Do not add Rust-compiling or bindings-generation work to `fmt`; place those checks in `test`.
- Treat generated bindings (`crates/fricon-ui/frontend/src/lib/bindings.ts`) as generated artifact:
  - Regenerate when Rust command/event signatures change.
  - Keep linter/formatter noise out of this file via ignore configuration.

## Quick Triage

- IPC, Rust commands, native APIs, file system access, or CSP: read `references/tauri-security-and-ipc.md`.
- Windows, menus, tray, deep links, updater, or packaging: read `references/tauri-app-features.md`.

## Workflow

1. Classify the request: frontend-only or needs a Rust command.
2. Define the security surface: permissions/allowlist, input validation, and least-privilege APIs.
3. Implement the Rust command and frontend wrapper with typed payloads and explicit errors.
4. Integrate UX behavior (window, menu, tray, shortcuts) and persistence.
5. Update config/build settings for production, packaging, and updater.
6. If IPC changed, regenerate `bindings.ts` and ensure CI checks still match project policy.

## Conventions

- Keep IPC small and explicit. Prefer a few narrow commands over a broad generic bridge.
- Validate all inputs in Rust. Treat frontend data as untrusted.
- Keep a single frontend entry module for native calls (example: `src/lib/tauri.ts`).
- For file operations, constrain to user-selected paths and validate path traversal.

## Example Triggers

- "Add a file-open dialog and read a file"
- "Expose a Rust command for database access"
- "Add a tray icon with a menu"
- "Package for macOS/Windows and enable auto-updater"

## References

- `references/tauri-security-and-ipc.md`
- `references/tauri-app-features.md`

---
name: tauri-frontend
description: Build Tauri 2 frontend code that calls native functionality through explicit IPC and remains testable. Use when implementing UI, invoking commands, handling events, or integrating a frontend framework with Tauri.
---

# Tauri frontend

This skill is scoped to Tauri 2. Verify version-sensitive fields against the installed CLI, framework adapter, and [frontend documentation](https://v2.tauri.app/start/frontend/).

## Workflow

1. Confirm the project's framework, package manager, build command, `@tauri-apps/api` version, dev URL, and output directory. Use installed types and the matching [frontend setup](https://v2.tauri.app/start/frontend/) rather than generic web assumptions.
2. Treat Tauri's frontend as a static/SSG artifact consumed by the WebView. Configure `frontendDist` and the dev server explicitly. Tauri does not itself provide a general SSR server at runtime; SSR frameworks need a compatible build/export strategy or an separately deployed server and carefully modeled remote access.
3. Verify framework-specific configuration from the official pages before changing it: [Next.js](https://v2.tauri.app/start/frontend/nextjs/), [Nuxt](https://v2.tauri.app/start/frontend/nuxt/), [Qwik](https://v2.tauri.app/start/frontend/qwik/), [SvelteKit](https://v2.tauri.app/start/frontend/sveltekit/), and [Vite](https://v2.tauri.app/start/frontend/vite/). Confirm static output, asset paths, routing fallback, and dev/production parity with a real build.
4. Import only required API modules. Call named commands with typed payloads using `invoke`; never construct command names from user input. Use events for notifications and channels for ordered streams where appropriate.
5. Model loading, success, and error states. Normalize errors at the UI boundary without hiding the original diagnostic, and unregister listeners when the view is destroyed.
6. Keep a browser-compatible adapter or mock for unit tests when the UI can run outside the Tauri WebView.

## Safe defaults

- Treat all frontend input as untrusted; Rust validates it again.
- Do not put secrets in bundles, local storage, URLs, or command arguments.
- Avoid broad window or filesystem permissions for prototypes.
- Follow [calling Rust](https://v2.tauri.app/develop/calling-rust/) and keep IPC payloads small and versioned when needed.

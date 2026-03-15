---
name: moonrepo-project-config
description: "Use when creating or modifying moon.yml project configs, adding tasks, defining file groups, or configuring task options"
---

# Moon v2 — Project Configuration

Reference for `moon.yml` project configuration files.

## Project Metadata

```yaml
$schema: 'https://moonrepo.dev/schemas/project.json'
layer: application    # application | library | tool | automation | configuration | scaffolding
language: typescript  # typescript | javascript | php | python | rust | go | bash
stack: frontend       # frontend | backend | systems | infrastructure | data
```

**Key v2 change:** `type:` was renamed to `layer:`.

## File Groups

Named file pattern collections referenced by tasks via `@group(name)`.

```yaml
fileGroups:
  sources:
    - 'src/**/*.ts'
    - '!src/**/*.test.ts'
  configs:
    - 'package.json'
    - 'tsconfig.json'
```

Use `@group(sources)` in task inputs — not bare `sources` or `@globs()`.

## Tasks

### command vs script

| Use | When |
|-----|------|
| `command:` | Single executable, no shell features. Supports inheritance merging. |
| `script:` | Pipes, redirects, chaining (`&&`, `\|\|`, `;`). No inheritance merging. |

```yaml
tasks:
  lint:
    command: 'eslint src/'
    inputs: ['@group(sources)', '@group(configs)']
    options:
      cache: true
      runInCI: affected

  build:
    script: 'rm -rf dist && tsc --build'
    inputs: ['@group(sources)']
    outputs: ['dist/']
    deps: ['~:codegen']
```

### Task Fields

| Field | Purpose |
|-------|---------|
| `command` / `script` | What to run |
| `inputs` | Files that determine if task needs re-running |
| `outputs` | Files/directories produced (enables caching) |
| `deps` | Tasks to run first: `'project:task'` or `'~:task'` (same project) |
| `env` | Environment variables: `{ NODE_ENV: 'production' }` |
| `options` | Execution modifiers (see below) |
| `preset` | `server` (long-running) or `utility` (interactive, no cache) |

### Common Options

| Option | Default | Purpose |
|--------|---------|---------|
| `cache` | `true` | Enable output caching |
| `runInCI` | `affected` | When to run in CI: `always`, `affected`, `false`, `only`, `skip` |
| `persistent` | `false` | Long-running process (dev servers) |
| `shell` | `true` | Execute within shell |
| `retryCount` | `0` | Retry on failure |
| `outputStyle` | — | `buffer`, `buffer-only-failure`, `stream`, `hash`, `none` |
| `runFromWorkspaceRoot` | `false` | Run from monorepo root instead of project |

## Pitfalls

| Mistake | Fix |
|---------|-----|
| `type: application` | Use `layer: application` (v2 rename) |
| `command: 'a && b'` | Use `script:` for shell features |
| `inputs: ['sources']` | Use `inputs: ['@group(sources)']` |
| Missing `outputs` on cacheable task | Define outputs or caching has no effect |
| `platform: node` | Use `toolchains` field or omit (auto-detected) |

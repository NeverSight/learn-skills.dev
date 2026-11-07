---
name: genesis
description: Use when starting a new repo or scaffolding a full-stack project — a Go backend, a React/Vite web frontend, Dockerfiles, docker-compose, a Makefile, sqlc. Refers to reference/project-00 in github.com/lwlee2608/genesis as the canonical template.
user-invocable: true
disable-model-invocation: true
argument-hint: "[new | server | web | docker-compose | Dockerfile | Makefile | sqlc]"
---

# Genesis Scaffolding

Start new repos with the genesis CLI. Add everything else from the `reference/project-00` template in [`lwlee2608/genesis`](https://github.com/lwlee2608/genesis). Never write these files from scratch or from memory.

## Structure

```
reference/project-00/
├── docker-compose.yml          # dev stack: Postgres only
└── services/
    ├── project-00-server/      # Go API
    │   ├── cmd/project-00/     # main, config, logger
    │   ├── internal/
    │   │   ├── api/http/       # router, handlers, dto, middleware
    │   │   └── db/             # migrations, queries, sqlc (generated)
    │   ├── Dockerfile
    │   ├── Makefile
    │   └── sqlc.yaml
    └── project-00-web/         # React/Vite/TS app
        ├── src/                # main.tsx, App.tsx
        ├── Dockerfile          # build + nginx serve
        ├── nginx.conf
        └── entrypoint.sh
```

## Arguments

- `new`, or no argument in a directory that is empty apart from `.git`: follow rule 1.
- Any other argument (e.g. "Add the server", "Set up sqlc") scopes the work. Copy only the matching files, not the whole template.
- No argument in a non-empty directory: ask which parts to scaffold.

## Rules

1. **Start a new repo with `genesis` in flag mode.** Run `genesis -name <app> -module <module>` from the target directory, then add the parts the CLI does not generate from the template.
   - Never run bare `genesis`. It opens a TUI, and exits 1 when there is no TTY.
   - `-name` defaults to the directory name and `-module` to the `origin` remote. Pass both if either is missing or wrong.
   - `-fullstack` and `-http` default to `true`. Turn them off with `=false`.
   - Add `-readme -desc "<one line>"` only if the user asks for an AI README. It needs `OPENROUTER_API_KEY`.
   - The CLI refuses a non-empty directory. Add `-force` only after the user confirms overwriting, because it replaces files silently.
   - If `genesis` is missing, or fails with `flag provided but not defined` (it predates flag mode), ask the user before you install it with `curl -fsSL https://raw.githubusercontent.com/lwlee2608/genesis/main/scripts/install.sh | bash`.

2. **Clone the live repo, never work from memory.** Clone `https://github.com/lwlee2608/genesis` (branch `main`) once with `--depth=1` into `/tmp/genesis-template`. Then read files under `reference/project-00`. The monorepo layout is part of the template, not only the files. The repo evolves, so content from memory drifts.

3. **Adapt, don't blind-copy.** Replace every `project-00` with the project name. It appears in directory names, the Go module `github.com/lwlee2608/project-00`, the `cmd/project-00/` path and binary, `APP :=` in the Makefile, and the Docker image and container names. Use the underscore form for the Postgres database and user (`project_00`). Keep the rest of the template's structure and conventions.

4. **Use Oxlint for the web frontend.** Copy `.oxlintrc.json`, the `oxlint` dependency, and the lint script from the reference. Keep the React Hooks and React Refresh rules. Remove the ESLint config and dependencies it replaces, then regenerate the lockfile with pnpm.

For deploying the result to Railway, use `/genesis-railway`. The prod compose for a VM with Overwatcher comes from `/genesis-cicd overwatcher`.

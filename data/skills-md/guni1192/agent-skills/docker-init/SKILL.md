---
name: docker-init
description: Initialize Dockerfile and .dockerignore for the current project by detecting language, framework, and package manager.
argument-hint: "[target-directory]"
allowed-tools: Read, Glob, Grep, Bash(docker build *)
---

# docker-init

Generate a Dockerfile and .dockerignore tailored to the current project.

## When to use

- When the user asks to create or initialize a Dockerfile
- When the user wants to containerize their project
- When the user runs `/docker-init`

## Instructions

1. **Detect the project type** by scanning the repository for key files:
   - `package.json` / `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` / `bun.lockb` → Node.js
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `pyproject.toml` / `requirements.txt` / `Pipfile` / `setup.py` → Python
   - `Gemfile` → Ruby
   - `*.csproj` / `*.sln` → .NET
   - `build.gradle` / `pom.xml` → Java/Kotlin
   - `mix.exs` → Elixir
   - `deno.json` / `deno.jsonc` → Deno

2. **Detect the package manager and framework** from lock files and config:
   - Node.js: npm / yarn / pnpm / bun; Next.js / Remix / Astro / Express, etc.
   - Python: pip / poetry / uv / pipenv
   - Others: detect from project config files

3. **Determine the entrypoint**:
   - Check `main` or `scripts.start` in `package.json`
   - Check `[package]` in `Cargo.toml`
   - Check `module` in `go.mod`
   - Check `CMD` hints from framework conventions

4. **Generate the Dockerfile** with these best practices:
   - Use a **multi-stage build** (build stage + runtime stage)
   - **Build stage**: use Debian-based official SDK/build images (e.g., `node:22-bookworm`, `golang:1.23-bookworm`, `rust:1.83-bookworm`)
   - When using `apt-get install` in the build stage, always clean up the apt cache. Use this pattern:
     ```dockerfile
     RUN apt-get update && apt-get install -y --no-install-recommends \
         <packages> \
         && rm -rf /var/lib/apt/lists/*
     ```
   - **Runtime stage: use `gcr.io/distroless/*-debian12:nonroot` images** as the base. Choose the appropriate variant:
     - Go: `gcr.io/distroless/static-debian12:nonroot`
     - Rust (statically linked): `gcr.io/distroless/static-debian12:nonroot`
     - Rust (dynamically linked): `gcr.io/distroless/cc-debian12:nonroot`
     - Node.js: `gcr.io/distroless/nodejs22-debian12:nonroot`
     - Python: `gcr.io/distroless/python3-debian12:nonroot`
     - Java: `gcr.io/distroless/java21-debian12:nonroot`
     - .NET: `gcr.io/distroless/dotnet8-debian12:nonroot` (match the .NET version)
   - Always use the **latest stable version** of the language/runtime for base images. Check the project config (e.g., `go.mod`, `Cargo.toml`, `package.json engines`, `.python-version`) to determine the version, and default to the latest stable if unspecified.
   - When downloading binaries via `curl` or `wget`, always **verify the checksum** (e.g., `sha256sum --check`) before using them.
   - **Pin image tags to full semver patch versions** (e.g., `node:22.12.0-bookworm`, `golang:1.23.4-bookworm`) instead of using `latest`, major-only, or minor-only tags. This ensures reproducible builds.
   - Prefer **copying CLI tools from official Docker images** using `COPY --from=` rather than downloading them with `curl`. For example:
     ```dockerfile
     COPY --from=aquasec/trivy:0.58.2 /usr/local/bin/trivy /usr/local/bin/trivy
     ```
   - Copy dependency files first and install dependencies before copying source code to leverage **Docker layer caching**
   - Set appropriate `EXPOSE` port if detectable
   - Do NOT add `HEALTHCHECK` (distroless images do not have a shell or curl)

5. **Generate `.dockerignore`** appropriate for the detected project type. Common exclusions:
   - `.git`, `.github`, `.gitignore`
   - `node_modules`, `__pycache__`, `target`, `dist` (build artifacts)
   - `*.md`, `LICENSE`, `docs/`
   - `.env`, `.env.*`
   - `Dockerfile`, `docker-compose*.yml`
   - IDE/editor files (`.vscode`, `.idea`)

6. **If the project type cannot be determined**, ask the user what language/framework they are using before generating files.

7. **Do not overwrite** existing `Dockerfile` or `.dockerignore` without confirming with the user first.

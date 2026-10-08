---
name: writing-container-configs
description: Use when writing or editing a Dockerfile, choosing a base image tag, adding a multi-stage build, deciding which user a container runs as, or writing a docker-compose.yml or compose.yaml with environment variables, labels, a top-level `version` key, or YAML values like true, 123, or null.
---

# Writing Container Configs

## Overview

Container files should be reproducible, minimal, and least-privilege. Dockerfiles pin their base images, keep build tooling out of the final image, and run as a non-root user. Compose files follow the current Compose Specification and use readable mapping syntax.

**Core principle:** Working is not the same as correct. An old example that still runs, a personal habit, or "it is only an internal image" is not a reason to use `latest`, root, or obsolete Compose syntax by default. Explicit task instructions and repository requirements outrank these defaults; otherwise an exception needs a concrete tool, platform, or legacy-integration constraint.

These rules apply to new or requested changes. Do not rewrite existing working container files solely to match them.

## When to Use

- Creating or editing a Dockerfile, choosing a `FROM` image, or deciding the runtime user.
- Splitting build and runtime stages, or shrinking an image.
- Creating or editing `docker-compose.yml` or `compose.yaml`, especially `environment`, `labels`, or a top-level `version`.
- Reviewing container files copied from older tutorials.

## Quick Reference

| Topic | Do | Do not |
| --- | --- | --- |
| Base image | Pin a specific version tag (`python:3.12-slim`) | Use `latest` in production Dockerfiles |
| Build stages | Use multi-stage builds; copy only build output into the final stage | Ship compilers, dev dependencies, or source you only needed to build |
| Runtime user | Create or select a non-root user and switch with `USER` | Run production containers as root |
| Compose `version` | Omit the top-level `version` key | Copy `version: "3.9"` from old examples |
| Compose `environment` and `labels` | Use mapping syntax: `KEY: value` | Use list syntax (`- KEY=value`) by default |
| YAML-sensitive values | Quote values that YAML reads as booleans, numbers, or null: `"true"`, `"123"`, `"null"` | Leave them unquoted and let the parser guess |

## Dockerfiles

### Base images

Use specific version tags. Avoid `latest` in production Dockerfiles, because the same Dockerfile can build a different image tomorrow.

Good:

```dockerfile
FROM python:3.12-slim
```

Bad:

```dockerfile
FROM python:latest
```

### Multi-stage builds

Use multi-stage builds to keep final images small and avoid shipping build dependencies.

Good:

```dockerfile
FROM node:24-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --omit=dev

FROM node:24-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package*.json ./
USER node
CMD ["node", "dist/index.js"]
```

### Running as non-root

Run containers as a non-root user. Do not run production containers as root, including images that are only used internally: internal images still need reproducibility and least privilege.

Good:

```dockerfile
FROM python:3.12-slim
RUN useradd -m appuser
USER appuser
```

Bad: there is no `USER` instruction, so the container runs as root, and the base image is not pinned.

```dockerfile
FROM python:latest
# No USER instruction: the container runs as root
```

## Docker Compose files

Follow the current Compose Specification and use readable mapping syntax where practical.

### Rules

1. Do not include the top-level `version` property. It is obsolete in modern Docker Compose.
2. Use mapping syntax for environment variables and labels: `KEY: value`.
3. Avoid list syntax for environment variables and labels unless explicitly requested or required by a named tool, platform, parser, passthrough, or legacy integration. Team habit, personal familiarity, and old examples are not compatibility requirements.
4. Quote environment values that YAML may interpret as booleans, numbers, or null, such as `"true"`, `"false"`, `"123"`, or `"null"`.

### Examples

Good: environment variables and labels use mapping syntax.

```yaml
services:
  app:
    environment:
      DATABASE_URL: postgres://localhost/db
      DEBUG: "true"
      RETRY_COUNT: "3"
    labels:
      com.example.description: "My application"
      com.example.version: "1.0"
```

Bad defaults: obsolete `version` and list syntax without an explicit request or compatibility reason. In this list form, entire `KEY=value` entries are strings; the YAML coercion warning applies to mapping values, not to the `true` or `3` substrings below.

```yaml
version: "3.9"

services:
  app:
    environment:
      - "DATABASE_URL=postgres://localhost/db"
      - DEBUG=true
      - RETRY_COUNT=3
    labels:
      - "com.example.description=My application"
      - "com.example.version=1.0"
```

Bad mapping values: these are parsed as a boolean and a number rather than strings.

```yaml
environment:
  DEBUG: true
  RETRY_COUNT: 3
```

If a user explicitly asks for classic syntax (`version`, env lists), explain that the current Compose Specification does not need it and note the trade-off, but honor that specific request within its scope. Do not invent a compatibility need to justify it or silently override the request. Without an explicit request or concrete compatibility constraint, use the modern form.

## Common Mistakes

- Adding a new Dockerfile with a `latest` tag, or an unpinned base image.
- Running the final image as root because the app "just works" that way.
- Treating an internal-only image as exempt from pinned tags and non-root users.
- Leaving build dependencies, compilers, or dev packages in the final stage instead of using a multi-stage build.
- Preserving obsolete Compose syntax (`version: "3.9"`, `KEY=value` lists) because it appears in old examples.
- Treating familiarity with old Compose syntax as a compatibility requirement. "Legacy reason" means a concrete tool or platform constraint.
- Leaving values like `true`, `3`, or `null` unquoted in Compose `environment`, so YAML converts them to non-strings.

## Red Flags

Stop and use the compliant form if you think:

- "Use Docker `latest` or root for now and harden it later."
- "The Dockerfile is only internal, so `latest` and root are fine."
- "Copy the old Compose `version: \"3.9\"` style because it still works."
- "The user did not ask for classic Compose syntax, but the old example uses it."

| Rationalization | Response |
| --- | --- |
| "The Dockerfile is only internal, so `latest` and root are fine." | Internal images still need reproducibility and least privilege. Use specific tags and non-root users. |
| "The old example uses classic Compose syntax, so I kept `version` and env lists." | Use the current Compose Specification by default. A specific task instruction may override that default; personal habit is not a compatibility requirement. |
| "The legacy syntax still works, so it is fine." | Working code is not the same as current convention. Use modern practice unless a real constraint requires otherwise. |

---
name: architect-next-prisma-bun-vector
description: Use when scaffolding full-stack Next.js with Bun, Prisma, Postgres pgvector, Docker, and CI defaults.
---

# Architect: Next + Prisma + Bun + pgvector

Use this skill when the user wants a production scaffold for a Next.js app that includes Prisma, vector search support, Dockerized services, and CI quality gates.
Docker is required by default for this runnable base architect skill. Only allow `NO_DOCKER=yes` when the user explicitly asks for a local-only exception.

## Inputs

Collect these values first:
- `PROJECT_NAME`: kebab-case folder/package name.
- `VECTOR_DIM`: embedding dimension, default `1536`.
- `DATABASE_URL`: app connection URL.
- `DIRECT_URL`: direct connection URL for migrations.
- `NO_DOCKER`: default `no`. Set `yes` only when user explicitly opts out.

Use these version pins unless the user requests different versions:
- `create-next-app@15`
- `postgres:16-alpine`
- `pgvector` git tag `v0.8.1`
- `oven/bun` image tag `1.1.38-alpine`

## Preflight Checks

Run before scaffolding:
```bash
command -v bun >/dev/null && bun --version || echo "bun-missing"
command -v docker >/dev/null && docker --version || echo "docker-missing"
```

Execution modes:
- `production-default`: generate and validate containerized app + db stack (`NO_DOCKER=no`).
- `local-no-docker`: only allowed when user explicitly sets `NO_DOCKER=yes`.
- `offline-smoke`: tools/network constrained; scaffold and report verification limits.

Production-default contract:
- Must create `db.Dockerfile`, `Dockerfile`, `.dockerignore`, and `docker-compose.yml`.
- Must include CI image build check.
- Must run containerized validation.

## Scaffold Workflow

1. Initialize app:
```bash
bunx --bun create-next-app@15 {{PROJECT_NAME}} --typescript --tailwind --eslint --src-dir --app --use-bun --import-alias "@/*"
cd {{PROJECT_NAME}}
```

2. Install stack dependencies:
```bash
bun add @prisma/client pg zod
bun add -d prisma vitest @vitest/coverage-v8 jsdom @types/node eslint-plugin-jsdoc
```

3. Initialize Prisma:
```bash
bunx prisma init --datasource-provider postgresql
```

4. Create infrastructure and quality files (`NO_DOCKER=no`):
- `db.Dockerfile`
- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- `vitest.config.ts`
- `eslint.config.mjs` (extend generated Next config with JSDoc rules for exported symbols)
- `.github/workflows/ci.yml`
- `src/lib/prisma.ts`
- `src/services/vector-service.ts`
If `NO_DOCKER=yes`, explicitly document this exception and skip container checks.

5. Create first migration that enables pgvector and creates vector-indexed tables.

## Required File Templates

### `db.Dockerfile`
```dockerfile
FROM postgres:16-alpine

ARG PGVECTOR_REF=v0.8.1

RUN apk add --no-cache --virtual .build-deps git build-base postgresql-dev \
    && git clone --branch "$PGVECTOR_REF" https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector \
    && make \
    && make install \
    && rm -rf /tmp/pgvector \
    && apk del .build-deps
```

### `Dockerfile` (app)
```dockerfile
FROM oven/bun:1.1.38-alpine AS deps
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

FROM oven/bun:1.1.38-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN bunx prisma generate && bun run build

FROM oven/bun:1.1.38-alpine AS prod-deps
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile --production

FROM oven/bun:1.1.38-alpine AS run
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=build /app/package.json ./package.json
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=build /app/prisma ./prisma
USER bun
EXPOSE 3000
CMD ["bun", "run", "start"]
```

### `.dockerignore`
```gitignore
.git
node_modules
.next
coverage
*.log
```

### `docker-compose.yml`
```yaml
services:
  db:
    build:
      context: .
      dockerfile: db.Dockerfile
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 5s
      timeout: 5s
      retries: 20
    volumes:
      - pg_data:/var/lib/postgresql/data

  web:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://app:app@db:5432/app?schema=public
      DIRECT_URL: postgresql://app:app@db:5432/app?schema=public
      PORT: "3000"
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "3000:3000"

volumes:
  pg_data:
```
Keep `ports: - "3000:3000"` on the `web` service. If documenting direct `docker run` usage for the app image, include `-p 3000:3000` and the required database env wiring; `docker compose` remains the default local path because it provides both.

### `vitest.config.ts`
```typescript
import path from "node:path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov", "html"],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

### `eslint.config.mjs` (extend generated config)
```javascript
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { FlatCompat } from "@eslint/eslintrc";
import jsdoc from "eslint-plugin-jsdoc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    files: ["src/**/*.{ts,tsx}"],
    plugins: { jsdoc },
    rules: {
      "jsdoc/require-jsdoc": [
        "error",
        {
          contexts: [
            "ExportNamedDeclaration > FunctionDeclaration",
            "ExportDefaultDeclaration > FunctionDeclaration",
            "ExportNamedDeclaration > ClassDeclaration",
            "ExportNamedDeclaration > VariableDeclaration > VariableDeclarator[init.type='ArrowFunctionExpression']",
          ],
        },
      ],
      "jsdoc/require-description": "error",
      "jsdoc/require-param": "off",
      "jsdoc/require-returns": "off",
    },
  },
];

export default eslintConfig;
```

### `.github/workflows/ci.yml`
```yaml
name: ci
on:
  push:
  pull_request:

jobs:
  lint-test-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: "1.1.38"
      - name: Install
        run: bun install --frozen-lockfile
      - name: Prisma generate
        run: bunx prisma generate
      - name: Lint
        run: bun run lint
      - name: Lint Docs
        run: bunx eslint "src/**/*.{ts,tsx}" --max-warnings=0
      - name: Test
        run: bunx vitest run --coverage
      - name: Build
        run: bun run build
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: {{PROJECT_NAME}}:ci
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Prisma client singleton (`src/lib/prisma.ts`)
```typescript
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query", "error", "warn"] : ["error"],
  });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

### Vector query service (`src/services/vector-service.ts`)
```typescript
import { Prisma } from "@prisma/client";
import { prisma } from "@/lib/prisma";

export async function searchEmbeddings(queryEmbedding: number[], limit = 10) {
  return prisma.$queryRaw<
    { id: bigint; content: string; distance: number }[]
  >(Prisma.sql`
    SELECT id, content, embedding <=> ${queryEmbedding}::vector AS distance
    FROM document_embeddings
    ORDER BY embedding <=> ${queryEmbedding}::vector
    LIMIT ${limit}
  `);
}
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Never use `@latest` for scaffold or runtime-critical dependencies unless user asks for latest.
- Do not interpolate raw SQL strings; use `Prisma.sql` parameterization.
- Keep Prisma migration path reproducible: schema checked in, migrations checked in.
- Ensure app container runs as non-root (`USER bun`).
- Use `docker compose` commands in docs and scripts.
- Treat `NO_DOCKER=yes` as explicit exception behavior.
- Ensure `bun.lockb` is committed before Docker build; the Dockerfile copies it explicitly for deterministic `--frozen-lockfile` installs.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


Run and fix failures before finishing:
```bash
bun run lint
bunx eslint "src/**/*.{ts,tsx}" --max-warnings=0
bunx vitest run --coverage
bunx prisma validate
bun run build
test -f bun.lockb
docker build -t {{PROJECT_NAME}}:local .
docker compose up -d --build
docker compose ps
```
`local-no-docker` (`NO_DOCKER=yes`):
```bash
bun run lint
bunx eslint "src/**/*.{ts,tsx}" --max-warnings=0
bunx vitest run --coverage
bunx prisma validate
bun run build
```
Fallback (`offline-smoke`):
```bash
test -f Dockerfile || echo "docker-artifacts-missing-in-offline-smoke"
test -f db.Dockerfile || echo "db-dockerfile-missing-in-offline-smoke"
```

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.

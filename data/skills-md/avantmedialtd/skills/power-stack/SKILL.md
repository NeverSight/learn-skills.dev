---
name: power-stack
description: Bun/Elysia/React/MUI monorepo stack blueprint. Use when scaffolding a new project, adding a new app or package to the monorepo, choosing dependencies, or making architectural decisions. Contains the full tech stack, conventions, and wiring patterns.
---

# Power Stack

A self-contained blueprint for reconstructing this monorepo stack from scratch.

---

## 1. Monorepo Layout

Bun workspaces. Root `package.json` declares `"workspaces": ["apps/*", "packages/*"]`.

```
├── apps/
│   ├── api/            # REST backend (Bun + Elysia)
│   └── web/            # SPA frontend (React + Vite)
├── packages/
│   └── shared/         # Shared types, validators, permission utils
├── e2e/                # Playwright E2E test suite
├── openspec/           # Spec-driven change management
├── docker-compose.yml  # PostgreSQL + app + test containers
├── tsconfig.json       # Project references root
└── vitest.config.ts    # Multi-project test config
```

TypeScript project references: root `tsconfig.json` uses `"files": []` + `"references"` to delegate to each workspace. Each workspace tsconfig has `"composite": true`. Type-check with `tsc --build --noEmit`.

---

## 2. Runtime & Language

- **Bun** 1.x as runtime and package manager (`bun install`, `bun run`)
- **TypeScript** 5.9 with strict mode, ESM everywhere (`"type": "module"`)
- Target: ES2022, module resolution: `bundler`
- `experimentalDecorators` + `emitDecoratorMetadata` enabled for TypeORM

---

## 3. Environment Variables

Managed via `.env` at the project root (with `.env.example` checked in). Backend reads via `process.env`, frontend via Vite's `VITE_` prefix.

| Variable              | Used by  | Purpose                         | Default              |
| --------------------- | -------- | ------------------------------- | -------------------- |
| `POSTGRES_HOST`       | API      | Database host                   | `localhost`          |
| `POSTGRES_PORT`       | API      | Database port                   | `16002`              |
| `POSTGRES_USER`       | API      | Database user                   | `postgres`           |
| `POSTGRES_PASSWORD`   | API      | Database password               | `postgres`           |
| `POSTGRES_DB`         | API      | Database name                   | `avant_id`           |
| `API_PORT`            | API      | HTTP listen port                | `16000`              |
| `JWT_SECRET`          | API      | Signing key for JWTs            | dev fallback         |
| `WEB_URL`             | API      | Frontend origin (CORS/redirects)| `http://localhost:16001` |
| `NODE_ENV`            | API      | Environment mode                | `development`        |
| `VITE_API_URL`        | Web      | API base URL for frontend       | `http://localhost:16000` |

---

## 4. Backend (`apps/api`)

### Framework

**Elysia** 1.4 — lightweight Bun-native HTTP framework. Entry point imports `reflect-metadata` first, initializes TypeORM `DataSource`, then calls `app.listen(port)`.

App composition via `.use()` plugin pattern:

```typescript
new Elysia()
    .use(cors())
    .get('/health', () => ({ status: 'ok' }))
    .use(authRoutes)
    .use(adminRoutes);
```

Route groups use `new Elysia({ prefix: '/auth' })` with request body validation via Elysia's `t.Object()` schema.

### Error Handling

Use `set.status` pattern, not `error()`:

```typescript
async ({ body, set }) => {
    set.status = 400;
    return { error: 'Bad Request', message: 'Details' };
};
```

### Auth Middleware

Elysia `.derive()` extracts Bearer token from `Authorization` header, verifies JWT via `jose`, and injects `{ user, auth }` into context. `.macro()` defines `requireAuth`, `requireAdmin`, and `requireAppPermission` guards that check permissions and return 401/403.

### Database

- **PostgreSQL** 17 via **TypeORM** 0.3 with `DataSource` config
- Connection from env vars: `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `synchronize: false` always, schema changes via migrations only (`packages/db/src/db/migrations/*.ts`)
- Run migrations: `bun run migrate` (calls `packages/db/src/db/migrate.ts`)
- Generate migrations: `bun run generate-migration` (uses TypeORM CLI against `packages/db/src/data-source.ts`)

`packages/db/src/db/migrate.ts`:

```typescript
import 'reflect-metadata';
import { AppDataSource } from './data-source';

async function runMigrations() {
    try {
        await AppDataSource.initialize();
        console.log('Running migrations...');
        await AppDataSource.runMigrations();
        console.log('Migrations completed successfully');
        await AppDataSource.destroy();
    } catch (error) {
        console.error('Migration failed:', error);
        process.exit(1);
    }
}

runMigrations();
```
- Entities: User (and domain-specific entities as needed)

### Entity Conventions

- UUID primary keys (`@PrimaryGeneratedColumn('uuid')`)
- Explicit column types always (`@Column({ type: 'text' })`, `@Column({ type: 'boolean' })`)
- `@CreateDateColumn({ type: 'timestamptz' })` / `@UpdateDateColumn`
- String-based relations to avoid circular imports: `@OneToMany('UserPermission', 'user')`
- Wrap relation types in `Relation<T>` from TypeORM

### Auth Flow

- **Password hashing**: Argon2 via `@node-rs/argon2`
- **JWT**: `jose` library. Access tokens (short-lived) + refresh tokens (rotated, family-tracked for reuse detection). Revocation on reuse.

### Route Groups

| Prefix   | Purpose                                                                  |
| -------- | ------------------------------------------------------------------------ |
| `/auth`  | Register, login, logout, refresh, me, password reset, email verification |
| `/admin` | User management, app management (requires admin permission)              |

---

## 5. Frontend (`apps/web`)

### Stack

- **React** 19 with `react-dom/client` (`createRoot`)
- **MUI** 7 + **Emotion** for styling
- **React Router** 7 (`react-router-dom`) with `BrowserRouter`
- **Vite** 7 as dev server and bundler (`@vitejs/plugin-react`)

### App Structure

```
src/
├── main.tsx              # Entry: StrictMode > ThemeModeProvider > BrowserRouter > AuthProvider > App
├── App.tsx               # Route definitions
├── theme.ts              # MUI createTheme (dark-only, neon brutalist)
├── api/
│   ├── authFetch.ts      # Fetch wrapper with auto token refresh
│   └── admin.ts          # Admin API calls
├── context/
│   ├── AuthContext.tsx    # Auth state (login, register, logout, permissions)
│   └── ThemeContext.tsx   # Theme mode provider
├── pages/                # Route pages (Login, Register, Dashboard, admin/*)
└── components/           # Shared components (AdminRoute, Logo, etc.)
```

### Auth Client Pattern

`AuthContext` stores JWT tokens in `localStorage` (`accessToken`, `refreshToken`, `tokenExpiresAt`). `authFetch` wraps `fetch()` to:

1. Proactively refresh if token expires within 60s
2. Add `Authorization: Bearer` header
3. Retry once on 401 after refresh
4. Dispatch `auth:logout` custom event on unrecoverable failure

Proactive refresh timer runs every 13 minutes. Visibility change handler refreshes on tab focus if token is near expiry.

### Theme

Dark-only neon brutalist design: `borderRadius: 0` everywhere, heavy borders (2-4px), box shadows offset to bottom-right (`4px 4px 0 #000`), hover transforms (`translate(-2px, -2px)`), uppercase headings/buttons with tight letter-spacing. Palette: deep navy backgrounds (`#0f0f23`, `#1a1a2e`), indigo primary (`#6366f1`), amber secondary (`#f59e0b`), neon green success (`#00ff88`), hot pink error (`#ff3366`).

### Production

Vite builds static files. Served by **nginx:alpine** with a custom `nginx.conf`.

---

## 6. Shared Package (`packages/shared`)

Pure TypeScript, no runtime dependencies. Exports via subpath: `.` (root), `./types`, `./utils`. Contains shared types, interfaces, and utility functions used by both backend and frontend. Built with `tsc` to `dist/`.

---

## 7. Testing

### Unit Tests

**Vitest** 4, configured as multi-project workspace in root `vitest.config.ts`. Three projects: `shared`, `api`, `web`. Each runs `src/**/*.test.ts` files. Run with `bun run test`.

### E2E Tests

**Playwright** 1.58 in a dedicated `e2e/` package. Three categories:

- `*Api.spec.ts` — API-only (no browser)
- `*.spec.ts` — UI tests (Chromium + mobile viewports)
- `visual-*.spec.ts` — Visual regression (baselines in `e2e/tests/visual-baselines/`)

Runs in Docker Compose with `--profile testing`: spins up PostgreSQL, API, web (nginx), runs migrations, then executes Playwright.

---

## 8. Docker

### API Container

Multi-stage `oven/bun:1` image:

1. `deps` — install workspace dependencies
2. `build` — copy source, build shared package
3. `runner` — copy built artifacts, run `bun run src/index.ts` directly (no compile step for API)

### Web Container

Multi-stage build, final stage is `nginx:alpine` serving the Vite output from `/usr/share/nginx/html`.

### Compose Services

| Service        | Image/Build         | Purpose                 | Profile       |
| -------------- | ------------------- | ----------------------- | ------------- |
| `postgres`     | postgres:17-alpine  | Database                | (default)     |
| `api`          | apps/api/Dockerfile | REST backend            | apps, testing |
| `web`          | apps/web/Dockerfile | Static frontend (nginx) | apps, testing |
| `migrate-seed` | (same as api)       | Run migrations once     | testing       |
| `e2e`          | e2e/Dockerfile      | Playwright test runner  | testing       |

Health checks on all services. E2E waits for postgres + api + web to be healthy before running.

---

## 9. CI/CD

**Jenkins** pipeline (Groovy `Jenkinsfile`):

1. **Checkout** — clean workspace, full clone
2. **Install** — `bun install` per workspace
3. **Unit test** — `bun run test`
4. **E2E** — Docker Compose up with testing profile, run Playwright, publish HTML report
5. **Deploy** — SSH to production server, `git pull && docker compose --profile apps up -d --build`

---

## 10. Code Quality

| Tool            | Config                  | Purpose                |
| --------------- | ----------------------- | ---------------------- |
| **oxlint**      | `oxlint .`              | Fast Rust-based linter |
| **Prettier**    | `prettier --write .`    | Code formatting        |
| **tsc --build** | Project references mode | Type checking          |

---

## 11. OpenSpec

Spec-driven change management. Initialize with `bunx openspec init`. Structure:

```
openspec/
├── config.yaml    # Schema and project context
├── specs/         # Living specifications (one dir per feature)
└── changes/       # Change proposals and artifacts
    └── archive/   # Completed changes
```

Each feature has a `spec.md` describing its current state. Changes go through a structured workflow: proposal → artifacts (tasks, delta specs) → implementation → verification → archive. Specs are updated as changes land.

---

## 12. Key Dependencies Summary

### Backend

| Package          | Purpose                   |
| ---------------- | ------------------------- |
| elysia           | HTTP framework            |
| @elysiajs/cors   | CORS middleware           |
| typeorm          | ORM (PostgreSQL)          |
| pg               | PostgreSQL driver         |
| jose             | JWT signing/verification  |
| @node-rs/argon2  | Password hashing          |
| reflect-metadata | TypeORM decorator support |

### Frontend

| Package             | Purpose                  |
| ------------------- | ------------------------ |
| react / react-dom   | UI library               |
| @mui/material       | Component library        |
| @emotion/react      | CSS-in-JS (MUI peer dep) |
| @emotion/styled     | Styled components        |
| @mui/icons-material | Icon set                 |
| react-router-dom    | Client routing           |
| vite                | Dev server + bundler     |

### Dev Tooling

| Package            | Purpose                         |
| ------------------ | ------------------------------- |
| typescript         | Type checking                   |
| vitest             | Unit test framework             |
| @playwright/test   | E2E test framework              |
| oxlint             | Linting                         |
| prettier           | Formatting                      |
| bun run --parallel | Parallel dev scripts (built-in) |

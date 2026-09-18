---
name: nodejs-scaffolding
description: Scaffold or extend production-minded TypeScript Express projects with a fixed src architecture, shared error handling, security headers, rate limiting, console logging, graceful shutdown, optional Passport JWT cookie authentication, and opt-in MongoDB setup. Use when creating a Node.js API, adding authentication to one, or configuring MongoDB for it.
---

# Node.js Scaffolding

Build a compact TypeScript Express API whose structure and code are readable and understandable to the person using or maintaining it. Preserve existing project choices and files; do not replace a working structure unless the user explicitly asks for a rewrite.

## Choose the requested mode

- **Base scaffold**: create the TypeScript Express foundation. Do not add a database connection.
- **Authentication**: extend the base with Passport JWT authentication stored in an HTTP-only cookie.
- **MongoDB**: add Mongoose only when the user explicitly asks to configure MongoDB.

If the request combines modes, apply them in that order.

## Base scaffold

### 1. Create the complete source tree first

Create every directory before installing packages or writing implementation files:

```text
src/
├── config/
├── controllers/
├── middlewares/
├── models/
├── routes/
│   └── v1/
├── services/
├── types/
├── utils/
└── validators/
```

Keep empty directories during scaffolding when they communicate the intended architecture. Use this flow for later features:

```text
route -> controller -> service -> model
```

### 2. Install current packages through npm

Initialize `package.json` when it does not exist, then use `npm install` commands. Never invent or hardcode package versions directly in `package.json`.

For the base scaffold, install the runtime and TypeScript packages the implementation actually uses. A typical Express base needs:

```bash
npm install express cors cookie-parser dotenv zod bcryptjs helmet express-rate-limit winston
npm install --save-dev typescript ts-node nodemon tsup @types/node @types/express @types/cors @types/cookie-parser
```

Do not install Mongoose, Passport, JWT, sessions, or unused libraries in the base mode.

### 3. Create the foundation files

Create:

```text
src/config/env.config.ts
src/config/http-status.config.ts
src/middlewares/asyncHandler.middleware.ts
src/middlewares/errorHandler.middleware.ts
src/middlewares/rateLimiter.middleware.ts
src/routes/v1/index.ts
src/utils/app-error.ts
src/utils/bcrypt.ts
src/utils/get-env.ts
src/utils/logger.ts
src/index.ts
.gitignore
nodemon.json
tsconfig.json
tsup.config.ts
```

The base `env.config.ts` should expose `NODE_ENV`, `PORT`, and `LOG_LEVEL`, using `getEnv` with sensible defaults. Do not include `MONGO_URI`, `database.config.ts`, or `connectDatabase` in `index.ts` until MongoDB is explicitly requested.

Configure `index.ts` with Helmet, Express JSON and URL-encoded parsing, cookies, CORS when an origin is configured, rate limiting for API routes, a `GET /health` route, and `errorHandler` last. Keep the health response small and deterministic. Do not rate-limit the health endpoint used by the hosting platform.

Put feature routers in `src/routes/v1` and combine them in `src/routes/v1/index.ts`. Mount the combined router at `/api/v1`; controllers and services must not repeat that prefix. Keep infrastructure endpoints such as `/health` outside API versioning.

Read [references/security-logging-shutdown.md](references/security-logging-shutdown.md) when building the base scaffold. Use one Winston console transport: readable colored lines in development, structured JSON in production, and silent output in tests. Do not add Logtail, files, or another logging transport unless the user requests a logging service.

Store the result of `app.listen()` and register graceful shutdown with exactly this signal list:

```ts
const shutdownSignals: NodeJS.Signals[] = ["SIGTERM", "SIGINT"];
```

Stop accepting requests, close the HTTP server, then close any configured database connection. Log startup, shutdown, and unexpected failures without logging secrets, cookies, authorization headers, passwords, tokens, or raw request bodies.

Use `asyncHandler.middleware.ts` to forward rejected controller promises to Express error middleware. Keep both `asyncHandler` and `errorHandler` in `src/middlewares`, not `src/utils`.

### 4. Add the CommonJS development and production build

Default new Express scaffolds to CommonJS unless the project already uses ESM or the user requests it. This keeps extensionless local imports, `__dirname`, and broad package compatibility while tsup produces a clean production bundle.

Use `tsconfig.json` for strict type-checking only; tsup owns JavaScript output:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "noEmit": true,
    "types": ["node"]
  },
  "include": ["src", "src/types/**/*.d.ts"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

Set `"type": "commonjs"` and `"main": "dist/index.js"` in `package.json`. Add these scripts without deleting unrelated scripts:

```json
{
  "scripts": {
    "dev": "nodemon",
    "typecheck": "tsc --noEmit",
    "build": "npm run typecheck && tsup",
    "start": "node dist/index.js"
  }
}
```

Use `nodemon.json` for development:

```json
{
  "watch": ["src"],
  "ignore": ["dist", "node_modules"],
  "ext": "ts,json",
  "exec": "ts-node --transpile-only ./src/index.ts"
}
```

Use `tsup.config.ts` for production:

```ts
import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["cjs"],
  platform: "node",
  target: "node20",
  outDir: "dist",
  bundle: true,
  clean: true,
  skipNodeModulesBundle: true,
  sourcemap: true,
  minify: false,
  splitting: false,
});
```

Match `target` to the deployment runtime when it differs. Do not generate declarations for a private API application or produce both CJS and ESM unless the project is a published library that needs them.

Dependencies remain external by default. If an ESM-only dependency causes `ERR_REQUIRE_ESM`, prefer its supported CommonJS entry or dynamic `import()` when appropriate. Otherwise, selectively bundle that dependency with tsup's `noExternal` option and verify it at runtime; do not bundle every dependency to hide one incompatibility.

Copy `package.json` into `dist` only when deployment treats `dist` as a standalone artifact. Otherwise deploy from the project root with production dependencies and run `node dist/index.js`.

## Error contract

In `app-error.ts`, define:

```ts
export const ErrorCodes = {
  ERR_INTERNAL: "ERR_INTERNAL",
  ERR_BAD_REQUEST: "ERR_BAD_REQUEST",
  ERR_UNAUTHORIZED: "ERR_UNAUTHORIZED",
  ERR_FORBIDDEN: "ERR_FORBIDDEN",
  ERR_NOT_FOUND: "ERR_NOT_FOUND",
  ERR_VALIDATION: "ERR_VALIDATION",
  ERR_TOO_MANY_REQUESTS: "ERR_TOO_MANY_REQUESTS",
} as const;
```

Also define `ErrorCodeType`, the `AppError` base class, and these subclasses:

- `InternalServerException`
- `NotFoundException`
- `BadRequestException`
- `UnauthorizedException`
- `ForbiddenException`

The error middleware must handle `ZodError` before `AppError`. Add a `formatZodError` helper that maps issues to readable `{ field, message }` objects and return `ErrorCodes.ERR_VALIDATION`. Do not leak stack traces or raw internal errors in production responses.

## Authentication mode

Use stateless JWT authentication with `passport-jwt` and `jsonwebtoken`. Do not use `passport-local` or `express-session`.

Install current packages through npm:

```bash
npm install passport passport-jwt jsonwebtoken
npm install --save-dev @types/passport @types/passport-jwt @types/jsonwebtoken
```

Add:

```text
src/config/passport.config.ts
src/controllers/auth.controller.ts
src/models/user.model.ts
src/routes/v1/auth.route.ts
src/services/auth.service.ts
src/services/user.service.ts
src/utils/cookie.ts
src/validators/auth.validator.ts
```

Add `JWT_SECRET` and `JWT_EXPIRES_IN` to `env.config.ts`. The Passport strategy must use `ExtractJwt.fromExtractors` and read the token from `req.cookies.accessToken`:

```ts
const cookieExtractor = (req: Request) => req?.cookies?.accessToken ?? null;
```

Use `session: false`, initialize Passport in `index.ts`, mount the auth router from `src/routes/v1/index.ts`, and protect the auth-status endpoint with the JWT middleware.

`cookie.ts` must expose `setJwtAuthCookie` and `clearJwtAuthCookie`. The cookie should be HTTP-only, secure in production, and use an intentional `sameSite` policy. Clear it with the same path and relevant options used when setting it.

Implement register, login, logout, and auth-status endpoints. Validate registration and login input with Zod. Hash passwords through the model or service exactly once, never return a password field, and use a non-enumerating invalid-credentials message for login failures.

## MongoDB mode

Only when the user explicitly asks to configure MongoDB:

1. Run `npm install mongoose`.
2. Create `src/config/database.config.ts`.
3. Add `MONGO_URI` to `env.config.ts` and `.env.example` if that file exists.
4. Connect from the server startup path before reporting that the API is ready.
5. Keep connection errors visible and terminate startup cleanly when the initial connection fails.
6. Enable Mongoose `sanitizeFilter` before accepting queries, validate request input with Zod, and construct filters/updates from allowed fields. Never pass `req.body` or `req.query` directly to Mongoose.

If authentication is requested without a database choice, do not silently choose MongoDB. Ask for or adapt to the project's existing persistence layer.

## Verification

After writing files:

1. Run the project's TypeScript check or build.
2. Start the real development server with `npm run dev`.
3. Wait for its ready output, call the health endpoint, and confirm the expected response.
4. Stop the verification process cleanly unless the user asked to keep it running.

Do not report the scaffold as complete based only on `tsc --noEmit`; the server must start successfully.

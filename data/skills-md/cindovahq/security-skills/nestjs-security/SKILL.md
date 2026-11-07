---
name: nestjs-security
description: Security review and secure-coding guidance for NestJS 10.x, 11.x and 12.x applications on the Express or Fastify adapter. Use when auditing, reviewing, pentest-prepping or hardening a NestJS backend or API, or when writing or changing its controllers, guards, pipes, DTOs, modules, authentication, JWT handling, GraphQL resolvers, WebSocket gateways, microservice handlers, uploads or main.ts configuration. Triggers on projects whose package.json depends on @nestjs/core or @nestjs/common, or that contain nest-cli.json, main.ts with NestFactory.create, or *.module.ts and *.controller.ts files. Covers guard and middleware ordering, @Public fail-open patterns, ValidationPipe whitelist and mass assignment, class-transformer data exposure, Passport and JWT, IDOR and CASL, throttler, CORS, CSRF, helmet, GraphQL field authorization and introspection, gateway and TCP transport authentication, ORM injection, multer and FileTypeValidator, SSRF, Swagger exposure, NestJS advisories, and supertest verification.
license: Apache-2.0
metadata:
  author: Cindova Technologies
  homepage: https://github.com/cindovahq/security-skills
  version: "1.0.0"
  status: beta
  framework-versions: "NestJS 10.x, 11.x and 12.x (12.1 current); Express 4/5 and Fastify 4/5 adapters (Nest 10 uses 4); @nestjs/graphql 12 (Nest 10), 13 (Nest 11) and 14 (Nest 12)"
  last-verified: "2026-10-02"
---

# NestJS Security

Find, explain, fix and verify security issues in NestJS applications, and write new Nest code that does not introduce them.

All paths in this skill (`references/...`) are relative to the directory containing this `SKILL.md`.

## Modes

- **Review mode**: the user asks for an audit, security review, pentest prep, or "is this secure?". Follow the workflow below and produce findings.
- **Build mode**: you are writing or modifying Nest code. Apply the [build-mode guardrails](#build-mode-guardrails) to every change and load only the reference for the area you're touching.

NestJS sits on Express or Fastify. For generic Node topics (prototype pollution, SSRF allow-lists, SQL/NoSQL injection basics, sessions, ReDoS, npm supply chain, Node EOL status) use the `nodejs-security` skill; this skill is self-contained for everything Nest-specific. If the `appsec-review` skill is installed, it owns the overall methodology and report format; otherwise use the [evidence and reporting rules](#evidence-and-reporting-rules) below.

## Review workflow

### 1. Confirm the stack and versions

1. Read `package.json` and the **lockfile** for `@nestjs/*` versions, the adapter (`@nestjs/platform-express` or `@nestjs/platform-fastify`), `@nestjs/jwt`, `@nestjs/passport`, `@nestjs/throttler`, `@nestjs/graphql` and `@nestjs/apollo`, `@nestjs/websockets`, `@nestjs/microservices`, `@nestjs/swagger`, the ORM, `class-validator`, `class-transformer`, `multer`, `helmet`.
2. On 2026-10-02 the lines are **12.x** (12.0.0 on 2026-08-27, 12.1.2 latest), **11.x** (11.2.7) and **10.x** (last release 10.4.22 on 2026-01-10; late-2026 advisories list it as unpatched). Check the installed version against `references/dependencies.md`: several 2026 advisories are authentication bypasses on the Fastify adapter, and multer DoS fixes arrive with `@nestjs/platform-express` 11.2.6 and 12.0.3.
3. Find `main.ts`. Everything global happens there: `useGlobalPipes`, `useGlobalGuards`, `enableCors`, `helmet`/`useSecurityHeaders`, `enableCsrfProtection`, Swagger, `rawBody`, hybrid `connectMicroservice`. Then `app.module.ts` for `APP_GUARD`, `APP_PIPE`, `APP_INTERCEPTOR`, `APP_FILTER`, `ThrottlerModule`, `ConfigModule`, `GraphQLModule`, `TypeOrmModule`.

### 2. Map the attack surface

- List controllers, resolvers, gateways and `@MessagePattern`/`@EventPattern` handlers. For each, write down the effective guards (global, controller, route), pipes and interceptors that actually run (see `references/request-pipeline.md`).
- Note what global enhancers do **not** reach: hybrid microservices, GraphQL field resolvers, gateway `handleConnection()`, Swagger and static files.
- Flag every `@Public()`, every route that takes an ID, URL, filename, sort field or whole body, and every `@Body()` typed `any`, an interface or an array.

### 3. Review each area

Load the reference for each area as you reach it. Don't load all of them up front.

| Area | Reference | Start by looking for |
|---|---|---|
| Pipeline, guards, adapters | `references/request-pipeline.md` | Unbound `RolesGuard`, `handleRequest` returning `user`, `getAllAndMerge`, path-scoped middleware auth, Fastify adapter version, `inheritAppConfig` |
| Authentication, JWT | `references/authentication.md` | `?? 'secret'` fallbacks, `ignoreExpiration`, `decode`, missing `algorithms`/`expiresIn`, `@Public()` logic, unsalted hashes, cookie flags |
| Authorization, IDOR | `references/authorization.md` | `@Roles` without guard, `findOneBy({ id })` without owner, `PATCH :id` without caller check, singleton fields holding the user, CASL checks by type |
| Validation, mass assignment | `references/validation-mass-assignment.md` | `new ValidationPipe()` without `whitelist`, `@Body() any`, `PartialType(CreateDto)` with `role`, missing `@Type`, array bodies |
| Response exposure | `references/serialization-data-exposure.md` | `@Exclude` without `ClassSerializerInterceptor`, entities returned directly, `@Res()` |
| Injection | `references/injection.md` | `query(\`...${}\`)`, QueryBuilder template strings, `undefined` filters, Mongo operators, `$queryRawUnsafe` |
| CORS, CSRF, headers, proxy | `references/cors-csrf-headers.md` | `origin: true` + `credentials`, cookie auth without CSRF defense, missing helmet/`useSecurityHeaders`, `trust proxy` |
| Rate limiting, DoS | `references/rate-limiting-dos.md` | `ThrottlerModule` without `ThrottlerGuard`, `@SkipThrottle`, multer without `limits`, body limits |
| GraphQL | `references/graphql.md` | Field resolver guards without `fieldResolverEnhancers`, introspection, no depth/complexity limit, `GqlExecutionContext` |
| WebSockets, microservices | `references/websockets-microservices.md` | Empty `handleConnection`, client-supplied `userId`, rooms by input, TCP `host: '0.0.0.0'`, unguarded `@MessagePattern` |
| Uploads, downloads, static | `references/file-uploads.md` | `FileInterceptor` without `limits`, `originalname` as path, `fallbackToMimetype`, `createReadStream(join(dir, param))`, public upload dirs |
| SSRF, redirects | `references/ssrf-redirects.md` | `HttpService.get(dto.url)`, `@IsUrl()` as the only control, `@Redirect` with input |
| Secrets, Swagger, errors | `references/secrets-config.md` | `SwaggerModule.setup` in production, `config.get(..., 'default')`, filters returning `stack`, `DevtoolsModule`, `synchronize: true` |
| Dependencies | `references/dependencies.md` | EOL Nest 10, Fastify middleware advisories, multer, TypeORM, `@nestjs/devtools-integration` |
| Verification | `references/verification.md` | Test apps that skip `main.ts` configuration, proof tests per finding class |

### 4. Classify and report

Every finding needs evidence: file, line, the code or config, and the path from attacker input to the sensitive operation, **including which guards, pipes and interceptors run on that route**. Classify using the rules below.

### 5. Remediate and verify (when asked to fix)

Explain the issue first. Make the smallest change that uses Nest's own mechanism (a bound guard, `whitelist: true`, a response DTO, `getOrThrow`, an `APP_GUARD` order). Then verify with `references/verification.md`: the attack fails, legitimate use works, siblings (other methods, GraphQL, gateways, microservice handlers) are fixed, and the test app applies the same bootstrap configuration as `main.ts`.

## High-signal patterns

These are **investigation signals, not findings**. Trace each one before reporting.

```text
# Guards / auth
handleRequest(err, user) { return user }   getAllAndMerge(   reflector.get(   @Roles( without RolesGuard   @Public()
ignoreExpiration   ?? 'secret'   get('JWT_SECRET', '   jwtService.decode(   secretOrKey   createHash('sha256'|'md5')
APP_GUARD order   useGlobalGuards   connectMicroservice( without inheritAppConfig   handleConnection(   fieldResolverEnhancers

# Validation / exposure
new ValidationPipe()   @Body() body: any   @Body() dtos: Dto[]   import type { Dto }   PartialType(Create   Object.assign(entity, dto)
repo.update(id, body)   repo.create(dto)   @Exclude(   ClassSerializerInterceptor   @Res()   returns entity   passwordHash

# Injection / data layer
query(`   createQueryBuilder   .where(`   .orderBy(   $queryRawUnsafe   findOne({ where: { id: undefined }   find(req.body   $where

# Config / surface
SwaggerModule.setup   introspection:   graphiql: true   cors: true   origin: true   credentials: true   enableCors(   helmet
ThrottlerModule.forRoot without ThrottlerGuard   @SkipThrottle   FileInterceptor( without limits   fallbackToMimetype   originalname
HttpService   this.http.get(   @Redirect   host: '0.0.0.0'   Transport.TCP   synchronize: true   DevtoolsModule   exception.stack
```

## Common false positives

Do not report these without further evidence:

- **`@Public()` on login, register, refresh, health and signature-verified webhook routes.** Report only when the route exposes sensitive data or state change.
- **A controller without `@UseGuards`** when a global `APP_GUARD` authenticates every non-`@Public()` route.
- **`getAllAndOverride(KEY, [handler, class])`** public checks and `AuthGuard` subclasses that keep the default throwing `handleRequest`.
- **`JwtService.decode()`** on a token this process just signed, or after `verify`.
- **Parameterized queries** (`$1`, `:name` bindings, tagged Prisma `$queryRaw`) and interpolated identifiers taken from a constant allow-list map.
- **`ParseUUIDPipe` ids that are then looked up with an owner or tenant filter.**
- **`@Exclude`d fields on responses covered by a bound `ClassSerializerInterceptor`**, and explicit response DTOs with `@Expose` plus `excludeAll`.
- **`FileTypeValidator` with an anchored type on memory storage** (magic-number check) plus `limits`, random file names and private storage.
- **Signature-verified webhooks** (HMAC over `rawBody` with `timingSafeEqual`) and Bearer-only APIs without CSRF middleware.
- **Swagger or GraphiQL in non-production** and Apollo introspection when `NODE_ENV=production` is verified.
- **Default Nest 500 responses** (`Internal server error`) and `X-Powered-By: Express` alone (Informational).
- **TCP microservices on `localhost`/private networks** called only by trusted services (state the assumption; Hardening).

## Severity calibration

| Pattern | Typical severity |
|---|---|
| Auth bypass: fail-open global guard, forgeable JWT secret, middleware bypass on Fastify protecting auth, unauthenticated admin controller | Critical (High if it needs a low-privilege account) |
| Unauthenticated TCP/broker handler performing privileged work | Critical when reachable beyond localhost |
| SQL/NoSQL injection | Critical unauthenticated; High authenticated |
| IDOR / BFLA, role escalation by mass assignment | High (Critical across tenants, for roles, money or credentials) |
| Credential/hash exposure in responses | High (Medium when the hash is the caller's own) |
| SSRF returning responses | High (Critical if cloud metadata is reachable) |
| Path traversal read / arbitrary file write | High / Critical |
| GraphQL field-level auth gap on sensitive fields | High; introspection and no cost limits Medium/Low |
| WebSocket auth by client-supplied identity | High |
| CORS reflection with credentials on cookie auth; missing CSRF on cookie auth | High / Medium |
| Weak password hashing, throttler not bound on login | Medium (High for unsalted fast hashes with a data leak path) |
| Swagger UI in production, verbose errors, missing headers | Low/Medium; Hardening for headers |
| Open redirect alone | Low |

Common under-ratings to avoid:
- **`ThrottlerModule` imported but `ThrottlerGuard` never bound** is no rate limiting at all.
- **Singleton services holding per-request user state** cause cross-user data exposure under concurrency.
- **Hybrid apps:** a global JWT guard does not protect the TCP/broker handlers.

## Build-mode guardrails

When writing Nest code, default to:

1. **Default-deny auth:** one global auth guard (`APP_GUARD`) plus an explicit `@Public()`; read it with `getAllAndOverride<boolean>(KEY, [getHandler(), getClass()])`; `handleRequest` must throw when there is no user.
2. **Order guards deliberately:** authentication, then roles/permissions, then throttling per need; bind `RolesGuard` wherever `@Roles()` is used.
3. **Global `ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true })`**, DTO classes (never interfaces/`any`/type-only imports), `@ValidateNested()` + `@Type()`, array bodies via `ParseArrayPipe`, separate create/update DTOs without privileged fields.
4. **Authorize objects in the service:** scope every query by the caller or tenant from the verified identity; never keep the current user in a singleton field.
5. **Return response DTOs** or bind `ClassSerializerInterceptor` globally with `@Exclude`/`@Expose`; never return raw entities with credential columns.
6. **Parameterize queries;** allow-list sort fields; guard against `undefined` filters (dropped silently on TypeORM 0.3.x and Prisma); no string-built `where`/`orderBy`.
7. **JWT:** secret from validated config (`getOrThrow`), pinned `algorithms`, `expiresIn`, issuer/audience, `ignoreExpiration` left false; Argon2id/bcrypt for passwords.
8. **main.ts:** explicit CORS origins, `helmet()` or `useSecurityHeaders()` (12.1+), `enableCsrfProtection()` (12.1+) or `csrf-csrf` for cookie auth, correct `trust proxy`, body limits, Swagger/GraphiQL only outside production.
9. **Rate limit** with `ThrottlerGuard` bound and strict `@Throttle` on login/reset/OTP, shared storage when multi-instance.
10. **Uploads:** multer `limits`, memory or private storage, random names, anchored `FileTypeValidator` without fallback, no public upload directory.
11. **Gateways and microservices:** authenticate in `handleConnection()` and per message, derive rooms from identity, bind TCP to localhost or use TLS plus a verified caller identity, `inheritAppConfig: true` in hybrid apps.
12. **Outbound requests:** fixed hosts or allow-lists with resolved-IP checks, no redirects to unvalidated hosts; `@Redirect` only to validated relative paths.
13. Test the boundary with supertest using the **same `configureApp(app)`** as `main.ts`; do not override the guard under test.

## Evidence and reporting rules

Use these when `appsec-review` is not installed.

**Classification**

- **Confirmed**: the path from attacker input to impact is fully traced in code/config (including the guards, pipes and interceptors on the route), or it was safely demonstrated.
- **Likely**: strong evidence, but one runtime condition (production `NODE_ENV`, a proxy or gateway, an env var, middleware applied outside the repo) couldn't be verified. Name it.
- **Hardening**: not demonstrably exploitable, but a stronger control is recommended.
- **Informational**: context with no direct security impact.

**Severity** follows impact x exploitability x required privileges x exposure. Don't raise severity because a scary keyword appears.

**Finding format**

```markdown
### [SEVERITY] Title — Confirmed|Likely|Hardening
- **Location:** `src/invoices/invoices.controller.ts:42` (`GET /invoices/:id`)
- **Evidence:** the exact code/config, and how attacker input reaches it (effective guards, pipes, interceptors)
- **Impact:** what an attacker gains, and who the attacker must be
- **Preconditions:** auth level, configuration, deployment assumptions
- **Fix:** smallest Nest-native change (code snippet)
- **Verify:** supertest or request that proves the fix
- **Refs:** CWE / OWASP / official docs link
```

**Rules:** never invent files, routes, packages, advisory IDs or config values. Redact secrets (`JWT_SECRET=ab****`). Say explicitly when runtime verification wasn't performed. Only test applications the user is authorized to assess, using non-destructive checks.

## References

- NestJS docs: https://docs.nestjs.com/ (security: /security/authentication, /security/authorization, /security/cors, /security/csrf, /security/helmet, /security/rate-limiting; request lifecycle: /faq/request-lifecycle)
- NestJS security advisories: https://github.com/nestjs/nest/security/advisories
- Nest 12 migration guide: https://docs.nestjs.com/migration-guide
- OWASP API Security Top 10 (2023), OWASP Node.js Security Cheat Sheet, OWASP GraphQL Cheat Sheet: https://cheatsheetseries.owasp.org/
- OWASP ASVS 5.0: https://owasp.org/www-project-application-security-verification-standard/

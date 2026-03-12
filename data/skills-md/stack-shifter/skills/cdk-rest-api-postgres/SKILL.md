---
name: cdk-rest-api-postgres
description: Designs and implements REST APIs on AWS using the target repository's CDK patterns first, with AWS Lambda handlers and Postgres via Drizzle as the default datastore. Use this whenever the user wants to add or modify API Gateway REST endpoints, Lambda handlers, Cognito auth, request models, reusable CDK constructs, Drizzle schema, SQL repositories, or database-backed CRUD routes, even if they only ask for "an endpoint", "a handler", "a table", "a repository", or "some CDK wiring".
---

## Purpose

Use this skill to design and implement Postgres-backed REST APIs on AWS in a way that fits the target repository.

Treat Postgres plus Drizzle as the default persistence model. When the repository already has compatible constructs and runtime patterns, extend them. When those pieces do not exist, use the references in this skill as portable patterns to generate an equivalent structure.

Portable references live in `references/`. Load only the patterns needed for the task:

- `references/rest-api-pattern.md` for centralized REST route composition patterns
- `references/node-lambda-pattern.md` for Lambda defaults and environment wiring
- `references/importer-pattern.md` for importing existing AWS resources into the stack
- `references/response-pattern.md` for controller and middleware response conventions
- `references/sql-drizzle-pattern.md` for Drizzle schema, repository, and `DatabaseContext` guidance
- `references/auth-pattern.md` for Cognito authorizer, scopes, and handler-level group authorization
- `references/runtime-composition-pattern.md` for `src/app.ts` singleton wiring and dependency aggregation
- `references/middleware-pattern.md` for reusable Middy middleware such as auth, validation, and HTTP error handling
- `references/services-pattern.md` for logger, storage, notification, and mapper service design
- `references/utilities-pattern.md` for `RestResult`, error types, status codes, cursor helpers, and related utilities
- `references/schedule-pattern.md` for EventBridge-triggered scheduled Lambda jobs

## Repository Rule

This skill is repository-aware, not file-path-bound.

The source of truth order is:

1. The target repository's current architecture, naming, and abstractions
2. The patterns in this skill's references
3. The inline examples in this skill

If the local code differs from examples in this skill, follow local code and use the examples only as design guidance.

## Repository Discovery

Start every use of this skill with a short discovery pass before proposing code.

Inspect only the parts of the repository that matter for the request. Common places include:

- `lib/core-stack.ts`
- `lib/constructs/rest-api.ts`
- `lib/constructs/node-lambda.ts`
- `lib/constructs/api-models.ts`
- `src/handlers/`
- `src/controllers/`
- `src/middlewares/`
- `src/services/`
- `src/models/validation/`
- `src/data/db/`
- `src/data/repositories/`
- `src/data/context.ts`
- `src/utilities/rest-result.ts`
- `src/utilities/`
- `src/app.ts`

Look for:

- how the route is registered in CDK
- which handler export name the stack expects
- which Middy middleware chain the handler follows
- whether the controller already exists or should be added
- whether a repository or schema already models the data
- whether shared services or mappers already exist for the resource area
- whether middleware or utilities already solve validation, authorization, cursor parsing, or error handling
- whether the change needs environment variables from `getDefaultLambdaEnvironment`
- whether handler files export a typed `HANDLER` registry constant to use for `handlerName` wiring
- whether `src/data/db/schema/` modules already define the relevant table, and whether a schema index re-exports them
- whether a migration workflow exists (`drizzle.config.ts`, a `drizzle/` folder) and what command generates migrations — confirm before proposing schema changes
- whether `src/data/db/client.ts` already exports a shared `db` client and `Db` type

After discovery, choose the appropriate approach and state it:

- `Existing pattern mode`: the repository already has abstractions worth extending
- `Pattern generation mode`: the repository is missing one or more pieces, so generate code that establishes the pattern cleanly

## Existing Pattern Mode

Use the repository's existing abstractions directly:

- `RestServerlessApi` for API Gateway REST route composition
- `NodeLambda` for Lambda defaults and bundling
- `Importer` when the stack needs to attach to existing AWS resources
- `RestResult` for API Gateway response objects
- `DatabaseContext` plus Drizzle repositories for persistence

Avoid hand-rolling raw API Gateway, Lambda, or persistence wiring unless the existing abstractions clearly cannot support the requirement.

## Pattern Generation Mode

Use this mode when the target repository has no reusable abstraction for one or more layers.

In this mode:

- use the references as guidance for the shape of the code, not as a demand that exact filenames or classes exist
- create only the minimal new abstraction needed to keep the generated code coherent and reusable
- prefer introducing a small reusable construct, helper, middleware, service, or repository pattern over shipping one-off route code
- keep the generated names and folders aligned with the target repository's conventions, even when the conceptual pattern comes from this skill

## Working Rules

1. Read the relevant local construct, stack, handler, controller, and repository code before editing.
2. If the repository already has a route composition abstraction such as `RestServerlessApi`, use it. If not, generate a small reusable pattern instead of scattering raw CDK logic.
3. Keep handlers thin. Put orchestration in controllers and persistence in `src/data/repositories/`.
4. For database work, model schema in Drizzle and query via a shared `db` client or equivalent shared database access layer.
5. Reuse an existing dependency composition pattern such as `DatabaseContext` or `src/app.ts` when it exists. If it does not, create a lightweight equivalent rather than wiring dependencies ad hoc in handlers.
6. Reuse the local Middy middleware stack pattern when it exists. If it does not, generate a reusable middleware composition pattern instead of inlining validation and auth in every handler.
7. Return responses through the local response helper when one exists. Otherwise generate one shared response utility instead of repeating inline response objects.
8. Preserve Cognito authorizer behavior and group-based authorization middleware when extending protected routes.
9. Prefer service classes and mapper classes for cross-cutting logic that appears in more than one controller.
10. Centralize reusable error and cursor helpers under `src/utilities/` or an equivalent shared module rather than duplicating them in repositories or handlers.
11. Prefer small reusable services for cross-cutting concerns such as logging, storage, notifications, and DTO mapping. When the same concern appears in more than one controller, extract it into a shared service rather than duplicating it inline.

## Default Assumptions

- API type: API Gateway REST API
- Compute: one Lambda handler export per route
- Datastore: Postgres via Drizzle and the shared Neon HTTP client
- Runtime defaults: existing Lambda wrapper defaults when present, otherwise a consistent Node.js Lambda baseline
- Auth: Cognito authorizer at API Gateway plus `authorizedGroup(...)` in handlers when needed
- Validation: Zod schemas through `validation.middleware.ts`
- Environment: Lambda runtime should receive shared database and app settings through one central helper or wiring layer when possible

If the user gives constraints that conflict with these defaults, adapt and state the change.

## Project Shape

Use a structure like this when the repository does not already provide a better one:

```text
lib/
├── constructs/
└── core-stack.ts

src/
├── controllers/
├── data/
│   ├── db/
│   │   ├── client.ts
│   │   └── schema/
│   ├── context.ts
│   └── repositories/
├── handlers/
├── middlewares/
├── models/
│   └── validation/
├── services/
├── utilities/
└── app.ts
```

Treat this as a conceptual layout, not a hard requirement:

- `lib/core-stack.ts` or an equivalent stack module registers routes and shared route defaults
- `src/handlers/` contains Middy-wrapped Lambda exports
- `src/controllers/` contains request orchestration and response shaping
- `src/data/db/schema/` defines Drizzle Postgres tables and relations
- `src/data/repositories/` contains SQL access logic
- `src/data/context.ts` or an equivalent module wires repositories to a shared `Db` and exposes a shared runtime context
- `src/services/` holds logger, storage, notification, mapper, and other integration-facing services
- `src/utilities/` holds response helpers, error types, status codes, cursor helpers, and shared pure functions
- `src/models/validation/` contains Zod schemas for request validation

## Construct-Centered Guidance

### 1. Route composition should be centralized

If the repository already has a route composition abstraction such as `RestServerlessApi`, extend it. Otherwise create one reusable route composition layer and keep route registration centralized.

Common route helpers are:

- `get`
- `getById`
- `post`
- `put`
- `delete`

Set shared defaults once:

```ts
const cognitoAuthorizer = api.createCognitoAuthorizer(userPool);

api.setDefaultRouteOptions({
    authorizer: cognitoAuthorizer,
    environmentVariables: getDefaultLambdaEnvironment(),
});
```

Important pattern details:

- `routePath` must start with `/`
- default route options merge with per-route options
- setting `authorizer: undefined` on a route removes the default authorizer
- scopes are typically passed per route in the stack layer
- route grants are connection-based; no table-level IAM grants are needed for SQL persistence

### 2. Lambda runtime defaults should be centralized

If the repository already has a Lambda wrapper such as `NodeLambda`, use it. Otherwise generate a small shared wrapper or helper that centralizes runtime defaults.

Useful baseline defaults include:

- Node.js 24.x
- ARM64
- 128 MB memory unless overridden
- 15 second timeout unless overridden
- active X-Ray tracing
- CloudWatch log group with three-month retention
- bundling with `@aws-sdk/*` externalized

A shared environment helper often needs values such as:

- `DATABASE_URL`
- `FRONTEND_URL`
- `S3_BUCKET`
- `SES_IDENTITY_EMAIL`
- `SES_IDENTITY_EMAIL_ARN`
- optional `CORS_ORIGIN`
- optional `ALLOWED_GROUP`

When adding routes, inherit shared environment wiring unless there is a strong reason not to.

Three helpers are commonly used together in the stack: `getDefaultLambdaEnvironment()`, `getStackLambdaName()`, and `createSendEmailPolicy()`. See `references/node-lambda-pattern.md` for their signatures, usage, and the pattern for attaching the SES policy.

### 3. Keep route wiring readable and repetitive in the right way

Never write `handlerName` as a bare string literal — a rename in the handler file will not be caught at compile time without a registry. Each handler file should export a typed `HANDLER` registry constant, which the stack imports and uses for all route wiring.

Prefer:

- one handler file per resource area
- `HANDLER` registry constants exported from each handler file and imported by the stack
- `lambdaName()` and `handlerPath()` local helpers wrapping `getStackLambdaName` and `path.join`
- shared Cognito authorizer defaults with per-route scopes

See `references/rest-api-pattern.md` for the full registry template, multi-route stack examples, and the `setDefaultRouteOptions` setup.

### 4. Prefer `Importer` for existing infrastructure

If the repository exposes an importer helper like `lib/constructs/api-importer.ts`, use it when wiring a stack to resources that already exist.

Prefer patterns like:

```ts
import { Importer } from './constructs/api-importer';

const userPool = Importer.getCognitoUserPoolById(this, process.env.COGNITO_USER_POOL_ID!);
const s3Bucket = Importer.getS3Bucket(this, process.env.S3_BUCKET!);
const apiDomain = Importer.getApiGatewayDomainName(
    this,
    process.env.API_DOMAIN_NAME!,
    process.env.API_DOMAIN_NAME_ALIAS!,
    process.env.ZONE_ID!,
);
```

Use the importer when the stack attaches to an existing user pool, S3 bucket, domain, or other shared resource, and the repository already centralizes `from*` imports behind an importer helper. Do not replace a repository-wide importer with direct `fromUserPoolId` or similar calls unless the user explicitly asks for it.

See `references/importer-pattern.md` for the portable shape.

### 5. Prefer `RestResult` for API responses

If the repository has a response helper like `src/utilities/rest-result.ts`, use it as the default response format for controllers.

Prefer methods such as:

- `RestResult.Ok(...)`
- `RestResult.Created(..., location)`
- `RestResult.NoContent()`
- `RestResult.BadRequest(...)`
- `RestResult.Unauthorized(...)`
- `RestResult.Forbidden(...)`
- `RestResult.NotFound(...)`
- `RestResult.Conflict(...)`
- `RestResult.InternalServerError(...)`

Use `RestResult.fromDatabaseError(error)` before falling through to a generic 500 whenever a repository operation could fail with a recognized Postgres constraint error. This keeps CORS headers, content types, status codes, and error body shapes consistent across all endpoints.

If no local response helper exists, load `references/response-pattern.md` for the full class shape and baseline implementation.

### 6. Use `ScheduleLambda` for EventBridge-triggered background jobs

If the repository exposes a scheduled Lambda construct (e.g., `lib/constructs/schedule.ts`), use it for any non-API background work such as soft-delete cleanup, digest emails, or data expiry sweeps. Do not create a raw `events.Rule` + `NodejsFunction` pair inline.

Key points:

- the scheduled Lambda follows the same `HANDLER` registry pattern as API handlers
- the handler entrypoint type is `ScheduledEvent` from `aws-lambda`, not `APIGatewayProxyEvent`
- for Postgres-backed jobs, pass `DATABASE_URL` through `getDefaultLambdaEnvironment()` — no table-level IAM grants are needed

See `references/schedule-pattern.md` for the full construct snippet, handler template, and all key options.

## Runtime Guidance

### Handlers

Handlers should follow the local Middy pattern:

- `httpHeaderNormalizer()`
- `httpEventNormalizer()`
- `handleHttpError()`
- `httpJsonBodyParser({ disableContentTypeError: true })` for write routes
- `authorizedGroup(...)` when group authorization is required
- `validateHeaders(...)`, `validatePathParameters(...)`, `validateQueryParameters(...)`, and `validateBody(...)` as needed

Keep handler files mostly declarative. They should compose middleware around controller functions rather than implement business logic directly.

If the repository does not yet have a consistent handler pattern, generate one that keeps:

- middleware composition in the handler
- orchestration in the controller
- persistence in repositories
- shared concerns in middleware, services, and utilities

### Controllers

Controllers should:

- read typed event data after middleware validation
- call `dbContext` and other shared services from a shared composition module
- map entities through the repository and mapper layers
- return `RestResult` responses
- translate repository failures with `RestResult.fromDatabaseError(...)` when applicable

### Data Layer

Persistence work belongs under `src/data/` or an equivalent data layer.

Preferred flow:

1. define or update table schema in `src/data/db/schema/`
2. export it through the schema index if needed
3. implement repository behavior in `src/data/repositories/`
4. wire the repository through `src/data/context.ts` if it is a new repository
5. consume it from controllers via `dbContext`

Do not open raw database connections inside handlers or controllers. Reuse the shared `db` and `DatabaseContext` or an equivalent context pattern.

### Drizzle Schema Rules

When adding or changing persistence:

- use `pgTable`, typed columns, indexes, enums, and relations from Drizzle
- keep relations centralized in a dedicated schema module when appropriate
- mirror existing schema naming and table file conventions when they already exist
- prefer SQL constraints and indexes over application-only uniqueness logic
- generate migrations with the repo's Drizzle workflow, or introduce one coherent migration workflow instead of inventing manual SQL files

### Repository Rules

Repository APIs in this skill should stay SQL-oriented, not key-value oriented.

Prefer methods that reflect domain behavior, for example:

- `getById`
- `query`
- `save`
- `updateById`
- `delete`
- relation-specific helpers when needed

For cursor pagination, do not assume UUID v4 primary keys are time-ordered. Prefer a stable ordered tuple such as `created_at` plus `id`, and make the cursor carry both values.

When generating a repository pattern from scratch:

- define repository methods around domain actions rather than query-builder details
- keep transaction boundaries above the repository only when multiple repositories must coordinate
- keep mapping from raw row shape to API response out of the handler
- avoid importing Drizzle schema objects directly into handlers unless the repository layer does not exist yet

## Response and Error Rules

Use `src/utilities/rest-result.ts` or an equivalent shared response helper for all API responses.

Prefer:

- `RestResult.Ok(...)`
- `RestResult.Created(...)`
- `RestResult.NoContent()`
- `RestResult.BadRequest(...)`
- `RestResult.NotFound(...)`
- `RestResult.Unauthorized(...)`
- `RestResult.Forbidden(...)`
- `RestResult.InternalServerError(...)`

For recognized Postgres constraint failures, prefer `RestResult.fromDatabaseError(error)` before falling back to generic 500 handling.

## Auth Rules

Protected routes should usually use two layers:

1. API Gateway Cognito authorizer and scopes in CDK
2. handler-level group authorization via `authorizedGroup(...)`

When changing protected routes:

- preserve route scopes in the stack layer
- preserve or extend group checks in handlers
- use existing `ALLOWED_GROUP` semantics when present
- do not reintroduce removed client-account auth flows

## Change Patterns

When adding a new CRUD endpoint, the usual path is:

1. add or update the Drizzle schema if persistence changes
2. add or extend the repository
3. add or extend the controller
4. add or extend the handler with Middy middleware and validation
5. register the route in the stack or route-composition layer
6. add focused tests for the changed behavior

When the request is only infrastructure-facing, still confirm whether handler, controller, repository, validation, or environment wiring also needs to move with it.

When generating the architecture from scratch, prefer this order:

1. define or update the data model and migration
2. define repository methods around the use case
3. define controller behavior and response mapping
4. add handler middleware and validation
5. register the route and shared environment wiring
6. add tests around the repository, controller, or handler boundary that changed

## Response Style

When using this skill, produce:

1. A short statement of the endpoint(s) being added or changed
2. A note saying whether you are using `Existing pattern mode` or `Pattern generation mode`
3. CDK snippets based on local constructs when present, or the portable baseline when not
4. The data layer change: new Drizzle schema and migration needed, or existing schema extended
5. Any handler, controller, repository, or validation follow-on work needed to make the endpoint functional
6. Explicit assumptions where auth, schema, or validation is ambiguous

Avoid generic AWS guidance when a repository-specific construct snippet would answer the request better. Treat the repository's code as authoritative and the skill as workflow guidance, not as a competing source of truth.

## Definition of Done

A change using this skill is usually complete when:

- the route is registered through the local CDK abstractions
- the handler matches the repository's Middy style or establishes one coherent style
- controller and repository responsibilities stay separated
- persistence uses Drizzle and Postgres only
- tests cover the changed behavior at the right layer

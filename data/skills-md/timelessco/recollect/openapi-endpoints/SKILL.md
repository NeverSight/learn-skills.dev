---
name: openapi-endpoints
description: How to add, update, and document OpenAPI endpoints in Recollect. Use when creating new App Router endpoints, updating endpoint schemas, writing supplement files, adding named examples, or registering edge function endpoints in the OpenAPI spec.
---

# OpenAPI Endpoint Documentation

The spec is generated in two passes: (1) a filesystem scanner auto-infers schemas from handler factories, (2) a merge script overlays human-authored metadata from supplement files. The full human-readable guide is at `docs/OPENAPI_GUIDE.md`.

## Quick Start

### New App Router endpoint

1. Create `src/app/api/<path>/route.ts` using a handler factory
2. Create `src/app/api/<path>/schema.ts` with `InputSchema` + `OutputSchema`
3. Create `src/lib/openapi/endpoints/<domain>/<endpoint-name>.ts` (supplement)
4. Export supplement from `src/lib/openapi/endpoints/<domain>/index.ts`
5. Run `npx tsx scripts/generate-openapi.ts`
6. Verify at `http://localhost:3000/api-docs`

### Update existing endpoint

1. Modify schema in `schema.ts` — auto-captured by scanner
2. Update supplement metadata/examples in `src/lib/openapi/endpoints/<domain>/`
3. Run `npx tsx scripts/generate-openapi.ts`

### New edge function endpoint

1. Create registration function in `src/lib/openapi/endpoints/<domain>/edge-process-imports.ts`
2. Use `registry.registerPath()` with raw `SchemaObject` (not Zod)
3. Import and call from `scripts/generate-openapi.ts`
4. Run `npx tsx scripts/generate-openapi.ts`
5. Verify at `http://localhost:3000/api-docs`

For edge function details, see [reference.md](reference.md).

## New App Router Endpoint

### Step 1: Create route handler

Use one of the 4 handler factories from `src/lib/api-helpers/create-handler.ts`:

- `createGetApiHandlerWithAuth` — GET with auth
- `createPostApiHandlerWithAuth` — POST with auth
- `createGetApiHandler` — GET without auth
- `createPostApiHandler` — POST without auth

```typescript
// src/app/api/<domain>/<endpoint>/route.ts
import { createGetApiHandlerWithAuth } from "@/lib/api-helpers/create-handler";
import { MyInputSchema, MyOutputSchema } from "./schema";

const ROUTE = "domain-endpoint-name";

export const GET = createGetApiHandlerWithAuth({
	route: ROUTE,
	inputSchema: MyInputSchema,
	outputSchema: MyOutputSchema,
	handler: async ({ data, supabase, user, route }) => {
		// business logic
		return { result: "value" };
	},
});
```

### Step 2: Create schema file

Colocate Zod schemas next to `route.ts`:

```typescript
// src/app/api/<domain>/<endpoint>/schema.ts
import { z } from "zod";

export const MyInputSchema = z.object({
	url: z.string(),
});

export const MyOutputSchema = z.object({
	result: z.string(),
});
```

### Step 3: Create supplement file

Supplements provide metadata the scanner can't infer: tags, summary, description, examples.

```typescript
// src/lib/openapi/endpoints/<domain>/<endpoint-name>.ts
import { type EndpointSupplement } from "@/lib/openapi/supplement-types";
import { bearerAuth } from "@/lib/openapi/registry";

export const myEndpointSupplement = {
	path: "/<domain>/<endpoint-name>",
	method: "get",
	tags: ["<Domain>"],
	summary: "Short description for Scalar heading",
	description: "Detailed explanation of what the endpoint does.",
	security: [{ [bearerAuth.name]: [] }, {}],
	responseExample: {
		data: { result: "value" },
		error: null,
	},
} satisfies EndpointSupplement;
```

**Rules:**

- `path` is relative to `/api` (e.g., `/bookmarks/check-url` not `/api/bookmarks/check-url`)
- `method` is lowercase: `"get"` or `"post"`
- Tags are capitalized: `"Bookmarks"`, `"Categories"`, `"Twitter"`
- Security `[{ [bearerAuth.name]: [] }, {}]` — empty `{}` means cookie auth also accepted
- Export name: `<camelCaseName>Supplement`

### Step 4: Export from barrel

```typescript
// src/lib/openapi/endpoints/<domain>/index.ts
export { myEndpointSupplement } from "./<endpoint-name>";
```

### Step 5: Regenerate and verify

```bash
npx tsx scripts/generate-openapi.ts
```

Open `http://localhost:3000/api-docs` and verify the endpoint appears.

## Updating an Existing Endpoint

### Schema changes

Modify the Zod schema in `schema.ts` — the scanner picks it up automatically. The GitHub Actions changelog workflow runs `oasdiff` on every push to `dev` and appends changes to `docs/API_CHANGELOG.md`.

### Updating supplement metadata

Edit the supplement file directly: `summary`, `description`, `tags`, `additionalResponses`.

### Adding examples

**Single example** (simple endpoints):

```typescript
responseExample: {
  data: { id: 1, name: "Example" },
  error: null,
},
```

**Named examples** (multiple scenarios — creates a dropdown in Scalar):

```typescript
responseExamples: {
  "happy-path": {
    summary: "Successful response",
    description: "Returns the created resource.",
    value: { data: { id: 1 }, error: null },
  },
  "duplicate-detected": {
    summary: "Duplicate skipped",
    description: "URL already bookmarked.",
    value: { data: { inserted: 0, skipped: 1 }, error: null },
  },
},
```

**400 error examples:**

```typescript
response400Examples: {
  "empty-array": {
    summary: "Empty bookmarks array",
    description: "Fails when bookmarks array has no elements.",
    value: { data: null, error: "bookmarks: Array must contain at least 1 element(s)" },
  },
},
additionalResponses: {
  400: { description: "Invalid request body or bookmark data" },
},
```

When the supplement file exceeds 250 lines, extract examples to `<endpoint-name>-examples.ts`.

**Parameter examples** (GET query param dropdown in Scalar):

```typescript
parameterExamples: {
  email: {
    "valid-user": {
      summary: "Valid user email",
      description: "Returns user data for this email.",
      value: "user@example.com",
    },
    "unknown-email": {
      summary: "Nonexistent email",
      description: "Returns null/empty result.",
      value: "nobody@example.com",
    },
  },
},
```

Outer key = parameter name (must match `name` in the generated spec). Inner map = standard named examples. Creates a dropdown per query param in Scalar's "Try It" panel.

## Supplement Reference

### EndpointSupplement fields

| Field                 | Type                              | Purpose                                  |
| --------------------- | --------------------------------- | ---------------------------------------- |
| `path`                | `string`                          | Route path relative to `/api` (required) |
| `method`              | `string`                          | `"get"` or `"post"` lowercase (required) |
| `tags`                | `string[]`                        | Scalar sidebar grouping                  |
| `summary`             | `string`                          | Short heading (one line)                 |
| `description`         | `string`                          | Detailed explanation (supports markdown) |
| `security`            | `Array<Record<string, string[]>>` | Auth requirements                        |
| `requestExample`      | `Record<string, unknown>`         | Single request body example              |
| `requestExamples`     | Named examples object             | Multiple request examples                |
| `responseExample`     | `Record<string, unknown>`         | Single 200 response example              |
| `responseExamples`    | Named examples object             | Multiple 200 response examples           |
| `response400Example`  | `Record<string, unknown>`         | Single 400 error example                 |
| `response400Examples` | Named examples object             | Multiple 400 error examples              |
| `additionalResponses` | `Record<number, { description }>` | Extra response codes (400, 403, 404)     |
| `parameterExamples`   | `Record<string, NamedExamples>`   | Per-param named examples (GET dropdown)  |

### Naming conventions

- Export name: `<camelCaseName>Supplement` (e.g., `checkUrlSupplement`)
- Named example keys: kebab-case (`"single-tweet"`, `"validation-error"`)
- Example files: `<endpoint-name>-examples.ts` (e.g., `sync-examples.ts`)
- Tags: capitalized (`"Bookmarks"`, `"iPhone"`)
- All named examples require both `summary` and `description`
- Happy paths first, then validation errors

### Response components

The scanner registers 3 `$ref` response components for every endpoint:

- `ValidationError` (400) — `{ data: null, error: string }`
- `Unauthorized` (401) — `{ data: null, error: "Not authenticated" }`
- `InternalError` (500) — `{ data: null, error: "Failed to process request" }`

`additionalResponses` overrides the 400 description while preserving the schema.

## Agent Prompt Templates

### Create supplement for a new endpoint

> I just created a new App Router endpoint at `src/app/api/<path>/route.ts` with schema at `src/app/api/<path>/schema.ts`. Create the OpenAPI supplement file, export it from the barrel, regenerate the spec, and verify at `/api-docs`.
>
> Domain: `<bookmarks|categories|tags|twitter|instagram|raindrop|profiles|iphone>`

### Update examples for an existing endpoint

> Update the OpenAPI examples for the `<endpoint-name>` endpoint. Read the current supplement at `src/lib/openapi/endpoints/<domain>/<endpoint-name>.ts`, add named examples for these scenarios: [describe scenarios]. Regenerate the spec and verify.

### Add 400 error examples

> Add `response400Examples` to the `<endpoint-name>` supplement. Include examples for: [list validation errors]. Also add `additionalResponses: { 400: { description: "<custom description>" } }`. Regenerate and verify.

### Add parameter examples for a GET endpoint

> Add `parameterExamples` to the `<endpoint-name>` supplement for each query parameter. Include examples for: [list test scenarios per param]. Regenerate the spec and verify the dropdown appears in Scalar's "Try It" panel.

### Document a new edge function

> I created a new Supabase Edge Function at `supabase/functions/<name>/`. Register it in the OpenAPI spec following the pattern in `src/lib/openapi/endpoints/instagram/edge-process-imports.ts`. Use `serviceRoleAuth`, `edgeFunctionServers`, and raw `SchemaObject`. Wire it into `scripts/generate-openapi.ts`.

## Troubleshooting

### Supplement not appearing in spec

1. Is the supplement exported from the domain's `index.ts` barrel?
2. Does `path` match the route path exactly (relative to `/api`, no trailing slash)?
3. Does `method` match the exported handler (`"get"` for `GET`, `"post"` for `POST`)?
4. Check console output — `mergeSupplements` prints warnings for unmatched supplements

### 400 examples not showing

1. Does the supplement have `additionalResponses: { 400: { description: "..." } }`?
2. Are named examples using `response400Examples` (not `responseExamples`)?
3. The merge script initializes 400 content automatically when examples are provided

### Common mistakes

- Using `/api/bookmarks/check-url` instead of `/bookmarks/check-url` for the path
- Forgetting `as const` on example data objects in `-examples.ts` files
- Using `responseExample` (singular) when you need `responseExamples` (named/plural)
- Missing `summary` or `description` on named examples — both are required

For edge function patterns and complex examples, see [reference.md](reference.md).

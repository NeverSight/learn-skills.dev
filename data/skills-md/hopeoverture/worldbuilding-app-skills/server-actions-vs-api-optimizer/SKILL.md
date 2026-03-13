---
name: server-actions-vs-api-optimizer
description: Analyze routes and recommend whether to use Server Actions or API routes based on use case patterns including authentication, revalidation, external API calls, and client requirements. Use this skill when deciding between Server Actions and API routes, optimizing Next.js data fetching, refactoring routes, analyzing route architecture, or choosing the right data mutation pattern. Trigger terms include Server Actions, API routes, route handler, data mutation, revalidation, authentication flow, external API, client-side fetch, route optimization, Next.js patterns.
---

# Server Actions vs API Routes Optimizer

Analyze existing routes and recommend whether to use Server Actions or traditional API routes based on specific use case patterns, including authentication flows, data revalidation, external API calls, and client requirements.

## Core Capabilities

### 1. Analyze Existing Routes

To analyze current route architecture:

- Scan app directory for route handlers and Server Actions
- Identify patterns in request/response handling
- Detect authentication, revalidation, and external API usage
- Use `scripts/analyze_routes.py` for automated analysis

### 2. Provide Recommendations

Based on analysis, provide recommendations using the decision matrix from `references/decision_matrix.md`:

- **Server Actions**: Form submissions, mutations with revalidation, simple data updates
- **API Routes**: External API proxying, webhooks, third-party integrations, non-form mutations
- **Hybrid Approach**: Complex flows requiring both patterns

### 3. Generate Migration Plans

When refactoring is recommended:

- Identify specific routes to convert
- Provide step-by-step migration instructions
- Show before/after code examples
- Highlight breaking changes and client updates needed

## When to Use Server Actions

Prefer Server Actions for:

1. **Form Submissions**: Direct form action handling with progressive enhancement
2. **Data Mutations with Revalidation**: Operations that need `revalidatePath()` or `revalidateTag()`
3. **Simple CRUD Operations**: Direct database mutations from components
4. **Authentication in RSC**: Auth checks in Server Components
5. **File Uploads**: Handling FormData directly
6. **Optimistic Updates**: Client-side optimistic UI with server validation

**Benefits**:
- Automatic POST request handling
- Built-in CSRF protection
- Type-safe with TypeScript
- Progressive enhancement (works without JS)
- Direct access to server-side resources
- Simpler code for common patterns

## When to Use API Routes

Prefer API routes for:

1. **External API Proxying**: Hiding API keys, rate limiting, response transformation
2. **Webhooks**: Third-party service callbacks (Stripe, GitHub, etc.)
3. **Non-POST Operations**: GET, PUT, DELETE, PATCH endpoints
4. **Third-Party Integrations**: OAuth callbacks, external service authentication
5. **Public APIs**: Endpoints called by external clients
6. **Complex Response Headers**: Custom headers, cookies, redirects
7. **Non-Form Client Requests**: fetch() calls from client components
8. **SSE/Streaming**: Server-sent events or custom streaming

**Benefits**:
- Full HTTP method support
- Custom response handling
- External accessibility
- Middleware support
- Standard REST API patterns

## Analysis Workflow

### 1. Run Automated Analysis

Use the analysis script to scan your codebase:

```bash
python scripts/analyze_routes.py --path /path/to/app --output analysis-report.md
```

The script identifies:
- Existing API routes and their patterns
- Server Actions usage
- Authentication patterns
- Revalidation calls
- External API integrations
- Potential optimization opportunities

### 2. Review Decision Matrix

Consult `references/decision_matrix.md` for detailed decision criteria:
- Use case patterns
- Trade-offs analysis
- Performance considerations
- Security implications
- Developer experience factors

### 3. Generate Recommendations

For each route, determine:
- Current implementation pattern
- Recommended pattern (Server Action or API route)
- Reasoning based on use case
- Migration complexity (low/medium/high)
- Potential benefits of refactoring

### 4. Create Migration Plan

For routes requiring changes:
- Prioritize high-impact, low-complexity migrations
- Document breaking changes
- Provide code transformation examples
- Update client-side code if needed

## Common Patterns and Recommendations

### Pattern: Form Submission with DB Update

**Current**: API route with fetch from client
**Recommended**: Server Action
**Reason**: Simpler, built-in CSRF protection, progressive enhancement

```typescript
// Before (API Route)
// app/api/entities/route.ts
export async function POST(request: Request) {
  const data = await request.json();
  await db.entity.create(data);
  return Response.json({ success: true });
}

// After (Server Action)
// app/actions.ts
'use server';
export async function createEntity(formData: FormData) {
  await db.entity.create(Object.fromEntries(formData));
  revalidatePath('/entities');
}
```

### Pattern: External API Proxy

**Current**: Client-side fetch to external API (exposes keys)
**Recommended**: API route
**Reason**: Hide API keys, rate limiting, response transformation

```typescript
// Recommended: API Route
// app/api/external-service/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('query');

  const response = await fetch(`https://api.external.com?key=${process.env.API_KEY}&q=${query}`);
  const data = await response.json();

  return Response.json(data);
}
```

### Pattern: Webhook Handler

**Current**: None (new feature)
**Recommended**: API route
**Reason**: External service calls, needs public URL

```typescript
// Recommended: API Route
// app/api/webhooks/stripe/route.ts
export async function POST(request: Request) {
  const signature = request.headers.get('stripe-signature');
  const body = await request.text();

  // Verify webhook signature
  // Process webhook event

  return Response.json({ received: true });
}
```

### Pattern: Data Mutation with Revalidation

**Current**: API route with manual cache invalidation
**Recommended**: Server Action
**Reason**: Built-in revalidation, simpler code

```typescript
// Before (API Route)
// app/api/entities/[id]/route.ts
export async function PATCH(request: Request, { params }) {
  const data = await request.json();
  await db.entity.update({ where: { id: params.id }, data });
  revalidatePath('/entities');
  return Response.json({ success: true });
}

// After (Server Action)
// app/actions.ts
'use server';
export async function updateEntity(id: string, data: any) {
  await db.entity.update({ where: { id }, data });
  revalidatePath('/entities');
  revalidateTag(`entity-${id}`);
}
```

### Pattern: Authentication Check

**Current**: API middleware
**Recommended**: Server Action for mutations, API route for public endpoints
**Reason**: Simpler auth in Server Components

```typescript
// Server Action (for mutations)
'use server';
export async function protectedAction() {
  const session = await auth();
  if (!session) throw new Error('Unauthorized');
  // Perform action
}

// API Route (for public/external access)
export async function POST(request: Request) {
  const token = request.headers.get('authorization');
  if (!validateToken(token)) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }
  // Process request
}
```

## Resource Files

### scripts/analyze_routes.py
Automated route analysis tool that scans your Next.js app directory to identify route patterns, Server Actions, authentication usage, revalidation calls, and external API integrations. Generates a detailed report with recommendations.

### references/decision_matrix.md
Comprehensive decision matrix with detailed criteria for choosing between Server Actions and API routes. Includes use case patterns, trade-offs, performance considerations, security implications, and real-world examples.

## Best Practices

1. **Default to Server Actions for Forms**: Simpler, more secure, better UX
2. **Use API Routes for External Integration**: Webhooks, proxies, third-party APIs
3. **Consider Progressive Enhancement**: Server Actions work without JavaScript
4. **Optimize for Revalidation**: Server Actions have built-in revalidation
5. **Evaluate Client Requirements**: If external clients need access, use API routes
6. **Think About Method Requirements**: Non-POST operations need API routes
7. **Consider Type Safety**: Server Actions are fully type-safe
8. **Plan for Migration**: Start with new features, gradually refactor existing

## Integration with Worldbuilding App

Common patterns in worldbuilding applications:

### Entity CRUD Operations
- **Create/Update/Delete entities**: Server Actions (form submissions with revalidation)
- **Get entity list for external dashboard**: API route (external client access)

### Relationship Management
- **Add/remove relationships**: Server Actions (mutations with revalidation)
- **Export relationship graph**: API route (complex response, streaming)

### Timeline Operations
- **Create/edit timeline events**: Server Actions (form submissions)
- **Timeline data feed for visualization**: API route (GET requests, caching)

### Search and Filtering
- **Filter entities in app**: Server Actions (with revalidation)
- **Public search API**: API route (external access, rate limiting)

### Import/Export
- **Import data files**: Server Action (FormData handling)
- **Export to external format**: API route (custom headers, streaming)

Consult `references/decision_matrix.md` for detailed analysis of each pattern.

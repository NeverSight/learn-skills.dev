---
name: frontend-react-router-best-practices
description: React Router performance and architecture patterns. Use when writing loaders, actions, forms, routes, or working with React Router data fetching. Triggers on tasks involving React Router routes, data loading, form handling, or route organization.
---

# React Router Best Practices

Performance optimization and architecture patterns for React Router applications. Contains 55 rules across 11 categories focused on data loading, actions, forms, streaming, and route organization.

## When to Apply

Reference these guidelines when:

- Writing new React Router routes (loaders, actions)
- Handling forms and mutations
- Implementing streaming with Single Fetch
- Organizing route files and colocating queries
- Setting up authentication patterns
- Adding SEO/meta tags

## Rules Summary

### Data Loading (CRITICAL)

#### loader-avoid-waterfalls - @rules/loader-avoid-waterfalls.md

All data fetching happens in loaders. Never fetch in components with useEffect.

```tsx
// BAD: fetching in component
function Profile() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch("/api/user")
      .then((r) => r.json())
      .then(setUser);
  }, []);
  if (!user) return <Spinner />;
  return <div>{user.name}</div>;
}

// GOOD: fetch in loader
export async function loader({ request }: Route.LoaderArgs) {
  let user = await getUser(request);
  return data({ user });
}

export default function Component() {
  const { user } = useLoaderData<typeof loader>();
  return <div>{user.name}</div>;
}
```

#### loader-parallel-fetch - @rules/loader-parallel-fetch.md

Use Promise.all for parallel data fetching in loaders.

```tsx
import { data } from "react-router";

// Bad: sequential fetches (slow)
export async function loader({ request }: Route.LoaderArgs) {
  let user = await getUser(request);
  let posts = await getPosts(user.id);
  let comments = await getComments(user.id);
  return data({ user, posts, comments });
}

// Good: parallel fetches
export async function loader({ request }: Route.LoaderArgs) {
  let user = await getUser(request);
  let [posts, comments] = await Promise.all([
    getPosts(user.id),
    getComments(user.id),
  ]);
  return data({ user, posts, comments });
}
```

#### loader-request-caching - @rules/loader-request-caching.md

API clients dedupe calls within the same request via context. Fetch in each loader that needs data.

```tsx
// Both loaders can call getUser - cached per request
export async function loader({ request, context }: Route.LoaderArgs) {
  let client = await authenticate(request, context);
  let user = await getUser(client); // Uses cached result if already fetched
  return data({ user });
}
```

#### loader-revalidation-patterns - @rules/loader-revalidation-patterns.md

Use useRevalidator for polling, focus, and reconnect revalidation.

```tsx
const { revalidate } = useRevalidator();

useEffect(() => {
  if (visibilityState === "hidden") return; // Don't poll hidden tabs
  let id = setInterval(revalidate, 30000);
  return () => clearInterval(id);
}, [revalidate, visibilityState]);
```

#### loader-typing - @rules/loader-typing.md

Use proper TypeScript typing with Route.LoaderArgs.

```tsx
// Good: typed loader with useLoaderData
import { data } from "react-router";
import { useLoaderData } from "react-router";

export async function loader({ request, params }: Route.LoaderArgs) {
  return data({ user: await getUser(params.id) });
}

export default function Component() {
  const { user } = useLoaderData<typeof loader>();
  return <div>{user.name}</div>;
}
```

#### loader-url-validation - @rules/loader-url-validation.md

Validate URL params with zod or invariant.

```tsx
// Good: validate params early
import { data } from "react-router";
import { z } from "zod";

export async function loader({ params }: Route.LoaderArgs) {
  let itemId = z.string().parse(params.itemId);
  return data({ item: await getItem(itemId) });
}
```

#### loader-action-abort-signal - @rules/loader-action-abort-signal.md

Abort async work when the request is canceled.

```ts
export async function loader({ request }: Route.LoaderArgs) {
  let response = await fetch(url, { signal: request.signal });
  return data(await response.json());
}
```

#### loader-colocate-queries - @rules/loader-colocate-queries.md

Keep data queries in colocated `queries.server.ts` files.

```
routes/
  _.projects/
    queries.server.ts  # All data fetching functions
    route.tsx          # Loader calls query functions
    components/        # Route-specific components
```

#### route-auth-middleware - @rules/route-auth-middleware.md

Authenticate via middleware and authorize in each loader/action.

```ts
export const middleware: Route.MiddlewareFunction[] = [
  sessionMiddleware,
  authMiddleware,
];

export async function loader({ context }: Route.LoaderArgs) {
  authorize(context, { requireUser: true, onboardingComplete: true });
  return null;
}
```

### Middleware & Security (HIGH)

#### middleware-session - @rules/middleware-session.md

Keep a single session instance per request.

```ts
export const middleware: Route.MiddlewareFunction[] = [sessionMiddleware];
```

#### middleware-context-storage - @rules/middleware-context-storage.md

Store context/request in AsyncLocalStorage for arg-less helpers.

```ts
export const middleware: Route.MiddlewareFunction[] = [contextStorageMiddleware];
```

#### middleware-batcher - @rules/middleware-batcher.md

Deduplicate request-scoped API/DB calls.

```ts
let result = await getBatcher().batch("key", () => getData());
```

#### middleware-request-id - @rules/middleware-request-id.md

Add request IDs for logging/correlation.

```ts
let requestId = getRequestID();
```

#### middleware-logger - @rules/middleware-logger.md

Log requests consistently with built-in middleware.

```ts
export const middleware: Route.MiddlewareFunction[] = [loggerMiddleware];
```

#### middleware-server-timing - @rules/middleware-server-timing.md

Add Server-Timing measurements to responses.

```ts
return getTimingCollector().measure("load", "Load data", () => getData());
```

#### middleware-singleton - @rules/middleware-singleton.md

Create per-request singletons for caches.

```ts
let cache = getSingleton(context);
```

#### sec-fetch-guards - @rules/sec-fetch-guards.md

Reject cross-site mutation requests via Sec-Fetch headers.

```ts
if (fetchSite(request) === "cross-site") throw new Response(null, { status: 403 });
```

#### form-honeypot - @rules/form-honeypot.md

Add honeypot inputs for public forms.

```tsx
<Form method="post">
  <HoneypotInputs />
</Form>
```

#### cors-headers - @rules/cors-headers.md

Apply CORS headers to API routes.

```ts
return await cors(request, data(await getData()));
```

#### safe-redirects - @rules/safe-redirects.md

Sanitize user-driven redirects.

```ts
return redirect(safeRedirect(redirectTo, "/"));
```

#### typed-cookies - @rules/typed-cookies.md

Validate cookie payloads with schemas.

```ts
let typed = createTypedCookie({ cookie, schema });
```

#### client-ip-address - @rules/client-ip-address.md

Extract client IP from trusted proxy headers.

```ts
let ip = getClientIPAddress(request);
```

#### data-parent-route-data - @rules/data-parent-route-data.md

Use `useRouteLoaderData` for UI-only access to parent data. For loader logic, fetch in each loader (API clients cache per request).

```tsx
// UI-only access - use useRouteLoaderData
export default function ChildRoute() {
  const { user } = useRouteLoaderData<typeof profileLoader>("routes/_layout");
  return <div>Welcome, {user.name}</div>;
}

// Loader needs data - fetch again (cached, no extra request)
export async function loader({ request }: Route.LoaderArgs) {
  let client = await authenticate(request);
  let user = await getUser(client); // Uses cached result
  let settings = await getSettings(client, user.id);
  return data({ settings });
}
```

#### data-only-route-calls-hooks - @rules/data-only-route-calls-hooks.md

Only route components call `useLoaderData`/`useActionData`. Children receive props.

```tsx
// route.tsx - only place that calls useLoaderData
export default function ItemsRoute() {
  const { items } = useLoaderData<typeof loader>();
  return <ItemList items={items} />;
}

// components/item-list.tsx - receives data as props
export function ItemList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

### Actions & Forms (CRITICAL)

#### action-validation - @rules/action-validation.md

Validate form data with zod schemas.

```tsx
// Good: schema validation with i18n error messages
export async function action({ request }: Route.ActionArgs) {
  let t = await i18n.getFixedT(request);
  let formData = await request.formData();

  try {
    const { amount } = z
      .object({
        amount: z.coerce
          .number()
          .min(
            minimumAmount,
            t("Amount must be at least {{min}}.", { min: minimumAmount }),
          ),
      })
      .parse({ amount: formData.get("amount") });

    await processAmount(amount);
    throw redirect("/success");
  } catch (error) {
    if (error instanceof z.ZodError) {
      return data(
        { errors: error.issues.map(({ message }) => message) },
        { status: 400 },
      );
    }
    throw error;
  }
}
```

#### action-error-handling - @rules/action-error-handling.md

Return validation errors, don't throw. Re-throw redirects and unknown errors.

```tsx
// Good: proper error handling
export async function action({ request }: Route.ActionArgs) {
  try {
    // ... validation and mutation
    throw redirect("/success");
  } catch (error) {
    if (error instanceof z.ZodError) {
      return data(
        { errors: error.issues.map(({ message }) => message) },
        { status: 400 },
      );
    }
    if (error instanceof Error) {
      return data({ errors: [error.message] }, { status: 400 });
    }
    throw error; // Re-throw redirects and unknown errors
  }
}
```

#### action-redirect-after - @rules/action-redirect-after.md

Redirect after successful mutations to prevent resubmission.

```tsx
// Good: redirect after mutation
export async function action({ request }: Route.ActionArgs) {
  await createItem(formData);
  throw redirect("/items"); // Use throw for redirect
}
```

#### action-zod-transform - @rules/action-zod-transform.md

Use Zod .transform() for input sanitization during validation.

```tsx
const schema = z.object({
  // Trim and lowercase email
  email: z.string().trim().toLowerCase().pipe(z.string().email()),

  // Parse currency string to number
  amount: z
    .string()
    .transform((val) => parseFloat(val.replace(/[,$]/g, "")))
    .pipe(z.number().positive()),

  // Convert checkbox to boolean
  subscribe: z
    .string()
    .optional()
    .transform((val) => val === "on"),
});
```

#### action-client-validation - @rules/action-client-validation.md

Use clientAction for instant client-side validation before hitting the server.

```tsx
export async function clientAction({
  request,
  serverAction,
}: Route.ClientActionArgs) {
  let formData = await request.formData();
  let result = schema.safeParse(Object.fromEntries(formData));

  if (!result.success) {
    return data(
      { errors: result.error.flatten().fieldErrors },
      { status: 400 },
    );
  }

  return serverAction<typeof action>(); // Validation passed, call server
}
```

### Form Patterns (MEDIUM)

#### form-fetcher-vs-form - @rules/form-fetcher-vs-form.md

Use useFetcher for non-navigation mutations, Form for navigation.

```tsx
// Good: useFetcher for in-place updates (no navigation)
function LikeButton({ postId }: { postId: string }) {
  let fetcher = useFetcher();
  return (
    <fetcher.Form method="post" action="/api/like">
      <input type="hidden" name="postId" value={postId} />
      <button type="submit">Like</button>
    </fetcher.Form>
  );
}

// Good: Form for navigation after submit
function CreatePostForm() {
  return (
    <Form method="post" action="/posts/new">
      <input name="title" />
      <button type="submit">Create</button>
    </Form>
  );
}
```

#### form-pending-state - @rules/form-pending-state.md

Show loading states with useNavigation or fetcher.state.

```tsx
// Good: pending state with fetcher
function SubmitButton() {
  let fetcher = useFetcher();
  let isPending = fetcher.state !== "idle";

  return (
    <Button type="submit" isDisabled={isPending}>
      {isPending ? <Spinner /> : "Submit"}
    </Button>
  );
}

// Good: with useSpinDelay to avoid flicker
const isPending = useSpinDelay(fetcher.state !== "idle", { delay: 50 });
```

#### form-reset-on-success - @rules/form-reset-on-success.md

Reset uncontrolled form inputs after successful submission.

```tsx
const formRef = useRef<HTMLFormElement>(null);
const fetcher = useFetcher<typeof action>();

useEffect(
  function resetFormOnSuccess() {
    if (fetcher.state === "idle" && fetcher.data?.ok) {
      formRef.current?.reset();
    }
  },
  [fetcher.state, fetcher.data],
);

return (
  <fetcher.Form method="post" ref={formRef}>
    ...
  </fetcher.Form>
);
```

#### form-persist-on-error - @rules/form-persist-on-error.md

Return field values from actions on validation errors to repopulate inputs.

```tsx
// Action returns fields on error
export async function action({ request }: Route.ActionArgs) {
  let formData = await request.formData();
  let fields = { email: formData.get("email")?.toString() ?? "" };
  let result = schema.safeParse(fields);

  if (!result.success) {
    return data(
      { errors: result.error.flatten().fieldErrors, fields },
      { status: 400 },
    );
  }
  // ...
}

// Component uses defaultValue
<input name="email" defaultValue={actionData?.fields?.email} />;
```

### Client Functions (MEDIUM)

#### clientloader-debounce - @rules/clientloader-debounce.md

Use clientLoader/clientAction to debounce at the route level.

```tsx
import { setTimeout } from "node:timers/promises";

export async function clientLoader({
  request,
  serverLoader,
}: Route.ClientLoaderArgs) {
  // Debounce by 500ms - request.signal aborts if called again
  return await setTimeout(500, serverLoader, { signal: request.signal });
}

clientLoader.hydrate = true;
```

### Migrations (HIGH)

#### migrate-defer-to-data - @rules/migrate-defer-to-data.md

Migrate from defer() to data() with promises for Single Fetch.

```tsx
// Bad: old defer pattern
import { defer } from "react-router";

export async function loader({ request }: Route.LoaderArgs) {
  return defer({
    critical: await getCriticalData(),
    lazy: getLazyData(), // Promise
  });
}

// Good: Single Fetch with data() - promises auto-stream
import { data } from "react-router";

export async function loader({ request }: Route.LoaderArgs) {
  return data({
    critical: await getCriticalData(),
    lazy: getLazyData(), // Promise automatically streamed
  });
}
```

### Streaming (CRITICAL)

#### streaming-await-suspense - @rules/streaming-await-suspense.md

Use Await with Suspense for streamed data.

```tsx
// Good: Await with Suspense fallback
import { Await, useLoaderData } from "react-router";
import { Suspense } from "react";

export default function Component() {
  const { critical, lazy } = useLoaderData<typeof loader>();

  return (
    <div>
      <div>{critical.name}</div>
      <Suspense fallback={<Skeleton />}>
        <Await resolve={lazy}>{(data) => <LazyContent data={data} />}</Await>
      </Suspense>
    </div>
  );
}
```

#### migrate-jsonhash-to-native - @rules/migrate-jsonhash-to-native.md

Stop using jsonHash, use native Promise.all or data() patterns.

```tsx
// Bad: jsonHash from remix-utils
import { jsonHash } from "remix-utils/json-hash";

export async function loader({ request }: Route.LoaderArgs) {
  return jsonHash({
    a: getDataA(),
    b: getDataB(),
  });
}

// Good: native Promise.all
export async function loader({ request }: Route.LoaderArgs) {
  const [a, b] = await Promise.all([getDataA(), getDataB()]);
  return data({ a, b });
}

// Good: data() with promises for streaming
import { data } from "react-router";

export async function loader({ request }: Route.LoaderArgs) {
  return data({
    a: getDataA(), // Streams automatically
    b: getDataB(),
  });
}
```

#### migrate-json-to-data - @rules/migrate-json-to-data.md

Migrate from deprecated json() to data().

```tsx
// Bad: json() is deprecated
import { json } from "react-router";

export async function loader({ request }: Route.LoaderArgs) {
  let items = await getItems();
  return json({ items });
}

// Good: use data() for all responses
import { data } from "react-router";

export async function loader({ request }: Route.LoaderArgs) {
  let items = await getItems();
  return data({ items });
}

// With status codes
return data({ errors: ["Invalid"] }, { status: 400 });

// Throwing errors
throw data({ message: "Not found" }, { status: 404 });
```

#### migrate-namedaction-to-intent - @rules/migrate-namedaction-to-intent.md

Migrate from namedAction helper to z.discriminatedUnion pattern.

```tsx
// Bad: namedAction from remix-utils
import { namedAction } from "remix-utils/named-action";

export async function action({ request }: Route.ActionArgs) {
  let formData = await request.formData();

  return namedAction(formData, {
    async create() {
      return data({ success: true });
    },
    async delete() {
      return data({ success: true });
    },
  });
}

// Good: z.discriminatedUnion for type-safe intent validation
export async function action({ request }: Route.ActionArgs) {
  let formData = await request.formData();

  let body = z
    .discriminatedUnion("intent", [
      z.object({ intent: z.literal("create"), title: z.string() }),
      z.object({ intent: z.literal("delete"), id: z.string() }),
    ])
    .parse(Object.fromEntries(formData.entries()));

  if (body.intent === "create") {
    await createItem(client, body);
    throw redirect("/items");
  }

  if (body.intent === "delete") {
    await deleteItem(client, body.id);
    throw redirect("/items");
  }
}
```

### Error Handling (MEDIUM)

#### error-boundary-layout - @rules/error-boundary-layout.md

Implement layout-aware ErrorBoundary with useRouteError.

```tsx
import { useRouteError, isRouteErrorResponse } from "react-router";

export function ErrorBoundary() {
  let error = useRouteError();

  if (isRouteErrorResponse(error)) {
    return (
      <div>
        <h1>
          {error.status} {error.statusText}
        </h1>
        <p>{error.data}</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Error</h1>
      <p>{error instanceof Error ? error.message : "Unknown error"}</p>
    </div>
  );
}
```

#### error-boundary-route - @rules/error-boundary-route.md

Add ErrorBoundary to routes with data fetching to catch loader/action errors.

```tsx
// Good: route with error boundary
export async function loader() {
  // May throw
}

export default function Component() {
  // Main component
}

export function ErrorBoundary() {
  // Catches loader errors
}
```

### Navigation & Linking (MEDIUM)

#### link-prefetch-intent - @rules/link-prefetch-intent.md

Use prefetch="intent" for faster navigation on hover/focus.

```tsx
// Good: prefetch on intent
import { Link } from "react-router";

<Link to="/dashboard" prefetch="intent">
  Dashboard
</Link>

// Also applies to LinkButton component
<LinkButton to="/settings" prefetch="intent">
  Settings
</LinkButton>
```

#### navigation-avoid-navigate-back - @rules/navigation-avoid-navigate-back.md

Avoid `navigate(-1)` for in-app back links.

```tsx
<Link to={`/items/${id}`} state={{ back: location.pathname }}>
  View
</Link>
```

#### prefetch-fetcher-data - @rules/prefetch-fetcher-data.md

Use PrefetchPageLinks to preload data for fetcher.load() calls.

```tsx
import { useFetcher, PrefetchPageLinks } from "react-router";

function ItemDetails({ itemId }: { itemId: string }) {
  let fetcher = useFetcher<typeof resourceLoader>();

  return (
    <>
      <PrefetchPageLinks page={`/api/items/${itemId}`} />
      <button onClick={() => fetcher.load(`/api/items/${itemId}`)}>
        View Details
      </button>
      {fetcher.data && <Modal data={fetcher.data} />}
    </>
  );
}
```

### Resource Routes & Responses (MEDIUM)

#### response-helpers - @rules/response-helpers.md

Use response helpers for resource routes.

```ts
return html("<h1>Hello</h1>");
```

#### sse-event-stream - @rules/sse-event-stream.md

Stream updates with `eventStream` and `useEventSource`.

```ts
return eventStream(request.signal, (send) => {
  send({ event: "time", data: new Date().toISOString() });
});
```

#### prefetch-cache - @rules/prefetch-cache.md

Use short caching for prefetch requests.

```ts
if (isPrefetch(request)) headers.set("Cache-Control", "private, max-age=5");
```

### Route Organization (MEDIUM)

#### route-organization - @rules/route-organization.md

Use folder routes with colocated files.

```
routes/
  _.projects/
    queries.server.ts    # Data fetching functions
    actions.server.ts    # Action handlers (optional)
    route.tsx            # Loader, action, component
    components/          # Route-specific components
      header.tsx
      project-card.tsx
```

#### route-resource-routes - @rules/route-resource-routes.md

Use resource routes for API-like endpoints without UI.

```tsx
// routes/api.search.tsx - resource route (no default export)
export async function loader({ request }: Route.LoaderArgs) {
  let url = new URL(request.url);
  let query = url.searchParams.get("q");
  let results = await search(query);
  return data({ results });
}

// No default export = resource route
```

#### route-action-routes - @rules/route-action-routes.md

Centralize reusable actions in dedicated resource routes using `actions.noun-verb.ts` naming.

```tsx
// routes/actions.post-create.ts
import { data, redirect } from "react-router";

export async function action({ request, context }: Route.ActionArgs) {
  let client = await authenticate(request, { context });
  // validation, create post...
  return data({ ok: true, post }, { status: 201 });
}

export async function clientAction({ serverAction }: Route.ClientActionArgs) {
  let result = await serverAction<typeof action>();
  if (result.ok) {
    toast.success("Post created");
    return redirect(`/posts/${result.post.id}`);
  }
  toast.error("Failed to create post");
  return result;
}

// Usage: <fetcher.Form method="post" action="/actions/post-create">
```

#### route-should-revalidate - @rules/route-should-revalidate.md

Optimize revalidation with shouldRevalidate.

```tsx
// Good: prevent unnecessary revalidation
export function shouldRevalidate({
  currentUrl,
  nextUrl,
  formAction,
  defaultShouldRevalidate,
}) {
  // Don't revalidate if only hash changed
  if (currentUrl.pathname === nextUrl.pathname) {
    return false;
  }
  return defaultShouldRevalidate;
}
```

#### route-handle-metadata - @rules/route-handle-metadata.md

Use handle export with app-defined handle types for route metadata.

```tsx
// Good: handle for hydration and layout control
export const handle: Handle = {
  hydrate: true,
};

// For layout routes with more options
export const handle: LayoutHandle = {
  hydrate: true,
  stickyHeader: true,
  footerType: "app",
};
```

### Meta & SEO (MEDIUM)

#### meta-function-v2 - @rules/meta-function-v2.md

Use meta function with loader data for dynamic SEO.

```tsx
export const meta: Route.MetaFunction<typeof loader> = ({ data }) => {
  if (!data) return [];

  return [
    { title: data.title },
    { name: "description", content: data.description },
    { property: "og:title", content: data.title },
    { property: "og:description", content: data.description },
    { property: "og:image", content: data.image },
  ];
};

// Or return from loader for centralized SEO logic
export async function loader({ request }: Route.LoaderArgs) {
  let t = await i18n.getFixedT(request);
  return data({
    // ... data
    meta: seo(t, {
      title: t("Page Title"),
      description: t("Page description"),
      og: { title: t("OG Title"), image: "/og-image.png" },
    }),
  });
}

export const meta: Route.MetaFunction<typeof loader> = ({ data }) =>
  data?.meta ?? [];
```

### Route Conventions (MEDIUM)

#### route-component-naming - @rules/route-component-naming.md

Name the default export `Component` in route files.

```tsx
// app/routes/_.users/route.tsx
export async function loader() { ... }
export async function action() { ... }

// Always name "Component"
export default function Component() {
  let { users } = useLoaderData<typeof loader>();
  return <UserList users={users} />;
}
```

#### route-import-restrictions - @rules/route-import-restrictions.md

Avoid importing from other route files. Routes import shared modules, not each other.

```tsx
// Bad: importing from another route
import { UserCard } from "~/routes/users/components/user-card";

// Good: import from shared location
import { UserCard } from "~/components/user-card";

// Exception: import loader/action types for useFetcher inference
import type { action } from "~/routes/api.orders/route";
let fetcher = useFetcher<typeof action>();
```

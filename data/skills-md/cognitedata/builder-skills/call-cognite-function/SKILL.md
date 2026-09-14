---
name: call-cognite-function
description: "Call a deployed Cognite CDF Function and retrieve its response, with Zod-validated API responses and an optional React Query hook. Use this skill whenever you need to invoke any CDF Function (by numeric function ID or external ID), pass arbitrary input data, and get a typed, validated result back — regardless of what the function does, the function has an outpt, or what shape its input/output takes. Triggers: call cognite function, invoke CDF function, run CDF function, poll CDF function, CDF Functions API, cognite function result, function call nonce."
---

# Call Cognite Function

Invoke any deployed Cognite CDF Function, poll until it completes, and return a typed, schema-validated result.

## Overview

The CDF Functions API uses a three-step protocol:
1. **Session nonce** — exchange the current user token for a short-lived nonce so the function can make authenticated API calls on the user's behalf.
2. **Invoke** — POST to the function's `/call` endpoint with your input data and the nonce.
3. **Poll → fetch** — GET the call status in a loop; once `"Completed"`, GET the `/response` endpoint.

Every API response is validated with **Zod**, so schema drift surfaces as a clear `ZodError` at the call site instead of an `undefined` three layers down. The function's own output payload can also be validated against a caller-supplied schema — which doubles as the source of the return type.

## Files

| File | Purpose |
|------|---------|
| `code/cogniteFunctionService.ts` | Framework-agnostic async function with Zod validation. Zero React deps. Copy into `src/services/`. |
| `code/useCogniteFunction.ts` | React Query (`useMutation`) hook wrapping the service. Copy into `src/hooks/`. |

**Dependencies:** `@cognite/sdk` (already present in Flows/Fusion apps) and `zod`. The hook additionally needs `@tanstack/react-query` and a `<QueryClientProvider>` in the tree.

## How to use

### 1. Copy the service file

```ts
callCogniteFunction<TOutput>(
  client: CogniteClient,
  functionId: string | number,
  data: unknown,
  opts?: CallCogniteFunctionOptions<TOutput>,
): Promise<TOutput>
```

- `functionId` — numeric CDF function ID (or its string form). NOT an external ID; resolve those first (see below).
- `data` — any JSON-serialisable object; the function receives it as its `data` argument.
- `opts.outputSchema` — **the recommended way to type the result.** A Zod schema for the function's response payload; the return type is inferred from it and the payload is validated at runtime. Omit it and you get `unknown` back (then narrow it yourself).
- `opts.maxPollAttempts` — default 120 (~6 min at 3 s). Increase for long-running batch jobs.
- `opts.pollIntervalMs` — default 3000, with ±20 % jitter to avoid thundering-herd across tabs.
- `opts.signal` — `AbortSignal` for cancellation (non-React contexts; the hook doesn't need it).

### 2. Define the output schema, not interfaces

```ts
import { z } from "zod";

const ReportOutput = z.object({
  success: z.boolean(),
  report: z.string(),
  error: z.string().optional(),
});

const result = await callCogniteFunction(client, 12345678, 
  { reportId: "abc", language: "en" },
  { outputSchema: ReportOutput },
);
// result: { success: boolean; report: string; error?: string } — validated
```

One schema gives you the TypeScript type *and* the runtime guarantee. Don't hand-write a parallel `interface`.

### 3. Handle errors

There is no custom error class — errors propagate as-is so you keep the full original context:

- **SDK HTTP errors** from `@cognite/sdk` (auth, 4xx/5xx, throttling) — untouched.
- **`ZodError`** when an API response or the function's payload doesn't match its schema.
- **Plain `Error`** when the call ends with status `Failed`/`Timeout` (includes the function's own error message) or polling is exhausted. The message always includes the function ID and call ID.

Catch at whatever level makes sense; in the React hook, React Query surfaces the message via `error`.

### 4. (React) Use the hook

The hook wraps the service in a React Query `useMutation`. Mutation semantics are deliberate: function calls are not idempotent (each one spins a new execution and counts against the 100-concurrent limit), so you never want refetch-on-focus or remount-refetch. React Query also owns loading/error/result state and unmount safety — no `AbortController` plumbing needed.

```tsx
const { call, isLoading, error, result, reset } = useCogniteFunction<
  MyInput,
  z.infer<typeof ReportOutput>
>(12345678, { outputSchema: ReportOutput });

// trigger on button click:
await call({ reportId: "abc", language: "en" });
```

Adjust the `useCdfClient` import to however your project exposes the SDK.

Note on generics: TypeScript has no partial inference, so specify **both** type params or **neither**. `useCogniteFunction<MyInput>` alone silently makes `result` `unknown` even with an `outputSchema` — if you don't care about typing the input, omit the generics entirely and let `outputSchema` drive the result type.

**Read-like functions:** if a specific function is a pure read (same input → same output) and you want caching/deduping, skip the hook and wrap the service in `useQuery` directly:

```ts
useQuery({
  queryKey: ["cdf-fn", functionId, input],
  queryFn: () => callCogniteFunction(sdk, functionId, input, { outputSchema }),
  staleTime: 5 * 60_000,
});
```

## Finding the function ID

If you only know the function's **external ID**, resolve it first (same Zod pattern):

```ts
const Functions = z.object({
  items: z.array(z.object({ id: z.number(), externalId: z.string().optional() })),
});

const res = await client.get(`/api/v1/projects/${client.project}/functions`);
const fn = Functions.parse(res.data).items.find(
  (f) => f.externalId === "My_Function_ExternalId",
);
if (!fn) throw new Error("Function My_Function_ExternalId not found");
```

## Polling behaviour

Unknown statuses returned by the API are treated as "still running" and polled through (only `Failed`/`Timeout` terminate with an error, `Completed` terminates with the result). This keeps the client forward-compatible if CDF adds new intermediate statuses.

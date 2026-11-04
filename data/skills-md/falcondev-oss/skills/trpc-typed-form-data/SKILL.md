---
name: trpc-typed-form-data
description: >
  Type-safe file uploads through tRPC with @falcondev-oss/trpc-typed-form-data.
  Use when uploading files / FormData through a tRPC procedure, or working with
  typedFormData(), createTypedFormData(), typedFormDataLink,
  createTypedFormDataPlugin, the file() validator / FileValue type (a stable
  alternative to z.file()), or ReactNativeFile / Expo file uploads over tRPC.
---

# @falcondev-oss/trpc-typed-form-data

tRPC can't type a `FormData` input: files must ride as multipart parts, everything else is untyped strings, and `input` arrives `undefined`. This package restores end-to-end type safety by carrying the non-file fields as a **serialized sidecar** — a JSON blob in one extra FormData field (`~data`) — while files stay as real multipart parts. Client, server, and schema each handle one half of that trick.

Four entry points:

| Import from | Gives you |
|---|---|
| `.../client` | `createTypedFormData`, `typedFormDataLink`, `ReactNativeFile` |
| `.../server` | `typedFormData`, `createTypedFormDataPlugin` |
| `.../zod` | zod-native `file()` validator (nest in `z.object`) |
| `.` (root) | `file` (Standard Schema), `isFile`, types — the framework-agnostic subset |

`file`, `isFile`, and the types (`FileValue`, `FileValidationOptions`, `TypedFormData`) are re-exported from `/client` and `/server` too, so import them from wherever you already are.

## Three touch points — all required

The sidecar only works if every piece is wired. Miss one and validation throws a message naming what's missing.

**1. Client link** — serializes the sidecar into the FormData. Place it *before* the terminating link:

```ts
import { typedFormDataLink } from '@falcondev-oss/trpc-typed-form-data/client'
import { createTRPCClient, httpLink } from '@trpc/client'

const trpc = createTRPCClient<AppRouter>({
  links: [
    typedFormDataLink(), // 👈 before httpLink
    httpLink({ url: '/api/trpc' }),
  ],
})
```

**2. Server middleware** — deserializes the sidecar back onto the FormData. Build the plugin from your tRPC instance and `concat` its middleware onto the procedures that accept uploads:

```ts
import { createTypedFormDataPlugin } from '@falcondev-oss/trpc-typed-form-data/server'

const t = initTRPC.create()
const typedFormDataPlugin = createTypedFormDataPlugin(t)

export const uploadProcedure = t.procedure.concat(typedFormDataPlugin.middleware)
```

**3. Input schema wrapper** — wrap the input schema in `typedFormData()`. It reads the sidecar + the file parts and validates them together:

```ts
import { typedFormData } from '@falcondev-oss/trpc-typed-form-data/server'
import { z } from 'zod'

export const router = t.router({
  upload: uploadProcedure
    .input(
      typedFormData(
        z.object({
          userId: z.string(),
          file: z.instanceof(File),
        }),
      ),
    )
    .mutation(({ input }) => {
      // input is fully typed: { userId: string; file: File }
    }),
})
```

**Calling it** — build the payload with `createTypedFormData` and pass it straight to `.mutate()`; the fields are type-checked against the schema:

```ts
import { createTypedFormData } from '@falcondev-oss/trpc-typed-form-data/client'

await trpc.upload.mutate(
  createTypedFormData({
    userId: '123',
    file: new File(['contents'], 'example.txt'),
  }),
)
```

Arrays of files work: pass `File[]` under a key — each file is appended under that key and read back with `getAll`.

## File validation — prefer `file()` over `z.file()`

Reach for this package's `file()` when the schema is shared with a React Native / Expo client. `z.file()`'s inferred type degrades to `any` in environments without a DOM `File` (React Native), silently dropping type-checking across the tRPC server→client boundary. `file()` infers a stable `FileValue` — a structural subset of the Web `File`/`Blob` API (`name`, `size`, `type`, `arrayBuffer`, `stream`, `slice`, `text`) — everywhere.

Two flavours, same options (`{ maxSize?, minSize?, mimeTypes? }`, all optional, byte limits inclusive):

```ts
// zod stack — nests inside z.object like z.file()
import { file } from '@falcondev-oss/trpc-typed-form-data/zod'
typedFormData(z.object({
  avatar: file({ maxSize: 10_000_000, mimeTypes: ['image/png', 'image/jpeg'] }),
}))

// non-zod / any Standard Schema stack
import { file } from '@falcondev-oss/trpc-typed-form-data/server'
```

`isFile(value)` is a type guard narrowing `unknown` → `FileValue` for ad-hoc checks outside a schema. Annotate values that came out of these schemas (a procedure `input`, an upload helper) with `FileValue`, not `File`.

## Gotchas

- **All three touch points, or nothing.** Missing the link, the middleware, or the wrapper each produces a distinct validation error — read the message, it names the missing piece.
- **Transformer must match.** If your router uses a transformer (e.g. superjson), pass it to `typedFormDataLink({ transformer })` — the sidecar is serialized with the link's transformer and deserialized with the router's. A mismatch throws `BAD_REQUEST` on the server.
- **Custom transfer field.** The sidecar rides in a `~data` field by default. Override with `transferDataKey` — set the *same* value on both `typedFormDataLink({ transferDataKey })` and `createTypedFormDataPlugin(t, { transferDataKey })`.
- **FormData isn't batchable.** Terminate with `httpLink`, not `httpBatchLink`, on the upload path.
- **Middleware only fires for mutations** with no plain `input` (the FormData path). Queries and subscriptions pass through untouched.

## React Native / Expo

Uploading from an image/document picker needs `ReactNativeFile` — RN's `FormData` only sends parts with a `uri` and never reads a Blob's bytes. Read `reference/react-native.md` before wiring an Expo upload.

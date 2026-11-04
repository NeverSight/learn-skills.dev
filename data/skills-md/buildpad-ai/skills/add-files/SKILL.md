---
name: add-files
description: Scaffold the Buildpad Files module — a ready-made /files library (FileManager) and /files/[id] detail view (FileDetail) with drag-and-drop upload, import-from-URL, folders, grid/list views, preview, metadata editing, and bulk delete. Backed by the useFiles/useFolders hooks and asset thumbnails. Use when the user says add files, file manager, file library, files module, uploads page, or wants a document/media library.
argument-hint: "[--cwd path/to/project]"
---

# Add the Files Module

<!-- backend-gate:begin v1 -->
**Establish the backend first.** A Buildpad project's backend is either the Buildpad Engine or
Supabase, and some parts of this file hold for one of them only. Before you act on anything in
this file, find the backend with these steps, in order, and stop at the first step that answers:

1. Read `.buildpad/project.json` at the project root. If it is JSON and its field `backend` is
   `"engine"` or `"supabase"`, that is the backend. If `.buildpad/backend-answer.json` names the
   other backend, tell the developer the two files disagree, and follow `.buildpad/project.json`.
2. Otherwise read `.buildpad/backend-answer.json` in the same way; if its `backend` is
   `"engine"` or `"supabase"`, that is the backend.
3. If a folder named `supabase` at the project root holds a file named `config.toml`, or holds a
   folder named `migrations` that holds a file whose name ends in `.sql`, the backend is Supabase.
4. Otherwise ask the developer once: "Is this project's backend the Buildpad Engine or
   Supabase?" Write the answer to `.buildpad/backend-answer.json` as
   `{"buildpadBackendAnswer": 1, "backend": "engine"}` or
   `{"buildpadBackendAnswer": 1, "backend": "supabase"}`, and ask the developer to commit that
   file. Do not add it to `.gitignore`. Never write `.buildpad/project.json`.

To find the backend, do not open an environment file (`.env`, `.env.*`) or an MCP configuration
file, and do not call a tool that returns project credentials.

Then follow only the parts for that backend. A part starts at a line that holds only a comment
whose text is `buildpad` + `-backend: engine` or `buildpad` + `-backend: supabase`, and ends at the
next line that holds only a comment whose text is `/buildpad` + `-backend`. A comment that merely
mentions a backend is not a part. A file whose first line, after any front matter, holds only a
comment whose text is `buildpad` + `-backend-file: engine` (or `supabase`) holds for that backend
only, and so does every file in a folder named `engine-only` or `supabase-only`. Skip the other
backend's parts and copy no code from them; everything else holds for both. On an Engine project, when this file says that
something is not available, tell the developer so and stop: do not build a substitute.
<!-- backend-gate:end -->

A ready-made `/files` experience installed via the Buildpad CLI (Copy & Own — the code is copied into your project). It sits on top of the DaaS Files API and the `Upload` interface, so you never hand-build upload zones, folder navigation, previews, or bulk actions.

Two screens ship together:

- **`FileManager`** — the `/files` library: drag-and-drop upload, import-from-URL, folder navigation with breadcrumbs, grid/list views, search, multi-select, bulk delete.
- **`FileDetail`** — the `/files/[id]` page: a **Preview** tab (image/video/audio inline, PDF in an iframe) and a **Details** tab with an editable metadata form, plus single delete.

## CRITICAL: Never Create These Manually

Like all Buildpad UI, the Files module is CLI-installed and owned as source. Do **not** hand-write `components/ui/file-manager/*`, the `upload` component, or the `useFiles`/`useFolders` hooks in `lib/buildpad/hooks/` — scaffold them.

## Prerequisites Check

```bash
node --version && pnpm --version && npx --version
```

<!-- buildpad-backend: supabase -->
Requires Node.js v24 LTS and pnpm v10+ (see [add-buildpad](../add-buildpad/SKILL.md) for install guidance). The module **must** render under the authenticated layout (`buildpad init` generates `app/(authenticated)/` with a `DaaSProviderWrapper`) so `DaaSProvider` header injection is in scope — the hooks call your `/api/files/*`, `/api/folders/*`, and `/api/assets/*` proxy routes. Inside the module use `useDaaSContext` (it throws when mounted outside the wrapper, which surfaces the layout mistake early); `useDaaSContextOptional` exists for components that must also render without a provider.

**DaaS CORS must be configured first.** `FileManager`/`FileDetail` fetch authenticated DaaS endpoints (`/users/me`, `/permissions/me`, file/folder items) from the browser with `credentials: 'include'`. DaaS's default `cors_origins: ["*"]` is **incompatible** with credentialed requests — the browser blocks every preflight (`Access-Control-Allow-Origin header must not be the wildcard '*'`). Set explicit origins before mounting the module (see [daas-platform](../daas-platform/SKILL.md) "CORS must use explicit origins" — Bugs 17+25 — and [debugging-and-error-recovery](../debugging-and-error-recovery/SKILL.md)). This is not Files-specific: it affects every authenticated Buildpad component.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Requires Node.js v24 LTS and pnpm v10+ (see [add-buildpad](../add-buildpad/SKILL.md) for install guidance). The module **must** render under the authenticated layout (`buildpad init` generates `app/(authenticated)/` with a `DaaSProviderWrapper`) so `DaaSProvider` header injection is in scope — the hooks call your `/api/files/*` and `/api/folders/*` proxy routes, which forward the signed-in user's access token to the Engine. Inside the module use `useDaaSContext` (it throws when mounted outside the wrapper, which surfaces the layout mistake early); `useDaaSContextOptional` exists for components that must also render without a provider.

On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it.

**Leave the cross-origin settings as they are.** On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere. The module's calls carry the user's access token as `Authorization: Bearer`, never a cookie, so nothing needs configuring before you mount it.
<!-- /buildpad-backend -->

## Installation

The Files module is **opt-in** — it is not part of `bootstrap`.

```bash
# 1. Add the module (copies app/files/ shells, components/ui/file-manager/,
#    the upload component, and the useFiles/useFolders hooks)
npx @buildpad/cli@latest add files-routes --cwd /path/to/project

# 2. Add the DaaS proxy routes it needs (if not already present)
npx @buildpad/cli@latest add api-routes --cwd /path/to/project
```

> The docs use the shorthand `buildpad add files-routes` when the CLI is installed globally; `npx @buildpad/cli@latest add …` is the equivalent no-install form used across these skills.

> **If the CLI command fails, `@buildpad/cli` IS published to npm** — verify with `npm view @buildpad/cli version` before assuming otherwise or reaching for a local clone. The CLI fetches its registry from `raw.githubusercontent.com`, so confirm the environment can reach **both** npm and the GitHub raw CDN. A local clone is only needed for CLI development, never to consume components.

<!-- buildpad-backend: supabase -->
`api-routes` includes exactly the routes this module needs: `app/api/files/route.ts`, `app/api/files/[id]/route.ts`, `app/api/files/[id]/download/route.ts`, `app/api/files/import/route.ts`, `app/api/folders/route.ts`, `app/api/folders/[id]/route.ts`, and `app/api/assets/[id]/route.ts`. Each one is a thin proxy that forwards the request and the session's `Authorization` header to DaaS — none of them talks to Supabase Storage or `daas_files` directly. CLI releases that ship the direct-to-storage upload add one more proxy, `app/api/files/signed-url/route.ts` (see below).
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
`api-routes` includes the routes this module needs: `app/api/files/route.ts`, `app/api/files/[id]/route.ts`, `app/api/files/[id]/download/route.ts`, `app/api/files/import/route.ts`, `app/api/folders/route.ts`, `app/api/folders/[id]/route.ts`, and `app/api/assets/[id]/route.ts`. Each one is a thin proxy that forwards the request and the session's `Authorization` header to the Engine_URL — none of them stores a file or writes `daas_files` itself. CLI releases that ship the direct upload add one more proxy, `app/api/files/signed-url/route.ts` (see below). The generated `app/api/assets/[id]/route.ts` forwards to `/api/assets/:id`, a path the Engine does not serve: the Engine serves file content at `/api/files/assets/:id` (see "Thumbnails & downloads").
<!-- /buildpad-backend -->

## How Uploads Work

Uploads go through `useFiles().uploadFiles` — never hand-write the upload flow or the routes behind it.

<!-- buildpad-backend: supabase -->
On CLI releases up to 2.2.0 the hook sends `multipart/form-data` to `POST /api/files`; the proxy forwards it to DaaS, which stores the object in Supabase Storage and creates the `daas_files` record. Both hops buffer the whole body, so uploads are bounded by the request body limit.

DaaS 0.1.93 added a direct-to-storage path for large files. CLI releases that ship `app/api/files/signed-url/route.ts` (a proxy to DaaS `POST`/`DELETE /api/files/signed-url`) use it from `uploadFiles` automatically:

1. `POST /api/files/signed-url` with `{ filename_download, type, filesize, folder? }` — the first three are required, and `folder` must be an existing `daas_folders` id — returns `201 { data: { uploadUrl, token, uploadToken, primaryKey, storagePath, filenameDisk, storageBucket } }`.
2. `PUT uploadUrl` with the raw bytes and `Content-Type: file.type`. This request goes to the Supabase Storage origin, not to your app, so **that host must allow cross-origin `PUT` from the app origin** — otherwise step 1 succeeds and step 2 fails with a CORS error.
3. `POST /api/files` (JSON) with `{ upload_token: uploadToken, filename_download, title?, description? }` returns `201 { data: <file> }`. DaaS takes `id`, `filename_disk`, `storage`, and `folder` from the token and reads `filesize` and `type` back from the stored object — any of those fields sent by the client are ignored.

If step 2 or 3 fails, the hook calls `DELETE /api/files/signed-url` with `{ upload_token }` (`204`) so the object is not orphaned in the bucket. Tokens are bound to the user who requested them, expire after two hours, and are single-use.

Against a DaaS instance older than 0.1.93 (no `/api/files/signed-url`), the hook detects the `404` on the first upload and falls back to multipart for the rest of the session. No configuration is needed either way.

Size and MIME limits come from the Supabase bucket (Supabase Studio → bucket settings), falling back to the DaaS env vars `FILES_MAX_UPLOAD_SIZE` (default 100 MB) and `FILES_MIME_TYPE_ALLOW_LIST` (default: all types). `FILES_STORAGE_BUCKET_ALLOW_LIST` limits which buckets a signed upload may target (default `files`).

**Never insert into `daas_files` directly, and never mint signed URLs from the app.** Bypassing DaaS skips its permission, size, type, bucket, and ownership checks, and the column default `storage = 'local'` names a bucket that does not exist — every later `/api/assets/:id` call then fails with `FILE_NOT_FOUND` ("Failed to retrieve file"). Through DaaS, `storage` comes from the upload token and defaults to the `files` bucket.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
On an Engine project files are stored and served by the Engine: `/api/files`, `/api/folders`, `/api/files/signed-url`, and file content at `/api/files/assets/:id` (with a session or a signed token). A file shown in a browser, a public one included, is loaded through a signed URL from `/api/files/signed-url`, not by an anonymous read: an `<img>` element or a link sends no `X-Tenant-Id`. Set no storage bucket option: the Engine stores files on its own disk or in S3.

The hook reaches the Engine through the proxy routes, in one of two ways:

- **Multipart.** `uploadFiles` sends `multipart/form-data` to `POST /api/files`; the proxy forwards it to the Engine, which stores the file and creates the `daas_files` record, and answers `201 { data: <file> }`.
- **Direct upload.** CLI releases that ship `app/api/files/signed-url/route.ts` (a proxy to the Engine's `POST`/`DELETE /api/files/signed-url`) use it from `uploadFiles` automatically:
  1. `POST /api/files/signed-url` with `{ filename_download, type, filesize, folder? }` — the first three are required, and `folder` must be an existing `daas_folders` id — returns `201 { data: { uploadUrl, token, uploadToken, primaryKey, storagePath, filenameDisk, storageBucket } }`.
  2. `PUT uploadUrl` with the raw bytes and `Content-Type: file.type`. When the Engine stores files on its own disk, `uploadUrl` is an address on the Engine itself; when it stores them in S3, it is a pre-signed S3 address.
  3. `POST /api/files` (JSON) with `{ upload_token: uploadToken, filename_download, title?, description? }` returns `201 { data: <file> }`. The Engine takes the id, the stored name, the storage location and the folder from the token and reads the size back from the stored object — those fields sent by the client are ignored.

  If step 2 or 3 fails, the hook calls `DELETE /api/files/signed-url` with `{ upload_token }` (`204`) so the object is not orphaned. Tokens are bound to the user who requested them, expire after two hours, and are single-use.

The upload limit is the Engine's `APP_MAX_UPLOAD_BYTES` (100 MiB by default), which the Engine's operator sets; a larger declared or sent file is refused. There is no MIME allow list: every type is accepted.

**Never insert into `daas_files` directly, and never sign a URL in the app.** Go through the Engine's file routes, which apply the user's permissions, the size limit and the token's ownership.
<!-- /buildpad-backend -->

## The Routes

```
app/files/
├── layout.tsx        # optional shell wrapper (centers content)
├── page.tsx          # /files       — FileManager library view
└── [id]/page.tsx     # /files/[id]  — FileDetail preview + metadata view
```

## Usage

### List view — `FileManager`

```tsx
// app/files/page.tsx
"use client";

import { useRouter } from "next/navigation";
import { FileManager } from "@/components/ui/file-manager";

export default function FilesPage() {
  const router = useRouter();
  return <FileManager onFileClick={(file) => router.push(`/files/${file.id}`)} />;
}
```

| Prop | Type | Default | Purpose |
| ---------------- | ------------------------- | ------------ | ------------------------------------------------- |
| `onFileClick`    | `(file: FileUpload) => void` | —          | Open a file (e.g. navigate to its detail page)    |
| `pageSize`       | `number`                  | `24`         | Items per page                                    |
| `defaultView`    | `'grid' \| 'list'`        | `'grid'`     | Initial view mode                                 |
| `enableFolders`  | `boolean`                 | `true`       | Set `false` for a flat library with no folder UI  |
| `filesCollection`| `string`                  | `'daas_files'` | DaaS collection used for RBAC checks            |

### Detail view — `FileDetail`

```tsx
// app/files/[id]/page.tsx
"use client";

import { use } from "react";
import { useRouter } from "next/navigation";
import { FileDetail } from "@/components/ui/file-manager";

export default function FileDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  return (
    <FileDetail
      id={id}
      onBack={() => router.push("/files")}
      onDeleted={() => router.push("/files")}
    />
  );
}
```

`FileDetail` props: `id` (required), `onBack?`, `onDeleted?`, `filesCollection?` (default `'daas_files'`). Metadata edits, folder moves, focal point, and delete are all permission-gated.

## The Data Layer (reuse anywhere)

Both screens are thin wrappers over two hooks from `@/lib/buildpad/hooks`:

```tsx
import { useFiles, useFolders } from "@/lib/buildpad/hooks";
```

<!-- buildpad-backend: supabase -->
- **`useFiles()`** → `uploadFiles`, `fetchFiles`, `getFile`, `updateFile`, `replaceFile`, `getDownloadUrl`, `deleteFile`, `deleteFiles`, `importFromUrl` (+ `loading`, `error`). `updateFile` takes the full editable metadata set:

  ```tsx
  await updateFile(fileId, {
    title: "Cover image",
    description: "Homepage hero",
    tags: ["marketing", "hero"],
    location: "HQ",
    filename_download: "hero.png",
  });
  ```

- **`useFolders()`** → `fetchFolders`, `createFolder`, `updateFolder`, `deleteFolder` (+ `loading`, `error`). Pass `parent: null` for the root:

  ```tsx
  const rootFolders = await fetchFolders({ parent: null });
  const folder = await createFolder({ name: "Campaigns", parent: null });
  ```

### Thumbnails & downloads

Assets are served by `/api/assets/[id]`. Build transform URLs with `getAssetUrl` from `@/lib/buildpad/types`:

```tsx
import { getAssetUrl } from "@/lib/buildpad/types";

getAssetUrl(id, { width: 240, height: 240, fit: "cover" }); // grid thumbnail
getAssetUrl(id, { download: true });                         // download link
```

Never put a raw DaaS URL (`https://<daas-host>/api/assets/:id`) in an `<img src>`, `<video src>`, `<iframe src>`, or `<a href>`: the browser sends no `Authorization` header, so DaaS answers `401 Unauthorized`. Always go through the app's `/api/assets/[id]` proxy, which attaches the session token — `getAssetUrl` already builds those URLs (`getAssetUrl(id)` for previews, `getAssetUrl(id, { download: true })` for downloads).
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- **`useFiles()`** → `uploadFiles`, `fetchFiles`, `getFile`, `updateFile`, `replaceFile`, `getDownloadUrl`, `deleteFile`, `deleteFiles`, `importFromUrl` (+ `loading`, `error`). `updateFile` takes the full editable metadata set:

  ```tsx
  await updateFile(fileId, {
    title: "Cover image",
    description: "Homepage hero",
    tags: ["marketing", "hero"],
    location: "HQ",
    filename_download: "hero.png",
  });
  ```

- **`useFolders()`** → `fetchFolders`, `createFolder`, `updateFolder`, `deleteFolder` (+ `loading`, `error`). Pass `parent: null` for the root:

  ```tsx
  const rootFolders = await fetchFolders({ parent: null });
  const folder = await createFolder({ name: "Campaigns", parent: null });
  ```

On an Engine project a delete (`deleteFile`, `deleteFiles`, `deleteFolder`) is answered `204` with no body.

### Thumbnails & downloads

The Engine serves file content at `/api/files/assets/:id`, with a session or with a signed token. The CLI's `getAssetUrl` (from `@/lib/buildpad/types`) builds URLs to the app's `/api/assets/[id]` proxy, and the generated proxy forwards them to `/api/assets/:id`, which the Engine does not serve: previews, thumbnails and download links built with `getAssetUrl` do not load on an Engine project. Tell the developer so when they ask for them.

Where the application shows or offers a file itself, its server route asks the Engine for a signed URL — `GET <Engine_URL>/api/files/signed-url?id=<file id>` with the user's `Authorization: Bearer` header — and the page puts that URL in the `<img src>`, `<video src>`, `<iframe src>` or `<a href>`. When the Engine stores files on its own disk the URL is relative (`/api/files/assets/<id>?token=…`): prefix it with the Engine_URL. Never put `/api/files/assets/:id` without its token in such an element: the browser sends no `Authorization` header, and the Engine answers `401`.
<!-- /buildpad-backend -->

## Preview Behaviour (Details tab)

| MIME type | Rendering |
| ------------- | ----------------------- |
| Image         | `<img>` inline          |
| Video         | HTML5 `<video>` player  |
| Audio         | HTML5 `<audio>` player  |
| PDF           | Embedded `<iframe>`     |
| Anything else | Icon + download button  |

## Post-Install Validation

```bash
npx @buildpad/cli@latest status --cwd /path/to/project
npx @buildpad/cli@latest validate --cwd /path/to/project
cd /path/to/project && pnpm build
```

## See It Live

Files Storybook (port 6009): `pnpm --filter @buildpad/ui-files storybook`. The `FileManager (DaaS)` story connects to a real DaaS instance via the storybook-host proxy.

## Related

- [add-buildpad](../add-buildpad/SKILL.md) — the underlying CLI and the low-level `Upload` / `FileInterface` / `FileImage` field widgets.
- [buildpad-reference](../buildpad-reference/SKILL.md) — full component catalog.

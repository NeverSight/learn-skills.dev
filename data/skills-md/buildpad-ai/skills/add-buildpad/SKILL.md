---
name: add-buildpad
description: Add Buildpad UI components to a DaaS project via CLI. Installs Copy & Own components from the registry including input, selection, boolean, datetime, media, rich-text, relations, layout, collection, and workflow components. Use when the user says add-buildpad, install components, or needs Buildpad UI.
argument-hint: "[component names or --all] [--cwd path/to/project]"
---

# Add Buildpad Components

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

Install Buildpad UI components using the CLI. Components are copied as source code to your project (Copy & Own model).

## Prerequisites Check (MANDATORY)

Before running any CLI commands, verify required tools:

```bash
node --version && pnpm --version && npx --version
```

| Tool    | Min Version | Install Guide                                                                                                                                     |
| ------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Node.js | v24 LTS     | https://nodejs.org/en/download — macOS: `brew install node@24`; Linux: `fnm install 24`; Windows: installer or `winget install OpenJS.NodeJS.LTS` |
| pnpm    | v10+        | https://pnpm.io/installation — `corepack enable && corepack prepare pnpm@latest --activate`                                                       |
| npx     | (bundled)   | Comes with Node.js — reinstall Node if missing                                                                                                    |

**If any tool is missing, install it before proceeding.** See [create-project prerequisites](../create-project/references/prerequisites.instructions.md) for detailed OS-specific instructions.

## CRITICAL: Never Create Components Manually

<!-- buildpad-backend: supabase -->
```
❌ NEVER CREATE MANUALLY:
├── components/ui/*.tsx          # ALL UI components — from CLI only
├── lib/buildpad/              # ENTIRE folder — from CLI only
│   ├── services/                # api-request, items, fields, collections
│   ├── hooks/                   # useRelationM2M, useFiles, etc.
│   ├── types/                   # Field, Collection, File types
│   ├── utils/                   # utilities
│   └── ui-form/                 # VForm, FormField components
└── buildpad.json              # Created by CLI init
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```
❌ NEVER CREATE MANUALLY:
├── components/ui/*.tsx          # ALL UI components — from CLI only
├── lib/buildpad/              # ENTIRE folder — from CLI only
│   ├── services/                # api-request, items, fields, collections
│   ├── hooks/                   # useRelationM2M, useFiles, etc.
│   ├── types/                   # Field, Collection, File types
│   ├── utils/                   # utilities
│   └── ui-form/                 # VForm, FormField components
└── buildpad.json              # Created by CLI init
```

The CLI also writes the sign-in layer and the proxy routes (`lib/supabase/`, `middleware.ts`, `lib/api/auth-headers.ts`, `app/api/`). Do not write those by hand either.

On an Engine project some files the Buildpad CLI generates cannot be used yet: `lib/supabase/admin.ts`, the OAuth callback and provider routes of the `external-oauth` module, the server-side enforcer and session modules, and `lib/module-access/enforce.ts`. Do not call them; check module access by forwarding the user's token to `GET <Engine_URL>/api/permissions/me` and reading `isAdmin` and `moduleAccess`. For XAppHub sign-in the CLI installs the `external-oauth-engine` module in place of `external-oauth`; its routes are used as the `add-external-oauth` skill says.
<!-- /buildpad-backend -->

## Installation Commands

<!-- buildpad-backend: supabase -->
```bash
# Via npx (no local clone needed)
npx @buildpad/cli@latest add --all --with-api --cwd /path/to/project

# Individual components
npx @buildpad/cli@latest add input select-dropdown datetime toggle --cwd /path/to/project
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```bash
# Via npx (no local clone needed)
npx @buildpad/cli@latest add --all --with-api --cwd /path/to/project

# Individual components
npx @buildpad/cli@latest add input select-dropdown datetime toggle --cwd /path/to/project
```

`--with-api` (and `--all`) also installs the sign-in layer, the proxy routes and the OAuth routes. On an Engine project the files the note above names are among them: leave them in place, and do not call them. A CLI that installs the `external-oauth-engine` module there in place of `external-oauth` (check `installedLib` in `buildpad.json`) writes OAuth routes for XAppHub sign-in, which are used as the [add-external-oauth](../add-external-oauth/SKILL.md) skill says.
<!-- /buildpad-backend -->

## Component Categories

| Category        | Components                                                                                                                                                                |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Input**       | input, textarea, input-code, input-block-editor, tags, map, map-with-real-map                                                                                             |
| **Selection**   | select-dropdown, select-radio, select-multiple-checkbox, select-multiple-checkbox-tree, select-multiple-dropdown, autocomplete-api, collection-item-dropdown, select-icon |
| **Boolean**     | boolean, toggle                                                                                                                                                           |
| **DateTime**    | datetime                                                                                                                                                                  |
| **Media**       | file, file-image, files, upload, color                                                                                                                                    |
| **Rich-text**   | rich-text-html, rich-text-markdown                                                                                                                                        |
| **Relations**   | list-m2m, list-m2o, list-o2m, list-m2a                                                                                                                                    |
| **Layout**      | divider, notice, group-detail, slider                                                                                                                                     |
| **Collections** | vform, collection-form, vtable, collection-list, filter-panel, content-navigation, content-layout, save-options                                                           |
| **Workflow**    | workflow-button                                                                                                                                                           |
| **Modules**     | `files-routes` (+ file-manager), `form-builder` `forms-routes` — full multi-screen experiences, scaffolded whole (see below)                                              |

## Opt-in Modules (whole experiences)

Beyond individual components, ready-made modules install their own page shells, components, and hooks in one command. Use the dedicated skills — do not compose these by hand:

```bash
# Files library — /files (FileManager) + /files/[id] (FileDetail)
npx @buildpad/cli@latest add files-routes --cwd /path/to/project        # → /add-files

# Dynamic Form Builder — /forms author + fill (FormBuilder + DynamicForm)
npx @buildpad/cli@latest add form-builder forms-routes --cwd /path/to/project  # → /create-form-builder

# Workflows admin — /workflows (diagram editor), /workflow-assignments, /workflow-instances
npx @buildpad/cli@latest add workflows-routes --cwd /path/to/project    # → /add-workflows

# Cron Jobs admin — /cron (jobs list + run history), /cron/[id] (job editor)
npx @buildpad/cli@latest add cron-routes --cwd /path/to/project         # → /add-cron

# AI Chat — a chat with a Chocolate Factory agent (docked panel, floating widget, "Ask AI" button)
npx @buildpad/cli@latest add ai-chat-routes --cwd /path/to/project      # → /add-ai-chat (browser-direct)
npx @buildpad/cli@latest add ai-chat-proxy-routes --cwd /path/to/project  # → /add-ai-chat (server proxy, Node server only)
```

<!-- buildpad-backend: supabase -->
Files and the Form Builder also need the DaaS proxy routes: `npx @buildpad/cli@latest add api-routes --cwd /path/to/project`. See [add-files](../add-files/SKILL.md) and [create-form-builder](../create-form-builder/SKILL.md). The Workflows module calls DaaS directly from the browser and needs no proxy routes; see [add-workflows](../add-workflows/SKILL.md).
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Files and the Form Builder also need the DaaS proxy routes: `npx @buildpad/cli@latest add api-routes --cwd /path/to/project`. On an Engine project each proxy route forwards the request with the signed-in user's access token to the Engine_URL. See [add-files](../add-files/SKILL.md) and [create-form-builder](../create-form-builder/SKILL.md). The Workflows module calls the Engine directly from the browser, with the user's access token as `Authorization: Bearer`, and needs no proxy routes; see [add-workflows](../add-workflows/SKILL.md).

On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it.

On an Engine project files are stored and served by the Engine: `/api/files`, `/api/folders`, `/api/files/signed-url`, and file content at `/api/files/assets/:id` (with a session or a signed token). A file shown in a browser, a public one included, is loaded through a signed URL from `/api/files/signed-url`, not by an anonymous read: an `<img>` element or a link sends no `X-Tenant-Id`. Set no storage bucket option: the Engine stores files on its own disk or in S3. The generated `app/api/assets/[id]/route.ts` forwards to `/api/assets/:id`, a path the Engine does not serve: see [add-files](../add-files/SKILL.md) for what to do instead.
<!-- /buildpad-backend -->

> The `ui.buildpad.ai` docs use the shorthand `buildpad add <targets>` (global install); `npx @buildpad/cli@latest add <targets>` is the equivalent no-install form.

## Post-Install Validation

```bash
# 1. Check installation status
npx @buildpad/cli@latest status --cwd /path/to/project

# 2. Fix any untransformed @buildpad/* imports
grep -r "from '@buildpad/" components/ lib/ 2>/dev/null

# 3. Run validation
npx @buildpad/cli@latest validate --cwd /path/to/project

# 4. Auto-fix common issues
npx @buildpad/cli@latest fix --cwd /path/to/project

# 5. Build to verify
cd /path/to/project && pnpm build
```

## Key Dependencies

If `pnpm install` doesn't resolve everything after CLI add:

<!-- buildpad-backend: supabase -->
```bash
pnpm add clsx tailwind-merge @mantine/core @mantine/hooks @mantine/dates @mantine/dropzone @mantine/tiptap @tabler/icons-react dayjs @supabase/ssr @supabase/supabase-js
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```bash
pnpm add clsx tailwind-merge @mantine/core @mantine/hooks @mantine/dates @mantine/dropzone @mantine/tiptap @tabler/icons-react dayjs @supabase/ssr @supabase/supabase-js
```

On an Engine project the Supabase client is kept for sign-in only. Keep `@supabase/ssr` and `@supabase/supabase-js`: the generated sign-in, the `DaaSProviderWrapper` and `lib/api/auth-headers.ts` use them to sign in against the Engine_URL and to read the signed-in user's session. Send no data call through the Supabase client.
<!-- /buildpad-backend -->

## References

- [Buildpad component guide](references/buildpad.instructions.md)

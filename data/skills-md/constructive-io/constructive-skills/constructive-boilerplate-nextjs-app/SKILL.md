---
name: constructive-boilerplate-nextjs-app
description: Set up and develop with the Constructive App frontend boilerplate — a Next.js application with authentication, organization management, invites, members, and a GraphQL SDK. Use when scaffolding a new Constructive frontend application from the boilerplate.
---

Set up and develop with the Constructive App frontend boilerplate — a Next.js application with authentication, organization management, invites, members, and a GraphQL SDK.

## When to Apply

Use this skill when:
- Setting up a new Constructive frontend application from the boilerplate
- Working with the constructive-app template (auth, orgs, invites, members)
- Needing to understand the project structure, routes, or configuration
- Running or customizing the Constructive App boilerplate

## Overview

The Constructive App boilerplate is a **frontend-only** Next.js application that connects to a Constructive backend. It provides production-ready authentication flows, organization management, invite handling, member management, and account settings — all powered by a generated GraphQL SDK.

## Setup

### 1. Clone the Boilerplate

Use `pgpm init` with the `-w` flag to scaffold a workspace from the template. All required arguments must be provided to avoid interactive prompts:

```bash
pgpm init -w \
  --repo constructive-io/sandbox-templates \
  --template nextjs/constructive-app \
  --name <workspace-name> \
  --fullName "<Author Full Name>" \
  --email "<author@example.com>" \
  --repoName <workspace-name> \
  --username <github-username> \
  --license MIT \
  --moduleName <module-name>
```

**Required arguments for non-interactive mode (avoid asking for user input):**

| Argument | Description |
|----------|-------------|
| `--name` | Workspace directory name |
| `--fullName` | Author's full name |
| `--email` | Author's email |
| `--repoName` | Repository name (typically same as workspace name) |
| `--username` | GitHub username |
| `--license` | License (MIT, APACHE-2.0, BSD-3-CLAUSE, etc.) |
| `--moduleName` | Module/package name inside the workspace |

The boilerplate is created at `<workspace-name>/packages/<module-name>/`.

> **Interactive mode (for humans):** Prompt will be asking for the arguments missing from the required arguments list:
> ```bash
> pgpm init -w --repo constructive-io/sandbox-templates --template nextjs/constructive-app
> ```

#### Adding to an Existing Workspace

If you already have a pnpm workspace (a directory with `pnpm-workspace.yaml`), use `pgpm init` **without** the `-w` flag to clone the boilerplate as a new module inside it. Run this from the **workspace root**:

```bash
pgpm init \
  --repo constructive-io/sandbox-templates \
  --template nextjs/constructive-app \
  --moduleName <module-name>
```

**Required arguments for existing workspace :**

| Argument | Description |
|----------|-------------|
| `--moduleName` | Module/package name for the new boilerplate |

This creates the module at `packages/<module-name>/` within your existing workspace. The workspace-level arguments (`--name`, `--fullName`, `--email`, etc.) are **not needed** since the workspace already exists.

> **Note:** You must run this from the workspace root or a valid `packages/` subdirectory. If you are not inside a pnpm workspace, pgpm will error with "Not inside a PNPM workspace." Use the `-w` flag (see above) to create a new workspace and module together.

> **Interactive mode (for humans):** :
> ```bash
> pgpm init --repo constructive-io/sandbox-templates --template nextjs/constructive-app
> ```

### 2. Install Dependencies

```bash
cd <workspace-name>/packages/<module-name>
pnpm install
```

### 3. Configure Environment

Create or verify `.env.local`:

```bash
# GraphQL endpoint (must point to a running Constructive backend)
NEXT_PUBLIC_SCHEMA_BUILDER_GRAPHQL_ENDPOINT=http://api.localhost:3000/graphql
```

### 4. Generate GraphQL SDK

The SDK must be generated against a running backend:

```bash
pnpm codegen
```

This runs `@constructive-io/graphql-codegen` using `graphql-codegen.config.ts` and outputs the SDK to `src/graphql/schema-builder-sdk/api`.

### 5. Start Development

```bash
pnpm dev
```

Opens at [http://localhost:3001](http://localhost:3001).

## Backend Requirements

This boilerplate requires a running Constructive backend. The easiest way is via **Constructive Hub**:

```bash
# Terminal 1: Start backend infrastructure
cd /path/to/constructive-hub
pnpm start

# Terminal 2: Start this frontend
cd /path/to/constructive-app
pnpm dev
```

Required backend services:

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL | 5432 | Database with Constructive schema |
| GraphQL Server (Public) | 3000 | API endpoint for app operations |
| GraphQL Server (Private) | 3002 | Admin operations |
| Job Service | 8080 | Background job processing |
| Email Function | 8082 | Email sending via SMTP |
| Mailpit SMTP | 1025 | Email server (development) |
| Mailpit UI | 8025 | View sent emails |

## Project Structure

```
src/
├── app/                        # Next.js App Router pages
│   ├── layout.tsx              # Root layout with providers
│   ├── page.tsx                # Home / org listing page
│   ├── login/                  # Login page
│   ├── register/               # Registration page
│   ├── forgot-password/        # Password reset request
│   ├── reset-password/         # Password reset form
│   ├── check-email/            # Email check prompt
│   ├── verify-email/           # Email verification
│   ├── invite/                 # Accept invite flow
│   ├── invites/                # Pending invites list
│   ├── account/                # Account management
│   ├── settings/               # App settings
│   ├── users/                  # User management
│   └── orgs/
│       └── [orgId]/            # Org-scoped pages
│           ├── layout.tsx      # Org layout with sidebar
│           ├── activity/       # Org activity
│           ├── invites/        # Org invites management
│           ├── members/        # Org members management
│           └── settings/       # Org settings
├── components/
│   ├── ui/                     # shadcn/ui components (43 components)
│   ├── auth/                   # Auth forms (login, register, reset, etc.)
│   ├── organizations/          # Org CRUD components
│   ├── invites/                # Invite management components
│   ├── members/                # Member management components
│   ├── account/                # Account settings components
│   ├── app-shell/              # Sidebar, navigation, layout shell
│   ├── layouts/                # Page layout wrappers
│   ├── settings/               # Settings UI
│   ├── shared/                 # Shared/reusable components
│   └── skeletons/              # Loading skeleton components
├── config/
│   └── branding.ts             # App name, logos, legal links
├── graphql/
│   ├── execute.ts              # GraphQL execution layer
│   ├── index.ts                # GraphQL exports
│   ├── typed-document.ts       # Typed document utilities
│   └── schema-builder-sdk/     # Generated SDK (via codegen)
├── hooks/                      # Shared React hooks
├── lib/
│   ├── auth/                   # Auth utilities and context
│   ├── gql/                    # GraphQL hooks and query factories
│   ├── navigation/             # Route and navigation helpers
│   ├── permissions/            # Permission checking utilities
│   ├── constants/              # App constants
│   ├── logger/                 # Logging utilities
│   ├── runtime/                # Runtime helpers
│   ├── utils/                  # General utilities
│   └── validation/             # Zod schemas and validation
├── store/                      # Client state management
├── app-config.ts               # App-wide configuration
└── app-routes.ts               # Route definitions
```

## Customization

### Branding

Edit `src/config/branding.ts` to customize:
- App name and tagline
- Logo and wordmark paths (relative to `/public`)
- Company name for legal footer
- Legal links (disclaimer, privacy policy, etc.)
- Home path for logo links

### Adding UI Components

Components use the Constructive shadcn registry:

```bash
npx shadcn@latest add @constructive/<component>
```

Registry URL is configured in `components.json`. Components use Base UI primitives, Tailwind CSS 4, and cva for variants.

### GraphQL SDK

The SDK is generated from the running backend schema. After backend schema changes:

```bash
pnpm codegen
```

Config in `graphql-codegen.config.ts` points to `http://api.localhost:3000/graphql` by default.

## Features

- **Authentication** — Login, register, logout, password reset, email verification
- **Organizations** — Create and manage organizations
- **Invites** — Send and accept organization invites
- **Members** — Manage organization members and roles
- **Account Management** — Profile, email verification, account deletion
- **App Shell** — Sidebar navigation, theme switching, responsive layout
- **Permissions** — Role-based access control for org features

## Troubleshooting

- **GraphQL errors on startup**: Ensure the Constructive backend is running and the endpoint in `.env.local` is correct
- **Empty SDK directory**: Run `pnpm codegen` with the backend running to generate the SDK
- **Password reset emails not arriving**: Requires the full backend stack (job service + email function). Check Mailpit UI at `http://localhost:8025`
- **Port conflicts**: The frontend runs on port 3001 by default. The backend GraphQL server uses port 3000

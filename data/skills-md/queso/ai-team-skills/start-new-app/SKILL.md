---
name: start-new-app
description: Scaffolds a new app from the context-kit template. Clones the repo, renames the project, initializes git, creates a PRD directory, and asks the user to provide a PRD.
---

# Start New App

Scaffold a new application from the [context-kit](https://github.com/queso/context-kit) template.

## Step 1: Ask for the App Name

Ask the user:

> **What should the app be called?** (This will be used for the directory name, package.json name, page titles, etc.)

Validate that the name is a reasonable kebab-case or lowercase slug (e.g. `my-cool-app`). If the user gives a human-readable name like "My Cool App", convert it to kebab-case (`my-cool-app`) and confirm with them.

Also ask:

> **Where should I create the project?** (Default: the current working directory's parent, so the new app sits alongside the current project)

If the user doesn't specify, use the parent of the current working directory.

## Step 2: Fetch the Latest Setup Instructions

Before cloning, fetch the context-kit README from GitHub to check for any updates to the setup process:

```
WebFetch: https://github.com/queso/context-kit/blob/main/README.md
```

Use the fetched instructions as the source of truth. The steps below reflect the current process but the README should take precedence if it has changed.

## Step 3: Clone and Initialize

Run these commands:

```bash
git clone https://github.com/queso/context-kit.git <app-name>
cd <app-name>
rm -rf .git
git init
```

Replace `<app-name>` with the name from Step 1. Clone into the directory chosen in Step 1.

## Step 4: Rename the Project

Update all references from "context-kit" to the user's app name:

1. **`package.json`** — Change the `"name"` field to the app name
2. **`CLAUDE.md`** — Replace the project title with the app name, and add `prd/` and `docs/` to the Directory Structure section:
   ```
   prd/                    Product Requirements Documents (NNNN-slug.md)
   docs/                   Technical documentation, architecture decisions, API specs
   ```
3. **`app/layout.tsx`** — Replace the title/metadata with the app name

Search the entire project for any other occurrences of "context-kit" and replace them as well. Use a case-insensitive search to catch variations like "Context Kit" or "Context-Kit".

## Step 5: Set Up Environment

```bash
cp .env.example .env
```

Do **not** modify the `.env` file contents — the user will configure it later.

## Step 6: Create Project Directories

```bash
mkdir -p prd
mkdir -p docs
```

- **`prd/`** — Where PRDs live, following the `NNNN-slug.md` naming convention.
- **`docs/`** — A place for technical documentation, architecture decisions, API specs, and other repo-level docs.

## Step 7: Initial Commit

Stage everything and create the initial commit:

```bash
git add -A
git commit -m "Initial scaffold from context-kit template"
```

## Step 8: Hand Off to the User

Present a summary of what was done:

- Where the project was created (full path)
- What was renamed
- That `.env` needs to be configured (DATABASE_URL, SITE_URL)
- That they can start the app with `docker compose up -d` or `pnpm install && pnpm db:generate && pnpm dev`

Then ask:

> **Ready to write your first PRD?** Describe the app you want to build — what problem it solves, who it's for, and what success looks like. I'll create a PRD in `prd/` to guide development.

If the user provides PRD content, use the `write-prd` skill workflow to create a properly structured PRD in `prd/0001-<slug>.md`.

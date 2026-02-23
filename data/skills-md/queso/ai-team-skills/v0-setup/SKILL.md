---
name: v0-setup
description: Fetches v0.dev designs via the Platform API and prepares them for adaptation into your project. Handles folder setup, source code retrieval, component inventory, and produces an adaptation brief. Use when integrating v0 designs.
---

# Skill: v0 Design Fetch & Adaptation

You are a v0.dev design integration specialist. When this skill is invoked, you fetch
v0 source code, analyze it against the current project, and produce an adaptation brief.

## Step 1: Parse `$ARGUMENTS`

`$ARGUMENTS` can be one of:

1. **A v0 URL** — e.g., `https://v0.app/chat/vacation-rental-website-pCP3OQ8u3PU`
   - Extract the chat ID from the URL slug
   - Derive a feature name from the slug (strip trailing hash ID)

2. **A v0 URL + custom name** — e.g., `https://v0.app/chat/abc123 dashboard`
   - Use the URL to fetch, but name the folder with the custom name

3. **A feature folder name** — e.g., `login-page`
   - Skip fetching; read directly from `designs/<feature-name>/`
   - Files should already be there (manually placed by the user)

## Step 2: Check Folder Structure

Ensure a `designs/` directory exists in the project root. If it doesn't exist:

1. Create the `designs/` directory
2. Copy `references/designs-agents.md` from this skill's directory into `designs/AGENTS.md`
3. Create a symlink: `designs/CLAUDE.md` → `designs/AGENTS.md`

This gives AI coding tools context that `designs/` contains reference files, not application code.

## Step 3: Fetch the v0 Design

If `$ARGUMENTS` contains a v0 URL:

1. **Check for `V0_API_KEY`** in the environment
   - If not set, tell the user:
     > Set `V0_API_KEY` in your environment. Get a key from https://v0.dev/chat/settings/keys
     > You can set it via shell (`export V0_API_KEY=your-key`), in `.claude/settings.local.json`
     > under `"env"`, or in a project `.env` file.
   - Stop and wait for the user to set it.

2. **Locate the fetch script** — check these paths in order:
   - `.claude/skills/v0-setup/scripts/fetch-v0.mjs` (project install)
   - `~/.claude/skills/v0-setup/scripts/fetch-v0.mjs` (global install)
   - Use whichever exists. If neither exists, tell the user the skill is not installed correctly.

3. **Run the fetch script:**
   ```
   node <skill-path>/scripts/fetch-v0.mjs <v0-url-or-chat-id> <feature-name> --output-dir <project-root>
   ```
   The script creates `designs/<feature-name>/` with all v0 source files and a `manifest.json`.

## Step 4: Analyze & Prepare Adaptation Brief

After files are fetched (or if working from an existing folder):

### 4a. Read project context

Read these files to understand the project's conventions:

1. `CLAUDE.md` — project-wide conventions, architecture, coding standards
2. `components.json` — shadcn/ui configuration (path aliases, component style)
3. `app/globals.css` — CSS custom properties, theme tokens, color scheme
4. `tailwind.config.ts` (if present) — extended theme values, custom utilities
5. `components/ui/` — list existing shadcn components so you know what's available
6. `app/` — existing route structure for placement decisions

### 4b. Inventory fetched files

1. Read all files in `designs/<feature-name>/`
2. Read `manifest.json` for metadata (source URL, file list)
3. Read `notes.md` if present — human overrides take priority over all defaults

### 4c. Check shadcn component availability

1. List all shadcn components imported by the v0 code (e.g., `@/components/ui/button`)
2. Check which exist locally in `components/ui/`
3. Note which need to be installed: `pnpm dlx shadcn@latest add <component-name>`

### 4d. Produce adaptation brief

Summarize your findings for the user:

- **Source**: v0 URL and chat ID
- **Files fetched**: count and list
- **Target location suggestion**: based on component names and project structure
- **shadcn components needed**: which exist, which must be installed
- **Theme compatibility notes**: any v0 color/spacing patterns that may need alignment
- **Recommended next steps**: install missing components, then adapt

## Step 5: Adapt the Design

Read the detailed adaptation process from `references/adaptation-rules.md` in this
skill's directory (same location as this SKILL.md). Follow the four-pass process
described there:

1. **Pass 1: Inventory & Planning** — file inventory, target location, dependency list
2. **Pass 2: Structural Integration** — imports, images, data, interactivity, file splitting
3. **Pass 3: Theme Alignment** — CSS variables, typography, spacing, dark mode, border radius
4. **Pass 4: Verification** — dev server, lint, type check

## Adaptation Notes Template

If the user wants to create a `notes.md` for a design, copy the template from
`references/template-notes.md` in this skill's directory into `designs/<feature-name>/notes.md`.

## Environment Setup Reference

The user needs `V0_API_KEY` in their environment. Options:

1. **Shell environment:** `export V0_API_KEY=your-key-here`
2. **Claude Code settings:** Add to `.claude/settings.local.json`:
   ```json
   {
     "env": {
       "V0_API_KEY": "your-key-here"
     }
   }
   ```
3. **Project `.env`:** Add `V0_API_KEY=your-key-here` (if the project loads dotenv)

Get the key from: https://v0.dev/chat/settings/keys

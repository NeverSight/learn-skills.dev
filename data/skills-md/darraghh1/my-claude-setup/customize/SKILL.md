---
name: customize
description: "Onboarding wizard that collects project details and fills all CUSTOMIZE markers across CLAUDE.md and rule files automatically."
argument-hint: "[optional: project-name]"
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: "Read Write Edit Glob Grep Bash(grep*) AskUserQuestion TaskCreate TaskUpdate TaskList TaskGet"
metadata:
  version: 1.0.0
---

# Customize Setup for Your Project

Customize this Claude Code setup for: **$ARGUMENTS**

## Critical

- **Do NOT modify hooks, agents, or other skills** — this skill ONLY fills CUSTOMIZE markers
- **Do NOT invent information** — if the user didn't provide something, ask for it
- **Keep it concise** — CLAUDE.md is loaded on every prompt. Verbose sections waste tokens.
- **Match the style** of existing content in each file when filling markers

## What This Skill Does

This setup has `<!-- CUSTOMIZE -->` markers in CLAUDE.md and `.claude/rules/*.md` that need
project-specific details. This skill collects your project information ONCE, then fills in
ALL markers automatically.

See `examples.md` in this skill directory for a complete example of what good customization
looks like (the "Acme HR" reference project).

## Task Tracking

Tasks survive context compacts — skipping this check causes lost progress and repeated work.

Before starting work, run `TaskList` to check if tasks already exist from a previous session or before a compact. If tasks exist:
1. Read existing tasks with `TaskGet` for each task ID
2. Find the first task with status `pending` or `in_progress`
3. Resume from that task — do NOT recreate the task list

If no tasks exist, create them after the first round of user questions:

**Example task list:**
```
Task 1: Collect project brief (all rounds)
Task 2: Read all CUSTOMIZE markers
Task 3: Fill CLAUDE.md
Task 4: Fill rule files
Task 5: Clean up markers
Task 6: Validate completeness
```

Mark each task `in_progress` when starting and `completed` when done.

## Step 1: Collect Project Brief

Use `AskUserQuestion` to collect project details. Ask up to 4 questions at a time, then
follow up with remaining questions. Do NOT proceed until all critical information is gathered.

### Round 1 — Core Identity

Ask these questions using `AskUserQuestion`:

1. **Project name and description** — "What is your project name and a one-line description?"
   - Example: "Acme SaaS — workforce management platform"

2. **App structure** — "Is this a monorepo or single app?"
   - If monorepo: ask for app names, ports, and purposes in follow-up
   - If single-app: note this and skip monorepo section

3. **Package manager** — "Which package manager?"
   - Options: npm, pnpm, yarn, bun

4. **Component library** — "What UI component library do you use?"
   - Options: shadcn/ui, Radix UI, MUI, custom, none
   - Follow up: "What is the import path?" (e.g., `@/components/ui`, `~/components`)

### Round 2 — Architecture

5. **Auth model** — "What is your auth/account model?"
   - Options: Single-user, Multi-tenant with teams, Multi-tenant with orgs, Other
   - If multi-tenant: "How are accounts scoped? (account_id FK, org_id, workspace_id)"

6. **Framework wrappers** — "Does your framework provide wrappers for Server Actions or auth?"
   - Example: "enhanceAction from MakerKit", "withAuth from next-auth"
   - If no wrapper: we'll use the default Zod + manual auth pattern

7. **Logging** — "What logging approach do you use?"
   - Options: console (dev only), Pino, Winston, framework logger
   - Follow up if not console: "What is the import path?" (e.g., `@/lib/logger`)

8. **Supabase client paths** — "Where are your Supabase client factories?"
   - Default: `@/lib/supabase/server` and `@/lib/supabase/client`
   - Or framework-provided: `@kit/supabase/server-client`

### Round 3 — Commands & Git

9. **Key commands** — "List your main dev commands:"
   - dev, build, test, lint, verify/check-all, migration commands, type generation
   - If unsure, ask to read `package.json` scripts

10. **Git strategy** — "What is your branch strategy?"
    - Options: main only, main + development, feature branches to main
    - Remote names (origin, upstream if forked from a template)

11. **CI/CD** — "What CI/CD do you use?"
    - Options: GitHub Actions, Vercel, GitLab CI, none yet
    - Key jobs: typecheck, lint, test, deploy

### Round 4 — Optional Features

12. **i18n** — "Do you use internationalization?"
    - If yes: library (next-intl, react-i18next), translation namespaces

13. **Testing structure** — "Where do your tests live?"
    - Default: `__tests__/{feature}/`
    - Or: `src/__tests__/`, `app/**/*.test.ts`, colocated

14. **Anything else** — "Any framework-specific patterns, admin panel requirements, feature flags, or special conventions I should know about?"

## Step 2: Read All CUSTOMIZE Markers

Before filling anything in, read every file that has markers to understand context:

```
CLAUDE.md
.claude/rules/git-workflow.md
.claude/rules/database.md
.claude/rules/patterns.md
.claude/rules/coding-style.md
.claude/rules/security.md
.claude/rules/ui-components.md
.claude/rules/forms.md
.claude/rules/testing.md
.claude/rules/i18n.md
.claude/rules/admin.md
.claude/rules/pages-and-layouts.md
.claude/rules/route-handlers.md
```

Read each file completely before editing.

## Step 3: Fill CLAUDE.md

This is the most important file — Claude reads it on every conversation.

### Marker: Project description (top of file)
Replace the `<!-- CUSTOMIZE: Replace with a brief description -->` comment with a one-line
description. Example: `Acme SaaS — Next.js App Router, Supabase, TypeScript.`

Remove the entire HTML comment block (the template instructions at the top of the file).

### Marker: Critical Rules
Add any framework-specific critical rules from the intake. Examples:
- If using a Server Action wrapper: "Skipping {wrapper} means unauthenticated data can reach the database."
- If using a specific logger: "Use `getLogger()` from `{path}` instead of console.log."
- If monorepo with upstream: "When merging upstream, propagate infrastructure changes to all product apps."

### Marker: Monorepo
- If monorepo: Add a table with app names, ports, and purposes
- If single-app: Remove the `## Monorepo` section entirely

### Marker: Commands
Add all commands from the intake in a code block. Group by category (dev, test, build, deploy).

### Marker: Architecture
Describe: multi-tenant model, data fetching patterns, auth, RLS approach, any special systems.

### Marker: Verification
Add the project's verify/check commands (typecheck, lint, test).

## Step 4: Fill Rule Files

For each rule file, replace `<!-- CUSTOMIZE -->` markers with project-specific content.

### git-workflow.md
- Remotes table (origin URL, upstream if applicable)
- Branch strategy (adjust the table)
- Verify command
- CI pipeline table
- Upstream merge process (if forked from template, otherwise remove section)

### database.md
- Migration/typegen command paths
- RLS helper functions (list any existing helpers, or keep the example)
- OTP components (if framework provides them, otherwise remove marker)

### patterns.md
- Server Action wrapper (replace manual pattern with framework wrapper if applicable)
- Supabase client import paths (update the table)
- Auth/account model (adjust or remove multi-tenant section)

### coding-style.md
- Server Action wrapper reference (match patterns.md)

### security.md
- Auth wrapper documentation

### ui-components.md
- Component library name and import path

### forms.md
- Server Action wrapper
- Form component library imports

### testing.md
- Test directory structure
- Test commands

### i18n.md
- i18n setup (library, config)
- Translation namespaces
- If no i18n: Delete the entire file (or leave as-is for future use)

### admin.md
- Admin verification pattern

### pages-and-layouts.md
- Loading component
- Workspace providers
- Feature flags (if applicable)

### route-handlers.md
- Route handler wrapper (if framework provides one)

## Step 5: Clean Up Markers

After filling all markers:

1. **Remove all `<!-- CUSTOMIZE -->` comments** — they served as prompts and should be
   deleted after customization. The content they prompted for is now filled in.

2. **Remove the template instruction block** at the top of CLAUDE.md (the HTML comment
   with "SETUP INSTRUCTIONS").

3. **Update file headers** — Change generic titles to project-specific ones:
   - `# Patterns — Next.js Supabase TypeScript` could become
     `# Patterns — Acme Next.js Supabase`

## Step 6: Validate

Run these checks to confirm completeness:

### Check 1: No remaining CUSTOMIZE markers

```bash
grep -rn "CUSTOMIZE" CLAUDE.md .claude/rules/ 2>/dev/null | grep -v "node_modules" || echo "All markers filled!"
```

If any remain, go back and fill them. If a marker cannot be filled due to missing
information, ask the user.

### Check 2: CLAUDE.md has content in all sections

Read back `CLAUDE.md` and verify:
- [ ] Project description is present (not a placeholder)
- [ ] Critical Rules section has content
- [ ] Monorepo section has content OR was removed for single-app
- [ ] Commands section has a code block with real commands
- [ ] Architecture section describes the actual architecture
- [ ] Verification section has real commands

### Check 3: No template instruction block remains

```bash
grep -c "SETUP INSTRUCTIONS" CLAUDE.md || echo "Template header removed!"
```

### Report

Print a summary:
```
Customization complete for {project-name}!

Files modified:
  - CLAUDE.md
  - .claude/rules/git-workflow.md
  - .claude/rules/database.md
  - ... (list all modified files)

Remaining markers: {count} (0 = fully customized)

Next steps:
  1. Review the changes: git diff
  2. Test the setup: start a new Claude Code session and verify context
  3. Optional: Add project-specific validators to post_tool_use.py
```

## Resuming After Context Compact

If you notice context was compacted or you're unsure of current progress:

1. Run `TaskList` to see all tasks and their status
2. Find the `in_progress` task — that's where you were
3. Run `TaskGet {id}` on that task to read full details
4. Continue from that task — don't restart from the beginning

Tasks persist across compacts. The task list is your source of truth for progress, not your memory.

**Pattern for every work session:**
```
TaskList → find in_progress or first pending → TaskGet → continue work → TaskUpdate (completed) → next task
```

## Troubleshooting

### Markers remain after Step 6 validation
The most common cause is a marker inside an HTML comment that looks like content.
Read the file, find the `<!-- CUSTOMIZE` comment, and either fill it or delete it.
If the marker needs information you don't have, use `AskUserQuestion` to ask.

### User unsure about commands or paths
Offer to read their `package.json` for commands: `Read package.json` and extract scripts.
For monorepo structures, `Glob "apps/*/package.json"` reveals app layout.

### i18n section not applicable
If the project doesn't use i18n, you can either delete `.claude/rules/i18n.md` entirely
or leave it with a note at the top: "i18n is not currently used in this project."

### User provides minimal answers
Ask follow-up questions. A one-word answer like "pnpm" is fine for package manager, but
"yes" for monorepo needs follow-up: "What are your app names, ports, and purposes?"

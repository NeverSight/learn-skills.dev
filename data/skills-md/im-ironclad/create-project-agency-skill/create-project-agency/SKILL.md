---
name: create-project-agency
description: >
  Bootstrap an AGENTS.md and documentation index for any project. Detects
  project signals from the filesystem, asks targeted questions, and generates
  structured project documentation. Use when setting up a new project or
  updating an existing AGENTS.md.
disable-model-invocation: true
license: MIT
metadata:
  author: ironcladapps
  version: "1.0.0"
  organization: Ironclad Apps
  abstract: >
    Project documentation bootstrapper that auto-detects tech stack, framework,
    testing tools, and project structure, then generates an AGENTS.md and
    supporting docs (architecture, testing, vision, contributing, PLAN.md)
    through guided questions.
---

# Create Project Agency

Generate an `AGENTS.md` and supporting documentation for the current project. Detects framework, tooling, and structure automatically, then asks targeted questions to fill gaps.

**Arguments**: `$ARGUMENTS`
- `--update` — Skip the existing-file prompt and go straight to update mode

---

## Phase 0: Setup & Existing File Check

### Step 1: CLAUDE.md Symlink Question

Ask the user:

> "This skill generates `AGENTS.md` as the primary documentation file. Would you also like a `CLAUDE.md` symlink pointing to it?"
> 1. Yes (recommended for Claude Code users)
> 2. No — just AGENTS.md

Store the choice as `{create_symlink}` (true/false).

### Step 2: Check for Existing Files

Check if `AGENTS.md` already exists in the project root.

**If it exists AND `--update` was NOT passed:**
- Show the user a summary of the existing file
- Ask: "AGENTS.md already exists. Would you like to: (1) Update it with new detections, (2) Regenerate from scratch, (3) Cancel?"
- If "Update" → proceed to Phase 1 in **update mode** (see Update Mode section below)
- If "Regenerate" → proceed to Phase 1 normally (will overwrite)
- If "Cancel" → stop

**If it exists AND `--update` was passed:**
- Proceed directly to Phase 1 in **update mode**

**If it does not exist:**
- Proceed to Phase 1 normally

Also check for an existing `CLAUDE.md` that is NOT a symlink — if found, note it for Phase 5 (warn before replacing with a symlink).

---

## Phase 1: Silent Detection

Scan the project root to build a detection profile. Do NOT ask the user anything yet — just gather signals. Use Glob and Read tools.

### What to Detect

**Package ecosystem** — check for these files at the project root:
- `package.json` → read `name`, `description`, `scripts`, `dependencies`, `devDependencies`, `workspaces`, `packageManager`
- Lockfiles: `yarn.lock` → yarn, `package-lock.json` → npm, `pnpm-lock.yaml` → pnpm, `bun.lock` / `bun.lockb` → bun
- `requirements.txt` / `pyproject.toml` / `setup.py` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `Gemfile` → Ruby
- `composer.json` → PHP

**Framework** — check for config files:
- `next.config.*` → Next.js (read for App Router vs Pages Router signals)
- `nuxt.config.*` → Nuxt
- `svelte.config.*` → SvelteKit
- `vite.config.*` → Vite
- `angular.json` → Angular
- `remix.config.*` → Remix
- `astro.config.*` → Astro

**TypeScript** — `tsconfig.json`:
- Check `compilerOptions.strict` for strict mode
- Check `compilerOptions.paths` for path aliases

**Monorepo** — check for:
- `turbo.json` → Turborepo
- `nx.json` → Nx
- `pnpm-workspace.yaml` → pnpm workspaces
- `workspaces` field in root `package.json` → yarn/npm workspaces
- `lerna.json` → Lerna

**Linting / formatting**:
- `.eslintrc*`, `eslint.config.*` → ESLint
- `.prettierrc*`, `prettier.config.*` → Prettier
- `biome.json`, `biome.jsonc` → Biome

**Testing**:
- `vitest.config.*` or `vitest` in devDeps → Vitest
- `jest.config.*` or `jest` in devDeps → Jest
- `playwright.config.*` or `@playwright/test` in devDeps → Playwright
- `cypress.config.*` or `cypress` in devDeps → Cypress
- `pytest.ini`, `conftest.py`, `pyproject.toml [tool.pytest]` → pytest

**Styling**:
- `tailwind.config.*` or `@tailwindcss` in deps → Tailwind CSS (check v3 config file vs v4 CSS-only)
- `postcss.config.*` → PostCSS

**Backend / database**:
- `convex/` directory → Convex
- `supabase/` directory or `supabase` in deps → Supabase
- `prisma/` directory → Prisma
- `drizzle.config.*` → Drizzle
- `firebase.json` or `firebaserc` → Firebase

**Existing documentation**:
- `README.md` → read for project description and setup instructions
- `docs/` directory → list contents
- Any root `.md` files → note them

**Directory structure**:
- List top-level directories (exclude: `node_modules`, `.git`, `dist`, `build`, `.next`, `.turbo`, `__pycache__`, `.venv`, `target`, `vendor`)
- For monorepos, also list workspace directories one level deep

### Detection Output Format

Build an internal profile object (not shown to user yet):

```
Project: {name from package.json or directory name}
Description: {from package.json or README}
Package Manager: {detected}
Language: {TypeScript strict | TypeScript | JavaScript | Python | Go | Rust | ...}
Framework: {detected}
Monorepo: {tool} with workspaces: [{list}]
Styling: {detected}
Backend: {detected}
Testing: {tools detected}
Linting: {tools detected}
Structure: {top-level dirs}
Existing Docs: {list of .md files found}
```

---

## Phase 2: Present Findings & Ask Questions

Show the detection summary in a clean format:

```
## Detected Project Profile

- **Project**: {name} — {description or "no description found"}
- **Package Manager**: {yarn | npm | pnpm | bun | pip | ...}
- **Language**: {TypeScript (strict) | TypeScript | JavaScript | ...}
- **Framework**: {Next.js (App Router) | Nuxt 3 | SvelteKit | ...}
- **Monorepo**: {Turborepo | Nx | none} — workspaces: {list}
- **Styling**: {TailwindCSS v4 | TailwindCSS v3 | CSS Modules | ...}
- **Backend**: {Convex | Supabase | Prisma + PostgreSQL | ...}
- **Testing**: {Vitest + Playwright | Jest + Cypress | ...}
- **Linting**: {ESLint + Prettier | Biome | ...}
- **Structure**: {key directories}
```

Then ask targeted questions using AskUserQuestion. Only ask what detection couldn't determine:

1. **Always ask**: "Is this detection correct? Anything to add or change?" (freeform)
2. **If no description found**: "What is this project in one sentence?"
3. **Always ask**: "Any hard constraints Claude should always follow?" (e.g., "never use npm", "always prefer server components", "use conventional commits")
4. **Always ask**: "Any conventions not captured above?" (e.g., naming patterns, file organization rules, component patterns)

Keep questions minimal. If detection was thorough, questions 1 and 3 may be sufficient.

5. **Always ask**: "Which of these detected technologies would you like documentation fetched for? Select all that apply." Present each detected technology as a selectable option (multiSelect). Group by category:
   - **Framework**: e.g., Next.js, Nuxt, SvelteKit
   - **Language**: e.g., TypeScript, Python, Go
   - **Backend/DB**: e.g., Supabase, Prisma, Drizzle, Convex
   - **Testing**: e.g., Vitest, Playwright, Jest, Cypress
   - **Styling**: e.g., TailwindCSS
   - **Other**: any other significant detected libraries
6. **Always ask**: "Any technologies NOT detected that you'd like docs fetched for?" (freeform)

Store selections from questions 5 and 6 as `{tech_docs_list}`.

---

## Phase 3: Fetch Tech Stack Documentation

For each technology in `{tech_docs_list}`, fetch documentation and save it locally.

### Step 1: Create docs directory

Create `.docs/` at the project root if it doesn't exist.

### Step 2: Fetch docs for each technology

For each technology in `{tech_docs_list}`:

1. **Resolve library** — Use the `resolve-library-id` Context7 MCP tool:
   - Query: the technology name (e.g., "next.js", "typescript", "tailwindcss")
   - Select the best matching library ID

2. **Query documentation** — Use the `query-docs` Context7 MCP tool with targeted queries:
   - Query topics relevant to the technology category (see Topic Guide below)
   - Run up to 3 queries per technology to cover core topics

3. **Save documentation** — Write fetched content to `.docs/{technology}/`:
   - Create subdirectory: `.docs/{technology}/` (e.g., `.docs/nextjs/`, `.docs/typescript/`)
   - Save each query result as a separate markdown file named by topic
   - File naming: `{topic}.md` (e.g., `routing.md`, `data-fetching.md`)
   - Prepend each file with: `# {Technology} — {Topic}\n\n> Source: Context7 documentation\n\n`

4. **Build index entry** — Record the files created for the compressed index

### Topic Guide

Query topics based on technology category:

**Frameworks (Next.js, Nuxt, SvelteKit, Remix, Astro, etc.):**
- Routing and navigation
- Data fetching and caching
- API routes / server functions

**Languages (TypeScript, Python, Go, Rust, etc.):**
- Type system / type utilities (TS), typing (Python), etc.
- Configuration and compiler options
- Common patterns and idioms

**Backend/DB (Supabase, Prisma, Drizzle, Convex, Firebase):**
- Schema definition and migrations
- Querying and mutations
- Authentication and security rules

**Testing (Vitest, Jest, Playwright, Cypress, pytest):**
- Configuration and setup
- Writing tests and assertions
- Mocking, fixtures, and test utilities

**Styling (TailwindCSS, etc.):**
- Configuration and customization
- Utility classes and patterns
- Responsive design and theming

### Step 3: Ask about .gitignore

Ask the user:

> "Would you like to add `.docs/` to `.gitignore`? These are fetched artifacts that can be re-generated, but committing them ensures availability in CI and for team members without Context7."
> 1. Yes — add to .gitignore (recommended for most projects)
> 2. No — commit docs to the repository

If yes, add `.docs/` to the project's `.gitignore` (create the file if it doesn't exist).

### Step 4: Verify

After fetching, list all files created in `.docs/` and confirm the count with the user:

> "Fetched documentation for {N} technologies ({list}). {X} files saved to `.docs/`. Proceeding to generate AGENTS.md."

### Fallback — If Context7 is unavailable

If Context7 MCP tools (`resolve-library-id`, `query-docs`) are not available:
1. Inform the user: "Context7 MCP is not available in this environment. I can't automatically fetch documentation."
2. Offer alternatives:
   - Skip tech docs (proceed without them)
   - User provides documentation URLs to fetch via WebFetch
   - User provides local documentation paths to index
3. If skipping, proceed to Phase 4 without tech docs index

---

## Phase 4: Generate AGENTS.md

Write the file using the template structure from `references/claude-md-template.md`. Read that file now for the exact format.

### Section Order (strict)

1. **Project header** — `# Name` + one-line description
2. **Tech Stack** — bulleted list: `- **Category**: Technology`
3. **Project Structure** — fenced ASCII tree, 1-2 levels deep. Add inline comments for non-obvious directories. Include "Future additions" line if the user mentioned planned directories.
4. **Conventions** — concrete, actionable rules. Use sub-sections (e.g., `### Testing`, `### Naming`) when a category has 3+ rules.
5. **Tech Stack Docs** (optional) — only if tech docs were fetched in Phase 3. Compressed index pointing to `.docs/` files.
6. **Implementation Plan** (optional) — only if `PLAN.md` exists. Brief pointer to the file.
7. **Doc Index** — compressed pipe-delimited format. Only list files that actually exist. Always include the index maintenance rule.

### Writing Rules

- **Be concrete, not generic.** "Use `yarn` for all package management" is good. "Follow best practices" is not.
- **Omit sections with nothing to say.** If there's no monorepo, don't include a structure section showing a flat project.
- **Use the user's words** from their answers in Phase 2 for constraints and conventions.
- **Keep it under 80 lines.** AGENTS.md should be scannable. Link to docs for details. The Tech Stack Docs index section doesn't count toward the 80-line target since it's a machine-generated reference.
- **No placeholder content.** Every line should be real information about this project.

### Tech Stack Docs Section (if Phase 3 fetched docs)

If tech docs were fetched in Phase 3, include this section between Conventions and Implementation Plan:

```markdown
## Tech Stack Docs

Prefer retrieval-led reasoning over pre-training-led reasoning for any tech stack tasks. Consult the relevant documentation below before implementing features or making technical decisions.

\```
[{ProjectName} Tech Docs]|root: ./.docs
|nextjs:{routing.md, data-fetching.md, api-routes.md}
|typescript:{type-system.md, configuration.md, patterns.md}
|tailwindcss:{configuration.md, utilities.md, theming.md}
\```
```

The format mirrors the Doc Index but uses the `.docs/` root. Each entry lists the actual files saved during Phase 3. Only include entries for technologies that have docs fetched.

---

## Phase 5: Verify & Iterate

Show the generated AGENTS.md content to the user. Ask:

"Here's the generated AGENTS.md. Would you like any adjustments before I write it?"

If the user requests changes, make them. When approved:
1. Write `AGENTS.md`
2. If `{create_symlink}` is true:
   - If `CLAUDE.md` exists as a real file (not a symlink), warn the user: "CLAUDE.md exists as a standalone file. Creating the symlink will replace it. Proceed?"
   - Create symlink: `ln -s AGENTS.md CLAUDE.md` (relative path)
3. Remind: "Don't forget to commit `AGENTS.md`" (and "`CLAUDE.md`" if the symlink was created) "to your repository."

---

## Phase 6: Guided Documentation Creation

After AGENTS.md is finalized, offer to create supporting documentation.

### Presenting the Menu

Show only doc types that make sense for the detected project:

| Doc | When to Offer | File Path |
|-----|--------------|-----------|
| Architecture | Always (non-trivial projects) | `docs/architecture.md` |
| Testing | When testing tools were detected | `docs/testing.md` |
| Vision | When user describes an ambitious product | `docs/vision.md` |
| Contributing | When project likely has collaborators (GitHub remote, multiple contributors in git log) | `docs/contributing.md` |
| Implementation Plan | When project is in active development | `PLAN.md` |

Present as a selectable menu:

"Would you like to create any supporting documentation? Select all that apply, or skip to finish."

- Architecture (recommended for most projects)
- Testing conventions
- Product vision
- Contributing guide
- Implementation plan (PLAN.md)
- Skip — I'm done

### Flow for Each Selected Doc

For each doc the user selects:

**1. Ask targeted questions** (3-5, tailored to what was detected):

**Architecture (`docs/architecture.md`):**
- "What's the rationale behind your tech stack choices?" (pre-fill from detection)
- "Describe your core domain model — what are the key entities and their relationships?"
- "What are the main data flows? (e.g., user action → API → database → real-time update)"
- "How is this deployed? (Vercel, AWS, self-hosted, etc.)"
- "Any planned architectural changes or future components?"

**Testing (`docs/testing.md`):**
- "What's your testing philosophy? (e.g., test as user stories, test pyramid, TDD)"
- "File naming conventions for tests?" (pre-fill if detected: `*.test.ts`, `*.spec.ts`)
- "Any test data conventions? (factories, fixtures, test email domains, cleanup strategy)"
- "What should be unit tested vs E2E tested?"
- "Any testing-specific tooling? (MSW, test containers, custom fixtures)"

**Vision (`docs/vision.md`):**
- "What problem does this project solve?"
- "Who is the target audience?"
- "What differentiates this from alternatives?"
- "What's the core UX philosophy?"

**Contributing (`docs/contributing.md`):**
- "What are the steps to set up the dev environment from scratch?"
- "What's the PR process? (branch naming, review requirements, merge strategy)"
- "Any code review expectations?"
- "Required checks before merging? (tests, linting, type-check)"

**Implementation Plan (`PLAN.md`):**
- "What phase is the project in now?"
- "What's been completed so far?"
- "What are the next 3-5 steps?"
- "Any key decisions already made that should be recorded?"

**2. Generate the doc** from answers + detected signals. Follow the same writing rules as Phase 4: concrete, not generic. Use the template examples as quality benchmarks — read them from `references/claude-md-template.md` for format guidance.

**3. Show output and ask for adjustments.**

**4. Write the file** and update the Doc Index in AGENTS.md:
- Add a new entry in the pipe-delimited format
- Entry format: `|{key}:{{file path} - {compressed single-line summary}}`

**5. Move to the next selected doc** or finish.

### After All Docs Are Created

Show a summary of everything that was created:

```
## Created files:
- AGENTS.md
- CLAUDE.md → AGENTS.md (symlink, if opted in)
- docs/architecture.md
- docs/testing.md
(etc.)

Remember to commit these files to your repository.
```

---

## Update Mode

When running in update mode (existing AGENTS.md + `--update` flag or user chose "Update"):

1. **Run Phase 1 detection** as normal
2. **Read current AGENTS.md** content
3. **Diff detection against current content** — identify:
   - New technologies/tools detected but not in AGENTS.md
   - Directory structure changes
   - New documentation files not in the Doc Index
4. **Present proposed changes** to the user:
   ```
   ## Proposed Updates to AGENTS.md

   **Add to Tech Stack:**
   - Vitest (detected in devDependencies)

   **Update Structure:**
   - New directory: `apps/mobile/`

   **Update Doc Index:**
   - Add: docs/contributing.md

   **No changes to:**
   - Conventions (still accurate)
   - Project description
   ```
5. **Ask for approval** — user can accept all, pick specific changes, or cancel
6. **Apply approved changes** — edit the file, don't regenerate from scratch
7. **Never remove content without asking** — if something in AGENTS.md wasn't detected, ask before removing: "I didn't detect {X} anymore. Should I remove it from AGENTS.md?"
8. **Tech docs check** — check if `.docs/` exists and if any newly detected technologies are missing docs. If new technologies detected since last run, offer to fetch docs for them. If `.docs/` exists, verify the Tech Stack Docs Index in AGENTS.md matches the actual files — add/remove index entries as needed.
9. **Symlink check** — if `{create_symlink}` is true, verify the `CLAUDE.md` symlink still exists and points to `AGENTS.md`; recreate if broken
10. **Migration** — if only `CLAUDE.md` exists (no `AGENTS.md`), offer to migrate: rename `CLAUDE.md` to `AGENTS.md` and create a symlink back

---

## Important Guidelines

- **Use Glob and Read tools** for all file detection — never guess what exists
- **Read `references/claude-md-template.md`** before generating any AGENTS.md content — it contains the canonical format and examples
- **Don't fabricate information** — if you can't detect something and the user didn't mention it, leave it out
- **Keep AGENTS.md under 80 lines** — it's a quick reference, not exhaustive documentation
- **The Doc Index uses pipe-delimited format** — match the exact format shown in the template
- **Always create the `docs/` directory** before writing files into it
- **Update AGENTS.md's Doc Index** every time a new doc is created
- **When the user opts for a CLAUDE.md symlink**, create it using a relative path (`ln -s AGENTS.md CLAUDE.md`). Never write content to the symlink directly.
- **Use Context7 MCP tools** (`resolve-library-id` then `query-docs`) to fetch tech documentation. Limit to 3 queries per technology.
- **Save all tech documentation to `.docs/{technology}/`** using lowercase kebab-case directory names (e.g., `.docs/nextjs/`, `.docs/tailwindcss/`).
- **The Tech Stack Docs Index is separate from the project Doc Index.** Tech docs point to `.docs/`, project docs point to `./docs/` or `./`.
- **Ask the user about `.gitignore`** for `.docs/` — some teams want to commit docs for offline/CI use, others prefer to treat them as fetched artifacts.

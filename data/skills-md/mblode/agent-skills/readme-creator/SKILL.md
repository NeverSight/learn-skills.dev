---
name: readme-creator
description: Writes or rewrites README.md files tailored to the project type (CLI, library, app, framework, monorepo, or skill bundle). Discovers project context, selects the right structure, writes section by section, and validates against quality checks. Use when creating a README, writing a README from scratch, rewriting a bad README, bootstrapping project documentation, or asking "write a README for this project."
---

# README Creator

Write or rewrite a README.md tailored to the project type and audience.

## Reference Files

| File | Read When |
|------|-----------|
| `references/section-templates.md` | Phase 3: choosing structure and writing sections for a specific project type |
| `references/quality-checklist.md` | Phase 5: validating the finished README against quality standards |
| `references/badges-and-shields.md` | Phase 4: adding badges after the main content is written |

## README Workflow

Copy this checklist to track progress:

```text
README progress:
- [ ] Phase 1: Discover project context
- [ ] Phase 2: Choose README structure
- [ ] Phase 3: Write sections
- [ ] Phase 4: Add badges and extras
- [ ] Phase 5: Validate quality
```

### Phase 1: Discover project context

Read the project before asking questions. Explore files to detect the project type:

- Read `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, or equivalent for name, description, license, dependencies, scripts, and bin field.
- Read existing README.md (if rewriting).
- Scan directory structure to understand architecture.

Classify into one of six project types:

| Type | Signals |
|------|---------|
| CLI tool | `bin` field in package.json, `src/cli.ts`, commander/yargs dependency |
| Library / package | `main`/`exports` in package.json, no bin field, `src/index.ts` |
| Web app | `next.config.ts`, `vite.config.ts`, framework dependency, no npm publish |
| Framework | Plugin/middleware architecture, configuration API, extensibility points |
| Monorepo | `turbo.json`, `pnpm-workspace.yaml`, `apps/` + `packages/` directories |
| Skill bundle | `skills/` directory with SKILL.md files |

Ask the user only for what cannot be discovered from the code:
- What problem does the project solve? (the "why")
- Who is the target audience?
- Any sections to include or exclude?

### Phase 2: Choose README structure

Load `references/section-templates.md`.

Select sections based on the project type:

| Section | CLI | Library | App | Framework | Monorepo | Skills |
|---------|-----|---------|-----|-----------|----------|--------|
| Title + one-liner | yes | yes | yes | yes | yes | yes |
| Badges | yes | yes | -- | yes | yes | -- |
| Features / highlights | yes | yes | yes | yes | -- | yes |
| Install | yes | yes | -- | yes | yes | -- |
| Quick start / usage | yes | yes | yes | yes | yes | yes |
| Options / API reference | yes | yes | -- | yes | -- | -- |
| Configuration | opt | opt | yes | yes | opt | -- |
| Environment variables | -- | -- | yes | -- | -- | -- |
| Packages table | -- | -- | -- | -- | yes | -- |
| Skills table | -- | -- | -- | -- | -- | yes |
| Requirements | yes | yes | opt | yes | opt | -- |
| Contributing | opt | opt | opt | opt | opt | opt |
| License | yes | yes | yes | yes | yes | opt |

### Phase 3: Write sections

Load `references/section-templates.md`. Write each section following the template for the detected project type.

Key principles:
- Title is the project name. One-liner directly below, no heading.
- Feature list above the fold (before Install) so readers see value before effort.
- Install: single fastest path first. `npm install -g` for CLIs, `npm install` for libraries.
- Usage: 3-5 runnable examples, simplest first. Real values, not `foo` or `example`.
- Every code block must be copy-pasteable and runnable without modification.
- A reader should be able to install and run something within 60 seconds.
- Progressive disclosure: basic first, advanced later or in linked docs.

### Phase 4: Add badges and extras

Load `references/badges-and-shields.md`. Add badges only if the project is published to a registry. Place directly below the title and one-liner. Maximum 4 badges.

Skip badges entirely for private apps, unpublished projects, and skill bundles.

### Phase 5: Validate quality

Load `references/quality-checklist.md`. Run through every applicable check. Fix issues before finalizing.

After fixes, reread the README top to bottom to confirm it flows naturally.

## Anti-patterns

- Do not write a README longer than the codebase warrants
- Do not include a table of contents for READMEs under 100 lines
- Do not use "About" or "Introduction" as the first heading
- Do not ship the default create-next-app or create-vite README
- Do not include badges for unpublished projects
- Do not include a "Features" section that restates the one-liner
- Do not write "This project is..." or "This is a..." — describe what it does directly
- Do not include empty Contributing or Acknowledgements sections
- Do not use `foo`, `bar`, or `test` as example values

## Skill Handoffs

| When | Run |
|------|-----|
| After README is written, audit prose quality | `docs-writing` |
| If project needs AGENTS.md / CLAUDE.md | `agents-md` |

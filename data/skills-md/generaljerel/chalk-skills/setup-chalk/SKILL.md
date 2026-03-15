---
name: setup-chalk
description: Initialize .chalk folder with style transfer — analyze a repo and capture its architecture, coding style, tech stack, design assets, and color palette into structured docs
owner: chalk
version: "1.0.0"
metadata-version: "1"
allowed-tools: Read, Write, Glob, Grep, Shell
argument-hint: "[optional: path to repo root, defaults to current project]"
---

Initialize a `.chalk/` folder for any repository, focused on **style transfer** — capturing everything an AI agent needs to replicate the project's architecture, coding conventions, design system, and visual identity.

## What This Skill Produces

```
.chalk/
  chalk.json                          # Project metadata
  docs/
    product/
      0_PRODUCT_PROFILE.md            # What the product is, who it's for, core JTBD
    engineering/
      0_ENGINEERING_PROFILE.md        # Full technical overview (existing or generated)
      1_architecture.md               # Architecture patterns, process model, data flow
      2_coding-style.md               # Naming, file structure, component patterns, conventions
      3_techstack.md                   # Every dependency with version, purpose, and layer
    ai/
      0_AI_PROFILE.md                 # Agent-facing orientation, gotchas, quick reference
    design/
      0_design-system.md              # Master design doc: colors, typography, spacing, tokens
      assets/                         # Copied logos, icons, favicons, brand marks
        (icon.svg, icon.png, etc.)
```

## Workflow

### Phase 1 — Discover

1. **Locate the repo root** — Use `$ARGUMENTS` if provided, otherwise use the current working directory.
2. **Check for existing `.chalk/`** — If it already exists, warn the user and ask whether to merge or overwrite. If merging, skip files that already exist and only fill gaps.
3. **Scan the repo** — Read these files to understand the project:
   - `README.md` (or `readme.md`)
   - `package.json` / `Cargo.toml` / `pyproject.toml` / `go.mod` / `Gemfile` (dependency manifest)
   - `tsconfig.json` / `tsconfig.*.json` (TypeScript config)
   - Build configs: `vite.config.*`, `next.config.*`, `webpack.config.*`, `electron.vite.config.*`, `turbo.json`
   - Styling: `tailwind.config.*`, `postcss.config.*`, any `*.css` files in `src/`
   - `.eslintrc*`, `.prettierrc*`, `biome.json` (linter/formatter config)
   - `Dockerfile`, `docker-compose.yml` (infrastructure)
   - Existing `AGENTS.md` or `.cursorrules`

### Phase 2 — Analyze

4. **Map the architecture** — Identify:
   - Process model (monolith, microservices, Electron multi-process, SPA, SSR, etc.)
   - Directory structure patterns (feature folders, atomic design, domain-driven, etc.)
   - Entry points (main, renderer, worker, API routes)
   - Data flow (state management, IPC, API calls, database)
   - Key abstractions (hooks, services, stores, controllers)

5. **Extract coding style** — Analyze 3-5 representative files from different layers:
   - Naming conventions (PascalCase components, camelCase functions, kebab-case files)
   - Export patterns (default vs named, barrel files)
   - Component patterns (function components, props interface above component, hooks)
   - State management approach (hooks, context, stores, IPC)
   - Error handling patterns
   - Comment style and density
   - Import ordering conventions
   - TypeScript strictness (strict mode, any usage, type vs interface preference)

6. **Catalog the tech stack** — For every dependency:
   - Name and version
   - Layer (runtime, build, dev, test)
   - Purpose (one sentence)
   - Group by category (UI, state, routing, styling, testing, build, etc.)

7. **Extract design tokens** — Search for:
   - CSS custom properties (`--var-name` in CSS files)
   - Tailwind theme extensions (in `tailwind.config.*`)
   - Color values: scan components for recurring hex codes, Tailwind color classes (e.g., `emerald-500`, `gray-900`)
   - Typography: font families, font sizes, font weights used in CSS and components
   - Spacing patterns: recurring padding/margin values, gap values
   - Border radius values
   - Shadow definitions
   - Breakpoints and responsive patterns
   - Z-index layers

8. **Find brand assets** — Glob for:
   - `**/icon.{svg,png,ico,icns}`
   - `**/logo*.{svg,png,jpg}`
   - `**/favicon*.{svg,png,ico}`
   - `**/brand*.{svg,png}`
   - `resources/**/*.{svg,png}`
   - `public/**/*.{svg,png,ico}`
   - `assets/**/*.{svg,png}`

### Phase 3 — Generate

9. **Create `.chalk/chalk.json`**

```json
{
  "version": "1.0",
  "projectName": "<from package.json name or directory>",
  "createdAt": "<ISO timestamp>",
  "updatedAt": "<ISO timestamp>"
}
```

10. **Create `.chalk/docs/product/0_PRODUCT_PROFILE.md`**

Summarize:
- Product name and one-liner (from README or package.json description)
- Primary users
- Core jobs to be done (inferred from features)
- Current status

11. **Create `.chalk/docs/engineering/0_ENGINEERING_PROFILE.md`**

Comprehensive technical overview combining architecture, stack, and data flow. This is the canonical "read this first" doc for agents.

12. **Create `.chalk/docs/engineering/1_architecture.md`**

Focus on:
- Process/runtime model with ASCII or Mermaid diagram
- Directory structure with purpose annotations
- Entry points and boot sequence
- Data flow and state management
- IPC / API boundaries
- Key design patterns used

13. **Create `.chalk/docs/engineering/2_coding-style.md`**

Focus on:
- File and folder naming conventions
- Component/module structure patterns
- Naming conventions (variables, functions, types, files)
- Import ordering
- Export patterns
- Props/interface conventions
- State management patterns
- Error handling approach
- Comment conventions
- Code examples from the actual codebase showing each pattern

14. **Create `.chalk/docs/engineering/3_techstack.md`**

Table format with columns: | Package | Version | Layer | Category | Purpose |
Group by category. Include both dependencies and devDependencies.

15. **Create `.chalk/docs/ai/0_AI_PROFILE.md`**

Agent-facing quick reference:
- "Start here" orientation
- File locations for key functionality
- Common pitfalls and gotchas
- Conventions to follow when writing code
- What NOT to do

16. **Create `.chalk/docs/design/0_design-system.md`**

Comprehensive design reference:
- **Color palette** — Every color used, with hex values, Tailwind class names, and usage context (primary, accent, background, text, border, error, success, warning)
- **Typography** — Font families, size scale, weight scale, line heights
- **Spacing** — Common spacing values and their usage
- **Borders** — Border widths, styles, radius values
- **Shadows** — Shadow definitions
- **Component patterns** — Button styles, card styles, panel patterns
- **Dark/light mode** — If applicable, how themes are handled
- **Icon system** — Which icon library, common icons used

17. **Copy brand assets** — Copy logo/icon files to `.chalk/docs/design/assets/`:
   - Only copy files < 500KB
   - Prefer SVG over PNG over other formats
   - Rename to descriptive names if needed (e.g., `app-icon.svg`, `app-icon.png`)

### Phase 4 — Verify

18. **List created files** — Print a tree of everything created under `.chalk/`.
19. **Summarize** — Tell the user what was captured and any gaps (e.g., "No CSS custom properties found", "No logo files detected").

## Doc Format Rules

- No YAML frontmatter (plain markdown)
- First `# Heading` is the document title
- `Last updated: YYYY-MM-DD (<brief note>)` immediately after the title
- Use `## Heading` for sections
- GFM features: tables, code blocks, checkboxes, Mermaid diagrams
- Use real code examples from the repo, not generic placeholders
- Be specific and concrete — hex codes not "brand green", actual file paths not "components folder"

## Style Transfer Focus

The goal is **fidelity**. An AI agent reading these docs should be able to:

1. Write new code that looks like it belongs in the codebase (coding style)
2. Place files in the right directories following the right patterns (architecture)
3. Use the correct libraries and APIs (tech stack)
4. Match the visual design exactly — right colors, right spacing, right typography (design system)
5. Use the brand assets correctly (design assets)

Prioritize **concrete examples over abstract rules**. Show real code snippets, real hex values, real file paths.

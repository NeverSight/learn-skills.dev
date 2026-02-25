---
name: docs-steward
description: >-
  Maintain and enhance the Astro+Starlight docs site. Syncs generated pages,
  scores content quality, performs health checks, and proposes site improvements.
  Use when skills, agents, or MCP servers change. NOT for writing skills,
  creating agents, or building MCP servers.
argument-hint: "[sync|sync installed|enhance|maintain|improve|improve design|improve ux|full|auto]"
license: MIT
model: opus
metadata:
  author: wyattowalsh
  version: "2.0"
hooks:
  PostToolUse:
    - matcher: Write
      hooks:
        - command: |
            file="$TOOL_INPUT_file_path"
            if echo "$file" | grep -q 'docs/src/content'; then
              echo "MDX file modified — run pnpm build to verify" >&2
            fi
---

# Docs Steward

Maintain, enhance, and improve the docs site at `agents.w4w.dev`. The site
uses Astro + Starlight + starlight-theme-black. The `wagents` CLI generates
MDX content pages from repository assets (skills, agents, MCP servers). This
skill wraps that CLI and extends it with AI-powered enhancement, health
checks, and site improvement capabilities.

## When to Invoke

Invoke this skill after any of these events:

- Creating or modifying any `skills/*/SKILL.md`
- Creating or modifying any `agents/*.md`
- Creating or modifying any `mcp/*/server.py` or `mcp/*/pyproject.toml`
- Running `wagents new skill`, `wagents new agent`, or `wagents new mcp`
- Installing new skills via `npx skills add`

Auto-invocation is enabled by default (the `disable-model-invocation` field is absent, which defaults to `false`).

When invoked after asset changes, run in **auto mode** (default). No approval
gates, no user prompts. Detect what changed, regenerate, enhance, verify.

## Scope

**In scope:** Documentation site generation, MDX page enhancement, build verification, health checks, site configuration improvements, generation pipeline improvements, Astro component creation, CSS design system updates.

**NOT for:** Writing new skills (`/skill-creator`), creating agents (`wagents new agent`), building MCP servers (`/mcp-creator`), editing source SKILL.md or agent.md content, or managing the README (`wagents readme`).

## Dispatch

| $ARGUMENTS | Mode | Description |
|------------|------|-------------|
| (empty) or `auto` | Auto sync + enhance | Detect changes, regenerate, enhance new/changed pages |
| `sync` | Full sync | Force full regeneration + build verification |
| `sync installed` | Sync installed | Scan ~/.claude/skills/ for new/removed/changed installed skills, regenerate docs |
| `enhance` | Enhance all | Improve content quality across all generated pages |
| `enhance <path>` | Enhance one | Improve a specific page |
| `maintain` | Health check | Validate links, detect stale/orphans, check build |
| `improve` | Improve site | Research latest Starlight features, propose + implement improvements |
| `improve design` | Improve design system | Audit CSS tokens, identify gaps, propose design system upgrades |
| `improve ux` | Improve UX | Audit component slots, propose islands and interactive features |
| `improve cli` | Improve pipeline | Analyze and improve docs generation modules |
| `full` | Full run | Sync, then Maintain, then Enhance, then Improve (sequential) |

## Auto Mode (Default)

This is the primary mode. Run it when auto-triggered or when `$ARGUMENTS`
is empty or `auto`.

### Step 1: Detect Changes

Run these commands to identify changed asset files:

```bash
git diff --name-only HEAD
git status --porcelain
```

Filter results for asset files matching these patterns:
- `skills/*/SKILL.md`
- `agents/*.md`
- `mcp/*/server.py`
- `mcp/*/pyproject.toml`

If no asset files changed, report "No asset changes detected" and exit.

### Step 2: Regenerate Pages

Run the CLI to regenerate all content pages:

```bash
uv run wagents docs generate
```

This produces MDX files under `docs/src/content/docs/` for skills, agents,
and MCP servers based on their source assets.

### Step 3: Enhance Changed Pages

For each new or changed page, enhance it. Read the generated MDX and its
source asset side by side, then improve:

1. **Descriptions**: Expand truncated or generic descriptions into specific,
   compelling text that explains what the asset does and when to use it.
2. **Usage examples**: Add clear invocation instructions if missing. For
   skills: show the `/skill-name` command and argument patterns. For agents:
   show how to spawn or reference them. For MCP servers: show connection config.
3. **Visual elements**: Add Starlight components where they improve
   comprehension:
   - `Aside` callouts for tips, warnings, and important notes
   - `Steps` for sequential instructions
   - `Tabs` for configuration variants (different agents, different modes)
   - `CardGrid` with `Card` for related items or feature overviews
4. **Cross-references**: Link to related assets. A skill that uses MCP
   servers should link to them. An agent with preloaded skills should link
   to those skills.
5. **Section structure**: Verify heading hierarchy (single h1, logical h2/h3
   nesting). Reorganize if needed.

Consult `references/quality-checklist.md` for scoring criteria and
`references/starlight-patterns.md` for component usage patterns.

### Scaling Strategy

| Pages to enhance | Strategy |
|-----------------|----------|
| 1-3 pages | Inline — enhance sequentially in current session |
| 4-12 pages | Subagent wave — 1 subagent per page, parallel |
| 13+ pages | Batched waves — 5 pages per subagent, 2-3 sequential waves |

Each subagent receives: the current MDX content, the source SKILL.md or
agent.md, the quality checklist, and the Starlight patterns reference.

### Step 4: Verify Build

Run the docs build to confirm nothing is broken:

```bash
cd docs && pnpm build
```

If the build fails, diagnose the error, fix it, and rebuild.

### Step 5: Validate Assets

Run the wagents validator to confirm all assets are still valid:

```bash
uv run wagents validate
```

Fix any validation errors before finishing.

## Sync Mode

Force a full regeneration and build verification, regardless of what changed.

1. Run `uv run wagents docs generate`
2. Run `cd docs && pnpm build`
3. Report: number of pages generated, build status, any warnings

No enhancement in this mode. Use it to reset the generated pages to
CLI baseline.

## Sync Installed Mode

When `$ARGUMENTS` is `sync installed`:

Scan `~/.claude/skills/` for installed skills not already in the repo's
`skills/` directory. The `wagents docs generate` command handles this
automatically via `--include-installed` (enabled by default).

1. Run `uv run wagents docs generate` (includes installed skill scanning)
2. For installed skills with sparse descriptions (<50 tokens), spawn a
   subagent to read the full SKILL.md and write a richer description for
   the docs page
3. Run `pnpm --dir docs build` to verify
4. Report: number of installed skills found, new/removed since last sync

Run this mode after installing new skills via `npx skills add`.

## Enhance Mode

### Enhance All

When `$ARGUMENTS` is `enhance` with no path:

1. List all generated MDX files under `docs/src/content/docs/`
2. For each page, score it against all 9 dimensions in `references/quality-checklist.md`
3. Spawn parallel subagents (Pattern A from orchestration guide), one per
   page or batch of 3-5 related pages
4. Each subagent receives:
   - The current MDX content
   - The corresponding source asset (SKILL.md, agent.md, or MCP files)
   - The quality checklist
   - The Starlight patterns reference
5. Each subagent enhances the page and writes the result
6. After all subagents complete, run `cd docs && pnpm build` to verify
7. Run `uv run wagents validate`

### Enhance One

When `$ARGUMENTS` is `enhance <path>`:

1. Read the specified MDX file
2. Locate its source asset
3. Score against all 9 dimensions in quality checklist
4. Enhance in-place
5. Verify build and validate

## Maintain Mode

Run a comprehensive health check on the documentation site.

### Step 1: Build Check

```bash
cd docs && pnpm build
```

Capture output. Look for broken link warnings, missing image errors,
build failures.

### Step 2: Staleness Detection

Compare generated MDX page modification times against source asset
modification times. Flag pages that are older than their source (the CLI
was not re-run after the asset changed).

```bash
# Example: compare skills
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  source="$skill_dir/SKILL.md"
  generated="docs/src/content/docs/skills/$skill_name.mdx"
  # Compare mtimes
done
```

### Step 3: Orphan Detection

Find generated pages whose source assets no longer exist. These are
orphans left behind when an asset was deleted but `wagents docs generate`
was not re-run.

### Step 4: Validation

```bash
uv run wagents validate
uv run wagents readme --check
```

### Step 5: Report

Present findings grouped by severity:

- **Critical**: Build failures, broken links to external resources
- **Warning**: Stale pages, orphaned pages, validation errors
- **Info**: README out of date, minor inconsistencies

Offer to fix each category. Apply fixes in parallel where possible.

## Improve Mode

### Improve Site

When `$ARGUMENTS` is `improve`:

1. Research latest Starlight docs via Context7 or web search for new
   features, components, or best practices
2. Audit the site configuration:
   - `docs/astro.config.mjs` — plugins, integrations, sidebar config
   - `docs/src/styles/custom.css` — theming, visual polish
   - `docs/src/content/docs/index.mdx` — landing page
3. Propose improvements grouped by category:
   - **New pages**: Missing content that should exist
   - **Navigation**: Sidebar structure, grouping, ordering
   - **Visual**: Theme enhancements, component usage, layout
   - **SEO**: Meta descriptions, OpenGraph, structured data
   - **Performance**: Image optimization, build config
4. **Ask the user before implementing** — present proposals with effort
   estimates and let the user choose what to implement
5. Implement approved improvements

### Improve Design

When `$ARGUMENTS` is `improve design`:

1. Read `docs/src/styles/custom.css` and `references/site-architecture.md`
2. Check design system maturity against the checklist in `references/advanced-patterns.md`
3. Identify missing tokens (spacing, shadows, radius, motion, z-index)
4. Propose additions with before/after visual impact
5. **Ask the user before implementing**

### Improve UX

When `$ARGUMENTS` is `improve ux`:

1. Read component overrides in `docs/src/components/starlight/`
2. Check unused Starlight slots from `references/site-architecture.md`
3. Evaluate which interactive islands would have highest impact
4. Propose 3-5 improvements ranked by effort vs. impact
5. **Ask the user before implementing**

### Improve Pipeline

When `$ARGUMENTS` is `improve cli`:

1. Read the documentation generation modules:
   - `wagents/docs.py` — index pages, sidebar, CLI page, docs subcommands
   - `wagents/rendering.py` — MDX page renderers (skill, agent, MCP)
   - `wagents/parsing.py` — frontmatter parsing, text transforms, MDX escaping
   - `wagents/catalog.py` — asset collection, node/edge data model
2. Identify gaps in the generation pipeline
3. **Ask the user before implementing**
4. Implement, regenerate, verify build

## Full Mode

Execute all modes in sequence:

1. **Sync**: `uv run wagents docs generate`
2. **Maintain**: Full health check, fix critical issues
3. **Enhance**: Score and improve all pages (parallel subagents)
4. **Improve**: Research and propose site improvements (ask first)

## Reference Files

| File | Content | When to Read |
|------|---------|--------------|
| references/quality-checklist.md | 9-dimension page scoring rubric, enhancement patterns with before/after examples | Scoring or enhancing pages |
| references/starlight-patterns.md | 10+ Starlight component patterns with import conventions and escape rules | Adding components to MDX |
| references/site-architecture.md | Design system tokens, Astro component slots, plugin config, island patterns | Improve Site or Improve Design mode |
| references/advanced-patterns.md | Interactive islands, marketplace UX, content collections, performance optimization | Improve Site or Improve UX mode |

Read these before enhancement work. They define the quality bar and
component patterns to follow.

## Critical Rules

1. Never delete pages generated by `wagents docs generate` — only enhance them
2. Always run `uv run wagents validate` after any changes to asset files
3. Always run `cd docs && pnpm build` to verify the build after changes
4. Never modify CLI-generated frontmatter (title, description) during enhancement
5. Always import Starlight components at top of MDX files before use
6. Never introduce raw JSX that breaks MDX parsing — escape `{`, `<`, `>` in prose
7. Always read references before enhancement work
8. Never assign the same file to multiple parallel subagents
9. Always revert enhancements that break the build, then rebuild
10. Never add fabricated or speculative content — enhance from source asset only
11. Always call `wagents docs generate` as foundation — never bypass the CLI
12. Never implement `improve` or `improve cli` changes without user approval

**Canonical terms** (use these exactly throughout):
- Modes: "Auto", "Sync", "Sync Installed", "Enhance All", "Enhance One", "Maintain", "Improve Site", "Improve Design", "Improve UX", "Improve Pipeline", "Full"
- Enhancement dimensions: "description", "usage examples", "visual elements", "cross-references", "structure", "interactivity", "external links", "agent compatibility"
- Severity levels: "Critical", "Warning", "Info"
- Page types: "skill page", "agent page", "MCP page", "index page", "landing page", "CLI page", "guide page"
- Pipeline modules: `wagents/docs.py`, `wagents/rendering.py`, `wagents/parsing.py`, `wagents/catalog.py`
- Site layers: "generated content" (MDX pages), "design system" (CSS), "components" (Astro overrides), "islands" (interactive client-side), "plugins" (Starlight ecosystem)

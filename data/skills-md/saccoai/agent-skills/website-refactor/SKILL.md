---
name: website-refactor
description: End-to-end website refactoring workflow using agent teams. Orchestrates content-extraction, web-audit, and seo-migration skills as specialized teammates alongside a designer. Use when the user wants to rebuild, redesign, or migrate an existing website.
---

This skill orchestrates a complete website refactor using **Claude Code agent teams**. It composes four standalone skills — `website-analysis`, `design-system`, `web-audit`, and `seo-migration` — as specialized teammates that work in parallel alongside a `designer` agent.

The user provides: the URL of the existing site, the target tech stack, and design direction (preserve brand, modernize, or fully redesign).

## Prerequisites

1. Agent teams enabled:
```json
// ~/.claude/settings.json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

2. Companion skills installed (each teammate follows its respective skill):
```bash
npx skills add saccoai/agent-skills@website-analysis -g
npx skills add saccoai/agent-skills@design-system -g
npx skills add saccoai/agent-skills@web-audit -g
npx skills add saccoai/agent-skills@seo-migration -g
```

## Agent Team Roles

| Teammate | Skill used | Focus | Owns (read/write) |
|----------|-----------|-------|-------------------|
| **Lead** (you) | — | Orchestrator — creates team, defines tasks, coordinates handoffs | Team config, spec document |
| **content-extractor** | `website-analysis` | Crawl original site, extract all content and assets | `src/data/`, `scripts/extract/`, `public/images/`, `public/assets/`, `content-inventory.md` |
| **design-system-extractor** | `design-system` | Extract visual design tokens from the live site | `design-system/` (tokens.css, design-tokens.md, tailwind-theme.ts, screenshots/, assets/) |
| **designer** | `frontend-design` | Implement pages with agreed aesthetic, test responsive | `src/app/`, `src/components/`, `src/app/globals.css`, `tailwind.config.*` |
| **seo-manager** | `seo-migration` | Redirects, metadata, sitemap, structured data, robots.txt | `seo-migration-report.md`, redirect config, `app/sitemap.ts`, `app/robots.ts` |
| **qa-auditor** | `web-audit` | Lighthouse, a11y, cross-browser, performance, mobile | `qa-reports/`, `qa-summary.md`, `scripts/audit/` |

**Lead does NOT implement or audit directly.** Enable delegate mode (`Shift+Tab`) after spawning the team.

## Workflow

```
Phase 1: Extract + Plan          Phase 2: Setup       Phase 3: Design
┌──────────────────────┐         ┌──────────┐         ┌─────────────────┐
│  content-extractor   │────────▶│  Lead     │────────▶│    designer     │
│  (website-analysis   │         │  scaffold │         │  (frontend-     │
│   skill)             │         │  project  │         │   design skill) │
└──────────────────────┘         │  + apply  │         └────────┬────────┘
                                 │  design   │                  │
┌──────────────────────┐         │  tokens   │                  │
│  design-system-      │────────▶│          │                  │
│  extractor           │         └──────────┘                  │
│  (design-system      │              │                        │
│   skill)             │              │                        │
└──────────────────────┘              │                        │
                                      │                        │
┌──────────────────────┐              │                        │
│  Lead plans spec,    │──────────────┘                        │
│  asks user questions │                                       ▼
└──────────────────────┘                          Phase 4+5: Verify + Audit
                                          ┌─────────────────────────────────┐
                                          │  content-extractor  (re-crawl   │
                                          │  new site, diff with original)  │
                                          │                                 │
                                          │  seo-manager (redirects,        │
                                          │  sitemap, structured data)      │
                                          │                                 │
                                          │  qa-auditor (lighthouse, a11y,  │
                                          │  cross-browser, performance)    │
                                          └──────────────┬──────────────────┘
                                                         │
                                                         ▼ issues?
                                          ┌──────────────────────────────┐
                                          │  designer fixes issues       │
                                          │  (via SendMessage from Lead) │
                                          └──────────────┬───────────────┘
                                                         │
                                                         ▼
                                          ┌──────────────────────────────┐
                                          │  Phase 6: Deploy             │
                                          └──────────────────────────────┘
```

### Phase 1: Content Extraction + Design System + Planning

**Spawn `content-extractor`** immediately (no dependencies):

```
Spawn teammate "content-extractor" with prompt:
"Follow the website-analysis skill. Crawl {ORIGINAL_URL} and extract ALL content.
Target stack: {TECH_STACK}.
Save to: content-inventory.md, src/data/*.ts, public/images/, public/assets/.
Take full-page screenshots of every page to screenshots/."
```

**Spawn `design-system-extractor`** in parallel (no dependencies):

```
Spawn teammate "design-system-extractor" with prompt:
"Follow the design-system skill. Extract the complete design system from {ORIGINAL_URL}.
Save to: design-system/ (tokens.css, design-tokens.md, tailwind-theme.ts, screenshots/, assets/).
Validate on 2-3 inner pages for consistency."
```

**While both extractors work**, the Lead:
1. Reviews the original site structure
2. Asks the user clarifying questions (AskUserQuestion):
   - Pages to add, remove, or merge?
   - Design direction: preserve brand, modernize, or full redesign?
   - New features to add (contact form, analytics, CMS)?
   - Target deployment platform?
3. Drafts the spec document

**Quality gate**: content-extractor completes `content-inventory.md` AND design-system-extractor completes `design-system/tokens.css`. Lead reviews both with user.

### Phase 2: Project Setup

**Lead** scaffolds the project (sequential — must complete before Phase 3):
1. Initialize project with target stack
2. Copy `design-system/tokens.css` `@theme` block into `src/app/globals.css`
3. Set up shared layout components (header, footer, navigation)
4. Configure base metadata template
5. Copy extracted logos from `design-system/assets/` to `public/`
6. Document environment variables in `.env.example`

### Phase 3: Design & Implementation

**Spawn `designer`** (depends on: Phase 1 + Phase 2):

```
Spawn teammate "designer" with prompt:
"Follow the frontend-design skill. Implement all pages for {SITE_NAME}.
Stack: {TECH_STACK}. Design direction: {DESIGN_DIRECTION}. Brand: {BRAND_DETAILS}.

Content is in src/data/ and content-inventory.md — read these first.

Design tokens are in design-system/tokens.css — the @theme block is already in globals.css.
Reference design-system/design-tokens.md for the full type scale, spacing, button specs,
and component patterns. Visual references are in design-system/screenshots/.

CRITICAL: For EACH page:
1. Implement using extracted content AND extracted design tokens
2. Screenshot at 390px (mobile) AND 1280px (desktop) via Playwright
3. Fix responsive issues BEFORE moving to the next page
4. Mark the page task as complete

Order: layout → homepage → content pages → complex pages → detail pages."
```

**Spawn `seo-manager`** in parallel (depends on: Phase 1):

```
Spawn teammate "seo-manager" with prompt:
"Follow the seo-migration skill. Using content-inventory.md:
1. Build the redirect map (old URLs → new URLs)
2. Generate redirect config for {PLATFORM} (Next.js/Vercel/etc.)
3. Create app/sitemap.ts with all new pages
4. Create app/robots.ts
5. Add structured data (JSON-LD) to relevant pages: Organization, BreadcrumbList, etc.
6. Ensure every page has: title, description, canonical, OG tags

Save redirect map and structured data specs so designer can integrate them."
```

**Lead** creates TaskCreate entries for each page to track progress.

### Phase 4: Content Verification

**After designer completes**, re-use `content-extractor` for verification:

```
SendMessage to "content-extractor":
"Now verify the new site at {NEW_URL}. Re-crawl and diff against your original extraction.
Generate content-diff-report.md showing:
- ✅ Matching content
- ❌ Missing text, links, images, metadata
Target: 100% parity (or document approved exceptions)."
```

### Phase 5: Quality Audits (Parallel)

**Spawn `qa-auditor`** (depends on: Phase 3 complete):

```
Spawn teammate "qa-auditor" with prompt:
"Follow the web-audit skill. Audit {NEW_URL} — test EVERY page.
Run: Lighthouse, axe-core accessibility, cross-browser (Chromium/Firefox/WebKit),
performance budget (LCP/CLS/INP), mobile responsiveness (390×844).
Generate qa-summary.md with pass/fail per page and detailed reports in qa-reports/."
```

**`seo-manager` validates** redirects and SEO in parallel:

```
SendMessage to "seo-manager":
"The new site is live at {NEW_URL}. Validate:
1. Test every redirect (curl -I old URLs, confirm 301)
2. Verify no chains or loops
3. Confirm sitemap.xml is valid and accessible
4. Validate structured data with Rich Results Test
5. Check canonical URLs
Generate seo-migration-report.md."
```

**If issues are found**, Lead routes them to designer:

```
SendMessage to "designer":
"Issues to fix:
From qa-auditor:
- /about: LCP 3.2s (optimize hero image)
- /contact: missing form label

From seo-manager:
- /blog/old-post: redirect target returns 404
- /about: missing og:image tag

See qa-reports/ and seo-migration-report.md for details."
```

### Phase 6: Final Review & Deploy

**Lead** coordinates:
1. Confirm qa-summary.md — all audits pass
2. Confirm content-diff-report.md — 100% parity
3. Confirm seo-migration-report.md — all redirects work, structured data valid
4. Test interactive elements (forms, navigation, mobile menu)
5. Verify `.env.example` is complete
6. Deploy to staging → verify → deploy to production

## Task Dependencies

```
TaskCreate: "Extract content"              → no dependencies
TaskCreate: "Extract design system"        → no dependencies
TaskCreate: "Scaffold project"             → depends on: extract design system (for tokens)
TaskCreate: "Build redirect map"           → depends on: extract content
TaskCreate: "Implement homepage"           → depends on: scaffold, extract content, extract design system
TaskCreate: "Implement content pages"      → depends on: scaffold, extract content, extract design system
TaskCreate: "Implement complex pages"      → depends on: scaffold, extract content, extract design system
TaskCreate: "Generate sitemap + robots"    → depends on: all implementation
TaskCreate: "Verify content parity"        → depends on: all implementation
TaskCreate: "Run quality audits"           → depends on: all implementation
TaskCreate: "Validate SEO + redirects"     → depends on: all implementation
TaskCreate: "Fix issues"                   → depends on: audits + verification
TaskCreate: "Deploy"                       → depends on: fix issues
```

## Key Principles

- **Delegate, don't implement**: Lead orchestrates via TaskCreate + SendMessage. Teammates do the work.
- **Skills as contracts**: Each teammate follows its standalone skill as a playbook. The skills define what to extract, audit, or migrate.
- **Parallel where possible**: content-extractor + scaffold in parallel. qa-auditor + seo-manager + content-verifier in parallel after implementation.
- **File ownership prevents conflicts**: No two teammates write to the same files. See the roles table above.
- **Feedback loops**: qa-auditor finds issues → Lead routes to designer → designer fixes → qa-auditor re-validates.
- **3-5 teammates**: This workflow uses 5 teammates (content-extractor, design-system-extractor, designer, seo-manager, qa-auditor). Don't add more unless the project is very large.

## Common Pitfalls

- **Lead doing implementation**: Use delegate mode. If you catch yourself editing `page.tsx`, stop and SendMessage to designer.
- **Designer starts before content is ready**: Set task dependencies. Designer must wait for content-extractor.
- **Skipping SEO**: seo-manager is not optional. Every migration needs redirects and metadata preservation.
- **Single-pass QA**: Always do at least two passes — auditor finds issues, designer fixes, auditor re-validates.
- **File conflicts**: If seo-manager needs to add structured data to page files that designer owns, have seo-manager write specs to a file and designer integrates them.

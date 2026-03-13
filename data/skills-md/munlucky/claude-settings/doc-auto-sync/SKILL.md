---
name: doc-auto-sync
description: Detects code changes, auto-updates related docs (PROJECT.md, README, CHANGELOG, generated docs), and bootstraps project documentation structure.
---

# Doc Auto-Sync Skill

> **Purpose**: Auto-detect code changes → identify affected docs → update or bootstrap them.
> **When**: After implementation-runner, before codex-review-code.

---

## Inputs
- `analysisContext.repo.changedFiles` — list of changed files
- `analysisContext.request.taskType` — feature/bugfix/refactor
- `analysisContext.artifacts.tasksRoot` — task document root

## Workflow

### 1. Change Detection → Doc Mapping

Map changed files to affected docs:

```yaml
docMapping:
  "src/api/**":
    - "docs/generated/api-reference.md"
    - "README.md#api"
    - ".claude/PROJECT.md#api-data-patterns"
  "src/components/**":
    - "ARCHITECTURE.md#components"
  "prisma/schema.prisma|drizzle/*":
    - "docs/generated/db-schema.md"
    - ".claude/PROJECT.md#type-domain-patterns"
  "package.json":
    - "README.md#installation"
    - ".claude/PROJECT.md#stack"
  ".env*":
    - "README.md#configuration"
    - ".claude/PROJECT.md#environment-variables"
  "*.config.*":
    - ".claude/PROJECT.md#verification-commands"
```

### 2. PROJECT.md Auto-Sync

Detect and update the relevant PROJECT.md section:

| Trigger | Section |
|---------|---------|
| `package.json` / `pyproject.toml` / `go.mod` changed | `## Stack` |
| New directory created or structure change | `## Directory / Structure` |
| API route file changed | `## API / Data Patterns` |
| Type definition or schema file changed | `## Type / Domain Patterns` |
| `.env*` file changed | `## Environment Variables` |
| Test config file changed (`jest.config`, `vitest.config`) | `## Testing Rules` |
| `package.json` scripts / `Makefile` changed | `## Verification / Commands` |

**Rules:**
- Only update sections with actual changes (diff-based)
- **CRITICAL: Preserve user-written content.** 
  - For lists (e.g. Stack), append new items; do not remove existing ones.
  - For descriptions, only append new info if missing.
  - Do not overwrite custom notes or comments.
- Add `<!-- auto-synced: YYYY-MM-DD -->` comment to updated sections

### 3. Document Bootstrap (New Projects)

If key documents are missing, recommend creation:

```yaml
bootstrapRules:
  always:
    - CHANGELOG.md
  ifMissing:
    - condition: "estimatedLOC > 5000"
      create: "ARCHITECTURE.md (skeleton)"
    - condition: "API route files exist"
      create: "docs/generated/api-reference.md"
    - condition: "ORM schema files exist"
      create: "docs/generated/db-schema.md"
  neverForce:
    - docs/design-docs/
```

**Bootstrap runs only on first detection or explicit `--init` flag.**

### 4. Freshness Check

Compare doc last-modified vs related source last-modified:

```yaml
freshnessCheck:
  staleThreshold: "30 days"
  checks:
    - "ARCHITECTURE.md vs project structure"
    - "docs/generated/* vs source code"
    - ".claude/PROJECT.md vs actual project state"
```

Stale docs → add to output `staleDocs[]` for pre-flight-check to surface.

### 5. CHANGELOG Entry

Generate a changelog entry for commit-moonshot:

```yaml
changelog:
  format: "Keep a Changelog"
  sections: [Added, Changed, Deprecated, Removed, Fixed, Security]
  source: "git diff + commit messages + analysisContext.request.taskType"
```

---

## Output (patch)
```yaml
notes:
  - "doc-auto-sync: updated=[count], bootstrapped=[count], stale=[count]"

docSync:
  updatedDocs:
    - path: ".claude/PROJECT.md"
      sections: ["stack", "apiPatterns"]
    - path: "docs/generated/api-reference.md"
      action: "regenerated"
  bootstrappedDocs:
    - path: "CHANGELOG.md"
      action: "created"
  staleDocs:
    - path: "ARCHITECTURE.md"
      lastModified: "2025-01-15"
      relatedCodeModified: "2025-02-10"
  changelogEntry:
    type: "Added"
    description: "Payment API endpoint with coupon validation"
  projectMdChanges:
    - section: "stack"
      diff: "+stripe@14.0.0"
```

---

## Scale Guidance

| Scale | Auto-generate | Manual |
|-------|--------------|--------|
| **Small** (< 5K LOC) | `PROJECT.md` sync, `CHANGELOG.md` | `README.md` (initial) |
| **Medium** (5K~50K) | + `docs/generated/*`, `README.md` sections | + `ARCHITECTURE.md` |
| **Large** (50K+) | + full suite | + `docs/design-docs/*` |

## Recommended Docs Structure

```
{project-root}/
├── ARCHITECTURE.md              # Module codemap, boundaries, invariants
├── CHANGELOG.md                 # Auto-generated at commit
├── README.md                    # Section-level auto-update
│
├── docs/
│   ├── design-docs/             # Complex feature designs (manual, opt-in)
│   │   └── {feature}.md
│   └── generated/               # Auto-extracted from code
│       ├── api-reference.md
│       └── db-schema.md
│
└── .claude/
    ├── PROJECT.md               # Auto-synced sections
    └── docs/tasks/              # Default tasksRoot (or docs/exec-plans/)
```

> **Note**: `docs/exec-plans/` is an optional alternative to `.claude/docs/tasks/` for git-tracked task docs.
> Configure via `PROJECT.md: documentPaths.tasksRoot`.

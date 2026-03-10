---
name: skill-writer
description: Use when creating new skills, editing existing skills, optimizing skill descriptions and structure, splitting large skills into references, or validating skills against best practices
---

# Skill Writer

Create and optimize Claude Skills following best practices and validation rules.

## Core Principles

1. **Context is scarce** — Claude is already smart. Only add what it doesn't know. Challenge each paragraph: "Does this justify its token cost?"
2. **Description is the trigger** — Description determines WHEN a skill loads. It MUST describe triggering conditions, NEVER summarize workflow.
3. **Progressive disclosure** — Three-level loading: metadata (~100 tokens, always loaded) → SKILL.md body (<5000 tokens, on trigger) → references/scripts/assets (on demand, unlimited).
4. **English-first** — Write descriptions in English for reliable LLM matching. Body can be bilingual.
5. **Directive-style** — Use `MUST`, `NEVER`, `CRITICAL RULE` for hard constraints (not just "should" or "try to").
6. **No duplication** — Information lives in EITHER SKILL.md or references, never both. Keep core workflow in SKILL.md; move detailed reference material out.

## Skill Types

| Type | Purpose | Naming Convention | Example |
|------|---------|-------------------|---------|
| **Reference** | API docs, CLI guides, tool documentation | `<tool>-cli-guide`, `<lib>-sdk` | argocd-cli-guide |
| **Pattern** | Reusable code patterns and architecture | `<name>-pattern` | zustand-mutative-pattern |
| **Migration** | Version upgrade guides with before/after | `<lib>-v6-to-v7` | mikro-orm-v6-to-v7 |
| **Discipline** | Rules and workflows to enforce | `<name>-sops`, `<name>-lint` | biome-lint |

Personal/team patterns: prefix with `wode-` to distinguish from generic skills.

## Creation Workflow

### Step 1: Define Scope

```
Who will use this skill?
  ├─ Anyone (generic)         → skills repo, no hardcoded paths
  ├─ Only me (user-level)     → can hardcode user paths (~/gits/)
  ├─ One project              → can hardcode project paths, service names
  └─ One use-case             → can hardcode MCP server names, endpoints
```

See [references/patterns.md](references/patterns.md) for detailed scope analysis.

### Step 2: Write Frontmatter

```yaml
---
name: my-skill-name
description: Use when [specific triggering conditions and symptoms]
---
```

**Quick rules:**
- `name`: lowercase kebab-case, 1-64 chars, MUST match directory name
- `description`: "Use when..." format, single line, <500 chars, English

See [references/frontmatter.md](references/frontmatter.md) for full spec including optional fields.

### Step 3: Write Instructions

- Role setting: "You are an expert..." at the top
- Use diff blocks for before/after comparisons
- Extract rules from code comments to explicit bullet lists
- Include error troubleshooting table (symptom → cause → fix)
- One excellent code example beats many mediocre ones

### Step 4: Organize Resources

When SKILL.md approaches 500 lines or ~5000 tokens, split into bundled resources:

| Directory | Purpose | Loaded into context? |
|-----------|---------|---------------------|
| `references/` | Docs Claude reads while working | Yes, on demand |
| `scripts/` | Executable code for deterministic tasks | No (executed directly) |
| `assets/` | Files used in output (templates, images) | No (used in output) |

```markdown
# SKILL.md (overview + navigation)
## Quick Start
[Core instructions — enough to handle 80% of cases]

## Detailed Docs
- **API Reference**: See [references/api.md](references/api.md)
- **Config Guide**: See [references/config.md](references/config.md)
```

**Rules:**
- References only one level deep (no `references/sub/`)
- Add table of contents if file >100 lines
- For very large references (>10k words), include grep patterns in SKILL.md so Claude can search efficiently
- Link with relative paths: `[title](references/file.md)`

### Step 5: Validate

```bash
just lint-skills     # Check all skills
just fix-skills      # Auto-fix (e.g., flatten multiline descriptions)
just update-readme   # Regenerate README.md skills table
```

## Validation Rules

Enforced by `lint-skills.ts`:

| Rule | Level | Detail |
|------|-------|--------|
| SKILL.md exists | error | Every skill directory must have SKILL.md |
| Valid YAML frontmatter | error | `---` delimited block at top of file |
| `name` matches directory | error | `name: foo` must be in `skills/foo/` |
| `name` kebab-case | warn | `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` |
| `name` ≤ 64 chars | error | Hard limit from spec |
| `description` exists | error | Required field |
| `description` no newlines | warn | Must be single line (auto-fixable with `--fix`) |
| `description` ≤ 1024 chars | warn | Spec hard limit |
| `description` ≤ 500 chars | warn | Recommended for conciseness |
| `description` starts "Use when..." | warn | Best practice for triggering |
| No workflow summary in description | warn | Description = WHEN to use, not WHAT it does |
| Metadata ≤ 150 tokens | info | name + description always loaded in every conversation |
| Metadata ≤ 200 tokens | warn | Metadata is too heavy for "always in context" cost |
| Body ≤ 500 lines | warn | Move excess to `references/` |
| Body ≤ 5000 tokens | warn | ~4 chars per token estimate |

## Description Rules (CRITICAL)

**MUST:** Start with "Use when..." and describe triggering conditions only.

**NEVER:** Summarize what the skill does or its workflow in the description.

**WHY:** When a description summarizes workflow, Claude follows the description shortcut instead of reading the full skill body. This causes it to miss important details.

```yaml
# GOOD — triggering conditions only
description: Use when upgrading @mikro-orm packages from v6 to v7, fixing v7 runtime/type errors...

# BAD — summarizes workflow
description: Migrates MikroORM by replacing packages, renaming APIs, and updating decorators

# GOOD — reference skill with trigger keywords
description: Use when managing Kubernetes apps via argocd CLI, including syncing, diffing, or viewing logs

# BAD — too vague
description: ArgoCD CLI helper
```

**Trigger keywords** (e.g., `Triggers on "argocd sync"...`) are acceptable for reference skills, but avoid for pattern/discipline skills.

See [references/description-rules.md](references/description-rules.md) for full guidelines.

## Directory Structure

```
skill-name/
├── SKILL.md           # Required. Case-sensitive.
├── references/        # Docs loaded into context on demand
│   ├── api.md
│   └── config.md
├── scripts/           # Executable code (token efficient, deterministic)
└── assets/            # Output resources (templates, images, fonts)
```

**Do NOT include:** README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, or any auxiliary documentation. Skills contain only what an AI agent needs to do the job.

## External Skills

Track external skill sources in `skills/skills.json`:

```json
[
  { "repo": "vercel/ai", "path": "skills/use-ai-sdk", "name": "ai-sdk" }
]
```

Workflow: add entry → `just update-skills` → `just update-readme`

## Checklist

**Before creating:**
- [ ] Identify 2-3 concrete use cases
- [ ] Determine scope (generic / user / project / case)
- [ ] Choose type (reference / pattern / migration / discipline)

**During creation:**
- [ ] `name` kebab-case, matches directory, ≤64 chars
- [ ] `description` "Use when...", single line, English, <500 chars
- [ ] `description` has NO workflow summary
- [ ] Body <500 lines / <5000 tokens
- [ ] Heavy reference in `references/`
- [ ] Hard constraints use MUST / NEVER / CRITICAL RULE
- [ ] Code examples complete and runnable
- [ ] Error troubleshooting table included

**After creation:**
- [ ] `just lint-skills` — 0 errors
- [ ] `just update-readme` — table updated
- [ ] Test: relevant query triggers the skill
- [ ] Test: unrelated query does NOT trigger

## References

- [YAML Frontmatter Specification](references/frontmatter.md)
- [Description & CSO Rules](references/description-rules.md)
- [Skill Patterns & Scope](references/patterns.md)

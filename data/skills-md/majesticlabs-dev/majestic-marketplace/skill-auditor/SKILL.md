---
name: skill-auditor
description: Audit installed skills across project, global, and plugin levels. Lists skills with line counts, identifies improvement opportunities (conciseness, clarity, overlap, token waste). Use when reviewing skill quality, finding bloated skills, or optimizing token budgets.
allowed-tools: Bash Read Glob Grep AskUserQuestion
---

# Skill Auditor

## Workflow

### Step 1: Discover All Skills

Scan these locations for `SKILL.md` files:

| Level | Path |
|-------|------|
| Global | `~/.claude/skills/*/SKILL.md` |
| Project | `.claude/skills/*/SKILL.md` |
| Plugin | `plugins/*/skills/*/SKILL.md` |

For each skill found, collect:
- **Name**: from frontmatter `name:` field (fall back to directory name)
- **Level**: global / project / plugin (include plugin name for plugin skills)
- **Lines**: total line count of `SKILL.md`
- **Has allowed-tools**: yes/no
- **Description length**: character count of `description:` field

### Step 2: Present Summary Table

Sort by line count descending. Format:

```
| # | Level | Plugin | Skill Name | Lines | Status |
```

Status indicators:
- `OVER` — exceeds 500-line limit
- `HEAVY` — 300-499 lines (approaching limit)
- `OK` — under 300 lines

Include totals:
- Total skills per level
- Total lines across all skills
- Average lines per skill
- Skills exceeding limits

### Step 3: Ask User for Selection

Use `AskUserQuestion` to ask which skills to review. Suggest:
- All skills marked OVER or HEAVY
- Top 5 largest skills by line count
- Option to review by plugin name
- Option to review all skills at a specific level

### Step 4: Deep Review (per selected skill)

Read each selected skill fully. Evaluate against these criteria:

**Conciseness (token efficiency)**
- Lines that don't change LLM behavior (fluff, attribution, personas)
- Redundant explanations of concepts Claude already knows
- Verbose examples that could be compressed
- Sections that repeat CLAUDE.md rules

**Clarity**
- Ambiguous instructions that could be interpreted multiple ways
- Missing context that forces Claude to guess
- Inconsistent terminology within the skill

**Scope Overlap**
- Compare skill's purpose against other skills at same level
- Flag skills that cover substantially similar ground
- Identify candidates for merging or splitting

**Structure**
- Frontmatter completeness (name, description, allowed-tools)
- Description quality (too short = undiscoverable, too long = wasteful)
- Section organization (follows marketplace conventions?)

### Step 5: Report Findings

For each reviewed skill, output:

```
## {skill-name} ({lines} lines)

**Verdict:** {TRIM | RESTRUCTURE | MERGE | OK}

**Issues:**
- [CONCISENESS] {specific finding with line reference}
- [CLARITY] {specific finding}
- [OVERLAP] overlaps with {other-skill}: {shared scope}

**Suggested savings:** ~{N} lines ({percentage}% reduction)
**Recommended actions:**
1. {specific action}
2. {specific action}
```

### Step 6: Summary

After all reviews, provide:
- Total potential line savings
- Skills recommended for merging (with rationale)
- Priority order for improvements (highest token savings first)

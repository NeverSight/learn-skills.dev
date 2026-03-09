---
name: tuzi-update-claude-md
description: 分析代码审查反馈或开发中发现的问题，提取通用规则并更新 CLAUDE.md 和详细规则文档。当用户说"更新规则"、"添加编码规则"、"update claude md"或发现需要记录的编码模式时使用。
---

# Update CLAUDE.md

Analyzes code review feedback or development issues, extracts general rules, and updates documentation with a layered strategy (summary in CLAUDE.md, details in docs/CODING_RULES.md).

## Core Principle

**CLAUDE.md must stay concise.** Summary rules only, 1-2 sentences each.

| Document | Content | Line Limit |
|----------|---------|------------|
| `CLAUDE.md` | Core summary rules (1-2 sentences) | ≤ 300 lines |
| `docs/CODING_RULES.md` | Detailed rules + error/correct examples | No limit |
| `docs/FEATURE_FLOWS.md` | Feature flow documentation | No limit |

## Parameters

- `$ARGUMENTS`: Description of the discovered issue or rule (optional)

## Preferences (EXTEND.md)

Use Bash to check EXTEND.md existence (priority order):

```bash
# Check project-level first
test -f .tuzi-skills/tuzi-update-claude-md/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.tuzi-skills/tuzi-update-claude-md/EXTEND.md" && echo "user"
```

┌──────────────────────────────────────────────────────────┬───────────────────┐
│                           Path                           │     Location      │
├──────────────────────────────────────────────────────────┼───────────────────┤
│ .tuzi-skills/tuzi-update-claude-md/EXTEND.md            │ Project directory │
├──────────────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.tuzi-skills/tuzi-update-claude-md/EXTEND.md      │ User home         │
└──────────────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  Result   │                                  Action                                   │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Found     │ Read, parse, apply settings                                               │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Not found │ Use defaults                                                              │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

**EXTEND.md Supports**: CLAUDE.md line limit | Rule categories | Commit message format

## Workflow

### Step 1: Gather Information

**If `$ARGUMENTS` provided**: Parse the described issue or rule.

**If no arguments**: Ask user what issue was discovered, or check recent git diff and commit messages:

```bash
git diff HEAD~3 --stat
git log --oneline -5
```

### Step 2: Assess Rule Priority

| Priority | Criteria | Action |
|----------|----------|--------|
| High | Frequent error pattern, causes serious bugs, core project convention | Add to both CLAUDE.md + CODING_RULES.md |
| Normal | Occasional issue, scenario-specific, detailed examples | Only CODING_RULES.md |
| Skip | One-off typo, overly specific business logic, already covered | Do not record |

### Step 3: Check Document Status

```bash
wc -l CLAUDE.md
```

If over 250 lines, prompt user to clean up before adding.

### Step 4: Update docs/CODING_RULES.md

Add to the appropriate section using this format:

```markdown
### [Issue Title]

**Scenario**: [When this issue occurs]

❌ **Wrong**:
\`\`\`typescript
// incorrect code
\`\`\`

✅ **Correct**:
\`\`\`typescript
// correct code
\`\`\`

**Reason**: [Why]
```

**Section categories**: TypeScript | React Components | Service Worker | Cache & Storage | API & Task Processing | UI Interaction

### Step 5: Update CLAUDE.md (High Priority Only)

Add 1-2 sentence summary only:

```markdown
N. **Rule Name**: Brief description (1-2 sentences)
```

Location: Under `## 核心编码规则` or equivalent section.

### Step 6: Check for Duplicates

- Check both CLAUDE.md and CODING_RULES.md for similar existing rules
- Supplement existing rules rather than creating new ones
- Avoid document bloat from redundancy

### Step 7: Confirm Update

Display summary:

```
## Documentation Updated

### docs/CODING_RULES.md
- Section: [section name]
- Added: [rule description]
- Includes: Error/correct examples + explanation

### CLAUDE.md (if applicable)
- Section: [section name]
- Added summary: [rule summary]

### Document Status
- CLAUDE.md: XXX lines (limit 300) ✅/⚠️
- CODING_RULES.md: XXX lines
```

### Step 8: Commit

```bash
git add CLAUDE.md docs/CODING_RULES.md
git commit -m "docs: add coding rule - [rule name]"
```

## Periodic Cleanup

When CLAUDE.md approaches 300 lines:

1. Merge similar rules
2. Remove outdated rules
3. Move overly detailed rules to CODING_RULES.md
4. Update cross-references

## Example Usage

```bash
# With argument
/tuzi-update-claude-md Claude keeps forgetting to add theme='light' to TDesign Tooltip

# Interactive
/tuzi-update-claude-md
```

## Extension Support

Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options.

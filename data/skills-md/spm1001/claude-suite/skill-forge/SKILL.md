---
name: skill-forge
description: Orchestrates ALL skill development — MANDATORY gate BEFORE writing or editing any SKILL.md file. Invoke FIRST when building, validating, improving, or refactoring skills. Supersedes skill-creator. Unified 6-step workflow with automated validation, CSO scoring, and subagent testing. Triggers on 'create skill', 'new skill', 'validate skill', 'check skill quality', 'improve skill discovery', 'check this skill', 'write SKILL.md', 'edit SKILL.md', 'update skill description', 'can I share this', 'scan for sharing'. (user)
---

# Skill Forge

Unified skill development toolkit. Supersedes `skill-creator` — combines its creation process with quality validation, description optimization, and testing.

**Iron Law: Skills must be discovered to be useful.** The description is everything.

## When to Use

- **BEFORE** writing any SKILL.md file
- When creating a new skill from scratch
- When improving an existing skill's discovery rate
- When validating skill quality before deployment
- When scanning a skill/repo before sharing publicly

## When NOT to Use

- One-off instructions (put in CLAUDE.md instead)
- Simple tool usage Claude already knows
- Tasks that don't repeat across sessions

## Rationalizations to Block

Claude frequently skips this skill by reasoning:
- **"I already know how to create skills"** — You know the generic pattern. This skill adds CSO scoring, lint, and project-specific conventions you don't have in training.
- **"skill-creator covers this"** — skill-forge supersedes skill-creator. Use forge, not creator.
- **"I'll validate later"** — Validation after writing is expensive rework. Forge-first, always.
- **"This is just a small edit to an existing skill"** — Small edits to descriptions are exactly where CSO scoring matters most.

## Quick Start

```bash
# 1. Initialize new skill
scripts/init_skill.py my-skill --path ~/.claude/skills

# 2. Edit SKILL.md (see Workflow below)

# 3. Lint for structure issues
scripts/lint_skill.py ~/.claude/skills/my-skill

# 4. Score description quality (CSO)
scripts/score_description.py ~/.claude/skills/my-skill

# 5. Test with subagent (optional but recommended)
scripts/test_skill.py ~/.claude/skills/my-skill

# 6. Package for distribution (optional)
scripts/package_skill.py ~/.claude/skills/my-skill
```

## Workflow: 6-Step Process

### Step 1: Understand with Concrete Examples

**Goal:** Know exactly how the skill will be used before building.

Questions to answer:
- "What would a user say that should trigger this skill?"
- "Can you give examples of how this skill would be used?"
- "What should happen after the skill triggers?"

**Exit criterion:** Clear list of trigger phrases and expected behaviors.

### Step 2: Plan Reusable Contents

Analyze each example to identify:

| Content Type | When to Include | Example |
|--------------|-----------------|---------|
| `scripts/` | Same code rewritten repeatedly | `rotate_pdf.py` |
| `references/` | Documentation Claude should reference | `schema.md` |
| `assets/` | Files used in output (not loaded) | `template.pptx` |

**Exit criterion:** List of scripts/references/assets to create.

### Step 3: Initialize

```bash
scripts/init_skill.py <skill-name> --path <directory>
```

Creates SKILL.md template, example scripts/references/assets. Delete unneeded files.

### Step 4: Edit

**Order matters:**
1. Create scripts/references/assets first
2. Test scripts actually work
3. Write SKILL.md last (it references the resources)

#### SKILL.md Structure

```yaml
---
name: kebab-case-name
description: [See CSO Patterns below]
---
```

**Body sections:**
- Core principle / Iron Law
- When to Use / When NOT to Use
- Workflow with success criteria
- Anti-patterns
- Quick reference
- Integration with other skills

#### Naming

- Lowercase letters, numbers, hyphens only. Max 64 chars.
- **Must match directory name exactly.**
- Gerund or capability form preferred.

| Good | Bad | Why |
|------|-----|-----|
| `systematic-debugging` | `debug` | Verb, not capability |
| `workspace-fluency` | `utils` | Generic, no information |
| `test-driven-development` | `pdf-helper` | "helper" is meaningless |
| `desired-outcomes` | `my-skill` | Doesn't describe purpose |

#### CSO Patterns (Critical)

**The description determines discovery.** Pattern: `[ACTION TYPE] + [SPECIFIC TRIGGER] + [METHOD/VALUE PREVIEW]`

**Best: MANDATORY gate with BEFORE condition**
```yaml
description: MANDATORY gate before writing any SKILL.md file. Invoke FIRST when building new skills - provides structure, naming, and quality checklist that MUST be validated before deployment.
```
Why: "MANDATORY gate" not optional, "before writing" timing, "FIRST" positioning, "MUST" imperative.

**Good: Specific trigger with method preview**
```yaml
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - four-phase framework (root cause, pattern analysis, hypothesis testing, implementation) ensures understanding before solutions.
```
Why: specific trigger + timing gate + method preview + value statement.

**Good: Natural phrase triggers**
```yaml
description: Coach on outcome quality. Triggers on 'check my outcomes', 'is this a good outcome', 'review my Todoist' when discussing strategic work.
```
Why: explicit phrases in quotes, context qualifier.

**Bad patterns to avoid:**

| Pattern | Problem | Fix |
|---------|---------|-----|
| "Helps with..." | Vague, no trigger | Specific phrases in quotes |
| "Use when creating..." | Too generic | "MANDATORY gate before..." |
| No timing condition | Optional invocation | Add BEFORE/FIRST/MANDATORY |
| Generic actions | Claude "knows" without loading | Domain-specific phrases |
| Command doesn't name skill | Not discoverable | "**Invoke the `name` skill**" |

Run `scripts/score_description.py` to validate. See `references/cso-guide.md` for full guidance.

### Step 5: Validate

```bash
# Automated lint (structure, naming, frontmatter)
scripts/lint_skill.py <skill-path>

# CSO score (description quality)
scripts/score_description.py <skill-path>

# Subagent test (discovery + workflow)
scripts/test_skill.py <skill-path>
```

**All checks must pass before Step 6.**

### Step 6: Package (Optional)

```bash
scripts/package_skill.py <skill-path> [output-dir]
```

Creates `.skill` file (zip format) for distribution.

## Quality Checklist

### Structure
- [ ] SKILL.md under 500 lines
- [ ] Name matches directory exactly (kebab-case)
- [ ] Name is gerund/capability form
- [ ] Description is third-person ("Orchestrates", not "Use")
- [ ] Description includes trigger AND method AND timing
- [ ] Description ends with `(user)` tag for user-defined skills
- [ ] References one level deep from SKILL.md
- [ ] YAML frontmatter has name and description only

### Content
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Concrete examples, not abstract rules
- [ ] Configuration values justified
- [ ] Error handling documented
- [ ] Dependencies explicitly listed
- [ ] Anti-patterns section present

### Workflow
- [ ] Clear phases/steps with success criteria
- [ ] When to Use AND When NOT to Use sections
- [ ] Integration points with other skills explicit
- [ ] Verification/validation included
- [ ] Quick reference for common operations

### Discovery
- [ ] BEFORE/MANDATORY/FIRST patterns used appropriately
- [ ] Trigger phrases are natural language in quotes
- [ ] Context qualifiers included (when appropriate)
- [ ] Method preview gives Claude enough to decide relevance
- [ ] If paired with command, command names the skill explicitly

## Skill Patterns

See `references/skill-patterns.md` for full taxonomy. Summary:

| Type | Key Feature | Description Pattern |
|------|-------------|-------------------|
| **Process** | Phases with gates | BEFORE condition |
| **Fluency** | Tool best practices | Specific trigger phrases |
| **Coaching** | Quality criteria | Natural language triggers |
| **Gate** | Checklist validation | MANDATORY language |
| **Skill+CLI** | Orchestrates CLI tool | BEFORE any `cli` command |

### Skill+CLI Pattern (Most Powerful)

When skill orchestrates a CLI tool. See `references/skill-cli-pattern.md` for full template.

```markdown
# {skill-name}
Orchestrates {domain} using `{cli}` command.
## CLI Reference
## Workflows
## When Skill Extends CLI (coaching, quality criteria)
## Error Recovery
```

### What High-Invocation Skills Share

1. **BEFORE conditions** in description
2. **Specific trigger phrases** in quotes
3. **Method preview** that's actionable
4. **Clear anti-patterns** that catch mistakes
5. **Integration points** that compose with other skills

### What Low-Invocation Skills Suffer From

1. Generic "Use when..." descriptions
2. Vague propositions ("helps with", "guides", "assists")
3. Missing timing gates
4. Documenting what Claude already knows

## Anti-Patterns

### Discovery Failures

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| "Use when creating..." | Claude bypasses skill | "MANDATORY gate before..." |
| "Helps with..." | Never invoked | Specific trigger phrases |
| No timing gate | Optional invocation | Add BEFORE/FIRST |
| Generic actions | Claude "knows" without loading | Domain-specific phrases |

### Structure Failures

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| SKILL.md > 500 lines | Token bloat | Split into references/ |
| Name doesn't match dir | Skill not found | Keep synchronized |
| Deeply nested refs | Discovery fails | One level deep max |

### Content Failures

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| Explaining known things | Wastes tokens | Domain-specific only |
| Magic constants | Unclear reasoning | Justify all values |
| Many options, no default | Analysis paralysis | Recommend one path |

## Quick Reference

### Minimum Viable Skill

```markdown
---
name: kebab-case-name
description: [TIMING] + [TRIGGER] + [METHOD/VALUE]. Triggers on 'phrase1', 'phrase2'. (user)
---

# Skill Title

[Core principle]

## When to Use
[Specific triggers with examples]

## When NOT to Use
[Clear boundaries]

## Workflow
[Steps with success criteria]

## Anti-Patterns
[What to avoid with fixes]
```

### Files to Include

| File | Purpose | When Required |
|------|---------|---------------|
| SKILL.md | Core instructions | Always |
| references/*.md | Detailed guides | When SKILL.md > 500 lines |
| scripts/*.py | Utility scripts | When deterministic code needed |
| assets/* | Output templates | When Claude uses files in output |

## Before Sharing

Run the sharing scanner:

```bash
scripts/scan.py <skill-path>
scripts/scan.py --risk high <skill-path>  # High-risk only
```

Detects: emails, paths with usernames, secrets, company terms.
See `references/sharing-scan.md` for triage guidelines.

## Integration

**Anthropic scripts (symlinked from skill-creator):**
- `init_skill.py` — generate template
- `package_skill.py` — create .skill file

**Forge scripts:**
- `lint_skill.py` — automated structure validation
- `score_description.py` — CSO quality scoring
- `test_skill.py` — subagent pressure testing
- `scan.py` — PII/secrets scanner for sharing
- `render_graphs.py` — DOT workflow diagrams to SVG

## References

- `references/cso-guide.md` — Claude Search Optimization principles
- `references/skill-cli-pattern.md` — Skill+CLI template
- `references/skill-patterns.md` — Pattern taxonomy with examples
- `references/rationalization-table.md` — Common excuses to block
- `references/sharing-scan.md` — Sharing triage guidelines
- `references/dot-graphs.md` — DOT graph syntax for workflow diagrams

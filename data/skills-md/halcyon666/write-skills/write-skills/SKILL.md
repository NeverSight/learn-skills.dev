---
name: write-skills
description: Creates high-quality Agent Skills (SKILL.md files) that follow the open Agent Skills specification. Use when asked to create a skill, write a SKILL.md, package agent instructions, build a reusable capability, or turn a workflow into a shareable skill. Produces spec-compliant, concise, well-structured skills optimized for agent discovery and execution.
---

# Write Skills

Create Agent Skills that are spec-compliant, concise, and effective. A skill is a directory containing a `SKILL.md` file with YAML frontmatter and Markdown instructions that extend agent capabilities.

## When to Use

- User asks to "create a skill", "write a SKILL.md", or "make this reusable"
- Packaging a workflow, domain expertise, or tool integration as a shareable skill
- Turning a successful task pattern into a repeatable capability
- Reviewing or improving an existing skill

## Skill Creation Workflow

### Step 1: Understand the Domain

Before writing, identify:

1. **What capability** does this skill provide?
2. **When should an agent activate** this skill? (trigger phrases, task types)
3. **What does the agent NOT already know?** (only add novel context)
4. **What's the failure mode** without this skill? (guides what to include)

### Step 2: Create the Directory

```bash
# Using the skills CLI
npx skills init my-skill-name

# Or manually
mkdir my-skill-name && touch my-skill-name/SKILL.md
```

### Step 3: Write the SKILL.md

Every SKILL.md has two parts: YAML frontmatter and Markdown body.

#### Frontmatter Rules

```yaml
---
name: my-skill-name
description: Does X and Y. Use when the user asks about Z or needs to accomplish W.
---
```

**Required fields:**

| Field | Constraints |
|-------|-------------|
| `name` | 1-64 chars. Lowercase letters, numbers, hyphens only. No leading/trailing/consecutive hyphens. Must match directory name. |
| `description` | 1-1024 chars. Third person. Describes what it does AND when to use it. Include trigger keywords. |

**Optional fields:**

| Field | Purpose |
|-------|---------|
| `license` | License name or reference (e.g., `MIT`, `Apache-2.0`) |
| `compatibility` | Environment requirements (e.g., `Requires git and docker`) |
| `metadata` | Key-value pairs (e.g., `author`, `version`) |
| `allowed-tools` | Space-delimited pre-approved tools (experimental) |

**Name conventions** (prefer gerund form):
- `processing-pdfs`, `analyzing-data`, `writing-tests`
- Also acceptable: `pdf-processing`, `data-analysis`
- Avoid: `helper`, `utils`, `tools`, vague nouns

**Description rules:**
- ALWAYS third person ("Processes files..." not "I process files..." or "You can use this to...")
- Include BOTH what it does AND when to activate
- Include specific trigger keywords agents use for discovery
- Be specific: "Generates commit messages by analyzing git diffs" not "Helps with git"

#### Body Content Rules

The Markdown body is loaded when the skill activates. Every token competes with conversation context.

**Core principle: The agent is already smart. Only add what it doesn't know.**

Challenge every line:
- "Does the agent need this explanation?" (probably not for common knowledge)
- "Does this paragraph justify its token cost?" (cut if no)
- "Am I explaining what a PDF is?" (don't)

**Target: under 500 lines.** If longer, split into reference files.

### Step 4: Structure the Body

Use this skeleton, adapting sections to the skill's domain:

```markdown
# Skill Title

Brief one-line purpose statement.

## When to Use

Bullet list of activation triggers and scenarios.

## Instructions

Step-by-step workflow. Use numbered steps for sequential tasks,
bullets for parallel/unordered items.

## Examples (if needed)

Input/output pairs showing expected behavior.

## Common Pitfalls (if needed)

Known failure modes and how to avoid them.
```

**Degrees of freedom** - match specificity to fragility:

| Situation | Freedom Level | Style |
|-----------|--------------|-------|
| Multiple valid approaches | High | Text instructions, general guidance |
| Preferred pattern exists | Medium | Pseudocode or parameterized scripts |
| Fragile/critical operations | Low | Exact scripts, explicit "do not modify" |

### Step 5: Add Reference Files (If Needed)

When SKILL.md exceeds ~300 lines, split into progressive disclosure:

```
my-skill/
├── SKILL.md              # Overview + navigation (<500 lines)
├── references/
│   ├── api-reference.md  # Loaded on demand
│   └── examples.md       # Loaded on demand
└── scripts/
    └── validate.py       # Executed, not loaded into context
```

**Rules for references:**
- Keep references ONE level deep from SKILL.md (no nested chains)
- Link explicitly: `See [API Reference](references/api-reference.md) for details`
- Files >100 lines should have a table of contents at top
- Use forward slashes in paths (even on Windows)

### Step 6: Validate

Check the skill against these criteria before shipping:

```
Validation Checklist:
- [ ] name: lowercase, hyphens, 1-64 chars, matches directory
- [ ] description: third person, includes triggers, <1024 chars
- [ ] Body: under 500 lines
- [ ] No time-sensitive information (dates, "current version")
- [ ] Consistent terminology throughout
- [ ] No unnecessary explanations of common knowledge
- [ ] References are one level deep (no nested chains)
- [ ] All file paths use forward slashes
- [ ] Scripts handle errors explicitly (no punting to agent)
```

If the `skills-ref` CLI is available:
```bash
skills-ref validate ./my-skill
```

## Quality Patterns

### Effective Descriptions (Examples)

```yaml
# Good - specific, includes triggers
description: Generates release notes from git history using conventional commits. Use when asked to create a changelog, write release notes, or summarize changes between versions.

# Good - clear capability + activation
description: Reviews React components for performance anti-patterns and suggests optimizations. Use when writing, reviewing, or refactoring React/Next.js code.

# Bad - vague
description: Helps with code.

# Bad - first person
description: I can help you write better code.
```

### Workflow Pattern

For multi-step tasks, provide a copyable checklist:

```markdown
## Workflow

Copy this checklist and track progress:

- [ ] Step 1: Analyze input
- [ ] Step 2: Generate plan
- [ ] Step 3: Validate plan
- [ ] Step 4: Execute
- [ ] Step 5: Verify output
```

### Feedback Loop Pattern

For tasks requiring validation:

```markdown
1. Generate output
2. Run validation: `python scripts/validate.py output.json`
3. If validation fails:
   - Review error messages
   - Fix issues
   - Re-validate
4. Only proceed when validation passes
```

### Template Pattern

Provide output templates when format consistency matters:

````markdown
## Output Format

Use this structure:

```markdown
# [Title]

## Summary
[One paragraph]

## Details
[Structured content]
```
````

### Conditional Workflow Pattern

Guide through decision points:

```markdown
## Choose Your Path

1. Determine the task type:
   - **Creating from scratch?** -> Follow "Creation" section
   - **Modifying existing?** -> Follow "Editing" section
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Fix |
|-------------|-------------|-----|
| Explaining common knowledge | Wastes tokens, agents already know | Cut it |
| Multiple tool options without default | Confuses agent | Pick one default, mention alternatives briefly |
| Vague description | Agent can't discover the skill | Be specific with triggers |
| First/second person in description | Breaks discovery when injected into system prompt | Use third person |
| Windows-style paths (`\`) | Breaks on Unix systems | Use forward slashes |
| Deeply nested references | Agent may partially read files | Keep one level deep |
| Time-sensitive content | Becomes wrong over time | Use "current" vs "legacy" sections |
| Magic numbers in scripts | Agent can't reason about values | Document why each value was chosen |
| Empty error handling | Failures become opaque | Handle errors explicitly with messages |

## Publishing

Once the skill is ready, publish it so others can install it:

1. Push the skill directory to a GitHub repository
2. Users install with: `npx skills add owner/repo`
3. The skill appears on the [skills.sh](https://skills.sh) leaderboard via anonymous telemetry when installed
4. To list without installing: `npx skills add owner/repo --list`

For multi-skill repos, place skills under a `skills/` directory:

```
my-repo/
└── skills/
    ├── skill-one/
    │   └── SKILL.md
    └── skill-two/
        └── SKILL.md
```

## Quick Reference: Spec Constraints

| Field | Max Length | Format |
|-------|-----------|--------|
| `name` | 64 chars | `[a-z0-9-]`, no leading/trailing/double hyphens |
| `description` | 1024 chars | Third person, non-empty |
| `compatibility` | 500 chars | Optional |
| SKILL.md body | ~500 lines | Markdown, no format restrictions |
| Reference depth | 1 level | From SKILL.md only |

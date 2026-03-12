---
name: creating-skills
description: Guides creation of agent skills following best practices and the open format specification. Covers pattern selection, frontmatter, directory structure, reference files, validation, and iteration. Use when creating a new skill, updating SKILL.md, or asking "how to write a skill"
---

# Creating Skills

This skill walks you through creating a well-structured agent skill from scratch.
Follow the workflow below step by step. Use the reference files for detailed guidance on specific topics.

## Reference Files

| File | Read When |
|------|-----------|
| `references/format-specification.md` | Checking format rules, frontmatter constraints, or naming conventions |
| `references/skill-patterns.md` | Choosing a skill pattern or viewing skeleton templates |
| `references/workflow-and-output-patterns.md` | Designing workflows, output formats, or feedback loops |
| `references/quality-checklist.md` | Running the pre-ship quality checklist |
| `references/anti-patterns.md` | Reviewing common mistakes to avoid |
| `references/evaluation-guide.md` | Creating evaluations to measure skill quality objectively |
| `references/hooks-recipes.md` | Setting up hooks in skills or understanding hook patterns |

## Core Principles

Before diving into mechanics, internalize these design principles:

**Context window is a public good.**
Every token in a skill competes with the user's code, conversation, and other tools.
Challenge each line with three questions: (1) Does Claude already know this? (2) Will the agent use this on every invocation? (3) Can this live in a reference file instead?

**Degrees of freedom.**
Match your specificity to the task's tolerance for variation:

| Level | When | Example |
|-------|------|---------|
| **High specificity** | Output must be exact (configs, schemas) | "Generate exactly this YAML structure" |
| **Medium specificity** | Process matters, details vary (workflows) | "Follow these steps, adapt to the project" |
| **Low specificity** | Agent judgment is the point (reviews, analysis) | "Check for these categories of issues" |

**Claude is already smart.**
Don't teach programming, well-known APIs, or common patterns.
Only add context Claude doesn't already have: project conventions, domain rules, non-obvious constraints.

**Enforce mechanically, not with checklists.**
If the skill's purpose is catching problems (review, audit, compliance), it should generate hooks, lint rules, or check scripts that run automatically — not be a list of things the agent must remember to check. A PostToolUse hook runs on every file edit; a skill instruction relies on agent discipline.

**Don't duplicate existing tools.**
Before building a skill, check what linters, formatters, and CI tools already handle in the target ecosystem. If ESLint catches unused imports, don't create a skill that also checks for them. Skills should add value beyond what standard tooling provides.

## Choose a Skill Pattern

Before writing anything, identify which pattern fits the task:

| Pattern | Best For | Example |
|---------|----------|---------|
| **Guided Workflow** | Multi-step processes with decisions | `creating-skills`, `deploying-apps` |
| **Rules-Based Audit** | Code review, linting, compliance | `reviewing-typescript`, `auditing-security` |
| **Scaffolding / Generation** | Creating files from templates | `generating-apis`, `initializing-projects` |
| **Knowledge Reference** | Lookup tables, conventions, mappings | `mapping-status-codes`, `converting-units` |

**Not sure?** Ask these questions:
1. Does the task have sequential steps? → Guided Workflow
2. Is it about checking/validating? → Rules-Based Audit
3. Does it produce files from templates? → Scaffolding / Generation
4. Is it primarily informational? → Knowledge Reference

Read `references/skill-patterns.md` for full skeleton templates and directory structures.

## Creation Workflow

Copy this checklist and work through it step by step:

```
- [ ] Step 1: Understand the skill
- [ ] Step 2: Choose a pattern
- [ ] Step 3: Initialize the skill
- [ ] Step 4: Write the SKILL.md body
- [ ] Step 5: Add reference files
- [ ] Step 6: Validate
- [ ] Step 7: Create evaluations
- [ ] Step 8: Test with real usage
- [ ] Step 9: Iterate
```

### Step 1: Understand the Skill

Before writing any files, have a conversation to clarify:

- **What does this skill do?** Get a one-sentence answer.
- **Who triggers it?** What prompts or situations should activate it?
- **What's the output?** Files created, code reviewed, information provided?
- **What does the agent need to know?** Domain knowledge, project conventions, constraints?
- **What does the agent already know?** Don't include common programming knowledge.

Synthesize into a draft description using the formula:
`[Does what] for/using [domain]. [Checks/covers what]. Use when [triggers]`

### Step 2: Choose a Pattern

Use the decision table above to select a primary pattern.
Most skills combine patterns — pick the dominant one and incorporate elements from others.

For example, `creating-skills` is primarily a Guided Workflow but includes:
- Rules-Based Audit elements (validation checklist)
- Scaffolding elements (init script)

### Step 3: Initialize the Skill

**Quick start** with the official CLI:

```bash
npx skills init <skill-name>
```

Or use the enhanced scaffolding script (includes best-practice guidance in the template):

```bash
python scripts/init_skill.py <skill-name> --path skills
```

This creates:
```
skills/<skill-name>/
├── SKILL.md          (template with TODOs)
└── references/       (empty, ready for use)
```

If not using the script, create this structure manually. The name must be kebab-case, preferably with a gerund first word (e.g., `analyzing-data`, not `data-analyzer`).

### Step 4: Write the SKILL.md Body

Open the generated `SKILL.md` and fill it in:

1. **Frontmatter**: Fill in `name` and `description`
   - Name: kebab-case, must match directory name
   - Description: third-person voice, recommend under 300 characters (spec max 1024), include "Use when" triggers
   - See `references/format-specification.md` for the full spec

2. **Reference Files table**: List every reference file with a "Read When" condition

3. **Main content**: Follow the skeleton for your chosen pattern
   - Target 150–300 lines for the body
   - Hard limit: 500 lines (agents lose focus beyond this)
   - Use progressive disclosure — put detailed content in reference files
   - Use ATX headings, fenced code blocks with language tags
   - One sentence per line for clean diffs

4. **Workflows**: Use copyable checklists for sequential steps
   - See `references/workflow-and-output-patterns.md` for patterns

### Step 5: Add Reference Files

Create reference files in `references/` for detailed content that would bloat the main SKILL.md.

Common reference file types:
- **Rules and specifications** — naming conventions, format constraints, allowed values
- **Examples** — input/output pairs, good/bad comparisons
- **Detailed step guides** — expanded instructions for complex steps
- **Decision matrices** — comparison tables for choosing between options

Rules for reference files:
- One level deep only (no nested directories under `references/`)
- Every file must be listed in the SKILL.md "Reference Files" table
- Files over 100 lines should include a table of contents
- Use kebab-case file names

### Step 6: Validate

Run the validator against your skill:

```bash
python scripts/validate_skill.py skills/<skill-name>
```

The validator checks:
- Frontmatter format and required fields
- Name matches directory, kebab-case format
- Description length and voice
- Body line count
- File references exist on disk
- No Windows-style paths
- No deeply nested references
- Reference files are listed in the body

For official spec compliance, also run: `skills-ref validate skills/<skill-name>`
(install: `pip install skills-ref`)

**Fix all errors** (blocking). **Review all warnings** (advisory — fix or acknowledge).

If errors persist after 3 attempts, review `references/anti-patterns.md` for common mistakes.

Also run through the manual `references/quality-checklist.md` for items the automated validator cannot check (content quality, token efficiency, terminology consistency).

### Step 7: Create Evaluations

Before testing, define what success looks like.
Write 3–5 evaluation cases that cover the happy path, an edge case, and a failure mode you anticipate.
See `references/evaluation-guide.md` for the full methodology and JSON format.

Key steps:
1. **Establish a baseline**: Complete the target task **without** the skill installed. Record where the agent struggles.
2. **Write evaluation cases**: Each is a prompt + expected behaviors checklist.
3. **Score the baseline**: This is the bar your skill must beat.

### Step 8: Test with Real Usage

Automated validation catches format issues but not usability problems. Test with real tasks:

1. **Install the skill**: Copy to `~/.claude/skills/` or use `npx skills add`
2. **Start a fresh session**: The agent should not have prior context about this skill
3. **Trigger naturally**: Use a prompt that would naturally activate the skill
4. **Evaluate the output**: Did the agent follow the workflow? Was the output correct?

**What to observe** during testing:
- Does the agent explore unexpected paths not covered by the skill?
- Does the agent miss connections between sections that seem obvious to you?
- Does the agent over-rely on one section while ignoring others?
- Is there content the agent consistently skips or ignores?

**Multi-model testing**: Test with at least two capability levels:
- **Haiku**: Can the skill work with a smaller model? Simplify if not.
- **Sonnet/Opus**: Does the skill produce high-quality output with a capable model?

If the skill fails or produces poor output, go back to Step 4 and revise.

### Step 9: Iterate

Skills improve through real usage and feedback.

**Establish a baseline first**: If you haven't already (Step 7), complete the target task without the skill to see what the agent does on its own.
This reveals which parts of your skill actually add value vs. what the agent already handles.

**Use the Claude A/B pattern**:

1. **Claude A**: Use the skill as-is with a real task. Note where it struggles.
2. **Claude B**: Open a new session. Describe the problems. Ask Claude B to suggest improvements to the SKILL.md.
3. **Apply and re-test**: Incorporate the suggestions, then repeat from Step 6.

**Gather team feedback**: If others use the skill, ask them what worked and what didn't.
Different users trigger skills differently — their experience reveals gaps your testing missed.

This external feedback loop catches blind spots that self-review misses.

## Anti-Patterns Quick Reference

Avoid these common mistakes (see `references/anti-patterns.md` for full details):

| Anti-Pattern | Fix |
|-------------|-----|
| Over-explaining (things Claude already knows) | Only include domain-specific or non-obvious info |
| Windows-style backslash paths | Always use forward slashes |
| Deeply nested references | Keep `references/` one level deep |
| Too many options without a default | Always recommend a default |
| "When to use" in body instead of description | Put triggers in the frontmatter `description` |
| Unlisted reference files | List every file in the Reference Files table |
| Time-sensitive claims | Use evergreen phrasing or link to sources |
| Wrong voice in description | Use third-person: "Guides..." not "Guide..." |
| Building enforcement as a checklist | Generate hooks, lint rules, or check scripts instead |
| Duplicating linter/formatter functionality | Check what tools exist first; skills should add value beyond standard tooling |
| Platform-specific scripts without fallbacks | Scripts must work on both Windows and macOS/Linux — branch on `platform.system()` where needed |

## Related Skills

When using this skill alongside others:

- After creating a skill, use a **reviewing** skill to audit it against project standards
- For skills that generate code, pair with a **testing** skill to validate output
- For API-related skills, consider a **documenting** skill for endpoint coverage

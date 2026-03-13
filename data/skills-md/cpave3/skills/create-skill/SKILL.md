---
name: create-skill
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations. Also use when users want to run evals to test a skill, benchmark skill performance, optimize a skill's description for better triggering accuracy, or when they say "turn this into a skill". Trigger on any mention of creating, writing, building, improving, or testing skills.
---

# Create Skill

Create new skills and iteratively improve them through testing and evaluation.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized one equipped with procedural knowledge no model can fully possess.

Skills provide: specialized workflows, tool integrations, domain expertise, and bundled resources (scripts, references, assets).

## Core Principles

### Concise is Key

The context window is a public good shared with system prompt, conversation history, other skills, and user requests. **Claude is already very smart** — only add context it doesn't already have. Challenge each piece: "Does Claude really need this?" and "Does this justify its token cost?" Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match specificity to the task's fragility and variability:

- **High freedom** (text instructions): Multiple valid approaches, context-dependent decisions
- **Medium freedom** (pseudocode/parameterized scripts): Preferred pattern exists, some variation acceptable
- **Low freedom** (specific scripts, few parameters): Fragile operations, consistency critical, exact sequence required

Think of Claude exploring a path: a narrow bridge needs guardrails (low freedom), an open field allows many routes (high freedom).

### Explain the Why

Explain *why* things are important rather than using heavy-handed MUSTs. LLMs have good theory of mind — when given reasoning, they go beyond rote instructions. If you find yourself writing ALWAYS or NEVER in all caps, reframe and explain the reasoning instead.

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description — required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

### SKILL.md (required)

- **Frontmatter** (YAML): `name` and `description` fields only. The description is the primary triggering mechanism — Claude reads it to decide when to use the skill. All "when to use" info goes here, not in the body.
- **Body** (Markdown): Instructions and guidance. Only loaded after the skill triggers.

### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability or that get rewritten repeatedly.

- **When to include**: Same code rewritten repeatedly, deterministic reliability needed, errors need explicit handling
- **Benefits**: Token efficient, deterministic, may execute without loading into context
- **Test added scripts** by actually running them to verify correctness

### References (`references/`)

Documentation loaded into context as needed.

- **When to include**: Database schemas, API docs, domain knowledge, company policies, detailed workflow guides
- **Avoid duplication**: Information lives in either SKILL.md or references, not both. Keep SKILL.md lean; move detailed reference material to separate files.
- **Large files** (>300 lines): Include a table of contents. If >10k words, include grep patterns in SKILL.md.

### Assets (`assets/`)

Files used in output, not loaded into context.

- **When to include**: Templates, images, icons, boilerplate code, fonts, sample documents
- **Benefits**: Separates output resources from documentation

### What NOT to Include

Do NOT create extraneous files: README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md, etc. The skill should only contain what an AI agent needs to do the job.

## Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — When skill triggers (<500 lines ideal)
3. **Bundled resources** — As needed (unlimited; scripts can execute without loading)

Keep SKILL.md under 500 lines. When approaching this limit, split content into separate files with clear references describing when to read them.

**Pattern 1: High-level guide with references**
```markdown
## Quick start
[Minimal working example]

## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md)
- **API reference**: See [REFERENCE.md](REFERENCE.md)
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```
Claude reads only the relevant reference for the user's query.

**Pattern 3: Conditional details** — Show basics, link to advanced content only when needed.

**Guidelines:**
- Keep references one level deep from SKILL.md
- For files >100 lines, include a table of contents

## Skill Creation Process

Figure out where the user is in this process and help them progress. Maybe they want to create from scratch, or maybe they already have a draft and want to iterate.

### Step 1: Capture Intent

Start by understanding what the skill should do. The conversation may already contain a workflow to capture (e.g., "turn this into a skill") — extract what you can from history first.

Key questions (don't overwhelm — start with the most important):
1. What should this skill enable Claude to do?
2. When should it trigger? (specific phrases, contexts, file types)
3. What's the expected output format?
4. What specific use cases should it handle?
5. Does it need executable scripts or just instructions?
6. Any reference materials to include?

Check available MCPs for research. Come prepared with context to reduce burden on the user.

### Step 2: Plan Reusable Resources

Analyze each concrete example by considering how to execute it from scratch, then identifying what scripts, references, and assets would help when executing repeatedly.

**Examples:**
- PDF rotation → `scripts/rotate_pdf.py` (same code rewritten each time)
- Frontend webapp → `assets/hello-world/` template (same boilerplate each time)
- BigQuery queries → `references/schema.md` (re-discovering schemas each time)

Create a list of reusable resources: scripts, references, and assets.

### Step 3: Create and Implement

Create the directory structure. Only create subdirectories the skill actually needs — most skills need just SKILL.md and perhaps one resource directory.

Implement the planned resources. This may require user input (e.g., brand assets, documentation). Test added scripts by running them.

### Step 4: Write SKILL.md

The skill is for another Claude instance. Include information beneficial and non-obvious to Claude — procedural knowledge, domain details, reusable assets. Use imperative/infinitive form.

#### Writing the Description

The description is **the only thing the agent sees** when deciding which skill to load. It must provide enough info to know:
1. What capability this skill provides
2. When/why to trigger it (keywords, contexts, file types)

**Format:**
- Max 1024 characters
- Third person voice
- First sentence: what it does
- Second sentence: "Use when [specific triggers]"
- Make descriptions slightly "pushy" — Claude tends to under-trigger. Instead of just describing functionality, explicitly list contexts that should trigger the skill, even non-obvious ones.

**Good:** "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction."

**Bad:** "Helps with documents."

#### Writing the Body

**Output format patterns:**
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
```

**Example patterns:**
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

Reference any bundled resources and describe clearly when to read them.

### Step 5: Review

After drafting, verify:
- [ ] Description includes specific triggers ("Use when...")
- [ ] Description is slightly pushy (lists non-obvious trigger contexts)
- [ ] SKILL.md under 500 lines
- [ ] No time-sensitive info (dates, versions that will go stale)
- [ ] Consistent terminology throughout
- [ ] Concrete examples included
- [ ] References one level deep, clearly linked from SKILL.md
- [ ] No extraneous documentation files
- [ ] Scripts tested and working

Present the draft to the user:
- Does this cover your use cases?
- Anything missing or unclear?
- Should any section be more/less detailed?

### Step 6: Test and Evaluate

After the skill draft is ready, create 2-3 realistic test prompts and run them. See [references/eval-workflow.md](references/eval-workflow.md) for the complete testing and evaluation workflow, including:
- Spawning with-skill and baseline runs
- Drafting quantitative assertions
- Grading, benchmarking, and launching the eval viewer
- Reading user feedback

Save test cases to `evals/evals.json`. See [references/schemas.md](references/schemas.md) for the JSON schema.

If the user prefers to skip formal evals ("just vibe with me"), that's fine — adapt to their preference.

### Step 7: Iterate and Improve

This is the heart of the loop. Apply feedback from user evaluation:

1. **Generalize from feedback** — The skill will be used across many prompts, not just test examples. Avoid fiddly, overfitting changes. If something is stubbornly wrong, try different metaphors or patterns rather than adding rigid constraints.

2. **Keep the skill lean** — Remove what isn't pulling its weight. Read transcripts, not just outputs — if the skill makes the model waste time unproductively, trim those parts.

3. **Look for repeated work** — If all test runs independently wrote similar helper scripts, bundle that script in `scripts/`. Save every future invocation from reinventing the wheel.

4. **Apply, rerun, review, repeat** — After improving, rerun all test cases into a new iteration directory. Keep going until the user is happy, feedback is empty, or no meaningful progress.

See [references/eval-workflow.md](references/eval-workflow.md) for detailed iteration mechanics.

## Description Optimization

After creating or improving a skill, offer to optimize the description for better triggering accuracy. This uses an automated loop that tests different descriptions against eval queries.

See the "Description Optimization" section in [references/eval-workflow.md](references/eval-workflow.md) for the full workflow including trigger eval generation, review, and the optimization loop.

## Reference Files

### Agents (read when spawning specialized subagents)
- [agents/grader.md](agents/grader.md) — How to evaluate assertions against outputs
- [agents/comparator.md](agents/comparator.md) — How to do blind A/B comparison between outputs
- [agents/analyzer.md](agents/analyzer.md) — How to analyze benchmark results and why one version beat another

### References
- [references/schemas.md](references/schemas.md) — JSON schemas for evals.json, grading.json, timing.json, benchmark.json, comparison.json, analysis.json
- [references/eval-workflow.md](references/eval-workflow.md) — Detailed eval/testing/benchmarking workflow, iteration mechanics, description optimization, and environment-specific instructions

### Scripts
- `scripts/run_loop.py` — Automated description optimization loop
- `scripts/run_eval.py` — Execute evaluation queries
- `scripts/aggregate_benchmark.py` — Calculate benchmark statistics
- `scripts/improve_description.py` — Optimize skill descriptions
- `scripts/generate_report.py` — Create HTML reports
- `scripts/package_skill.py` — Package skills for distribution
- `scripts/quick_validate.py` — Quick validation utility

### Assets
- `assets/eval_review.html` — HTML template for eval query review
- `eval-viewer/generate_review.py` — Generate the eval results viewer
- `eval-viewer/viewer.html` — HTML viewer for eval results

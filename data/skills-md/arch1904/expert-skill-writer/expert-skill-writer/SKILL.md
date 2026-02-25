---
name: expert-skill-writer
description: >
  Write production-quality skills for Claude from scratch or improve existing ones.
  Use this skill whenever the user wants to author a SKILL.md, design a skill folder,
  write skill instructions, craft frontmatter descriptions, structure a multi-file skill,
  or get guidance on skill architecture and best practices. Also use when the user says
  "write a skill", "build a skill", "create a skill for X", "help me make a skill",
  "improve this skill", "review my skill", or asks about skill structure, trigger phrases,
  progressive disclosure, or skill design patterns. This skill focuses on the writing
  craft — producing well-structured, effective skill content — not on eval/benchmark
  workflows.
metadata:
  author: arch1904
  version: 1.0.0
  source: The Complete Guide to Building Skills for Claude (Anthropic, Jan 2026)
  repository: https://github.com/arch1904/expert-skill-writer
license: MIT
---

# Expert Skill Writer

You are an expert skill author. Your job is to help the user write, review, or improve
Claude skills — the folders of instructions that teach Claude how to handle specific
tasks and workflows. Everything you know about skill writing comes from Anthropic's
official guide. You are opinionated, precise, and thorough.

## Your Process

Adapt to where the user is. They might arrive with a blank slate, a rough idea, an
existing SKILL.md that needs work, or a conversation they want captured as a skill.
Regardless of entry point, move through these phases:

### Phase 1: Understand Intent

Before writing anything, get clear on:

1. **What should this skill enable Claude to do?** — Get concrete. "Helps with projects"
   is not an answer. "Orchestrates sprint planning in Linear by fetching project status,
   analyzing velocity, suggesting prioritization, and creating tasks" is.
2. **When should this skill trigger?** — What phrases would a real user actually say?
   What file types might be involved? What contexts indicate this skill is needed?
3. **What's the expected output?** — A document? A workflow execution? A code file?
   A series of MCP calls?
4. **What category does this fall into?** — Consult `references/skill-categories.md`
   for the three primary categories: Document/Asset Creation, Workflow Automation,
   or MCP Enhancement. Most skills lean toward one.

If the conversation already contains a workflow the user wants to capture (e.g., they
say "turn this into a skill"), extract answers from the conversation history first — the
tools used, the sequence of steps, corrections the user made, input/output formats
observed. Then confirm with the user before proceeding.

### Phase 2: Design the Architecture

Before writing the SKILL.md, decide on the skill's structure:

**Folder structure** — Every skill needs at minimum:
```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional - executable code
├── references/       # Optional - docs loaded as needed
└── assets/           # Optional - templates, fonts, icons
```

**Progressive disclosure** — Skills use a three-level loading system. This is a core
design principle; get it right:

- **Level 1 (YAML frontmatter):** Always loaded in Claude's system prompt. Provides
  just enough for Claude to know *when* to use the skill. Keep this tight — the
  description field is the most important part of the entire skill.
- **Level 2 (SKILL.md body):** Loaded when Claude decides the skill is relevant.
  Contains the full instructions. Keep under 500 lines; under 5,000 words.
- **Level 3 (Linked files):** Additional files in scripts/, references/, assets/ that
  Claude navigates only as needed. Use these for detailed docs, large reference
  materials, and executable code.

The goal: minimize token usage while maintaining specialized expertise.

**Composability** — Your skill will coexist with others. Do not assume it's the only
capability available. Write instructions that work well alongside other loaded skills.

**Portability** — Skills work identically across Claude.ai, Claude Code, and API.
Write once, works everywhere (provided the environment supports any dependencies).

### Phase 3: Write the Frontmatter

This is the most important part. The YAML frontmatter determines whether Claude
ever loads your skill. Consult `references/frontmatter-spec.md` for the complete
specification.

**The description field is everything.** Structure it as:

`[What it does] + [When to use it] + [Key capabilities]`

Rules for writing descriptions:
- MUST include BOTH what the skill does AND when to use it (trigger conditions)
- Include specific phrases users would actually say
- Mention relevant file types if applicable
- Stay under 1024 characters
- No XML angle brackets
- Be slightly "pushy" — Claude tends to undertrigger skills, so err on the side of
  making it clear when the skill should activate. Instead of just stating what it does,
  explicitly say "Use when..." and list trigger contexts generously.

Write descriptions, then review them by asking: "If Claude read only this description,
would it know exactly when to load this skill and when not to?" If no, rewrite.

### Phase 4: Write the Instructions

The body of SKILL.md is where the real craft lives.

**Start from this recommended structure** and adapt it for the specific skill:

```markdown
---
name: your-skill
description: [What it does. Use when user asks to ...]
---

# Your Skill Name

# Instructions

# Step 1: [First Major Step]
Clear explanation of what happens.

Example:
\`\`\`bash
python scripts/fetch_data.py --project-id PROJECT_ID
\`\`\`
Expected output: [describe what success looks like]

(Add more steps as needed)

# Examples
Example 1: [common scenario]
User says: "Set up a new marketing campaign"
Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters
Result: Campaign created with confirmation link

(Add more examples as needed)

# Troubleshooting
Error: [Common error message]
Cause: [Why it happens]
Solution: [How to fix]

(Add more error cases as needed)
```

Then apply these principles throughout:

**Use the imperative form.** You're giving Claude direct instructions, not writing
documentation for humans.

**Be specific and actionable.**
```
# Good
Run `python scripts/validate.py --input {filename}` to check data format.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)

# Bad
Validate the data before proceeding.
```

**Explain the why, not just the what.** Today's LLMs are smart. They have good theory
of mind and when given a good understanding of *why* something matters, they go beyond
rote instructions and really deliver. If you find yourself writing ALWAYS or NEVER in
all caps or using super rigid structures, that's a yellow flag — reframe and explain
the reasoning so the model understands why.

**Include error handling.** For every workflow step, anticipate what can go wrong and
tell Claude what to do about it:
```
# Common Issues

# MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Check Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect
```

**Provide examples.** Show Claude what good input/output looks like for common
scenarios:
```
## Examples
Example 1: [common scenario]
User says: "Set up a new marketing campaign"
Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters
Result: Campaign created with confirmation link
```

**Use progressive disclosure in the body too.** Keep SKILL.md focused on core
instructions. Move detailed documentation, API references, and large examples to
`references/` files and link to them clearly with guidance on when to read them.
For large reference files (over 300 lines), include a table of contents.

**For critical validations, consider bundling a script** that performs the checks
programmatically rather than relying on language instructions. Code is deterministic;
language interpretation is not.

**Keep the prompt lean.** Remove things that are not pulling their weight. If
instructions are making the model waste time on unproductive steps, cut them. Every
line should earn its place.

### Pro Tip: Iterate on a Single Task First

Before broad testing, the most effective skill creators iterate on a single challenging
task until Claude succeeds, then extract the winning approach into the skill. This
leverages Claude's in-context learning and provides faster signal than broad testing.
Once you have a working foundation, expand to multiple test cases for coverage.

### Phase 5: Review and Validate

Before declaring the skill done, run through the quality checklist in
`references/quality-checklist.md`. Key checks:

**Structural validation:**
- Folder named in kebab-case
- SKILL.md file exists with exact spelling (case-sensitive)
- YAML frontmatter has `---` delimiters
- `name` field is kebab-case, no spaces, no capitals
- `description` includes WHAT and WHEN
- No XML angle brackets anywhere
- No README.md inside the skill folder

**Content validation:**
- Instructions are clear and actionable
- Error handling included for workflows
- Examples provided for common scenarios
- References clearly linked with guidance on when to read them

**Triggering validation** — mentally test:
- Would this trigger on obvious task requests?
- Would this trigger on paraphrased versions of those requests?
- Would this avoid triggering on unrelated topics?

**Debugging tip:** Ask Claude "When would you use the [skill name] skill?" Claude
will quote the description back. Adjust based on what's missing.

## Anti-Patterns to Avoid

**Vague descriptions.** "Helps with projects" will never trigger correctly. Be specific.

**Missing trigger phrases.** "Creates sophisticated multi-page documentation systems"
sounds impressive but gives Claude no signal about *when* to load it.

**Too-technical descriptions with no user triggers.** "Implements the Project entity
model with hierarchical relationships" — no real user would say this.

**Instructions too verbose.** If SKILL.md is bloated, Claude's attention degrades.
Keep it focused; move detail to references.

**Instructions buried.** Put critical instructions at the top. Use clear headers.
Repeat key points if needed.

**Ambiguous language.**
```
# Bad
Make sure to validate things properly

# Good
CRITICAL: Before calling create_project, verify:
- Project name is non-empty
- At least one team member assigned
- Start date is not in the past
```

**Overtriggering.** If your skill loads for everything, add negative triggers:
```
description: Advanced data analysis for CSV files. Use for statistical
modeling, regression, clustering. Do NOT use for simple data exploration
(use data-viz skill instead).
```

**Oppressively constrictive MUSTs.** Rather than piling on rigid rules, explain the
reasoning. Generalize from specific feedback rather than overfitting to examples.

## Workflow Patterns

When the skill involves multi-step workflows, consult `references/workflow-patterns.md`
for the five proven patterns: Sequential Orchestration, Multi-MCP Coordination,
Iterative Refinement, Context-Aware Tool Selection, and Domain-Specific Intelligence.
Choose the pattern that fits the use case, or combine patterns as needed.

## Writing Style for Skills

- Use the imperative form in instructions
- Explain *why* things matter, not just *what* to do
- Be specific and actionable — vague instructions produce vague results
- Keep the tone direct but not robotic; skills are for AI agents but clarity matters
- Start with a draft, then look at it with fresh eyes and improve it
- Use theory of mind — try to make the skill general, not narrowly fitted to specific
  examples
- For large skills, add hierarchy with clear pointers about where to go next

## Presenting the Skill

After writing the skill, present it to the user as a downloadable folder. If the
`present_files` tool is available, package the skill and share it. Always explain:

1. What the skill does and when it triggers
2. The folder structure and what each file contains
3. How to install it (upload to Claude.ai via Settings > Capabilities > Skills,
   or place in Claude Code skills directory)
4. Suggested test prompts to verify it works

## A Note on Quality

This task matters. Skills get used across many conversations by many users. A
well-written skill creates compounding value; a poorly-written one creates
compounding frustration. Take your time. Write a draft, review it critically, and
improve it before presenting. Really try to understand what the user wants and
needs, then transmit that understanding into clear, effective instructions.

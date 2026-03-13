---
name: skill-forge
description: Build, validate, and iterate on Claude skills from scratch or from existing workflows. Use whenever someone wants to create a skill, turn a workflow into a skill, improve an existing skill, review a skill for quality, package a skill for upload, or asks about skill best practices. Also triggers on phrases like "make a skill", "build a skill", "skill for X", "turn this into a skill", "skill template", or "help me with SKILL.md".
---

# Skill Forge

You are a skill-building expert. Your job is to help users create high-quality, production-ready Claude skills — fast. A good skill should be buildable in 15-30 minutes.

## Core Philosophy

Skills teach Claude **once** so users benefit **every time**. The best skills are specific, actionable, and embed domain expertise that would otherwise need to be re-explained in every conversation.

Three things matter most:
1. **The description field** — this is how Claude decides whether to load your skill. Get it wrong and nothing else matters.
2. **Progressive disclosure** — don't dump everything into SKILL.md. Use references/ for depth.
3. **Specificity over completeness** — a skill that does one thing brilliantly beats one that does ten things vaguely.

---

## Modes

Detect which mode the user needs based on context:

### Create Mode
User wants to build a new skill. Follow the **Skill Creation Workflow** below.

### Improve Mode  
User has an existing skill that isn't performing well. Follow the **Improvement Loop** below.

### Review Mode
User wants feedback on a skill they've written. Run the **Quality Audit** below.

### Extract Mode
The current conversation already contains a workflow the user wants to capture as a skill. Mine the conversation for: tools used, step sequences, corrections made, input/output formats. Then fast-track into Create Mode with pre-filled answers.

---

## Skill Creation Workflow

### Step 1: Capture Intent (2-3 minutes)

Get answers to these questions — extract from conversation history first if the user said "turn this into a skill":

1. **What should this skill enable?** Get a concrete description, not abstract goals.
2. **Who is the user?** Technical depth matters — a developer skill reads differently from a non-technical workflow.
3. **What are 2-3 specific use cases?** Real scenarios with trigger phrases.
4. **What's the output?** Files, messages, API calls, structured data?
5. **What tools are needed?** Built-in (code execution, file creation) or MCP servers?

Identify which **skill category** this falls into:

| Category | Description | Example |
|----------|-------------|---------|
| Document & Asset Creation | Consistent, high-quality output generation | Frontend design, docx, pptx |
| Workflow Automation | Multi-step processes with methodology | Sprint planning, onboarding |
| MCP Enhancement | Workflow guidance on top of MCP tool access | Sentry code review, Linear workflows |

### Step 2: Draft the Skill (5-10 minutes)

Create the folder structure:

```
skill-name/
├── SKILL.md          # Required — main instructions
├── scripts/          # Optional — executable code for deterministic tasks
├── references/       # Optional — detailed docs loaded as needed
└── assets/           # Optional — templates, fonts, icons
```

**Critical rules:**
- Folder name: `kebab-case` only (no spaces, underscores, or capitals)
- File must be exactly `SKILL.md` (case-sensitive)
- No `README.md` inside the skill folder
- No XML angle brackets (`<` `>`) in YAML frontmatter
- No "claude" or "anthropic" in the skill name

#### Writing the Frontmatter

This is the most important part. The description is how Claude decides whether to load your skill.

```yaml
---
name: your-skill-name
description: [WHAT it does] + [WHEN to use it with specific trigger phrases] + [key capabilities]
---
```

**Description writing rules:**
- Must include BOTH what the skill does AND when to use it
- Under 1024 characters
- Include specific phrases users would actually say
- Mention relevant file types if applicable
- Be slightly "pushy" — Claude tends to undertrigger, so err on the side of broader matching
- Include negative triggers if there's confusion risk ("Do NOT use for X")

Good descriptions follow this pattern:
```
[What it does]. Use when [trigger conditions]. Handles [key capabilities]. 
Do NOT use for [disambiguation if needed].
```

**Test your description mentally:** If a user said each of these, would Claude know to load the skill?
- The obvious request ("help me do X")
- A paraphrased version ("I need to set up Y")  
- An indirect reference ("can you handle the Z thing")

#### Writing the Instructions

Use the imperative form. Explain **why** things matter, not just what to do. Today's models are smart — they respond better to understanding than to rigid MUST/NEVER rules.

Structure the SKILL.md body like this:

```markdown
# Skill Name

Brief overview of what this skill does and the value it provides.

## Instructions

### Step 1: [First Major Step]
Clear explanation with specifics.

Example:
\`\`\`bash
python scripts/process.py --input {filename}
\`\`\`
Expected output: [what success looks like]

### Step 2: [Next Step]
...continue with clear, actionable steps...

## Examples

### Example 1: [Common scenario]
User says: "..."
Actions: numbered list of what happens
Result: what the user gets

## Error Handling

### [Common error]
Cause: why it happens
Solution: how to fix it
```

**Key writing principles:**
- Keep SKILL.md under ~500 lines (5,000 words max). Move detailed docs to `references/`.
- Put critical instructions near the top — Claude pays more attention to what it reads first.
- For large reference files (>300 lines), include a table of contents.
- Use examples generously — they're worth more than abstract rules.
- Prefer scripts for deterministic/repetitive validation over language instructions. Code is deterministic; language interpretation isn't.
- When referencing bundled files, tell Claude exactly when to read them: "Before writing queries, consult `references/api-patterns.md` for rate limiting guidance."

### Step 3: Validate (1-2 minutes)

Run the validation script on the completed skill:

```bash
python scripts/validate_skill.py /path/to/skill-folder
```

This checks all structural requirements, frontmatter formatting, description quality, and common mistakes.

Also do a manual "description test" — ask yourself: "When would you use the [skill name] skill?" If Claude would quote back something that doesn't match your intent, revise the description.

### Step 4: Test (5-10 minutes)

Create 3 test cases:

1. **Obvious trigger** — the most direct request ("Help me do X with this skill")
2. **Paraphrased trigger** — natural language variation ("I need to set up Y")  
3. **Negative test** — something that should NOT trigger this skill

For each, mentally trace: Does the skill load? Does it follow the right steps? Is the output what you'd expect?

If the skill produces objectively verifiable outputs (file transforms, data extraction, structured output), write assertions. If it produces subjective outputs (writing style, design), vibes-based assessment is fine.

### Step 5: Package

Package the skill for upload to Claude.ai:

```bash
python scripts/package_skill.py /path/to/skill-folder
```

This creates a `.zip` file ready for upload via Settings > Capabilities > Skills.

---

## Improvement Loop

When a skill isn't performing well:

1. **Diagnose the problem:**
   - **Undertriggering** → Description is too vague or missing trigger phrases. Add more specific keywords and contexts.
   - **Overtriggering** → Description is too broad. Add negative triggers, narrow scope.
   - **Wrong execution** → Instructions are ambiguous, buried, or too verbose. Restructure, move critical steps to the top.
   - **Inconsistent results** → Add validation scripts, explicit quality criteria, or examples of good vs bad output.

2. **Apply fixes based on diagnosis:**
   - For description issues: Rewrite and re-test with trigger scenarios
   - For instruction issues: Restructure, add examples, use scripts for deterministic checks
   - For output quality: Add iterative refinement loops, quality checklists, or reference files with standards

3. **Re-test** with the same cases plus any new edge cases discovered.

4. **Generalize from feedback** — don't overfit to specific failing examples. The skill will be used across many different prompts. If you find yourself adding very specific fixes, step back and think about the underlying principle.

**Writing style when improving:**
- Explain the *why* behind changes rather than stacking up rigid rules
- If you're writing ALWAYS or NEVER in all caps, that's a yellow flag — try explaining the reasoning instead
- Keep the prompt lean — remove things that aren't pulling their weight
- Read transcripts, not just outputs — if the skill makes Claude waste time on unproductive steps, trim those parts

---

## Quality Audit

When reviewing a skill, check against this rubric:

### Structure (Pass/Fail)
- [ ] Folder is kebab-case
- [ ] SKILL.md exists (exact case)
- [ ] YAML frontmatter has `---` delimiters
- [ ] `name` field is kebab-case, no spaces, no capitals
- [ ] No XML tags in frontmatter
- [ ] No README.md in skill folder

### Description Quality (Score 1-5)
- Does it say WHAT the skill does?
- Does it say WHEN to use it with specific triggers?
- Does it mention relevant file types?
- Is it under 1024 characters?
- Would Claude correctly identify when to load it?

### Instruction Quality (Score 1-5)
- Are instructions specific and actionable?
- Are examples included?
- Is error handling covered?
- Is progressive disclosure used (references/ for depth)?
- Is the SKILL.md under 500 lines?

### Overall Assessment
Provide: strengths, weaknesses, specific recommendations, and a revised description if needed.

---

## Skill Patterns Reference

When the skill's use case matches one of these patterns, consult `references/patterns.md` for detailed templates:

| Pattern | Use When |
|---------|----------|
| Sequential Workflow | Multi-step process in specific order |
| Multi-MCP Coordination | Workflow spans multiple services |
| Iterative Refinement | Output quality improves with iteration |
| Context-Aware Selection | Same outcome, different tools by context |
| Domain Intelligence | Specialized knowledge beyond tool access |

Read `references/patterns.md` for full templates of each pattern.

---

## Communication Style

Adapt to the user's technical level:
- If they're clearly technical, use precise terminology freely
- If they seem newer to this, briefly explain terms like "frontmatter", "kebab-case", "progressive disclosure"
- Always have something cooking — when the user provides info, start drafting immediately rather than asking more questions
- Show outputs early: "Here's a first draft — take a look and tell me what to adjust"

---

## Final Packaging

When the skill is ready, always:

1. Run `python scripts/validate_skill.py /path/to/skill-folder` for final validation
2. Run `python scripts/package_skill.py /path/to/skill-folder` to create the uploadable zip
3. Present the packaged file to the user
4. Give them clear next steps: "Upload this via Settings > Capabilities > Skills in Claude.ai"

---
name: create-skill
description: Creates a new agent skill following best practices for structure, description writing, and progressive disclosure. Use when the user wants to author a new SKILL.md, scaffold a skill directory, or build a reusable skill. Do NOT use for improving an existing skill — use optimize-skill instead.
license: MIT
metadata:
  author: github.com/hyf0
  version: "1.0.0"
---

## Workflow

Follow these 9 steps in order. Copy this checklist into your response and check off each step as you complete it:

```
Task Progress:
- [ ] Step 1: Understand the skill with concrete examples
- [ ] Step 2: Choose skill name
- [ ] Step 3: Write description
- [ ] Step 4: Write frontmatter
- [ ] Step 5: Write SKILL.md body
- [ ] Step 6: Decide on progressive disclosure
- [ ] Step 7: Create bundled resources
- [ ] Step 8: Validate
- [ ] Step 9: Iterate
```

### Step 1: Understand the Skill with Concrete Examples

Work through 2-3 concrete examples of how the skill will be used. Ask the user:
- What does the skill do? Can you show me an example of how you'd use it?
- What would a user say that should trigger this skill?
- Does it need `allowed-tools` (does it run shell commands, use MCP tools)?
- Should this be a background skill? (always-loaded context, not user-invocable — see frontmatter-spec for `user-invocable: false`)

For each example, walk through how it would be executed from scratch. This reveals what knowledge, scripts, or assets are needed.

Classify the skill category:
- **Document/asset creation** — generates files, reports, configs
- **Workflow automation** — multi-step processes, scaffolding, setup
- **MCP enhancement** — extends or coordinates MCP server capabilities

### Step 2: Choose Skill Name

Rules:
- Gerund form for processes (`creating-components`), noun form for tools (`code`)
- Kebab-case, max 64 characters, must match folder name

### Step 3: Write the Description

This is the highest-impact field — a poor description causes the skill to never be invoked.

Follow the "What + When" formula and all rules in:
-> See [description-writing](reference/description-writing.md)

### Step 4: Write the Frontmatter

Use the exact YAML schema and constraints in:
-> See [frontmatter-spec](reference/frontmatter-spec.md)

### Step 5: Write the SKILL.md Body

Rules:
- Under 500 lines (~5,000 words max)
- Only include knowledge the agent does not already have — do not teach general programming, standard libraries, or well-known tools
- No time-sensitive information (versions that expire, URLs that rot)
- Consistent terminology throughout — pick one term for each concept and stick with it
- Imperative voice
- For any workflow with 3+ steps, include a copyable task list checklist (`- [ ]` items) that the agent copies and checks off as it progresses — this prevents step-skipping and makes progress observable
- Match instruction specificity to task fragility — see "Degrees of Freedom" in skill-patterns

Choose the best skill pattern for the use case:
-> See [skill-patterns](reference/skill-patterns.md)

### Step 6: Decide on Progressive Disclosure

Determine whether content belongs in SKILL.md or in bundled resources:
-> See [progressive-disclosure](reference/progressive-disclosure.md)

### Step 7: Create Bundled Resources (If Needed)

A skill can include three types of bundled resources:

- **`reference/`** — Documentation loaded into context as needed (schemas, guides, examples). One level deep, one topic per file, kebab-case filenames.
- **`scripts/`** — Executable code (Python, Bash, etc.) for tasks needing deterministic reliability or repeatedly rewritten code. Test scripts by running them.
- **`assets/`** — Files used in output but not loaded into context (templates, fonts, icons, boilerplate).

Do NOT create extraneous files like README.md, CHANGELOG.md, or INSTALLATION_GUIDE.md inside the skill folder. The skill should only contain what the agent needs to do the job.

### Step 8: Validate

**Triggering test:** Ask the agent "When would you use the [skill-name] skill?" — it should quote the description back accurately. If it cannot, revise the description.

**Anti-patterns check:** Review the skill against the anti-patterns list:
-> See [anti-patterns](reference/anti-patterns.md)

**Final checks:**
- SKILL.md is under 500 lines
- All links to bundled resources resolve to existing files
- Frontmatter YAML is valid (check with a YAML parser if available)
- No agent-specific language — the skill should work with any agent supporting the open skill standard
- No XML angle brackets in frontmatter fields

### Step 9: Iterate

Skills are living documents. After the initial version:

1. Use the skill on real tasks
2. Observe where the agent struggles or takes unexpected paths
3. Watch for triggering issues:
   - **Under-triggering** (skill doesn't load when it should) — add more trigger phrases and keywords to the description
   - **Over-triggering** (skill loads for unrelated queries) — add negative triggers ("Do NOT use for X"), narrow scope
   - **Instructions not followed** — put critical instructions at the top, use stronger language, consider scripts for deterministic operations
4. Update SKILL.md and bundled resources based on observations
5. Re-test and repeat

## Output

Deliver the complete skill directory to the user:
- `skills/{skill-name}/SKILL.md`
- `skills/{skill-name}/reference/*.md` (if applicable)
- `skills/{skill-name}/scripts/*.py` (if applicable)
- `skills/{skill-name}/assets/*` (if applicable)

Summarize what was created and suggest testing the skill by invoking it with one of the identified use cases.

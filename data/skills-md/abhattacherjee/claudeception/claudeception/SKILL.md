---
name: claudeception
description: "Extracts reusable knowledge from work sessions and codifies it into Claude Code skills. Use when: (1) /claudeception command to review session learnings, (2) save this as a skill or extract a skill from this, (3) what did we learn?, (4) after non-obvious debugging, workarounds, or trial-and-error discovery. Evaluates whether current work contains extractable knowledge, checks for existing skills, and creates or updates skills following the skill-authoring best practices."
metadata:
  version: 3.2.0
---

# Claudeception

You are Claudeception: a continuous learning system that extracts reusable knowledge from work sessions and 
codifies it into new Claude Code skills. This enables autonomous improvement over time.

## Core Principle: Skill Extraction

When working on tasks, continuously evaluate whether the current work contains extractable 
knowledge worth preserving. Not every task produces a skill—be selective about what's truly 
reusable and valuable.

## When to Extract a Skill

Extract a skill when you encounter:

1. **Non-obvious Solutions**: Debugging techniques, workarounds, or solutions that required 
   significant investigation and wouldn't be immediately apparent to someone facing the same 
   problem.

2. **Project-Specific Patterns**: Conventions, configurations, or architectural decisions 
   specific to this codebase that aren't documented elsewhere.

3. **Tool Integration Knowledge**: How to properly use a specific tool, library, or API in 
   ways that documentation doesn't cover well.

4. **Error Resolution**: Specific error messages and their actual root causes/fixes, 
   especially when the error message is misleading.

5. **Workflow Optimizations**: Multi-step processes that can be streamlined or patterns 
   that make common tasks more efficient.

## Skill Quality Criteria

Before extracting, verify the knowledge meets these criteria:

- **Reusable**: Will this help with future tasks? (Not just this one instance)
- **Non-trivial**: Is this knowledge that requires discovery, not just documentation lookup?
- **Specific**: Can you describe the exact trigger conditions and solution?
- **Verified**: Has this solution actually worked, not just theoretically?

## Extraction Process

### Step 1: Check for Existing Skills

**Goal:** Find related skills before creating. Decide: update or create new.

```sh
# Skill directories (project-first, then user-level)
SKILL_DIRS=(
  ".claude/skills"
  "$HOME/.claude/skills"
  "$HOME/.codex/skills"
  # Add other tool paths as needed
)

# List all skills
rg --files -g 'SKILL.md' "${SKILL_DIRS[@]}" 2>/dev/null

# Search by keywords
rg -i "keyword1|keyword2" "${SKILL_DIRS[@]}" 2>/dev/null

# Search by exact error message
rg -F "exact error message" "${SKILL_DIRS[@]}" 2>/dev/null

# Search by context markers (files, functions, config keys)
rg -i "getServerSideProps|next.config.js|prisma.schema" "${SKILL_DIRS[@]}" 2>/dev/null
```

| Found                                            | Action                                                   |
|--------------------------------------------------|----------------------------------------------------------|
| Nothing related                                  | Create new                                               |
| Same trigger and same fix                        | Update existing (e.g., `version: 1.0.0` → `1.1.0`)       |
| Same trigger, different root cause               | Create new, add `See also:` links both ways              |
| Partial overlap (same domain, different trigger) | Update existing with new "Variant" subsection            |
| Same domain, different problem                   | Create new, add `See also: [skill-name]` in Notes        |
| Stale or wrong                                   | Mark deprecated in Notes, add replacement link           |

**Versioning:** patch = typos/wording, minor = new scenario, major = breaking changes or deprecation.

If multiple matches, open the closest one and compare Problem/Trigger Conditions before deciding.

### Step 2: Identify the Knowledge

Analyze what was learned:
- What was the problem or task?
- What was non-obvious about the solution?
- What would someone need to know to solve this faster next time?
- What are the exact trigger conditions (error messages, symptoms, contexts)?

### Step 3: Research Best Practices (When Appropriate)

Search the web for technology-specific best practices when the topic involves specific
frameworks, libraries, or tools. Skip for project-specific internal patterns.

**Search strategy:** `"[technology] [problem] best practices 2026"` → incorporate into
Solution section, add source URLs to References section.

### Step 4: Structure and Save the Skill

**Use the `skill-authoring` skill** for the complete authoring workflow: frontmatter rules,
directory layout (SKILL.md + scripts/ + references/), description writing, template,
and quality checklist.

**Key rules (quick reference):**
- Frontmatter: only `name`, `description`, `version` (no author, date, tags)
- Description: third person, ≤1024 chars, numbered trigger conditions
- SKILL.md body: ≤500 lines, extract lookup material to `references/`
- Scripts: add `--help`, error handling, `chmod +x`
- Save: project-specific → `.claude/skills/`, user-wide → `~/.claude/skills/`

### Step 5: Update Project Artifacts

After saving skill changes, update project-level artifacts that track changes:

1. **CHANGELOG.md** — Add entries under `[Unreleased]` for:
   - New skills → `### Added` section
   - Updated skills → `### Documentation` section
   - Script fixes bundled with skill updates → `### Fixed` section
2. **Commit message** — Use `docs(skills):` prefix for skill-only changes,
   or `fix(skills):` if a script bug was also fixed

**Why this step exists:** Skill extraction focuses on the SKILL.md files and scripts,
making it easy to forget that the project's CHANGELOG.md also needs to reflect these
changes. Without this step, skill updates get committed without any changelog entry,
violating project conventions.

## Retrospective Mode

When `/claudeception` is invoked at the end of a session:

1. **Review the Session**: Analyze the conversation history for extractable knowledge
2. **Identify Candidates**: List potential skills with brief justifications
3. **Prioritize**: Focus on the highest-value, most reusable knowledge
4. **Extract**: Create skills for the top candidates (typically 1-3 per session)
5. **Summarize**: Report what skills were created and why

## Self-Reflection Prompts

Use these prompts during work to identify extraction opportunities:

- "What did I just learn that wasn't obvious before starting?"
- "If I faced this exact problem again, what would I wish I knew?"
- "What error message or symptom led me here, and what was the actual cause?"
- "Is this pattern specific to this project, or would it help in similar projects?"
- "What would I tell a colleague who hits this same issue?"

## Memory Consolidation

When extracting skills, also consider:

1. **Combining Related Knowledge**: If multiple related discoveries were made, consider 
   whether they belong in one comprehensive skill or separate focused skills.

2. **Updating Existing Skills**: Check if an existing skill should be updated rather than 
   creating a new one.

3. **Cross-Referencing**: Note relationships between skills in their documentation.

## Quality Gates

**Use the `skill-authoring` skill's quality checklist** for the full pre-publish verification.

Quick check before saving:
- [ ] Knowledge is reusable, non-trivial, specific, and verified
- [ ] No sensitive information (credentials, internal URLs)
- [ ] Doesn't duplicate existing skills (Step 1 search completed)
- [ ] SKILL.md follows `skill-authoring` frontmatter and structure rules
- [ ] CHANGELOG.md `[Unreleased]` updated with skill changes (Step 5)

## Example: Complete Extraction Flow

**Scenario**: Discovered `getServerSideProps` errors don't appear in browser console.

1. **Identify**: Problem = server-side errors invisible in browser. Trigger = empty console + error page.
2. **Research**: Searched "Next.js getServerSideProps error handling 2026" → found official patterns.
3. **Structure**: Created `~/.claude/skills/nextjs-server-side-error-debugging/SKILL.md`
   with trigger conditions, solution steps, and References section linking to official docs.
4. **Verify**: Tested with real Next.js error → confirmed terminal shows stack trace.

See `examples/` directory for complete sample skills.

## Integration with Workflow

### Automatic Trigger Conditions

Invoke this skill immediately after completing a task when ANY of these apply:

1. **Non-obvious debugging**: The solution required >10 minutes of investigation and
   wasn't found in documentation
2. **Error resolution**: Fixed an error where the error message was misleading or the
   root cause wasn't obvious
3. **Workaround discovery**: Found a workaround for a tool/framework limitation that
   required experimentation
4. **Configuration insight**: Discovered project-specific setup that differs from
   standard patterns
5. **Trial-and-error success**: Tried multiple approaches before finding what worked

### Explicit Invocation

Also invoke when:
- User runs `/claudeception` to review the session
- User says "save this as a skill" or similar
- User asks "what did we learn?"

### Self-Check After Each Task

After completing any significant task, ask yourself:
- "Did I just spend meaningful time investigating something?"
- "Would future-me benefit from having this documented?"
- "Was the solution non-obvious from documentation alone?"

If yes to any, invoke this skill immediately.

Remember: The goal is continuous, autonomous improvement. Every valuable discovery
should have the opportunity to benefit future work sessions.

## See Also
- `skill-authoring` — how to structure, write, and optimize skills (the HOW)
- Anthropic docs: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

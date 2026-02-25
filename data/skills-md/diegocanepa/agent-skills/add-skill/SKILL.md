---
name: add-skill
description: "Capture a useful pattern from the current conversation and contribute it to the diegocanepa/agent-skills repository via a Pull Request."
---

# ➕ Add Skill from Conversation

Distill a reusable pattern or solution from the current conversation into a new skill and submit it to the shared repository.

## When to Use

Use this skill when:
- You've solved a problem an agent will likely encounter again.
- The user says "save this as a skill", "add this to our skills", or similar.
- A new workflow, pattern, or integration approach has been developed.

---

## Workflow

### Step 1: Identify the Skill

Ask the user (if not already clear):
- **Name**: What should this skill be called? (use kebab-case, e.g. `postgres-migrations`)
- **Description**: One sentence — what does the skill do and when should an agent use it?
- **Category** for `docs/SKILLS.md`: Orchestration / Development / VCS / Utilities?

### Step 2: Extract Key Learnings from the Conversation

Review the conversation and extract:
- The problem that was solved.
- The approach or solution (tools, patterns, steps).
- Any caveats, edge cases, or prerequisites.

Present a brief summary to the user before writing the file.

### Step 3: Create the Skill using `skill-creator`

Use the [skill-creator](../skill-creator/SKILL.md) skill to scaffold and write the `SKILL.md` content for `skills/<skill-name>/SKILL.md`.

The skill-creator will guide the structure. Make sure the generated `SKILL.md` includes:
- `name` and `description` frontmatter fields (required by the CLI).
- Self-contained instructions that an agent can follow without prior context.
- Relative links to other skills if applicable (e.g. `[vcs-commit](../vcs-commit/SKILL.md)`).

**Quality check before proceeding:**

```
Skill Content Review:
- [ ] Frontmatter has `name` and `description`
- [ ] Instructions are self-contained and clear
- [ ] No hardcoded values that should be user-configurable
- [ ] Links to other skills use relative paths
- [ ] An agent could follow this with no prior context
```

If any check fails → improve the content → re-check.

### Step 4: Create the Branch

Use `vcs-branch`:
```
feat/add-skill-<skill-name>
```

### Step 5: Commit and Push

Commit using `vcs-commit`:
```bash
git add skills/<skill-name>/SKILL.md
git commit -m "feat(skills): add <skill-name> skill"
git push -u origin feat/add-skill-<skill-name>
```

### Step 6: Update the Skill Catalog

Add the new entry to `docs/SKILLS.md` under the appropriate category:
```markdown
| **[<skill-name>](../skills/<skill-name>/SKILL.md)** | <description> |
```

Commit this as part of the same or a follow-up commit.

### Step 7: Create the Pull Request

Use `vcs-change-request` to open a PR via the GitHub MCP against the skills repository:

- **Owner**: `diegocanepa`
- **Repo**: `agent-skills`
- **URL**: `https://github.com/diegocanepa/agent-skills`
- **Head branch**: `feat/add-skill-<skill-name>`
- **Base branch**: `main`

PR description template:
```markdown
## Summary

Adds a new skill: **<skill-name>**

<Description of what the skill does and when to use it.>

## Checklist
- [ ] Frontmatter with `name` and `description`
- [ ] Added to `docs/SKILLS.md`
- [ ] Instructions are self-contained
```

### Step 8: MITM — Confirm with User

> "The skill `<skill-name>` is ready and the PR has been submitted. Does the content look correct?"

**Feedback Loop:** If the USER wants to refine → update the file → amend/push → re-present.

---

## Notes
- Never push directly to `main`.
- The skill file must be self-contained — the entire `diegocanepa/agent-skills` repo can be installed by anyone, so no project-specific assumptions.
- The `description` frontmatter is the most important field — it's what the agent scans to decide whether to use the skill.

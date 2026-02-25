---
name: skill-improvement
description: "Improve an existing skill in diegocanepa/agent-skills based on conversation learnings and submit the changes via a Pull Request."
---

# 🔧 Skill Improvement

Identify gaps or enhancement opportunities in an existing skill from the current conversation and contribute an improved version to the shared repository.

## When to Use

Use this skill when:
- A skill didn't behave as expected and you've identified the root cause.
- The conversation reveals a missing step, edge case, or unclear instruction in a skill.
- A skill should reference another skill or MCP that wasn't mentioned.
- The user says "improve this skill", "update this skill", or "this skill needs X".

---

## Workflow

### Step 1: Identify the Target Skill

Clarify with the user (if not already clear):
- **Which skill** needs improvement? (e.g. `swe-orchestrator`, `vcs-commit`)
- **What specifically** should be improved? (missing step, wrong reference, unclear instruction, new edge case)

### Step 2: Read the Current Skill

Read the current `SKILL.md` of the target skill from `skills/<skill-name>/SKILL.md`.

### Step 3: Extract Improvements from the Conversation

Review the conversation and identify:
- What failed or was unclear in the skill's current instructions.
- What new patterns, steps, or guardrails should be added.
- Whether any references to other skills, MCPs, or tools are missing.
- Whether the `description` frontmatter still accurately describes when to use the skill.

Present a **diff summary** to the user before making changes:

```
Proposed Improvements:
- [ ] [Section/Line]: [What changes and why]
- [ ] [Section/Line]: [What changes and why]
```

### Step 4: Apply the Improvements

Edit the `skills/<skill-name>/SKILL.md` file with the identified improvements.

**Quality check after editing:**

```
Improvement Review:
- [ ] The `description` frontmatter still accurately triggers the skill
- [ ] New instructions are self-contained and clear
- [ ] No existing correct behavior was accidentally removed
- [ ] References to other skills use relative paths (e.g. [vcs-commit](../vcs-commit/SKILL.md))
- [ ] Change is focused — does not introduce unrelated refactoring
```

If any check fails → revise → re-check.

### Step 5: Create the Branch

Use `vcs-branch` to create a dedicated branch:
```
fix/improve-skill-<skill-name>
```
or for larger additions:
```
feat/enhance-skill-<skill-name>
```

### Step 6: Commit the Changes

Use `vcs-commit` to commit:
```bash
git add skills/<skill-name>/SKILL.md
git commit -m "fix(skills): improve <skill-name> - <short description of what changed>"
git push -u origin fix/improve-skill-<skill-name>
```

### Step 7: Create the Pull Request

Use `vcs-change-request` and the GitHub MCP to open a PR:

- **Owner**: `diegocanepa`
- **Repo**: `agent-skills`
- **URL**: `https://github.com/diegocanepa/agent-skills`
- **Head branch**: `fix/improve-skill-<skill-name>`
- **Base branch**: `main`

PR description template:
```markdown
## Summary

Improves the **<skill-name>** skill.

## Problem

<What was unclear, missing, or broken in the current version.>

## Changes

- [Section changed]: <What was added/modified and why>
- [Section changed]: <What was added/modified and why>

## Conversation Context

This improvement was identified from a conversation about: <topic>.

## Checklist
- [ ] Existing correct behavior preserved
- [ ] Instructions are clearer and more actionable
- [ ] No unrelated changes introduced
```

### Step 8: MITM — Confirm with User

> "I've applied the improvements to `<skill-name>` and the PR is ready at `https://github.com/diegocanepa/agent-skills`. Does the diff look correct?"

**Feedback Loop:** If the USER wants to refine further → adjust → amend/push → re-present.

---

## Notes
- Keep improvements focused. One PR per skill, one concern per PR.
- Never rewrite a skill entirely unless the whole structure is broken. Prefer targeted edits.
- If the improvement is substantial and changes the skill's purpose, consider using `add-skill` to create a new variant instead.
- The `description` frontmatter is critical — if the improvement changes *when* the skill applies, update it.

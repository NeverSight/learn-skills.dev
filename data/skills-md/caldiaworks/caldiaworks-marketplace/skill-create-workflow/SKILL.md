---
name: skill-create-workflow
description: >-
  Orchestrate the full skill development lifecycle from idea to publication.
  Guides through ideation, requirements definition, skill implementation, and marketplace registration.
  Use when: "create a new skill end-to-end", "skill development workflow", "build and publish a skill",
  "スキル開発ワークフロー", "スキルを作って公開", "新しいスキルを開発".
---

# Skill Development Workflow

Orchestrate the full lifecycle of creating a skill for the CaldiaWorks marketplace.

This workflow combines general-purpose skills (`ideation`, `usdm`) with skill-specific tools (`skill-creator`) to guide the user from a rough idea to a published skill.

## Mandatory Execution Rule

Each invoked skill defines its own internal steps (e.g., ideation has Steps 1-6, USDM has Steps 1-5, skill-creator has its own workflow). **Every internal step of every invoked skill must be executed in order without exception.** Do not skip, merge, or silently omit any step — even if the step seems trivial or the answer seems obvious.

If a step requires user input or confirmation, ask. If a step produces output, present it. If a step offers output format choices, ask the user to choose.

Violating this rule degrades the quality of the output and erodes user trust. There is no acceptable reason to skip a step.

## Workflow Steps

Execute these steps in order. Each step produces output that feeds into the next.

If the user already has artifacts from earlier steps (e.g., an idea document or a USDM requirements document), skip the completed steps and start from the appropriate point:

- User has an idea document → start at Step 2
- User has a USDM requirements document → start at Step 3
- User has an implemented skill → start at Step 4

### Step 1: Ideation

Invoke the `ideation` skill to explore and refine the skill idea.

- Input: User's rough idea or problem description
- Output: Idea document at `.docs/ideas/YYYY-MM-DD-<topic>.md`
- The idea document captures What, Why, Scope, Stakeholders, and Approaches

Ask the user: "Do you want to proceed to requirements definition, or keep this as an idea draft?"

- If the user wants to proceed → continue to Step 2
- If the user wants to stop → end the workflow here

### Step 2: Requirements Definition

Invoke the `usdm` skill with the idea document as input.

- Input: The idea document from Step 1
- Output: USDM requirements document at `.docs/`
- The requirements document decomposes the idea into Requirement → Reason → Description → Specification hierarchy

Ask the user: "Requirements are ready. Proceed to implementation?"

### Step 3: Implementation

Invoke the `skill-creator` skill to implement the skill.

- Input: The USDM requirements document from Step 2
- Follow the skill-creator process: understand → plan → initialize → edit → **test → iterate**
- Output: A complete skill directory under `skills/<skill-name>/`

The skill must include:
- `SKILL.md` with proper frontmatter
- Any necessary bundled resources (scripts/, references/, assets/)
- `.claude-plugin/plugin.json`

**Implementation is not complete until skill-creator's full cycle (including eval and iteration) has been executed.** A draft SKILL.md alone does not constitute a completed implementation. The skill-creator defines test cases, runs them, grades expectations, and iterates until stopping criteria are met. All of these steps must be performed.

### Step 4: Marketplace Registration

Register the skill in both marketplace manifests.

1. Verify `.claude-plugin/plugin.json` exists in the skill directory:

```json
{
  "name": "<skill-name>",
  "version": "0.1.0",
  "description": "<Short description>",
  "skills": ["."]
}
```

2. Add the skill path to **both** root-level manifests:
   - `.claude-plugin/plugin.json` — Add `"./skills/<skill-name>"` to the `skills` array
   - `.claude-plugin/marketplace.json` — Add `"./skills/<skill-name>"` to `plugins[0].skills` array

3. Bump the version in **both** files. Both must always have the same version number.

4. Add the skill to `README.md`:
   - Add the `npx skills add` install command to the installation section
   - Add the skill name and description to the Available Skills table

5. Report completion to the user with the registered skill path.

### Step 5: Version Management

If this workflow modified any **existing** skills (not just the new skill), update their versions.

1. Check `git diff` for all files changed during this workflow.
2. For each skill directory under `skills/` that has modifications, bump the `version` field in its `.claude-plugin/plugin.json`.
3. Do not modify files under `.claude/` — that directory is managed by the plugin installation system, not by this workflow.

### Step 6: Final Verification

Before reporting completion, verify all artifacts are consistent.

1. Every skill listed in `.claude-plugin/marketplace.json` `plugins[0].skills` is also listed in `.claude-plugin/plugin.json` `skills`, and vice versa.
2. Both root manifests have the same version number.
3. Every skill listed in the manifests exists under `skills/<name>/` with a `SKILL.md` and `.claude-plugin/plugin.json`.
4. Every skill listed in the manifests has an entry in `README.md` (install command + table row).
5. No unintended files were added to `.gitignore` — check that existing patterns are not duplicated.

### Step 7: Branch Cleanup

After all PRs are merged and the workflow is complete, clean up the working environment.

1. Switch back to the `develop` branch and pull the latest changes.
2. Delete remote feature branches created during this workflow using `git push origin --delete <branch>`.
3. Run `git fetch --prune` to update remote tracking state.
4. Delete local feature branches created during this workflow whose upstream is gone.
5. Delete the eval workspace directory if it exists (`skills/<skill-name>-workspace/`).
6. Verify the working tree is clean with `git status` and `git branch -a`.

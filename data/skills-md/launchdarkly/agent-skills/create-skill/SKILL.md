---
name: create-skill
description: "Add a new skill to the LaunchDarkly agent-skills repo. Use when creating a new SKILL.md, adding a skill to the catalog, or aligning with repo conventions. Guides exploration of existing skills before creating."
license: Apache-2.0
compatibility: Works in repositories following the Agent Skills open standard
metadata:
  author: launchdarkly
  version: "0.2.0"
---

# Create a LaunchDarkly Skill

You're using a skill that will guide you through adding a new skill to the LaunchDarkly agent-skills repository. Your job is to explore existing skills to understand the patterns, assess what the new skill needs, create it following conventions, and verify it validates correctly.

## Prerequisites

- Access to the LaunchDarkly agent-skills repo (or a fork)
- Understanding of the workflow you want to encode
- Python 3.x (for validation scripts)

## Core Principles

1. **Explore First**: Look at existing skills before creating. Match their structure and style.
2. **Job to Be Done**: Every skill should clearly state what job it helps accomplish.
3. **References for Details**: Keep SKILL.md focused on the workflow. Move deep content to `references/`.
4. **Validate Before Commit**: Run validation scripts to catch issues.

## Workflow

### Step 1: Explore Existing Skills

Before creating anything, understand how skills are structured in this repo.

1. **Browse the skills directory.**
   - Look at `skills/feature-flags/` and other categories
   - Note the directory layout: `skills/<category>/<skill-name>/`
   - Each skill has `SKILL.md` and optionally `references/`, `README.md`, `marketplace.json`

2. **Read 1–2 similar skills.**
   - If adding a feature-flag skill, read `launchdarkly-flag-create` or `launchdarkly-flag-cleanup`
   - If adding an AI-config skill, read those under `ai-configs/` if present
   - Observe: job-to-be-done intro, workflow steps, Core Principles, Edge Cases, What NOT to Do, References

3. **Check the template.**
   - Read `template/SKILL.md.template` for the expected structure
   - The template reflects the workflow-based pattern used across skills

See [Skill Structure](references/skill-structure.md) for the full structure guide.

### Step 2: Assess What's Needed

Based on the user's request and your exploration:

1. **Choose category and name.**
   - Category: `feature-flags`, `ai-configs`, `skill-authoring`, or new category
   - Name: lowercase, hyphens only, under 64 chars (e.g., `my-new-skill`)
   - Directory: `skills/<category>/<skill-name>/`

2. **Identify the job to be done.**
   - What does the user want to accomplish?
   - What should the agent explore, assess, and verify?
   - What references will the skill need?

3. **Plan the workflow.**
   - Step 1: Explore (what to look for)
   - Step 2: Assess (decision table or logic)
   - Step 3: Execute (with references)
   - Step 4: Verify (what the agent actually does)

See [Frontmatter & Metadata](references/frontmatter.md) for required fields.

### Step 3: Create the Skill

1. **Create the directory.**
   ```
   skills/<category>/<skill-name>/
   ```

2. **Create SKILL.md.**
   - Copy `template/SKILL.md.template` into the new directory
   - Fill in frontmatter: `name` (must match folder name), `description`, `compatibility`, `metadata`
   - Write the job-to-be-done intro and workflow steps
   - Link to references for detailed content
   - Keep SKILL.md under 500 lines

3. **Add references.**
   - Create `references/` directory
   - Add reference files for implementation details, API patterns, decision guides
   - Link from SKILL.md

4. **Add supporting files (optional).**
   - `README.md` — short description, link to SKILL.md
   - `marketplace.json` — if publishing to a marketplace (see existing skills for format)

5. **Update repo docs.**
   - Add the skill to the table in `README.md`
   - If the skill requires specific tools, document them in the skill

See [Skill Structure](references/skill-structure.md) for file layout and content guidelines.

### Step 4: Update the Catalog

Regenerate the skills catalog so the new skill is discoverable:

```bash
python3 scripts/generate_catalog.py
```

This updates `skills.json`. Commit the updated file with your new skill.

### Step 5: Verify

Confirm the skill is valid and complete:

1. **Run validation:**
   ```bash
   python3 scripts/validate_skills.py
   ```
   Fix any reported errors (frontmatter, naming, length limits).

2. **Run tests (if present):**
   ```bash
   python3 -m unittest discover -s tests
   ```

3. **Check structure:**
   - SKILL.md exists and has valid frontmatter
   - `name` in frontmatter matches directory name
   - References are linked and exist
   - README.md table includes the new skill

4. **Report results:**
   - ✓ Skill created and validates
   - ✓ Catalog updated
   - ⚠️ Flag any validation issues or missing pieces

## Edge Cases

| Situation | Action |
|-----------|--------|
| `name` doesn't match folder name | Fix folder name or frontmatter so they match exactly |
| SKILL.md over 500 lines | Move detailed content into `references/` |
| Category doesn't exist | Create `skills/<new-category>/` and add the skill |
| Marketplace.json needed | Copy format from `launchdarkly-flag-create/marketplace.json` |
| Validation fails | Fix the specific error (often frontmatter or naming) |
| Catalog not regenerated | Run `python3 scripts/generate_catalog.py` before commit |

## What NOT to Do

- Don't create a skill without exploring existing ones first
- Don't put long implementation details in SKILL.md — use references
- Don't forget to run `validate_skills.py` before committing
- Don't skip updating README.md and the catalog
- Don't use internal-only links or tools unless the skill is internal-only

## References

- [Skill Structure](references/skill-structure.md) — File layout, workflow pattern, content guidelines
- [Frontmatter & Metadata](references/frontmatter.md) — Required fields, naming rules, versioning

---
name: aios-skill-publisher
description: >
  Create and publish proprietary skills for the AIOS system. Use when asked
  to create a new skill, build a skill, make a skill, write a skill, or
  publish a skill. Also use when converting a workflow or process into a
  reusable skill, or when user says new AIOS skill or references the
  aios-skills repository. Do NOT use for installing marketplace skills or
  editing existing community skills.
metadata:
  author: claim-supply
  version: 1.0.0
---

# AIOS Skill Publisher

## Purpose
Automate the creation and publishing of proprietary skills for Claim Supply / NoManagement B.V. Ensures every custom skill follows a consistent format, uses the aios- prefix, publishes to the mrnobrands/aios-skills GitHub repo, and becomes installable via npx.

## When to Use
- User asks to create, build, make, or write a new skill
- User asks to publish a skill to the AIOS repo
- User wants to convert a workflow or process into a reusable skill
- User references proprietary skill creation or aios-skills

### Do NOT Use For
- Installing marketplace skills (use npx skills add directly)
- Editing existing marketplace community skills
- Creating skills for other repos or systems

## Context Loading

### Always Read
1. This SKILL.md
2. references/skill-template.md — blank template for new skills
3. references/naming-rules.md — naming and format conventions

## Process

### Step 1: Gather Requirements
Ask the user (if not already clear):
- What does this skill do? (one sentence)
- When should it trigger? (what phrases or tasks activate it)
- Does it need reference files? (templates, examples, patterns)

If the user has already provided enough detail, skip to Step 2.

### Step 2: Determine Skill Name
- Take the users description and create a kebab-case name
- Prepend aios- prefix (always lowercase)
- Examples: aios-lead-scoring, aios-weekly-digest, aios-client-onboarding
- Confirm the name with the user before proceeding

### Step 3: Locate the Repo
Detect which machine you are on:
- If /Users/luca exists → Mac path: /Users/luca/NoBrands Dropbox/MR. NO/Github/aios-skills/
- If /home/luca exists and no /Users → VPS path: /home/luca/aios-skills/

### Step 4: Create Skill Directory
mkdir -p [REPO_PATH]/aios-[skill-name]/references

### Step 5: Write SKILL.md
Use the template from references/skill-template.md. Critical rules:
- name field matches directory name exactly (all lowercase, kebab-case)
- description under 1024 characters, no XML angle brackets
- description includes trigger phrases, NOT a workflow summary
- Include metadata.author: claim-supply and metadata.version: 1.0.0
- Required sections: Purpose, When to Use, Context Loading, Process, Quality Gates, Output Format

### Step 6: Create Reference Files (if needed)
Place in references/ directory. Each file is kebab-case .md. Only create references the skill actually needs.

### Step 7: Validate
- name field matches directory name (lowercase kebab-case)
- description has trigger phrases, not workflow summary
- description under 1024 characters, no angle brackets
- All required sections present
- No placeholder text remaining
- No README.md in skill folder

### Step 8: Publish to GitHub
cd [REPO_PATH] && git add -A && git commit -m "Add aios-[skill-name]" && git push

### Step 9: Install Locally
npx -y skills add -y -g mrnobrands/aios-skills

### Step 10: Notify User
Report: skill name, GitHub URL, install command, confirmation of local install.

## Quality Gates
- Lowercase aios- prefix naming convention followed
- Folder name matches name field exactly
- YAML frontmatter valid and under 1024 chars
- Description contains trigger phrases only
- All SKILL.md sections present and filled in
- No README.md in skill folder
- Git push succeeded
- npx install succeeded

## Output Format
1. New directory in mrnobrands/aios-skills repo
2. Valid SKILL.md with proper frontmatter
3. Optional reference files in references/
4. Git commit and push to GitHub
5. Local npx install

## Examples

### Example 1: Create a lead scoring skill
User says: "Create a new skill for scoring incoming leads"
Result: aios-lead-scoring/ with SKILL.md, pushed to GitHub, installed locally

### Example 2: Convert a process to a skill
User says: "Turn our weekly digest process into a skill"
Result: aios-weekly-digest/ with full process as a skill

## Troubleshooting

### Git push fails
Cause: No git credentials or repo not cloned.
Fix Mac: Check gh auth status. Run gh auth login if needed.
Fix VPS: Check git config. May need personal access token.

### npx install shows old skills
Cause: npm cache serving stale version.
Fix: Wait 1-2 minutes and retry.

### Skill does not trigger
Cause: Description missing trigger phrases or too vague.
Fix: Add specific keywords. Test: "When would you use the [skill] skill?"

## References
- references/skill-template.md — Blank SKILL.md template
- references/naming-rules.md — Naming conventions and rules

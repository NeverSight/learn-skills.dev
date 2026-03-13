---
name: better-skill-publish
description: "Package a agent skill into a complete GitHub repository ready for distribution via skills.sh. Generates README, LICENSE, plugin.json, marketplace.json, .gitignore, and the proper directory structure. Optionally initializes a git repo and creates a GitHub repository. This skill should be used when publishing a skill, packaging a skill for distribution, preparing a skill repo, or when the user says 'publish skill', 'package skill', 'release skill', '发布技能', '打包 skill'."
---

# Skill Publish

## Language

**Match user's language**: Respond in the same language the user uses.

## Overview

Package a agent skill into a complete, distributable GitHub repository. Generates all the surrounding files (README, LICENSE, plugin.json, marketplace.json) and optionally creates the GitHub repo.

## How It Works

1. Identify the skill to publish
2. Optionally review first with better-skill-review
3. Collect publishing metadata through dialogue
4. Generate the repository structure with `publish.py`
5. Optionally initialize git and create GitHub repo

## Dialogue Flow

Progress:
- [ ] Step 1: Identify the skill
- [ ] Step 2: Pre-publish validation
- [ ] Step 3: Collect metadata
- [ ] Step 4: Generate repository
- [ ] Step 5: Post-generation

### Step 1: Identify the Skill

Accept the skill location in multiple forms:

| Input | Detection | Action |
|-------|-----------|--------|
| Directory with SKILL.md | Direct path | Use as-is |
| SKILL.md file path | Path ends in `SKILL.md` | Use parent directory |
| Current directory | No input, cwd has SKILL.md | Auto-detect |

### Step 2: Pre-Publish Validation

Check for `better-skill-review` availability:
1. First try: `{SKILL_DIR}/../better-skill-review/scripts/validate.py`
2. Fallback: `~/.agents/skills/better-skill-review/scripts/validate.py`

If found, suggest running validation:

```bash
python3 <validate.py path> run --path <skill-path>
```

If there are failures, recommend fixing them before proceeding. Warnings are acceptable.

If better-skill-review is not available, offer:
- A) Install it: `npx skills add psylch/better-skills@better-skill-review -g -y`
- B) Continue without it (quick manual check: verify SKILL.md exists with valid frontmatter)
- C) Cancel

### Step 3: Collect Metadata

Use AskUserQuestion to gather:

1. **GitHub owner/org** — Default: try to infer from `git config user.name` or `gh api user -q .login`. Ask user to confirm or change.

2. **Repository name** — Default: `<skill-name>-skill` (e.g., `cors-audit-skill`). Suggest the convention but let user override.

3. **Version** — Default: `1.0.0`. Use semver.

4. **License** — Default: MIT. Options: MIT, Apache-2.0, GPL-3.0.

5. **Output directory** — Where to create the repo. Default: parent directory of the skill.

### Step 4: Generate Repository

```bash
python3 {SKILL_DIR}/scripts/publish.py generate \
    --skill-path <path> \
    --owner <owner> \
    --repo <repo-name> \
    --version <version> \
    [--license mit|apache2|gpl3] \
    [--output <dir>] \
    [--force]
```

Where `{SKILL_DIR}` is the directory containing this SKILL.md file.

The script outputs JSON to stdout:
```json
{
  "status": "ok",
  "output_dir": "/path/to/output",
  "repo": "owner/repo-name",
  "created": [".claude-plugin/plugin.json", "README.md", "LICENSE", ...],
  "hint": "Repository files generated. Next: git init or gh repo create."
}
```

### Step 5: Post-Generation

Present a completion report:

```
[Skill Publish] Complete!

Skill: <skill-name>
Repository: <owner>/<repo>
License: <license>
Output: <directory>

Files created:
• <list from JSON "created" field>

Next Steps:
→ A) Initialize git repo
→ B) Create GitHub repo and push
→ C) Done — handle git manually
```

Then let the user choose:

**Option A: Initialize git repo**
```bash
cd <output-dir>
git init
git add .
git commit -m "Initial commit"
```

**Option B: Create GitHub repo and push**
```bash
cd <output-dir>
git init
git add .
git commit -m "Initial commit"
gh repo create <owner>/<repo> --public --source . --push
```

**Option C: Done** — User will handle git themselves.

After creation, remind the user:
- Edit README.md and README.zh.md to polish auto-generated content
- Register on skills.sh if they want public discoverability
- Test installation: `npx skills add ./ -g -y`

## Generated Repository Structure

```
<repo-name>/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   └── <skill-name>/        # Copied from source
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
├── README.md
├── README.zh.md
├── LICENSE
└── .gitignore
```

## Distribution Guide Reference

For details about skills.sh registry, versioning strategy, and publishing conventions, read `references/distribution_guide.md`.

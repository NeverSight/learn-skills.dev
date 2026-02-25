---
name: readme-doctor
description: README diagnosis and treatment. Diagnoses README problems, analyzes reference styles, and prescribes improvements. Use for "fix my README", "analyze this README", "make README like [reference]", "create README based on my GitHub style", or when user provides reference URLs/files for README guidance.
---

# README Doctor

Diagnose README problems, analyze reference styles, and prescribe improvements.

## Diagnosis Process

```
Patient (README) Intake → Diagnosis → Prescription → Treatment
```

## Mode 1: Diagnose & Treat (Default)

Diagnose current project's README and prescribe improvements.

### Step 1: Intake

```bash
# Check current README
[ -f README.md ] && cat README.md

# Gather project info
[ -f package.json ] && cat package.json | jq '{name, description, version}'
[ -f pyproject.toml ] && grep -E "^(name|version|description)" pyproject.toml
```

### Step 2: Diagnosis Checklist

| Item | Diagnosis Criteria |
|------|-------------------|
| **Title** | Is the project name clear? |
| **Description** | Does it explain "what & why" in 1-2 sentences? |
| **Installation** | Can anyone follow it? |
| **Usage** | Is there a runnable example? |
| **Context** | Is necessary background provided? |
| **Structure** | Does it follow cognitive funneling (broad → specific)? |
| **Freshness** | Does content match current project state? |

### Step 3: Prescription Output

```markdown
## Diagnosis Results

### Healthy
- [x] Installation section exists
- [x] License stated

### Needs Attention
- ⚠️ Description too long (3 lines → 1-2 recommended)
- ⚠️ No usage example

### Needs Treatment
- ❌ Title only says "Project" → Change to actual name
- ❌ Install command outdated (npm install → npm i recommended)

## Prescription

### 1. Fix Title
- Current: `# Project`
- Recommended: `# my-awesome-tool`

### 2. Shorten Description
- Current: "This project is... (3 lines)"
- Recommended: "CLI tool for X. One-liner."

### 3. Add Usage Example
\`\`\`bash
my-tool --input file.txt --output result.json
\`\`\`
```

## Mode 2: Reference Analysis

Analyze style from user-provided reference READMEs.

### Input Formats

```bash
# GitHub URL
"Analyze https://github.com/vercel/next.js/blob/canary/README.md"

# Local file
"Analyze ~/projects/example/README.md"

# Direct paste
"Analyze this README style: [paste content]"
```

### Analysis Items

| Category | What to Analyze |
|----------|-----------------|
| **Structure** | Section order, hierarchy |
| **Style** | Badges, emojis, code blocks |
| **Tone** | Formal/casual, concise/verbose |
| **Format** | Tables, lists, blockquotes usage |

### Analysis Result Example

```json
{
  "structure": ["Title", "Badges", "Description", "Features", "Install", "Usage", "Contributing", "License"],
  "styles": {
    "badges": true,
    "emoji_in_headers": false,
    "code_blocks": ["bash", "typescript"],
    "images": false,
    "toc": false
  },
  "tone": "professional-concise",
  "avg_section_length": "short"
}
```

## Mode 3: GitHub Pattern Analysis

Extract README patterns from user's GitHub repositories.

```bash
# Analyze user repos
gh repo list <username> --limit 10 --json name,url

# Fetch README
gh api /repos/<owner>/<repo>/readme --jq '.content' | base64 -d
```

Extract common patterns from at least 3 READMEs.

## Mode 4: Best Practices Check

Evaluate README quality based on `references/best-practices.md`.

### Required Checks

- [ ] Title + one-liner description
- [ ] Installation method
- [ ] Usage example
- [ ] License

### Recommended Checks

- [ ] Badges (npm version, license, etc.)
- [ ] Contributing guide
- [ ] Changelog link

## Using References

When user provides a reference:

1. **Analyze Reference** → Extract style/structure
2. **Diagnose Current Project** → Identify issues
3. **Prescribe** → Suggest improvements in reference style

```
User: "Make my README like Vercel's style. Reference: https://github.com/vercel/next.js"

Process:
1. Fetch Vercel's README
2. Analyze: badges at top, concise sections, professional tone
3. Diagnose current README
4. Prescribe: "Add badges section", "Shorten description to 1 line", "Add Features table"
```

## Templates

Project type templates in `templates/` folder:

| Template | Use For |
|----------|---------|
| `templates/oss.md` | Open source |
| `templates/personal.md` | Personal projects |
| `templates/internal.md` | Internal tools |
| `templates/xdg-config.md` | Config files |

## References

| File | Content |
|------|---------|
| `references/best-practices.md` | README best practices |
| `references/section-checklist.md` | Section checklist |
| `references/templates.md` | Language-specific patterns |

## Usage Examples

```
# Diagnosis request
"Fix my README"
"Diagnose this README"

# Reference-based
"Make README like this: https://github.com/facebook/react"
"Change to this style: [README content]"

# GitHub pattern
"Create README based on my GitHub style"
"Make README matching my other projects"

# New project
"I need a README for a new CLI tool"
```

## Prerequisites

- `gh` CLI (for GitHub pattern analysis)
- `jq` (for JSON processing)
- Python 3.6+ (for running scripts)

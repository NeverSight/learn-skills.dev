---
name: skill-standardization
description: Standardize and validate SKILL.md files to match the project specification. Use when creating new skills, converting existing skills to standard format, or validating skill file structure. Handles section heading conversion, frontmatter standardization, and missing section detection.
allowed-tools: Bash Read Write Edit Glob Grep
metadata:
  tags: skill-management, standardization, validation, automation, scripting
  platforms: Claude, ChatGPT, Gemini
---


# Skill Standardization

## When to use this skill

- Creating new SKILL.md files following the standard template
- Converting existing skills with non-standard section headings
- Validating skill files against the project specification
- Batch processing multiple skill files for consistency
- Ensuring all skills have required sections (Examples, Best practices, References)

## Instructions

### Step 1: Run the conversion script

Execute the main conversion script to standardize all SKILL.md files:

```bash
cd /path/to/.agent-skills
python3 scripts/convert_skills.py
```

This script will:
- Convert Korean section headings to English
- Standardize frontmatter (add missing tags, platforms)
- Add missing required sections with templates

### Step 2: Remove duplicate sections

If files have duplicate sections after conversion:

```bash
python3 scripts/remove_duplicates.py
```

### Step 3: Final cleanup

For any remaining non-standard headings:

```bash
python3 scripts/final_cleanup.py
```

## Available Scripts

| Script | Purpose |
|--------|---------|
| `convert_skills.py` | Main conversion script - handles section headings, frontmatter, missing sections |
| `remove_duplicates.py` | Removes duplicate Examples, Best practices, References sections |
| `final_cleanup.py` | Direct string replacement for remaining Korean headings |

## Section Heading Conversions

| Legacy heading | Standard heading |
|--------|---------|
| `## Purpose (legacy)` | `## Purpose` |
| `## When to Use (legacy)` | `## When to use this skill` |
| `## Procedure (legacy)` | `## Instructions` |
| `## Examples (legacy)` | `## Examples` |
| `## Best Practices (legacy)` | `## Best practices` |
| `## References (legacy)` | `## References` |
| `## Output Format (legacy)` | `## Output format` |
| `## Constraints (legacy)` | `## Constraints` |
| `## Metadata (legacy)` | `## Metadata` |
| `### Step N (legacy):` | `### Step N:` |

## Standard SKILL.md Structure

```markdown
---
name: skill-name
description: Clear description (max 1024 chars)
tags: [tag1, tag2]
platforms: [Claude, ChatGPT, Gemini]
---

# Skill Title

## When to use this skill
- Scenario 1
- Scenario 2

## Instructions

### Step 1: [Action]
Content...

### Step 2: [Action]
Content...

## Examples

### Example 1: [Scenario]
Content...

## Best practices
1. Practice 1
2. Practice 2

## References
- [Link](url)
```

## Examples

### Example 1: Convert a single file manually

```python
from pathlib import Path
import re

filepath = Path('backend/new-skill/SKILL.md')
content = filepath.read_text()

# Normalize legacy headings to standard
content = content.replace('## Best Practices', '## Best practices')
content = content.replace('## Reference', '## References')
content = re.sub(r'### Step (\d+):', r'### Step \1:', content)

filepath.write_text(content)
```

### Example 2: Validate a skill file

```bash
# Check for required sections
grep -E "^## (When to use|Instructions|Examples|Best practices|References)" SKILL.md
```

## Best practices

1. **Run all three scripts in sequence** for complete standardization
2. **Review changes** before committing to ensure content wasn't lost
3. **Keep section content** - only headings are converted, not content
4. **Test with one file first** when making script modifications

## References

- [README.md](../../README.md) - Repository overview and SKILL.md conventions
- [.agent-skills/README.md](../README.md) - Skill repository structure and examples

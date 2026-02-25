---
name: markdown-validation
description: Validate markdown documentation files for formatting issues, syntax errors, broken links, and quality standards. Use when checking .md files for compliance with documentation standards or after editing markdown files.
---

# Markdown Validation

This skill provides comprehensive markdown validation capabilities for documentation files.

## When to Use

Use markdown-validation when:
1. Validating markdown files for syntax and formatting errors
2. Checking documentation quality after edits
3. Enforcing documentation standards across the project
4. Identifying broken links or invalid references
5. Reviewing markdown files before commits

## Validation Checks

### 1. Syntax Validation
- Valid markdown syntax
- Proper header hierarchy (no skipped levels)
- Balanced code fences
- Correct list formatting
- Proper link syntax

### 2. Link Validation
- Internal links point to existing files
- Anchor links match actual headers
- No broken external links (when network available)

### 3. Formatting Standards
- Consistent heading styles
- Proper code block language tags
- Table formatting correctness
- No trailing whitespace
- Consistent list markers

### 4. Documentation Quality
- Files have descriptive headers
- Code examples are complete
- Links are descriptive (not "click here")
- Tables have headers
- Proper frontmatter when required

## Usage

### Automatic Validation

The validation script runs automatically when triggered by hooks on markdown file edits.

### Manual Validation

**Validate a single file**:
```bash
./docs/skills/markdown-validation/scripts/validate-markdown.py path/to/file.md
```

**Validate multiple files**:
```bash
./docs/skills/markdown-validation/scripts/validate-markdown.py file1.md file2.md file3.md
```

**Validate a directory**:
```bash
find docs/ -name "*.md" -exec ./docs/skills/markdown-validation/scripts/validate-markdown.py {} +
```

## Output Format

Validation results are returned in structured format:

```
✅ path/to/file.md - PASS

❌ path/to/other.md - FAIL
  Line 15: Header level skipped (h1 -> h3)
  Line 42: Broken internal link: [docs/missing.md](docs/missing.md)
  Line 87: Unclosed code fence
```

## Integration with Hooks

This skill works best when integrated with PostToolUse hooks:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q '\\.md\"'; then $CLAUDE_PROJECT_DIR/docs/skills/markdown-validation/scripts/validate-markdown.py \"$(echo \"$CLAUDE_TOOL_INPUT\" | grep -o '\"[^\"]*\\.md\"' | tr -d '\"')\"; fi"
        }]
      }
    ]
  }
}
```

## Common Issues and Fixes

### Issue: Header Level Skipped
**Problem**: `# Header 1` followed by `### Header 3` (skipped h2)
**Fix**: Maintain sequential header hierarchy

### Issue: Broken Internal Link
**Problem**: Link points to non-existent file
**Fix**: Update link target or create missing file

### Issue: Unclosed Code Fence
**Problem**: ``` opened but not closed
**Fix**: Add closing ``` after code block

### Issue: No Language Tag
**Problem**: Code fence missing language identifier
**Fix**: Add language: ```python, ```bash, ```javascript

## Configuration

Create `.markdown-validation.json` in project root to customize validation:

```json
{
  "checkLinks": true,
  "checkSyntax": true,
  "requireFrontmatter": false,
  "allowedHeaderLevels": [1, 2, 3, 4, 5, 6],
  "requireLanguageTags": true,
  "maxLineLength": null
}
```

## References

- **Markdown Specification**: See `references/markdown-spec.md`
- **Project Standards**: See `references/documentation-standards.md`

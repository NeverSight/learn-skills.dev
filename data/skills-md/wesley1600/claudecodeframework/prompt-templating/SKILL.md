---
name: prompt-templating
description: "Fill prompt templates with variables from task context, replacing placeholders like {user_name} or {analysis}. Use when you need consistent, reusable prompts with dynamic content insertion and validation of required variables."
tools: ["Read", "Write", "Edit", "Grep"]
version: "1.0.0"
---

# Prompt Templating

Transforms prompt templates with placeholders into complete prompts by filling in variables from the current task context. Ensures consistency, reduces repetition, and validates that all required variables are provided.

## Overview

This skill enables you to:
- Load prompt templates with placeholders like `{variable_name}`
- Fill placeholders with values from the current context
- Distinguish between required and optional variables
- Provide default values for optional variables
- Warn users about missing required variables
- Validate and sanitize variable values

## When to Use

Use this skill when:
- Creating consistent prompts across multiple similar tasks
- Building reusable prompt patterns for summarization, analysis, or code review
- Ensuring critical context variables are always included
- Maintaining a library of standardized prompts
- Reducing copy-paste errors in repetitive prompting tasks

## Template Syntax

### Basic Placeholders
```
{variable_name}
```

### Optional Variables with Defaults
```
{variable_name:default_value}
```

### Syntax Rules
- Variable names: lowercase, alphanumeric, underscores only
- No spaces inside braces: `{name}` ✓, `{ name }` ✗
- Nested braces not supported
- Escape literal braces with backslash: `\{not_a_variable\}`

## Workflow

### 1. Identify Template Requirements

When a user requests templating:
- Ask which template file to use (or create a new one)
- Identify what variables need to be filled
- Determine which variables are required vs optional

### 2. Load Template

Read the template file from:
- `.claude/skills/prompt-templating/templates/` (shared templates)
- User-specified path (custom templates)

Example templates available:
- `code-review.txt` - Code review prompts
- `summarization.txt` - Document summarization
- `analysis.txt` - General analysis tasks
- `bug-report.txt` - Bug investigation prompts

See `templates/` directory for all available templates.

### 3. Parse Template

Scan template for placeholders:
- Extract all `{variable_name}` patterns
- Identify required variables (no default)
- Identify optional variables (has `:default`)
- Build a list of needed variables

### 4. Gather Variables

Collect variable values from:
- User's explicit instructions
- Current task context
- File contents (if referenced)
- Previous conversation context
- Default values (for optional variables)

### 5. Validate Variables

**CRITICAL: Missing Required Variables**

If any required variable lacks a value:
1. **STOP** - Do not proceed with template filling
2. List all missing required variables clearly
3. Ask the user to provide values for missing variables
4. Suggest reasonable values if context provides hints
5. Wait for user confirmation before proceeding

Example warning:
```
⚠️  Missing Required Variables:
- {user_name}: The name of the user or author
- {project_name}: The project being analyzed

Please provide these values to continue.
```

### 6. Fill Template

Replace placeholders with values:
1. Process required variables first
2. Apply default values for unprovided optional variables
3. Perform substitution left-to-right
4. Preserve formatting and indentation
5. Handle escaped braces (don't replace `\{...\}`)

### 7. Output Result

Present the filled template:
- Show the complete rendered prompt
- Indicate which default values were used
- Confirm with user if appropriate
- Save to file if requested

## Variable Extraction Patterns

### From User Messages
```
User: "Use 'John Smith' for the author name"
→ {author_name} = "John Smith"
```

### From Context
```
Working on file: src/components/Header.tsx
→ {file_path} = "src/components/Header.tsx"
→ {file_name} = "Header.tsx"
→ {component_name} = "Header"
```

### From Code Analysis
```
Function being reviewed: calculateTotal()
→ {function_name} = "calculateTotal"
```

## Best Practices

### 1. Clear Variable Names
Use descriptive names:
- Good: `{analysis_type}`, `{target_audience}`, `{code_file_path}`
- Bad: `{x}`, `{temp}`, `{var1}`

### 2. Reasonable Defaults
For optional variables, provide sensible defaults:
- `{tone:professional}` - Default tone is professional
- `{max_length:500}` - Default max length 500 words
- `{format:markdown}` - Default output format

### 3. Document Templates
Every template should have:
- Header comment explaining purpose
- List of required variables
- List of optional variables with defaults
- Example usage

### 4. Validate Early
Check for missing variables BEFORE filling template to avoid partial outputs.

### 5. Sanitize Input
For security-sensitive contexts:
- Escape special characters if needed
- Validate variable formats (emails, paths, etc.)
- Warn about potentially unsafe values

## Example Usage Scenarios

### Scenario 1: Code Review Template

Template file: `templates/code-review.txt`
```
Review the following code in {file_path}:

Focus areas:
- {focus_area_1}
- {focus_area_2:performance}
- {focus_area_3:security}

Code to review:
{code_content}

Provide feedback for: {reviewer_name}
```

User request: "Review Header.tsx for bugs"

Process:
1. Load template
2. Extract variables: `file_path`, `focus_area_1`, `focus_area_2` (optional), `focus_area_3` (optional), `code_content`, `reviewer_name`
3. Gather from context:
   - `file_path` = "src/components/Header.tsx"
   - `focus_area_1` = "bugs" (from user request)
   - `code_content` = (read from file)
4. Missing: `reviewer_name`
5. **WARN** about missing `reviewer_name`
6. Ask user for reviewer name
7. Fill template once all values provided

### Scenario 2: Analysis Summary

Template: `templates/summarization.txt`
User provides all variables explicitly
Fill and output immediately

See `examples/` directory for complete scenarios.

## Error Handling

### Missing Required Variable
```
❌ Error: Required variable '{variable_name}' not provided
Description: {what this variable represents}
Please provide a value to continue.
```

### Invalid Variable Name in Template
```
⚠️  Warning: Invalid variable syntax at position X
Found: '{INVALID NAME}'
Variables must use lowercase, alphanumeric, underscore only.
```

### Template File Not Found
```
❌ Error: Template file not found: {path}
Available templates:
  - templates/code-review.txt
  - templates/analysis.txt
  ...
```

## Advanced Features

### Conditional Sections (Optional)
For advanced templates, support conditional inclusion:
```
{?if:variable_name}
This section only appears if variable_name is provided
{?endif}
```

### Repeated Sections (Optional)
For lists:
```
{?foreach:item in items}
- {item}
{?endforeach}
```

**Note**: These advanced features are optional enhancements. Start with basic placeholder replacement.

## Reference Files

- `templates/` - Pre-built template files
- `examples/` - Complete usage examples
- `reference/variables.md` - Common variable definitions
- `reference/template-syntax.md` - Detailed syntax guide

## Quick Start

1. User requests templated prompt
2. Load template from `templates/` or custom path
3. Extract all `{variables}`
4. Check for missing required variables
5. **WARN if any missing** and stop
6. Fill template with values
7. Output result

## Summary

This skill ensures consistent, validated prompts by:
- ✓ Replacing placeholders with context values
- ✓ Warning about missing required variables
- ✓ Applying defaults for optional variables
- ✓ Maintaining prompt style consistency
- ✓ Reducing manual repetition

Always validate before filling to prevent incomplete outputs.

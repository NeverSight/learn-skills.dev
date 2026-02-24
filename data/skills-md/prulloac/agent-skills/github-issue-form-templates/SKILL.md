---
name: github-issue-form-templates
description: Create and manage GitHub issue form templates using YAML syntax. Use when you need to design custom issue forms for GitHub repositories with specific field types, validations, default labels, and assignees. Helps with creating bug reports, feature requests, documentation issues, and custom workflows. Includes YAML syntax guidance, field type reference, validation patterns, best practices, and ready-to-use templates.
---

# GitHub Issue Form Templates

## Overview

GitHub issue form templates are YAML-based forms that replace markdown templates, offering a structured way to collect issue information. Instead of free-form text, issue forms provide:

- **Structured fields**: Text inputs, dropdowns, checkboxes, textareas, and more
- **Validations**: Required/optional fields, regex patterns, min/max lengths
- **Auto-assignment**: Default assignees and labels
- **Metadata**: Issue types and project assignments

Issue forms are stored in `.github/ISSUE_TEMPLATE/` as YAML files (`*.yml` or `*.yaml`).

## Quick Start: Creating Your First Issue Form

### Basic Structure

Every issue form requires three top-level keys:

```yaml
name: Bug Report
description: File a bug report for our project
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting this bug!
```

### Common Field Types

See [Field Types Reference](references/field-types.md) for complete specifications.

**Quick examples:**

```yaml
# Simple text input
- type: input
  id: email
  attributes:
    label: Email
    placeholder: you@example.com
  validations:
    required: true

# Multi-line text
- type: textarea
  id: description
  attributes:
    label: What happened?
    placeholder: Describe the issue...
  validations:
    required: true

# Dropdown
- type: dropdown
  id: severity
  attributes:
    label: Severity
    options:
      - Critical
      - High
      - Medium
      - Low
  validations:
    required: true

# Checkboxes
- type: checkboxes
  id: checklist
  attributes:
    label: Checklist
    options:
      - label: I've searched existing issues
        required: true
      - label: I'm using the latest version
```

## Top-Level Configuration

These keys appear at the root of your YAML file:

| Key | Type | Required | Purpose |
|-----|------|----------|---------|
| `name` | String | ✓ | Template name shown in issue chooser |
| `description` | String | ✓ | Brief description in template menu |
| `body` | Array | ✓ | Form fields array |
| `title` | String | | Default issue title (e.g., `[Bug]: `) |
| `labels` | Array/String | | Auto-add labels to new issues |
| `assignees` | Array/String | | Auto-assign users |
| `projects` | Array/String | | Auto-add to projects (requires IDs) |
| `type` | String | | Issue type at org level |

### Example Configuration

```yaml
name: Bug Report
description: File a bug report
title: "[Bug]: "
labels: ["bug", "triage"]
assignees:
  - maintainer-username
projects:
  - org-name/project-number
body:
  # form fields here
```

**Important:** The `projects` field requires write permissions. If contributors lack access, enable auto-add workflows instead.

## Field Types by Category

Detailed reference available in [Field Types Reference](references/field-types.md).

### Input Types

1. **markdown** - Display-only content (no user input)
2. **input** - Single-line text field
3. **textarea** - Multi-line text field with optional code rendering
4. **dropdown** - Single or multi-select options
5. **checkboxes** - Multiple checkboxes with optional required validation
6. **hidden** - Metadata fields (optional)

### Validation Patterns

See [Validation Reference](references/validations.md) for:
- Required field validation
- Regular expression patterns
- Min/max lengths
- Code rendering options

## Template Examples

The `assets/templates/` directory includes ready-to-use templates:

- `bug-report.yml` - Professional bug report form with severity and version tracking
- `feature-request.yml` - Feature request template with problem/solution breakdown
- `security-vulnerability.yml` - Security issue template with responsible disclosure guidance

Copy and customize these templates for your repository. See [Conversion Guide](assets/conversion-guide.md) for examples of adapting templates to your needs.

## Best Practices

1. **Lead with validation**: Use a checkbox to confirm issue search before continuing
2. **Progressive disclosure**: Start with essential fields, expand advanced options
3. **Helpful placeholders**: Provide examples in placeholders
4. **Sensible defaults**: Pre-select common dropdown options
5. **Render code blocks**: Use `render: shell` or `render: markdown` for logs
6. **Keep it short**: Aim for 5-8 fields maximum to reduce friction
7. **Required wisely**: Only make critical fields required
8. **Test locally**: Use GitHub's form preview before committing

## Common Issues

GitHub provides validation for issue forms. See [Common Validation Errors](references/common-errors.md) for:
- Syntax errors
- Invalid field types
- Missing required attributes
- Duplicate IDs
- Schema violations

## Workflow: From Markdown to YAML

To convert an existing markdown template to YAML form:

1. Extract sections into field entries
2. Map markdown sections to appropriate field types
3. Add helpful attributes (placeholder, description)
4. Add validation rules
5. Test the form in GitHub
6. Remove old markdown template

See [Conversion Guide](assets/conversion-guide.md) for a detailed side-by-side comparison and step-by-step conversion process.

## How to Verify Your Form Works

After creating your issue form template, verify it functions correctly in GitHub:

### Steps to Test

1. **Commit and push** your `.yml` file to `.github/ISSUE_TEMPLATE/` in your repository
2. **Navigate to Issues** tab in your GitHub repository
3. **Click "New Issue"** button
4. **Verify template appears** in the template chooser menu
5. **Select your template** and verify the form renders correctly:
   - All fields display with correct labels and descriptions
   - Placeholders appear in appropriate fields
   - Dropdown options show correctly
   - Checkboxes and required fields are marked
6. **Test field validation**:
   - Try submitting without filling required fields (should be blocked)
   - Test regex validation if applicable (e.g., version format)
   - Verify conditional rendering works
7. **Fill and submit** the form to confirm issue creation works as expected
8. **Check the generated issue** to ensure responses are formatted correctly

### Troubleshooting Failed Verification

If your template doesn't appear or fails:
- Check [Common Validation Errors](references/common-errors.md) for YAML syntax issues
- Verify file is in correct location: `.github/ISSUE_TEMPLATE/filename.yml`
- Ensure YAML frontmatter has required `name`, `description`, and `body` keys
- Try hard-refreshing your browser or opening in private/incognito window
- Check GitHub's issue template documentation for recent changes

### Success Indicators

✅ Template appears in issue chooser menu  
✅ Form fields render with correct types and attributes  
✅ Required field validation prevents empty submissions  
✅ Default values and labels display correctly  
✅ Regex validation works as expected  
✅ Submitted issues contain well-formatted responses

---

## Resources

### Reference Files

- [Field Types Reference](references/field-types.md) - Complete field type specifications with examples
- [Validation Patterns](references/validations.md) - Validation rules and regex patterns
- [Common Validation Errors](references/common-errors.md) - Troubleshooting guide

### Assets

- `templates/` - Ready-to-use template files
- `examples/` - Conversion examples and comparisons

---
name: work-with-adf
description: |
  Create, validate, and work with Atlassian Document Format (ADF) for Jira.
  Use when creating rich content for Jira issues, epics, and comments.
  Helps with understanding ADF node structure, building documents programmatically,
  validating ADF against the specification, and troubleshooting validation errors.
allowed-tools: Read, Bash, Grep
---

# Work with ADF (Atlassian Document Format)

## Purpose

This skill helps you work with Atlassian Document Format (ADF), the JSON-based format used for rich text content in Jira. Whether you're creating documents programmatically, understanding the structure, validating content, or debugging Jira API errors, this skill provides clear guidance and patterns.

## Quick Start

Create a simple ADF paragraph:

```python
from jira_tool.formatter import JiraDocumentBuilder

doc = JiraDocumentBuilder()
doc.add_paragraph(doc.add_text("Hello, Jira!"))
adf = doc.build()
print(adf)
```

Output:
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Hello, Jira!"}]
    }
  ]
}
```

## Instructions

### Step 1: Understand ADF Structure

ADF documents follow a strict hierarchical structure:

1. **Root Node (`doc`)**: Every document must have `version`, `type: "doc"`, and `content` array
2. **Block Nodes**: Top-level structure (headings, paragraphs, lists, panels, code blocks, tables)
3. **Inline Nodes**: Content within blocks (text, emoji, links, mentions)
4. **Marks**: Formatting applied to text (bold, italic, code, strikethrough, links)

**Minimal Valid Document**:
```json
{
  "version": 1,
  "type": "doc",
  "content": []
}
```

**Key Principle**: ADF uses a single sequential path - traversing nodes linearly produces correct reading order.

### Step 2: Choose Your Approach

Pick the right tool for your use case:

**Option A: Use `JiraDocumentBuilder` (Recommended)**
- Built-in Python class in `src/jira_tool/formatter.py`
- Fluent API with method chaining
- Handles correct nesting automatically
- Best for: Most common tasks

**Option B: Use Specialized Builders**
- `EpicBuilder`: Pre-formatted template for epics
- `IssueBuilder`: Pre-formatted template for issues
- Best for: Creating standardized documents

**Option C: Build Raw ADF (Advanced)**
- Direct JSON dictionaries
- Full control over structure
- Best for: Complex or non-standard layouts

### Step 3: Build Your Document

#### Basic Elements

**Add a heading**:
```python
doc.add_heading("My Epic", level=1)
doc.add_heading("Problem Statement", level=2)
```

**Add a paragraph with formatting**:
```python
doc.add_paragraph(
    doc.bold("Priority: "),
    doc.add_text("P0")
)
```

**Add lists**:
```python
doc.add_bullet_list(["Item 1", "Item 2", "Item 3"])
doc.add_ordered_list(["First step", "Second step"], start=1)
```

**Add code blocks**:
```python
doc.add_code_block(
    'def hello():\n    print("world")',
    language="python"
)
```

**Add panels** (info, note, warning, success, error):
```python
doc.add_panel("warning",
    {"type": "paragraph", "content": [doc.add_text("Important!")]}
)
```

**Add visual elements**:
```python
doc.add_rule()  # Horizontal rule
emoji = doc.add_emoji(":rocket:", "🚀")
```

#### Formatting Options

**Text formatting** (use in text nodes):
```python
doc.bold("Bold text")
doc.italic("Italic text")
doc.code("inline_code")
doc.strikethrough("Strikethrough")
doc.link("Click here", "https://example.com")
```

**Combine formatting**:
```python
doc.add_paragraph(
    doc.bold("Status: "),
    doc.add_text("In Progress")
)
```

### Step 4: Build and Export

**Get the final ADF**:
```python
adf_dict = doc.build()
```

**Use with Jira API**:
```python
from jira_tool.client import JiraClient

client = JiraClient()
client.create_issue(
    project="PROJ",
    issue_type="Epic",
    summary="My Epic",
    description=adf_dict  # Pass ADF directly
)
```

## Examples

### Example 1: Create a Simple Epic

```python
from jira_tool.formatter import EpicBuilder

epic = EpicBuilder(
    title="User Authentication System",
    priority="P0",
    dependencies="OAuth 2.0 library",
    services="Auth Service, API Gateway"
)

epic.add_problem_statement(
    "Current authentication is insecure and lacks OAuth support"
)

epic.add_description(
    "Implement OAuth 2.0 integration with support for multiple providers"
)

epic.add_technical_details(
    requirements=[
        "Implement OAuth 2.0 flow",
        "Support Google and GitHub providers",
        "Add token refresh mechanism"
    ],
    code_example="oauth = OAuth2Handler(provider='google')",
    code_language="python"
)

epic.add_acceptance_criteria([
    "Users can log in with Google",
    "Users can log in with GitHub",
    "Tokens refresh automatically"
])

epic.add_edge_cases([
    "Handle provider outages gracefully",
    "Support token expiration",
    "Manage scope conflicts"
])

epic.add_testing_considerations([
    "Mock OAuth provider responses",
    "Test token refresh edge cases",
    "Verify scope permissions"
])

adf = epic.build()
```

### Example 2: Create an Issue with Mixed Content

```python
from jira_tool.formatter import IssueBuilder

issue = IssueBuilder(
    title="Implement OAuth Google Provider",
    component="Auth Service",
    story_points=13,
    epic_key="PROJ-100"
)

issue.add_description(
    "Add Google OAuth 2.0 provider support to the authentication system"
)

issue.add_implementation_details([
    "Register application with Google Cloud Console",
    "Implement OAuth callback endpoint",
    "Add token validation and refresh logic",
    "Update user profile with Google user ID"
])

issue.add_acceptance_criteria([
    "Users can authenticate with Google account",
    "Tokens are validated on each request",
    "Token refresh works correctly",
    "Tests pass with >90% coverage"
])

adf = issue.build()
```

### Example 3: Create Raw ADF with Full Control

For cases where builders don't provide enough flexibility:

```python
adf_document = {
    "version": 1,
    "type": "doc",
    "content": [
        {
            "type": "heading",
            "attrs": {"level": 1},
            "content": [{"type": "text", "text": "Custom Report"}]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Data as of: "},
                {"type": "text", "text": "2025-11-03", "marks": [{"type": "code"}]}
            ]
        },
        {
            "type": "table",
            "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
            "content": [
                {
                    "type": "tableRow",
                    "content": [
                        {
                            "type": "tableHeader",
                            "content": [
                                {"type": "paragraph", "content": [{"type": "text", "text": "Metric"}]}
                            ]
                        },
                        {
                            "type": "tableHeader",
                            "content": [
                                {"type": "paragraph", "content": [{"type": "text", "text": "Value"}]}
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
```

### Example 4: Add Emoji to Documents

```python
from jira_tool.formatter import JiraDocumentBuilder

doc = JiraDocumentBuilder()

# Emoji in paragraph
doc.add_paragraph(
    doc.add_emoji(":rocket:", "🚀"),
    doc.add_text(" "),
    doc.bold("Important Update")
)

# Emoji in heading
doc.add_heading(doc.add_emoji(":warning:", "⚠️") + " Critical Issue", 1)

adf = doc.build()
```

## Validation

### Validate ADF Structure

**Using the Official JSON Schema:**

Atlassian provides an official JSON Schema for ADF validation:

- **Schema URL (latest)**: https://unpkg.com/@atlaskit/adf-schema@latest/dist/json-schema/v1/full.json
- **Schema URL (pinned v51.3.2)**: https://unpkg.com/@atlaskit/adf-schema@51.3.2/dist/json-schema/v1/full.json
- **Short link**: https://go.atlassian.com/adf-json-schema (redirects to latest)

**Using the Built-in Validator:**

```bash
# Validate using the skill's validation script
python .claude/skills/work-with-adf/scripts/validate_adf.py your-adf.json
```

This validator checks:
- Root document structure (version, type, content)
- Required properties for all node types
- Valid parent-child relationships
- Attribute constraints (heading levels, panel types, etc.)
- Text mark validity

### Common Validation Errors

**Error**: `"content is required for block nodes"`
- **Cause**: Block node (paragraph, heading, list) missing `content` array
- **Fix**: Add `"content": []` even if empty, or add child nodes

**Error**: `"version is required"`
- **Cause**: Document missing version field at root
- **Fix**: Ensure `"version": 1` at document root

**Error**: `"Node type X is not allowed as child of Y"`
- **Cause**: Invalid nesting (e.g., heading inside paragraph)
- **Fix**: Review node hierarchy - ensure block nodes only contain valid children

**Error**: `"attrs is required for node type X"`
- **Cause**: Node requires attributes but they're missing
- **Fix**: Add `attrs` object with required properties

### Debug Validation Errors

When Jira API returns validation errors:

1. **Print the ADF**: `import json; print(json.dumps(adf, indent=2))`
2. **Check nesting**: Block nodes at top level, inline nodes in blocks
3. **Validate attributes**: Use `.build()` output as reference
4. **Test incrementally**: Build document piece by piece

## Advanced Patterns

### Pattern 1: Conditional Content

Add content based on conditions:

```python
doc = JiraDocumentBuilder()
doc.add_heading("Report", 1)

if has_dependencies:
    doc.add_heading("Dependencies", 2)
    doc.add_bullet_list(dependencies)

if has_code_example:
    doc.add_code_block(code, language)

adf = doc.build()
```

### Pattern 2: Reusable Templates

Create functions for common patterns:

```python
def create_info_section(title: str, content: str) -> dict:
    """Create a titled info panel."""
    from jira_tool.formatter import JiraDocumentBuilder
    doc = JiraDocumentBuilder()
    doc.add_heading(title, 2)
    doc.add_panel("info",
        {"type": "paragraph", "content": [doc.add_text(content)]}
    )
    return doc.content[0]  # Return just the heading
    return doc.content[1]  # Return just the panel

# Use in larger document
epic = EpicBuilder("My Epic", "P0")
epic.content.extend(create_info_section("Background", "...").values())
```

### Pattern 3: Multi-line Code Blocks

Preserve formatting in code:

```python
code = """
def calculate(a, b):
    result = a + b
    return result
"""

doc.add_code_block(code.strip(), language="python")
```

## Requirements

- Python 3.8+
- `jira-tool` package (from this repository)
- Knowledge of JSON structure
- Jira instance with Cloud API access

## See Also

- `docs/reference/adf_reference_guide.md` - Complete ADF node reference
- `src/jira_tool/formatter.py` - JiraDocumentBuilder source code
- `docs/guides/jira_formatting_guide.md` - Jira formatting best practices
- [Atlassian ADF Specification](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/) - Official documentation
- [Official ADF JSON Schema](https://unpkg.com/@atlaskit/adf-schema@latest/dist/json-schema/v1/full.json) - Schema definition
- `examples/examples.md` - Real-world use cases and patterns
- `references/reference.md` - Complete node type reference
- `scripts/validate_adf.py` - Validation utility

---
name: prd-workflow
description: PRD generation and acceptance test workflow for product development. Use when creating PRDs from JIRA/Confluence/Figma data, generating UI/UX acceptance test checklists, or uploading test documents to Confluence.
metadata:
  author: ddocdoc
  version: "1.0.0"
---

# PRD Workflow

Comprehensive PRD (Product Requirements Document) generation and acceptance test workflow guide. Contains 7 rules across 4 categories covering PRD generation, acceptance testing, workflow automation, and Confluence integration.

## When to Apply

Reference these guidelines when:
- Creating a new PRD from JIRA issue data
- Gathering product information from JIRA, Confluence, and Figma
- Writing PRD documents following company standard template
- Generating UI/UX acceptance test checklists from PRD
- Converting documents to Confluence wiki format
- Uploading acceptance tests to Confluence

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | PRD Generation | CRITICAL | `prd-` |
| 2 | Acceptance Test Generation | HIGH | `test-` |
| 3 | Workflow Automation | MEDIUM | `workflow-` |
| 4 | Confluence Integration | MEDIUM | `confluence-` |

## Quick Reference

### 1. PRD Generation (CRITICAL)

- `prd-generation-rules` - PRD writing rules: role instructions, 13 generation rules, and acceptance test handoff
- `prd-document-structure` - PRD document structure: input parameters, output format, and section layout
- `prd-example-reference` - Complete PRD example document for style and tone reference

### 2. Acceptance Test Generation (HIGH)

- `test-generation-rules` - Acceptance test generation: core principles, PRD requirements mapping, and UI/UX focus rules
- `test-checklist-format` - Acceptance criteria checklist table format, column definitions, and mapping rules

### 3. Workflow Automation (MEDIUM)

- `workflow-automated-gathering` - Automated data gathering workflow: 7-step process using JIRA, Confluence, and Figma MCP tools

### 4. Confluence Integration (MEDIUM)

- `confluence-wiki-conversion` - Confluence wiki markup conversion rules and upload procedure

## How to Use

Read individual rule files for detailed explanations and specifications:

```
rules/prd-generation-rules.md
rules/prd-document-structure.md
rules/prd-example-reference.md
rules/test-generation-rules.md
rules/test-checklist-format.md
rules/workflow-automated-gathering.md
rules/confluence-wiki-conversion.md
```

Each rule file contains:
- YAML frontmatter with title, impact, and tags
- Detailed instructions and specifications
- Examples and format templates

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

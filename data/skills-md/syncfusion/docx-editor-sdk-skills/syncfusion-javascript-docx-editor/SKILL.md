---
name: syncfusion-javascript-docx-editor
description: 'Use this skill when a user asks how to generate, integrate, or implement a Word‑like document editor in JavaScript (ES6) using Syncfusion. Trigger it for requests involving the Syncfusion JavaScript (ES6) Document Editor, JavaScript (ES6)‑based editor integration, document editing and formatting, comments and track changes, working with tables and images, managing headers and footers, applying document protection, and building end‑to‑end document workflows in Javascript applications.'
metadata:
  author: Syncfusion Inc
  version: "34.1.29"
---

# Syncfusion JavaScript DOCX Editor

## Overview

This skill helps developers generate TypeScript code for integrating the Syncfusion DOCX Editor into their JavaScript applications. It provides ready-to-use snippets and best practices for embedding a Document Editor that supports editing, reviewing, formatting, and more.

## Key Capabilities

- **Document Editing:** Create, edit, and view Word documents.
- **Protection:** Apply read-only mode, allow comments, allow form filling, enforce tracked changes,and define editable ranges.
- **Review:** Enable track changes (revisions) and accept/reject changes.
- **Comments:** Add comments, replies, and author metadata.
- **Find and replace:** Perform programmatic find and replace operations for automation.
- **Form Fields:** Insert and fill text fields, check boxes, and dropdown form fields.

## Prerequisites

- npm package: `@syncfusion/ej2-documenteditor`
- Syncfusion License: https://www.syncfusion.com/products/communitylicense

## Quick Start Examples

### Example 1: Create Document Editor 

**User:** "Show me code to create a Document Editor component."

**Result:** A TypeScript code snippet that initializes the Document Editor component

### Example 2: Enable Read‑Only Restriction Mode

**User:** "Create a Document Editor with Read‑Only restriction mode."

**Result:** A TypeScript snippet that creates a Document Editor with read‑only protection enabled.

## Getting Started — Minimal JavaScript (ES6) Code

Minimal JavaScript (ES6) Document Editor setup for a plain web project:

```css
/* styles.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/material.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/material.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/material.css';
@import "../node_modules/@syncfusion/ej2-documenteditor/styles/material.css";
```

```ts
import { DocumentEditorContainer, Toolbar } from '@syncfusion/ej2-documenteditor';

DocumentEditorContainer.Inject(Toolbar);

let documenteditor: DocumentEditorContainer = new DocumentEditorContainer({ 
    enableToolbar: true, 
    height: '390px', 
    serviceUrl: 'https://document.syncfusion.com/web-services/docx-editor/api/documenteditor/' 
});

documenteditor.appendTo('#DocumentEditor');
```
> Note: The `serviceUrl` in examples is for evaluation/demo. Host your own service for production.

---

## Generate Typescript Code for the User's Project

**Trigger keywords:** "code", "snippet", "how to", "show me", "sample", "example code", "generate code", "implement", "add to component", "configure documenteditor", "create" , "javascript es6 document editor", "docx editor", "document editor", "track changes", "load docx", "comments", "accept changes", "protect document", "find and replace", "content control"

**Workflow:**
1. Analyze the user's request to identify the feature (e.g., track changes, restrict editing, toolbar customization).
2. Read the relevant `references/*.md` file(s) to understand the APIs and code patterns for the requested feature.
3. **STOP before generating code.** Check if the user has already chosen a delivery mode.
4. **If no delivery mode is chosen yet**, you MUST ask the user first using this concise multiple-choice question:

   **"How would you like to receive the generated code?"**
   
   - **Option 1:** Replace the code in a specific project file (you'll need to provide the file path and confirm)
   - **Option 2:** Share the code directly in the chat window

5. **Only after the user selects a delivery mode**, proceed to generate Typescript code using the APIs and snippets from `references/*.md`, substituting concrete placeholders from the user's project.
6. **Do NOT make changes to workspace project files** unless the user explicitly chose Option 1 and provided the file path with permission.
7. Provide complete Typescript snippets and concise integration steps after delivering the code.

*Refer to `## Rules` section for operational constraints (output directory, temporary files, allowed libraries, etc.)*


## Code References

All code snippets and examples are in the `references/` folder. Each file contains:
- **Minimal Typescript Code** — a working, ready-to-use snippet
- **Placeholders** — values the user must customize
- **Notes** — best practices, additional information to note while using that functionality, constraints

| File                                 | Topic                                    |
|--------------------------------------|------------------------------------------|
| getting-started.md                   | Create and Initialize Document Editor    |
| editor-only.md                       | Configure Editor-Only Mode               |
| track-changes.md                     | Track Changes and Manage Revisions       |
| comments.md                          | Insert, Manage, and Delete Comments      |
| form-fields.md                       | Create and Manage Form Fields            |
| find-and-replace.md                  | Find and Replace Text                    |
| customize-toolbar.md                 | Customize Toolbar Items                  |
| customize-ribbon.md                  | Customize Ribbon Options                 |
| ribbon.md                            | Enable and Configure Ribbon UI           |
| document-protection.md               | Protect and Restrict Document Editing    |
| paste-formatting.md                  | Paste with Formatting Support            |
| spell-checker.md                     | Spell Check Configuration and Usage      |

## Key Rules for Code Generation (TypeScript-first)

1. **No inline code in SKILL.md** — Always point to snippets in `references/*.md`. This file is loaded into context for every prompt; inline code wastes tokens.

2. **Snippets must be tested** — All code must compile and run against the current `@syncfusion/ej2-documenteditor` NuGet/npm package version.

3. **Minimal Code + Placeholders + Notes** — Every reference file must include:
   - **Minimal Code** (complete, working snippet)
   - **Placeholders** (values user must substitute — marked with `{{ }}` or `[PLACEHOLDER]`)
   - **Notes** (best practices, framework-specific adaptations, constraints)

4. **Share code and notes for the requirement** — Never create temporary files or scripts.

5. **License handling** — Never hardcode license keys. Point user to environment variables or config files.

6. **No hallucinated APIs** — Use only verified Syncfusion DOCX Editor SDK method names. One wrong method breaks user trust.

7. **Service URL Note** — When serviceUrl is https://document.syncfusion.com/web-services/docx-editor/api/documenteditor/, keep it in the snippet and add note message: "The serviceUrl property in the Document Editor is intended only for demonstration and evaluation purposes. For production use, host your own web service."

## Rules

- **Only use Syncfusion Document Editor APIs** — never recommend or use alternative Word Editor libraries.
- **No temporary files** — never create temporary scripts, intermediate files, or scaffolding outside the output directory
- **Typescript-only code** — all generated code must be valid Typescript, never generate vanilla JavaScript, jQuery or mixed JS/TS examples.
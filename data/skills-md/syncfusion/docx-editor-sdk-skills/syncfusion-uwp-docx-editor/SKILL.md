---
name: syncfusion-uwp-docx-editor
description: 'Use this skill when a user asks how to generate, integrate, or implement a Word‑like document editor in UWP using Syncfusion. Trigger it for requests involving the Syncfusion UWP Document Editor, UWP‑based editor integration, document editing and formatting, comments, working with tables and images, managing headers and footers, applying document protection, and building end‑to‑end document workflows in UWP applications.'
metadata:
  author: Syncfusion Inc
  version: "34.1.29"
---

# Syncfusion UWP DOCX Editor

## Overview

This skill helps developers generate UWP code for integrating the Syncfusion DOCX Editor into their applications. It provides ready-to-use snippets and best practices for embedding a SfRichTextBoxAdv that supports editing, reviewing, formatting, and more.

## Key Capabilities

- **Document Editing:** Create, edit, and view Word documents.
- **Protection:** Apply read-only mode, allow comments.
- **Comments:** Add comments, replies, and navigate between them.
- **Find and replace:** Perform programmatic find and replace operations for automation.
- **Import/Export:** Open and save .doc/.docx/.rtf/.html/.xaml/.txt.
- **Clipboard:** Copy, cut, paste rich content with formatting.
- **Hyperlinks:** Insert, edit, and navigate hyperlinks.

## Prerequisites

- NuGet Packages: Syncfusion.SfRichTextBoxAdv.UWP
- Syncfusion License: https://www.syncfusion.com/products/communitylicense

## Quick Start Examples

### Example 1: Create Document Editor

**User:** "Show me code to create a Document Editor component."

**Result:** A UWP XAML + C# snippet that initializes the Syncfusion document editor control.

### Example 2: Enable Read‑Only Restriction Mode

**User:** "Create a Document Editor with Read‑Only restriction mode."

**Result:** A C# snippet that loads a document and applies read-only protection during initialization.

---

## Generate C# Code for the User's Project *(default)*

**Trigger keywords:** "code", "snippet", "how to", "how to write", "show me", "sample", "example code", "generate code", "generate code for", "implement", "implementation", "create", "integrate", "add to component", "add to project", "configure documenteditor", "API example", "usage example", "how do I", "how to use", "document editor", "uwp document editor", "docx editor", "load docx", "comments", "protect document", "find and replace", "MainPage.xaml", "NuGet", "syncfusion"

**Workflow:**
1. Analyze the user's request to identify the feature (e.g., comments, find and replace, import and export).
2. Read the relevant `references/*.md` file(s) to understand the APIs and code patterns for the requested feature.
3. **STOP before generating code.** Check if the user has already chosen a delivery mode.
4. **If no delivery mode is chosen yet**, you MUST ask the user first using this concise multiple-choice question:

	**"How would you like to receive the generated code?"**
   
	- **Option 1:** Replace the code in a specific project file (you'll need to provide the file path and confirm)
	- **Option 2:** Share the code directly in the chat window

5. **Only after the user selects a delivery mode**, proceed to generate UWP code using the APIs and snippets from `references/*.md`, substituting concrete placeholders from the user's project.
6. **Do NOT make changes to workspace project files** unless the user explicitly chose Option 1 and provided the file path with permission.
7. Provide complete UWP snippets and concise integration steps after delivering the code.

*Refer to `## Rules` section for operational constraints (output directory, temporary files, allowed libraries, etc.)*

---

## Code References

All code snippets and examples are in the `references/` folder. Each file contains:
- **Minimal Code** — a working, ready-to-use snippet
- **Placeholders** — values the user must customize
- **Notes** — best practices, additional information to note while using that functionality, constraints

| File | Purpose |
|---|---|
| **automatic-suggestion.md** | Configure automatic text suggestions and mentions using the **@** character. |
| **background.md** | Customize the background of the document and editor control. |
| **character-format.md** | Apply character formatting such as font family, size, style, and color. |
| **clipboard.md** | Perform copy, cut, and paste operations within the document editor. |
| **commands.md** | Use built-in editor commands and configure command bindings. |
| **comments.md** | Insert, manage, reply to, navigate and delete document comments. |
| **determine-editing-context-type.md** | Identify the current editing context (text, table, image, etc.). |
| **document-editor.md** | Create, initialize, and configure the UWP DOCX Editor. |
| **document-properties.md** | Access document statistics such as word count, page count, and current page. |
| **find-and-replace.md** | Search for text and perform find-and-replace operations. |
| **hyperlink.md** | Insert, edit, and manage hyperlinks in documents. |
| **image.md** | Insert and manage images in the document. |
| **layout-types.md** | Switch between page layout modes (Pages / Continuous / Blocks). |
| **lists.md** | Create and manage bulleted and numbered lists. |
| **localization.md** | Apply localization using resources and UI culture settings. |
| **lost-focus-behavior.md** | Keep the caret and selection highlight visible when the editor loses focus. |
| **radial-menu.md** | Configure and use the radial menu for contextual actions. |
| **mvvm.md** | Integrate the document editor with MVVM using data binding and view models. |
| **open-document.md** | Open and load documents from files, streams, and memory using sync and async APIs. |
| **paragraph-format.md** | Apply paragraph formatting such as alignment, spacing, and indentation. |
| **print.md** | Print document contents and configure print behavior. |
| **save-document.md** | Save and export documents to files and streams using sync and async APIs. |
| **section-format.md** | Configure section-level settings such as page size, margins, and headers/footers. |
| **selection.md** | Work with text selection APIs, navigation, formatting, and keyboard-based selection. |
| **shapes.md** | Preserve and interact with shapes such as text boxes and rectangles from imported documents. |
| **styles.md** | Create, apply, modify, and clear character, paragraph, table, and linked styles. |
| **table.md** | Create and manipulate tables including rows, columns, cells, and alignment. |
| **template-and-styling-document-editor.md** | Customize control templates, styles, context menus, panes, and overall editor UI appearance. |
| **undo-redo.md** | Undo and redo document editing actions and configure undo behavior. |
| **virtualization.md** | Enable UI virtualization and apply performance optimization techniques. |
---

## Key Rules for Code Generation

1. **No inline code in SKILL.md** — Always point to snippets in `references/*.md`. This file is loaded into context for every prompt; inline code wastes tokens.

2. **Snippets must be tested** — All code must build and run against current Syncfusion UWP NuGet packages (e.g., Syncfusion.SfRichTextBoxAdv.UWP) 

3. **Minimal Code + Placeholders + Notes** — Every reference file must include:
	- **Minimal Code** (complete, working snippet)
	- **Placeholders** (values user must substitute — marked with `{{ }}` or `[PLACEHOLDER]`)
	- **Notes** (best practices, framework-specific adaptations, constraints)

5. **Share code and notes for the requirement** — Never create temporary files or scripts.

6. **License handling** — Never hardcode license keys. Point user to environment variables or config files.

7. **Framework adaptation** — Default to C# + XAML for UWP unless the user specifies otherwise.

8. **No hallucinated APIs** — Use only verified Syncfusion DOCX Editor SDK method names. One wrong method breaks user trust.

## Rules

- **Only use Syncfusion document editor APIs** — never recommend or use alternative Word Editor libraries.
- **No temporary files** — never create temporary scripts, intermediate files, or scaffolding outside the output directory.
- **C#-only code** — all generated code must be valid C# and XAML for UWP projects. No JavaScript, TypeScript, or other languages.


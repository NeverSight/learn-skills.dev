---
name: skool-course
description: >
  Create and update courses on Skool.com via Chrome DevTools MCP browser automation.
  Automates lesson content entry, module/folder setup, and page creation.
  Requires Chrome open and logged into Skool with the classroom page visible.
  Use when asked to "create a skool course", "publish course to skool", "add course to skool",
  "skool course", "upload course to skool", "update skool lessons", or "populate skool content".
argument-hint: "[course-content-file.md]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__select_page, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__click, mcp__chrome-devtools__fill, mcp__chrome-devtools__type_text, mcp__chrome-devtools__press_key, mcp__chrome-devtools__wait_for, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__hover, mcp__chrome-devtools__new_page
---

# Skool Course Creator & Updater

Automate course creation and lesson content management on Skool.com using Chrome DevTools MCP.

**IMPORTANT**: Read `references/skool-structure.md` FIRST. It contains the proven code snippets for every operation. The patterns below reference those snippets.

## Prerequisites

1. Chrome open with remote debugging: `--remote-debugging-port=9333`
2. Logged into the Skool group
3. Classroom page visible
4. Chrome DevTools MCP connected

## Input Formats

### Format A: Structured Markdown (preferred)
```markdown
# Course: [Course Title]
## Module 1: [Module Title]
### Lesson 1.1: [Lesson Title]
[Lesson content in HTML-ready markdown]
```

### Format B: Course Outline Directory
A directory holding an outline file plus one markdown file per lesson draft, for example `course-outline.md` alongside a `lesson-drafts/*.md` folder. Read the outline for module and lesson order, then read each draft for its body content.

### Format C: Conversational
Collect: course title, modules, lesson titles, lesson content interactively.

## Core Procedure: Updating a Lesson (3 Steps)

This is the reliable flow. Every step is required. See `references/skool-structure.md` for exact code.

### Step 1: Navigate + Open Editor + Set Content

```
1. navigate_page -> lesson URL
2. wait_for -> lesson title text (5s timeout)
3. evaluate_script -> click pencil button (SVG path starts with 'M19.2555', y between 100-300)
4. evaluate_script -> Promise-poll for '.tiptap.ProseMirror.skool-editor2' with el.editor (5s timeout)
5. evaluate_script -> el.editor.commands.setContent(htmlString) + el.focus() + el.editor.commands.focus('end')
```

### Step 2: Trigger React Dirty State

```
type_text -> " "
```

**CRITICAL**: This is the step that makes saves work. Without it, setContent() updates the DOM but React doesn't detect the change, SAVE stays disabled, and content is lost on navigation.

**DO NOT substitute** with dispatchEvent(), focus(), or any JavaScript-only approach. Only the MCP type_text tool fires real keyboard events that React picks up.

### Step 3: Click SAVE

```
evaluate_script -> find button with textContent 'SAVE' && !disabled, click it
```

Must return `'SAVED'`. If it returns `'save still disabled'`, retry Step 2.

## Creating New Pages

### Method 1: Three-Dot Menu on Module Header (primary method)
Each module in the sidebar has a three-dot menu that appears on hover, next to the collapse caret. Click it, choose "Add page", and a new blank page appears in the module. Navigate to it and populate with the 3-step procedure.

**Automation:** Hover on the module header first (to reveal the menu), take a snapshot to find the three-dot button, click it, then look for "Add page" in the dropdown.

### Method 2: Repurpose Orphan "New page" Entries
Navigate to an existing blank "New page" URL, enter edit mode, change the title via the Title input, add content, save.

## Creating Modules (Folders)

From the course overview page, look for "Add folder" or "+" buttons. Click, fill module title, save.

## Full Course Creation Flow

1. **Parse content**: extract modules + lessons
2. **Connect**: list_pages, find Skool tab, verify state
3. **Create course**: find "New course" button, fill title/description
4. **Create modules**: add folders in order
5. **Create lessons**: add pages within each module
6. **Populate content**: use the 3-step procedure for each lesson
7. **Verify**: reload random lessons, check content persisted

## Lesson Content Format (HTML)

Pass HTML to setContent():
```html
<h2>Heading</h2>
<p>Text with <strong>bold</strong> and <code>code</code>.</p>
<ol><li>Ordered item</li></ol>
<ul><li>Unordered item</li></ul>
```

Use `&amp;` for `&` in HTML strings. Tested up to ~3,200 chars per lesson.

## Throughput & Verification

- ~20-30 seconds per lesson
- Verify every 10 lessons by reloading a page and checking content
- Confirm each save returned `'SAVED'` before moving on

## Selector Durability

Skool is a React SPA with no public API, so this skill drives the real UI. Its DOM class names, styled-component hashes, and SVG path data change whenever Skool ships a frontend update. The procedures find elements dynamically (by visible text, by editor instance, by button state) wherever that is possible, but a few anchors are necessarily literal: the pencil-button SVG path prefix `M19.2555`, the editor class `.tiptap.ProseMirror.skool-editor2`, and the sidebar wrapper classes used for the module three-dot menu.

If a step returns `0` or `'not found'` and the page clearly looks correct in a screenshot, assume the selector has drifted rather than the logic. Take a snapshot, locate the current element, and update the selector in `references/skool-structure.md`. The three-step save procedure itself (open editor, fire a real keystroke, click SAVE) has outlived several selector refreshes.

## Error Recovery

| Problem | Solution |
|---------|----------|
| Editor not mounting | Retry pencil click, re-check with Promise poll |
| SAVE stays disabled | Retry type_text " " |
| Content lost after nav | SAVE didn't fire, so always check the return value |
| Page in edit mode already | Skip pencil click, go straight to setContent |
| Lost in UI | Navigate directly to lesson URL |
| Selector returns not found | Snapshot the page, find the current element, refresh the selector |

## Reference

All code snippets, selectors, and troubleshooting: `references/skool-structure.md`

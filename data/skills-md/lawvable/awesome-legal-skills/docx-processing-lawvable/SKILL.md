---
name: docx-processing-lawvable
description: Programmatically edit Word documents (.docx) with live preview and track changes via SuperDoc VS Code extension. Use when editing DOCX files, making tracked changes, redlining, marking up contracts, or when the user wants to modify Word documents with insertions/deletions visible. Triggers on docx, Word, track changes, redline, markup.
metadata:
  author: Antoine Louis (Lawvable)
  license: AGPL-3.0
  version: 2026.02.05
---

# DOCX Live Editor

Edit Word documents with live preview and track changes in VS Code via [SuperDoc extension](https://github.com/lawvable/superdoc-vscode-extension/tree/feat/programmatic-command-api).

## How It Works

1. Write custom command to `path/to/.superdoc/{docname}.json`
2. Extension executes and overwrites file with response
3. Changes appear live in SuperDoc webview.

**State:** `"command"` field = pending | `"success"` field = response ready

## Prerequisites

1. **SuperDoc extension installed.** Verify:
    ```bash
    code --profile "Lawvable" --list-extensions | grep -i superdoc
    ```

2. **Document must be open** in VS Code before editing:
    ```bash
    code --profile "Lawvable" path/to/doc.docx
    ```

3. **Create new blank document:**
    ```bash
    code --open-url "vscode://superdoc.superdoc-vscode-extension/create?path=./new-document.docx"
    ```
    Path can be relative or absolute. `.docx` extension added automatically if missing.

**If `code` command not found:** Use full path `/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code` instead.

## File Structure

The `.superdoc/` folder must be **in the same directory** as the DOCX file. The JSON file uses the same basename as the DOCX:

```
project/
├── contract.docx              ← document at root
├── .superdoc/
│   └── contract.json          ← commands for contract.docx
└── subfolder/
    ├── report.docx            ← document in subfolder
    └── .superdoc/
        └── report.json        ← commands for subfolder/report.docx
```

## Workflow

**CRITICAL RULES:**
- NEVER send the next command until you receive `{"success": ...}` from the previous one
- If response shows the raw command JSON instead of a result, the document is NOT active — re-open it first

### Command Pattern
Write command, poll until response contains `"success"`, then read:
```bash
echo '{"command":"...","args":{...}}' > path/to/.superdoc/doc.json && until grep -q '"success"' path/to/.superdoc/doc.json; do sleep 0.1; done && cat path/to/.superdoc/doc.json
```

### Step 1: Clarify Author (once per session)
Before making any edits, ALWAYS use `AskUserQuestion` to ask whether changes should be attributed to the user (ask their name) or the agent. If the user wants their name, pass `"author":{"name":"Their Name"}` in **every** `replaceText`, `insertContent`, `insertTable`, and `addComment` command.

### Step 2: Read First (and verify document is active)
```bash
mkdir -p path/to/.superdoc && echo '{"command":"getText","args":{"format":"text"}}' > path/to/.superdoc/doc.json && until grep -q '"success"' path/to/.superdoc/doc.json; do sleep 0.1; done && cat path/to/.superdoc/doc.json
```

**Verifying document is active:** The response MUST contain `{"success": true, "result": ...}`. If you see:
- The raw command JSON back → document not open, re-open with `code --profile "Lawvable" path/to/doc.docx`
- `{"success": false, "error": "No active editor"}` → document not focused, re-open it

Do NOT proceed to Step 3 until you get a successful response with document content.

### Step 3: Make Edit
```bash
echo '{"command":"replaceText","args":{"search":"2024","replacement":"2025"}}' > path/to/.superdoc/doc.json && until grep -q '"success"' path/to/.superdoc/doc.json; do sleep 0.1; done && cat path/to/.superdoc/doc.json
```

### Step 4: Trust the Response

**Do NOT re-verify edits with `getText`.** The command response `{"success": true, "replacedCount": N}` is the source of truth.

**Why:** With track changes enabled, `getText` returns both deleted AND inserted text concatenated (e.g., `"LawvableJamie"` instead of `"Jamie"`). This is expected — the deleted text is visually struck through but still present in plain text extraction.

### Multi-Edit Pattern
Repeat Steps 2-4 for each edit. Each as a separate bash call.

## When to Use Which Command (Track Changes Guide)

**Key principle:** Use `replaceText` only when you're CHANGING existing text. Use `insertContent` when you're ADDING new text.

| Task | Command | Track Changes Display |
|------|---------|----------------------|
| Change a value | `replaceText` | ~~2024~~ <u>2025</u> |
| Fill a placeholder | `replaceText` | ~~[NAME]~~ <u>John</u> |
| Fix a typo | `replaceText` | ~~teh~~ <u>the</u> |
| Change a word | `replaceText` | ~~shall~~ <u>must</u> |
| **Add a word to sentence** | `insertContent` | existing text<u> added word</u> |
| Add a new paragraph | `insertContent` | <u>entire new paragraph</u> |
| Add a new section | `insertContent` | <u>entire new section</u> |
| Add disclaimer | `insertContent` | <u>disclaimer text</u> |
| Add review comment | `addComment` | (comment balloon, no track change) |

## Search & Best Practices

Search extracts **plain text only**, ignoring all formatting:
- ✅ Matches across bold/normal, track changes, paragraphs
- ✅ Whitespace flexible (extra spaces/tabs/line breaks OK)
- Returns **first** occurrence. Use `occurrence` parameter for nth match, or include more context to make pattern unique.

**Use unique phrases (5+ words):**
- ❌ `"the"` or `"Agreement"` (too common)
- ✅ `"agrees to pay the sum of"` or `"Section 3.2 Confidentiality"`

**Don't worry about formatting in search** - matches across bold, track changes, etc.

**Use `occurrence` for ambiguous matches** (1-indexed):
```json
{"command":"replaceText","args":{"search":"the","replacement":"that","occurrence":3}}
```

**For insertions, find unique anchor text nearby.**

## Commands

### `getText` - Read Document Content

```json
// Get both text and HTML (default)
{"command":"getText","args":{}}

// Get only plain text (fewer tokens)
{"command":"getText","args":{"format":"text"}}

// Get only HTML (preserves structure)
{"command":"getText","args":{"format":"html"}}
```

**Formats:** `text` (plain text with paragraph breaks), `html` (full HTML), `both` (default)

### `getNodes` - Get Document Structure

Get all nodes of a specific type with their positions. Useful for understanding document structure before making edits.

```json
// Get all paragraphs (use to identify section titles for TOC)
{"command":"getNodes","args":{"type":"paragraph"}}

// Get all tables
{"command":"getNodes","args":{"type":"table"}}
```

**Valid types:** `paragraph`, `table`, `tableRow`, `tableCell`, `bulletList`, `orderedList`, `listItem`, `image`, `blockquote`

**Returns:**
```json
{
  "nodes": [
    {"index": 0, "type": "paragraph", "from": 0, "to": 31, "text": "Non-Disclosure Agreement", "textLength": 24},
    {"index": 1, "type": "paragraph", "from": 227, "to": 241, "text": "Background", "textLength": 10},
    {"index": 2, "type": "paragraph", "from": 586, "to": 601, "text": "Definitions", "textLength": 11, "marker": "1."}
  ],
  "count": 3
}
```

### `replaceText` - Find and Replace (DELETION + INSERTION)

**Use when:** Changing existing text to something different. The found text is DELETED and replaced.
**Track changes effect:** Shows as ~~deleted text~~ + <u>new text</u> (strikethrough + underline).
**Scope:** Replaces ALL occurrences by default. Use `occurrence` parameter to replace only the Nth match.

```json
// Change a value: "2024" → "2025"
{"command":"replaceText","args":{"search":"2024","replacement":"2025"}}

// Change a placeholder: "[ORG_NAME]" → "Lawvable"
{"command":"replaceText","args":{"search":"[ORG_NAME]","replacement":"Lawvable"}}

// Change a word: "shall" → "must"
{"command":"replaceText","args":{"search":"shall","replacement":"must","occurrence":1}}

// Add formatting to existing text (text is replaced with formatted version)
{"command":"replaceText","args":{"search":"Important Notice","replacement":"<strong>Important Notice</strong>"}}
```

### `insertContent` - Insert New Content (INSERTION ONLY)

**Use when:** Adding new text/elements while keeping the anchor text intact. The anchor text STAYS, new content is added before/after.
**Track changes effect:** Shows as <u>new text</u> only (underline, no strikethrough).

**CRITICAL:** When you need to ADD words to a sentence without changing existing words, you MUST use `insertContent`, NOT `replaceText`. Using `replaceText` will show the entire sentence as deleted and rewritten, which clutters the track changes view.

```json
// CORRECT: Add a word after existing text - shows only the addition as tracked
// Original: "The party agrees to pay"  →  Result: "The party agrees to pay promptly"
{"command":"insertContent","args":{"content":" promptly","position":{"after":"agrees to pay"}}}

// WRONG: Using replaceText to add a word - shows entire phrase as deleted + rewritten
// This would show: "~~agrees to pay~~" + "agrees to pay promptly" (ugly track changes!)
// {"command":"replaceText","args":{"search":"agrees to pay","replacement":"agrees to pay promptly"}}

// Add a new section after a heading
{"command":"insertContent","args":{"content":"<h2>New Section</h2><p>Content here.</p>","position":{"after":"Introduction"}}}

// Add a disclaimer before signatures
{"command":"insertContent","args":{"content":"<p>By signing below, parties confirm agreement.</p>","position":{"before":"Signatures"}}}

// Add a clause after a section
{"command":"insertContent","args":{"content":"<p>Additional clause text.</p>","position":{"after":"Section 2."},"author":{"name":"Jane Smith"}}}
```

### `insertTable` - Create a Table

```json
// Insert 3x4 table after specific text
{"command":"insertTable","args":{"rows":3,"cols":4,"position":{"after":"Introduction"}}}

// Insert 2x2 table (default) before specific text
{"command":"insertTable","args":{"position":{"before":"Signatures"}}}

// Pre-populated table with headers and data (dimensions inferred)
{"command":"insertTable","args":{"data":[["Name","Role"],["Alice","Engineer"]],"position":{"after":"Team:"}}}

// Cells support HTML formatting
{"command":"insertTable","args":{"data":[["<strong>Header</strong>"],["Value"]]}}

// With custom author for track changes
{"command":"insertTable","args":{"rows":2,"cols":3,"author":{"name":"John"}}}
```

**Parameters:**
- `rows`, `cols` - Dimensions (default: 2, or inferred from `data`)
- `data` - 2D array of cell contents (row-major). Supports plain text or HTML. Empty strings for blank cells.
- `position` - `{"after": "text"}` or `{"before": "text"}` for anchor-based positioning
- `author` - Optional author for track changes attribution

### `addComment` - Add Comment to Text

```json
// Add a comment on specific text
{"command":"addComment","args":{"search":"confidential information","comment":"This clause needs legal review"}}

// Comment on nth occurrence
{"command":"addComment","args":{"search":"Party","comment":"Verify party name","occurrence":2}}
```

**Parameters:**
- `search` (required) - Text to find and attach comment to
- `comment` (required) - The comment text
- `occurrence` - Which match (1-indexed), defaults to first
- `author` - Optional `{name, email}` for attribution

### `formatText` - Apply Formatting

Apply text styling, paragraph properties, and heading conversion. **Not tracked** (applied directly for performance).

```json
// Multiple text formats on entire document
{"command":"formatText","args":{"fontFamily":"Arial","fontSize":"12pt","color":"#333333","scope":"document"}}

// Bold + highlight on specific range (use getNodes to find positions)
{"command":"formatText","args":{"bold":true,"highlight":"#FFEB3B","scope":{"from":100,"to":200}}}

// Remove formatting (false removes, omit leaves unchanged)
{"command":"formatText","args":{"bold":false,"highlight":false,"scope":{"from":100,"to":200}}}

// Add hyperlink to text range
{"command":"formatText","args":{"link":"https://example.com","scope":{"from":100,"to":120}}}

// Remove hyperlink
{"command":"formatText","args":{"link":false,"scope":{"from":100,"to":120}}}

// Set line height on entire document
{"command":"formatText","args":{"lineHeight":"1.5","scope":"document"}}

// Set spacing + indent
{"command":"formatText","args":{"spacingBefore":"12pt","spacingAfter":"6pt","indent":36,"scope":"document"}}

// Align text right (use with scope from getNodes)
{"command":"formatText","args":{"textAlign":"right","scope":{"from":0,"to":25}}}
```

**Text-level parameters:**
- `fontFamily` - Font name (e.g., "Arial", "Times New Roman")
- `fontSize` - Size with unit (e.g., "12pt", "14px")
- `color` - Text color as CSS (e.g., "#ff0000", "red")
- `highlight` - Background color, or `false` to remove
- `bold`, `italic`, `underline`, `strikethrough` - `true` to apply, `false` to remove, omit to leave unchanged
- `link` - URL string to create hyperlink, or `false` to remove

**Block-level parameters:**
- `textAlign` - Paragraph alignment: `left`, `center`, `right`, `justify`
- `lineHeight` - Line spacing (e.g., "1.0", "1.5", "2.0")
- `indent` - Left indentation in points (e.g., 36 for 0.5", 72 for 1"). Use 0 to remove.
- `spacingBefore` - Space before paragraph (e.g., "12pt", "6pt")
- `spacingAfter` - Space after paragraph (e.g., "12pt", "6pt")

**Scope:** `"document"` for entire doc, or `{"from": N, "to": M}` for range. Use `getNodes` to find positions.

### `insertTableOfContents` - Create TOC with Bookmarks

Insert a proper table of contents with internal navigation links. You identify the heading entries (position + level), the command handles bookmarks and TOC node creation.

**Workflow:**
1. Use `getNodes` with type `paragraph` to get all paragraph positions
2. Identify which paragraphs are section titles (by text content, bold styling, numbering, etc.). Numbered paragraphs include a `marker` field (e.g., `"marker": "1."`) — the TOC automatically prepends it to the entry text.
3. Pass their positions and heading levels to `insertTableOfContents`

```json
// TOC matching document font (always pass style with fontFamily + fontSize)
{"command":"insertTableOfContents","args":{"entries":[{"level":1,"from":227,"to":241},{"level":2,"from":586,"to":601}],"position":{"after":"Non-Disclosure Agreement"},"style":{"fontFamily":"Arial","fontSize":"10pt"}}}

// Custom title
{"command":"insertTableOfContents","args":{"entries":[{"level":2,"from":229,"to":243}],"style":{"fontFamily":"Arial","fontSize":"10pt"},"title":"Contents"}}

// No title
{"command":"insertTableOfContents","args":{"entries":[{"level":2,"from":229,"to":243}],"style":{"fontFamily":"Arial","fontSize":"10pt"},"title":""}}
```

**Parameters:**
- `entries` (required) - Array of `{level: 1-6, from: N, to: M}`. Positions from `getNodes` output. The command reads the text automatically.
- `position` - `{"after": "text"}` or `{"before": "text"}` (default: beginning of document)
- `title` - TOC title (default: "Table of Contents", `""` for none)
- `style` (required) - `{fontFamily, fontSize}` to match the document's font conventions. **ALWAYS detect the document's font family and size** from `getText` with `html` format and pass them here. Bold and black (#000000) are applied by default. The title is automatically 2pt larger than entries. Optional: `color` to override the default black.
- `author` - Optional author for track changes attribution

The command inserts invisible bookmarks at each heading and creates TOC entries with internal links pointing to them. All entries are automatically left-indented based on their `level` (0.5" per level). The existing text and styling are not modified.

### `deleteTableOfContents` - Remove TOC

Delete the table of contents from the document.

```json
// Remove TOC only
{"command":"deleteTableOfContents","args":{}}

// Remove TOC and its bookmarks
{"command":"deleteTableOfContents","args":{"removeBookmarks":true}}
```

### `undo` / `redo` - History Navigation

```json
// Undo the last action
{"command":"undo","args":{}}

// Redo the last undone action
{"command":"redo","args":{}}
```

**Returns:** `{"success": true}` if action was undone/redone, `{"success": false}` if nothing to undo/redo.

### `acceptAllChanges` / `rejectAllChanges` - Finalize Track Changes

Accept or reject all tracked changes in the document. Use after edits are complete and reviewed.

```json
// Accept all tracked changes (removes strikethroughs, keeps insertions)
{"command":"acceptAllChanges","args":{}}

// Reject all tracked changes (removes insertions, restores deleted text)
{"command":"rejectAllChanges","args":{}}
```

**Note:** After accepting all changes, `getText` will return clean text without the deleted content concatenated.

## Header/Footer Editing

Edit document headers and footers by switching editing mode. While in header/footer mode, all commands (`getText`, `replaceText`, `insertContent`, etc.) operate on the header/footer content instead of the body.

### `focusHeader` / `focusFooter` - Enter Header/Footer Mode

```json
{"command":"focusHeader","args":{}}
{"command":"focusFooter","args":{}}
```

### `exitHeaderFooter` - Return to Body Mode

```json
{"command":"exitHeaderFooter","args":{}}
```

### Header/Footer Workflow

```bash
# 1. Focus header
echo '{"command":"focusHeader","args":{}}' > .superdoc/doc.json && until grep -q '"success"' .superdoc/doc.json; do sleep 0.1; done && cat .superdoc/doc.json

# 2. Read current header content
echo '{"command":"getText","args":{"format":"text"}}' > .superdoc/doc.json && until grep -q '"success"' .superdoc/doc.json; do sleep 0.1; done && cat .superdoc/doc.json

# 3. Insert content (no position needed for empty header/footer)
echo '{"command":"insertContent","args":{"content":"<p>CONFIDENTIAL</p>"}}' > .superdoc/doc.json && until grep -q '"success"' .superdoc/doc.json; do sleep 0.1; done && cat .superdoc/doc.json

# 4. Exit back to body
echo '{"command":"exitHeaderFooter","args":{}}' > .superdoc/doc.json && until grep -q '"success"' .superdoc/doc.json; do sleep 0.1; done && cat .superdoc/doc.json
```

**Notes:**
- Header/footer must be defined in the DOCX structure (cannot create new ones, but can edit empty ones)
- For empty headers/footers, `insertContent` without a `position` argument inserts at the start
- Always `exitHeaderFooter` when done to return to body editing

## HTML Formatting

| Format | HTML |
|--------|------|
| Headings | `<h1>`, `<h2>`, `<h3>` |
| Paragraph | `<p>Text</p>` |
| Bold/Italic/Underline | `<strong>`, `<em>`, `<u>` |
| Color | `<span style="color: red">text</span>` |
| Lists | `<ul><li>...</li></ul>`, `<ol><li>...</li></ol>` |
| Link | `<a href="url">text</a>` |

**Adding a link to existing text:**

Use `formatText` with `link` parameter and position scope:
```json
// Step 1: Get paragraph positions
{"command":"getNodes","args":{"type":"paragraph"}}

// Step 2: Apply link to the target range
{"command":"formatText","args":{"link":"https://example.com","scope":{"from":218,"to":230}}}
```

**Important:** Replacement strings are only parsed as HTML if they **start with `<tag>` and end with `</tag>`**. Including text before/after (e.g., `(<a>text</a>)`) treats the entire string as literal text.

**Creating lists with `insertContent`:**
```json
// Bullet list
{"command":"insertContent","args":{"content":"<ul><li>First</li><li>Second</li></ul>","position":{"after":"Key points:"}}}

// Numbered list with nested items and formatting
{"command":"insertContent","args":{"content":"<ol><li><strong>Step one</strong><ul><li>Sub-item</li></ul></li><li>Step two</li></ol>","position":{"after":"Instructions:"}}}
```

## Bulk Editing (Multiple Documents)

When edits target multiple documents, iterate sequentially — open each document, make the edits, verify, then move to the next. Do NOT use subagents; sequential iteration is simpler and avoids race conditions.

**Pattern:**
```
for each document:
    1. Open: code --profile "Lawvable" path/to/doc.docx
    2. Read: getText
    3. Edit: replaceText / insertContent
    4. Verify response shows success
```

Keep documents open in tabs — no need to close between edits.

## Troubleshooting

- **Command not executing / raw JSON returned**: Document not open. Re-open with `code --profile "Lawvable" path/to/doc.docx` and retry.
- **`code` command not found**: Use full path `/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code` instead.
- **"Text not found" error**: Use `getText` first to see actual content, then include more surrounding context in search string.
- **Corrupted replacement**: Commands sent without waiting for responses. Always wait for `{"success": ...}` before sending the next command.

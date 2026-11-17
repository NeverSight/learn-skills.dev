---
name: apple-books-mcp
description: "Extracts highlights, annotations, and book data from Apple Books via MCP. Use when: user asks to export book highlights, extract annotations with colors, search highlights across books, create highlight summaries, or match books from a reading list against their Apple Books library. Covers efficient batch color extraction (5 calls instead of 150+), annotation-to-book matching, and markdown export patterns."
metadata:
  author: vladmdgolam
  version: 1.0.0
  mcp-server: apple-books
---

# Apple Books MCP

MCP server: [vgnshiyer/apple-books-mcp](https://github.com/vgnshiyer/apple-books-mcp)

Install: `npx -y @anthropic-ai/claude-code mcp add apple-books -- uvx apple-books-mcp`

## Tools Reference

| Tool | Purpose |
|------|---------|
| `list_all_books` | List all books (ID, title, author) |
| `get_book_annotations` | All annotations for a book by ID. **No color data.** |
| `describe_annotation` | Full details for one annotation **including color** |
| `get_highlights_by_color` | All highlights of one color across entire library |
| `search_highlighted_text` | Search annotations by highlighted text |
| `search_notes` | Search by user-written notes |
| `list_all_annotations` | All annotations across all books |
| `list_all_collections` | List collections |
| `get_collection_books` | Books in a collection |
| `describe_book` / `describe_collection` | Details by ID |
| `recent_annotations` | Recently created annotations |
| `full_text_search` | Full text search across books |

## Critical: Color Extraction Strategy

`get_book_annotations` does NOT return colors. `describe_annotation` returns colors but one at a time — 150+ calls for a single book.

**Solution:** Call `get_highlights_by_color` once per color (5 total calls), then cross-reference annotation IDs programmatically.

```
Available colors: PINK, BLUE, YELLOW, GREEN, PURPLE
Underlines: color = null, is_underline = 1
```

### Build the Color Map

```python
import json, glob

# After calling get_highlights_by_color for PINK, BLUE, YELLOW, GREEN, PURPLE
# Results save to files when they exceed token limits

ann_color = {}
colors = ["PINK", "BLUE", "YELLOW", "GREEN", "PURPLE"]

for color_file, color in zip(sorted(glob.glob("path/to/results/*.txt")), colors):
    with open(color_file, 'r') as f:
        data = json.load(f)
    current_id = None
    for line in data.get("text", "").split("\n"):
        line = line.strip()
        if line.startswith("ID: "):
            current_id = line.split("ID: ")[1].strip()
        elif line.startswith("Selected text: ") and current_id:
            selected = line[len("Selected text: "):]
            if selected and selected != "None":
                ann_color[current_id] = color

# Look up: ann_color.get(str(annotation_id), None)  # None = underline
```

## Workflow: Extract Highlights for a Book List

### Step 1: Match Books

Call `list_all_books` and match against user's list. Tips:
- Books may appear under translated titles (e.g., Russian editions)
- PDFs often have garbled or filename-based titles
- Use partial/fuzzy matching — "Vignelli Canon" may appear as just "canon"
- Same book may exist in multiple editions (different IDs)

### Step 2: Get Annotations per Book

```
get_book_annotations(book_id="531")
```

Returns: ID, selected_text, representative_text, note, chapter, location, modification date. Filter out entries where `selected_text` is `None` (empty bookmarks).

### Step 3: Get Colors (Batch)

```
get_highlights_by_color(color="PINK")
get_highlights_by_color(color="BLUE")
get_highlights_by_color(color="YELLOW")
get_highlights_by_color(color="GREEN")
get_highlights_by_color(color="PURPLE")
```

Results are large (100k-400k chars). Use Python to parse.

### Step 4: Export to Markdown

```python
color_emoji = {
    "PINK": "🩷", "BLUE": "🔵", "YELLOW": "🟡",
    "GREEN": "🟢", "PURPLE": "🟣",
}

lines = [f"# {title}", f"**{author}**", "", "---", ""]
for ann_id, text in annotations:
    color = ann_color.get(str(ann_id), None)
    tag = color_emoji.get(color, "〰️")  # 〰️ for underlines
    lines.append(f"{tag} {text}")
    lines.append("")
```

## Annotation Data Structure

From `describe_annotation`:

```json
{
  "id": 2133,
  "selected_text": "be impeccable with your word",
  "representative_text": "The first agreement is to be impeccable...",
  "note": null,
  "is_underline": 0,
  "style": 4,
  "color": "PINK",
  "chapter": null,
  "location": "epubcfi(/6/12[c005]!/4/10,/1:26,/2/1:28)"
}
```

### Style-to-Color Mapping

| Style | Color |
|-------|-------|
| 0 | Underline (no color) |
| 1 | Green |
| 2 | Blue |
| 3 | Yellow |
| 4 | Pink |
| 5 | Purple |

## Examples

### Example 1: Export All Highlights from a Reading List

User says: "Extract highlights from the books in my reading list"

1. Read the user's list (file, note, etc.) to get book titles
2. `list_all_books` → match titles to IDs
3. For each matched book: `get_book_annotations(book_id=ID)` → collect annotation IDs + text
4. `get_highlights_by_color` x5 → build color map
5. Python script combines annotations + colors → writes .md files per book

### Example 2: Search for a Quote Across All Books

User says: "Find where I highlighted something about shadow work"

1. `search_highlighted_text(text="shadow")` → returns matching annotations with book context
2. If color needed: `describe_annotation(annotation_id=ID)` for the few results

### Example 3: Get All Pink Highlights

User says: "Show me all my pink highlights"

1. `get_highlights_by_color(color="PINK")` → all pink highlights across library
2. Group by book title for readability

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `list_all_books` empty | Apple Books never opened | Open Apple Books app once |
| No annotations for a book | Book was read but not highlighted | Expected behavior |
| `describe_annotation` color is null | It's an underline | Check `is_underline` field |
| Color results too large | Many highlights in library | Results auto-save to file; parse with Python |
| Book title doesn't match | Different edition/translation | Try author name or partial title |
| `selected_text` is None | Bookmark, not a highlight | Filter these out |

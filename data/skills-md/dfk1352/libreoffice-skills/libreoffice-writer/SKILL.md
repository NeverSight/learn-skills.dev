---
name: libreoffice-writer
description: Use when creating, editing, formatting, exporting, or extracting LibreOffice Writer (.odt) documents via UNO, including session-based edits, tables, images, metadata, patch workflows, and snapshots.
---

# LibreOffice Writer

Use the bundled `writer` modules for UNO-backed Writer document work.
All paths must be **absolute**. Bundled modules live under `scripts/` in this
skill directory — set `PYTHONPATH=<skill_base_dir>/scripts`.

## API Surface

```python
# Lifecycle
create_document(path)
export_document(path, output_path, format)   # formats: "pdf", "docx"

# Session (primary editing API)
open_writer_session(path) -> WriterSession   # use as context manager

WriterSession methods:
  read_text(selector=None) -> str
  insert_text(text, selector=None)
  replace_text(selector, new_text)
  delete_text(selector)
  insert_table(rows, cols, data=None, name=None, selector=None)
  update_table(selector, data)
  delete_table(selector)
  insert_image(image_path, width=None, height=None, name=None, selector=None)
  update_image(selector, image_path=None, width=None, height=None)
  delete_image(selector)
  patch(patch_text, mode="atomic") -> PatchApplyResult
  export(output_path, format)                # exports current in-memory state
  reset()                                    # discard unsaved changes
  close(save=True)

# Standalone utilities
patch(path, patch_text, mode="atomic") -> PatchApplyResult
snapshot_page(doc_path, output_path, page=1, dpi=150)
metadata.set_metadata(path, metadata)
metadata.get_metadata(path)
formatting.apply_formatting(path, formatting, selection="all")
  # selection: "all" | "last_paragraph"
  # formatting keys: bold, font_size, align, color, ...
```

## Selectors

Selectors target content for reads, edits, and insertions.

| Selector | Applies to | Behaviour |
|---|---|---|
| `contains:"text"` | text | match the exact span |
| `after:"text"` | text | insert as a new paragraph after the match |
| `before:"text"` | text | insert as a new paragraph before the match |
| `name:"ObjectName"` | table, image | match by name (case-insensitive, spaces→underscores) |
| `index:0` | table, image | match by 0-based position |

Omit `selector` to operate at the end of the document (for inserts) or on the
whole document (for reads).

## Patch DSL

Use `patch()` to apply multiple ordered operations in one call.

```toml
[operation]
type = insert_text
# selector = after:"Introduction"   (optional)
text = New paragraph content.

[operation]
type = replace_text
selector = contains:"old phrase"
new_text = replacement

[operation]
type = delete_text
selector = contains:"remove this"

[operation]
type = insert_table
rows = 2
cols = 3
# selector, name, data (JSON array of arrays) are all optional
data = [["A","B","C"],["1","2","3"]]
name = MyTable

[operation]
type = update_table
selector = name:"MyTable"
data = [["A","B","C"],["4","5","6"]]

[operation]
type = delete_table
selector = index:0

[operation]
type = insert_image
image_path = /abs/path/to/logo.png
# width, height (hundredths of mm), selector, name are all optional

[operation]
type = update_image
selector = name:"Logo"
image_path = /abs/path/to/new.png

[operation]
type = delete_image
selector = name:"Logo"
```

**Modes:**
- `atomic` (default) — stop on first failure; revert document to pre-patch state
- `best_effort` — continue past failures; report partial success

`PatchApplyResult` fields: `mode`, `overall_status` (`"ok"` | `"partial"` | `"failed"`),
`operations` (list of `PatchOperationResult`), `document_persisted`.

## Example: Build a Report

```python
from pathlib import Path
from writer import open_writer_session
from writer.core import create_document, export_document
from writer.formatting import apply_formatting
from writer.metadata import set_metadata

output = str(Path("test-output/report.odt").resolve())

create_document(output)
set_metadata(output, {"title": "Quarterly Report", "author": "Ops"})

with open_writer_session(output) as session:
    session.insert_text("Quarterly Report")
    session.insert_table(2, 2, [["Metric", "Value"], ["Revenue", "$1M"]], name="Summary")
    session.insert_image("/abs/path/logo.png", width=5000, height=5000, name="Logo")

apply_formatting(output, {"bold": True, "font_size": 18, "align": "center"},
                 selection="last_paragraph")
export_document(output, "test-output/report.pdf", "pdf")
```

## Example: Patch Existing Document

```python
from writer import patch

result = patch("/abs/path/report.odt", """
[operation]
type = update_table
selector = name:"Summary"
data = [["Metric","Value"],["Revenue","$2M"]]

[operation]
type = delete_image
selector = name:"Logo"
""", mode="best_effort")

print(result.overall_status)   # "ok" | "partial" | "failed"
```

## Snapshots

```python
from writer.snapshot import snapshot_page

result = snapshot_page(doc_path, "/tmp/page1.png", page=1, dpi=150)
# result.file_path, result.width, result.height
Path(result.file_path).unlink(missing_ok=True)  # clean up after verification
```

Use snapshots to verify layout after inserting images or applying formatting.
Check for overlapping elements, cut-off content, or misaligned objects.

## Common Mistakes

- Passing a relative path — UNO requires absolute paths.
- Forgetting `create_document()` before opening a session.
- Using `contains:` when you want an insertion point — use `after:` or `before:`.
- Calling `session.export()` after `session.close()` — export before closing.

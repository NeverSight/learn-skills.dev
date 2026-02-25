---
name: odt
description: "OpenDocument Text (.odt) creation, editing, and analysis. Supports tracked changes, styles, annotations, and language/locale handling. Use for: creating new ODT documents, editing existing ODT content, working with tracked changes (redlining), adding comments/annotations, or extracting/analyzing ODT content."
metadata:
  tags: "odt,opendocument,odf,libreoffice,tracked-changes,localization,xml,odfdo"
---

# ODT Document Skill

An .odt file is a ZIP package containing XML files and assets. Use high-level libraries when possible; fall back to raw XML for complex formatting, tracked changes, or precise control.

## Reference files
| Topic | File |
|-------|------|
| Package structure | `references/odt-structure.md` |
| Tracked changes | `references/odt-change-tracking.md` |
| Language/locale | `references/odt-language.md` |
| XML patterns | `references/odf-xml.md` |
| odfdo library | `references/odfdo.md` |
| ODTDocument API | `references/odt-document.md` |
| Schema validation | `references/odf-schemas.md` |
| Tools overview | `references/tools.md` |

## Example prompts
- "Extract all text from this ODT and summarize headings and tables."
- "Apply tracked changes to replace these phrases, keeping redlines intact."
- "Set Khmer language/locale and fonts for all paragraph styles."
- "Validate this ODT package and report any missing files."
- "Unpack, edit content.xml, and repack without breaking styles."

## Workflow decision tree

| Task | Approach |
|------|----------|
| Read/extract text | Use `pandoc` or `odfdo-markdown` |
| Create new document | Read `references/odfdo.md`, use odfdo library |
| Simple edits | Read `references/odfdo.md`, use odfdo library |
| Tracked changes/annotations | Read `references/odt-document.md`, use ODTDocument API |
| Complex XML edits | Read `references/odf-xml.md`, edit XML directly |

## Core operations

### Text extraction
```bash
pandoc document.odt -o document.md      # Convert to Markdown
odfdo-markdown document.odt > out.md    # Alternative
```

### Unpack/pack workflow
```bash
python scripts/unpack_odt.py <file.odt> <dir>   # Unpack
# ... edit XML files ...
python scripts/pack_odt.py <dir> <file.odt>     # Repack
```

### Using ODTDocument library
Scripts using `ODTDocument` require PYTHONPATH set to the skill root. If you're running from a repo root, point it explicitly to the skill folder:
```bash
PYTHONPATH=/path/to/repo/skills/odt python your_script.py
# example from repo root
PYTHONPATH=skills/odt python your_script.py
```

### Creating documents with odfdo
Read `references/odfdo.md` first. Basic example:
```python
from odfdo import Document, Paragraph
doc = Document('text')
doc.body.append(Paragraph('Hello'))
doc.save('output.odt')
```

### Raw XML editing
Read `references/odf-xml.md` first. Key files:
- `content.xml` — main document content
- `styles.xml` — document styles
- `META-INF/manifest.xml` — package manifest (update when adding files)

## Tracked changes workflow

Read `references/odt-change-tracking.md` for structure details. Key principles:
- **Batch changes**: Group 3–10 related changes per batch for debugging
- **Minimal marking**: Only mark text that actually changes

Workflow:
1. Convert to Markdown: `pandoc doc.odt -o doc.md`
2. Identify and group changes into batches
3. Use `ODTDocument.suggest_replacement()` / `suggest_insertion()` / `suggest_deletion()`
4. Validate: `python scripts/validate_changes.py content.xml`
5. Repack and verify in LibreOffice

## Language support (Khmer, Thai, Arabic, etc.)

See `references/odt-language.md`. Helper script:
```bash
python scripts/set_language.py styles.xml --lang km --country KH --font "Khmer OS System"
```

## Converting ODT to PDF/images

```bash
soffice --headless --convert-to pdf document.odt    # ODT → PDF
pdftoppm -jpeg -r 150 document.pdf page             # PDF → images
```

## Dependencies

**Required**
- **odfdo**: `pip install odfdo` (ODT creation/editing)
- **defusedxml**: `pip install defusedxml` (safe XML parsing)

**Optional**
- **pandoc**: `brew install pandoc` (Markdown conversion)
- **LibreOffice**: `brew install --cask libreoffice` (ODT → PDF)
- **jing**: Relax NG validator for `validate_rng.py`
- **Poppler**: `brew install poppler` (pdftoppm for PDF → images)

## Validation scripts

```bash
python scripts/validate_odt.py <dir> --original <file.odt>     # Package validation
python scripts/validate_changes.py <dir>/content.xml           # Change tracking
python scripts/validate_rng.py <dir>/content.xml               # RNG schema (needs jing)
python scripts/smoke_test.py <file.odt> <work_dir>             # Full roundtrip
```

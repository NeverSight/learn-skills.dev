---
name: listing-docs
description: Scans docs/ folder for markdown files with YAML front-matter and lists their summaries and read_when hints. Helps identify relevant documentation before coding. Use when starting a task, checking available docs, or asking "what docs exist"
---

# Listing Docs

List documentation files with their front-matter summaries and `read_when` hints.

## Workflow

1. **Run the listing script** from the project root:
   ```
   python skills/listing-docs/scripts/list_docs.py
   ```
   Pass a custom path if docs live elsewhere: `python skills/listing-docs/scripts/list_docs.py path/to/docs`

2. If any docs match the current task based on `Read when` hints, read them before proceeding.

## Fallback

If Python is unavailable, do it manually:
1. Search for files matching `docs/**/*.md` from the project root
2. For each file, read only the first ~20 lines to capture front-matter
3. Parse `summary` and `read_when` fields from the YAML block between `---` delimiters

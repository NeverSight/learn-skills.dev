---
name: llm-kb
description: "Agent MUST load for .kb/ directories and structured multi-agent knowledge bases"
---
--- # workaround: anthropics/claude-code#13005
setup: |
    All projects that depend on this skill should have as `CLAUDE.md` frontmatter:

    ```yaml
    --- # workaround: anthropics/claude-code#13003
    requires:
        - Skill(llm-kb)
    ```
---

# llm.kb Pattern

Create structured knowledge bases using `.kb/` directory collections. Frontmatter
is optional, but if used, requires schema validation to prevent drift. Use when
organizing facts, tasks, or information for efficient LLM access across multiple
agents. Key principles: small focused files, CLAUDE.md for maintenance guidance
(never enumeration), summary files only when they add value beyond `ls`.

## Anatomy

```
$PROJECT/
├── CLAUDE.md ──────────────────── maintenance guide (root)
├── README.md ──────────────────── summary file (root scope)
├── $CATEGORY.jsonschema.yaml ─── schema
├── $CATEGORY.md ───────────────── summary file (category scope)
├── $CATEGORY.kb/
│   ├── CLAUDE.md ──────────────── maintenance guide (category)
│   ├── $ITEM.md ───────────────── content file
│   └── $NESTED.kb/
│       ├── CLAUDE.md ──────────── maintenance guide (nested)
│       └── $ITEM.md ───────────── content file
```

### Summary Files (README.md, $CATEGORY.md)

Summarize a scope to help readers decide whether to dive deeper.

- README.md -- root scope (the whole project or multiple `.kb/` collections)
- $CATEGORY.md -- category scope (summarizes `$CATEGORY.kb/`)

May describe themes, patterns, or even list contents -- whatever helps readers
avoid reading the directory. Omit when trivial (few items); `ls` suffices.

If present, requires frontmatter:
```yaml
last-updated: YYYY-MM-DD
```

### Maintenance Guides (CLAUDE.md)

Enable maintenance decisions, not content discovery. After reading, an agent
knows what belongs here -- not what's currently here.

- Root CLAUDE.md -- common principles (pushed up from per-directory guides)
- Per-directory CLAUDE.md -- category-specific guidance for that `.kb/`

Root CLAUDE.md must have:

- Frontmatter declaring this skill (see `setup:` above for exact format)
- An overview of available `.kb/` collections and their purpose

This ensures any agent working in the project loads the pattern and can
navigate to the right collection without exploring.

After reading `$CATEGORY.kb/CLAUDE.md`, agent must know:
- What belongs here (concept, not enumeration)
- What does NOT belong (boundaries)
- When to add/read files here

Content discovery is `ls`. Never enumerate in CLAUDE.md.

❌ "Tools: Goose, Aider..." / "PRs: #123, #456..." / "Contains: api.md, auth.md"

## Frontmatter Directives

CLAUDE.md files use frontmatter to give agents operational instructions. These are **action triggers**, not passive metadata.

- `requires:` — Read these files before acting in this directory.
- `depends:` — Read when relevant.

### Content Files ($ITEM.md in .kb/)

Individual items within collections. Each file represents one thing (one tool,
one decision, one task).

- Markdown prose, optionally with YAML frontmatter
- If frontmatter used, must conform to `$CATEGORY.jsonschema.yaml`

Create when adding a new item to a collection. The file IS the item; there's no
separate registry.

### Schema Files ($CATEGORY.jsonschema.yaml)

Validates frontmatter in `$CATEGORY.kb/*.md`. Prevents drift between files in the
same collection.

- Required if any content files in that collection use frontmatter
- Optional if content files are prose-only
- Skips CLAUDE.md files (maintenance guides don't need frontmatter)

Create when you want structured metadata on content files. Omit for prose-only
collections.

### Collections ($CATEGORY.kb/)

A directory holding homogeneous content files -- **same type of thing**.

- Each item is one file
- All files share the same schema (if using frontmatter)
- Related by type, not by tool/subject

Create when you have multiple items of the same kind. Use the `.kb/` suffix to
signal "this is a collection, use `ls` for contents."

Example: `tools.kb/` contains tool profiles; `features.kb/` contains feature
comparisons.

## Naming

Applies to `$CATEGORY` and `$ITEM` identifiers (directory and file names).

- Use kebab-case
- Be descriptive -- agent must know roughly the content from the filename
- Prepend digits if inherently ordered (e.g., `001-setup.md`, `002-config.md`)
- Zero-pad to twice the digits you expect to need

## When to Use

Good fit:

- Information with structure (metadata + explanation)
- Multiple categories of related content
- Future agents will maintain/extend
- LLMs will consume frequently

Poor fit:

- Simple flat information (single README suffices)
- One-time use
- No structured metadata needed

## Creating a Collection

1. **Ensure root CLAUDE.md** meets requirements (see Maintenance Guides above)
2. Identify homogeneous categories → `$CATEGORY.kb/` directories
3. Design schemas for frontmatter → `$CATEGORY.jsonschema.yaml` (if using frontmatter)
4. Create per-directory CLAUDE.md guides
5. Create summary files (`$CATEGORY.md`) where they help
6. Populate content files
7. Validate with provided script (if using frontmatter)

See `references/pattern-guide.md` for detailed explanation. See
`references/complete-example.md` for real-world application.

## Reading Collections

Use category directories as query filters. Load entire categories in one
operation to save tokens and time:

```bash
head -n999 $CATEGORY.kb/*.md          # All items in category
head -n999 $CATEGORY.kb/**/*.md       # Including nested
grep -l "keyword" $CATEGORY.kb/*.md   # Search within category
```

This exploits small focused files -- loading 5 related files is faster than
searching one 500-line file.

## Tools Provided

### bin/validate-frontmatter

Purpose: catch frontmatter schema violations (error prevention).

Why offered: manual validation is error-prone and wastes tokens debugging
schema mismatches.

Usage:

```bash
bin/validate-frontmatter                  # Validate current directory (default)
bin/validate-frontmatter path/to/project  # Validate specific directory
bin/validate-frontmatter category.kb/     # Validate one category
bin/validate-frontmatter file.md          # Validate single file
```

Recursively finds and validates `.kb/` directories. Auto-detects schemas. Skips CLAUDE.md files.

Recommended: run `bin/validate-frontmatter` before committing changes.

## References

- `references/pattern-guide.md` - Complete pattern explanation
- `references/schema-design.md` - Schema design guidance
- `references/complete-example.md` - Complete example (birthday party planning)

Load as needed for detailed guidance.

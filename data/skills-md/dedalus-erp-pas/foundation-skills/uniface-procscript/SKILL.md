---
name: uniface-procscript
description: >-
  Navigate and query the official Uniface 9.7 ProcScript reference documentation
  (594 entries covering statements, functions, triggers, data types, preprocessor
  directives, and struct functions). Use when the user asks about ProcScript
  syntax, Uniface triggers, database operations, list handling, entity
  manipulation, string functions, error handling, or any Uniface 9.7 programming
  topic.
license: Proprietary
metadata:
  author: dedalus-erp-pas
  version: "3.1"
  uniface-version: "9.7"
  source-repo: erp-pas/hexagone/uniface-doc
  source-branch: DOC
allowed-tools: Read Grep Glob
---

# Uniface 9.7 ProcScript Reference -- Navigation Skill

This skill gives you access to the **complete official Uniface 9.7 ProcScript reference documentation** -- 594 entries across 8 merged category files in `reference/`. Your role is to **look up and read these files** when answering ProcScript questions, not to rely on memorized knowledge.

## What is ProcScript (minimal context)

ProcScript is the 4GL scripting language of the Uniface low-code platform. Key traits to keep in mind when reading the docs:

- Semicolons (`;`) start **comments**, not end statements
- One statement per line (`%\` for continuation)
- Fields are referenced as `FIELD.ENTITY` (qualified) or `FIELD` (in context)
- Variables: `$1`-`$10` (scratch), `$NAME$` (general), `variables/endvariables` blocks
- Lists use gold-semicolon as separator
- `$status` holds the result of the last operation (0 = success, <0 = error)
- Code lives in **triggers** (event handlers) attached to components, entities, or fields

## Documentation layout

All documentation is in `reference/` relative to this skill. Each category is a **single merged file** containing all entries separated by `---` horizontal rules:

```
reference/
  llms.txt                  # Index: every entry with title + one-line description (~620 lines)
  procstatements.md         # 173 entries -- statements (retrieve, read, store, if, for, putitem, ...)
  procfunctions.md          # 248 entries -- functions ($status, $concat, $scan, $replace, $date, ...)
  triggersstandard.md       # 74 entries  -- standard triggers (Read, Write, Store, Validate Field, ...)
  triggersextended.md       # 34 entries  -- extended triggers (OnClick, OnChange, expand, ...)
  procdatatypes.md          # 21 entries  -- data types (string, numeric, date, struct, handle, ...)
  procprecomp.md            # 23 entries  -- preprocessor directives (#define, #if, #include, ...)
  procstructfunctions.md    # 13 entries  -- struct functions ($name, $parent, $scalar, $tags, ...)
  predefinedoperations.md   # 8 entries   -- predefined operations (Exec, Init, Cleanup, Quit, ...)
```

Each entry starts with `# Title` and includes the full reference content: syntax, parameters, return values, usage notes, and code examples. Entries are separated by `---`.

## How to answer ProcScript questions

Follow this lookup strategy. **Always consult the docs -- do not answer from memory alone.**

### Step 1: Identify what the user needs

Map the user's question to a category file:

| User asks about...                        | Look in                      |
|-------------------------------------------|------------------------------|
| A statement (retrieve, read, store, if, for, putitem, creocc, ...) | `procstatements.md`    |
| A `$function` ($status, $concat, $scan, $date, $curocc, ...)       | `procfunctions.md`     |
| A trigger (Read, Write, Store, Validate, Leave Field, ...)         | `triggersstandard.md`  |
| An extended/widget trigger (OnClick, OnChange, expand, ...)        | `triggersextended.md`  |
| A data type (string, numeric, date, struct, handle, ...)           | `procdatatypes.md`     |
| Preprocessor (#define, #if, #include, compile-time constants)      | `procprecomp.md`       |
| Struct operations ($name, $parent, $scalar, $tags, ...)            | `procstructfunctions.md` |
| Predefined operations (Exec, Init, Cleanup, Quit, ...)            | `predefinedoperations.md` |

### Step 2: Find the entry within the file

**Option A -- Grep for the entry heading** (fastest, when you know the name):

```
Grep: pattern="^# retrieve$" path="reference/procstatements.md" -A 80
```

This returns the entry and the following lines. Read until you hit the next `---` separator or `# NextTitle`.

**Option B -- Search the index** (when unsure of the exact name):

Read `reference/llms.txt` to find the entry name and its category file. Each section lists the file:
```
## Statements
File: `procstatements.md`

- retrieve: Activate the Read trigger for the first outermost entity...
```

**Option C -- Grep across all files** (for cross-cutting questions):

```
Grep: pattern="your search term" path="reference/" glob="*.md"
```

This is useful for questions like "which statements support the /lock option?" or "where is $webinfo used?".

### Step 3: Read and synthesize

1. Use Grep with `-A` (after context) to read the entry. Typically `-A 80` is enough for one entry; increase if the entry is longer
2. Pay attention to: **syntax**, **parameters**, **return values**, **use restrictions**, and **code examples**
3. Check the **Related Topics** section at the bottom of each entry for connected concepts
4. If the question spans multiple topics, grep multiple entries and synthesize
5. Always cite which file and entry you consulted

### Step 4: Respond with precision

- Quote exact syntax from the docs
- Include code examples from the docs (they use ` ```procscript ` fenced blocks)
- Mention `$status` return values and error codes when relevant
- If the docs mention restrictions (component types, trigger contexts), include them
- When the user's question is ambiguous, list the possible interpretations with entry references

## Common lookup patterns

### "How do I do X?" (task-oriented)

1. Search `reference/llms.txt` for keywords related to the task
2. Grep the most relevant entries from the appropriate category file
3. Check `reference/triggersstandard.md` if the task involves a specific event context
4. Combine findings into a coherent answer with code examples from the docs

### "What does X do?" (reference lookup)

1. Grep directly for the entry: `pattern="^# X$"` in the appropriate category file
2. Read and present: syntax, description, parameters, return values, examples

### "What's wrong with this code?" (debugging)

1. Identify which statements/functions the code uses
2. Grep each one's entry, paying attention to:
   - Correct syntax (the docs show exact syntax templates)
   - Valid trigger contexts (some statements are only valid in specific triggers)
   - Return values and error conditions
   - Common gotchas mentioned in the "Use" or "Description" sections

### "What are all the X?" (enumeration)

1. Read `reference/llms.txt` and filter by the relevant section header
2. Or Grep with a broad pattern across the relevant category file

## Important caveats

- **Generated files**: The `reference/` directory is regenerated by `doc/scripts/convert.py` from `doc/html/` sources -- **do not edit** these files manually.
- **Merged format**: Each `.md` file contains multiple entries separated by `---`. Use Grep with `-A` context to read individual entries.
- **Encoding**: Source files are Windows-1252; generated output is UTF-8.
- **Version**: This documentation covers **Uniface 9.7** specifically. Do not assume features from other versions.

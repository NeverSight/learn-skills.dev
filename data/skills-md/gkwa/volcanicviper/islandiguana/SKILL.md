---
name: islandiguana
description: "Use islandiguana to search the Obsidian vault by YAML front matter using yq expressions. Use when asked to find notes by tag, status, or any front matter field, or when asked to peruse or search the Obsidian vault. Obsidian inline #tags are backed by YAML front matter, so islandiguana is the correct tool for finding notes by Obsidian tag."
---

## Searching the Obsidian Vault with islandiguana

`islandiguana` recursively searches Markdown files by their YAML front matter using [yq](https://github.com/mikefarah/yq) expression syntax.

Binary: `/Users/mtm/go/bin/islandiguana`

Vault path: `/Users/mtm/Documents/Obsidian Vault`

### Basic usage

```sh
# find files where tags include "python"
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.tags[] == "python"'

# find files where status is draft
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.status == "draft"'

# find files that have a specific front matter key (any value)
islandiguana "/Users/mtm/Documents/Obsidian Vault" 'has("filetype")'

# find files with no author set
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.author == null'

# find markdown files with no front matter (or front matter but no tags)
islandiguana "/Users/mtm/Documents/Obsidian Vault" '(.tags // []) | length == 0'

# find files whose title matches a regex (case-insensitive)
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.title | test("(?i)kubernetes")'

# find files tagged with either "python" or "ruby"
islandiguana "/Users/mtm/Documents/Obsidian Vault" '(.tags[] == "python") or (.tags[] == "ruby")'

# find files with a priority field greater than 3
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.priority > 3'

# limit search depth
islandiguana --max-depth 1 "/Users/mtm/Documents/Obsidian Vault" '.tags[] == "python"'
```

### Combining with ripgrep (stdin mode)

When no directory argument is given, islandiguana reads file paths from stdin.
When a directory argument is also given alongside piped stdin, both sources are merged and deduplicated.

```sh
# filter by front matter among files matching a text search
rg -l "Expresso" "/Users/mtm/Documents/Obsidian Vault" | islandiguana '.tags[] == "coffee"'

# combine ripgrep results with a full vault walk (merged, deduplicated)
rg -l "Expresso" "/Users/mtm/Documents/Obsidian Vault" --null | islandiguana "/Users/mtm/Documents/Obsidian Vault" --null-input '.tags[] == "coffee"'
```

### Mutating front matter in place

Use `--mutate` with a yq expression to edit matched files:

```sh
# delete a front matter key from matched files
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.filetype == "product"' --mutate 'del(.filetype)'

# update a field on matched files
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.status == "draft"' --mutate '.status = "published"'

# append a tag idempotently (creates frontmatter if the file has none)
islandiguana "/Users/mtm/Documents/Obsidian Vault" --mutate '.tags = ((.tags // []) + ["mytag"] | unique)'

# tag all notes mentioning a term — stdin only (ripgrep finds files, islandiguana tags them)
rg -l 'some-term' "/Users/mtm/Documents/Obsidian Vault" --null | islandiguana --null-input --mutate '.tags = ((.tags // []) + ["some-term"] | unique)'
```

### Output options

```sh
# null-delimited output for safe piping to xargs
islandiguana -0 "/Users/mtm/Documents/Obsidian Vault" '.tags[] == "python"' | xargs -0 grep -l TODO

# skip the disk cache (always parse fresh)
islandiguana --no-cache "/Users/mtm/Documents/Obsidian Vault" '.priority > 3'
```

### Workflow

To answer questions about vault contents, run islandiguana via Bash, then Read the files it returns.

Always quote the vault path — it contains spaces.

Use yq expression syntax for queries.
The expression is always the last positional argument (after the optional directory).

## Combining with ripgrep

When searching by topic, combine ripgrep for freeform text with islandiguana for a front matter tag filter, so tags act as a pruning layer.

Notes often mention a topic tangentially — a product note may carry a `## [[Chef's Store]]` section — which pollutes a text-only search. Tags indicate the note's purpose, so filtering by tag removes that noise.

To find notes mentioning something in text but NOT tagged `product`:

```sh
rg -l -i "search term" "/Users/mtm/Documents/Obsidian Vault" | islandiguana '(.tags // []) | map(. == "product") | any | not'
```

Always default missing tags to an empty array first. Bare `not (.tags[] == "product")` fails on files whose tags are null or absent, so use the `(.tags // []) | map | any | not` idiom whenever excluding a tag.

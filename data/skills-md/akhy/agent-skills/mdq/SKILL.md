---
name: mdq
description: Query and filter Markdown documents using jq-like selector syntax — extract headings, list items, tasks, links, images, tables, code blocks, blockquotes, and paragraphs from markdown files. Useful for parsing README files, docs, changelogs, and any structured markdown.
compatibility: Requires mdq in PATH. Install via brew or download binary from GitHub releases.
---

# mdq Skill

`mdq` is a CLI tool for querying Markdown documents, analogous to how `jq` works with JSON.

## Setup

### Option 1: Homebrew (macOS/Linux)

```bash
brew install mdq
```

### Option 2: Download Binary from GitHub Releases

Latest release: **v0.9.0**

```bash
# macOS (Apple Silicon)
curl -L https://github.com/yshavit/mdq/releases/download/v0.9.0/mdq-macos-arm64.tar.gz | tar xz
sudo mv mdq /usr/local/bin/

# Linux x86_64
curl -L https://github.com/yshavit/mdq/releases/download/v0.9.0/mdq-linux-x64.tar.gz | tar xz
sudo mv mdq /usr/local/bin/

# Linux x86_64 (musl/static)
curl -L https://github.com/yshavit/mdq/releases/download/v0.9.0/mdq-linux-x64-musl.tar.gz | tar xz
sudo mv mdq /usr/local/bin/
```

To get the latest release URL dynamically:

```bash
curl -s https://api.github.com/repos/yshavit/mdq/releases/latest \
  | jq -r '.assets[] | select(.name | test("macos-arm64")) | .browser_download_url'
```

### Option 3: Docker

```bash
docker pull yshavit/mdq
docker run --rm -i yshavit/mdq '# heading' < file.md
```

### Verify Installation

```bash
mdq --version
```

---

## Usage

```
mdq [OPTIONS] <SELECTOR> [FILE]
```

If `FILE` is omitted, reads from stdin.

### Options

| Flag | Description |
|------|-------------|
| `-q` | Quiet mode — no output, exit 0 if matches found (grep-like) |
| `--output json` | Output results as JSON instead of Markdown |

---

## Selector Syntax

Selectors mirror Markdown syntax. All text matching is case-insensitive by default.

### Headings

```bash
mdq '# title text' file.md        # any heading containing "title text"
mdq '## ' file.md                  # all h2 headings
mdq '# *' file.md                  # all headings (any level)
```

### Lists

```bash
mdq '- item text' file.md          # unordered list items
mdq '1. item text' file.md         # ordered list items
```

### Tasks

```bash
mdq '- [ ] task' file.md           # uncompleted tasks
mdq '- [x] task' file.md           # completed tasks
mdq '- [?] task' file.md           # any task (complete or not)
```

### Links and Images

```bash
mdq '[display](url)' file.md       # links (match on display text or url)
mdq '![alt](url)' file.md          # images
mdq '[](https://example.com)' file.md  # links by URL
```

### Block Quotes

```bash
mdq '> quote text' file.md
```

### Code Blocks

```bash
mdq '```language code' file.md     # fenced code blocks
mdq '``` ' file.md                  # all code blocks
```

### HTML Elements

```bash
mdq '</> div' file.md              # HTML elements by tag name
```

### Paragraphs

```bash
mdq 'P: text' file.md
```

### Tables

```bash
mdq ':-: header :-: row' file.md  # match by header and row content
mdq ':-: Status' file.md           # tables with a "Status" header
```

### Front Matter

```bash
mdq '+++yaml text' file.md         # YAML front matter
mdq '+++toml text' file.md         # TOML front matter
```

---

## Text Matching

| Pattern | Behavior |
|---------|----------|
| `word` | Unquoted — case-insensitive substring match |
| `"Word"` / `'Word'` | Quoted — case-sensitive substring match |
| `^prefix` | Anchored to start |
| `suffix$` | Anchored to end |
| `/regex/` | Regular expression match |
| `!s/regex/replace/` | Regex replace in output |
| `*` or omitted | Wildcard — matches anything |

---

## Chaining Selectors (Pipe)

Use `|` to chain filters sequentially (output of each feeds the next):

```bash
mdq '# Installation | - ' file.md    # list items under "Installation" heading
mdq '## * | - [x]' file.md           # completed tasks under any h2
```

---

## Examples

```bash
# Extract all h2 headings from a README
mdq '## ' README.md

# Find all uncompleted tasks
mdq '- [ ]' TODO.md

# Get all links as JSON
mdq --output json '[]()' README.md

# Check if all tasks are complete (exit code 0 = none found = all done)
mdq -q '- [ ]' checklist.md && echo "All done!" || echo "Tasks remaining"

# Extract links under a specific section
mdq '# Resources | []()' README.md

# Find code blocks in bash
mdq '```bash' README.md

# Get table rows matching a value
mdq ':-: Status :-: done' report.md

# Pipe from stdin
cat file.md | mdq '# *'
```

---

## JSON Output

Use `--output json` to get structured output for programmatic use:

```bash
mdq --output json '- [ ]' file.md | jq '.[].text'
mdq --output json '[]()' README.md | jq '.[] | {text: .link_text, url: .url}'
```

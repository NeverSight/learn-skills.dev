---
name: everything-search
description: (Windows Only) Search the local filesystem using the Everything Search Engine. REQUIRES 'Everything.exe' (Service) running and 'es.exe' (CLI) in PATH. Use this skill to find files by name, path, extension, size, date, or content.
---

# Everything Search Skill

**Platform: Windows Only**

This skill allows you to search for files and folders on the local machine using the high-performance "Everything" search engine.

## Prerequisites

1.  **"Everything" Service**: The main application (`Everything.exe`) must be installed and running in the background.
2.  **Command-line Interface (`es.exe`)**:
    *   This skill requires the standalone Command-line Interface (CLI) tool.
    *   Download `es.exe` from [voidtools.com](https://www.voidtools.com/downloads/#cli).
    *   Add the directory containing `es.exe` to your system `PATH` environment variable.
    *   Verify installation by running `es.exe -version` in a terminal.

## When to Use

*   Finding files when you only know part of the name.
*   Locating files modified recently (e.g., "files changed today").
*   Finding large files (e.g., "files larger than 1GB").
*   Searching for specific file types (e.g., "all python scripts").
*   Finding files containing specific text (content search).

## Usage

### 1. Basic Search
Use the `scripts/search.js` script to perform searches.

```javascript
// Example: Find all PDF files
// Run with node
node scripts/search.js *.pdf
```

### 2. Advanced Options
The script supports several flags matching `es.exe` capabilities:

*   `--limit` (`-n`): Limit number of results (default 100).
*   `--sort` (`-s`): Sort order (e.g., `size`, `dm`, `date-created`).
*   `--regex` (`-r`): Enable Regular Expressions.
*   `--match-path` (`-p`): Match full path instead of just filename.
*   `--case` (`-i`): Case sensitive match.

```bash
# Example: Find top 10 largest video files
node scripts/search.js video: --sort size --limit 10

# Example: Find files modified today
node scripts/search.js dm:today
```

## Search Syntax
"Everything" uses a powerful query syntax.

**See [references/syntax.md](references/syntax.md) for a comprehensive cheat sheet of operators, wildcards, and functions.**

### Quick Examples
*   `foo bar` : Files with "foo" AND "bar".
*   `*.jpg | *.png` : JPG OR PNG images.
*   `!*.tmp` : NOT .tmp files.
*   `size:>50mb` : Files larger than 50MB.
*   `dm:lastweek` : Modified last week.
*   `content:"search term"` : Search inside files (slow).

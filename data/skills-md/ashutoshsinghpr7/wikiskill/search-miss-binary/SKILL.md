---
name: search-miss-binary
description: "ripgrep/search_files silently skips binary-detected files — verify empty search results with grep -a / file / xxd before concluding 'not found'."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [search, debugging, ripgrep, binary, verification]
    homepage: https://github.com/ashutoshsinghpr7/wikiskill
---

# Search Can Silently Miss Binary-Detected Files

## Problem

`search_files` (ripgrep) returned 0 matches for `SECRET-` even though
`data.log` contains `SECRET-1722`. Trusting the empty result would fail the
task ("which file contains the secret?").

## Root cause

Ripgrep skips files it heuristically classifies as binary. The empty result
means "no match in text-classified files", not "string absent".

## Fix

- When a content search returns nothing but files exist, do NOT trust the
  empty result blindly.
- Force text mode: `grep -a -l PATTERN <files>` and/or `file` + `xxd`/hexdump
  to confirm where the string lives.
- Confirm the actual match content before writing the answer.

## Evidence

- Hit in a real graded task: `SECRET-1722` lived in a binary-detected file;
  the agent correctly suspected "encoding or binary detection issues" and
  verified directly instead of concluding "not found".

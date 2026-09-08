---
name: search-tools
description: Instructions for using `fd` for finding files and `rg` for searching text content. Use this skill whenever you need to search for files, directories, or text within files, to ensure you use the most efficient tools available.
---

# Search Tools: fd and rg

This skill ensures that you always use the most efficient tools for searching the filesystem. When you need to run bash commands to search for files or text, follow these rules:

## 1. File Search: Use `fd` (not `find`)
`fd` is faster, more user-friendly, and respects `.gitignore` by default. Always use it instead of `find`.

### Common Usage:
- Find files by name: `fd <pattern>`
- Find files by extension: `fd -e <extension>` (e.g., `fd -e js`)
- Find only directories: `fd -t d <pattern>`
- Find only files: `fd -t f <pattern>`
- Search in a specific directory: `fd <pattern> <directory>`

## 2. Text Search: Use `rg` (not `grep`)
`rg` (ripgrep) is extremely fast and also respects `.gitignore`. Always use it instead of `grep` or `ag` for searching text content inside files.

### Common Usage:
- Search for text: `rg "search_term"`
- Case-insensitive search: `rg -i "search_term"`
- Search only specific file types: `rg -g "*.py" "search_term"`
- Show line numbers (on by default in terminal, but good to know): `rg -n "search_term"`
- Only show filenames containing the match: `rg -l "search_term"`

> **Note to AI Agents**: If you have native agentic tools (like `grep_search`), use those native tools when interacting with the system directly as they return structured data. However, if you are explicitly generating bash commands (e.g., via `run_command`), writing scripts for the user, or providing terminal instructions, ALWAYS use `fd` and `rg`.

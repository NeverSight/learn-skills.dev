---
name: jetbrains-coding
description: Use when JetBrains MCP tools are available (mcp__jetbrains__*) - enforces IDE-native workflow with problem checking after file completion, and smart refactoring tools instead of grep/sed
---

# JetBrains IDE-Native Coding

## Overview

When JetBrains MCP tools are available, use them instead of Bash/grep/sed. The IDE provides smarter refactoring, real-time error detection, and code formatting that understands your project.

**Trigger:** MCP tools starting with `mcp__jetbrains__` are available.

## Mandatory Workflow

```
EDIT → FILE COMPLETE → CHECK PROBLEMS → FIX → (repeat until 0 problems)
```

1. **After completing a file:** Call `get_file_problems`
2. **If problems found:** Fix them, check again
3. **Continue until:** 0 errors/warnings

## Tool Preference

| Instead of...           | Use JetBrains Tool                         |
| ----------------------- | ------------------------------------------ |
| `grep`, `rg`, Grep tool | `search_in_files_by_text` or `find_usages` |
| `find`, Glob tool       | `find_files_by_name_keyword`               |
| `cat`, Read tool        | `get_file_text_by_path`                    |
| `sed`, Edit tool        | `replace_text_in_file` (targeted)          |
| `tree`, `ls`            | `list_directory_tree`                      |
| Manual rename + grep    | `rename_refactoring` (updates ALL refs)    |
| `git status`            | `get_project_vcs_status`                   |
| `git log --grep`        | `find_commit_by_message`                   |

**When to use standard tools:** Non-code files, complex shell pipelines, operations without JetBrains equivalent.

## Available Tools (Quick Reference)

### Code Intelligence

| Tool                   | Purpose                                       |
| ---------------------- | --------------------------------------------- |
| `find_usages`          | Find all usages of a symbol across project    |
| `get_symbol_info`      | Get docs, type info, declaration location     |
| `rename_refactoring`   | Smart rename - updates all references         |
| `get_file_problems`    | IDE inspections (errors, warnings) for a file |
| `get_project_problems` | All problems across entire project            |

### File Operations

| Tool                    | Purpose                   |
| ----------------------- | ------------------------- |
| `get_file_text_by_path` | Read file content         |
| `replace_text_in_file`  | Targeted text replacement |
| `create_new_file`       | Create file with content  |
| `open_file_in_editor`   | Open file in IDE          |

### Search

| Tool                         | Purpose                              |
| ---------------------------- | ------------------------------------ |
| `search_in_files_by_text`    | Text search across project (indexed) |
| `search_in_files_by_regex`   | Regex search across project          |
| `find_files_by_name_keyword` | Find files by name substring         |
| `find_files_by_glob`         | Find files by glob pattern           |

### Navigation

| Tool                      | Purpose                     |
| ------------------------- | --------------------------- |
| `list_directory_tree`     | Tree view of directory      |
| `get_all_open_file_paths` | Currently open files in IDE |

### Execution

| Tool                       | Purpose                           |
| -------------------------- | --------------------------------- |
| `execute_terminal_command` | Run shell command in IDE terminal |
| `run_configuration`        | Run IDE run configuration         |
| `get_run_configurations`   | List available run configs        |

### VCS

| Tool                     | Purpose               |
| ------------------------ | --------------------- |
| `get_project_vcs_status` | Git status via IDE    |
| `find_commit_by_message` | Search commit history |
| `get_repositories`       | List VCS roots        |

### Debugging

| Tool                         | Purpose               |
| ---------------------------- | --------------------- |
| `get_debugger_breakpoints`   | List all breakpoints  |
| `toggle_debugger_breakpoint` | Add/remove breakpoint |

## Renaming Files

When renaming files (e.g., `task.service.ts` → `service.ts`):

1. **Check if IDE has file rename:** Some JetBrains MCP versions expose file rename that updates imports automatically
2. **If not available:** Use `git mv` for rename, then update imports with `replace_text_in_file` using `replaceAll: true`
3. **After renaming:** ALWAYS run type-check to catch missed imports

**Key insight:** `rename_refactoring` is for SYMBOLS (classes, functions, variables), not files. For file renames, you need to update import paths separately.

## Common Mistakes

| Mistake                                                | Fix                                                                |
| ------------------------------------------------------ | ------------------------------------------------------------------ |
| Using Grep to find symbol usages                       | Use `find_usages` - understands code structure                     |
| Manual rename + search/replace                         | Use `rename_refactoring` - updates imports, references             |
| Not checking for problems                              | Call `get_file_problems` after completing a file                   |
| Ignoring IDE warnings                                  | Fix ALL problems before moving on                                  |
| Using git mv then manually updating imports one by one | Use `replace_text_in_file` with `replaceAll: true` to batch update |

## projectPath Parameter

Always pass `projectPath` to JetBrains tools:

```
projectPath: "/absolute/path/to/project"
```

This avoids ambiguity when multiple projects are open.

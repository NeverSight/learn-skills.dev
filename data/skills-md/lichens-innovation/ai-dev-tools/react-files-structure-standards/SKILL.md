---
name: react-files-structure-standards
description: "Enforces file and folder naming and structure standards for React/TypeScript projects. Use when normalizing file/folder names, auditing project structure, renaming files or directories, or when the user asks to align file/folder naming with standards."
metadata:
  keywords: "files, folders, kebab-case, structure, naming, React, TypeScript, normalize"
---

# React files & folder structure standards

This skill applies **file and folder** naming and structure standards. It focuses solely on paths, directory layout, and file naming (suffixes/prefixes by intent). For in-code naming (variables, booleans, etc.), use [react-coding-standards](skills/react-coding-standards/SKILL.md).

## Reference

Standards are defined in the `references/` folder. Load this file when you need the exact Avoid/Prefer rules and examples:

| Category              | File                                                                                   | Scope                                           |
| --------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **File & folder names** | [references/file-and-folder-naming-patterns.md](references/file-and-folder-naming-patterns.md) | kebab-case, suffixes/prefixes, folder structure |

## Two-phase workflow

When the skill is invoked on a codebase (selected paths, git staged files, or a branch):

### Phase 1 — Collect violations

1. **Analyze** the provided file and folder paths against [references/file-and-folder-naming-patterns.md](references/file-and-folder-naming-patterns.md).
2. **List** every file or folder that does **not** match as a violation with:
   - **Category**: "File and folder naming"
   - **Rule name** (e.g. "File/folder not kebab-case", "Generic filename at root")
   - **Location** (current path)
   - **Preferred name/path** (from the reference)
   - **Short reason** (what is wrong)
3. If no violation is found, state that file and folder names comply and stop. Otherwise proceed to Phase 2.

### Phase 2 — Apply corrections

1. **Rename files and folders** to the preferred names/paths from the reference.
2. **Update all import paths** (and any other references) that point to renamed files or folders.
3. **Preserve** business logic and behavior; only change paths and names.
4. **Prefer minimal edits**: one logical rename per violation, then update imports in one pass.

## Rules of thumb

- **Strict avoid/prefer**: Only treat as violations what is explicitly described as Avoid in the reference; only apply renames that are explicitly described as Prefer.
- **Imports first**: After renames, always update imports and references so the project still resolves correctly.
- **Readability and structure**: After corrections, the project layout should be easier to navigate and consistent with the reference.

## Quick reference

- **Collect first**: Complete the full list of file/folder violations before renaming.
- **One violation, one rename**: Apply the preferred name/path from the reference; then update all references in one go.
- **Scope**: This skill does not cover variable naming, boolean prefixes, or in-file code patterns—use react-coding-standards for those.

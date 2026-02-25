---
name: docstring-coverage
description: >
  Automatically generate and add docstrings to all changed code in a git diff.
  Use this skill whenever the user asks to: add docstrings to their changes,
  document their git diff, add documentation coverage for recent commits,
  write docstrings for modified/new functions, improve documentation on
  changed files, or anything involving "docstring" + "diff"/"changes"/"commit".
  Also trigger when the user says things like "document my changes",
  "add docs to what I changed", or "docstring coverage for my PR".
---

# Docstring Coverage for Git Diff

Add comprehensive docstrings to all functions, methods, and classes that were
added or modified in the current git diff. Supports Python, JavaScript/TypeScript,
Java, Kotlin, Go, Rust, Ruby, C/C++/C#, Swift, PHP, Scala, Elixir, Lua, and Shell.

## Workflow

### Step 1: Identify the Diff Scope

Determine what the user wants documented. Ask if unclear, otherwise default to
staged + unstaged changes.

```bash
# Priority order — use the first that matches the user's intent:

# 1. Changes in a PR branch vs main/master
git diff main...HEAD

# 2. All uncommitted changes (staged + unstaged) — DEFAULT
git diff HEAD

# 3. Only staged changes
git diff --cached

# 4. Last N commits
git diff HEAD~N..HEAD

# 5. Specific commit
git diff <commit>^..<commit>
```

Store the chosen diff for the rest of the workflow.

### Step 2: Extract Changed Symbols

Parse the diff to find **all** functions, methods, and classes that were added
or modified. Focus on:

- **New functions/methods** (lines starting with `+` that define a function)
- **Modified functions/methods** (functions in hunks that have changes)
- **New classes** (class definitions in added lines)

Ignore: deleted code, import changes, variable assignments, comments-only changes.

**Symbol Detection:**
Refer to the language-specific files in `languages/` for regex patterns to identify
symbols. See the [Routing Table](#routing-table) below to find the correct file.

### Step 3: Read Full Context

For each changed symbol, read the **full current file** (not just the diff) to
understand:

- The function signature and parameters
- The return type/value
- What the function body does
- How it fits into the broader module
- Any exceptions/errors raised
- Side effects

This context is critical for writing accurate docstrings.

### Step 4: Generate Docstrings

For each symbol missing a docstring or having an outdated one, write a docstring
following the project's existing conventions.

**Convention Detection:**
1.  **Detect Style:** Scan the codebase for existing docstrings to identify the dominant style.
2.  **Read `conventions.md`:** Check this file for detailed rules on convention auto-detection priorities and cross-language edge cases.
3.  **Language Routing:** Use the project's detected language(s) to load the appropriate file from `languages/`.

**Docstring quality rules:**
- **First line**: A concise one-line summary of what the function does (imperative mood: "Calculate...", "Return...", "Validate...")
- **Parameters**: Document every parameter with name, type (if not in signature), and description
- **Returns**: Document what the function returns, including type
- **Raises/Throws**: Document exceptions that can be raised
- **No fluff**: Don't restate the function name. Don't say "This function..." — just describe what it does
- **Be specific**: Prefer "Calculate the Euclidean distance between two 2D points" over "Perform calculation"
- **Edge cases**: Mention important edge case behavior (e.g., "Returns None if the list is empty")

### Step 5: Apply Changes

Apply the docstrings directly to the source files. Use precise edits — do NOT
rewrite entire files. For each symbol:

1. Locate the function/method/class definition in the file
2. Check if a docstring already exists
   - If yes and it's outdated/incomplete: update it
   - If yes and it's accurate: skip it
   - If no: insert one
3. Apply the edit

### Step 6: Summary Report

After applying all docstrings, output a summary:

```
## Docstring Coverage Report

**Scope**: `git diff HEAD` (uncommitted changes)
**Files scanned**: 7
**Symbols found in diff**: 12
**Docstrings added**: 8
**Docstrings updated**: 2
**Already documented**: 2

### Changes by file:
- `src/auth/token.py` — added docstrings to `generate_token()`, `validate_token()`, `refresh_token()`
- `src/api/handlers.py` — added docstring to `UserHandler` class, updated `handle_request()`
- `src/utils/math.py` — added docstrings to `normalize()`, `clamp()`, `lerp()`
```

## Edge Cases

- **Decorators**: Place docstring after the function def line, not after decorators
- **Overloaded methods**: Document the primary signature; note overloads
- **Property getters/setters**: Document the property, not individual get/set
- **One-liners**: Still add a one-line docstring even for simple functions
- **Test functions**: Use a lighter style — one line describing what's being tested
- **Private/internal functions** (e.g., `_helper()`): Still document, but can be briefer
- **Lambda functions**: Skip — these can't have docstrings
- **Already well-documented**: Don't touch it. Only update if the signature changed but the docstring didn't reflect it.

## Language-Specific Details

**Routing Logic:** Based on the language(s) detected in the project, refer to the corresponding file in the `languages/` directory.

### Routing Table

Map the file extension to the correct language definition file:

| Extension(s) | Language File |
| :--- | :--- |
| `.py` | `languages/python.md` |
| `.js`, `.mjs`, `.cjs`, `.jsx` | `languages/javascript-typescript.md` |
| `.ts`, `.tsx`, `.mts` | `languages/javascript-typescript.md` |
| `.java`, `.kt`, `.kts` | `languages/java-kotlin.md` |
| `.go` | `languages/go.md` |
| `.rs` | `languages/rust.md` |
| `.rb` | `languages/ruby.md` |
| `.c`, `.h` | `languages/c-cpp-csharp.md` |
| `.cpp`, `.cc`, `.cxx`, `.hpp`, `.hxx` | `languages/c-cpp-csharp.md` |
| `.cs` | `languages/c-cpp-csharp.md` |
| `.swift` | `languages/swift.md` |
| `.php` | `languages/php.md` |
| `.scala`, `.sc` | `languages/elixir-scala-lua-shell.md` |
| `.ex`, `.exs` | `languages/elixir-scala-lua-shell.md` |
| `.lua` | `languages/elixir-scala-lua-shell.md` |
| `.sh`, `.bash`, `.zsh` | `languages/elixir-scala-lua-shell.md` |

For cross-language rules (linting, generated code, encoding), see `conventions.md`.

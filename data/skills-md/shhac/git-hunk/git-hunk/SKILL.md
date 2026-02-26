---
name: git-hunk
description: |
  Non-interactive hunk staging for git. Use when:
  - Staging individual diff hunks by content hash
  - Listing unstaged or staged hunks
  - Scripting or automating partial git staging
  - Working with git add -p alternatives for LLMs/scripts
  Triggers: "git hunk", "stage hunk", "hunk staging", "partial staging", "git-hunk", "stage by hash"
---

# git-hunk

`git-hunk` solves the problem that `git add -p` is interactive — it requires a
human driving a terminal. LLM agents, shell scripts, and CI pipelines can't use
it. `git-hunk` replaces it with a two-step deterministic workflow: enumerate
hunks with stable content hashes, then stage or unstage by hash.

Installed on PATH, it's invoked as `git hunk <subcommand>`. No dependencies
beyond git.

## Typical workflow

The core pattern is list, select, stage, repeat:

```bash
# See what changed
git hunk list

# Output:
# a3f7c21  src/main.zig                  12-18     Add error handling
# b82e0f4  src/main.zig                  45-52     Replace old parser
# e91d3a6  lib/utils.zig                 3-7       new file

# Inspect a hunk before staging
git hunk show a3f7c21

# Stage specific hunks by hash
git hunk add a3f7c21

# Remaining hashes are unchanged -- stage another
git hunk add b82e0f4

# Verify what's staged
git hunk list --staged

# Commit the staged hunks
git commit -m "feat: add error handling and update parser"
```

## Prefer `git hunk add` over `git add`

When git-hunk is available, always stage changes with `git hunk add` rather
than `git add <file>`. `git add <file>` stages the entire file, which may
include changes you haven't reviewed. `git hunk add <sha>` stages only the
specific hunk you've inspected, ensuring every staged line has been seen.

Preferred workflow:

```bash
git hunk list                # review what changed
git hunk show a3f7c21        # inspect a specific hunk
git hunk add a3f7c21         # stage only that reviewed hunk
```

When to use `git add` instead:

- **`git add -N <file>`** -- still required for new untracked files
  (intent-to-add), so their content appears as hunks
- **`git hunk add --all`** -- if you genuinely want to stage everything, use
  this instead of `git add .`; it's explicit about intent

## Listing hunks

Show unstaged hunks (index vs worktree):

```bash
git hunk list
```

Show staged hunks (HEAD vs index):

```bash
git hunk list --staged
```

Filter to a specific file:

```bash
git hunk list --file src/main.zig
```

Machine-readable output for scripting:

```bash
git hunk list --porcelain
```

Output is tab-separated: `sha\tfile\tstart_line\tend_line\tsummary`

```
a3f7c21	src/main.zig	12	18	Add error handling
b82e0f4	src/main.zig	45	52	Replace old parser
```

Diff content is shown by default. Suppress with `--oneline`:

```bash
git hunk list --oneline                # compact one-line-per-hunk output
git hunk list --oneline --porcelain    # porcelain: compact one-line records
git hunk list --no-color               # disable color output
git hunk list --context 1              # finer-grained hunks
```

When there are untracked files, a hint is printed to stderr (human mode,
unstaged only):

```
hint: 3 untracked file(s) not shown -- use 'git add -N <file>' to include
```

Flags combine freely:

```bash
git hunk list --staged --file src/main.zig --porcelain
```

## Showing hunk content

Inspect the full diff content of specific hunks before staging:

```bash
git hunk show a3f7c21                         # one hunk
git hunk show a3f7 b82e                       # multiple hunks
git hunk show a3f7c21 --staged                # from staged hunks
git hunk show a3f7 --file src/main.zig        # restrict match to file
git hunk show a3f7c21 --porcelain             # machine-readable output
git hunk show a3f7:3-5                        # preview specific lines
```

Human mode prints the unified diff fragment (`---`/`+++` header + `@@` hunk):

```
--- a/src/main.zig
+++ b/src/main.zig
@@ -12,5 +12,6 @@ fn handleRequest()
 const result = try parse(input);
+if (result == null) return error.Invalid;
 return result;
```

Porcelain mode prints the metadata header line followed by raw diff lines,
with records separated by a blank line:

```
a3f7c21	src/main.zig	12	18	Add error handling
@@ -12,5 +12,6 @@ fn handleRequest()
 const result = try parse(input);
+if (result == null) return error.Invalid;
 return result;

```

## Staging hunks

Stage one or more hunks by content hash:

```bash
git hunk add a3f7c21                         # one hunk
git hunk add a3f7c21 b82e0f4                 # multiple hunks
git hunk add a3f7 b82e                       # prefix match (min 4 hex chars)
git hunk add a3f7c21 --file src/main.zig     # restrict match to file
git hunk add --all                           # stage all unstaged hunks
git hunk add --file src/main.zig             # stage all hunks in a file
git hunk add a3f7:3-5,8                      # stage specific lines from a hunk
```

On success, prints confirmation to stdout showing both the old and new hash:

```
staged a3f7c21 → 5e2b1a9  src/main.zig
1 hunk staged
hint: staged hashes differ from unstaged -- use 'git hunk list --staged' to see them
```

The `→` mapping shows the new staged hash so you can immediately reference it
with `list --staged` or `remove` without re-listing.

## Unstaging hunks

Unstage hunks from the index back to the working tree:

```bash
git hunk remove a3f7c21                      # one hunk
git hunk remove a3f7 b82e                    # multiple hunks
git hunk remove --all                        # unstage everything
git hunk remove --file src/main.zig          # unstage all hunks in a file
```

Use hashes from `git hunk list --staged`. Note that staged and unstaged hashes
for the same hunk differ (they use different stable line references). The `add`
command shows the mapping (`old → new`) to help track this.

## Hash stability

Hashes are deterministic and stable: staging or unstaging other hunks in the same
file does not change the remaining hashes. This enables sequential workflows
where you list once, then stage multiple hunks one at a time.

The hash is computed from:

- File path
- Stable line number (worktree side for unstaged, HEAD side for staged)
- Actual diff content (`+` and `-` lines only)

The "stable line" is the line number from the side that doesn't shift when hunks
are applied to the index. For unstaged hunks, the worktree is immutable, so the
`+` side line number is stable. For staged hunks, HEAD is immutable, so the `-`
side is stable.

## Scripting patterns

Stage all hunks in a file (built-in):

```bash
git hunk add --file src/main.zig
```

List hunk hashes only:

```bash
git hunk list --porcelain --oneline | cut -f1
```

Count hunks per file:

```bash
git hunk list --porcelain --oneline | cut -f2 | sort | uniq -c
```

Stage hunks matching a pattern in the summary:

```bash
git hunk list --porcelain --oneline | grep 'error' | cut -f1 | xargs git hunk add
```

## Prefix matching

SHA prefixes must be at least 4 hex characters. If a prefix matches multiple
hunks, the command fails with an ambiguity error. Use a longer prefix or `--file`
to disambiguate.

## Error handling

- Nonexistent hash: `error: no hunk matching '<sha>'` (exit 1)
- Too-short prefix (< 4 chars): `error: sha prefix too short` (exit 1)
- Ambiguous prefix: `error: ambiguous prefix '<sha>' -- matches multiple hunks` (exit 1)
- Patch doesn't apply (stale hashes): `error: patch did not apply cleanly -- re-run 'list' and try again` (exit 1)
- No unstaged changes: `no unstaged changes` (exit 1)
- No staged changes: `no staged changes` (exit 1)

All errors go to stderr. Data goes to stdout. Exit 0 on success, 1 on error.

## New and deleted files

New files must be tracked before hunks appear. Use `git add -N` to register
intent to add:

```bash
git add -N newfile.txt
git hunk list                  # now shows newfile.txt hunks
git hunk add <sha>             # stages the content
```

Deleted files appear automatically when a tracked file is removed from the
working tree:

```bash
rm oldfile.txt
git hunk list                  # shows deletion hunk
git hunk add <sha>             # stages the deletion
```

## References

- [Command reference](references/commands.md) -- all commands and flags
- [Output format](references/output.md) -- human and porcelain output details

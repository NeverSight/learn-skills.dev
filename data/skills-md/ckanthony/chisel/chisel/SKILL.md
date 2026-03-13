---
name: chisel
description: Use Chisel MCP filesystem tools efficiently — patch-based edits, minimal token reads, shell exec patterns, and anti-patterns to avoid.
---

# Chisel Agent Skill

You have access to a Chisel MCP server. Chisel exposes precision filesystem tools designed to minimise token cost and maximise safety. The cardinal rule: **never read a full file when you only need part of it, and never write a full file when you only need to change part of it.**

---

> ⚠️ **`shell_exec` has no shell interpreter.** Pipe (`|`), `&&`, `||`, `$()`, and all shell metacharacters are passed as **literals** to the process — they are never interpreted. Each `shell_exec` call runs exactly one command. Compose multi-step logic across separate calls.

---

## Tool Selection

```
Need to find something in a file or directory?
  └─ shell_exec (grep / find / sed / awk / stat / ls)

Need to edit an existing file?
  ├─ Small targeted change (< whole file)  → patch_apply
  │    └─ patch_apply fails twice on a small file?  → write_file (see below)
  └─ Overwrite entirely / file is tiny     → write_file

Need to add content to the end of a file?
  └─ append

Need to create a directory?
  └─ create_directory

Need to rename or relocate a file?
  └─ move_file
```

---

## Reading — Never Fetch What You Don't Need

Always start with the minimum slice required. Only escalate if the first call does not give enough context.

| Goal | Call |
|------|------|
| Find which lines contain a symbol | `shell_exec grep ["-n", "symbol", "/root/file"]` |
| Multi-file symbol search | `shell_exec grep ["-rn", "symbol", "/root"]` |
| List all headers in a Markdown file | `shell_exec grep ["-n", "^#", "/root/file.md"]` |
| Extract one section by header | `shell_exec sed ["-n", "/^## Section/,/^## /p", "/root/file.md"]` |
| Read lines 40–60 of a large file | `shell_exec sed ["-n", "40,60p", "/root/file"]` |
| Show every line with its number (small files) | `shell_exec cat ["-n", "/root/file"]` |
| Count occurrences | `shell_exec grep ["-c", "pattern", "/root/file"]` |
| Get file size / line count | `shell_exec wc ["-l", "/root/file"]` |
| List directory contents | `shell_exec ls ["-la", "/root/dir"]` |
| Find files by name | `shell_exec find ["/root", "-name", "*.rs"]` |
| Inspect file type / metadata | `shell_exec stat ["/root/file"]` |
| Tail a log | `shell_exec tail ["-n", "50", "/root/app.log"]` |

**Avoid calling `cat` on a file longer than ~50 lines.** Use `sed -n 'M,Np'` to window in, or `cat -n` on short files to get line numbers before writing a patch.

---

## Editing — Prefer Diffs Over Full Rewrites

### `patch_apply` — primary edit tool

Send only the changed lines. The file is written atomically; a hunk mismatch returns `PatchFailed` and leaves the original untouched.

```diff
--- a/src/main.rs
+++ b/src/main.rs
@@ -12,7 +12,7 @@
 fn main() {
-    let port = 3000;
+    let port = 8080;
     start_server(port);
 }
```

Rules for a valid patch:
- Context lines (no prefix) must match the file **exactly**, including whitespace.
- `@@ -L,N +L,N @@` line numbers must be **exact** for the current file state — both the start line and the count. A wrong line number in the header produces `PatchFailed` even if the content lines are correct. Always run `grep -n` or `cat -n` first to confirm the real line numbers before writing the hunk header.
- To create a new file use `--- /dev/null` as the source header; the file must not exist.
- You can include multiple `@@` hunks in a single call — all are applied atomically.

**When `PatchFailed` is returned:**
1. Re-read the exact lines with `grep -n` or `sed -n 'L-3,L+3p'`.
2. Regenerate the patch from the actual content — both context lines and hunk header.
3. **If `PatchFailed` happens twice on a file under ~100 lines:** stop debugging the hunk. Use `cat -n` to read the whole file, correct it in full, and use `write_file` instead.

### `write_file` — full overwrite

Use when:
- Creating a new file with substantial initial content.
- The change touches so much of the file that a diff would be larger than the file itself.
- The file is short (< ~30 lines) and a full rewrite is cleaner.
- **`patch_apply` has failed twice** on a short file — `write_file` is the safe recovery path.

### `append`

Use for log entries, appending lines to a config, or adding to an incrementally-built file. The file must already exist.

---

## In-place Transformation with `shell_exec sed -i`

For bulk replacements (rename a symbol, fix a repeated pattern), `sed` mutates the file directly — no diff needed.

> ⚠️ **`sed -i` has different signatures on macOS (BSD sed) vs Linux (GNU sed). Use exactly the forms below — do not improvise alternatives.**
>
> | Platform | Argument array |
> |---|---|
> | **Linux** (GNU sed) | `["-i", "s/Old/New/g", "/abs/path/file"]` |
> | **macOS** (BSD sed) | `["-i", "", "s/Old/New/g", "/abs/path/file"]` |
>
> On macOS the empty string `""` is the backup-suffix argument (meaning: no backup file). Chisel passes it through to BSD sed correctly as a separate argument — **do not omit it, do not replace it with `-i.bak`, and do not combine it with `-i` into a single arg like `"-i''"`.** Any deviation produces a cryptic BSD sed parse error (`command a expects \`…) and wastes turns.
>
> **If you are unsure which platform you're on**, use `shell_exec stat ["/proc/version"]` (Linux) or `shell_exec uname ["-s"]` to check. Alternatively, prefer `patch_apply` or `write_file` for single-file edits — they are platform-independent.

```
# Linux
shell_exec sed ["-i", "s/OldName/NewName/g", "/root/src/lib.rs"]

# macOS — the "" is mandatory and is passed correctly; do not second-guess this
shell_exec sed ["-i", "", "s/OldName/NewName/g", "/root/src/lib.rs"]
```

A successful in-place edit returns `exit_code: 0` with empty stdout. Non-zero exit or any stderr output means the expression or path is wrong — fix those, do not change the `-i` form.

---

## Workflow Patterns

### Locate → Read slice → Patch

The standard low-token edit loop:

1. `grep -n "target_symbol" /root/file` — find the line number.
2. `sed -n "L-5,L+10p" /root/file` — read a tight window around it.
3. Verify the `@@ -L,N +L,N @@` header matches exactly.
4. `patch_apply` — send the diff against that exact content.

**Short files only:** use `cat -n /root/file` in step 1 to see every line numbered at once — faster than a grep/sed pair when the file is < 50 lines.

### Explore unfamiliar codebase

1. `ls -la /root` — top-level layout.
2. `find /root -name "*.rs" -not -path "*/target/*"` — enumerate source files.
3. `grep -rn "struct MyStruct" /root/src` — locate the definition.
4. `sed -n "L,L+30p" /root/src/file.rs` — read the struct body.

> **Relative paths are auto-anchored to root.** `.` means the root itself, `subdir/file` means `root/subdir/file`.
> Absolute paths also work. Traversal (`../escape`) is always blocked.

### Create a new file with boilerplate

Use `write_file`. Once it exists, all subsequent edits go through `patch_apply`.

### Rename a symbol across many files

**Preferred — one call via `find -exec … {} +`:**

`find -exec cmd {} +` batches all matched paths into a single command invocation. No shell, no loop, one `shell_exec` call regardless of how many files match.

```
# macOS (BSD sed)
shell_exec find ["/root/src", "-name", "*.rs", "-exec", "sed", "-i", "", "s/OldName/NewName/g", "{}", "+"]

# Linux (GNU sed)
shell_exec find ["/root/src", "-name", "*.rs", "-exec", "sed", "-i", "s/OldName/NewName/g", "{}", "+"]
```

The `{}` placeholder and `+` terminator are passed literally to `find` — they are not shell metacharacters and require no escaping.

**Fallback — one call per file** (only if `find -exec` is unavailable or the pattern needs per-file logic):

1. `grep -rl "OldName" /root/src` — get the file list.
2. For each file:
   - **Linux:** `sed ["-i", "s/OldName/NewName/g", "/root/src/file.rs"]`
   - **macOS:** `sed ["-i", "", "s/OldName/NewName/g", "/root/src/file.rs"]`

### Scaffold a directory tree

```
create_directory /root/src/handlers
write_file /root/src/handlers/mod.rs "..."
write_file /root/src/handlers/auth.rs "..."
```

---

## Error Handling

| Error | Meaning | Fix |
|-------|---------|-----|
| `PatchFailed` | Context lines or hunk header don't match current file | Re-read with `grep -n` / `cat -n`, fix both header line numbers and context, regenerate patch. If it fails twice on a short file, use `write_file`. |
| `OutsideRoot` | Path escapes configured root | Use only paths under the root the server was started with |
| `NotFound` | File doesn't exist | Use `write_file` to create, or check path with `find` |
| `ReadOnly` | Server in read-only mode | Writes are disabled; only reads and `shell_exec` work |
| `CommandNotAllowed` | Command not in whitelist | Use only: `grep sed awk find cat head tail wc sort uniq cut tr diff file stat ls du` |

---

## What Not To Do

| Anti-pattern | Why | Do instead |
|---|---|---|
| `cat /root/large_file.rs` | Returns thousands of tokens you mostly won't use | `grep -n` to locate, `sed -n` to slice; `cat -n` only on files < 50 lines |
| `write_file` for a 3-line change in a 500-line file | Uploads entire file, risks hallucination corrupting unrelated lines | `patch_apply` with a targeted hunk |
| Shell pipelines in a single `shell_exec` (`cmd1 \| cmd2`) | **No shell interpreter** — `\|`, `&&`, `$()` are literals, not operators | Make separate `shell_exec` calls; compose in your logic |
| `find / -name "*.env"` | Path validated against root; will be blocked or return nothing useful | Always scope `find` to `/root/...` |
| Sending a patch with approximate context lines or wrong line numbers | `PatchFailed` — both context and `@@ -L,N @@` must be exact | Run `grep -n` or `cat -n` first, then diff against the real content |
| Running one `sed` call per file for a bulk replacement | N tool calls when 1 will do | `find ["/root", "-name", "*.ext", "-exec", "sed", "-i", "", "s/x/y/g", "{}", "+"]` — batches all files into one sed invocation |
| `sed -i "s/x/y/" file` on macOS without `""` | BSD sed requires an explicit suffix arg — omitting it silently misparses arguments | macOS: `["-i", "", "s/x/y/g", "/abs/file"]`; Linux: `["-i", "s/x/y/g", "/abs/file"]` |
| Using `-i.bak` or `-i''` instead of `["-i", ""]` | Chisel passes the empty string through correctly — no workaround needed | Stick to `["-i", ""]` two-arg form; do not invent alternatives |
| Retrying with a different `-i` form after a BSD sed parse error | The error is the expression or path, not the `-i ""` form | Fix the sed expression or path; keep `["-i", ""]` as-is |
| Continuing to retry `patch_apply` after two failures on a small file | Wastes turns; context drift compounds the problem | `cat -n` the file, use `write_file` to rewrite it correctly |

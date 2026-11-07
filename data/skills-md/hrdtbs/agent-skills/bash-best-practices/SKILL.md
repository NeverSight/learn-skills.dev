---
name: bash-best-practices
description: Write, review, and debug robust Bash scripts. Make sure to use this skill whenever the user needs help with shell scripts (bash, sh), asks to write a CLI tool in bash, debugs a failing shell script, or needs to ensure predictable behavior in CI/CD or production systems, even if they do not explicitly ask for best practices.
---

# Bash Best Practices

You are an expert Systems Administrator and Senior Backend Engineer. Your goal is to write defensive, strict bash scripts that behave predictably in production.

## Core Directives

### 1. Strict Mode
Start scripts with `set -euo pipefail`.
**Why:** This makes your script fail fast and loudly on errors (`-e`), undefined variables (`-u`), and hidden failures in pipelines (`-o pipefail`), preventing silent data corruption or unpredictable behavior.
*Note: Use `command || true` or `if ! command; then ...` if a command is expected to fail.*

### 2. Variable Quoting
Double-quote variables (e.g., `"${FILE_PATH}"`). Use `${VAR}` for clean delineation.
**Why:** Quoting prevents word splitting and globbing issues, especially when file paths or user inputs contain spaces or special characters. It ensures the variable is treated as a single literal string.

### 3. Conditions
Prefer Bash's `[[ ]]` over POSIX `[ ]`.
**Why:** `[[ ]]` is safer and provides more features. It handles empty strings gracefully without quoting tricks, supports regex matching (`=~`), and allows built-in logical operators (`&&`, `||`) directly inside the brackets.

### 4. Function Scoping
Use `local` for variables inside functions.
**Why:** By default, variables in Bash are global. Using `local` prevents accidental namespace pollution and weird side-effects when one function modifies a variable that another function is relying on.

### 5. Command Substitution
Prefer `$()` over backticks `` ` ``.
**Why:** `$()` is more visually distinct, easier to read, and crucially, it can be nested easily without needing complicated escaping rules.

## Script Structure and Conventions

1. **Use `function` keyword or `name()` but be consistent.** Usually `my_func() { ... }` is preferred for POSIX compatibility, but `function my_func() { ... }` is fine in Bash. Stick to one style.
2. **Use lower_snake_case for local variables and UPPER_SNAKE_CASE for environment/global constants.**
3. **Use `trap` for cleanup.** If your script creates temporary files or starts background processes, use `trap` to ensure they are cleaned up even if the script crashes or is interrupted.
   ```bash
   TMP_DIR=$(mktemp -d)
   trap 'rm -rf "${TMP_DIR}"' EXIT
   ```
4. **Provide helpful error messages.** Output error messages to `stderr` (`>&2`) instead of `stdout`.
   ```bash
   echo "Error: Directory not found" >&2
   ```

## Anti-Patterns to Avoid

- **Parsing `ls` output.**
  - **Why:** File names can contain spaces, newlines, or control characters. Iterating over `ls` output will break on these filenames, causing unintended operations. Use globbing (`for file in *.txt`) or `find` instead.
- **Using `echo` to print variables that might contain hyphens.**
  - **Why:** If the variable starts with `-e` or `-n`, `echo` interprets it as a flag, swallowing the text and silently altering output. Use `printf '%s\n' "${var}"` instead.
- **Using `cat` to pipe a single file into a command (UUOC).**
  - **Why:** It spawns an unnecessary process, wastes resources, and obscures the input source. Use input redirection (`grep "error" < file.txt`) or pass the file as an argument.

## Examples

**Example 1: Safe Variable Quoting**
Input: `echo $USER_INPUT`
Output: `printf '%s\n' "${USER_INPUT}"`

**Example 2: Iterating Over Files**
Input:
```bash
for file in $(ls *.txt); do
  echo "Processing $file"
done
```
Output:
```bash
for file in *.txt; do
  # Avoid error if no match
  [[ -e "${file}" ]] || break
  printf 'Processing %s\n' "${file}"
done
```

**Example 3: Function Scoping**
Input:
```bash
my_func() {
  count=5
  echo "Count is $count"
}
```
Output:
```bash
my_func() {
  local count=5
  printf 'Count is %s\n' "${count}"
}
```

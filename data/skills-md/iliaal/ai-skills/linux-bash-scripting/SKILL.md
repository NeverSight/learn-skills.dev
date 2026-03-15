---
name: linux-bash-scripting
description: >-
  Defensive Bash scripting for Linux: safe foundations, argument parsing,
  production patterns, ShellCheck compliance. Use when writing bash scripts,
  shell scripts, cron jobs, or CLI tools in bash.
---

# Linux Bash Scripting

Target: GNU Bash 4.4+ on Linux. No macOS/BSD workarounds, no Windows paths, no POSIX-only restrictions.

## Script Foundation

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
shopt -s inherit_errexit

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

trap 'printf "Error at %s:%d\n" "${BASH_SOURCE[0]}" "$LINENO" >&2' ERR
trap 'rm -rf -- "${_tmpdir:-}"' EXIT
```

- `-E` propagates ERR traps into functions
- `inherit_errexit` propagates errexit into `$()`  command substitutions
- Always create temp dirs under the EXIT trap: `_tmpdir=$(mktemp -d)`
- Wrap body in `main() { ... }` with source guard: `[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"` — enables sourcing for testing

## Core Rules

- Quote every expansion: `"$var"`, `"$(cmd)"`, `"${array[@]}"`
- `local` for function variables, `local -r` for function constants, `readonly` for script constants
- `printf '%s\n'` over `echo` — predictable behavior, no flag interpretation
- `[[ ]]` for conditionals; `(( ))` for arithmetic; `$()` over backticks
- End options with `--`: `rm -rf -- "$path"`, `grep -- "$pattern" "$file"`
- Require env vars: `: "${VAR:?must be set}"`
- Never `eval` user input; build commands as arrays: `cmd=("grep" "--" "$pat" "$f"); "${cmd[@]}"`
- Separate `local` from assignment to preserve exit codes: `local val; val=$(cmd)`
- Debug tracing: `PS4='+${BASH_SOURCE[0]}:${LINENO}: '` with `bash -x` — shows file:line per command
- Named exit codes: `readonly EX_USAGE=64 EX_CONFIG=78` — no magic numbers in `exit`
- Pipeline diagnostics: `"${PIPESTATUS[@]}"` shows exit code of each pipe stage, not just last failure

## Safe Iteration

```bash
# NUL-delimited file processing
while IFS= read -r -d '' f; do
    process "$f"
done < <(find /path -type f -name '*.log' -print0)

# Array from command output
readarray -t lines < <(command)
readarray -d '' files < <(find . -print0)

# Glob with no-match guard
for f in *.txt; do [[ -e "$f" ]] || continue; process "$f"; done
```

## Argument Parsing

```bash
verbose=false; output=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose) verbose=true; shift ;;
        -o|--output)  output="$2"; shift 2 ;;
        -h|--help)    usage; exit 0 ;;
        --)           shift; break ;;
        -*)           printf 'Unknown: %s\n' "$1" >&2; exit 1 ;;
        *)            break ;;
    esac
done
```

## Production Patterns

**Dependency check:**
```bash
require() { command -v "$1" &>/dev/null || { printf 'Missing: %s\n' "$1" >&2; exit 1; }; }
require jq; require curl
```

**Dry-run wrapper:**
```bash
run() { if [[ "${DRY_RUN:-}" == "1" ]]; then printf '[dry] %s\n' "$*" >&2; else "$@"; fi; }
run cp "$src" "$dst"
```

**Atomic file write** — write to temp, rename into place:
```bash
atomic_write() { local tmp; tmp=$(mktemp); cat >"$tmp"; mv -- "$tmp" "$1"; }
generate_config | atomic_write /etc/app/config.yml
```

**Retry with backoff:**
```bash
retry() { local n=0 max=5 delay=1; until "$@"; do ((++n>=max)) && return 1; sleep $delay; ((delay*=2)); done; }
retry curl -fsSL "$url"
```

**Script locking** — prevent concurrent runs:
```bash
exec 9>/var/lock/"${0##*/}".lock
flock -n 9 || { printf 'Already running\n' >&2; exit 1; }
```

**Idempotent operations** — safe to rerun:
```bash
ensure_dir()  { [[ -d "$1" ]] || mkdir -p -- "$1"; }
ensure_link() { [[ -L "$2" ]] || ln -s -- "$1" "$2"; }
```

**Input validation:** `[[ "$1" =~ ^[1-9][0-9]*$ ]] || die "Invalid: $1"` — validate at script boundaries with `[[ =~ ]]`

- `umask 077` for scripts creating sensitive files
- Signal cleanup: `trap 'cleanup; exit 130' INT TERM` — preserves correct exit codes for callers

## Logging

```bash
log() { printf '[%s] [%s] %s\n' "$(date -Iseconds)" "$1" "${*:2}" >&2; }
info()  { log INFO "$@"; }
warn()  { log WARN "$@"; }
error() { log ERROR "$@"; }
die()   { error "$@"; exit 1; }
```

## Anti-Patterns

| Bad | Fix |
|-----|-----|
| `for f in $(ls)` | `for f in *; do` or `find -print0 \| while read` |
| `local x=$(cmd)` | `local x; x=$(cmd)` — preserves exit code |
| `echo "$data"` | `printf '%s\n' "$data"` |
| `cat file \| grep` | `grep pat file` |
| `kill -9 $pid` first | `kill "$pid"` first, `-9` as last resort |
| `cd dir; cmd` | `cd dir || exit 1` or subshell `(cd dir && cmd)` |

## Performance

- Parameter expansion over externals: `${path%/*}` not `dirname`, `${path##*/}` not `basename`, `${var//old/new}` not `sed`
- `(( ))` over `expr`; `[[ =~ ]]` over `echo | grep`
- Cache results: `val=$(cmd)` once, reuse `$val`
- `xargs -0 -P "$(nproc)"` for parallel work
- `declare -A map` for lookups instead of repeated grep

## Bash 4.4+ / 5.x

- `${var@Q}` shell-quoted, `${var@U}` uppercase, `${var@L}` lowercase
- `declare -n ref=varname` nameref for indirect access
- `wait -n` wait for any background job
- `$EPOCHSECONDS`, `$EPOCHREALTIME` — timestamps without forking `date`

## Linux-Specific

- `/proc/self/status`, `/proc/cpuinfo`, `/proc/meminfo` for system info
- `systemctl` for services; `journalctl -u svc` for logs
- GNU coreutils: `sed -i` (no `''`), `grep -P` (PCRE), `readlink -f`
- `timeout 30s cmd` to prevent hangs
- `flock` for script locking (see above)
- Package install: `apt-get install -y` / `dnf install -y` / `pacman -S --noconfirm`

## ShellCheck

Run `shellcheck --enable=all script.sh`. Key rules:
- **SC2155**: Separate declaration from assignment
- **SC2086**: Double-quote variables
- **SC2046**: Quote command substitutions
- **SC2164**: `cd dir || exit`
- **SC2327/SC2328**: Use `${BASH_REMATCH[n]}` not `$n` for regex captures

Pre-commit: `shellcheck *.sh && shfmt -i 2 -ci -d *.sh`

## Verify

Run `shellcheck --enable=all` and `shfmt -d` with zero warnings before declaring done. Test edge cases: empty input, missing files, spaces in paths.

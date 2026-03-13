---
name: writing-justfiles
description: "Create, edit, and maintain `justfile` automation for any codebase using the `just` command runner. Trigger whenever a request involves creating a new `justfile`, modifying/updating an existing `justfile`, adding or changing recipes, refactoring `justfile` structure, or automating project commands via `just`."
---

# Writing Justfiles

Guide for creating well-structured `justfile` recipes using best practices from the official Just manual and community conventions.

## Core Principles

- **just is a command runner, not a build system.** Keep recipes focused on running commands, not tracking file dependencies.
- **Start simple.** One justfile per project. Add complexity only when needed.
- **Document every recipe.** Comments above recipes appear in `just --list` output.
- **Quote all interpolated arguments** to prevent word splitting: `"{{arg}}"`.

## File Naming & Location

- Name the file `justfile` (lowercase preferred).
- Place it at the project root so `just` finds it from any subdirectory.

## Recipe Structure

### Basic Recipe

```just
# build the project
build:
    cargo build --release
```

### Recipe with Parameters

```just
# deploy to a target environment
deploy env='staging':
    ./scripts/deploy.sh "{{env}}"
```

- Use default values for optional parameters.
- Always quote `{{parameter}}` interpolations inside shell commands.
- Prefix parameters with `$` to export them as environment variables: `foo $bar:`.

### Multi-line Script Recipes

For non-trivial logic, use `[script]` so all lines run as a single script (sharing state), unlike normal recipes where each line is a separate shell invocation:

```just
# run database migration
[script('bash')]
migrate:
    set -euo pipefail
    echo "Running migrations..."
    ./manage.py migrate
```

- Always use `set -euo pipefail` at the top of bash script recipes for strict error handling.
- Prefer `[script]` over shebang (`#!/usr/bin/env bash`) recipes for better cross-platform compatibility.

### Dependencies

```just
# run all checks then deploy
release: test lint
    echo "Releasing..."

# run tests
test:
    cargo test

# run linter
lint:
    cargo clippy
```

- Use `&&` for dependencies that must all succeed before the recipe body runs: `release: test && lint`.
- Use `[parallel]` attribute to run dependencies concurrently when they are independent.

## Essential Attributes

Apply attributes above recipe definitions:

```just
# organize into groups for `just --list`
[group('build')]
build:
    cargo build

# hide helper recipes from listings
[private]
_setup:
    echo "internal setup"

# stay in the invocation directory
[no-cd]
commit file:
    git add "{{file}}"
    git commit

# require user confirmation before destructive actions
[confirm]
clean:
    rm -rf target/

# platform-specific recipes
[macos]
install-deps:
    brew install hugo

[linux]
install-deps:
    apt-get install hugo
```

- Prefix helper recipe names with `_` as a shorthand for `[private]`.
- Use `[no-cd]` for recipes that operate relative to the caller's working directory.
- Use `[confirm]` for destructive or irreversible operations.
- Use `[no-exit-message]` on helper recipes that may exit non-zero intentionally (e.g., user cancellation or precondition checks), to suppress just's default error output.

### Script Recipes (`[script]`)

The `[script]` attribute (v1.33.0+) runs a recipe as a single script, like shebang recipes but without needing a shebang line. It avoids cross-platform shebang issues (e.g., `cygpath` on Windows, inconsistent shebang splitting across OSes).

```just
# plain [script] uses the script-interpreter setting (default: sh -eu)
[script]
process:
    echo "step 1"
    echo "step 2"

# [script(COMMAND)] specifies the interpreter explicitly
[script('bash')]
complex:
    set -euo pipefail
    for f in *.txt; do
        echo "Processing $f"
    done

# use with python or other languages
[script('python3')]
analyze:
    import json
    data = json.loads('{"key": "value"}')
    print(data["key"])
```

- `[script]` (no argument) uses `set script-interpreter` (defaults to `sh -eu`), **not** `set shell`.
- `[script('command')]` specifies the interpreter directly.
- Prefer `[script]` over shebang recipes for better cross-platform compatibility.
- Configure the default script interpreter globally:

```just
set script-interpreter := ['bash', '-euo', 'pipefail']
```

## Settings

Declare settings at the top of the justfile:

```just
# load .env file automatically
set dotenv-load

# use bash instead of sh
set shell := ["bash", "-cu"]

# suppress command echoing by default
set quiet

# search parent directories for recipes not found locally
set fallback
```

## Variables & Expressions

```just
# assign variables
version := "1.0.0"
release_branch := "main"

# use built-in functions
home := env_var('HOME')
os_name := os()
arch_name := arch()
project_dir := justfile_directory()

# conditional expressions
profile := if env_var_or_default('CI', '') != '' { "release" } else { "debug" }
```

## Default Recipe

Make the first recipe a help/list command so bare `just` shows available recipes:

```just
# list available recipes
[default]
list:
    @just --list --list-heading $'just what?\n' --list-prefix '~> '
```

Always use this exact default recipe to provide a friendly listing.

## Organizing Large Justfiles

### Imports

Split into modules when the justfile grows large:

```just
import? '.just/build.just'
import? '.just/deploy.just'
import? '.just/test.just'
```

- Use `?` to make imports optional (won't error if file is missing).
- Keep a `.just/` directory for module files.

### Recommended Directory Structure

```
justfile                 # main orchestration
.just/
  build.just             # build commands
  deploy.just            # deployment recipes
  test.just              # test recipes
```

## Common Patterns

### Sanity-Check Dependencies

```just
[private, no-cd, no-exit-message, script('bash')]
_on-branch:
    if [[ $(git rev-parse --abbrev-ref HEAD) == "main" ]]; then
        echo "Error: must be on a feature branch" >&2
        exit 1
    fi

# create a pull request (requires feature branch)
pr: _on-branch
    gh pr create --fill
```

### Unified Project Interface

Provide a consistent set of recipe names across all projects:

```just
# start the dev server
run:
    <project-specific command>

# run the test suite
test:
    <project-specific command>

# format source code
format:
    <project-specific command>

# run linters and type checks
check:
    <project-specific command>
```

### Timestamped Git Branches

```just
[no-cd]
@utcdate:
    TZ=UTC date +"%Y-%m-%d"

# create a dated feature branch
[script('bash')]
branch name:
    NOW=$(just utcdate)
    git checkout -b "$USER/$NOW-{{name}}"
```

### Suppress Command Echo

Prefix a line with `@` to hide the command itself (only show output):

```just
version:
    @echo "v1.2.3"
```

## Formatting & Style

- Use 4-space indentation (required by `just --fmt`).
- Run `just --fmt --unstable` to auto-format the justfile.
- **After editing a justfile, always run `just --fmt --check --unstable` to verify formatting.** If it reports errors, run `just --fmt --unstable` to fix them automatically.
- Keep recipes short; extract complex logic into shell scripts.
- Add a blank line between recipes for readability.

## Debugging & Testing

- `just --dry-run <recipe>` — preview commands without executing.
- `just --verbose <recipe>` — print each command before running it.
- `just --list` — show all available recipes with descriptions.
- `just --evaluate` — print all variable values.

## Gotchas

- **Working directory**: by default, recipes run in the justfile's directory, not the caller's. Use `[no-cd]` to change this.
- **Each line is a separate shell** (unless using `[script]` recipes). Variables set on one line are not available on the next — use `[script]` to share state across lines.
- **Use `{{variable}}`** for just interpolation, not `$variable` (which is shell expansion).
- **Use normal shell expansion** in recipe lines: `$(...)` and `$var`. Avoid over-escaping with `$$(...)`/`$$var` unless you explicitly need a literal `$` in the final command.
- **Always quote arguments**: `"{{arg}}"` prevents word-splitting on spaces or special characters.
- **Avoid dense one-liners** with nested substitutions; assign intermediate shell variables for readability and fewer quoting bugs.
- **Indentation must be consistent** within a recipe — don't mix tabs and spaces.

## References

- [Just Programmer's Manual](https://just.systems/man/en/)
- [GitHub Repository](https://github.com/casey/just)
- [Attributes Reference](https://just.systems/man/en/attributes.html)

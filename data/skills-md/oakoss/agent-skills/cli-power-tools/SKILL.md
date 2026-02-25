---
name: cli-power-tools
description: 'Performs advanced CLI operations, structured data transformation, and Unix forensics with modern Rust-powered tools. Use when searching codebases with ripgrep, transforming JSON or YAML with jq, refactoring across files with sed and fd, debugging APIs with httpie, or navigating directories with zoxide.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://github.com/BurntSushi/ripgrep'
user-invocable: false
---

# Utility Pro

## Overview

Masters the command-line environment by turning raw text and unstructured data into actionable insights. Combines Rust-powered search tools (ripgrep, fd, bat), structured data shells (Nushell), JSON manipulation (jq/yq), and modern HTTP clients (xh) for high-performance CLI workflows.

**Core philosophy:** Replace legacy text-parsing pipelines (grep/awk/sed chains) with purpose-built tools that understand structure. ripgrep understands gitignore rules, fd understands file types, jq understands JSON, and Nushell understands tables.

**When to use:** Codebase-wide search and analysis, multi-file refactoring, JSON/YAML transformation pipelines, API debugging, directory navigation, log parsing, disk usage auditing, dependency tracing.

**When NOT to use:** GUI-based tasks, complex application logic (write a script instead), tasks requiring interactive prompts.

## Quick Reference

| Pattern                  | Tool / Command                                                           | Key Points                                         |
| ------------------------ | ------------------------------------------------------------------------ | -------------------------------------------------- |
| Text search              | `rg "pattern" -g "*.tsx"`                                                | 10-100x faster than grep, respects `.gitignore`    |
| File search              | `fd -e pdf` or `fd "pattern"`                                            | Fast alternative to `find` with smart defaults     |
| Syntax-highlighted read  | `bat file.ts`                                                            | Cat with syntax highlighting and git integration   |
| Directory jump           | `z project-name`                                                         | Remembers frequently visited directories           |
| Fuzzy search             | `fzf` or `CTRL-T` / `CTRL-R`                                             | Interactive selection for files and history        |
| Tree view                | `eza --tree --level=2`                                                   | Metadata-rich ls replacement with tree support     |
| JSON query               | `jq '.items[] \| select(.active)'`                                       | Full functional programming for JSON               |
| YAML query               | `yq '.config.database' file.yml`                                         | jq-like syntax for YAML files                      |
| HTTP request             | `xh POST api.example.com/v1/data key=value`                              | Colorized, user-friendly HTTP client               |
| Multi-file refactor      | `fd -e tsx -x sed -i 's/Old/New/g' {}`                                   | Find files then execute transforms                 |
| Structured shell         | `ls \| where size > 1mb \| sort-by size`                                 | Nushell tables instead of text parsing             |
| Log parsing              | `rg "ERROR" --json \| jq 'select(.type == "match") \| .data.lines.text'` | Combine ripgrep JSON output with jq filters        |
| File preview with search | `fzf --preview 'bat --color=always {}'`                                  | Browse files with syntax-highlighted preview       |
| Find recently changed    | `fd --changed-within 1h`                                                 | Find files modified within a time window           |
| Export count by file     | `rg -c "pattern" -g "*.ts" \| sort -t: -k2 -rn`                          | Count matches per file, sorted by frequency        |
| JSON format conversion   | `yq -o json config.yml`                                                  | Convert between YAML, JSON, CSV, and other formats |
| Advanced regex search    | `rg -P "(?<=function\s)\w+" --only-matching`                             | PCRE2 for lookahead/lookbehind patterns            |
| Git-aware file listing   | `eza -la --git --icons`                                                  | Show file metadata with inline git status          |

## Tool Overview

| Category         | Modern Tool    | Replaces              | Key Advantage                            |
| ---------------- | -------------- | --------------------- | ---------------------------------------- |
| Text search      | ripgrep (`rg`) | grep, ag, git grep    | Speed, `.gitignore` awareness, Unicode   |
| File search      | fd             | find                  | Smart defaults, regex, parallelism       |
| File viewer      | bat            | cat, less             | Syntax highlighting, git diff markers    |
| Directory jump   | zoxide (`z`)   | cd, autojump          | Frecency-based ranking, fzf fallback     |
| Fuzzy finder     | fzf            | manual piping         | Universal selector for any list          |
| File listing     | eza            | ls, tree              | Tree view, git status, icons             |
| JSON processing  | jq             | awk, python oneliners | Typed, functional JSON transforms        |
| YAML processing  | yq             | sed on YAML           | jq-compatible syntax for YAML            |
| HTTP client      | xh             | curl, httpie          | HTTPie syntax, Rust speed, single binary |
| Structured shell | Nushell        | bash + awk/sed        | Typed tables, native format conversion   |

## Common Mistakes

| Mistake                                               | Correct Pattern                                                                    |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Using `grep` instead of `ripgrep` for codebase search | Use `rg` which is 10-100x faster and respects `.gitignore` by default              |
| Piping `ls` output into `grep` for file filtering     | Use `fd` for file discovery, or `eza -D` / `eza --ignore-glob` for listing         |
| Writing complex `awk` scripts for structured data     | Use Nushell or `jq` which natively understand JSON, CSV, and YAML                  |
| Running `rm -rf` in scripts without a dry-run step    | Always add a verification or dry-run step before destructive operations            |
| Using capturing groups in regex when not needed       | Prefer non-capturing groups `(?:...)` for better performance in large-scale scans  |
| Searching `node_modules` or `.git` directories        | Use `rg` which skips these by default, or configure exclusions explicitly          |
| Forgetting `select(.type == "match")` on `rg --json`  | ripgrep JSON emits begin, match, context, end, and summary message types           |
| Using `curl` with verbose flag syntax                 | Use `xh` which provides colorized output and HTTPie-compatible request-item syntax |
| Parsing text output between tools with `cut`/`tr`     | Use Nushell pipelines that preserve structured data through every stage            |
| Anchoring regex with `.*` at the start                | Anchor with `^` when possible; unanchored `.*` causes expensive backtracking       |

## Installation

All tools are available via common package managers. Most are single statically linked binaries.

| Tool    | macOS (Homebrew)       | Linux (apt/cargo)                                |
| ------- | ---------------------- | ------------------------------------------------ |
| ripgrep | `brew install ripgrep` | `apt install ripgrep` or `cargo install ripgrep` |
| fd      | `brew install fd`      | `apt install fd-find` or `cargo install fd-find` |
| bat     | `brew install bat`     | `apt install bat` or `cargo install bat`         |
| zoxide  | `brew install zoxide`  | `cargo install zoxide`                           |
| fzf     | `brew install fzf`     | `apt install fzf`                                |
| eza     | `brew install eza`     | `cargo install eza`                              |
| jq      | `brew install jq`      | `apt install jq`                                 |
| yq      | `brew install yq`      | `snap install yq` or `go install`                |
| xh      | `brew install xh`      | `cargo install xh`                               |
| Nushell | `brew install nushell` | `cargo install nu`                               |

Shell integration (add to shell config after installing):

| Tool   | Shell Integration Required                                |
| ------ | --------------------------------------------------------- |
| zoxide | `eval "$(zoxide init zsh)"` (or bash/fish equivalent)     |
| fzf    | Source keybinding and completion scripts from fzf install |

## Delegation

- **Large-scale codebase search and analysis**: Use `Explore` agent to run ripgrep queries, trace dependencies, and map code patterns
- **Multi-file refactoring workflows**: Use `Task` agent to coordinate fd, sed, and verification steps across an entire project
- **Pipeline architecture for data transformation**: Use `Plan` agent to design structured pipelines combining jq, Nushell, and API tools

## References

- [Modern Unix Toolbox](references/modern-unix-toolbox.md) -- ripgrep, fd, bat, zoxide, fzf, eza, terminal setup
- [Advanced Regex and jq](references/advanced-regex-and-jq.md) -- named captures, lookahead/lookbehind, jq filters, integrated pipelines
- [Nushell Structured Data](references/nushell-structured-data.md) -- table paradigm, API interaction, scripting, Unix interop

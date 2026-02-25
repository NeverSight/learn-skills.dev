---
name: shell-integration
description: |
  Shell scripting and terminal integration patterns for building tools that integrate with Zsh, Bash, and Fish. Covers completion systems (compdef/compadd, complete/compgen, fish complete), ZLE widgets, hooks (precmd/preexec/chpwd, PROMPT_COMMAND), readline, bindkey, parameter expansion, ZDOTDIR loading order, event systems, abbreviations, POSIX shell scripting, terminal control codes (ANSI/CSI escape sequences), tput, stty, signal handling, process management (job control, traps), and shell plugin distribution patterns.

  Use when building shell plugins, writing completion scripts, implementing terminal UI with escape sequences, managing dotfiles, creating installation scripts, handling signals and process management, or integrating native binaries with shell wrappers.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# Shell Integration

## Overview

Shell integration covers the APIs and patterns for building tools that extend or interact with Unix shells. This includes completion systems, prompt hooks, key bindings, terminal control, and plugin distribution across Zsh, Bash, and Fish.

**When to use:** Building CLI tool completions, shell plugins, prompt customizations, terminal UI, dotfile managers, installation scripts, or native binary wrappers.

**When NOT to use:** General-purpose scripting unrelated to shell extension (use POSIX scripting reference for standalone scripts), GUI applications, or web server development.

## Quick Reference

| Pattern             | Shell | Key Points                                                      |
| ------------------- | ----- | --------------------------------------------------------------- |
| Completion function | Zsh   | `compdef`, `compadd`, `zstyle` for matcher configuration        |
| Completion function | Bash  | `complete`, `compgen`, `COMP_WORDS`, `COMP_CWORD`, `COMPREPLY`  |
| Completion function | Fish  | `complete -c cmd -a args`, condition flags, subcommand patterns |
| ZLE widget          | Zsh   | `zle -N widget func`, `bindkey` to map keys                     |
| Prompt hook         | Zsh   | `precmd`, `preexec`, `chpwd` via `add-zsh-hook`                 |
| Prompt hook         | Bash  | `PROMPT_COMMAND` (string or array in Bash 5.1+)                 |
| Event handler       | Fish  | `--on-event`, `--on-variable`, `--on-signal`                    |
| Abbreviation        | Fish  | `abbr -a name expansion`, `--function` for dynamic              |
| Parameter expansion | Zsh   | `${(s.:.)var}`, `${var:=default}`, flags and modifiers          |
| Terminal control    | All   | ANSI/CSI escape sequences, `tput`, `stty`                       |
| Signal handling     | All   | `trap` builtin, cleanup patterns, `EXIT`/`INT`/`TERM`           |
| Process management  | All   | Job control (`&`, `wait`, `bg`, `fg`), subshells, coprocesses   |
| Plugin installation | All   | Sourcing strategies, version detection, `ZDOTDIR` loading order |

## Common Mistakes

| Mistake                                               | Correct Pattern                                                |
| ----------------------------------------------------- | -------------------------------------------------------------- |
| Using `echo -e` for escape sequences portably         | Use `printf` or `tput` for portability across shells and OSes  |
| Modifying `PROMPT_COMMAND` with `=` in Bash           | Append with `+=` to avoid overwriting other tools              |
| Defining Fish event handlers in lazy-loaded functions | Place event handlers in config.fish or source them explicitly  |
| Hardcoding terminal capabilities                      | Query via `tput` which respects `TERM` and terminfo            |
| Missing `emulate -L zsh` in Zsh functions             | Always set local options to avoid polluting caller environment |
| Using `$COMP_LINE` splitting instead of `COMP_WORDS`  | Use `COMP_WORDS[$COMP_CWORD]` for reliable word extraction     |
| Not quoting `$@` in wrapper scripts                   | Always use `"$@"` to preserve argument boundaries              |
| Assuming `/bin/sh` is Bash                            | Target POSIX sh for portable scripts, test with `dash`         |
| Using `function` keyword in POSIX scripts             | Use `name() { ... }` syntax for POSIX compatibility            |
| Ignoring `EXIT` trap for cleanup                      | Always set `trap cleanup EXIT` for temp files and state        |

## Delegation

- **Completion testing**: Use `Explore` agent to verify completions interactively
- **Script review**: Use `Task` agent for cross-shell compatibility audits
- **Code review**: Delegate to `code-reviewer` agent

> If the `rust` skill is available, delegate native binary compilation patterns to it. Shell wrappers often invoke Rust-compiled binaries for performance-critical operations.
> If the `cli-power-tools` skill is available, delegate modern CLI utility patterns to it. Many shell plugins wrap tools like `fd`, `ripgrep`, and `fzf`.

## References

- [Zsh integration: ZLE, completions, hooks, parameter expansion](references/zsh-integration.md)
- [Bash integration: readline, completions, PROMPT_COMMAND, shopt](references/bash-integration.md)
- [Fish integration: completions, events, abbreviations, functions](references/fish-integration.md)
- [Terminal control: ANSI/CSI sequences, tput, stty, capabilities](references/terminal-control.md)
- [POSIX scripting: portable patterns, signal handling, process management](references/posix-scripting.md)
- [Plugin distribution: installation scripts, dotfile management, version detection](references/plugin-distribution.md)

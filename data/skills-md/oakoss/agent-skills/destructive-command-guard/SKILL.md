---
name: destructive-command-guard
description: 'Blocks dangerous commands before execution via a Rust-based Claude Code hook. Use when configuring agent safety guards, setting up destructive command blocking, or auditing CLI protection rules. Use for git reset protection, rm -rf interception, force-push blocking, pack-based command filtering, and PreToolUse hook safety.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
user-invocable: false
---

# Destructive Command Guard

A high-performance Claude Code hook that intercepts and blocks destructive commands before they execute. Written in Rust with SIMD-accelerated filtering via the `memchr` crate and Aho-Corasick multi-pattern matching for sub-millisecond latency. Assumes agents are well-intentioned but fallible.

## Overview

DCG uses a whitelist-first architecture: safe patterns are checked before destructive patterns, and unrecognized commands are allowed by default (fail-safe). This ensures legitimate workflows are never broken while known dangerous patterns are always blocked. DCG runs as a `PreToolUse` hook in Claude Code, receiving JSON on stdin for each Bash tool invocation and returning exit code `0` (allow) or `2` (block). It only inspects direct Bash tool invocations, not contents of shell scripts.

The processing pipeline has four stages: JSON parsing, command normalization (strips absolute paths like `/usr/bin/git`), SIMD quick-reject filter (skips regex for commands without `git` or `rm`), and pattern matching. The `memchr` crate provides hardware-accelerated substring search (SSE2/AVX2 on x86_64, NEON on ARM), while Aho-Corasick handles multi-pattern matching in O(n) time regardless of pattern count.

DCG supports 49+ modular security packs organized by category (git, filesystem, databases, containers, Kubernetes, cloud providers, infrastructure tools). Core packs (`core.git`, `core.filesystem`) are always enabled; additional packs are configured via `~/.config/dcg/config.toml` or the `DCG_PACKS` environment variable. The `dcg scan` subcommand can also audit files for destructive command contexts, suitable for CI integration.

DCG is not published on crates.io; it is installed from GitHub via `cargo +nightly install` or prebuilt binaries for Linux, macOS, and Windows WSL. The threat model assumes agents are well-intentioned but fallible; DCG catches honest mistakes, not adversarial attacks.

## Quick Reference

| Category         | Blocked Commands                                                                   |
| ---------------- | ---------------------------------------------------------------------------------- |
| Uncommitted work | `git reset --hard`, `git checkout -- <file>`, `git restore <file>`, `git clean -f` |
| Remote history   | `git push --force` / `-f`, `git branch -D`                                         |
| Stashed work     | `git stash drop`, `git stash clear`                                                |
| Filesystem       | `rm -rf` (outside `/tmp`, `/var/tmp`, `$TMPDIR`)                                   |

| Category      | Allowed Commands                                                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Safe git      | `git status`, `git log`, `git diff`, `git add`, `git commit`, `git push`, `git pull`, `git fetch`, `git branch -d`, `git stash`, `git stash pop` |
| Safe patterns | `git checkout -b`, `git restore --staged`, `git clean -n`, `git push --force-with-lease`                                                         |
| Temp dirs     | `rm -rf /tmp/*`, `rm -rf $TMPDIR/*`                                                                                                              |

| Setting              | Value                                |
| -------------------- | ------------------------------------ |
| Exit code (safe)     | `0`                                  |
| Exit code (blocked)  | `2`                                  |
| Default behavior     | Allow (fail-safe)                    |
| Pattern priority     | Safe checked first, then destructive |
| Safe patterns        | 34                                   |
| Destructive patterns | 16                                   |

| Pack Category  | Examples                                                        |
| -------------- | --------------------------------------------------------------- |
| Core (default) | `core.git`, `core.filesystem`                                   |
| Database       | `database.postgresql`, `database.mysql`, `database.mongodb`     |
| Containers     | `containers.docker`, `containers.compose`, `containers.podman`  |
| Kubernetes     | `kubernetes.kubectl`, `kubernetes.helm`, `kubernetes.kustomize` |
| Cloud          | `cloud.aws`, `cloud.gcp`, `cloud.azure`                         |
| Infrastructure | `infrastructure.terraform`, `infrastructure.ansible`            |
| System         | `system.disk`, `system.permissions`, `system.services`          |
| Other          | `strict_git`, `package_managers`                                |

| Environment Variable | Purpose                            |
| -------------------- | ---------------------------------- |
| `DCG_PACKS`          | Enable packs (comma-separated)     |
| `DCG_DISABLE`        | Disable specific packs             |
| `DCG_VERBOSE`        | Verbose output                     |
| `DCG_BYPASS`         | Bypass DCG entirely (escape hatch) |
| `DCG_COLOR`          | Color mode (auto, always, never)   |

| Installation Method | Command                                                                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Quick install       | `curl -fsSL ".../install.sh" \| bash -s -- --easy-mode`                                                                 |
| From source         | `cargo +nightly install --git https://github.com/Dicklesworthstone/destructive_command_guard destructive_command_guard` |
| Prebuilt binaries   | Linux x86_64, Linux ARM64, macOS Intel, macOS Apple Silicon, Windows WSL                                                |

| Processing Stage  | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| JSON parsing      | Reads `PreToolUse` hook input, allows non-Bash tools          |
| Normalization     | Strips absolute paths (`/usr/bin/git` becomes `git`)          |
| SIMD quick-reject | `memchr` substring search skips regex for irrelevant commands |
| Pattern matching  | Safe patterns first, then destructive, default allow          |

## Common Mistakes

| Mistake                                                          | Correct Pattern                                                               |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Forgetting to restart Claude Code after adding the hook          | Always restart Claude Code after modifying `~/.claude/settings.json`          |
| Using `DCG_BYPASS=1` permanently in shell profile                | Only set bypass temporarily for a single command, then remove it              |
| Assuming DCG inspects commands inside scripts                    | DCG only inspects direct Bash tool invocations, not contents of `./deploy.sh` |
| Blocking `git branch -d` (lowercase) thinking it is destructive  | Lowercase `-d` is safe (merge-checked); only uppercase `-D` force-deletes     |
| Not enabling database or cloud packs for production environments | Configure relevant packs in `~/.config/dcg/config.toml` for your stack        |
| Expecting DCG to stop malicious actors                           | DCG catches honest mistakes; determined users can always bypass the hook      |
| Running `cargo install` without nightly toolchain                | DCG requires Rust nightly (edition 2024); use `cargo +nightly install`        |

## Delegation

- **Audit which destructive commands an agent session has attempted**: Use `Explore` agent
- **Set up DCG with custom packs for a new project environment**: Use `Task` agent
- **Plan a layered safety architecture combining DCG with other guardrails**: Use `Plan` agent

## References

- [Command detection and processing pipeline](references/command-detection.md)
- [Pack configuration and environment variables](references/pack-configuration.md)
- [Installation and Claude Code setup](references/installation.md)
- [Safety patterns and edge cases](references/safety-patterns.md)
- [Troubleshooting and FAQ](references/troubleshooting.md)

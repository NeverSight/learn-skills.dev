---
name: tools
description: |
    Use when working with fundamental CLI tools and utilities that are essential for software development across all languages and platforms. Covers shells, version control, system package managers, containers, remote access, HTTP clients, data processing, and build runners.
    USE FOR: CLI tools, developer tooling, shell scripting, version control, system package managers, containers, remote access, build automation, text processing, choosing cross-platform dev tools
    DO NOT USE FOR: language-specific package managers (use language-specific skills like npm/pip/cargo), IDE configuration, language-specific build tools (use language-specific skills)
license: MIT
metadata:
  displayName: "Developer Tools"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Git Documentation"
    url: "https://git-scm.com/doc"
  - title: "Docker Documentation"
    url: "https://docs.docker.com"
---

# Developer Tools

## Overview

These are the tools every developer needs regardless of language or framework — the bedrock of the development environment. Whether you are writing Python, C#, Rust, or JavaScript, you will reach for these tools daily: a shell to run commands, Git to track changes, a package manager to install software, and containers to ship reproducible environments. Mastering this foundational layer makes everything built on top of it faster and more reliable.

## Tool Landscape

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer Tools                          │
├─────────────────────────────────────────────────────────────┤
│  Shells:            PowerShell Core, Bash/Zsh               │
│  Version Control:   Git                                     │
│  Package Managers:  choco, winget, brew, apt, snap          │
│  Containers:        Docker, Podman                          │
│  Remote Access:     SSH, SCP                                │
│  HTTP Clients:      curl, wget, HTTPie                      │
│  Data Processing:   jq, yq                                  │
│  Pattern Matching:  Regular Expressions                     │
│  Build Runners:     Make, Just, Task                        │
└─────────────────────────────────────────────────────────────┘
```

## Choosing the Right Sub-Skill

| Need | Look In |
|------|---------|
| Writing cross-platform shell scripts | `powershell-core` |
| Writing Unix shell scripts, Bash/Zsh automation | `bash` |
| Version control, branching, merging, rebasing | `git` |
| Installing system-level software and managing OS packages | `package-managers` |
| Containerizing applications, Docker Compose, Podman | `docker` |
| Remote server access, key management, tunneling | `ssh` |
| Making HTTP requests from the command line | `curl` |
| Parsing and transforming JSON or YAML data | `jq` |
| Text pattern matching, search-and-replace with regex | `regex` |
| Running build tasks, command orchestration | `make` |

## Platform Availability

| Tool | Windows | macOS | Linux |
|------|---------|-------|-------|
| PowerShell Core (pwsh) | Yes (built-in on Win11, installable) | Yes (brew) | Yes (apt/dnf) |
| Bash | Yes (WSL, Git Bash) | Yes (built-in) | Yes (built-in) |
| Zsh | Yes (WSL) | Yes (default shell) | Yes (installable) |
| Git | Yes (winget/choco) | Yes (Xcode CLT / brew) | Yes (apt/dnf) |
| choco | Yes | No | No |
| winget | Yes (built-in on Win10+) | No | No |
| brew | No | Yes | Yes |
| apt | No | No | Yes (Debian/Ubuntu) |
| snap | No | No | Yes |
| Docker | Yes (Docker Desktop / WSL2) | Yes (Docker Desktop) | Yes (native) |
| Podman | Yes | Yes (brew) | Yes (native) |
| SSH / SCP | Yes (built-in on Win10+) | Yes (built-in) | Yes (built-in) |
| curl | Yes (built-in on Win10+) | Yes (built-in) | Yes (built-in) |
| wget | Yes (choco/winget) | Yes (brew) | Yes (built-in) |
| HTTPie | Yes (pip/choco) | Yes (brew) | Yes (apt/pip) |
| jq | Yes (choco/winget) | Yes (brew) | Yes (apt) |
| yq | Yes (choco/winget) | Yes (brew) | Yes (snap/apt) |
| Make | Yes (choco, WSL) | Yes (Xcode CLT) | Yes (built-in) |
| Just | Yes (cargo/choco) | Yes (brew/cargo) | Yes (cargo/apt) |
| Task (go-task) | Yes (choco/winget) | Yes (brew) | Yes (snap/apt) |

## Best Practices

- **Automate your setup with dotfiles.** Keep your shell configuration, Git config, and tool settings in a version-controlled dotfiles repository so you can bootstrap any new machine in minutes.
- **Use cross-platform tools where possible.** Prefer tools like PowerShell Core, Docker, and Git that work identically on Windows, macOS, and Linux to reduce friction when switching environments or collaborating across teams.
- **Learn at least one shell deeply.** Surface-level knowledge of many shells is less valuable than deep expertise in one. Pick PowerShell or Bash and master its scripting, pipeline, and debugging capabilities.
- **Version control everything.** Not just source code — configuration files, infrastructure definitions, documentation, and scripts all belong in Git.
- **Use containers for reproducible environments.** Docker and Podman eliminate "works on my machine" problems by packaging applications with their exact dependencies.
- **Prefer declarative build runners.** Tools like Make, Just, and Task let you define project commands (build, test, lint, deploy) in a single file, making onboarding and CI/CD consistent.

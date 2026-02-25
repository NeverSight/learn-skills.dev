---
name: extension-guide
description: Guide users through creating Sindri extensions. Use when creating new extensions, understanding extension.yaml structure, or learning about the extension system. Asks user to choose V2 or V3 before delegating to specialized version-specific skills.
---

# Sindri Extension Guide

Sindri supports extensions for **both V2 (Bash/Docker)** and **V3 (Rust CLI)** platforms. Before proceeding with extension creation, you need to choose which platform you're targeting.

## Version Differences at a Glance

| Aspect | V2 | V3 |
|--------|-----|-----|
| **Implementation** | Bash (~52K lines) | Rust (~11.2K lines) |
| **Extension Directory** | `v2/docker/lib/extensions/` | `v3/extensions/` |
| **Schema Location** | `v2/docker/lib/schemas/extension.schema.json` | `v3/schemas/extension.schema.json` |
| **CLI** | `./v2/cli/extension-manager` | `sindri extension` |
| **Install Methods** | 6 (mise, apt, binary, npm, script, hybrid) | 7 (adds npm-global) |
| **Categories** | 11 | 12 (different set) |
| **VisionFlow** | Supported | Not available |

### V2 Categories
`base`, `agile`, `language`, `dev-tools`, `infrastructure`, `ai`, `database`, `monitoring`, `mobile`, `desktop`, `utilities`

### V3 Categories
`ai-agents`, `ai-dev`, `claude`, `cloud`, `desktop`, `devops`, `documentation`, `languages`, `mcp`, `productivity`, `research`, `testing`

## When to Choose V2

- **VisionFlow workflows** - vf-* extensions only available in V2
- **Proven stability** - Battle-tested codebase
- **Docker-first** - Deep Docker/container integration
- **Team familiar with Bash** - V2 scripts are all Bash

## When to Choose V3

- **New projects** - Modern architecture
- **Windows support** - Native Windows binaries
- **Performance** - 10-50x faster CLI operations
- **Advanced collision handling** - Smart merge strategies for cloned projects
- **Project-context merging** - CLAUDE.md file management

## Required Action: Choose Version

**Before creating an extension, use AskUserQuestion to determine:**

1. Which Sindri version (V2 or V3)?
2. Basic extension details (name, category, purpose)

Then delegate to the appropriate specialist skill:
- **V2**: Use `/extension-guide-v2` skill
- **V3**: Use `/extension-guide-v3` skill

## Slash Commands

| Command | Description |
|---------|-------------|
| `/extension-guide` | This router (choose version first) |
| `/extension-guide-v2` | V2-specific extension guide |
| `/extension-guide-v3` | V3-specific extension guide |

## Quick Decision Tree

```
Creating an extension?
    │
    ├── Need VisionFlow (vf-*)?
    │   └── V2 only
    │
    ├── New AI/Claude tool?
    │   └── V3 recommended (better categories, collision handling)
    │
    ├── Language runtime (Node, Python, etc.)?
    │   └── Either works (V3 preferred for new projects)
    │
    └── Windows support needed?
        └── V3 only
```

## Shared Features (Both V2 and V3)

Both versions support the **capabilities system** for advanced extensions:

- **project-init** - Commands to initialize projects
- **auth** - API key and CLI authentication
- **hooks** - Lifecycle hooks (pre/post install, pre/post project-init)
- **mcp** - Model Context Protocol server registration
- **features** - Feature flags for advanced functionality

Most extensions don't need capabilities - they're for extensions that manage project setup (like Claude Flow, Agentic QE, Spec-Kit).

---

**Next Step:** Ask the user which version they need, then invoke the appropriate specialist skill.

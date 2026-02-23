---
name: readme-craft
description: Production-grade README.md patterns for any project type. Use when creating project documentation, writing README files, or improving existing docs. Covers hero sections, quick start examples, comparison tables, troubleshooting guides, and limitation transparency. Triggers on README, documentation, project setup, open source.
---

# README Craft

For general technical writing patterns, see `technical-writer` skill.

## Common Failures

- Installation first -> Lead with TL;DR and value prop
- Describes what it IS -> Describe what problem it SOLVES
- No examples -> One example per feature minimum
- Hidden limitations -> Dedicated limitations section
- Single install method -> Three+ pathways

## Golden Structure

### Tier 1: Hero Section

```markdown
<p align="center">
  <img src="logo.png" width="200" alt="Project Name">
</p>

<p align="center">
  <a href="..."><img src="https://img.shields.io/..." alt="CI"></a>
  <a href="..."><img src="https://img.shields.io/..." alt="Version"></a>
  <a href="..."><img src="https://img.shields.io/..." alt="License"></a>
</p>

<p align="center">
  <b>One-line description of what problem this solves</b>
</p>

```bash
curl -sSL https://example.com/install.sh | bash
```
```

Badge templates: see [references/badge-reference.md](references/badge-reference.md)

### Tier 2: TL;DR

```markdown
## TL;DR

**Problem:** [Specific pain point users face]

**Solution:** [How this tool solves it]

| Feature | Benefit |
|---------|---------|
| Feature 1 | Quantified benefit |
| Feature 2 | Quantified benefit |
| Feature 3 | Quantified benefit |
```

### Tier 3: Quick Start

```markdown
## Quick Start

# 1. Install
curl -sSL https://example.com/install.sh | bash

# 2. Initialize
mytool init

# 3. Run core workflow
mytool process input.txt --output result.json

# 4. Verify
mytool status
```

**Rule:** 5-10 commands demonstrating the core workflow.

### Tier 4: Reference Sections

- Philosophy/Design decisions
- Alternatives comparison
- Installation (multiple methods)
- Command reference
- Configuration options
- Architecture (for complex systems)

### Tier 5: Support Sections

- Troubleshooting
- Limitations
- FAQ
- Contributing
- License

## Section Templates

### Comparison Table

```markdown
## Why [Tool] Over Alternatives?

| Feature | [Tool] | Alternative A | Alternative B |
|---------|--------|---------------|---------------|
| Speed | 50ms | 200ms | 150ms |
| Memory | 10MB | 50MB | 30MB |
| Feature X | Yes | No | Partial |

**Choose [Tool] when:** [specific use case]
**Choose Alternative A when:** [specific use case]
```

### Installation (Multiple Methods)

```markdown
## Installation

### Quick Install (Recommended)

```bash
curl -sSL https://example.com/install.sh | bash
```

### Package Managers

```bash
# macOS
brew install mytool

# Linux
apt install mytool  # Debian/Ubuntu
dnf install mytool  # Fedora

# Windows
winget install mytool
```

### From Source

```bash
git clone https://github.com/user/mytool
cd mytool
make install
```
```

### Command Reference

```markdown
## Commands

### Global Flags

| Flag | Description |
|------|-------------|
| `-v, --verbose` | Increase output verbosity |
| `-q, --quiet` | Suppress non-error output |
| `--config PATH` | Use custom config file |

### `mytool init`

Initialize a new project.

```bash
mytool init                    # Interactive setup
mytool init --template minimal # Use template
mytool init --force            # Overwrite existing
```
```

### Troubleshooting

```markdown
## Troubleshooting

### Error: "Permission denied"

**Cause:** Installation script lacks execute permissions.

**Fix:**
```bash
chmod +x install.sh
./install.sh
```

### Error: "Command not found"

**Cause:** Binary not in PATH.

**Fix:**
```bash
export PATH="$HOME/.local/bin:$PATH"
# Add to ~/.bashrc or ~/.zshrc for persistence
```
```

### Limitations

```markdown
## Limitations

**Current constraints:**

| Limitation | Workaround | Planned Fix |
|------------|------------|-------------|
| Max 10MB files | Split large files | v2.0 |
| No Windows GUI | Use WSL | Under review |
| Single-threaded | Use multiple instances | v1.5 |

**Out of scope:**
- Feature X (use [Alternative] instead)
- Feature Y (not planned)
```

### FAQ

```markdown
## FAQ

<details>
<summary><b>Q: How does this compare to [Alternative]?</b></summary>

[Tool] focuses on [specific strength], while [Alternative] excels at [different use case].

</details>
```

## Pre-Publication Checklist

**Hero:**
- [ ] Logo/image present
- [ ] Badges current and working
- [ ] One-liner describes the problem solved
- [ ] Quick install command visible

**Content:**
- [ ] TL;DR within first scroll
- [ ] Every feature has an example
- [ ] Code blocks are copy-paste ready
- [ ] 3+ installation methods documented

**Trust:**
- [ ] Comparison with alternatives (honest)
- [ ] Limitations documented
- [ ] Top 5 errors in troubleshooting
- [ ] All links verified

## Anti-Patterns

| Do NOT | Do Instead |
|--------|------------|
| Start with installation | Start with value proposition |
| "This tool is a..." | "This tool solves..." |
| Screenshot-only demos | Executable code blocks |
| Claim without example | Example per feature |
| Hide limitations | Dedicated section |

## Reference Examples

Study these for excellent README patterns:
- **ripgrep** - Benchmark data, comparison matrices
- **bat** - Feature highlights, visual demos
- **starship** - Configuration presets, install matrix
- **jq** - Tutorial progression, manual linking

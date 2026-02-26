---
name: agent-converter
description: Converts agent definitions between Markdown (with YAML frontmatter) and TOML formats. Use when transforming agent configurations for different agent systems — MD format for rich tool restrictions, TOML format for Codex-style agents with sandbox modes.
---

# Agent Converter

## Objective

Convert agent definitions between two formats:

1. **Markdown format** (`.md` with YAML frontmatter) — Rich format with explicit tool restrictions
2. **TOML format** (`.toml`) — Simple format for Codex agents with sandbox modes

## Inputs

- **Source file**: Path to an agent `.md` file (or directory of agents)
- **Output format**: `toml` (default) or `md`
- **Output directory**: Where to write converted files (default: same as source)

## Commands

### Convert single agent MD → TOML

```bash
python3 skills/agent-converter/scripts/convert_agent.py <input.md> [--output <dir>]
```

### Convert all agents in directory

```bash
python3 skills/agent-converter/scripts/convert_agent.py --batch <input_dir> [--output <dir>]
```

### Convert TOML → MD

```bash
python3 skills/agent-converter/scripts/convert_agent.py <input.toml> --to-md [--output <dir>]
```

## Format Mapping

| MD Frontmatter | TOML Field |
|----------------|------------|
| `name` | (derived from filename) |
| `description` | Included in `developer_instructions` |
| `tools` | Mapped to `sandbox_mode` |
| Markdown body | `developer_instructions` |

### Tool → Sandbox Mode Mapping

| Tools | Sandbox Mode |
|-------|--------------|
| `Read`, `Grep`, `Glob` only | `read-only` |
| Any Write/Edit tools | `allow-edits` |
| No tools specified | `allow-edits` (default) |

### Sandbox Mode → Tool Mapping (reverse)

| Sandbox Mode | Tools |
|--------------|-------|
| `read-only` | `Read`, `Grep`, `Glob` |
| `allow-edits` | `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep` |

## Example Conversion

### Input: `explorer.md`

```markdown
---
name: explorer
description: >
  Read-only codebase explorer.
tools:
  - Read
  - Grep
  - Glob
---

# Explorer — Read-Only Codebase Navigator

You are a read-only explorer agent...
```

### Output: `explorer.toml`

```toml
sandbox_mode = "read-only"

developer_instructions = """
Role: Read-only codebase explorer.

Tools: Read, Grep, Glob

---

# Explorer — Read-Only Codebase Navigator

You are a read-only explorer agent...
"""
```

## Workflow

1. Parse source file (MD or TOML)
2. Extract metadata and instructions
3. Map format-specific fields
4. Write output in target format
5. Report conversion summary

## Error Handling

| Error | Resolution |
|-------|------------|
| Missing frontmatter | Treat as plain markdown, use defaults |
| Invalid TOML | Report parse error with line number |
| Unknown tools | Warn and include in output as-is |
| File exists | Prompt user or use `--force` to overwrite |

## References

- Format specification: `skills/agent-converter/references/format-spec.md`
- Example agents: `.agents/sub-agents/`
---
name: massgen-config-creator
description: Guide for creating properly structured YAML configuration files for MassGen. This skill should be used when agents need to create new configs for examples, case studies, testing, or demonstrating features.
license: MIT
---

# Config Creator

This skill provides guidance for creating new YAML configuration files that follow MassGen conventions and best practices.

## Purpose

The config-creator skill helps you create well-structured, validated configuration files for MassGen agents. It ensures consistency across the codebase and helps avoid common mistakes.

## When to Use This Skill

Use the config-creator skill when you need to:

- Create example configs demonstrating new features
- Write configs for case studies or releases
- Build reusable multi-agent workflow configs
- Test new backend or tool integrations
- Share configuration patterns with users

## Authoritative Documentation

**IMPORTANT:** The primary source of truth for config creation is:

**📖 `docs/source/development/writing_configs.rst`**

This file contains:
- Complete config creation workflow
- All current conventions and rules
- Property placement reference
- Validation checklist
- Common patterns and examples
- Up-to-date templates

**Always consult this document** for the latest configuration standards.

## Critical Rules (Quick Reference)

### 1. Never Invent Properties

**ALWAYS read 2-3 existing configs first** to understand current conventions:

```bash
# Find similar configs
ls massgen/configs/tools/{category}/

# Read examples
cat massgen/configs/basic/multi/two_agents_gemini.yaml
cat massgen/configs/tools/mcp/filesystem_claude.yaml
```

### 2. Property Placement Matters

- `cwd` → **BACKEND-level** (individual agent workspace)
- `context_paths` → **ORCHESTRATOR-level** (shared read-only files)
- `enable_web_search` → **BACKEND-level**
- `enable_planning_mode` → **ORCHESTRATOR.COORDINATION-level**

See `docs/source/development/writing_configs.rst` for complete property reference.

### 3. Key Conventions

✅ **DO:**
- Prefer cost-effective models (gpt-5-nano, gpt-5-mini, gemini-2.5-flash)
- Give all agents identical `system_message`
- Use separate workspaces per agent
- Include "What happens" comments explaining execution flow

❌ **DON'T:**
- Reference massgen v1 or legacy paths
- Invent new properties
- Suggest cleanup commands that delete logs

## Quick Start Workflow

### Step 1: Research Existing Configs

```bash
# Find configs in your category
ls massgen/configs/tools/{relevant_category}/

# Read 2-3 similar examples
cat massgen/configs/basic/multi/two_agents_gemini.yaml
```

### Step 2: Copy and Adapt

- Copy a similar config as your starting point
- Adapt values, never invent properties
- Follow the structure from existing configs

### Step 3: Test

```bash
massgen --config massgen/configs/tools/{category}/{your_config}.yaml "Test prompt"
```

### Step 4: Validate

Refer to the validation checklist in `docs/source/development/writing_configs.rst`

## File Naming and Location

**Naming Pattern:**
```
{agent_description}_{feature}.yaml
```

**Location Categories:**
- `massgen/configs/basic/` - Simple examples
- `massgen/configs/tools/filesystem/` - Filesystem operations
- `massgen/configs/tools/web-search/` - Web search
- `massgen/configs/tools/code-execution/` - Code execution
- `massgen/configs/tools/multimodal/` - Image, vision, audio
- `massgen/configs/tools/mcp/` - MCP integrations
- `massgen/configs/tools/planning/` - Planning mode

## Common Patterns (Quick Reference)

### Single Agent
```yaml
agent:  # Singular
  id: "my_agent"
  backend:
    type: "claude"
    model: "claude-sonnet-4"
```

### Multi-Agent
```yaml
agents:  # Plural
  - id: "agent_a"
    backend:
      type: "openai"
      model: "gpt-5-mini"
    system_message: "Shared task description"

  - id: "agent_b"
    backend:
      type: "gemini"
      model: "gemini-2.5-flash"
    system_message: "Shared task description"
```

### With Filesystem Access
```yaml
agents:
  - backend:
      cwd: "workspace1"  # Backend-level

orchestrator:
  context_paths:  # Orchestrator-level
    - path: "massgen/configs/resources/v0.0.29-example/source"
      permission: "read"
```

## Reference Files

**Primary Documentation:**
- **Config writing guide**: `docs/source/development/writing_configs.rst` ⭐ START HERE
- **YAML schema reference**: `docs/source/reference/yaml_schema.rst`
- **Example configs**: `massgen/configs/`

**Supporting Documentation:**
- **Supported models**: `docs/source/reference/supported_models.rst`
- **Backend configuration**: `docs/source/user_guide/backends.rst`
- **MCP integration**: `docs/source/user_guide/mcp_integration.rst`

## Tips for Agents

When creating configs programmatically:

1. **Always read the authoritative docs first**: `docs/source/development/writing_configs.rst`
2. **Read existing configs** to understand current patterns
3. **Copy structure** from similar configs, don't invent
4. **Test immediately** after creating
5. **When in doubt**, consult the full guide in `docs/source/development/writing_configs.rst`

This skill is a quick reference guide. For comprehensive, up-to-date information, always refer to the official documentation files listed above.

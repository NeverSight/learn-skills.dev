---
name: opencode-config
description: Configure OpenCode settings using JSON or Markdown files for project-specific or global preferences
license: MIT
compatibility: opencode
metadata:
  audience: developers using OpenCode who need to customize behavior per project or globally
  category: configuration
---

# OpenCode Configuration Skill

Understand and manage OpenCode configuration files in JSON or Markdown format, with proper precedence between global and project settings. This skill emphasizes research-driven verification because configuration details change over time.

## When to use me

- Setting up OpenCode for a new project with custom settings
- Creating team-wide configuration standards
- Understanding why certain settings aren't being applied (precedence issues)
- Migrating from deprecated configuration patterns to current best practices
- Verifying configuration details against official documentation

## What I do

- Explain OpenCode configuration formats (JSON/JSONC vs Markdown with YAML frontmatter)
- Clarify precedence order between global, project, and environment-based configs
- Provide examples for common configuration scenarios (models, permissions, tools, modes)
- Validate configuration files and check for common issues using included scripts
- Emphasize research-driven verification using search tools to stay current with changes
- Generate configuration files with proper schema references and variable substitution
- Include validation script (`scripts/validate-config.sh`) to check existing configuration files

## Examples

```bash
# Create a project-specific opencode.json with custom model
cat > opencode.json << EOF
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-haiku-4-5",
  "permission": {
    "edit": "ask",
    "bash": "ask"
  }
}
EOF

# Create a global mode using Markdown
mkdir -p ~/.config/opencode/modes/
cat > ~/.config/opencode/modes/review.md << 'EOF'
---
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
---

You are in code review mode. Focus on code quality, potential bugs, and security considerations without making direct changes.
EOF
```

## Output format

When analyzing configuration:

```yaml
config_source: ~/.config/opencode/opencode.json
config_type: global
format: json
precedence: 2/6
effective_settings:
  model: anthropic/claude-sonnet-4-5
  autoupdate: true
```

When creating configuration:

```json
{
  "status": "created",
  "file": ".opencode/modes/debug.md",
  "format": "markdown",
  "precedence": "project"
}
```

## Notes

- **Critical**: OpenCode configuration changes frequently. ALWAYS verify details using search tools (`searxng_searxng_web_search`, `searxng_web_url_read`) before providing specific implementation guidance.
- Configuration precedence (later overrides earlier):
  1. Remote config (`.well-known/opencode`)
  2. Global config (`~/.config/opencode/opencode.json`)
  3. Custom config (`OPENCODE_CONFIG` env var)
  4. Project config (`opencode.json` in project)
  5. `.opencode` directories (agents, commands, plugins)
  6. Inline config (`OPENCODE_CONFIG_CONTENT` env var)
- JSON and JSONC formats are supported for `opencode.json`; Markdown with YAML frontmatter is supported for modes, agents, commands, etc.
- The `$schema` field provides validation and autocomplete in editors.
- Use `{env:VAR}` and `{file:path}` for variable substitution in config files.
- Modes are now configured through the `agent` option (deprecated `mode` option).
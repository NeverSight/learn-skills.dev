---
name: create-plugin
description: Interactive initialization script that acts as a Plugin Architect. Generates a compliant '.claude-plugin' directory structure and `plugin.json` manifest using diagnostic questioning to ensure proper L4 patterns and Tool Connector schemas.
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---
# Agent Plugin Designer & Architect

You are not merely a file generator; you are an **Agent Plugin Architect**. Your job is to design a robust, strictly formatted Agent Plugin boundary that acts as a secure container for sub-agents and skills. Because we demand absolute determinism and compliance with Open Standards, you must deeply understand the design before scaffolding.

## Execution Steps:

### Phase 1: The Architect's Discovery Interview
Before proceeding, you MUST use your file reading tools to consume:
1. `plugins reference/agent-scaffolders/references/hitl-interaction-design.md`
2. `plugins reference/agent-scaffolders/references/pattern-decision-matrix.md`

Use progressive diagnostic questioning to understand the plugin design. Do not dump the theories on the user; just ask the questions:

- **Plugin Name**: Must be descriptive, kebab-case, lowercase.
- **Architecture Style**: Ask using a numbered option menu:
  ```
  Which architecture pattern should this plugin follow?
  1. Standalone — works entirely without external tools
  2. Supercharged — works standalone but enhanced with MCP integrations
  3. Integration-Dependent — requires MCP tools to function
  ```
- **External Tool Integrations**: If supercharged or integration-dependent, ask which tool categories are needed (e.g., `~~CRM`, `~~project tracker`, `~~source control`). These will seed the `CONNECTORS.md`.
- **Interaction Style**: Based on the `hitl-interaction-design.md` matrix, will skills in this plugin need guided discovery interviews with users, or are they primarily autonomous?
- **Pattern Routing**: Based on the `pattern-decision-matrix.md`, explicitly ask the diagnostic questions. If the user triggers an L4 pattern (like Escalation Taxonomy), alert them that you will ensure the plugin's scaffolded skills adhere to that standard.

### Phase 1.5: Recap & Confirm
**Do NOT immediately scaffold after the interview.**
You must pause and explicitly list out:
- The decided Plugin Name and Architecture Style
- The tool connectors (if any) you plan to write to CONNECTORS.md
- Any L4/L5 Patterns you noted during discovery (Crucially, note if the plugin requires Client-Side Compute Sandboxes or XSS Compliance Gates due to artifact generation).
Ask the user: "Does this look right? (yes / adjust)"

### 2. Scaffold the Plugin
Execute the deterministic `scaffold.py` script. **CRITICAL: Apply the Iteration Directory Isolation Pattern**.
If the user is testing a design iteration, DO NOT overwrite the main directory. Append `--iteration <N>` to save to `.history/iteration-<N>/`.
```bash
python3 ./scripts/scaffold.py --type plugin --name <requested-name> --path <destination-directory>
```
*(Note: Usually `<destination-directory>` will be inside the `plugins/` root).*

### Authoritative plugin.json Schema Reference

The `plugin.json` manifest lives at `.claude-plugin/plugin.json` inside the plugin root.
The scaffold script generates this automatically, but agents MUST verify it matches this schema.

**Minimal (only `name` is required):**
```json
{
  "name": "plugin-name"
}
```

**Full recommended manifest:**
```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name"
  }
}
```

**Optional fields:** `homepage`, `repository`, `license`, `keywords`

**Custom path overrides (supplements auto-discovery, does not replace it):**
```json
{
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Ignored by runtime (kept for human documentation only):**

The agent runtime auto-discovers skills from `skills/*/SKILL.md`, agents from `agents/`,
etc. These arrays are NOT read by Claude/Cowork, but are useful for humans browsing
the manifest to understand what a plugin contains:
```json
{
  "skills": ["skill-a", "skill-b"],
  "agents": [],
  "hooks": [],
  "commands": [],
  "dependencies": ["other-plugin-name"]
}
```

**Key rules:**
- `name` must be kebab-case (lowercase, hyphens, no spaces)
- `version` is semver - start at `0.1.0`
- File lives at `.claude-plugin/plugin.json` (hyphen, not underscore)
- `author` is an object with a `name` field, not a string

### 3. Generate CONNECTORS.md (If Supercharged)
If the user indicated MCP integrations, create a `CONNECTORS.md` file at the plugin root using the `~~category` abstraction pattern:

```markdown
# Connectors

| Category | Examples | Used By |
|----------|----------|---------|
| ~~category-name | Tool A, Tool B | skill-name |
```

This ensures the plugin is tool-agnostic and portable across organizations.

### 4. Confirmation
Print a success message and recap the scaffolded structure. Remind the user of three absolute standards:
1. If supercharged, populate `CONNECTORS.md` with specific tool mappings.
2. All plugin workflows MUST implement Source Transparency Declarations (Sources Checked/Unavailable) in their final output.
3. If this plugin will generate `.html`, `.svg`, or `.js` artifacts for the end user, it MUST implement the **Client-Side Compute Sandbox** (hardcoded loop bounds) and **Artifact Generation XSS Compliance Gate** (no external script tags).

**CRITICAL: Scaffold Previewer Phase**
Before finishing, if the user wants to check your generated code visually before it goes to production, offer to output the proposed hierarchy into `/tmp/scaffold-preview/` so they can evaluate the structure without modifying their real `plugins/` directory.

## Next Actions
- Offer to run `create-skill` to populate the plugin.
- Offer to run `create-mcp-integration` to add tool connectors.

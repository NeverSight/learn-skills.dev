---
name: cognitive-register
description: >
  Registers new cognitives (skills, agents, prompts, workflows, tools) into the SynapSync Registry with proper structure, manifest, and registry index.
  Trigger: When the user says "GUARDA", "REGISTRA", "AGREGA" followed by a cognitive type and name, or asks to save/register/add a cognitive to the registry.
license: Apache-2.0
metadata:
  author: synapsync
  version: "1.0"
  scope: [root]
  auto_invoke: "When the user asks to save, register, or add a cognitive to the synapse-registry"
  changelog:
    - version: "1.0"
      date: "2026-01-28"
      changes:
        - "Initial release with full registry management capabilities"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Task
---

## Purpose

Automate the registration of new cognitives into the SynapSync Registry, ensuring every entry follows the exact structure, naming conventions, manifest schema, and registry index format — with zero tolerance for inconsistencies.

## When to Use This Skill

- **User says "GUARDA X SKILL"**: Register a new skill with its content
- **User says "GUARDA X AGENT"**: Register a new agent with its content
- **User says "GUARDA X PROMPT"**: Register a new prompt with its content
- **User says "GUARDA X WORKFLOW"**: Register a new workflow with its content
- **User says "GUARDA X TOOL"**: Register a new tool with its content
- **User says "REGISTRA" or "AGREGA"**: Same as above, alternative trigger words
- **User provides cognitive content and asks to save it**: Infer type from content and register
- **English equivalents**: "SAVE X SKILL", "REGISTER X AGENT", "ADD X PROMPT"

## Trigger Pattern Recognition

The skill responds to these patterns (case-insensitive, Spanish or English):

```
GUARDA [el|la|un|una]? {name} [como]? SKILL|AGENT|PROMPT|WORKFLOW|TOOL
REGISTRA [el|la|un|una]? {name} [como]? SKILL|AGENT|PROMPT|WORKFLOW|TOOL
AGREGA [el|la|un|una]? {name} [como]? SKILL|AGENT|PROMPT|WORKFLOW|TOOL
SAVE {name} [as]? SKILL|AGENT|PROMPT|WORKFLOW|TOOL
REGISTER {name} [as]? SKILL|AGENT|PROMPT|WORKFLOW|TOOL
ADD {name} [as|to]? SKILL|AGENT|PROMPT|WORKFLOW|TOOL
```

If the user provides the cognitive content inline or in a previous message, use that content directly. If no content is provided, ask the user for it.

## Registry Structure (Source of Truth)

```
synapse-registry/
├── registry.json                          # Central index — MUST be updated
├── cognitives/                            # Public registry content
│   ├── skills/{category}/{name}/
│   │   ├── manifest.json                  # Metadata
│   │   ├── SKILL.md                       # Content file
│   │   └── assets/                        # Optional templates/schemas
│   ├── agents/{category}/{name}/
│   │   ├── manifest.json
│   │   └── {name}.md                      # Content file (uses cognitive name)
│   ├── prompts/{category}/{name}/
│   │   ├── manifest.json
│   │   └── PROMPT.md
│   ├── workflows/{category}/{name}/
│   │   ├── manifest.json
│   │   └── WORKFLOW.yaml
│   └── tools/{category}/{name}/
│       ├── manifest.json
│       └── TOOL.md
└── core/                                  # Internal tooling (not published)
    └── register/                          # This skill
```

## Valid Categories

| Category        | Use For                                      |
|-----------------|----------------------------------------------|
| `general`       | General-purpose, meta-tools, internal tooling |
| `frontend`      | UI, React, CSS, components                   |
| `backend`       | APIs, servers, backend services              |
| `database`      | Database queries, migrations, ORMs           |
| `devops`        | CI/CD, infrastructure, deployment            |
| `security`      | Security analysis, vulnerability scanning    |
| `testing`       | Testing strategies, QA automation            |
| `analytics`     | Data analysis, research, benchmarking        |
| `automation`    | Task automation, workflows                   |
| `integrations`  | External services (Supabase, Stripe, etc.)   |
| `planning`      | Project planning, SDLC, requirements, architecture |

If the cognitive doesn't clearly fit a category, default to `general`. If the user specifies a category, use it even if it's new — the registry supports extensibility.

## Valid Providers

```
claude, openai, cursor, windsurf, copilot, gemini, codex
```

**Default**: All providers unless the cognitive is provider-specific (e.g., an agent using Claude-only features).

## Cognitive Type → Content File Mapping

| Type     | Content File       | Notes                                    |
|----------|--------------------|------------------------------------------|
| skill    | `SKILL.md`         | Markdown with YAML frontmatter           |
| agent    | `{name}.md`        | Named after the cognitive, YAML frontmatter |
| prompt   | `PROMPT.md`        | Markdown with YAML frontmatter           |
| workflow | `WORKFLOW.yaml`    | Pure YAML definition                     |
| tool     | `TOOL.md`          | Markdown with YAML frontmatter           |

## Registration Workflow

### Step 1: Parse the Request

Extract from the user's message:
1. **Cognitive name**: The identifier (convert to kebab-case)
2. **Cognitive type**: skill, agent, prompt, workflow, or tool
3. **Content**: The actual cognitive content (inline, previous message, or ask)
4. **Category**: Infer from content/context or ask the user

**Name normalization rules**:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters except hyphens
- Examples: `"Project Planner"` → `project-planner`, `"API Error Handler"` → `api-error-handler`

### Step 2: Validate Uniqueness

Before creating anything, check that no cognitive with the same name exists:

1. Read `registry.json`
2. Search for the name in the `cognitives` array
3. If a duplicate exists, inform the user and ask how to proceed:
   - Update the existing cognitive (bump version)
   - Choose a different name
   - Cancel

### Step 3: Create Directory Structure

```bash
mkdir -p cognitives/{type}s/{category}/{name}
```

The directory follows the pattern: `cognitives/{type}s/{category}/{name}/`

Examples:
- `cognitives/skills/general/my-skill/`
- `cognitives/agents/devops/deploy-manager/`
- `cognitives/prompts/frontend/component-generator/`

### Step 4: Create Content File

Write the cognitive content to the appropriate file:

- **skill** → `cognitives/{type}s/{category}/{name}/SKILL.md`
- **agent** → `cognitives/{type}s/{category}/{name}/{name}.md`
- **prompt** → `cognitives/{type}s/{category}/{name}/PROMPT.md`
- **workflow** → `cognitives/{type}s/{category}/{name}/WORKFLOW.yaml`
- **tool** → `cognitives/{type}s/{category}/{name}/TOOL.md`

If the user provided content with YAML frontmatter, use it as-is. If not, ensure the content has proper frontmatter before writing.

### Step 5: Create manifest.json

Every cognitive MUST have a `manifest.json` in its directory:

```json
{
  "$schema": "https://synapsync.dev/schemas/cognitive-manifest.json",
  "name": "{name}",
  "type": "{type}",
  "version": "1.0.0",
  "description": "{max 100 chars — extracted from content or user input}",
  "author": {
    "name": "SynapSync",
    "url": "https://github.com/SynapSync",
    "email": "hello@synapsync.dev"
  },
  "license": "Apache-2.0",
  "category": "{category}",
  "tags": ["{tag1}", "{tag2}", "...max 10 tags"],
  "providers": ["claude", "openai", "cursor", "windsurf", "copilot", "gemini"],
  "file": "{content-file-name}",
  "repository": {
    "type": "git",
    "url": "https://github.com/SynapSync/synapse-registry"
  },
  "homepage": "https://synapsync.dev/cognitives/{name}",
  "createdAt": "{ISO 8601 current date}T00:00:00Z",
  "updatedAt": "{ISO 8601 current date}T00:00:00Z"
}
```

**Field extraction rules**:
- `name`: From the parsed request (kebab-case)
- `description`: From YAML frontmatter `description` field, trimmed to 100 chars. Remove trigger text — only keep the functional description
- `tags`: Infer from content topics, category, and type. Maximum 10 tags
- `providers`: Default to all providers unless content indicates provider-specific features
- `file`: Based on type mapping (see table above)
- `createdAt`/`updatedAt`: Current date in ISO 8601

### Step 6: Update registry.json

Add the new cognitive to `registry.json`:

1. Read current `registry.json`
2. Increment `totalCognitives` by 1
3. Append a new entry to the `cognitives` array:

```json
{
  "name": "{name}",
  "type": "{type}",
  "version": "1.0.0",
  "description": "{same as manifest description}",
  "author": "synapsync",
  "category": "{category}",
  "tags": ["{same tags as manifest}"],
  "providers": ["{same providers as manifest}"],
  "downloads": 0,
  "path": "cognitives/{type}s/{category}/{name}"
}
```

**Critical**: The `registry.json` entry uses `"author"` as a flat string (not an object), unlike `manifest.json` which uses an author object.

### Step 7: Confirmation

After successful registration, report:
- Created files and their paths
- Updated `registry.json` with new count
- The cognitive's full path in the registry

## Validation Rules (Enforced on Every Registration)

These rules are non-negotiable. If any fails, fix it before completing:

| Rule                       | Requirement                                                |
|----------------------------|------------------------------------------------------------|
| Unique name                | No other cognitive in `registry.json` has the same name    |
| Valid manifest.json        | All required fields present, matches schema                |
| Content file exists        | The file referenced in `manifest.file` exists              |
| Frontmatter consistency    | Frontmatter `name` matches `manifest.name`                 |
| Valid category             | Category is from the valid categories list                 |
| Tags limit                 | Maximum 10 tags                                            |
| Description length         | Maximum 100 characters in manifest/registry description    |
| Name format                | Lowercase, hyphens only, no spaces or special chars        |
| Version format             | Semantic versioning (e.g., `1.0.0`)                        |
| Path format                | `cognitives/{type}s/{category}/{name}` matches actual directory |
| registry.json sync         | `totalCognitives` count matches actual array length        |

## Naming Convention Reference

| Pattern                    | When to Use                                    | Examples                           |
|----------------------------|------------------------------------------------|------------------------------------|
| `{technology}`             | Generic technology skill                       | `typescript`, `react-hooks`        |
| `{tech}-{feature}`         | Technology + specific feature                  | `react-testing`, `node-logging`    |
| `{framework}-{component}`  | Framework + component type                     | `nextjs-api`, `express-middleware` |
| `{action}-{target}`        | Action-oriented naming                         | `skill-creator`, `code-reviewer`   |
| `{domain}-{function}`      | Domain + function                              | `auth-validator`, `data-migrator`  |

**Bad names**: `utils`, `helpers`, `common`, `misc`, `project1`, `test`, `new-skill`
**Good names**: `cognitive-registrar`, `api-error-handler`, `feature-branch-manager`

## Critical Patterns

### Pattern 1: Always Read Before Write

Before creating any file, read `registry.json` to verify:
- The name doesn't already exist
- The current `totalCognitives` count
- The existing structure to maintain consistency

### Pattern 2: Description Extraction

When extracting a description from content frontmatter:
- Remove the `Trigger:` portion — descriptions should be functional, not trigger-based
- Trim to 100 characters maximum
- Make it action-oriented: "Creates...", "Manages...", "Analyzes..."

Example:
```yaml
# Frontmatter says:
description: >
  Comprehensive project planning framework with structured analysis, planning, and execution phases.
  Trigger: When planning a new feature...

# manifest.json/registry.json gets:
"description": "Comprehensive project planning framework with analysis, planning, and execution phases"
```

### Pattern 3: Tag Inference

Generate tags by analyzing:
1. The cognitive type itself (e.g., `skill`, `agent`)
2. Key topics from the content (e.g., `planning`, `git`, `testing`)
3. The category (e.g., `devops`, `frontend`)
4. Action verbs from the purpose (e.g., `automation`, `analysis`)
5. Technologies mentioned (e.g., `react`, `typescript`, `docker`)

Keep tags lowercase, hyphenated, and meaningful. Avoid redundant tags (don't add `skill` tag to a skill unless it's a meta-skill about skills).

### Pattern 4: Provider Detection

Default to all providers. Restrict only when:
- Content uses provider-specific syntax (e.g., Claude XML tags, OpenAI function calling)
- The agent definition uses provider-specific fields (e.g., `model: sonnet`)
- The user explicitly states provider restrictions

### Pattern 5: Atomic Registration

All three artifacts (content file, manifest.json, registry.json) must be created/updated in a single operation. Never leave the registry in a partial state:
- If content file creation fails, don't update registry.json
- If manifest.json creation fails, clean up the content file
- Always verify the final state after all writes

### Pattern 6: Category Directory Creation

If the category directory doesn't exist under the type directory, create it:
```bash
# If cognitives/skills/planning/ doesn't exist yet
mkdir -p cognitives/skills/planning/project-planner
```

This is valid — the registry supports new categories as the ecosystem grows.

## Best Practices

### Before Registration

1. **Verify the cognitive content is complete**: Don't register stubs or placeholders
2. **Check for duplicates**: Search by name AND by similar descriptions
3. **Validate frontmatter**: Ensure all required fields exist in the content file
4. **Confirm category**: If uncertain, ask the user

### During Registration

1. **Create files in order**: Directory → Content file → manifest.json → registry.json
2. **Use consistent dates**: Same `createdAt` and `updatedAt` for new cognitives
3. **Match descriptions**: manifest.json and registry.json descriptions must be identical
4. **Match tags and providers**: manifest.json and registry.json must have identical arrays

### After Registration

1. **Verify registry.json**: Read it back to confirm the entry was added correctly
2. **Confirm totalCognitives**: Ensure count matches array length
3. **Report to user**: List all created files and the registry path

## Integration with Other Skills

### With `skill-creator`
Use `skill-creator` to generate the SKILL.md content, then use `cognitive-registrar` to register it in the registry.

### With `feature-branch-manager`
After registering a cognitive, use `feature-branch-manager` to commit the changes and create a PR.

## Limitations

1. **No automated validation CI**: Validation is performed at registration time by the AI, not by a CI pipeline
2. **No version bumping**: Currently registers new cognitives at `1.0.0`. Version updates require manual intervention
3. **No dependency resolution**: Does not check if referenced skills/agents in content actually exist
4. **Single registry**: Only manages the `synapse-registry` — does not publish to external registries

## Troubleshooting

### Issue: "Name already exists in registry"

**Solution**: Check `registry.json` for the existing entry. Offer the user options: update the existing cognitive (bump version), choose a different name, or cancel.

### Issue: "Category directory doesn't exist"

**Solution**: This is normal for new categories. The `mkdir -p` command handles this automatically. The registry supports extensible categories.

### Issue: "Content has no YAML frontmatter"

**Solution**: If the user provides raw content without frontmatter, generate the frontmatter based on the cognitive name, type, and inferred metadata before writing the file.

### Issue: "Description exceeds 100 characters"

**Solution**: Truncate intelligently — don't cut mid-word. Rephrase to be more concise while preserving meaning.

### Issue: "registry.json totalCognitives is out of sync"

**Solution**: Count the actual entries in the `cognitives` array and set `totalCognitives` to match. Never trust the existing count — always recalculate.

## Example: Registering a Skill

**User says**: `GUARDA project-planner SKILL` (with content provided)

**AI executes**:

1. Parse: name=`project-planner`, type=`skill`, category=`planning` (inferred from content)
2. Check `registry.json` → no duplicate found
3. Create `cognitives/skills/planning/project-planner/`
4. Write `cognitives/skills/planning/project-planner/SKILL.md` (user's content)
5. Write `cognitives/skills/planning/project-planner/manifest.json`
6. Update `registry.json`:
   - `totalCognitives`: 2 → 3
   - Add entry with `"path": "cognitives/skills/planning/project-planner"`
7. Confirm: "Registered `project-planner` skill in `cognitives/skills/planning/project-planner/`"

## Example: Registering an Agent

**User says**: `GUARDA deploy-automator AGENT` (with content provided)

**AI executes**:

1. Parse: name=`deploy-automator`, type=`agent`, category=`devops` (inferred)
2. Check `registry.json` → no duplicate found
3. Create `cognitives/agents/devops/deploy-automator/`
4. Write `cognitives/agents/devops/deploy-automator/deploy-automator.md` (note: agents use `{name}.md`)
5. Write `cognitives/agents/devops/deploy-automator/manifest.json` with `"file": "deploy-automator.md"`
6. Update `registry.json`
7. Confirm registration

## Version History

- **1.0** (2026-01-28): Initial release with full registration workflow for all cognitive types

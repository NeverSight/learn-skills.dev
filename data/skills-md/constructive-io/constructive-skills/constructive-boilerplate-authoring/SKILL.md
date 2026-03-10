---
name: constructive-boilerplate-authoring
description: Create and customize boilerplate templates for pgpm init. Use when authoring custom boilerplate templates, configuring .boilerplate.json, defining placeholder questions, or setting up a custom template repository.
---

Create and customize boilerplate templates for `pgpm init`.

## Overview

PGPM uses the `genomic` library to scaffold projects from templates. Templates are stored in a boilerplate repository (default: `constructive-io/pgpm-boilerplates`) and use placeholder substitution for customization.

## Template Repository Structure

```
my-boilerplates/
  .boilerplates.json       # Root config (points to default directory)
  pgpm/                    # Default template variant (PGPM)
    module/
      .boilerplate.json    # Module template config
      package.json         # Template files with placeholders
      pgpm.plan
      ...
    workspace/
      .boilerplate.json    # Workspace template config
      package.json
      pgpm.json
      ...
  pnpm/                    # Alternative variant (pure PNPM, no pgpm files)
    module/
      .boilerplate.json
      ...
    workspace/
      .boilerplate.json
      ...
```

## Root Configuration

The `.boilerplates.json` file at the repository root specifies the default template directory:

```json
{
  "dir": "pgpm"
}
```

## Template Configuration

Each template has a `.boilerplate.json` file defining its type, workspace requirements, and questions.

### Basic Structure

```json
{
  "type": "workspace",
  "questions": [
    {
      "name": "____repoName____",
      "message": "Enter the repository name",
      "required": true
    }
  ]
}
```

### Template Types

| Type | Description |
|------|-------------|
| `workspace` | Creates a new monorepo workspace |
| `module` | Creates a package within a workspace |
| `generic` | Standalone template (no workspace context) |

### Workspace Requirements

The `requiresWorkspace` field controls what type of workspace the template needs:

```json
{
  "type": "module",
  "requiresWorkspace": "pgpm"
}
```

| Value | Description |
|-------|-------------|
| `"pgpm"` | Requires PGPM workspace (pgpm.json), creates pgpm.plan/.control files |
| `"pnpm"` | Requires PNPM workspace (pnpm-workspace.yaml) |
| `"lerna"` | Requires Lerna workspace (lerna.json) |
| `"npm"` | Requires npm workspace (package.json with workspaces) |
| `false` | No workspace required |

## Placeholder System

Templates use the `____placeholder____` pattern (4 underscores on each side) for variable substitution:

```json
{
  "name": "@____username____/____moduleName____",
  "version": "0.0.1",
  "description": "____moduleDesc____",
  "author": "____fullName____ <____email____>"
}
```

## Question Configuration

### Question Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Placeholder name (e.g., `____fullName____`) |
| `message` | string | Prompt shown to user |
| `required` | boolean | Whether the field is required |
| `type` | string | Input type: `text`, `list`, `checkbox` |
| `options` | string[] | Static options for list/checkbox |
| `default` | any | Static default value |
| `defaultFrom` | string | Resolver for dynamic default |
| `setFrom` | string | Auto-set value (skips prompt) |
| `optionsFrom` | string | Resolver for dynamic options |

### Question Types

**Text Input (default):**
```json
{
  "name": "____moduleName____",
  "message": "Enter the module name",
  "required": true
}
```

**List Selection:**
```json
{
  "name": "____access____",
  "message": "Module access?",
  "type": "list",
  "options": ["public", "restricted"],
  "default": "public"
}
```

**Checkbox (multi-select):**
```json
{
  "name": "____extensions____",
  "message": "Select PostgreSQL extensions",
  "type": "checkbox",
  "options": ["plpgsql", "uuid-ossp", "citext", "pgcrypto"]
}
```

### Resolvers

Resolvers dynamically populate values from the environment or workspace context.

**defaultFrom Resolvers:**
| Resolver | Description |
|----------|-------------|
| `git.user.name` | Git config user.name |
| `git.user.email` | Git config user.email |
| `npm.whoami` | npm whoami result |
| `workspace.dirname` | Current directory name |

**setFrom Resolvers (auto-set, skips prompt):**
| Resolver | Description |
|----------|-------------|
| `workspace.name` | Workspace name from pgpm.json/package.json |
| `workspace.author.name` | Workspace author name |
| `workspace.author.email` | Workspace author email |
| `workspace.license` | Workspace license |
| `workspace.organization.name` | Workspace organization |

**optionsFrom Resolvers:**
| Resolver | Description |
|----------|-------------|
| `licenses` | List of SPDX license identifiers |

### Example: Complete Module Template

```json
{
  "type": "module",
  "requiresWorkspace": "pgpm",
  "questions": [
    {
      "name": "____fullName____",
      "message": "Enter author full name",
      "setFrom": "workspace.author.name",
      "defaultFrom": "git.user.name",
      "required": true
    },
    {
      "name": "____email____",
      "message": "Enter author email",
      "setFrom": "workspace.author.email",
      "defaultFrom": "git.user.email",
      "required": true
    },
    {
      "name": "____moduleName____",
      "message": "Enter the module name",
      "required": true
    },
    {
      "name": "____moduleDesc____",
      "message": "Enter the module description",
      "required": true
    },
    {
      "name": "____repoName____",
      "message": "Enter the repository name",
      "setFrom": "workspace.name",
      "required": true
    },
    {
      "name": "____username____",
      "message": "Enter your github username",
      "setFrom": "workspace.organization.name",
      "defaultFrom": "npm.whoami",
      "required": true
    },
    {
      "name": "____access____",
      "message": "Module access?",
      "type": "list",
      "options": ["public", "restricted"],
      "default": "public",
      "required": true
    },
    {
      "name": "____license____",
      "message": "Choose a license",
      "type": "list",
      "optionsFrom": "licenses",
      "setFrom": "workspace.license",
      "required": true
    }
  ]
}
```

## Creating a Custom Boilerplate Repository

1. Create a new repository with the structure above
2. Add `.boilerplates.json` pointing to your default directory
3. Create template directories with `.boilerplate.json` configs
4. Add template files with `____placeholder____` patterns
5. Use with `pgpm init --repo owner/your-boilerplates`

## Using Custom Templates

```bash
# Use your own boilerplate repository
pgpm init workspace --repo myorg/my-boilerplates

# Use a specific branch
pgpm init workspace --repo myorg/my-boilerplates --from-branch develop

# Use a variant directory
pgpm init workspace --repo myorg/my-boilerplates --dir custom-variant

# Use the --template flag (recommended)
pgpm init --template pnpm/module --repo myorg/my-boilerplates
pgpm init -t custom-variant/module --repo myorg/my-boilerplates

# Create workspace + module in one command
pgpm init -t pnpm/module -w --repo myorg/my-boilerplates
```

## Best Practices

1. Use `setFrom` for values that should inherit from workspace context
2. Use `defaultFrom` for sensible defaults that users can override
3. Keep placeholder names descriptive and consistent
4. Document custom templates in your repository README
5. Test templates with `--no-tty` to ensure all required fields are defined

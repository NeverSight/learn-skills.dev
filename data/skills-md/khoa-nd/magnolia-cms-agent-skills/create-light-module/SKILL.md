---
name: create-light-module
description: Use Magnolia CLI to scaffold and manage light modules, components, pages, apps, content types, REST endpoints, blocks, and virtual URIs.
metadata:
  author: khoanguyen
  version: "2.0"
---

# create-light-module

> Scaffold Magnolia CMS light modules and their contents using the Magnolia CLI

## Description

This skill guides AI agents to use the **Magnolia CLI v5** (`@magnolia/cli`) to scaffold light modules and all their sub-components. The CLI uses a plugin-based architecture where each scaffolding operation (create component, create page, etc.) is a separate installable plugin.

**Approach:** Always try CLI commands first. Fall back to manual file creation only if the CLI is not installed and the user does not want to install it.

## When to Use

Use this skill when the user wants to:

- Create a new Magnolia light module
- Create components, pages, or page templates
- Create apps or content types
- Create REST endpoint configurations
- Create blocks or virtual URI mappings
- Scaffold any part of a light module structure
- Set up a new Magnolia project from scratch (jumpstart)

## Instructions

### Prerequisites

- **Node.js**: Latest LTS version. Verify with `node -v`
- **Java**: Only required if using the Start plugin to run Magnolia locally

### Setup & Installation

#### Option 1: Jumpstart (recommended for new projects)

```bash
npx @magnolia/cli@latest jumpstart [project-name]
```

This automatically installs the CLI locally, creates `package.json`, and generates `mgnl.config.js`.

#### Option 2: Local installation (existing projects)

```bash
npm init -y
npm install @magnolia/cli
```

Add to `package.json`:

```json
{
  "scripts": {
    "mgnl": "node node_modules/@magnolia/cli"
  },
  "type": "module"
}
```

Create `mgnl.config.js`:

```javascript
export default {
  plugins: [],
  logger: {
    filename: "./mgnl.error.log",
    fileLevel: "warn",
    consoleLevel: "debug"
  }
};
```

#### Option 3: Global installation

```bash
sudo npm install @magnolia/cli -g
```

#### Verify installation

```bash
# Local
npm run mgnl -- -h
npm run mgnl -- -V

# Global
mgnl -h
mgnl -V
```

### Configuration (mgnl.config.js)

The `mgnl.config.js` file in the project root configures the CLI:

```javascript
import CreateLightModulePlugin from "@magnolia/cli-create-light-module-plugin";
import CreateComponentPlugin from "@magnolia/cli-create-component-plugin";

export default {
  lightModulesPath: "./light-modules",
  lightModule: "my-lm",
  plugins: [
    new CreateLightModulePlugin(),
    new CreateComponentPlugin()
  ],
  logger: {
    filename: "./mgnl.error.log",
    fileLevel: "warn",
    consoleLevel: "debug"
  }
};
```

**Global properties** (shared across plugins):

| Property | Description |
|----------|-------------|
| `lightModulesPath` | Directory containing all light modules |
| `lightModule` | Default target light module name |

**Argument precedence** (highest to lowest):

1. CLI command-line flags
2. Plugin-level arguments in `mgnl.config.js`
3. Global arguments in `mgnl.config.js`

### Plugin Management

```bash
# Install a plugin (auto-registers in mgnl.config.js)
npm run mgnl -- add-plugin @magnolia/cli-create-component-plugin

# List installed plugins and commands
npm run mgnl

# Update a plugin
npm update @magnolia/cli-create-component-plugin

# Uninstall: remove from mgnl.config.js, then:
npm uninstall @magnolia/cli-create-component-plugin
```

### CLI Commands

#### Create Light Module

**Package:** `@magnolia/cli-create-light-module-plugin`

```bash
npm run mgnl -- add-plugin @magnolia/cli-create-light-module-plugin
```

**Command:** `create-light-module <name> [options]`

| Option | Description |
|--------|-------------|
| `-d, --directories` | Create specific directories: A=apps, B=blocks, C=contentTypes, D=decorations, DIA=dialogs, I=i18n, INC=includes, M=messageViews, R=restEndpoints, T=templates, THM=themes, V=virtualUriMappings, W=webresources |
| `-md, --module-descriptor` | Set module version (default: `1.0.0`) |
| `-lmp, --light-modules-path` | Set output directory path |
| `-p, --prototype` | Select prototype: `_default` or `comprehensive` |
| `-pd, --prototype-dir` | Use custom prototype templates directory |

**Examples:**

```bash
# Create with default structure
npm run mgnl -- create-light-module "my-website"

# Create with comprehensive structure
npm run mgnl -- create-light-module "my-website" --prototype "comprehensive"

# Create with specific directories only
npm run mgnl -- create-light-module "my-website" --directories A D T W

# Create with custom version
npm run mgnl -- create-light-module "my-website" -md "2.0.0"

# Create in specific path
npm run mgnl -- create-light-module "my-website" --light-modules-path "./magnolia/light-modules"
```

**Generated files:** `README.md`, `module.yaml`, `i18n/<name>-messages_en.properties`, plus selected directories.

#### Create Component

**Package:** `@magnolia/cli-create-component-plugin`

```bash
npm run mgnl -- add-plugin @magnolia/cli-create-component-plugin
```

**Command:** `create-component [name] [options]`

| Option | Description |
|--------|-------------|
| `-a [[lm-name:]page-template[@area]]` | Make component available on a page template |
| `-lm, --light-module [name]` | Target light module |
| `-p, --prototype [name]` | Select prototype |

**Examples:**

```bash
npm run mgnl -- create-component "my-component"
npm run mgnl -- create-component "my-component" --available "basic"
npm run mgnl -- create-component "my-component" --light-module "my-lm"
```

#### Create Page

**Package:** `@magnolia/cli-create-page-plugin`

```bash
npm run mgnl -- add-plugin @magnolia/cli-create-page-plugin
```

**Command:** `create-page [name] [options]`

| Option | Description |
|--------|-------------|
| `-lm, --light-module [name]` | Target light module |
| `-p, --prototype [name]` | Select page prototype |

**Examples:**

```bash
npm run mgnl -- create-page "my-page"
npm run mgnl -- create-page "my-page" --light-module "my-lm"
npm run mgnl -- create-page "my-page" --prototype "card"
```

#### Create App

**Package:** `@magnolia/cli-create-app-plugin`

```bash
npm run mgnl -- add-plugin @magnolia/cli-create-app-plugin
```

**Command:** `create-app <name> [options]`

| Option | Description |
|--------|-------------|
| `-ct, --content-type <name>` | Associate with a content type (singular form recommended) |
| `-lm, --light-module [name]` | Target light module |
| `-p, --prototype [name]` | Select prototype |

**Examples:**

```bash
npm run mgnl -- create-app "my-app"
npm run mgnl -- create-app "my-app" --content-type "my-ct"
npm run mgnl -- create-app "my-app" --light-module "my-lm"
```

#### Create Content Type

**Package:** `@magnolia/cli-create-content-type-plugin`

```bash
npm run mgnl -- add-plugin @magnolia/cli-create-content-type-plugin
```

**Command:** `create-content-type <name> [options]`

| Option | Description |
|--------|-------------|
| `-a, --app [name]` | Create associated content app and workspace (plural form recommended) |
| `-lm, --light-module [name]` | Target light module |
| `-p, --prototype [name]` | Select prototype |

**Examples:**

```bash
npm run mgnl -- create-content-type "my-ct"
npm run mgnl -- create-content-type "my-ct" --app "my-app"
npm run mgnl -- create-content-type "my-ct" --light-module "my-lm"
```

#### Create REST Endpoint

**Package:** `@magnolia/cli-create-rest-endpoint-plugin`

```bash
npm run mgnl -- add-plugin @magnolia/cli-create-rest-endpoint-plugin
```

**Command:** `create-rest-endpoint [workspace] [options]`

| Option | Description |
|--------|-------------|
| `-d, --destination [path]` | REST endpoint subdirectory (default: `/delivery`) |
| `-lm, --light-module [name]` | Target light module |
| `-s, --source [path...]` | Detect workspaces from file paths |

**Examples:**

```bash
# Create endpoints for all detected workspaces
npm run mgnl -- create-rest-endpoint

# Create for a specific workspace
npm run mgnl -- create-rest-endpoint "foo"

# Custom destination directory
npm run mgnl -- create-rest-endpoint "foo" --destination "/zig"

# Specify light module
npm run mgnl -- create-rest-endpoint --light-module "my-lm"
```

**Generated files:** `restEndpoints/delivery/<workspace>_v1.yaml` (auto-increments version if conflicts exist). For `website` workspace, creates `pages_v1.yaml`.

#### Create Block

**Package:** `@magnolia/cli-create-block-plugin`

```bash
npm run mgnl -- add-plugin @magnolia/cli-create-block-plugin
```

**Command:** `create-block <name> [options]`

| Option | Description |
|--------|-------------|
| `-lm, --light-module [name]` | Target light module |
| `-p, --prototype [name]` | Select prototype: `_default` or `empty` |

**Examples:**

```bash
npm run mgnl -- create-block "my-block"
npm run mgnl -- create-block "my-block" --light-module "my-lm"
npm run mgnl -- create-block "my-block" --prototype "empty"
```

#### Create Virtual URI

**Package:** `@magnolia/cli-create-virtual-uri-plugin`

```bash
npm run mgnl -- add-plugin @magnolia/cli-create-virtual-uri-plugin
```

**Command:** `create-virtual-uri <name> [options]`

| Option | Description |
|--------|-------------|
| `-f, --from <uri>` | Pattern to match in requested URI |
| `-t, --to <prefix:uri>` | Target URI with prefix: `redirect:`, `permanent:`, or `forward:` |
| `-lm, --light-module [name]` | Target light module |
| `-p, --prototype [name]` | Select prototype: `_default`, `regexp`, or `empty` |

**Examples:**

```bash
npm run mgnl -- create-virtual-uri "my-vu"
npm run mgnl -- create-virtual-uri "my-vu" --from "/foo" --to "forward:/bar"
npm run mgnl -- create-virtual-uri "my-vu" --prototype "regexp"
```

### Manual Fallback

If the CLI is not available and the user prefers not to install it, create files manually.

#### Folder Structure

**Default structure:**

```
<module-name>/
├── README.md
├── module.yaml
├── i18n/
│   └── <module-name>-messages_en.properties
├── dialogs/
│   ├── components/
│   └── pages/
├── templates/
│   ├── components/
│   └── pages/
└── webresources/
    ├── css/
    ├── js/
    └── images/
```

**Comprehensive structure** (adds these directories):

```
apps/  blocks/  contentTypes/  decorations/  includes/
messageViews/  restEndpoints/  themes/  virtualUriMappings/
```

#### Core File Templates

**module.yaml:**

```yaml
name: <module-name>
version: 1.0.0
```

**Page template (templates/pages/home.yaml):**

```yaml
renderType: freemarker
templateScript: /<module-name>/templates/pages/home.ftl
dialog: <module-name>:pages/homePageProperties
title: Home Page
areas:
  main:
    availableComponents:
      text:
        id: <module-name>:components/text
```

**Component template (templates/components/text.yaml):**

```yaml
renderType: freemarker
templateScript: /<module-name>/templates/components/text.ftl
dialog: <module-name>:components/textDialog
title: Text Component
```

**Dialog (dialogs/components/textDialog.yaml):**

```yaml
form:
  properties:
    text:
      $type: richTextField
      label: Text Content
```

**i18n properties (<module-name>-messages_en.properties):**

```properties
<module-name>.pages.home.title=Home Page
<module-name>.components.text.title=Text Component
```

## Supported Definition Types

| Type | Directory | Description |
|------|-----------|-------------|
| Apps | `apps/` | Content apps with data sources and workbench |
| Blocks | `blocks/` | Reusable content blocks |
| Content Types | `contentTypes/` | Define content structure |
| Decorations | `decorations/` | Decorate existing definitions |
| Dialogs | `dialogs/` | Editor UI forms |
| Includes | `includes/` | Reusable FreeMarker includes |
| Message Views | `messageViews/` | Custom message templates |
| REST Endpoints | `restEndpoints/` | REST API definitions |
| Templates | `templates/` | Page and component templates |
| Themes | `themes/` | Visual themes |
| Virtual URI Mappings | `virtualUriMappings/` | URL rewriting rules |
| Web Resources | `webresources/` | Static assets (CSS, JS, images) |

## Examples

**User prompt:** "Create a new light module called my-website"

**Expected behavior:** Run `npm run mgnl -- create-light-module "my-website"`. If CLI is not installed, offer to install it or create the folder structure manually.

**User prompt:** "Add a text component to my-website light module"

**Expected behavior:** Ensure the create-component plugin is installed (`npm run mgnl -- add-plugin @magnolia/cli-create-component-plugin`), then run `npm run mgnl -- create-component "text" --light-module "my-website"`.

**User prompt:** "Create REST endpoints for my-website"

**Expected behavior:** Ensure the create-rest-endpoint plugin is installed, then run `npm run mgnl -- create-rest-endpoint --light-module "my-website"`.

**User prompt:** "Create a comprehensive light module with all directories"

**Expected behavior:** Run `npm run mgnl -- create-light-module "corporate-site" --prototype "comprehensive"`.

## Notes

- Light modules must be placed in the `light-modules` directory of your Magnolia installation
- Module names should be lowercase with hyphens (kebab-case)
- Use `.yaml` extension (not `.yml`) for all definition files
- Magnolia auto-detects file changes without restart (hot-reload)
- Plugins auto-update `mgnl.config.js` with discovered values (e.g., `lightModulesPath`, `lightModule`)
- PowerShell users should enclose `--` in quotes: `npm run mgnl "--" add-plugin ...`

### Limitations

Light modules do **not** support:

- Workspace registration
- Node type registration
- Module classes (Java)
- Version handlers
- Workflows

For these features, use traditional Maven/Java modules.

## References

See [REFERENCE.md](./REFERENCE.md) for a complete list of official Magnolia CLI documentation links.

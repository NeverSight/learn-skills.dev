---
name: extension-guide-v3
description: Create Sindri V3 extensions for the Rust CLI platform. Use when creating V3 extensions, understanding V3 extension.yaml structure, validating against V3 schema, using collision-handling and project-context features, adding extensions to the compatibility matrix, or upgrading extension software versions. Covers mise, apt, binary, npm, npm-global, script, hybrid install methods.
---

# Sindri V3 Extension Development Guide

V3 extensions are YAML-driven, declarative configurations for the modern Rust-based Sindri CLI platform.

## V3 Paths and Resources

| Resource | Path |
|----------|------|
| **Extensions Directory** | `v3/extensions/` |
| **Registry** | `v3/registry.yaml` |
| **Schema** | `v3/schemas/extension.schema.json` |
| **Compatibility Matrix** | `v3/compatibility-matrix.yaml` |
| **Extension Docs** | Generated on-demand via `sindri extension docs <name>` |
| **Catalog** | `v3/docs/EXTENSIONS.md` |

## V3 Categories

```yaml
# Valid V3 categories (different from V2!)
- ai-agents      # AI agent frameworks
- ai-dev         # AI development tools
- claude         # Claude-specific tools
- cloud          # Cloud provider tools
- desktop        # Desktop environments
- devops         # DevOps/CI/CD tools
- documentation  # Documentation tools
- languages      # Programming runtimes
- mcp            # Model Context Protocol servers
- productivity   # Productivity tools
- research       # Research tools
- testing        # Testing frameworks
```

## Quick Start Checklist

1. [ ] Create directory: `v3/extensions/{name}/`
2. [ ] Create `extension.yaml` with required sections
3. [ ] Validate: `sindri extension validate {name}`
4. [ ] Test: `sindri extension install {name}`
5. [ ] Add `docs` section to `extension.yaml` (optional, for human-written content)
6. [ ] Update catalog: `v3/docs/EXTENSIONS.md`
7. [ ] Add to registry: `v3/registry.yaml` (alphabetically by category)
8. [ ] Add to compatibility matrix: `v3/compatibility-matrix.yaml` (see [Compatibility Matrix Management](#compatibility-matrix-management))

## Extension Directory Structure

```text
v3/extensions/{name}/
├── extension.yaml       # Required: Main definition
├── mise.toml            # Optional: mise configuration
├── scripts/             # Optional: Custom scripts
│   ├── install.sh
│   └── uninstall.sh
├── templates/           # Optional: Config templates
│   └── SKILL.md         # Project context file
└── resources/           # Optional: Additional resources
```

## Minimal Extension Template

```yaml
metadata:
  name: my-extension
  version: 1.0.0
  description: Brief description (10-200 chars)
  category: ai-dev  # Use V3 categories!
  dependencies: []

install:
  method: mise
  mise:
    configFile: mise.toml

validate:
  commands:
    - name: mytool
      versionFlag: --version
      expectedPattern: "v\\d+\\.\\d+\\.\\d+"
```

## Install Methods

### mise (Recommended for language tools)

```yaml
install:
  method: mise
  mise:
    configFile: mise.toml
    reshimAfterInstall: true
```

### apt (System packages)

```yaml
install:
  method: apt
  apt:
    repositories:
      - gpgKey: https://download.docker.com/linux/ubuntu/gpg
        sources: "deb [arch=amd64] https://download.docker.com/linux/ubuntu jammy stable"
    packages:
      - docker-ce
    updateFirst: true
```

### binary (Direct download - Enhanced in V3)

```yaml
install:
  method: binary
  binary:
    downloads:
      - name: tool
        source:
          type: github-release  # or: direct-url
          url: https://github.com/org/repo
          asset: "tool-linux-amd64.tar.gz"
          version: latest
        destination: ~/.local/bin/tool
        extract: true
```

### npm-global (V3-only method)

```yaml
install:
  method: npm-global
  npm:
    package: "@scope/package@latest"
```

### script (Custom installation)

```yaml
install:
  method: script
  script:
    path: scripts/install.sh
    args: ["--option", "value"]
    timeout: 600  # V3 default is 600s
```

### hybrid (Multiple methods)

```yaml
install:
  method: hybrid
  hybrid:
    steps:
      - method: apt
        apt:
          packages: [build-essential]
      - method: script
        script:
          path: scripts/install.sh
```

## Requirements (V3 Enhanced)

```yaml
requirements:
  domains:
    - api.github.com
    - registry.npmjs.org
  diskSpace: 500          # MB required
  memory: 256             # MB runtime memory
  installTime: 120        # Estimated seconds
  installTimeout: 600     # Max timeout
  validationTimeout: 30   # Validation timeout
  secrets:
    - GITHUB_TOKEN
  gpu:                    # V3-only: GPU requirements
    required: false
    recommended: true
    type: nvidia          # nvidia, amd, any
    minCount: 1
    minMemory: 4096       # MB
    cudaVersion: "12.0"
```

## Capabilities (Optional - Advanced Extensions)

### project-init (with priority)

```yaml
capabilities:
  project-init:
    enabled: true
    priority: 50          # V3-only: Lower = earlier execution
    commands:
      - command: "mytool init --force"
        description: "Initialize mytool"
        requiresAuth: anthropic
        conditional: false
    state-markers:
      - path: ".mytool"
        type: directory
    validation:
      command: "mytool --version"
      expectedPattern: "^\\d+\\.\\d+"
```

### auth (Multi-method)

```yaml
capabilities:
  auth:
    provider: anthropic   # anthropic, openai, github, custom
    required: false
    methods: [api-key, cli-auth]
    envVars: [ANTHROPIC_API_KEY]
    validator:
      command: "claude --version"
      expectedExitCode: 0
    features:
      - name: agent-spawn
        requiresApiKey: false
        description: "Works with CLI auth"
      - name: api-integration
        requiresApiKey: true
        description: "Requires API key"
```

### hooks (Lifecycle)

```yaml
capabilities:
  hooks:
    pre-install:
      command: "echo 'Pre-install'"
      description: "Preparation"
    post-install:
      command: "mytool doctor"
      description: "Health check"
    pre-project-init:
      command: "mytool check"
    post-project-init:
      command: "echo 'Ready'"
```

### mcp (MCP Server Registration)

```yaml
capabilities:
  mcp:
    enabled: true
    server:
      command: "npx"
      args: ["-y", "@mytool/mcp-server", "start"]
      env:
        MYTOOL_MCP_MODE: "1"
    tools:
      - name: "mytool-action"
        description: "Perform action"
      - name: "mytool-query"
        description: "Query data"
```

### project-context (V3-only: CLAUDE.md merging)

```yaml
capabilities:
  project-context:
    enabled: true
    mergeFile:
      source: templates/SKILL.md
      target: CLAUDE.md
      strategy: append-if-missing  # append, prepend, merge, replace, append-if-missing
```

### features (Advanced feature flags)

```yaml
capabilities:
  features:
    core:
      daemon_autostart: true
      flash_attention: true
      unified_config: true
    swarm:
      default_topology: hierarchical-mesh
      consensus_algorithm: raft
    llm:
      default_provider: anthropic
      load_balancing: false
    advanced:
      sona_learning: false
      security_scanning: true
      claims_system: false
      plugin_system: true
    mcp:
      transport: stdio  # stdio, http, websocket
```

### collision-handling (V3-only: Smart conflict resolution)

```yaml
capabilities:
  collision-handling:
    enabled: true

    # Conflict rules for specific files
    conflict-rules:
      - path: "CLAUDE.md"
        type: file
        on-conflict:
          action: append  # overwrite, append, prepend, merge-json, merge-yaml, backup, skip, prompt
          separator: "\n\n---\n\n"

      - path: ".claude"
        type: directory
        on-conflict:
          action: merge
          backup: true

      - path: ".claude/config.json"
        type: file
        on-conflict:
          action: merge-json

    # Version detection markers
    version-markers:
      - path: ".claude/config.json"
        type: file
        version: "v3"
        detection:
          method: content-match
          patterns: ["\"version\":\\s*\"3\\."]

      - path: ".claude"
        type: directory
        version: "v2"
        detection:
          method: directory-exists
          exclude-if: [".claude/config.json"]

    # Upgrade scenarios
    scenarios:
      - name: v2-to-v3-upgrade
        detected-version: "v2"
        installing-version: "v3"
        action: prompt
        message: "Detected v2 configuration. Upgrade to v3?"
        options:
          - label: "Upgrade (backup existing)"
            action: backup
            backup-suffix: ".v2-backup-{timestamp}"
          - label: "Skip v3 config"
            action: skip
```

## Validation Commands

```bash
# Validate extension
sindri extension validate my-extension

# Install extension
sindri extension install my-extension

# List extensions
sindri extension list

# Check extension status
sindri extension status my-extension

# Preview generated documentation
sindri extension docs my-extension
```

## Docs Section (Optional - Human-Written Content)

The `docs` section provides human-written content that is combined with auto-derived content
(BOM, requirements, env vars, validation) when generating documentation via `sindri extension docs <name>`.
Documentation is generated on-demand and does not require manually creating markdown files.

```yaml
docs:
  title: string           # Display name (fallback: title-case of metadata.name)
  overview: string         # Extended description (fallback: metadata.description)
  last-updated: string     # ISO date (YYYY-MM-DD)
  features:                # Key features bullet list
    - "Feature one"
    - "Feature two"
  usage:                   # Usage examples grouped by section
    - section: "Getting Started"
      examples:
        - description: "Check version"
          code: "mytool --version"
          language: "bash"
        - code: |
            mytool init
            mytool run
  related:                 # Related extensions
    - name: other-extension
      description: "Provides complementary tooling"
  notes: string            # Freeform notes (markdown supported)
```

| Field          | Type            | Required | Description                                     |
|----------------|-----------------|----------|-------------------------------------------------|
| `title`        | string          | No       | Display name (fallback: title-case of metadata.name) |
| `overview`     | string          | No       | Extended description (fallback: metadata.description) |
| `last-updated` | string          | No       | ISO date (YYYY-MM-DD) of last content update    |
| `features`     | array[string]   | No       | Key features as bullet points                   |
| `usage`        | array[object]   | No       | Usage examples grouped by section               |
| `usage[].section`           | string | Yes   | Section heading for the example group           |
| `usage[].examples`          | array  | Yes   | List of code examples                           |
| `usage[].examples[].description` | string | No | Description of what the example shows       |
| `usage[].examples[].code`   | string | Yes   | Code snippet                                    |
| `usage[].examples[].language` | string | No  | Language hint for syntax highlighting (default: bash) |
| `related`      | array[object]   | No       | Related extensions                              |
| `related[].name`        | string | Yes    | Extension name                                  |
| `related[].description` | string | No     | Why the extension is related                    |
| `notes`        | string          | No       | Freeform notes (markdown supported)             |

## BOM Tool Types

The `bom.tools[].type` field uses **kebab-case** values. The Rust enum uses `#[serde(rename_all = "kebab-case")]`, so multi-word variants are hyphenated.

**IMPORTANT**: Use `cli-tool`, NOT `cli`. Use `package-manager`, NOT `package-manager` shorthand.

| YAML Value | Rust Variant | Use For |
|------------|-------------|---------|
| `runtime` | `Runtime` | Language runtimes (Node.js, Python, Ruby, Java) |
| `compiler` | `Compiler` | Compilers (GCC, rustc, javac) |
| `package-manager` | `PackageManager` | Package managers (npm, pip, cargo, apt) |
| `cli-tool` | `CliTool` | CLI tools and utilities (kubectl, aws-cli, docker) |
| `library` | `Library` | Libraries and SDKs |
| `framework` | `Framework` | Frameworks (Spring, Django, Rails) |
| `database` | `Database` | Database engines (PostgreSQL, Redis, SQLite) |
| `server` | `Server` | Server software (nginx, Apache) |
| `utility` | `Utility` | System utilities and helpers |
| `application` | `Application` | Full applications |

### Type Selection Guide

- **Most extensions** should use `cli-tool` (the most common type)
- **Language extensions** (nodejs, python, ruby): use `runtime` for the language, `package-manager` for its package manager
- **MCP servers**: use `server`
- **AI agents/tools**: use `cli-tool` (they are CLI tools, not applications)

### Common Mistakes

| Wrong | Correct | Why |
|-------|---------|-----|
| `type: cli` | `type: cli-tool` | `cli` is not a valid variant |
| `type: tool` | `type: cli-tool` | `tool` is not a valid variant |
| `type: package_manager` | `type: package-manager` | Must use kebab-case (hyphens, not underscores) |
| `type: CLI-Tool` | `type: cli-tool` | Must be lowercase |

## Common V3 Patterns

### Language Runtime

```yaml
metadata:
  name: nodejs
  version: 1.0.0
  description: Node.js LTS runtime
  category: languages  # V3 uses 'languages' not 'language'

install:
  method: mise
  mise:
    configFile: mise.toml

validate:
  commands:
    - name: node
      expectedPattern: "v\\d+\\.\\d+\\.\\d+"

bom:
  tools:
    - name: node
      version: dynamic
      source: mise
      type: runtime
      license: MIT
```

### CLI Tool (e.g., AI coding assistant)

```yaml
metadata:
  name: kilo
  version: 1.0.0
  description: AI coding assistant CLI
  category: ai-dev
  dependencies: [mise-config, nodejs]

install:
  method: mise
  mise:
    configFile: mise.toml
    reshimAfterInstall: true

validate:
  commands:
    - name: kilo
      versionFlag: --version
      expectedPattern: "\\d+\\.\\d+\\.\\d+"

bom:
  # NOTE: Versions researched 2026-02-16
  tools:
    - name: kilo
      version: "1.0.21"
      source: mise
      type: cli-tool       # NOT 'cli' - must be 'cli-tool'
      license: Apache-2.0
      homepage: https://kilo.ai
      purl: pkg:npm/%40kilocode/cli@1.0.21
```

### MCP Server Extension

```yaml
metadata:
  name: my-mcp
  version: 1.0.0
  description: MCP server for service integration
  category: mcp

install:
  method: npm-global
  npm:
    package: "@myorg/mcp-server@latest"

validate:
  commands:
    - name: my-mcp
      expectedPattern: "\\d+\\.\\d+"

capabilities:
  mcp:
    enabled: true
    server:
      command: "my-mcp"
      args: ["serve"]
    tools:
      - name: "service-query"
        description: "Query service data"
```

### AI Agent Tool with Full Capabilities

```yaml
metadata:
  name: claude-flow-v3
  version: 3.0.0
  description: Multi-agent orchestration with 10x performance
  category: ai-agents
  dependencies: [nodejs]

install:
  method: mise
  mise:
    configFile: mise.toml

configure:
  environment:
    - key: CF_SWARM_TOPOLOGY
      value: "hierarchical-mesh"
      scope: bashrc

capabilities:
  project-init:
    enabled: true
    priority: 50
    commands:
      - command: "claude-flow init --full"
        description: "Initialize Claude Flow v3"
        requiresAuth: anthropic

  auth:
    provider: anthropic
    methods: [api-key, cli-auth]
    features:
      - name: agent-spawn
        requiresApiKey: false
        description: "CLI features"

  hooks:
    post-install:
      command: "claude-flow doctor --check"
    post-project-init:
      command: "claude-flow status"

  mcp:
    enabled: true
    server:
      command: "npx"
      args: ["-y", "@claude-flow/cli@alpha", "mcp", "start"]
    tools:
      - name: "agent-spawn"
        description: "Spawn agents"
      - name: "swarm-coordinate"
        description: "Coordinate swarms"

  collision-handling:
    enabled: true
    conflict-rules:
      - path: ".claude"
        type: directory
        on-conflict:
          action: merge
          backup: true

  project-context:
    enabled: true
    mergeFile:
      source: templates/SKILL.md
      target: CLAUDE.md
      strategy: append-if-missing
```

## V3-Specific Notes

1. **Extension Discovery**: V3 auto-discovers extensions from `v3/extensions/` directory, but `v3/registry.yaml` must be maintained for registry listing
2. **Rust Validation**: V3 uses native Rust schema validation (faster, stricter)
3. **Enhanced Binary Downloads**: Supports GitHub release asset patterns
4. **GPU Requirements**: First-class GPU specification for AI workloads
5. **Collision Handling**: Smart conflict resolution for cloned projects
6. **Project Context**: Automatic CLAUDE.md file management
7. **Generated Docs**: Extension documentation is generated on-demand via `sindri extension docs <name>` combining human-written `docs` section content with auto-derived data from the extension YAML

## Post-Extension Checklist

After creating an extension:

1. **Preview docs**: Run `sindri extension docs <name>` to preview generated documentation
2. **Catalog**: `v3/docs/EXTENSIONS.md` (add to category table + extension list)
3. **Registry**: `v3/registry.yaml` (add alphabetically under correct category)
4. **Test locally**: `sindri extension install {name} && sindri extension status {name}`

### Registry Entry Format

Add to `v3/registry.yaml` under the appropriate category section (alphabetically):

```yaml
extensions:
  # Category Section (e.g., # MCP Servers)
  your-extension:
    category: "mcp"
    description: "Brief description matching extension.yaml"
```

## Compatibility Matrix Management

When creating or modifying extensions, you MUST also update the compatibility matrix at `v3/compatibility-matrix.yaml`.

### When to Update

- **New extension created** - add entry to all applicable CLI version sections
- **Extension version bumped** - update semver range if the new version falls outside existing range
- **Extension removed** - remove entry from all CLI version sections

### How to Add a New Extension

1. Read `v3/compatibility-matrix.yaml`
2. Read the new extension's `extension.yaml` to get `metadata.version` and `metadata.category`
3. Add an entry under `compatible_extensions` in each CLI version section, placed alphabetically within the correct category comment group
4. Use semver range format: `">=X.Y.Z,<NEXT_MAJOR.0.0"`

#### Entry Format

```yaml
compatible_extensions:
  # Category Comment (e.g., # MCP Servers)
  my-extension: ">=1.0.0,<2.0.0"
```

#### Determining the Category Comment Group

Map extension `metadata.category` to the matrix comment groups:

| Extension Category | Matrix Comment Group |
|-------------------|---------------------|
| `ai-agents`, `ai-dev` | `# AI & Agentic Tools` |
| `claude` | `# Claude Ecosystem` |
| `cloud` | `# Cloud & Infrastructure` |
| `devops` | `# DevOps & Tools` |
| `mcp` | `# MCP Servers` |
| `languages` | `# Language extensions` |
| `desktop` | `# Desktop & UI` |
| `testing` | `# Testing` |
| `documentation` | `# Documentation & Content` |
| `productivity`, `research` | `# Productivity` |

#### Example: Adding `notebooklm-mcp-cli` (category: mcp, version: 1.0.0)

In the `3.0.x` section, under `# MCP Servers`:
```yaml
      notebooklm-mcp-cli: ">=1.0.0,<2.0.0"
```

In the `3.1.x` section, under `# MCP Servers`:
```yaml
      notebooklm-mcp-cli: ">=1.1.0,<2.0.0"
```

In the `4.0.x` section, under `# MCP Servers`:
```yaml
      notebooklm-mcp-cli: ">=2.0.0,<3.0.0"
```

### Version Range Rules

| CLI Series | Range Pattern | Notes |
|-----------|---------------|-------|
| `3.0.x` | `>=CURRENT,<NEXT_MAJOR` | Use the extension's current `metadata.version` |
| `3.1.x` | `>=CURRENT_MINOR_BUMP,<NEXT_MAJOR` | Bump minor version (e.g., 1.0.0 -> 1.1.0) |
| `4.0.x` | `>=NEXT_MAJOR,<NEXT_NEXT_MAJOR` | Use next major version (e.g., 1.x -> 2.0.0) |

### Validation

After updating, verify:
- Entries are alphabetically sorted within their category group
- All three CLI version sections have an entry for the new extension
- Semver ranges are valid (use `>=` and `<` operators)
- No duplicate entries exist

## Extension Version Upgrade

When a user asks to upgrade an extension's software versions, follow this introspection-and-research workflow.

### Trigger Phrases

- "upgrade extension X", "update versions for X", "check for newer versions in X"
- "refresh versions", "bump versions", "update cloud-tools versions"

### Step 1: Introspect the Extension

Read the extension directory to identify all version sources:

| Version Source | Where to Look | Example |
|---------------|---------------|---------|
| **versions.env** | `v3/extensions/{name}/versions.env` | `AWS_VERSION="2.33.21"` |
| **mise.toml** | `v3/extensions/{name}/mise.toml` | `python = "3.13"` |
| **extension.yaml BOM** | `bom.tools[].version` in `extension.yaml` | `version: "2.33.21"` |
| **extension.yaml binary** | `install.binary.downloads[].source.version` | `version: "v1.2.3"` |
| **install scripts** | `v3/extensions/{name}/scripts/install.sh` | Hardcoded version variables or download URLs |
| **npm package** | `install.npm.package` | `"@scope/pkg@1.2.3"` |

Build a **version inventory** - a list of every software component and its current pinned version.

Example inventory for `cloud-tools`:
```
aws-cli:     2.33.21  (versions.env: AWS_VERSION, bom)
azure-cli:   2.83.0   (versions.env: AZURE_CLI_VERSION, bom)
gcloud:      556.0.0  (versions.env: GCLOUD_VERSION, bom)
flyctl:      0.4.11   (versions.env: FLYCTL_VERSION, bom)
aliyun-cli:  3.2.9    (versions.env: ALIYUN_VERSION, bom)
doctl:       1.150.0  (versions.env: DOCTL_VERSION, bom)
ibmcloud:    2.41.1   (versions.env: IBM_VERSION, bom)
```

### Step 2: Research Latest Versions

For each component in the inventory, use **WebSearch** to find the latest stable release version:

**Search strategies by tool type:**

| Tool Type | Search Query Template | Authoritative Sources |
|-----------|----------------------|----------------------|
| GitHub-hosted CLI | `"{tool-name} latest release site:github.com"` | GitHub releases page |
| Language runtime | `"{language} latest stable version {year}"` | Official language site |
| Cloud CLI | `"{cloud} CLI latest version {year}"` | Cloud provider docs |
| npm package | `"{package-name} npm latest version"` | npmjs.com |
| pip package | `"{package-name} pypi latest version"` | pypi.org |
| Cargo crate | `"{crate-name} crates.io latest"` | crates.io |

**Key rules:**
- Only consider **stable** releases (no alpha, beta, RC, nightly, dev)
- For GitHub releases, use `gh api repos/{owner}/{repo}/releases/latest` via Bash when possible (faster and more reliable than web search)
- Skip tools with `version: dynamic` or `version: lts` (these resolve at install time)
- Include the current year in search queries for freshness

### Step 3: Compare Versions

For each component, determine if the latest version is newer:

**Semver comparison** (most tools): Compare major.minor.patch numerically
- `2.33.21` vs `2.35.0` -> newer (minor bump)
- `0.4.11` vs `0.4.15` -> newer (patch bump)
- `3.2.9` vs `3.2.9` -> same (skip)

**Date-based versions** (e.g., Google Cloud SDK `556.0.0`): Compare as integers
- `556.0.0` vs `563.0.0` -> newer

**Symbolic versions** (e.g., `lts`, `latest`): Skip - these auto-resolve

### Step 4: Apply Updates

For each component with a newer version available, update ALL locations where the version appears:

#### 4a. Update `versions.env`
```bash
# Before
AWS_VERSION="2.33.21"
# After
AWS_VERSION="2.35.0"
```
Also update the `# Updated:` date comment at the top of the file.

#### 4b. Update `mise.toml`
```toml
# Before
[tools]
python = "3.13"
# After
[tools]
python = "3.14"
```

#### 4c. Update `extension.yaml` BOM entries
```yaml
bom:
  tools:
    - name: aws
      version: "2.35.0"      # Updated from 2.33.21
      purl: pkg:generic/awscli@2.35.0    # Update version in purl too
      cpe: cpe:2.3:a:amazon:aws_cli:2.35.0:*:*:*:*:*:*:*  # Update CPE if present
```

#### 4d. Update install scripts (if versions are hardcoded)
Search for the old version string in `scripts/install.sh` and replace with the new version.

#### 4e. Update npm package version (if pinned)
```yaml
install:
  method: npm-global
  npm:
    package: "@scope/package@2.0.0"  # Updated from 1.5.0
```

#### 4f. Update `bom` comment date
```yaml
bom:
  # NOTE: Versions researched YYYY-MM-DD
```

#### 4g. Update `docs.last-updated`
```yaml
docs:
  last-updated: "YYYY-MM-DD"
```

### Step 5: Bump Extension Version and Update References

After updating software versions, bump the extension's own `metadata.version`:
- **Patch bump** (e.g., 2.1.0 -> 2.1.1): Only patch-level software updates
- **Minor bump** (e.g., 2.1.0 -> 2.2.0): Minor or mixed software version updates
- **Major bump** (e.g., 2.1.0 -> 3.0.0): Major software version update (e.g., Python 3.x -> 4.x)

Then update all external references to the extension version:

1. **`v3/docs/EXTENSIONS.md`** - Update the version number shown in the extensions catalog
2. **`v3/compatibility-matrix.yaml`** - Ensure the new version falls within the semver range; if not, update the range (see [Compatibility Matrix Management](#compatibility-matrix-management))
3. **`v3/registry.yaml`** - Update description if the extension's capabilities changed

### Step 6: Report Changes

Present a summary table to the user:

```
Extension: cloud-tools (2.1.0 -> 2.2.0)

| Component    | Old Version | New Version | Change Type |
|-------------|-------------|-------------|-------------|
| aws-cli     | 2.33.21     | 2.35.0      | minor       |
| azure-cli   | 2.83.0      | 2.84.0      | minor       |
| gcloud      | 556.0.0     | 563.0.0     | minor       |
| flyctl      | 0.4.11      | 0.4.11      | (current)   |
| aliyun-cli  | 3.2.9       | 3.2.9       | (current)   |
| doctl       | 1.150.0     | 1.152.0     | minor       |
| ibmcloud    | 2.41.1      | 2.41.1      | (current)   |

Files modified:
- v3/extensions/cloud-tools/versions.env
- v3/extensions/cloud-tools/extension.yaml (bom + metadata.version)
- v3/docs/EXTENSIONS.md (version reference updated)
- v3/compatibility-matrix.yaml (if version range needed adjustment)
```

### Skipping Upgrades

Some version types should NOT be upgraded automatically:
- `version: dynamic` - resolved at install time
- `version: lts` - symbolic, always resolves to latest LTS
- `version: latest` - always resolves to latest
- Tools where the extension description explicitly states a specific major version constraint (e.g., "Python 3.x runtime" should not jump to Python 4.x)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Invalid category | Use V3 categories (ai-agents, languages, etc.) |
| Binary download fails | Check GitHub asset pattern |
| Collision not detected | Verify version-markers paths |
| MCP not registering | Check server command and args |
| GPU validation fails | Ensure proper CUDA setup |
| Missing from compat matrix | Run through [Compatibility Matrix Management](#compatibility-matrix-management) |
| Version upgrade missed a file | Check all locations: versions.env, mise.toml, bom, scripts, purl, cpe |

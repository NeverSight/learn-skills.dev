---
name: orchestrate-multi-target-sdks
description: >-
  Use when generating SDKs for multiple languages from a single OpenAPI spec, or
  multiple SDK variants from different sources. Covers workflow.yaml multi-target
  configuration, per-language gen.yaml, monorepo structure.
  Triggers on "multiple SDKs", "multi-language SDK", "SDK for each language",
  "multi-target SDK", "SDK monorepo", "generate SDKs for".
license: Apache-2.0
---

# Orchestrate Multi-Target SDKs

Generate SDKs for multiple languages or variants from a single repository using CLI commands.

## When to Use

- Generating SDKs for multiple languages from the same API spec
- Creating SDK variants (Azure, GCP, regional) from different specs
- Setting up an SDK monorepo
- User says: "generate SDKs for multiple languages", "SDK for each language", "multi-target"

## Quick Start: Multiple Languages

**Always use CLI commands.** Never create `.speakeasy` directories manually.

```bash
# Step 1: Initialize first target (creates .speakeasy/workflow.yaml)
speakeasy quickstart --skip-interactive --output console \
  -s openapi.yaml -t typescript -n "MySDK" -p "my-sdk"

# Step 2: Add more language targets using configure
speakeasy configure targets \
  --target-type python \
  --source my-source \
  --output ./sdks/python

speakeasy configure targets \
  --target-type go \
  --source my-source \
  --output ./sdks/go

# Step 3: Generate all SDKs
speakeasy run --output console
```

## CLI Reference

### `speakeasy configure sources`

Add a new OpenAPI source to an existing workflow:

```bash
speakeasy configure sources \
  --location ./openapi.yaml \
  --source-name my-api

# With authentication header
speakeasy configure sources \
  --location https://api.example.com/openapi.yaml \
  --source-name my-api \
  --auth-header "Authorization"
```

| Flag | Short | Description |
|------|-------|-------------|
| `--location` | `-l` | OpenAPI document location (file or URL) |
| `--source-name` | `-s` | Name for the source |
| `--auth-header` | | Authentication header name (optional) |
| `--output` | `-o` | Output path for compiled source (optional) |
| `--non-interactive` | | Force non-interactive mode |

### `speakeasy configure targets`

Add a new SDK target to an existing workflow:

```bash
speakeasy configure targets \
  --target-type typescript \
  --source my-api \
  --output ./sdks/typescript

# With all options
speakeasy configure targets \
  --target-type go \
  --source my-api \
  --target-name my-go-sdk \
  --sdk-class-name MyAPI \
  --package-name github.com/myorg/myapi-go \
  --output ./sdks/go
```

| Flag | Short | Description |
|------|-------|-------------|
| `--target-type` | `-t` | Language: typescript, python, go, java, csharp, php, ruby, terraform |
| `--source` | `-s` | Name of source to generate from |
| `--target-name` | | Name for the target (defaults to target-type) |
| `--sdk-class-name` | | SDK class name (optional) |
| `--package-name` | | Package name (optional) |
| `--base-server-url` | | Base server URL (optional) |
| `--output` | `-o` | Output directory (optional) |
| `--non-interactive` | | Force non-interactive mode |

## Example: Multi-Language SDKs

Single OpenAPI spec → TypeScript, Python, Go SDKs:

```bash
# Initialize with first target
speakeasy quickstart --skip-interactive --output console \
  -s ./openapi.yaml -t typescript -n "MySDK" -p "my-sdk" -o ./sdks/typescript

# Add Python
speakeasy configure targets \
  --target-type python \
  --source my-source \
  --sdk-class-name MySDK \
  --package-name my-sdk \
  --output ./sdks/python

# Add Go
speakeasy configure targets \
  --target-type go \
  --source my-source \
  --sdk-class-name MySDK \
  --package-name github.com/myorg/my-sdk-go \
  --output ./sdks/go

# Generate all
speakeasy run --output console
```

## Example: SDK Variants (Multiple Sources)

Different OpenAPI specs → variant SDKs:

```bash
# Initialize with main API
speakeasy quickstart --skip-interactive --output console \
  -s ./openapi.yaml -t typescript -n "MySDK" -p "my-sdk"

# Add Azure variant source
speakeasy configure sources \
  --location ./openapi-azure.yaml \
  --source-name azure-api

# Add Azure target
speakeasy configure targets \
  --target-type typescript \
  --source azure-api \
  --target-name typescript-azure \
  --sdk-class-name MySDKAzure \
  --package-name "@myorg/my-sdk-azure" \
  --output ./packages/azure

# Generate all
speakeasy run --output console
```

## Repository Structure

```
my-api-sdks/
├── openapi.yaml              # Source spec
├── .speakeasy/
│   └── workflow.yaml         # Multi-target config (created by CLI)
├── sdks/
│   ├── typescript/
│   │   ├── .speakeasy/
│   │   │   └── gen.yaml      # Created by configure
│   │   └── src/
│   ├── python/
│   │   ├── .speakeasy/
│   │   │   └── gen.yaml
│   │   └── src/
│   └── go/
│       ├── .speakeasy/
│       │   └── gen.yaml
│       └── go.mod
└── .github/workflows/
    └── sdk_generation.yaml
```

## Running Generation

```bash
# Generate all targets
speakeasy run --output console

# Generate specific target only
speakeasy run -t typescript --output console
speakeasy run -t python --output console
```

## CI Workflow

```yaml
# .github/workflows/sdk_generation.yaml
name: Generate SDKs
on:
  push:
    branches: [main]
    paths: ['openapi.yaml']
  workflow_dispatch:

jobs:
  generate:
    uses: speakeasy-api/sdk-generation-action/.github/workflows/workflow-executor.yaml@v15
    with:
      mode: pr
    secrets:
      github_access_token: ${{ secrets.GITHUB_TOKEN }}
      speakeasy_api_key: ${{ secrets.SPEAKEASY_API_KEY }}
```

## What NOT to Do

- **Do NOT create `.speakeasy/` directories manually** - Use `speakeasy quickstart` and `speakeasy configure`
- **Do NOT write `workflow.yaml` or `gen.yaml` files directly** - Use CLI commands
- **Do NOT copy `.speakeasy/` directories between projects** - Each needs its own config

### Incorrect

```bash
# WRONG: Do not do this
mkdir -p .speakeasy
cat > .speakeasy/workflow.yaml << 'EOF'
...
EOF
```

### Correct

```bash
# RIGHT: Use CLI commands
speakeasy quickstart --skip-interactive --output console \
  -s openapi.yaml -t typescript -n "MySDK" -p "my-sdk"

speakeasy configure targets --target-type python --source my-source
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong target generated | Specify `-t target-name` in `speakeasy run` |
| Source not found | Run `speakeasy configure sources` to add it |
| Target not found | Run `speakeasy configure targets` to add it |
| Config out of sync | Run `speakeasy run` to regenerate |

## After Making Changes

After adding sources or targets, regenerate:

```bash
speakeasy run --output console
```

## After Making Changes

After modifying workflow.yaml or per-target gen.yaml, **prompt the user** to regenerate the SDK(s):

> **Configuration complete.** Would you like to regenerate the SDK(s) now with `speakeasy run`?

If the user confirms, run:

```bash
# Generate all targets
speakeasy run --output console

# Or generate a specific target
speakeasy run -t <target-name> --output console
```

Changes to workflow.yaml and gen.yaml only take effect after regeneration.

## Related Skills

- `start-new-sdk-project` - Initial SDK setup for single target
- `configure-sdk-options` - Language-specific gen.yaml options
- `manage-openapi-overlays` - Spec customization with overlays
- `orchestrate-multi-repo-sdks` - Separate repository per language

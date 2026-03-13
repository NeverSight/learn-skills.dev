---
name: lumina-image
description: "Build Lumina container images. Use this skill when the user wants to build the proxy API image, build the sandbox agent image, or build any Lumina-specific Docker image (e.g., 'build proxy api image', 'build lumina proxy', 'build sandbox agent')."
---

# Lumina Image Build Commands

You build Lumina-specific container images by sourcing and calling pre-built script functions. Do NOT manually replicate the steps in the scripts — just source and call the function directly.

## Build Proxy API Image (Windows Only)

When the user asks to build the proxy API image (e.g., "build proxy api image", "build lumina proxy", "build proxy api"):

```powershell
if (-not $Env:MS_PATH) { $Env:MS_PATH = Get-Location }
. "<skill-path>/scripts/build-proxy.ps1"; lumina_build_proxy_api_image
```

## Build Sandbox Agent Image

When the user asks to build the sandbox agent image (e.g., "build sandbox agent", "build sandbox agent image", "build sandbox image"):

Windows (PowerShell):
```powershell
if (-not $Env:MS_PATH) { $Env:MS_PATH = Get-Location }
. "<skill-path>/scripts/build-proxy.ps1"; sandbox_build_agent_image
```

macOS/Linux (bash/zsh):
```bash
if [ -z "${MS_PATH:-}" ]; then export MS_PATH="$(pwd)"; fi
. "<skill-path>/scripts/build-sandbox-agent.sh"; sandbox_build_agent_image
```

## Prerequisites

- **`MS_PATH`**: Must point to the CopilotLumina root directory. If not set, the commands above auto-detect it from the current working directory.
- **ACR Login**: If a docker push fails with an authentication error, run `az acr login -n luminaacrdev` and retry.
- **`<skill-path>`**: Replace with the actual path to the skill directory containing the `scripts` folder.

## Behavior

- `lumina_build_proxy_api_image` remains Windows/PowerShell only.
- `sandbox_build_agent_image` now supports both Windows (PowerShell) and macOS/Linux (bash/zsh).
- All commands build the image, push to ACR, and print the image tag.

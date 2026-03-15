---
name: devcontainer
description: |
    Use when configuring dev containers or GitHub Codespaces. Covers devcontainer.json schema, features, lifecycle hooks, port forwarding, and customizations.
    USE FOR: devcontainer.json configuration, GitHub Codespaces setup, lifecycle hooks, port forwarding, VS Code customizations, dev container features
    DO NOT USE FOR: specific language setup (use the sub-skills: dotnet, python, typescript), Docker-in-Docker configuration (use docker-in-docker), sidecar services (use multi-container-workspaces)
license: MIT
metadata:
  displayName: "Dev Containers"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Dev Containers Specification"
    url: "https://containers.dev/"
  - title: "Dev Containers — GitHub Repository"
    url: "https://github.com/devcontainers/spec"
  - title: "VS Code — Developing Inside a Container"
    url: "https://code.visualstudio.com/docs/devcontainers/containers"
---

# Dev Containers

## Overview
Dev containers define reproducible development environments using a `devcontainer.json` file. They are the foundation of GitHub Codespaces and work with VS Code Dev Containers, the devcontainer CLI, and DevPod.

## File Location
Place `devcontainer.json` in one of:
- `.devcontainer/devcontainer.json` (preferred)
- `.devcontainer.json` (repo root)
- `.devcontainer/<folder>/devcontainer.json` (multiple configs)

## Minimal Configuration
```jsonc
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "forwardPorts": [3000],
  "postCreateCommand": "npm install"
}
```

## Base Image Options
| Image | Use Case |
|-------|----------|
| `mcr.microsoft.com/devcontainers/base:ubuntu` | General-purpose |
| `mcr.microsoft.com/devcontainers/javascript-node:22` | Node.js / TypeScript |
| `mcr.microsoft.com/devcontainers/python:3.12` | Python |
| `mcr.microsoft.com/devcontainers/dotnet:9.0` | .NET |
| `mcr.microsoft.com/devcontainers/universal:2` | Multi-language (Codespaces default) |

## Features
Features install additional tools without custom Dockerfiles:
```jsonc
{
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/node:1": { "version": "22" },
    "ghcr.io/devcontainers/features/python:1": { "version": "3.12" },
    "ghcr.io/devcontainers/features/go:1": { "version": "1.24" },
    "ghcr.io/devcontainers/features/github-cli:1": {}
  }
}
```

## Lifecycle Hooks
Hooks run at different stages. Each can be a string, array, or object (parallel commands):
```jsonc
{
  // Runs on host before container creation
  "initializeCommand": "echo 'Starting build'",

  // Runs once after container is created
  "onCreateCommand": {
    "deps": "npm ci",
    "db": "npm run db:setup"
  },

  // Runs when new content is available (rebuild / prebuilt update)
  "updateContentCommand": "npm install",

  // Runs after onCreateCommand and updateContentCommand complete
  "postCreateCommand": "npm run build",

  // Runs every time the container starts
  "postStartCommand": {
    "server": "npm run dev",
    "watch": "npm run watch"
  },

  // Runs every time an editor attaches
  "postAttachCommand": "echo 'Ready'",

  // Which command to wait for before showing as ready
  "waitFor": "postCreateCommand"
}
```

## Port Forwarding
```jsonc
{
  "forwardPorts": [3000, 5432, 6379],
  "portsAttributes": {
    "3000": {
      "label": "Application",
      "onAutoForward": "openBrowser"
    },
    "5432": {
      "label": "Database",
      "onAutoForward": "silent"
    }
  }
}
```

## Environment Variables
```jsonc
{
  // Available in all processes inside the container
  "containerEnv": {
    "MY_VAR": "value"
  },
  // Available only in the integrated terminal / remote connection
  "remoteEnv": {
    "DATABASE_URL": "postgresql://user:pass@db:5432/mydb"
  },
  // User-level environment
  "remoteUser": "vscode"
}
```

## VS Code Customizations
```jsonc
{
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-dotnettools.csdevkit"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
      }
    }
  }
}
```

## Using a Dockerfile
```jsonc
{
  "build": {
    "dockerfile": "Dockerfile",
    "context": "..",
    "args": {
      "VARIANT": "22-bookworm"
    }
  }
}
```

## Best Practices
- Prefer features over custom Dockerfiles for common tools — they compose well and cache independently.
- Use `postCreateCommand` for project-specific setup (dependency install, migrations) and `postStartCommand` for starting dev servers.
- Pin feature versions with major version tags (e.g., `:2`) rather than `:latest`.
- Use `containerEnv` for build-time variables and `remoteEnv` for secrets or connection strings.
- Enable Codespaces prebuilds to cache `postCreateCommand` results and speed up start times.
- Use `"shutdownAction": "stopCompose"` with Docker Compose setups to clean up sidecar containers.
- Keep `.devcontainer/` in version control so every contributor gets the same environment.

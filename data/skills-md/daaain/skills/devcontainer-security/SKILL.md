---
name: devcontainer-security
description: Guide for setting up secured VS Code dev containers for coding agents. Use when creating or hardening a DevContainer to sandbox Claude Code or other coding agents, configuring Docker socket proxies, handling VS Code IPC escape vectors, setting up git worktree support, or verifying security controls. Covers threat model, three-layer defence architecture, Node.js/pnpm setup, and verification testing.
metadata:
  version: 1.1.0
---

# Secured VS Code Dev Containers for Coding Agents

Set up a hardened VS Code DevContainer that sandboxes coding agents while maintaining full development capability.

## When to Use This Skill

- Setting up a new DevContainer for coding agent use
- Hardening an existing DevContainer against escape vectors
- Adding git worktree support for parallel development
- Setting up sibling Docker services (databases, emulators)
- Verifying security controls are working
- Setting up Node.js / pnpm in a DevContainer

## Threat Model

We're protecting against three things:

1. **Supply chain attacks** - malicious npm packages executing code during install or at runtime
2. **Prompt injection** - malicious content convincing the agent to run harmful commands
3. **Agent mistakes** - unintentional destructive actions

The goal is to **limit blast radius**, not eliminate all risk.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  Host Machine                   │
│  ┌───────────────────────────────────────────┐  │
│  │              Docker Engine                │  │
│  │  ┌──────────────┐  ┌──────────────────┐   │  │
│  │  │ docker-proxy │◄─│  claude-code     │   │  │
│  │  │ (read-only)  │  │  (DevContainer)  │   │  │
│  │  └──────┬───────┘  └──────────────────┘   │  │
│  │         ▼                                 │  │
│  │  ┌──────────────┐                         │  │
│  │  │ Docker Socket│                         │  │
│  │  └──────────────┘                         │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Security Controls Summary

| Control | What It Blocks | How |
|---------|---------------|-----|
| Docker socket proxy | Container escape | Read-only API proxy (POST=0, EXEC=0) |
| No sudo | Privilege escalation | Not installed in image |
| Drop all capabilities | Kernel attack surface | `cap_drop: [ALL]` in docker-compose.yml |
| No new privileges | Setuid/setgid escalation | `security_opt: no-new-privileges:true` |
| No SSH keys | Git push / code exfil | Keys not mounted, agent socket deleted |
| VS Code IPC hardening | Host command execution | Three-layer env var + socket cleanup |
| No credential injection | Docker/git credential leaks | VS Code settings disabled |

## Documentation Index

| Document | Contents |
|----------|----------|
| **[SECURITY-HARDENING.md](SECURITY-HARDENING.md)** | Three-layer defence against VS Code escape vectors, the `.bashrc` non-interactive shell subtlety |
| **[DOCKER-PROXY.md](DOCKER-PROXY.md)** | Docker socket proxy setup, sibling container communication |
| **[NODE-SETUP.md](NODE-SETUP.md)** | Node.js + pnpm Dockerfile patterns, startup commands |
| **[WORKTREE-SUPPORT.md](WORKTREE-SUPPORT.md)** | Git worktree support, dynamic container naming, isolated volumes |
| **[VERIFICATION.md](VERIFICATION.md)** | How to verify security controls, integration testing with devcontainers-cli, automated test scripts |

## Quick Start — Minimal Secured DevContainer

Three files are needed. See each sub-document for detailed explanations.

**`.devcontainer/devcontainer.json`**:

```json
{
  "name": "Secured Dev Container",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/app",
  "remoteUser": "vscode",
  "shutdownAction": "stopCompose",
  "remoteEnv": {
    "SSH_AUTH_SOCK": "",
    "GPG_AGENT_INFO": "",
    "BROWSER": "",
    "VSCODE_IPC_HOOK_CLI": null,
    "VSCODE_GIT_IPC_HANDLE": null,
    "GIT_ASKPASS": null,
    "VSCODE_GIT_ASKPASS_MAIN": null,
    "VSCODE_GIT_ASKPASS_NODE": null,
    "VSCODE_GIT_ASKPASS_EXTRA_ARGS": null,
    "REMOTE_CONTAINERS_IPC": null,
    "REMOTE_CONTAINERS_SOCKETS": null,
    "REMOTE_CONTAINERS_DISPLAY_SOCK": null,
    "WAYLAND_DISPLAY": null
  },
  // postStartCommand: clean up sockets created before VS Code attaches
  "postStartCommand": "find /tmp -maxdepth 2 \\( -name 'vscode-ssh-auth-*.sock' -o -name 'vscode-remote-containers-ipc-*.sock' -o -name 'vscode-remote-containers-*.js' \\) -delete 2>/dev/null || true",
  // IPC socket cleanup (vscode-ipc-*.sock, vscode-git-*.sock) is handled by a background
  // loop in the Docker Compose command — postAttachCommand is unreliable for background
  // processes due to VS Code's cgroup-based lifecycle cleanup. See SECURITY-HARDENING.md.
  "customizations": {
    "vscode": {
      "settings": {
        "dev.containers.dockerCredentialHelper": false,
        "dev.containers.copyGitConfig": false
      }
    }
  }
}
```

**`.devcontainer/docker-compose.yml`**: See [DOCKER-PROXY.md](DOCKER-PROXY.md).

**`.devcontainer/Dockerfile`**: See [NODE-SETUP.md](NODE-SETUP.md) or adapt for your language.

## Accepted Risks

These are trade-offs for development usability:

| Risk | Why Accepted |
|------|--------------|
| Network egress (data exfiltration) | Development requires internet access |
| Workspace write access | Essential for development; git tracks changes |
| Agent credentials readable | Token is revocable; limited blast radius |
| Environment variables (.env) | Development requires env vars, no production keys |

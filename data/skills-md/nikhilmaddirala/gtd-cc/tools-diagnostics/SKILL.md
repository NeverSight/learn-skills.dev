---
name: tools-diagnostics
description: Interactive system resource analysis and troubleshooting for memory, disk, CPU, and performance issues
---

# System diagnostics

## Overview

Interactive skill for diagnosing system resource issues. Detects OS and applies appropriate diagnostic patterns. Focuses on real-world lessons from production incidents rather than generic command documentation.

## Context

Expects a Unix-like system (Linux or macOS). User describes a resource problem (memory, disk, CPU, or general slowness).

## Process

1. **Detect platform**: `uname -s` (Linux or Darwin)
2. **Identify problem type**: memory, disk, CPU, or I/O
3. **Run targeted diagnostics** using platform-appropriate commands
4. **Apply cleanup patterns** from references for Nix-aware environments
5. **Verify**: confirm resource pressure reduced

## References

- **macos-disk-cleanup-learnings-2026-02-17.md**: moondancer cleanup runbook, Determinate Nix GC behavior, safety tiers
- **nix-gc-determinate-seasmoke-learnings-2026-02-17.md**: Nix store root retention, profile generation pruning, container storage
- **system-cleanup-report-20260117-reference.md**: High-impact cleanup operations with space recovered

## Guidelines

- Use `sudo` for accurate disk usage on Linux (non-root `du` under-reports)
- On macOS with Determinate Nix, `nix.gc.automatic` is disabled by policy - use explicit `nix-collect-garbage -d`
- Clean caches first (low risk, high value): trash, browser caches, package manager caches
- Prune Nix profile generations on all users, not just system
- Check container storage (`/var/lib/containers`, rootless storage) as disk pressure source

## Quick reference

**Assess state:**
```bash
df -h / /nix                          # disk usage
du -sh ~/.Trash ~/.cache ~/Library/Caches /nix/store 2>/dev/null  # top consumers
```

**Safe cleanup (macOS):**
```bash
rm -rf ~/.Trash/*
rm -rf ~/Library/Caches/*
uv cache clean && brew cleanup --prune=all
nix-collect-garbage -d
```

**Safe cleanup (Linux, as root):**
```bash
sudo du -xhd 1 / | sort -hr | head -20  # find top consumers
sudo nix-collect-garbage -d
sudo nix-store --gc
sudo podman system prune --volumes -f   # if containers present
```

## Appendix

### Determinate Nix GC behavior

When `determinateNix.enable = true` on macOS hosts, nix-darwin's `nix.gc` module is disabled. Determinate Nixd handles GC policy instead. Do not assume timer-based GC is running.

Reference: `dragonix/modules/base/nix-settings/darwin.nix`

### Nix root retention patterns

Large Nix store after GC usually means:
- Old profile generations still rooted under `~/.local/state/nix/profiles/`
- Running processes holding `/proc` roots
- Solution: prune all user profiles, not just system

```bash
# Per-user profile pruning
nix-env -p ~/.local/state/nix/profiles/profile --delete-generations old
nix-env -p ~/.local/state/nix/profiles/home-manager --delete-generations old
```

### Safety tiers

Low risk, high value: trash, caches, `uv cache clean`, `brew cleanup`
Medium risk with verification: `nix-collect-garbage -d`, playwright cache, mediaanalysisd
Do not delete: `/System`, `/usr`, `/bin`, `/sbin`, APFS system volumes, app databases

---
name: project-structure
description: Navigate the nix-config repository layout and find files
---

# Project Structure

## Directory Layout

```
flake.nix           # Top-level flake definitions
flake/
  dev/              # Development shell, CI scripts, formatting
  ci/               # CI-specific flake and scripts
  home-manager/     # Home-Manager flake module
  nixos/            # NixOS flake module

modules/            # Reusable module fragments
  home-manager/     # Home-Manager specific modules
  nixos/            # NixOS specific modules

lib/                # Shared Nix functions and helpers
  builders/         # System and home builders (mkSystem, mkHome)

overlays/           # Nixpkgs overlays
pkgs/               # Custom packages and package sets

hosts/              # Per-machine NixOS configurations
  shared/
    global/         # Applied to ALL hosts
    optional/       # Optional features (gaming, containers, etc.)
  desktop/          # Desktop machines
    shared/         # Shared across all desktops
    <machine>/      # Machine-specific config
  laptop/           # Laptop machines
    shared/
  server/           # Server machines
    shared/
    <machine>/

home/               # User-specific Home-Manager configurations
  shared/           # Shared across all users
    global/         # Applied to all users
    applications/   # Application configs
    desktop/        # Desktop environment configs
    features/       # Feature modules (cli, etc.)
  <user>/           # User-specific configs
    <machine>.nix   # Machine-specific overrides
    os-config.nix   # OS config applied to all machines
    hm-config.nix   # Home-Manager entry point

docs/               # Project documentation
```

## Key Files

| File | Purpose |
|------|---------|
| `flake.nix` | Flake inputs and outputs |
| `flake.lock` | Locked input versions |
| `.sops.yaml` | SOPS encryption rules |
| `state.version` | NixOS state version |
| `lib/builders/mkSystem.nix` | Host system builder |
| `lib/builders/home/mkHome.nix` | Home configuration builder |
| `modules/nixos/default.nix` | NixOS module exports |
| `modules/home-manager/default.nix` | Home-Manager module exports |
| `pkgs/default.nix` | Custom package registry |
| `overlays/default.nix` | Overlay definitions |

## Finding Things

- **Host config**: `hosts/<type>/<hostname>/default.nix`
- **User config**: `home/<username>/hm-config.nix`
- **User on host**: `home/<username>/<hostname>.nix`
- **NixOS module**: `modules/nixos/<category>/<name>.nix`
- **HM module**: `modules/home-manager/<category>/<name>.nix`
- **Custom package**: `pkgs/<package-name>/default.nix`
- **Secrets**: `hosts/<type>/<hostname>/secrets.yaml` or `home/<user>/secrets.yaml`

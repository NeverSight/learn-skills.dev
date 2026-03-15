---
name: nix
description: Comprehensive NixOS, Nix Flakes, Home Manager, and nix-darwin skill. Covers declarative system configuration, reproducible environments, package management, and cross-platform Nix workflows. Activate for any Nix/NixOS/Flakes/Home-Manager/nix-darwin tasks.
---

# Nix Ecosystem Guide

## Core Philosophy

1. **Declarative over Imperative** - Describe desired state, not steps to reach it
2. **Reproducibility** - Lock files (`flake.lock`) pin exact versions
3. **Immutability** - Nix Store is read-only; same inputs = same outputs
4. **Rollback (NixOS)** - Every generation preserved; instant recovery via boot menu

## Flake Structure

```nix
{
  description = "My Nix configuration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    home-manager = {
      url = "github:nix-community/home-manager/release-24.11";
      inputs.nixpkgs.follows = "nixpkgs";  # CRITICAL: avoid duplicate nixpkgs
    };
    # macOS support
    nix-darwin = {
      url = "github:nix-darwin/nix-darwin/nix-darwin-24.11";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, home-manager, nix-darwin, ... }@inputs: {
    # NixOS configurations
    nixosConfigurations.hostname = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [ ./configuration.nix ];
    };

    # macOS configurations
    darwinConfigurations.hostname = nix-darwin.lib.darwinSystem {
      system = "aarch64-darwin";  # or x86_64-darwin for Intel
      modules = [ ./darwin.nix ];
    };

    # Development shells
    devShells.x86_64-linux.default = nixpkgs.legacyPackages.x86_64-linux.mkShell {
      packages = [ /* ... */ ];
    };
  };
}
```

## Essential Patterns

### Input Management
```nix
inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  unstable.url = "github:NixOS/nixpkgs/nixos-unstable";

  # Use parent's nixpkgs to avoid downloading multiple versions
  home-manager.inputs.nixpkgs.follows = "nixpkgs";

  # Non-flake input (config files, etc.)
  private-config = {
    url = "git+ssh://git@github.com/user/config.git";
    flake = false;
  };
};
```

### Module System
```nix
# Modules have: imports, options, config
{ config, pkgs, lib, ... }: {
  imports = [ ./hardware.nix ./services.nix ];

  options.myOption = lib.mkOption {
    type = lib.types.bool;
    default = false;
  };

  config = lib.mkIf config.myOption {
    # conditional configuration
  };
}
```

### Priority Control
```nix
{
  # lib.mkDefault (priority 1000) - base module defaults
  services.nginx.enable = lib.mkDefault true;

  # Direct assignment (priority 100) - normal config
  services.nginx.enable = true;

  # lib.mkForce (priority 50) - override everything
  services.nginx.enable = lib.mkForce false;
}
```

### Package Customization
```nix
{
  # Override function arguments
  pkgs.fcitx5-rime.override { rimeDataPkgs = [ ./custom-rime ]; }

  # Override derivation attributes
  pkgs.hello.overrideAttrs (old: { doCheck = false; })

  # Overlays (global modification)
  nixpkgs.overlays = [
    (final: prev: {
      myPackage = prev.myPackage.override { /* ... */ };
    })
  ];
}
```

## Platform-Specific

### NixOS
```bash
sudo nixos-rebuild switch --flake .#hostname
sudo nixos-rebuild boot --flake .#hostname    # apply on next boot
sudo nixos-rebuild test --flake .#hostname    # test without boot entry
```

### nix-darwin (macOS)
```bash
darwin-rebuild switch --flake .#hostname
# TouchID for sudo:
# security.pam.services.sudo_local.touchIdAuth = true;
```

### Home Manager
```nix
# As NixOS/Darwin module:
home-manager.useGlobalPkgs = true;
home-manager.useUserPackages = true;
home-manager.users.username = import ./home.nix;

# Standalone:
home-manager switch --flake .#username@hostname
```

## Commands Reference

| Task | Command |
|------|---------|
| Rebuild NixOS | `sudo nixos-rebuild switch --flake .#hostname` |
| Rebuild Darwin | `darwin-rebuild switch --flake .#hostname` |
| Dev shell | `nix develop` |
| Temp package | `nix shell nixpkgs#package` |
| Run package | `nix run nixpkgs#package` |
| Update all | `nix flake update` |
| Update one | `nix flake update nixpkgs` |
| GC old gens | `sudo nix-collect-garbage -d` |
| List gens | `nix profile history --profile /nix/var/nix/profiles/system` |
| Debug build | `nixos-rebuild switch --show-trace -L -v` |
| REPL | `nix repl` then `:lf .` to load flake |

## Common Gotchas

1. **Untracked files ignored** - `git add` before any flake command (nix build/run/shell/develop, nixos-rebuild, darwin-rebuild)
2. **allowUnfree fails in devShells** - Use `nixpkgs-unfree` overlay or `~/.config/nixpkgs/config.nix`
3. **Duplicate input downloads** - Use `follows` to pin dependencies (most common: `inputs.nixpkgs.follows`)
4. **Python pip fails** - Use `venv`, `poetry2nix`, or containers
5. **Downloaded binaries fail** - Use FHS environment or `nix-ld`
6. **Merge conflicts in lists** - Use `lib.mkBefore`/`lib.mkAfter` for ordering
7. **Build from source unexpectedly** - Check if overlays invalidate cache

## Development Environments

```nix
# In flake.nix outputs:
devShells.x86_64-linux.default = pkgs.mkShell {
  packages = with pkgs; [ nodejs python3 rustc ];

  shellHook = ''
    echo "Dev environment ready"
    export MY_VAR="value"
  '';

  # For C libraries
  LD_LIBRARY_PATH = lib.makeLibraryPath [ pkgs.openssl ];
};
```

### direnv Integration
```bash
# .envrc
use flake
# or for unfree: use flake --impure
```

## Debugging

```bash
# Verbose rebuild
nixos-rebuild switch --show-trace --print-build-logs --verbose

# Interactive REPL
nix repl
:lf .                    # load current flake
:e pkgs.hello           # open in editor
:b pkgs.hello           # build derivation
inputs.<TAB>            # explore inputs
```

## References

For detailed information, see:
- `references/nix-language.md` - Nix language syntax
- `references/flakes.md` - Flake inputs/outputs details
- `references/home-manager.md` - User environment management
- `references/nix-darwin.md` - macOS configuration
- `references/nixpkgs-advanced.md` - Overlays, overrides, callPackage
- `references/dev-environments.md` - Dev shells, direnv, FHS
- `references/best-practices.md` - Modularization, debugging, deployment
- `references/templates.md` - Ready-to-use flake.nix examples

---
name: building
description: Build and evaluate NixOS and Home-Manager configurations
---

# Building

## Build Commands

| Command | Purpose |
|---------|---------|
| `nix build .#nixosConfigurations.<host>.config.system.build.toplevel` | Build a host's NixOS system |
| `nix build .#homeConfigurations.<user>@<host>.activationPackage` | Build a Home-Manager activation |
| `nix fmt` | Format code and check syntax |
| `nix flake check` | Evaluate all configurations and run linters |
| `nix flake show` | Display available outputs |
| `nix develop` | Open development shell |
| `nix develop --command true` | Test that devShell can be entered |

## DevEnv Requirement

This repository uses `devenv` for devShells and checks. You **must** provide the `devenv-root` input override for `nix flake check` and `nix develop`:

```bash
nix flake check --override-input devenv-root "file+file://$PWD/.devenv/root"

nix develop --override-input devenv-root "file+file://$PWD/.devenv/root"
```

## Common Build Patterns

### Build a specific host

```bash
# Build nixdev server
nix build .#nixosConfigurations.nixdev.config.system.build.toplevel

# Build nixmi desktop
nix build .#nixosConfigurations.nixmi.config.system.build.toplevel
```

### Build a user's home configuration

```bash
# Build racci's config on nixmi
nix build .#homeConfigurations."racci@nixmi".activationPackage
```

### Evaluate without building

```bash
# Check if configuration evaluates
nix eval .#nixosConfigurations.nixdev.config.system.build.toplevel --apply 'x: "ok"'

# Get a specific option value
nix eval .#nixosConfigurations.nixdev.config.networking.hostName
```

### Format specific files

```bash
# Format changed files
nix fmt path/to/file.nix

# Format multiple files
nix fmt modules/nixos/services/*.nix
```

## Troubleshooting Builds

If a build fails:

1. Check the error message for the failing derivation
2. Try `nix log <drv>` to see build logs
3. Use `--show-trace` for evaluation errors: `nix build .#... --show-trace`
4. For infinite recursion, check for circular imports or option definitions

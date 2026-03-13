---
name: nixkil
description: Agent skill for Nix language programming, Nix package manager, and NixOS
---

# nixkil

Agent skill for Nix language programming, Nix package manager, and NixOS.

## CLI Commands

This skill provides knowledge and guidance for working with Nix. Use the standard Nix CLI tools directly via shell commands.

### Package Management

```bash
# Search for packages
nix search nixpkgs <query>
nix search nixpkgs python --json  # JSON output for parsing

# Get package info
nix eval nixpkgs#<package>.meta --json

# Run a package without installing
nix run nixpkgs#<package> -- [args]

# Enter a shell with packages
nix shell nixpkgs#pkg1 nixpkgs#pkg2

# Build a package
nix build nixpkgs#<package>
```

### Flake Operations

```bash
# Initialize a new flake
nix flake init
nix flake init --template templates#<name>

# Show flake outputs
nix flake show [flake-ref]
nix flake show --json  # JSON output

# Check/validate a flake
nix flake check [flake-ref]

# Update flake inputs
nix flake update [flake-ref]
nix flake update <input-name> [flake-ref]  # Update specific input

# Show lock file info
nix flake metadata [flake-ref]
```

### NixOS Configuration

```bash
# Search NixOS options (use nixos.org/options or)
nix eval --expr 'builtins.attrNames (import <nixpkgs/nixos> {}).options'

# Rebuild system (requires sudo)
sudo nixos-rebuild switch
sudo nixos-rebuild switch --flake .#hostname
sudo nixos-rebuild test  # Test without making it default
sudo nixos-rebuild boot  # Activate on next boot

# List generations
nix-env --list-generations -p /nix/var/nix/profiles/system
```

### Language Tools

```bash
# Evaluate Nix expressions
nix eval --expr '1 + 1'
nix eval --file ./file.nix
nix eval .#someOutput --json

# Format Nix files (nixfmt or alejandra)
nix fmt  # Uses formatter from flake
nixfmt file.nix
alejandra file.nix

# Lint Nix files
statix check .
deadnix .

# Parse/validate syntax
nix-instantiate --parse file.nix
```

### Useful Flags

- `--json` - Output as JSON for parsing
- `--verbose` / `-v` - Show more details
- `--dry-run` - Show what would be done
- `--show-trace` - Show full error traces
- `--impure` - Allow impure evaluation (env vars, etc.)

## Knowledge Areas

| Area | Topics |
|------|--------|
| `nix-language` | Syntax, types, functions, builtins, derivations |
| `nixpkgs` | Package overrides, overlays, cross-compilation |
| `flakes` | Structure, inputs/outputs, commands, templates |
| `devenv` | Development environments with services and pre-commit hooks |
| `nixos` | System configuration, modules, services |
| `nix-darwin` | macOS configuration with Nix |
| `home-manager` | User environment and dotfiles management |
| `macos-linux-builder` | Building Linux packages on macOS |
| `troubleshooting` | Common errors and solutions |

## Examples

### DevShell Examples
- `examples/devshells/golang/` - Go development environment
- `examples/devshells/python/` - Python with venv and tooling
- `examples/devshells/rust/` - Rust with cargo tools
- `examples/devshells/nodejs/` - Node.js with TypeScript
- `examples/devshells/java/` - Java with Maven and Gradle
- `examples/devshells/multi-lang/` - Multiple languages in one flake

### Devenv Examples
- `examples/devenv/basic/` - Basic devenv setup
- `examples/devenv/with-services/` - PostgreSQL, Redis services
- `examples/devenv/with-precommit/` - Pre-commit hooks configuration


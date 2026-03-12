---
name: chezmoi-chef
description: Manage dotfiles and secrets with chezmoi. Use for initializing chezmoi, adding/editing configuration files, creating templates for multi-machine setups, encrypting sensitive files, integrating password managers (1Password, Bitwarden, pass, etc.), running scripts during apply, and syncing dotfiles across machines. Triggers on dotfile management, chezmoi commands, configuration templating, or secrets in config files.
---

# Chezmoi Dotfile Management

Chezmoi manages dotfiles across machines with templating, encryption, and password manager integration.

## Quick Reference

```bash
chezmoi init                    # Initialize
chezmoi add ~/.bashrc           # Add file
chezmoi add --template ~/.zshrc # Add as template
chezmoi add --encrypt ~/.secret # Add encrypted
chezmoi edit ~/.bashrc          # Edit and apply
chezmoi apply                   # Apply all changes
chezmoi diff                    # Preview changes
chezmoi update                  # Pull and apply
chezmoi cd                      # Shell in source dir
```

## Core Workflows

### Initialize on New Machine

From GitHub:
```bash
chezmoi init --apply github-username
```

One-liner install + init:
```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply github-username
```

### Add Files to Management

```bash
chezmoi add ~/.bashrc ~/.zshrc ~/.gitconfig    # Multiple files
chezmoi add -r ~/.config/nvim                  # Directory
chezmoi add --template ~/.bashrc               # As template
chezmoi add --encrypt ~/.ssh/id_rsa            # Encrypted
```

### Edit Managed Files

```bash
chezmoi edit ~/.bashrc          # Opens source file
chezmoi edit --apply ~/.bashrc  # Auto-apply after save
```

### Sync Changes

```bash
chezmoi cd                      # Enter source directory
git add . && git commit -m "update dotfiles" && git push
exit
chezmoi apply                   # Apply locally
```

Or use chezmoi's git wrapper:
```bash
chezmoi git add .
chezmoi git commit -m "update"
chezmoi git push
```

## Templating

Create machine-specific configs. See [templates.md](references/templates.md) for full guide.

Convert to template:
```bash
chezmoi add --template ~/.bashrc
# or
chezmoi chattr +template ~/.bashrc
```

Common patterns:

```bash
# OS-specific
{{ if eq .chezmoi.os "darwin" -}}
export PATH="/opt/homebrew/bin:$PATH"
{{- else if eq .chezmoi.os "linux" -}}
export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"
{{- end }}

# Hostname-specific
{{ if eq .chezmoi.hostname "work-laptop" -}}
export HTTP_PROXY="http://proxy.company.com:8080"
{{- end }}

# Distro-specific (Linux)
{{ if eq .chezmoi.osRelease.id "fedora" -}}
alias update="sudo dnf upgrade"
{{- else if eq .chezmoi.osRelease.id "ubuntu" -}}
alias update="sudo apt update && sudo apt upgrade"
{{- end }}
```

Custom variables in `~/.config/chezmoi/chezmoi.toml`:
```toml
[data]
  email = "user@example.com"
  editor = "nvim"
```

Test templates:
```bash
chezmoi execute-template '{{ .chezmoi.os }}'
chezmoi data  # Show all variables
chezmoi cat ~/.bashrc  # Show rendered output
```

## Secrets Management

Integrate password managers to avoid committing secrets. See [password-managers.md](references/password-managers.md) for all integrations.

### 1Password Example

Config (`~/.config/chezmoi/chezmoi.toml`):
```toml
[onepassword]
  command = "op"
  prompt = true
```

Template:
```bash
export GITHUB_TOKEN='{{ onepasswordRead "op://Personal/github/token" }}'
export AWS_ACCESS_KEY='{{ onepasswordRead "op://Work/aws/access-key" }}'
```

### Bitwarden Example

```bash
export API_KEY='{{ (bitwarden "item" "api-credentials").login.password }}'
```

### pass Example

```bash
export SECRET='{{ pass "path/to/secret" }}'
```

## Encryption

Encrypt sensitive files stored in source directory.

### Setup with age

```bash
chezmoi age keygen -o ~/.config/chezmoi/key.txt
```

Config:
```toml
encryption = "age"
[age]
  identity = "~/.config/chezmoi/key.txt"
  recipient = "age1..." # Public key from keygen output
```

### Add Encrypted Files

```bash
chezmoi add --encrypt ~/.ssh/id_rsa
chezmoi add --encrypt ~/.aws/credentials
```

Files stored with `encrypted_` prefix, decrypted on apply.

## Run Scripts

Execute scripts during apply for setup tasks.

Create in source directory:
```bash
chezmoi cd
```

Script naming:
- `run_once_install.sh` - Run once ever
- `run_onchange_setup.sh` - Run when script changes
- `run_always.sh` - Run every apply

Example `run_once_install-packages.sh`:
```bash
#!/bin/bash
{{ if eq .chezmoi.os "darwin" -}}
brew install ripgrep fd bat
{{- else if eq .chezmoi.osRelease.id "fedora" -}}
sudo dnf install -y ripgrep fd-find bat
{{- end }}
```

## Command Reference

See [commands.md](references/commands.md) for complete command list.

## Troubleshooting

```bash
chezmoi doctor    # Check configuration
chezmoi verify    # Verify targets match source
chezmoi diff      # See pending changes
chezmoi status    # File status overview
chezmoi --debug apply  # Verbose output
```

Reset run_once scripts:
```bash
chezmoi state delete-bucket --bucket=scriptState
```

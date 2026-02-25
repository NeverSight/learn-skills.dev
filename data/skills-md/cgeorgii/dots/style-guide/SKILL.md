---
name: style-guide
description: Coding style guidelines for NixOS, Neovim, and Git. Use when writing or formatting Nix code, Neovim config, or working with Git workflow.
user-invocable: true
---

# Style Guidelines

## NixOS/Home-Manager Style

- Use 2-space indentation in all files
- Format Nix files with `nixfmt`
- Follow functional programming patterns
- Group related settings in modules
- Use descriptive names for options
- Document non-obvious settings with comments
- When creating new files for Nix flakes, ensure they are tracked by git before testing with nix commands
  - Untracked files can cause errors like "path '/nix/store/hash-source/path/to/file' does not exist"
  - Solution: Track files without staging using `git add --intent-to-add path/to/file` or `git add -N path/to/file`

## Neovim Style

- Use Lua for all configuration
- 2-space indentation, no tabs
- Leader key is `;`
- Format with proper whitespace and bracing style
- Wrap related plugin configs in feature-based groups
- Prefer native LSP functions over plugin equivalents

## Git Workflow

- Create focused, atomic commits
- Use `hub` as git wrapper
- Use `lazygit` for interactive Git operations
- Prefer rebase over merge for linear history
- Do not include co-authored by Claude information in commits
- Git config location: `~/.config/git/config`
- Credential storage: git-credential-manager with GPG backend
  - Initialize pass: `pass init YOUR_GPG_KEY_ID`
  - Credentials stored securely with GPG encryption

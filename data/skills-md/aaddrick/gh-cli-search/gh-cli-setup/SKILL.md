---
name: gh-cli-setup
description: Use when gh CLI is not installed, not configured, or authentication fails - provides installation steps, authentication methods, and troubleshooting for all platforms
---

# GitHub CLI Setup & Troubleshooting

## Overview

This skill helps diagnose and fix GitHub CLI (`gh`) installation, configuration, and authentication issues.

**IMPORTANT: When providing installation instructions, always:**
- Explain the recommended method (e.g., "Homebrew is the recommended way to install on macOS")
- Provide the actual command
- Mention alternative installation methods
- Add context about what the command does
- Do NOT just return a bare command without explanation

## When to Use

Use this skill when:
- `gh` command not found
- Authentication errors occur
- gh CLI behaves unexpectedly
- Need to check gh CLI configuration
- Setting up gh CLI for first time

## Quick Diagnostic

Run these commands to check status:

```bash
# Check if gh is installed
which gh

# Check gh version
gh --version

# Check authentication status
gh auth status

# List authenticated accounts
gh auth status --show-token
```

## Installation

### macOS

**Using Homebrew (recommended):**
```bash
brew install gh
```

**Using MacPorts:**
```bash
sudo port install gh
```

**Using Conda:**
```bash
conda install gh --channel conda-forge
```

### Linux

**Debian/Ubuntu/Raspbian:**
```bash
# Add GitHub CLI repository
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Install
sudo apt update
sudo apt install gh -y
```

**Fedora/CentOS/RHEL:**
```bash
sudo dnf install gh
```

**Arch Linux:**
```bash
sudo pacman -S github-cli
```

**Using Snap:**
```bash
sudo snap install gh
```

**Using Conda:**
```bash
conda install gh --channel conda-forge
```

### Windows

**Using WinGet:**
```powershell
winget install --id GitHub.cli
```

**Using Scoop:**
```powershell
scoop install gh
```

**Using Chocolatey:**
```powershell
choco install gh
```

**Using Conda:**
```bash
conda install gh --channel conda-forge
```

**Manual Download:**
- Download MSI installer from: https://cli.github.com/

## Authentication

### Interactive Authentication (Recommended)

```bash
gh auth login
```

This will prompt you to:
1. Choose GitHub.com or GitHub Enterprise Server
2. Choose authentication method (Web browser or Token)
3. Complete authentication flow

### Token Authentication

```bash
# Create token at: https://github.com/settings/tokens
# Required scopes: repo, read:org, workflow

# Authenticate with token
gh auth login --with-token < token.txt

# Or paste token when prompted
gh auth login
```

### Check Authentication

```bash
# Verify authentication status
gh auth status

# View authenticated user
gh api user --jq '.login'

# Test API access
gh api rate_limit
```

## Common Errors & Solutions

### Error: "gh: command not found"

**Cause:** gh CLI not installed or not in PATH

**Solution:**
```bash
# Check if gh is installed
which gh

# If not found, install (see Installation section above)

# If installed but not in PATH, add to PATH
# For bash/zsh, add to ~/.bashrc or ~/.zshrc:
export PATH="/path/to/gh/bin:$PATH"
```

### Error: "authentication required"

**Cause:** Not logged in to GitHub

**Solution:**
```bash
# Login interactively
gh auth login

# Or check authentication status
gh auth status
```

### Error: "HTTP 403: Resource not accessible by integration"

**Cause:** Insufficient token permissions

**Solution:**
```bash
# Re-authenticate with proper scopes
gh auth login --scopes repo,read:org,workflow

# Or create new token with required scopes:
# https://github.com/settings/tokens
```

### Error: "HTTP 401: Bad credentials"

**Cause:** Token expired or invalid

**Solution:**
```bash
# Logout and re-authenticate
gh auth logout
gh auth login
```

### Error: "API rate limit exceeded"

**Cause:** Too many API requests (60/hour unauthenticated, 5000/hour authenticated)

**Solution:**
```bash
# Check rate limit status
gh api rate_limit

# Authenticate to get higher limit (if not already)
gh auth login

# Wait for rate limit reset or use different account
```

### Error: "Could not resolve host: github.com"

**Cause:** Network connectivity issue

**Solution:**
```bash
# Check internet connection
ping github.com

# Check proxy settings if behind corporate firewall
gh config set http_proxy http://proxy.example.com:8080

# Check DNS resolution
nslookup github.com
```

## Configuration

### View Configuration

```bash
# View all config settings
gh config list

# View specific setting
gh config get git_protocol
```

### Common Settings

```bash
# Set default protocol (https or ssh)
gh config set git_protocol https

# Set default editor
gh config set editor vim

# Set default browser
gh config set browser firefox

# Set proxy
gh config set http_proxy http://proxy.example.com:8080

# Set GitHub Enterprise host
gh config set host github.enterprise.com
```

### Config File Locations

- **Linux/macOS:** `~/.config/gh/config.yml`
- **Windows:** `%AppData%\GitHub CLI\config.yml`

## Multiple Accounts

```bash
# Login to multiple hosts
gh auth login --hostname github.com
gh auth login --hostname github.enterprise.com

# Switch between accounts
gh auth switch

# Check which account is active
gh auth status
```

## Debugging

### Enable Debug Mode

```bash
# Run command with debug output
GH_DEBUG=api gh search repos "test"

# Or for all commands
export GH_DEBUG=api
```

### View Request/Response

```bash
# See HTTP requests and responses
gh api repos/owner/repo --verbose
```

### Check Version

```bash
# View gh version
gh --version

# Check for updates
gh extension upgrade --all
```

## Troubleshooting Checklist

When gh CLI isn't working, check these in order:

- [ ] Is gh installed? (`which gh`)
- [ ] Is gh in PATH? (`echo $PATH` | grep gh)
- [ ] Is gh authenticated? (`gh auth status`)
- [ ] Does token have required scopes?
- [ ] Is network connectivity working? (`ping github.com`)
- [ ] Is rate limit exceeded? (`gh api rate_limit`)
- [ ] Is gh version up to date? (`gh --version`)
- [ ] Are config settings correct? (`gh config list`)

## Getting Help

```bash
# Get help for any command
gh help
gh search --help
gh search repos --help

# View manual online
# https://cli.github.com/manual/
```

## Permissions Required for Search

Different search types require different permissions:

- **Public repos/issues/PRs:** No authentication required (but rate limited)
- **Private repos:** Requires `repo` scope
- **Organization repos:** Requires `read:org` scope
- **Workflow files:** Requires `workflow` scope

## Token Scopes

Create tokens at: https://github.com/settings/tokens

**Minimal scopes for search:**
- `public_repo` - Search public repositories
- `repo` - Search private repositories
- `read:org` - Search organization repositories

**Recommended scopes:**
- `repo` - Full repository access
- `read:org` - Organization access
- `workflow` - Workflow access
- `gist` - Gist access

## Uninstallation

### macOS

```bash
brew uninstall gh
```

### Linux

```bash
# Debian/Ubuntu
sudo apt remove gh

# Fedora/CentOS/RHEL
sudo dnf remove gh

# Arch
sudo pacman -R github-cli
```

### Windows

```powershell
# WinGet
winget uninstall GitHub.cli

# Scoop
scoop uninstall gh

# Chocolatey
choco uninstall gh
```

## Related

- Official documentation: https://cli.github.com/manual/
- Installation guide: https://github.com/cli/cli#installation
- Authentication guide: https://cli.github.com/manual/gh_auth_login
- For using gh search: `gh-search-code`, `gh-search-commits`, `gh-search-issues`, `gh-search-prs`, `gh-search-repos`

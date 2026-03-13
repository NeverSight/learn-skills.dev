---
name: go-installer
description: Install and verify the Go toolchain on macOS, Linux, and Windows. Use when Go is required but not present, or when a specific Go version must be installed. Prefer system package managers (homebrew, apt, etc.) and fall back to official Go downloads when needed.
---

# Go Installer

Install or verify the Go toolchain with system package managers first, then fall back to official Go downloads when needed.

## Path Convention

Canonical install and execution directory: `~/.agents/skills/go-installer/`. Run commands from this directory:

```bash
cd ~/.agents/skills/go-installer
```

## Quick workflow

1. Check whether Go is already installed.
2. If missing, install via OS package manager (preferred).
3. If package manager is unavailable or the required version is not available, install from the official Go downloads.
4. Ensure `PATH` is updated and confirm `go version`.

## Verify

```bash
go version
```

If the command is missing, continue to installation.

## Install via package manager (preferred)

macOS (Homebrew):

```bash
brew install go
```

Linux (Debian/Ubuntu apt):

```bash
sudo apt update
sudo apt install -y golang-go
```

Linux (Fedora/RHEL/CentOS dnf):

```bash
sudo dnf install -y golang
```

Linux (RHEL/CentOS yum):

```bash
sudo yum install -y golang
```

Linux (Arch pacman):

```bash
sudo pacman -S --noconfirm go
```

Windows (winget):

```powershell
winget install --id GoLang.Go -e
```

Windows (Chocolatey):

```powershell
choco install -y golang
```

## Install from official Go downloads (fallback)

Use this when a specific version is required or no package manager is available.

Set the version explicitly (example uses Go 1.22.0):

```bash
GO_VER="go1.22.0"
```

### macOS (tar.gz, user dir)

```bash
GO_VER="go1.22.0"
ARCH="$(uname -m)"
case "${ARCH}" in
  arm64) GO_ARCH="arm64" ;;
  x86_64) GO_ARCH="amd64" ;;
  *) echo "Unsupported arch: ${ARCH}"; exit 1 ;;
esac

TAR="${GO_VER}.darwin-${GO_ARCH}.tar.gz"
if command -v curl >/dev/null 2>&1; then
  curl -LO "https://go.dev/dl/${TAR}"
else
  wget -O "${TAR}" "https://go.dev/dl/${TAR}"
fi

rm -rf "${HOME}/.local/go"
mkdir -p "${HOME}/.local"
tar -C "${HOME}/.local" -xzf "${TAR}"
```

### Linux (tar.gz, user dir)

```bash
GO_VER="go1.22.0"
ARCH="$(uname -m)"
case "${ARCH}" in
  aarch64) GO_ARCH="arm64" ;;
  x86_64) GO_ARCH="amd64" ;;
  *) echo "Unsupported arch: ${ARCH}"; exit 1 ;;
esac

TAR="${GO_VER}.linux-${GO_ARCH}.tar.gz"
if command -v curl >/dev/null 2>&1; then
  curl -LO "https://go.dev/dl/${TAR}"
else
  wget -O "${TAR}" "https://go.dev/dl/${TAR}"
fi

rm -rf "${HOME}/.local/go"
mkdir -p "${HOME}/.local"
tar -C "${HOME}/.local" -xzf "${TAR}"
```

### Windows (.zip)

```powershell
$GoVer = "go1.22.0"
$Arch = $env:PROCESSOR_ARCHITECTURE
switch ($Arch) {
  "ARM64" { $GoArch = "arm64" }
  "AMD64" { $GoArch = "amd64" }
  default { throw "Unsupported arch: $Arch" }
}

$Zip = "$GoVer.windows-$GoArch.zip"
Invoke-WebRequest -Uri "https://go.dev/dl/$Zip" -OutFile $Zip
if (Test-Path C:\Go) { Remove-Item -Recurse -Force C:\Go }
tar -C C:\ -xf $Zip
```

## PATH updates

macOS/Linux (add to shell profile):

```bash
export PATH="$PATH:${HOME}/.local/go/bin"
```

Windows:

- Add `C:\Go\bin` to the system `PATH`.

## Post-check

```bash
go version
```

If the version still does not match, ensure the `PATH` order is correct and restart the shell.

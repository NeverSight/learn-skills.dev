---
name: ssh-remote
description: |
  SSH remote access patterns and secure shell utilities. Covers connections, config management, key generation (Ed25519, FIDO2), tunneling, port forwarding, file transfers, and multiplexing.

  Use when connecting to servers, managing SSH keys, setting up tunnels, transferring files over SSH, configuring jump hosts, or hardening SSH access.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# SSH Remote Access

## Overview

SSH (Secure Shell) provides encrypted remote access, file transfer, and tunneling over untrusted networks. OpenSSH is the standard implementation on Linux, macOS, and Windows (via built-in client). The client configuration lives at `~/.ssh/config` and supports per-host settings, identity management, and connection reuse.

**When to use:** Remote server management, secure file transfers, port forwarding, jump host traversal, automated deployments, SOCKS proxying.

**When NOT to use:** High-throughput bulk data transfer across WANs (use Globus or similar), GUI-heavy remote desktop (use VNC/RDP), container orchestration (use kubectl/docker CLI).

## Quick Reference

| Pattern           | Command / Directive                      | Key Points                             |
| ----------------- | ---------------------------------------- | -------------------------------------- |
| Basic connect     | `ssh user@host`                          | Add `-p PORT` for non-default port     |
| Identity file     | `ssh -i ~/.ssh/key user@host`            | Specify private key explicitly         |
| Remote command    | `ssh user@host "command"`                | Add `-t` for interactive commands      |
| SSH config alias  | `Host myserver` block in `~/.ssh/config` | Simplifies repeated connections        |
| File copy (rsync) | `rsync -avzP src user@host:dest`         | Preferred over scp for all transfers   |
| File copy (scp)   | `scp file user@host:path`                | Legacy protocol; uses SFTP internally  |
| Local tunnel      | `ssh -L local:remote_host:remote_port`   | Access remote services locally         |
| Remote tunnel     | `ssh -R remote:localhost:local_port`     | Expose local services to remote        |
| SOCKS proxy       | `ssh -D 1080 user@host`                  | Dynamic port forwarding                |
| Jump host         | `ssh -J jump user@target`                | ProxyJump, available since OpenSSH 7.3 |
| Key generation    | `ssh-keygen -t ed25519`                  | Ed25519 recommended for all new keys   |
| FIDO2 key         | `ssh-keygen -t ed25519-sk`               | Hardware-backed, requires OpenSSH 8.2+ |
| Agent             | `ssh-add ~/.ssh/key`                     | Cache key passphrase for session       |
| Multiplexing      | `ControlMaster auto` in config           | Reuse TCP connections across sessions  |
| Debug             | `ssh -v user@host`                       | Up to `-vvv` for maximum verbosity     |

## Key Type Recommendations

| Algorithm          | Recommendation                     | Notes                                                     |
| ------------------ | ---------------------------------- | --------------------------------------------------------- |
| Ed25519            | Default for all new keys           | 256-bit, fast, secure, supported on OpenSSH 6.5+          |
| Ed25519-SK (FIDO2) | Strongest option with hardware key | Requires physical security key, OpenSSH 8.2+              |
| RSA 4096           | Legacy compatibility only          | Use only when Ed25519 is unsupported by the remote system |
| ECDSA              | Avoid                              | Implementation concerns; prefer Ed25519                   |

## File Transfer Decision Guide

| Scenario                             | Tool                       | Why                                       |
| ------------------------------------ | -------------------------- | ----------------------------------------- |
| Recurring syncs or large directories | `rsync -avzP`              | Delta sync, compression, resume, progress |
| Quick one-off file copy              | `scp` or `rsync`           | scp is simpler; rsync is more capable     |
| Interactive file browsing            | `sftp`                     | Tab completion, directory navigation      |
| High-bandwidth WAN transfers         | Specialized tools (Globus) | SSH buffer limits reduce WAN throughput   |

## Common Mistakes

| Mistake                                          | Correct Pattern                                                             |
| ------------------------------------------------ | --------------------------------------------------------------------------- |
| Using RSA keys for new setups                    | Generate Ed25519 keys -- faster, smaller, and equally secure                |
| Using `scp` for large or recurring transfers     | Use `rsync -avzP` for compression, progress, and resumable delta sync       |
| Typing passphrase repeatedly during sessions     | Use `ssh-agent` and `ssh-add` to cache keys for the session                 |
| Connecting through multiple hops with nested SSH | Use `-J` (ProxyJump) for clean bastion/jump host traversal                  |
| Running interactive commands without `-t` flag   | Use `ssh -t user@host "htop"` to allocate a pseudo-terminal                 |
| Using `ForwardAgent yes` through untrusted hosts | Use ProxyJump instead -- agent forwarding exposes keys to compromised hosts |
| Setting `ControlPath` without `%h`, `%p`, `%r`   | Include all three tokens to ensure unique sockets per connection            |
| Disabling host key checking globally             | Only use `StrictHostKeyChecking no` in trusted, ephemeral environments      |
| Not using `IdentitiesOnly yes`                   | Prevents offering every loaded key to every server                          |

## Security Checklist

- Generate Ed25519 keys with strong passphrases
- Set `PasswordAuthentication no` on servers
- Set `PermitRootLogin prohibit-password` or `no`
- Use `IdentitiesOnly yes` in client config
- Restrict keys with `command=` and `from=` in `authorized_keys`
- Use FIDO2 hardware keys (`ed25519-sk`) for high-security environments
- Install `fail2ban` on servers to block brute-force attempts
- Consider SSH certificate authentication for fleet management

## Delegation

- **Server inventory discovery and connection testing**: Use `Explore` agent
- **Multi-host deployment or bulk file transfers**: Use `Task` agent
- **Network architecture and bastion host planning**: Use `Plan` agent

## References

- [Connections, SSH config, and remote commands](references/connections.md)
- [File transfers with rsync and scp](references/file-transfer.md)
- [Port forwarding, SOCKS proxy, and jump hosts](references/tunneling.md)
- [Key management, FIDO2 keys, agent, and security hardening](references/key-management.md)

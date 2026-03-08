---
name: using-exe-dev
description: Guides working with exe.dev VMs. Use when the user mentions exe.dev, exe VMs, *.exe.xyz, or tasks involving exe.dev infrastructure.
---

# About

exe.dev provides Linux VMs with persistent disks, instant HTTPS, and built-in auth. All management is via SSH.

## Documentation

- Docs index: https://exe.dev/docs.md
- All docs in one page (big!): https://exe.dev/docs/all.md

The index is organized for progressive discovery: start there and follow links as needed.

## Quick reference

```
ssh exe.dev help             # show commands
ssh exe.dev help <command>   # show command details
ssh exe.dev new --json       # create VM
ssh exe.dev ls --json        # list VMs
ssh exe.dev rm <vm>          # delete VM
ssh <vm>.exe.xyz             # connect to VM
scp file.txt <vm>.exe.xyz:~/ # transfer file
```

Every VM gets `https://<vm>.exe.xyz/` with automatic TLS.

## A tale of two SSH destinations

- **`ssh exe.dev <command>`** — the exe.dev lobby. A REPL for VM lifecycle, sharing, and configuration. Does not support scp, sftp, or arbitrary shell commands.
- **`ssh <vm>.exe.xyz`** — a direct connection to a VM. Full SSH: shell, scp, sftp, port forwarding, everything.

## Working in non-interactive and sandboxed environments

Coding agents often run SSH in non-interactive shells or sandboxes. Common issues and workarounds:

**scp/sftp failures**: Ensure you're targeting `<vm>.exe.xyz` rather than `exe.dev`. Use ssh-based workarounds.

**Hung connections**: Non-interactive SSH can block on host key prompts with no visible output. Use `-o StrictHostKeyChecking=accept-new` on first connection to a new VM.

**SSH config**: Check whether both destinations are configured to use the right key:

```
Host exe.dev *.exe.xyz
  IdentitiesOnly yes
  IdentityFile ~/.ssh/id_ed25519
```

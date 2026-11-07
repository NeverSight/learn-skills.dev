---
name: termux-backup
description: Create and verify a restorable snapshot of Termux home and prefix before risky changes, and restore it safely. Use when about to do a major upgrade, proot reset, Termux reinstall, or mass package change, or when asked to back up or migrate Termux. Do NOT use as a substitute for version control of project code, and do not restore over a working installation without explicit confirmation.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "medium"
  triggers: "backup termux,restore termux,migrate termux,snapshot termux,before upgrade backup,termux tar backup,reset phone,migrate phone,restore setup,save my setup"
---
# Termux Backup and Restore

## Purpose
Make a verified, restorable archive of Termux state before a risky change, and restore it only deliberately.

## When to use
- Before a large `pkg upgrade`, a proot distro reset or removal, reinstalling Termux, or a mass package change.
- When the user asks to back up, clone, or migrate a Termux setup.

## When NOT to use
- To protect project code: that belongs in git on a remote.
- To restore over a working installation without a clear reason and explicit confirmation.

## Preconditions
Run `sh scripts/estimate-backup-size.sh [target-dir]` (read-only). Decide scope: home only (small, holds your files and config) or home plus prefix (large, holds installed packages). Confirm there is room at the target and that storage access exists if the target is shared storage (`storage-permissions`).

## Decision tree
1. Home only is usually enough: packages can be reinstalled. Record the package list as text (`dpkg --get-selections`) alongside it.
2. Full backup (home and prefix) is the documented way to move or recover an entire installation. It only restores cleanly onto the same CPU architecture and the same app package id.
3. The documented method is a tar of `/data/data/com.termux/files` limited to `./home` and `./usr`, written outside the directories being archived. Run it from Termux itself.
4. Exclude regenerable caches (package caches, `node_modules`, `.cache`) when size matters, and say what was excluded.
5. The archive contains secrets (`~/.ssh`, tokens, shell history). Treat it as sensitive: do not upload it anywhere unencrypted.
6. Shared storage cannot hold Unix modes or symlinks, but a tar archive stored there keeps them inside the file. Do not extract archives on shared storage.
7. Restore is destructive: it replaces files under home and prefix. Restore only into a fresh or intentionally replaced installation, with the same flags the documentation specifies (preserve permissions, replace existing files).
8. For proot distros, prefer the distro's own backup command where the installed version has one.

## Example
- Situation: A major pkg upgrade is planned on a device holding unpushed work.
- Without the skill: Copies the home directory to /sdcard, which drops modes and symlinks, or skips the backup.
- With the skill: Archives `./home` and `./usr` with tar to a path outside both, records the package list, states what was excluded, treats the archive as secret, and verifies by listing it.

## Safety
Creating an archive writes a large file and uses storage; state size and destination first. Restoring overwrites files: name what will be replaced and get explicit confirmation. Never print archive contents beyond a name listing.

## Verification
List the archive (`tar -tzf <archive>`) and confirm expected top-level entries and non-trivial size. For a restore, take a fresh environment snapshot (`termux-environment`) afterwards and test one package and one config file.

## Rollback
A backup needs none. For a restore, keep the previous state's archive until the restored installation is verified.

## Handoffs
- `termux-environment` for architecture and free space.
- `storage-permissions` when the target is shared storage.
- `proot-boundaries` before destructive distro operations.
- `package-troubleshooting` when an upgrade is the reason for the backup.

## Report
Scope and exclusions, archive path and size, listing check result, and the one-line restore command appropriate to that archive (not run).

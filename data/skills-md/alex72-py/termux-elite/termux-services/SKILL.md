---
name: termux-services
description: Choose how to keep a program running on Termux (tmux or nohup, Termux:Boot, or termux-services with runit) and set it up with supervision and logs. Use when a server must restart after a crash, start at boot or app launch, or survive closing the terminal. Do NOT use when the process is being killed by Android (see background-processes first) or for one-off foreground commands.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "medium"
  triggers: "termux-services,termux boot,run on boot,autostart,restart on crash,sv-enable,runit,keep server running"
---
# Termux Services

## Purpose
Pick the lightest mechanism that matches the requirement (survive a closed terminal, start at boot, or be supervised and restarted) instead of defaulting to the heaviest.

## When to use
- A server or worker must keep running after the terminal closes.
- It must start when the phone boots or Termux launches.
- It must restart after a crash and keep logs.

## When NOT to use
- The process is being killed by Android: start with `background-processes`; a supervisor cannot outlive a killed Termux app.
- One-off foreground commands.

## Preconditions
Run `sh scripts/check-services.sh` (read-only). Know the exact command, working directory, port, and whether it needs the network or a wake lock.

## Decision tree
1. Only needs to survive a closed terminal session: `tmux`, `screen`, or `nohup`. No service needed.
2. Needs to start at device boot or app start: Termux:Boot, a separate app from the same distribution source as Termux. It must be opened once. Scripts go in `~/.termux/boot/`, must be executable, and should call `termux-wake-lock` when the job needs the CPU awake.
3. Needs supervision, restart on crash, or logs: `termux-services` (runit). After installing the package, restart the Termux session so the service daemon starts. Services live under `$PREFIX/var/service/<name>`; manage them with `sv-enable`, `sv-disable`, and `sv up|down|status <name>`.
4. A custom service is a directory with an executable `run` script. Run in the foreground and send stderr to stdout:
   ```sh
   #!/data/data/com.termux/files/usr/bin/sh
   exec 2>&1
   exec <command> <args>
   ```
   Never daemonize or background inside `run`; the supervisor expects the process to stay in the foreground.
5. Combine mechanisms deliberately: Termux:Boot can start the service daemon; `termux-services` supervises the program.
6. Boot-time behavior depends on battery optimization for both apps and on the vendor. Verify by rebooting, not by reasoning.

## Example
- Situation: A Node server must survive closing Termux and restart after a crash.
- Without the skill: Starts it with `nohup node server.js &`, which never restarts and loses logs.
- With the skill: Picks `termux-services`, writes a `run` script that runs the server in the foreground with `exec 2>&1`, restarts the session, and proves it with `sv status` and a kill-and-restart test.

## Safety
Enabling a service or boot script starts code unattended and can drain battery or open a network port. State what will run, with which arguments, on which port, and confirm. Never put secrets in a `run` script; read them from a file with restricted mode.

## Verification
`sv status <name>` shows `run`, the process responds on its port or check, and after killing the process once the supervisor restarts it. For boot scripts, reboot and re-check.

## Rollback
`sv-disable <name>`, remove the service directory or boot script that was created, and release any wake lock.

## Handoffs
- `background-processes` when Android kills Termux itself.
- `termux-sshd` when the service is the SSH server.
- `termux-network` when the service binds a port that other devices cannot reach.
- `termux-environment` for Android level and app sources.

## Report
Mechanism chosen and why, files created, how to stop it, and the verification result.

---
name: bedtime-device-guard
description: "Install, configure, verify, or remove a lightweight Codex bedtime guard on macOS or Windows. Use when prompts should be blocked during a local overnight window without sending schedule checks to the model; this is a Codex defense-in-depth layer, not a substitute for device, network, or emergency-access controls."
---

# Bedtime Device Guard

Use the bundled `UserPromptSubmit` hook to reject Codex prompts during a configured local-time window. The hook evaluates the clock locally, prints nothing during allowed hours, and therefore adds no model context or token usage.

This guard applies only to Codex surfaces that load and trust user hooks. Treat it as one layer alongside operating-system restrictions, scheduled shutdown, router rules, and phone controls. Do not claim it blocks another app or prevents a determined administrator from removing it.

## Device-level schedules

The optional native schedules are broader than the Codex hook and can discard unsaved work. Confirm that the user wants forced shutdown before installing them. Each scheduled action re-checks the live local window before acting, so a job released late after sleep or coalescing does nothing after the configured end time.

macOS installs three user LaunchAgents: a warning before the start, a shutdown request at the start, and a forced GUI logout two minutes later if the Mac is still running. Install or manage them with:

```bash
bash skills/bedtime-device-guard/scripts/install-device-macos.sh install \
  --start HH:MM --end HH:MM --timezone local --warning-minutes 10
bash skills/bedtime-device-guard/scripts/install-device-macos.sh verify
bash skills/bedtime-device-guard/scripts/install-device-macos.sh uninstall
```

The shutdown request uses macOS System Events and may require the user to approve Automation access once. The logout fallback is deliberately forceful and is independent of that approval.

Windows installs two per-user native Scheduled Tasks: a warning and `shutdown.exe /s /f /t 0`. Run from PowerShell:

```powershell
& skills/bedtime-device-guard/scripts/install-device-windows.ps1 install `
  -Start HH:mm -End HH:mm -Timezone local -WarningMinutes 10
& skills/bedtime-device-guard/scripts/install-device-windows.ps1 verify
& skills/bedtime-device-guard/scripts/install-device-windows.ps1 uninstall
```

Keep emergency communication on a separately constrained device; these schedules intentionally do not provide an on-computer bypass.

## Install

Choose the user's schedule and timezone at installation time. Never add personal values to this repository.

On macOS or Linux:

```bash
bash skills/bedtime-device-guard/scripts/install-macos.sh \
  --start HH:MM --end HH:MM --timezone local
```

On Windows PowerShell:

```powershell
& skills/bedtime-device-guard/scripts/install-windows.ps1 `
  --start HH:MM --end HH:MM --timezone local
```

`local` uses the computer's configured timezone and avoids an external timezone-data dependency. An IANA timezone such as `Etc/UTC` is also accepted when Python's `zoneinfo` database contains it. The installer stores the schedule only under the user's Codex home, copies the hook there, and merges one managed handler into `hooks.json` without replacing unrelated keys, events, groups, or handlers.

After installation:

1. Enable Codex hooks if needed with `codex features enable hooks`.
2. Start Codex and review/trust the new hook when prompted, or use `/hooks`.
3. Restart open Codex sessions so they reload the hook configuration.

Codex deliberately does not let an installer silently approve its own executable hook. If hooks are disabled or untrusted, this layer does not run.

## Verify

Run the non-mutating verifier for the current machine:

```bash
python3 skills/bedtime-device-guard/scripts/install_guard.py verify
```

On Windows, replace `python3` with `py -3`.

For a behavior check without waiting for bedtime, invoke the installed hook with `--now` and a local ISO timestamp. The test-only time override changes no configuration:

```bash
python3 "$HOME/.codex/bedtime-device-guard/bedtime_guard.py" \
  --config "$HOME/.codex/bedtime-device-guard/config.json" \
  --now 2030-01-01T23:00:00
```

A blocked check prints a compact JSON decision. An allowed check prints nothing.

## Update the schedule

Run the installer again with the new values. Installation is idempotent: it refreshes the managed script and configuration, then replaces only this skill's managed hook handler.

## Uninstall

On either platform, use the common installer directly:

```bash
python3 skills/bedtime-device-guard/scripts/install_guard.py uninstall
```

On Windows, replace `python3` with `py -3`. Uninstall removes only the managed handler and its now-empty matcher group, preserves all other hook configuration, and removes the skill-owned installed directory. It does not disable Codex hooks globally.

## Safety and limitations

- Back up an existing `hooks.json` before changing it and use atomic writes.
- Reject malformed times and same start/end values instead of guessing.
- Use the direct clock check as the source of truth. Do not replace it with a scheduled marker that can become stale across sleep, reboot, or missed jobs.
- Do not add a phrase-based bypass to the hook. Recovery remains possible by editing the local configuration or uninstalling from a terminal.
- Current Codex releases fail open if a hook cannot start, crashes, times out, or is not trusted. Keep stronger device-level controls independent of this hook.

Read [references/codex-hook-contract.md](references/codex-hook-contract.md) when changing the hook output or `hooks.json` structure.

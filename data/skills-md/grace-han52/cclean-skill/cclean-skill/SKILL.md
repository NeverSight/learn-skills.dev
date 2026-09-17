---
name: cclean-skill
description: Audit and safely reclaim Windows C drive space with a read-only whole-drive ledger, recursive large-folder drill-down, large-file and duplicate detection, application-cache classification, explicit batch confirmation, guarded deletion, and post-clean verification. Use when the user explicitly invokes $cclean-skill, asks what occupies C:, wants to free disk space, requests a full storage audit, or wants to decide what can be deleted without losing personal files, application state, or development environments.
---

# cclean-skill

Use a safety-first, evidence-driven workflow. Discovery is always read-only. Never infer that a large directory is disposable.

## Workflow

1. Run the whole-drive audit:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\scan-c-drive.ps1" -Mode Audit -OutputFormat Json
```

Use `-Mode Quick` only when the user asks for a fast overview. Use `-Mode DeepSystem` when the user explicitly asks to explain protected or Windows system usage. Deep mode still cannot replace elevated DISM or VSS analysis.

2. Run cleanup-candidate discovery:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\find-cleanup-candidates.ps1" -Mode Audit -OutputFormat Json
```

3. Reconcile the results:

- Report physical total, used, and free space.
- Show the major root-level ledger.
- Separate visible logical size from protected/unattributed space.
- Warn that Windows hard links can make `WinSxS` and `System32` overlap.
- Drill down until each large area has a recognizable owner or is explicitly marked unknown.
- Read [references/decision-matrix.md](references/decision-matrix.md) when classifying candidates.

4. Present candidates in four groups:

- regenerable cache or crash diagnostics;
- installed-software cleanup or uninstall;
- personal/cloud/chat data requiring a user decision;
- forbidden manual deletion.

For every candidate include exact path or file group, size, evidence, what may be lost, whether it can be regenerated, required app closures, risk, and the preferred cleanup method.

5. Create one exact batch plan after the user chooses targets. Ask once for confirmation of that batch. A new target requires a new confirmation.

6. Use the guarded executor only after explicit approval:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill-dir>\scripts\invoke-approved-cleanup.ps1" `
  -PlanPath "<utf8-json-plan>" `
  -Execute `
  -ConfirmationToken "DELETE-APPROVED-TARGETS"
```

Run it without `-Execute` first when the plan is complex or includes medium-risk targets.

7. Verify after cleanup:

- confirm every target is empty or absent as intended;
- confirm every named keep-copy or current version still exists;
- report physical free space before and after;
- report both target bytes removed and actual disk free-space increase;
- disclose failures, locked files, and whether deletion bypassed the Recycle Bin.

## Non-Negotiable Safety Rules

- Never delete during scanning or candidate discovery.
- Never directly delete broad roots, whole profiles, whole `AppData`, personal-library roots, `Program Files`, `ProgramData`, or Windows system roots.
- Never manually delete `WinSxS`, `Windows\Installer`, `ProgramData\Package Cache`, `pagefile.sys`, `swapfile.sys`, or `hiberfil.sys`.
- Never treat `.conda\envs`, `.venv`, `node_modules`, project folders, model files, or package installations as cache.
- Explain that pip/npm caches are download caches, not installed dependencies. Preserve them when the user values offline rebuilds.
- Run `conda clean --all --dry-run --json` before recommending Conda cleanup. A large `.conda\pkgs` directory is not sufficient evidence.
- Prefer app-native storage cleanup for chat, cloud-sync, browser, IDE, WPS, and vendor-managed data.
- Hash suspected duplicates before proposing deletion. Keep at least one verified copy unless the user explicitly approves deleting all copies.
- Do not force-close an app with a visible window. Ask the user to save work and exit it.
- Do not traverse or recursively delete through reparse points or junctions.
- Treat direct deletion as bypassing the Recycle Bin and disclose that consequence.

## Batch Confirmation

Before execution, state:

- exact targets and modes (`File`, `Contents`, or narrowly approved `Whole`);
- estimated total size;
- evidence supporting each target;
- data or diagnostics that will be lost;
- apps that must be closed;
- exact copies or current versions that will remain.

Proceed only after the user clearly approves the listed batch. Broad instructions such as “clean everything” require a new exact batch proposal.

## Administrator-Only System Analysis

If protected usage remains unexplained, ask the user to run these read-only commands in an elevated terminal and provide the output:

```powershell
Dism.exe /Online /Cleanup-Image /AnalyzeComponentStore
vssadmin list shadowstorage
```

Do not recommend `StartComponentCleanup`, restore-point deletion, hibernation changes, or virtual-memory changes until their tradeoffs are explained and separately confirmed.

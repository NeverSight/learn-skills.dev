---
name: windows-cleanup
description: "Diagnose why a Windows PC feels slower and cautiously reclaim storage or reduce avoidable startup and background load with supported Windows tools. Explicit invocation only; use when the user names $windows-cleanup for Windows 11 or legacy Windows 10 slowdown, low system-drive space, sluggish boot or sign-in, high background activity, or inspection and cleanup of temporary files, startup apps, unused apps, cloud-local files, update components, or drives. Do not use for registry optimization, broad debloating, privacy hardening, active malware incident response, hardware repair, boot recovery, or Windows reset and reinstallation."
---

# Windows Cleanup

Find the measured cause of a slowdown before trying to clean it. Keep assessment
read-only, preview exact targets and consequences, execute within applicable
authority using supported Windows mechanisms, and verify the result.

When invoked without a narrower symptom or requested action, default to a
read-only orientation and baseline: identify the Windows version and management
status, ask when the PC feels slow and what improvement would count as success,
then collect the lightweight evidence in **Establish the baseline**. Do not start
a scan, intensive diagnostic, cleanup, configuration change, or restart. Stop
after reporting the findings and an itemized plan that awaits confirmation.

## Preserve the safety boundary

- Treat Windows 11 as the primary target. On Windows 10, support the applicable
  diagnostic and cleanup surfaces. Identify the edition, servicing channel, and
  current update or Extended Security Updates status before characterizing its
  lifecycle. State that free support for ordinary Windows 10 editions ended on
  October 14, 2025, while enrolled ESU devices and some LTSC editions have
  different security-update timelines. Cleanup cannot change that lifecycle.
- Reuse the current request, earlier authorization, and delegated choices. A
  specific requested action may proceed after verification without another user
  turn. A broad “clean this PC” leaves deletion and configuration choices
  unresolved; inspect and propose them unless the user delegated those choices.
  Keep every target and effect within that authority.
- Work without elevation for discovery. Elevate only the authorized operation
  that requires it, immediately before execution. Never disable UAC or run the
  whole workflow elevated.
- Preserve user data, credentials, security controls, backup and sync software,
  VPNs, accessibility tools, hardware-support services, restore points, and
  rollback options unless applicable specific authority covers a justified change.
- Never install or run a registry cleaner, “optimizer,” debloater, or third-party
  bulk driver updater. Never recursively delete from Windows-owned or
  application-managed directories because a name or size makes the contents
  look disposable.
- Stop cleanup experimentation when the drive's Properties surface reports a
  critical health warning, an active security incident is suspected, the system
  is unstable or unable to boot, or a required backup cannot be verified.
  Preserve evidence and hand off to the appropriate recovery, security, or
  hardware workflow. Do not confuse this health warning with Storage's red
  capacity bar, which indicates low free space and remains within this workflow.
- Never request, display, log, or persist a BitLocker recovery key. Ask only
  whether an accessible backup of the key has been verified when the proposed
  work could affect boot, firmware, TPM, partitions, or recovery.

Read [references/safety-boundaries.md](references/safety-boundaries.md) before
interpreting findings, proposing actions, or executing cleanup. It defines the
supported inspection surfaces, mutation classes, forbidden operations, and
version-sensitive Microsoft references.

## Establish the baseline

1. Ask when the slowdown appears: boot or sign-in, idle, a specific workload,
   after an update, or under storage pressure. Record when it began and what a
   successful improvement would look like.
2. Identify the Windows version and build, system drive, exact free bytes and
   percentage, recent restart state, and whether the device is managed by an
   organization. Respect policy-managed settings and stop if required authority
   is unavailable.
3. Capture evidence while the problem is visible when practical:
   - Task Manager CPU, memory, disk, and startup impact;
   - Settings storage categories and Cleanup recommendations;
   - Windows Update history and current pending state;
   - Defender status and detection history, without starting a scan;
   - active power mode, Reliability Monitor, and narrowly time-correlated events;
   - volume capacity and provider-reported physical-drive health.
4. Do not use a universal low-space threshold. Report the exact capacity and
   treat Windows Storage's red capacity bar as low free space, not proof of drive
   failure. Do not infer that every warning in Event Viewer caused the slowdown
   or that no drive-health warning proves a SATA drive is healthy.
5. Before a resource-intensive diagnostic, explain its duration, load, possible
   restart, and whether it can remediate automatically. Proceed when the request
   or delegated diagnostic authority covers those effects; otherwise ask.

## Diagnose before proposing cleanup

Rank evidence-backed causes rather than assuming accumulated files are the
cause. Distinguish at least:

- sustained CPU, memory, or disk pressure from storage capacity;
- startup and background load from interactive workload demand;
- update, malware, corruption, power, or thermal symptoms;
- ordinary storage consumption from a critical or failing device;
- recoverable local copies from files whose deletion propagates to the cloud;
- apparent component-store size from actual reclaimable component storage.

If the evidence points to unsupported hardware, a failing drive, an active
security incident, boot failure, or an application-specific defect, report that
finding and stop at the boundary instead of disguising another workflow as
cleanup.

## Preview an actionable plan

For every proposed action, show:

| Field | Required detail |
| --- | --- |
| Evidence | The baseline observation that justifies the action |
| Exact target | Category, setting, app, startup entry, drive, or command |
| Expected benefit | Measured bytes or the specific pressure likely to improve |
| Data effect | What is deleted, retained, disabled, repaired, or made online-only |
| Risk and recovery | Reversibility, backup or restore prerequisite, and rollback |
| Operational cost | Elevation, time, resource load, network use, and restart |

Label estimates as estimates. Inventory Downloads, Recycle Bin, personal files,
`Windows.old`, synced folders, and unused apps item by item; never absorb them
into a generic temporary-files approval. Explain that disabling startup does not
uninstall an app, while uninstalling may remove local app data and can require an
installer, license, or account to reverse.

Ask only about previewed actions whose targets or effects exceed existing
authority. Already-authorized actions may proceed in the same turn. An unresolved
action blocks its dependent work; independent authorized actions may proceed
after their own prerequisites pass.

## Apply authorized actions

1. Re-read the live setting or target immediately before mutation and stop if it
   differs materially from the preview. Reassess the target, effects, and safe
   preconditions; ask again only when the change exceeds existing authority.
2. Prefer the smallest evidence-backed and most reversible supported mechanism:
   Settings storage surfaces before raw file operations; disabling a measured
   nonessential startup entry before uninstalling its app; OneDrive **Free up
   space** before deleting a synced file; media-appropriate drive optimization
   only after analysis shows a need.
3. Apply one action class at a time. Record the prior setting, command result,
   files or categories affected, actual bytes reclaimed, and restart requirement.
4. Do not interrupt servicing, repair, scan, or drive operations. If an action
   fails, preserve its output and stop that branch instead of escalating to
   ownership changes, ACL changes, forced deletion, or a broader repair.
5. Treat SFC, DISM repair, CHKDSK repair, component cleanup, Windows Update,
   Defender scans, power changes, hibernation changes, and drive optimization as
   distinct actions requiring applicable authority, not routine cleanup steps.
6. Save work and explain a required restart. Proceed when existing authority
   covers its interruption; otherwise ask before restarting.

## Verify the outcome

Repeat the relevant baseline under the same workload and after the same boot
stage when possible. Compare exact free space, startup behavior, and resource
pressure; inspect new Defender, Update, Reliability, or operation results only
where relevant. Restore a reversible setting if the intended benefit did not
materialize, the prior state is still safe, and the authorized change includes
that restoration; otherwise propose the rollback before applying it.

Finish by reporting:

- findings and their evidence;
- authorized actions completed and exact settings or targets retained;
- measured results, separately from estimates;
- restarts, recovery artifacts, or online-only files created;
- failures, skipped actions, and risks that remain;
- the next supported workflow when cleanup was not the actual remedy.

Do not claim that the PC is “fixed” unless the user’s original symptom and
success criterion were reproduced and measurably improved.

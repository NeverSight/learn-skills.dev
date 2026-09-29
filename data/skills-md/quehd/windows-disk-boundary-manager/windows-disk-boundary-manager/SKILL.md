---
name: windows-disk-boundary-manager
description: Manage Windows C drive pressure and storage boundaries for AI coding work. Use when Codex needs to inspect disk usage on C:, identify large folders or AI-related caches, preview safe cleanup candidates, classify paths as allowed or risky on C:, set free-space floors and storage budgets, or move repos, models, caches, and temp data off the system drive.
---

# Windows Disk Boundary Manager

Manage C drive pressure in three layers: discover what is using space, govern what can be cleaned or moved safely, and define boundaries so AI work stops growing back onto C:.

## Three-Layer Model

### 1. Discover

Start here unless the user already has trustworthy disk facts.

- Run `scripts/discover-storage.ps1` to inspect:
  - C drive free space
  - largest root folders
  - user-profile hotspots
  - AI and development cache hotspots
- Read `references/windows-hotspots.md` when you need examples of common Windows and AI-coding storage offenders.
- Summarize the top offenders with sizes before suggesting actions.

### 2. Govern

Use this layer to reclaim space safely.

- Run `scripts/cleanup-preview.ps1` first. It is preview-only.
- Prefer the smallest-risk wins first:
  - temp folders
  - package caches
  - browser or tool caches
  - moved-or-stale downloads
  - stale virtual environments or build output
- Separate candidates into:
  - safe-cache-cleanup
  - review-before-delete
  - migrate-not-delete
- Never delete from C: without a preview and explicit user approval.

### 3. Boundary

Use this layer to stop C: from filling again.

- Run `scripts/check-boundary.ps1` on candidate paths or workspace roots.
- Read `references/boundary-rules.md` for the default model:
  - allowed-core-system
  - warn-review
  - forbidden-heavy-on-c
- Recommend non-system roots such as:
  - `D:\Dev`
  - `D:\Caches`
  - `D:\AI`
  - `D:\Temp`
- Prefer environment variables and tool config over junctions or symlinks.

## Default Workflow

1. Discover current pressure with `scripts/discover-storage.ps1`.
2. Name the top 5 to 10 offenders with sizes and categories.
3. Preview reclaimable space with `scripts/cleanup-preview.ps1`.
4. Classify important paths with `scripts/check-boundary.ps1`.
5. Propose a boundary plan:
   - what stays on C:
   - what moves off C:
   - which thresholds should trigger action
6. Only after approval, perform explicit cleanup or migration commands.

## What Good Output Looks Like

Produce these sections when handling a real request:

- `Pressure summary`: current C: free space and risk level
- `Top offenders`: biggest folders with sizes
- `Fast wins`: safe cleanup candidates
- `Boundary risks`: paths that should not live on C:
- `Policy`: recommended free-space floor, preferred roots, and migration rules
- `Next actions`: smallest safe steps first

## Safety Rules

- Never delete anything without previewing and getting user approval.
- Never blindly remove from `C:\Windows`, `C:\Program Files`, `C:\Program Files (x86)`, or `C:\ProgramData`.
- Do not move active caches or model directories while the owning tool is running.
- Verify the destination drive exists and has enough free space before suggesting migration.
- Prefer config or environment-variable relocation over filesystem tricks.
- Use junctions or symlinks only when the user explicitly wants that approach.
- Treat model weights, datasets, package caches, and repo worktrees as high-risk growth paths on C:.

## Resources

- `scripts/discover-storage.ps1`: discovery layer
- `scripts/cleanup-preview.ps1`: governance layer
- `scripts/check-boundary.ps1`: boundary layer
- `references/windows-hotspots.md`: common Windows and AI-coding storage hotspots
- `references/boundary-rules.md`: default boundary model, thresholds, and relocation guidance

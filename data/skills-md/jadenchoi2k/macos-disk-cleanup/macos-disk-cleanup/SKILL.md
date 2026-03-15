---
name: macos-disk-cleanup
description: "Analyze and clean up macOS disk space for any user. Use when the user says 'free up space', 'disk full', 'storage cleanup', 'clean my Mac', 'what's taking up space', 'Storage Almost Full', 'delete caches', 'reclaim disk space', 'check disk usage', 'low on storage'. Targets: Trash, Downloads, Photos, Mail, iMessage, Music, browser caches, cloud storage, iOS backups, app caches, large apps, macOS installers, screen recordings, system data, developer tools (Xcode, npm, Docker, Homebrew). Actions: scan, analyze, identify, clean, delete, prune, reclaim, free up."
---

# macOS Disk Cleanup

You are a careful Mac maintenance assistant. Your job is to find and reclaim disk space while never deleting anything the user hasn't approved. Show the problem before proposing the fix. Speak in plain language -- the user may not be technical.

## Iron Rules

1. NEVER delete without showing sizes first and getting user confirmation
2. NEVER touch ~/Documents, ~/Desktop, ~/Photos, or ~/Downloads without explicit approval
3. NEVER attempt to delete files under `/System`, `/usr`, or root-level `/Library` (SIP-protected)
4. ALWAYS present a summary table before any cleanup action
5. ALWAYS show before/after disk usage for every session
6. ALWAYS check if an app is running before deleting its cache (`pgrep`)
7. ALWAYS guard tool commands with `command -v` checks (not every Mac has brew, npm, docker, etc.)
8. For cloud-synced folders, WARN that deleting may remove files from the cloud too
9. When in doubt, recommend the user review files manually rather than auto-deleting

## When to Use

- User says "free up space", "disk full", "storage cleanup", "clean up Mac"
- User is running low on disk space or got a "Storage Almost Full" warning
- User wants to know what's taking up space

## When NOT to Use

- User wants to clean up files within a specific project (not system-wide)
- User is asking about iCloud storage plan management
- User wants to fully uninstall applications (suggest AppCleaner or similar)

## Modes

### Scan Only (default when user asks "what's using my space?")
Run Steps 1-2 only. Present the summary table. Do NOT offer to delete unless the user asks.

### Cleanup (when user says "clean up" or "free up space")
Run all steps. Always confirm before any deletion.

### Targeted ("I need X GB free")
1. Calculate current free space with `df -h /`
2. Sort cleanup targets by size (largest first) and safety (safest first)
3. Present cumulative table showing how many items needed to hit the goal
4. Stop recommending once the target is met

## Step 1: Assess Disk Usage

```bash
df -h /
```

Scan the largest directories:

```bash
du -sh ~/Library ~/Downloads ~/.Trash ~/Desktop ~/Documents ~/Pictures ~/Music ~/Movies 2>/dev/null | sort -rh
```

Library breakdown:

```bash
du -sh ~/Library/Caches ~/Library/Application\ Support ~/Library/Mail ~/Library/Messages ~/Library/Containers ~/Library/Group\ Containers ~/Library/Mobile\ Documents 2>/dev/null | sort -rh
```

Check for APFS snapshots (can silently hold space even after deleting files):

```bash
tmutil listlocalsnapshots / 2>/dev/null
```

If snapshots exist, note: "APFS snapshots may be holding space. These are managed by Time Machine."

## Step 2: Identify Cleanup Targets

Scan all categories below. Skip any that don't exist on this Mac. Sort results by size and present only items > 500MB (unless user is extremely space-constrained).

---

### 2.1 Trash (typically 0-50GB)

**Path:** `~/.Trash`
**Safety: SAFE**

```bash
du -sh ~/.Trash 2>/dev/null
```

- Clean with: `osascript -e 'tell application "Finder" to empty the trash'`
- Or: `rm -rf ~/.Trash/{*,.*} 2>/dev/null`
- Also check volume-specific trash: `sudo du -sh /Volumes/*/.Trashes 2>/dev/null`

---

### 2.2 Downloads Folder (typically 2-30GB)

**Path:** `~/Downloads`
**Safety: ASK FIRST**

```bash
du -sh ~/Downloads 2>/dev/null
```

Find old DMG/ZIP/PKG installers:

```bash
find ~/Downloads \( -name "*.dmg" -o -name "*.zip" -o -name "*.pkg" -o -name "*.iso" \) -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $9}'
```

Find files older than 90 days:

```bash
find ~/Downloads -maxdepth 1 -mtime +90 -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $9}' | sort -rh | head -20
```

- Always list files and ask user before deleting

---

### 2.3 Photos & Media (typically 5-200GB)

**Path:** `~/Pictures`, `~/Movies`, `~/Music/GarageBand`
**Safety: CAUTION** -- User's personal files. Never delete without explicit consent.

```bash
du -sh ~/Pictures/Photos\ Library.photoslibrary ~/Movies ~/Music/GarageBand 2>/dev/null
```

Check for old iPhoto libraries (pre-2015 migration leftovers):

```bash
find ~/Pictures -name "iPhoto Library*" -exec du -sh {} \; 2>/dev/null
```

Check for iMovie/GarageBand:

```bash
du -sh ~/Movies/iMovie\ Library.imovielibrary ~/Movies/iMovie\ Theater 2>/dev/null
du -sh /Library/Application\ Support/GarageBand "/Library/Application Support/Logic" 2>/dev/null
```

**Advice:**
- If Photos uses iCloud, suggest "Optimize Mac Storage" in Photos > Settings > iCloud
- Old iPhoto libraries can often be deleted after confirming Photos imported everything
- GarageBand sound libraries (2-15GB): removable via GarageBand > Sound Library
- iMovie projects: suggest exporting finished projects and removing source

---

### 2.4 Mail Downloads & Attachments (typically 1-10GB)

**Path:** `~/Library/Containers/com.apple.mail/Data/Library/Mail Downloads`
**Safety: SAFE** -- Cached attachments re-download from server.

```bash
du -sh ~/Library/Mail 2>/dev/null
du -sh ~/Library/Containers/com.apple.mail/Data/Library/Mail\ Downloads 2>/dev/null
```

- Mail Downloads: safe to clear
- For the main Mail folder: suggest user manage via Mail.app (delete old mail, large attachments)
- Suggest: Mail > Settings > Accounts > uncheck "Download Attachments"

---

### 2.5 Messages / iMessage Attachments (typically 0.5-15GB)

**Path:** `~/Library/Messages/Attachments`
**Safety: CAUTION** -- Cannot be re-downloaded.

```bash
du -sh ~/Library/Messages/Attachments 2>/dev/null
```

- Manage via Messages > Settings > keep messages (30 days / 1 year / forever)
- Warn user: deleted attachments cannot be recovered

---

### 2.6 Music, Podcasts & Apple Music Cache (typically 1-30GB)

**Safety: MIXED** -- Caches safe; actual music files need user decision.

```bash
du -sh ~/Music 2>/dev/null
du -sh ~/Music/iTunes 2>/dev/null
du -sh ~/Library/Group\ Containers/*apple.podcast* 2>/dev/null
du -sh ~/Library/Caches/com.apple.Music 2>/dev/null
```

**Advice:**
- Old iTunes folder may be a duplicate after migration to Music app
- Podcast episodes: Podcasts app > Settings > auto-delete played episodes
- Apple Music cache: safe to delete, rebuilds on next play

---

### 2.7 Browser Caches (typically 1-10GB)

**Safety: SAFE** -- Caches rebuild automatically. User stays logged in.

**IMPORTANT: Check if browser is running before deleting. Use `pgrep -x "Google Chrome"`, `pgrep -x Safari`, etc.**

```bash
du -sh ~/Library/Caches/com.apple.Safari ~/Library/Caches/Google ~/Library/Caches/Firefox ~/Library/Caches/BraveSoftware ~/Library/Caches/com.microsoft.edgemac 2>/dev/null | sort -rh
```

- Close the browser first, then delete its cache folder
- Sites may load slightly slower temporarily

---

### 2.8 Cloud Storage Local Caches (typically 1-20GB)

**Safety: CACHE ONLY** -- Only delete cache folders, NEVER the sync folders.

```bash
du -sh ~/Library/Caches/CloudKit ~/Dropbox/.dropbox.cache ~/Library/Application\ Support/Google/DriveFS ~/Library/Caches/com.microsoft.OneDrive 2>/dev/null | sort -rh
```

**Advice:**
- iCloud: enable "Optimize Mac Storage" in System Settings > Apple ID > iCloud
- Dropbox: `.dropbox.cache` is safe to clear
- Google Drive: can switch to "streaming" mode
- Do NOT delete main sync folders (~/Dropbox, ~/Google Drive) -- that deletes cloud files

---

### 2.9 iOS / iPadOS Backups (typically 5-50GB per device)

**Path:** `~/Library/Application Support/MobileSync/Backup`
**Safety: CAUTION** -- May be the only copy.

```bash
du -sh ~/Library/Application\ Support/MobileSync/Backup 2>/dev/null
ls -la ~/Library/Application\ Support/MobileSync/Backup/ 2>/dev/null
```

- Manage via Finder: connect device > General > Manage Backups
- If user uses iCloud Backup, local backups may be redundant
- Always confirm before deleting

---

### 2.10 Application Caches (typically 2-20GB total)

**Path:** `~/Library/Caches`
**Safety: SAFE** -- Rebuild automatically.

**IMPORTANT: Check if app is running before deleting its cache.**

```bash
du -sh ~/Library/Caches 2>/dev/null
du -sh ~/Library/Caches/*/ 2>/dev/null | sort -rh | head -20
```

Common large caches: Spotify, Chrome (Google), Safari, Apple Music, app update caches (*.ShipIt)

- Close the app first before deleting its cache

---

### 2.11 Large Applications (typically 1-15GB each)

**Safety: SAFE** -- Can be re-downloaded.

```bash
find /Applications -maxdepth 2 -name "*.app" -exec du -sh {} \; 2>/dev/null | sort -rh | head -20
```

Common space hogs:
- **GarageBand** (1-3GB + up to 15GB sound libraries) -- delete if user never makes music
- **Xcode** (12-35GB) -- only needed by developers
- **iMovie** (2-3GB)
- **Logic Pro** / **Final Cut Pro** (1-6GB + libraries)
- **Microsoft Office** (4-8GB total)
- **Adobe Creative Cloud** (2-10GB each)

---

### 2.12 Old macOS Installers (typically 5-13GB each)

**Safety: SAFE**

```bash
find /Applications -maxdepth 1 -name "Install macOS*" -exec du -sh {} \; 2>/dev/null
```

- Left over from macOS upgrades; safe to delete after successful upgrade

---

### 2.13 App Leftovers from Uninstalled Apps (typically 0.5-5GB total)

**Path:** `~/Library/Application Support`, `~/Library/Containers`
**Safety: SAFE** -- Orphaned files from deleted apps.

```bash
ls ~/Library/Application\ Support/ 2>/dev/null
ls ~/Library/Containers/ 2>/dev/null
```

- Cross-reference with installed apps in /Applications
- Safe to remove if the app is no longer installed

---

### 2.14 Screen Recordings & Desktop Clutter (typically 0.5-10GB)

**Safety: ASK FIRST**

```bash
du -sh ~/Desktop 2>/dev/null
find ~/Desktop ~/Documents ~/Downloads \( -name "Screen Recording*" -o -name "Screenshot*" -o -name "*.mov" -o -name "*.mp4" \) -size +100M -exec ls -lh {} \; 2>/dev/null
```

- Screen recordings can be 100MB+ per minute
- Suggest user review and delete old ones

---

### 2.15 System Data (typically 5-30GB)

**Safety: CAUTION**

**Time Machine local snapshots:**
```bash
tmutil listlocalsnapshots / 2>/dev/null
```
- Thin: `sudo tmutil thinlocalsnapshots / 99999999999 1`
- Safe to remove if external Time Machine backup exists

**System/user logs:**
```bash
du -sh ~/Library/Logs /var/log 2>/dev/null
```
- User logs (`~/Library/Logs/*`): safe to clear
- Crash reports (`~/Library/Logs/DiagnosticReports`): safe to clear

**Sleep image and swap:**
- Managed by macOS. Do NOT delete manually.

**Note:** On FileVault-enabled Macs, disk space numbers may appear inconsistent after cleanup. This is normal; APFS space reclamation takes time.

---

### 2.16 Fonts (typically 0.1-2GB)

**Safety: CAUTION**

```bash
du -sh ~/Library/Fonts /Library/Fonts 2>/dev/null
```

- User fonts in ~/Library/Fonts: safe to remove
- System fonts in /Library/Fonts: do NOT remove
- Manage via Font Book.app

---

### 2.17 Printer Drivers (typically 0.5-3GB)

**Safety: SAFE** -- Re-downloads when printer reconnected.

```bash
du -sh /Library/Printers 2>/dev/null
```

- Old drivers for printers no longer used
- Clean: `sudo rm -rf /Library/Printers/*`

---

### 2.18 Developer Tools (skip if not present)

**Guard:** Only check this section if developer tools are detected:

```bash
xcode-select -p &>/dev/null && echo "Dev tools found" || echo "No dev tools"
```

**Xcode & Simulators:**
```bash
if xcode-select -p &>/dev/null; then
    du -sh ~/Library/Developer/CoreSimulator ~/Library/Developer/Xcode/DerivedData ~/Library/Developer/Xcode/Archives ~/Library/Developer/Xcode/iOS\ DeviceSupport 2>/dev/null | sort -rh
fi
```

- DerivedData: safe to delete (check Xcode not running: `pgrep -x Xcode`)
- Old simulators: `xcrun simctl delete unavailable`
- Old runtimes: `xcrun simctl runtime delete <id>`

**Package Manager Caches:**
```bash
command -v brew &>/dev/null && du -sh "$(brew --cache)" 2>/dev/null
command -v npm &>/dev/null && du -sh ~/.npm 2>/dev/null
command -v pnpm &>/dev/null && du -sh ~/Library/pnpm 2>/dev/null
du -sh ~/Library/Caches/pip ~/Library/Caches/go-build ~/Library/Caches/CocoaPods ~/.cargo ~/.rustup ~/.gradle ~/.m2/repository ~/Library/Caches/Yarn 2>/dev/null | sort -rh
```

Clean (only run for installed tools):
```bash
command -v npm &>/dev/null && npm cache clean --force
command -v brew &>/dev/null && brew cleanup --prune=all && brew autoremove
command -v pip3 &>/dev/null && pip3 cache purge
command -v pnpm &>/dev/null && pnpm store prune
command -v go &>/dev/null && go clean -cache
command -v yarn &>/dev/null && yarn cache clean
command -v cargo &>/dev/null && rm -rf ~/.cargo/registry/cache ~/.cargo/registry/src
```

**Docker:**
```bash
if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
    docker system df
    # Show stopped containers before pruning:
    docker ps -a --filter "status=exited" --format "table {{.Names}}\t{{.Size}}" 2>/dev/null
fi
```
- `docker system prune -f` (removes stopped containers, unused images/networks)
- `docker builder prune -f` (removes build cache)

**Scattered project artifacts:**
```bash
find ~ -maxdepth 4 -name "node_modules" -type d -prune -exec du -sh {} + 2>/dev/null | sort -rh | head -10
find ~ -maxdepth 4 -type d \( -name ".venv" -o -name "venv" \) -exec du -sh {} + 2>/dev/null | sort -rh | head -10
```
- node_modules: always safe to delete (recreate with `npm install`)
- venvs: safe to delete (recreate with `pip install -r requirements.txt`)

---

## Step 3: Present and Confirm

Present a numbered summary table:

```
| # | Target                   | Size  | Safety       |
|---|--------------------------|-------|--------------|
| 1 | Trash                    | 8.2G  | Safe         |
| 2 | Downloads (old DMGs)     | 3.1G  | Review first |
| 3 | Mail Downloads cache     | 1.5G  | Safe         |
| 4 | Browser caches           | 2.3G  | Safe         |
| 5 | Application caches       | 4.1G  | Safe         |
| 6 | GarageBand (not used)    | 3.0G  | Safe         |
| 7 | Old macOS installer      | 12.2G | Safe         |
| 8 | iOS backup (old phone)   | 15G   | Confirm      |
|   | **Total reclaimable**    | ~49G  |              |
```

Ask the user which items to clean (e.g., "1, 3, 4, 5, 7" or "all safe items").

For Targeted mode, show cumulative column:
```
| # | Target              | Size | Cumulative | Safety |
|---|---------------------|------|------------|--------|
| 1 | Old macOS installer | 12G  | 12G        | Safe   |
| 2 | Trash               | 8G   | 20G        | Safe   |
| 3 | iOS backup          | 15G  | 35G        | Confirm|
"Cleaning items 1-2 would free 20GB, meeting your 15GB goal."
```

## Step 4: Clean and Report

1. Close any apps whose caches will be deleted (warn user)
2. Execute cleanup for confirmed items only
3. Show before/after:

```bash
df -h /
```

4. Report total space recovered

## Tips

- Suggest macOS built-in tool: Apple menu > System Settings > General > Storage
- For recurring cleanup, suggest enabling "Empty Trash automatically" (Finder > Settings > Advanced)
- For iCloud users, "Optimize Mac Storage" can free significant space automatically

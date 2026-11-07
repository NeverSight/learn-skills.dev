---
name: merge-branch-mac
description: Merge a branch of Windows-first (and Android) work into the mac branch, making sure every change translates to macOS or is written down as not yet doing so. Use when the user asks to merge into mac, merge the mac branch, catch mac up, or bring Windows work over to mac. Follows merge-branch's review gate in full, then adds a mac-translation pass whose verdict for each change — translated, needs mac work, or deferred — is recorded in the project's platform catch-up tracker (CATCHUP.md unless the project keeps it elsewhere), so no Windows behaviour goes silently missing on a Mac.
---

# Merge into the mac branch

You are responsible for the mac branch. Development is Windows (and Android)
first; macOS and iOS receive the work afterwards through the mac branch. The
incoming branch carries Windows and possibly Android changes, and the merge
has two jobs: land them, and leave the catch-up list true — every Windows
behaviour either works on a Mac or has a row saying it does not yet.

**The branch.** Usually `mac`; use whatever name the project gives it (some
call it `mac-catch`). If it does not exist, say so and ask before creating
it. The direction is almost always `<main>` → mac, which is what
merge-branch's direction rule recommends for a long-lived branch: resolve and
verify on the mac side, where breakage is contained.

**Follow [merge-branch](../merge-branch/SKILL.md) in full** — the survey, the
principles review, the "never take a product decision" rule, conflict
resolution by intent, verification, and the commit rules. This skill adds the
mac pass.

## Read first

- **The platform catch-up tracker.** `CATCHUP.md` (often `docs/macos/`), a
  platform matrix, or wherever the project's principles say Apple work is
  tracked. It holds what is already owed, the known platform differences, the
  numbering, and the status of earlier merges. If the project keeps a second
  tracker for desktop-versus-phone gaps, that is another axis — do not file
  platform rows there.
- **The project's macOS docs** (`docs/macos/` or similar — they may live only
  on the mac branch), including any release, signing or update runbook.
- `git log --oneline mac..<main>` and `git diff --stat mac...<main>`, as
  merge-branch's survey does. Note how many commits are coming: a merge of
  hundreds of commits needs the pass done per area, not per commit.

## The mac-translation pass

For every incoming change, ask: *what does this do on a Mac?* Look hardest at
the places that are Windows-shaped by nature:

| Where | Windows today | What a Mac needs |
|---|---|---|
| Data, config, cache and log locations | `%APPDATA%`, `%LOCALAPPDATA%` | `~/Library/Application Support`, `Caches`, `Logs` — not an XDG fallback; keep any override variable the project already has |
| Process and IPC | named pipes, `CreateNamedPipeW`, `tasklist`/`taskkill` | Unix sockets, `pkill`, the same protocol behind a `cfg` seam |
| Autostart and the tray | registry Run key, notification-area icon | login item or launch agent; a menu-bar item — never a silent loss of the tray's actions |
| Scripts and verbs | `.bat`, PowerShell | the POSIX script, verb for verb; a `.bat`-only behaviour with no shell equivalent is a row |
| Shortcuts | raw Ctrl checks | the platform command key (Cmd) where "the command key" is meant; a raw Ctrl check is a finding unless Ctrl is really meant |
| Window chrome | custom title bar, `.ico`, compositor assumptions | traffic lights, full-screen behaviour, `.icns`, the Dock |
| Files | path and filename assumptions, file watching, fsync semantics | case-insensitive but case-preserving paths, FSEvents behaviour, no reserved names |
| OS version and environment | `cmd /C ver`, console attach | `sw_vers`, nothing to attach — keep the Windows path `cfg(windows)` |
| Release and update | installer, Authenticode, in-place file swap | `.app` in a `.dmg`, `codesign` and notarization, a whole-bundle swap with the same rollback |
| Dependencies | a Windows-only crate in shared `[dependencies]` | a `[target.'cfg(target_os = "macos")'.dependencies]` entry, or a seam |
| Tests | chords, paths and separators spelled by hand | the platform's spelling, or a helper that owns it |

For each change the verdict is one of three, and it is said out loud in the
report:

- **Translates as is.**
- **Needs a mac seam** — a `cfg`, a port trait, a platform adapter — done in
  this merge, or a tracker row saying what and where.
- **Deliberately deferred** — a tracker row with the reason and the trigger
  that would bring it forward.

Never a silent no-op on a Mac.

- **Push the mechanism down.** When a change hard-codes a Windows mechanism in
  shared code where a platform seam belongs, that is a finding for the source
  branch — the fix goes there — not a mac-side patch that lets the leak stay.
- **Android-flavoured changes** usually map to iOS rather than macOS; note
  them for the iOS catch-up instead of forcing them into this merge.
- **When both branches numbered rows**, the tracker's numbering collides.
  Renumber on the mac side and say so in the merge commit.
- **The source branch may already have written the mac arm** beside the
  Windows one. Compile and test it — the merge is where an arm that was never
  built on a Mac gets its first run.

## Record it

Update the tracker as part of the merge, not after: for each Windows
behaviour the merge brought in, what translated, what needed mac work and
where it lives, and what is deferred — each deferred row with enough context
that someone can pick it up cold. A merge that leaves a Windows behaviour
missing on a Mac without a row saying so is not finished.

The merge commit message carries the same summary in brief: what came in,
what it cost on the mac side, and which rows the tracker gained or closed —
on top of the decisions merge-branch already asks you to write down.

## Verifying

- Build and test for the mac targets, not only the host's. From a Windows
  machine, `cargo check --target aarch64-apple-darwin` (if the target is
  installed) type-checks the pure Rust crates but cannot link or run the app;
  a macOS CI job, if the project has one, is the arbiter for building and
  testing.
- State the literal status per target in the report — *type-checked*,
  *built*, *executed* (only on a Mac someone ran) — and what could not be
  verified from this machine, rather than implying it passed.
- Do not push unless asked.

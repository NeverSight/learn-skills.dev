---
name: loop-report
description: "Builds and delivers the live progress page of a long-running delegated loop (matt-auto, autocode, and any loop that runs for minutes to hours on the user's behalf) — one self-contained HTML the user can read while the loop runs and keep afterwards. The build is `assets/render.py` over `assets/shell.html` plus the calling loop's view; the delivery is `assets/deliver.py` (Orca artifact link, or the worktree's Orca browser tab when links are unavailable, or the path), which keeps the route stable for the whole run. Callers run those two scripts and relay the answer; they never run `orca` commands themselves. Called by interview-report (matt-auto's decision graph) and autocode (the experiment board); do not trigger standalone."
---

# Loop report (the shared progress page)

A delegated loop runs unattended for a long time. Two things make that bearable for the person who delegated it: they can see where it is without opening a terminal, and the page they are looking at keeps updating. This skill owns both — the page and how it reaches the user — for every loop in this harness, so no loop grows its own copy.

The loop owns its *graph* (matt-auto's decision stages and ticket waves, autocode's hypothesis frontier and metric trend). This skill owns everything around it: the design system, the 진행 상황 header with percent, elapsed time and ETA, blockers, the 결과 panel measured from git, the auto-refresh poll, the theme toggle, the modal — and the delivery.

## Two scripts, two verbs

Both live in `assets/` next to this file. `<this skill's dir>` is the directory holding this SKILL.md: `~/.codex/skills/loop-report` under the npx installer on Codex, the installed weed-harness plugin's `skills/loop-report` on Claude Code or a native Codex plugin install, `~/.agents/skills/loop-report` under Orca.

**Build** — the caller writes its data JSON next to the page and names its view:

```
python3 <this skill's dir>/assets/render.py \
  --data <dir>/<slug>.data.json --out <dir>/<slug>.html \
  --view <the loop's skill dir>/assets/view.html
```

The script validates the common contract below, then the view's own `validate.py`, and refuses to write a page that would render wrong — so a regeneration is "edit the JSON, rerun the script". Never splice the shell or a view by hand (no `cp` + `sed`/`perl`): a hand-rolled substitution silently ate 30 KB of the shell in testing. Never edit the shell's or a view's CSS/JS. If `python3` is missing, say so and stop.

**Deliver** — after every build. Which way depends on the platform:

- **Claude Code** — publish the page with the **Artifact tool** on the same file path every time (same path, same URL; favicon on the first publish only) and relay the URL. No probe, no `deliver.py`; without the Artifact tool the page is a path, said once.
- **Codex, OpenCode, Orca** — `deliver.py`, below.


```
python3 <this skill's dir>/assets/deliver.py probe   --page <dir>/<slug>.html
python3 <this skill's dir>/assets/deliver.py publish --page <dir>/<slug>.html [--rerun-share]
python3 <this skill's dir>/assets/deliver.py show    --page <dir>/<slug>.html
```

- `probe` runs once, early in the loop, before its first gate (the page need not exist yet), so the user learns *before* the gate whether there will be a public link. `publish` runs after every regeneration. `show` reports the current route without doing anything — for a status command or a fresh context that has no publish answer in memory.
- The answer is one JSON line on stdout: `{"route": "link|tab|path", "url", "browserPageId", "bin", "reason"}`. Relay it as-is to the user or the calling loop — the URL, or "browser tab + path", or the path, plus `reason` whenever the route is not `link`. Exit code 0 means answered (a run with no link is an answer, not an error); 1 means the page file is missing.
- The script chooses the route in order link → tab → path, picks the Orca executable (`orca` inside an Orca terminal, `orca-ide` elsewhere on Linux, falling through the broken `--no-sandbox` shim), shares once and updates afterwards so the URL stays the same, reuses the worktree's browser tab and reloads it after each regeneration, and keeps all of that in `<dir>/<slug>.delivery.json`. Nothing else reads or writes that file.
- A refused share (`artifact_sharing_disabled`) is a device setting only a human can flip in Orca desktop › Settings › Artifacts; the script does not retry it, and its `reason` carries the explanation once and a short tag afterwards — relay it once. On a headless runtime (`orca serve` on a server) that switch may be unreachable, so the tab is the delivery for that run, not something to wait for. Pass `--rerun-share` only when the user says they turned sharing on (or signed in, for `authentication_required`). A transient `update` failure keeps the existing link and says the previous version is still showing; the CLI caps a page at 800 KB, so a size failure means the data block grew wrong. Links expire 30 days after the last update.
- A `link` from `probe` is provisional — sharing can still be refused at the first `publish`. Hosted pages run in a sandboxed frame without `localStorage`, so a view that keeps edits there keeps them only for that page load; say "export before reloading" when handing over a link to such a page.
- Inside Orca's built-in browser the page cannot reload itself (script reloads of `file://` pages are ignored), which is why `publish` after every regeneration is not optional there.

Loops that call these scripts require weed-harness ≥ 3.1 (the version that ships `deliver.py`); when the script is missing, say `weed-harness 3.1 required: deliver.py missing` once and hand over the rendered path.

## Common data contract

```json
{
  "title": "실행 제목, in Korean",
  "slug": "run-slug",
  "generated": "2026-09-04",
  "summary": "2-4 plain-language sentences for someone with zero context, in Korean.",
  "progress": {
    "state": "running",
    "updated": "2026-09-04T10:12:00+09:00",
    "startedAt": "2026-09-04T09:30:00+09:00",
    "current": "지금 무엇을 하고 있는지 한 줄",
    "note": "선택 — 읽는 사람이 알아야 할 한 줄",
    "blockers": [ { "title": "H004", "reason": "측정 실패", "detail": "bench.py exit 2 — 머지 후 metric이 실행되지 않음" } ]
  },
  "outcome": {
    "baseRef": "2dacebe", "headRef": "3b0523e", "branch": "feature/x",
    "note": "이 diff가 무엇인지 한 줄 — 생략 가능",
    "files": [ { "path": "src/foo.ts", "status": "added", "kind": "code", "added": 120, "removed": 0, "note": "이 파일이 하는 일, 한 줄" } ]
  }
}
```

- Everything else in the file belongs to the view (see the loop's own skill for its keys).
- `progress` is present from the moment the loop is under way until it ends. `state` is `running` / `blocked` / `done`; `updated` is read from the clock (`date -Iseconds`) when you write the file — a stamp typed from memory makes the page's "N분 전 갱신" lie. `startedAt` drives 경과; percent and ETA come from the view.
- `progress.blockers` is for anything that stops the run and has no node in the view: `title`, a short `reason`, and a `detail` with the specific, checkable fact. "막혔습니다" with no detail is the failure the box exists to prevent.
- The page polls while `state` is not `done` (and on a gate page with no `progress` yet), skipping the reload while the reader has unsaved edits. `state: "done"` on the final regeneration is what stops it.
- `outcome` is the final regeneration only, together with `progress.state: "done"` (`render.py` refuses it otherwise). `status` ∈ added / modified / deleted / renamed; `kind` ∈ code / docs (`.md`/`.mdx`/`.txt`/`.rst` and docs directories) / other (lockfiles, generated output, binaries). `added` / `removed` come from `git diff --numstat <baseRef>..<headRef>` — never estimated; a binary gets `0`/`0` and a note. Leave the loop's own bookkeeping (its log folder, `.unlazy/**`, `.autocode/**`) out. `note` is one Korean line per file. Totals are computed in the page.
- Every human-facing string is Korean; ids and JSON structure stay English.

## The view interface (for loop authors)

A view is one file, `assets/view.html` in the loop's skill, with one `<style>` block and one `<script>` block, each tag at column 0. The script assigns `window.LoopView` with any of: `kind`, `meta(data, ctx)`, `progress(data, ctx) → { percent, remainingMin, count } | null`, `blockers(data, ctx)`, `renderProgress(host, ctx)` (inside the 진행 상황 card), `renderOutcome(host, ctx)` (inside 결과, above the file table), `render(host, ctx)` (the main area), `hasUnsavedEdits()`. `ctx` carries the data and the shell's helpers (`el`, `bar`, `stat`, `section`, `kvRow`, `modal`, `clickable`, `shortRef`, time formatters, `prefs`/`setPref`). A `validate.py` next to the view exposes `validate(data) → [errors]`. The shell's CSS classes (`.flow`, `.wcol`, `.tnode`, `.badge`, `.stat`, `.panel`, `.kv`) are the component set; a view adds only what the shell lacks. Read `assets/shell.html`'s header comment and the existing views (`interview-report`, `autocode`) before writing a new one. `tests/test_deliver.py` runs `deliver.py` against a fake Orca CLI — run it after touching the script.

## Red flags

- Building the page with `cp` + `sed`/`perl`, or editing the shell's or a view's CSS/JS → the scripts exist because those shortcuts shipped broken pages.
- Running `orca artifacts` / `tab` / `reload` from a loop instead of `deliver.py publish` → two owners of one route drift apart; the script owns the route and `delivery.json`.
- Skipping `publish` after a regeneration, or skipping the page because publishing failed → in the Orca tab the old version stays on screen; and the local HTML is still the report when only the link is missing.
- Passing `--rerun-share` on your own, or on every regeneration → the device setting only changes when a human flips it.
- `progress.updated` from memory, `state` left at `running` on the final page, `outcome` line counts not from `git diff --numstat`, a blocker with a vague `detail` → each one makes the page lie in a way the reader cannot see.

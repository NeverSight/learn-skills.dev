---
name: blurt
description: >-
  Screen + voice → structured work. The user records their screen while talking (demoing their product, browsing,
  exploring an idea); turn the recording into items — bug/polish issues with repro steps, frames and suspected code,
  ideas with the inspiration behind them, notes, todos — let them review on a local page, then export (Feishu/Lark
  Bitable, CSV/Markdown, GitHub Issues…) or start fixing. Use when the user wants to record feedback / QA / ideas by
  talking while using their screen, hands over such a video, or wants to process recordings from the Blurt app.
  Triggers: "blurt", "/blurt", "开始口喷", "口喷鸡", "开始录", "录屏提 bug", "录一下我的想法", "record feedback",
  "turn this recording into issues", "处理我录的视频", "process my recordings".
---

# blurt 🐔 — show it, say it, get structured work back

People think best out loud with their eyes on the screen. They jump between topics, correct themselves, point at
things. Your job: capture that with no friction, then do the tedious part (splitting, writing up, picking and
marking screenshots, finding the code, filing) with care. Optimise for the user's flow: never interrupt a
recording, ask few questions, make review fast.

Scripts live in `scripts/` next to this file; run them with `uv run <skill-dir>/scripts/<name>.py ...` (each
declares its deps; `uv` installs them on first use). Every script has `--help`. Always reply in the user's
language; write items in the language the user spoke.

## 0. Setup (first run, or when something fails)

- `doctor.py` → OS, RAM/GPU, ffmpeg, configured ASR, recommendations, `todo` list.
- Missing ffmpeg/uv: offer the install command; run it only after the user agrees.
- ASR: if none configured, pick from `asr_recommendations` + the language the user speaks, tell the user in one
  line what and why (size, local vs cloud, cost), run its `setup`. Details: `reference/asr.md`. Cloud keys are set
  by the user in their env — never ask them to paste keys in chat.
- `record.py build` — macOS: compiles the native recorder (Xcode Command Line Tools; else a Tk fallback) and
  installs the **Blurt** menu-bar app into ~/Applications. Windows: the Start-menu shortcut appears on first
  recording. Mention it in one line: "Blurt is also in your Applications — ⌥⇧R records from anywhere".
- `record.py test` → look at the returned `frame` yourself. Wallpaper-only/black or `ok: false` ⇒ Screen Recording
  permission missing; `mic_silent: true` ⇒ Microphone permission / wrong mic. On macOS the permission belongs to the
  app hosting you (Terminal, iTerm, VS Code, Claude, Codex…) and that app must be restarted after granting.
  macOS 15+ may show an "allow … to bypass the window picker" prompt — the user clicks Allow themselves.
- Optional project config `.blurt/config.json`: export target, owners/module map, column mapping, custom lenses in
  `.blurt/lenses/`. Suggest adding `.blurt/sessions/` to `.gitignore`.

## 1. Record (or pick up a recording)

**From the chat:** if the thing to look at is a local dev server/app in this repo, check it is running. Start
`record.py start` **in the background** (`--last-region` to reuse the last area) and tell the user in a few lines
what happens:
- a dimmed overlay: drag to draw the area (or click a window, F = full screen) → **开始录制** / Enter. Only that area
  is recorded — tabs, bookmarks and other windows stay private;
- 3-2-1 countdown (click to skip), then a small floating bar: timer · mic level · ⏸ pause · ↺ restart/discard ·
  **完成**. ⌥⇧P pause/resume, ⌥⇧S finish (Windows: Alt+Shift). The bar is never in the recording;
- talk naturally, point with the mouse; click **完成** — no need to send another chat message.
The task ends with `DONE video=…` → continue with §2 right away (`CANCELLED`, exit 2 → acknowledge and stop). From
the chat you can also `record.py stop | pause | resume | restart`.

**Waiting on a background step** (here and in §5): if your harness wakes you when a background task finishes (Claude
Code), end your turn — you'll be notified. If it doesn't (Codex), a finished turn can't be resumed by the child
process: keep the turn open and wait on that same tool session with long polls (no busy loop); don't send a final
response while it runs.

**Existing video** (QuickTime, OBS, Loom, phone, a teammate's Blurt recording…): create
`.blurt/sessions/<timestamp>/`, copy it in as `recording.<ext>` (with `events.jsonl` / `meta.json` if it came from
Blurt), continue with §2.

**Blurt app recordings:** the menu-bar app records into the current workspace — `~/Blurt/recordings/<ts>/` by
default, or `<project>/.blurt/sessions/<ts>/` when a project is bound. `record.py inbox` lists all of them with
`processed` / `reviewed` flags. "Process my recordings" → do §2–§4 for each unprocessed one (fan out to subagents
if available), then one review per session (or merge into one session dir if the user wants a single list).
`meta.json` has `author` — keep it on items when several people's recordings are combined.

## 2. Transcribe

`transcribe.py run <session>/recording.mp4` → `transcript.json` + `transcript.txt` (`[mm:ss.s-mm:ss.s] text`).
For Whisper/API backends pass `--prompt` with a short glossary (product, page/module names, people) from the repo.
Also run `frames.py scan <video>` (visual-activity index for candidates/sheets).

## 3. Understand → items

Read the whole transcript first, glance at a few frames, then write `<session>/items.json`
(schema: `reference/schema.md`). Decide **per item** what it is — the recording decides, not a mode switch:

| kind | when | lens |
|---|---|---|
| `issue` | something in the product to fix or polish | `reference/lenses/issue.md` |
| `idea` | something to build / change / borrow ("这个网站的这里好") | `reference/lenses/idea.md` |
| `note` | an observation / finding / fact worth keeping | `reference/lenses/note.md` |
| `task` | an action item that isn't a product issue | `reference/lenses/task.md` |
| custom | a lens in `.blurt/lenses/` or `~/.blurt/lenses/` fits, or the user asked for it | that file |

Principles — judgement, not rules:
- One item = one thing. People jump around, revisit, correct themselves ("不对，是…"), or say two things in one
  sentence: merge revisits, drop retracted remarks, split compounds. Pure narration is not an item.
- Fix ASR errors from context (repo vocabulary, what's on screen). Keep `quote` close to what was said.
- Don't invent. When unsure, write your best guess, set `confidence: "low"`, add a short `questions` entry.
- Read URLs / product names off the frames into `source`.
- `code_refs` (issues, inside a repo): grep the visible text / route / component; list the likely `path:line`s.
- Give the session a `title`. For idea-heavy or exploratory recordings write a `digest` (markdown): themes, the
  strongest ideas, how they connect, suggested next step — it becomes the review page's Overview.

## 4. Evidence: frames & clips

Pick 1–3 frames per item that show *the point* (the bug itself, the part of the page that inspired the idea):
- `frames.py sheet <video> --from S --to E -o <session>/sheets/<id>.jpg` → ~6 diverse settled candidates with
  timestamps in one image; `--at t1 t2 …` for specific moments ("这里 / this / look"). Speech often trails the action.
- Marking the spot — never estimate coordinates from a thumbnail or contact sheet:
  1. `frames.py grid <video> --at T -o <session>/sheets/<id>-grid.jpg` → labelled 0–1 grid plus the recorded cursor
     and nearby clicks (events.jsonl — exact). Read box edges off the grid (`--crop` zooms, labels stay full-frame).
  2. `frames.py grab <video> --at T -o <session>/frames/<id>-1.jpg --box x,y,w,h`; `--ring cursor|click` when the user
     pointed at / clicked it. Tiny detail → second frame with `--crop`.
  3. **Look at every annotated frame before using it.** Box not on the point → fix and re-grab.
- Animations / flows / timing: `frames.py clip --from --to -o <session>/clips/<id>.mp4` (< 20 MB).
- Many items (> ~12)? Fan out frame work to subagents in batches if your harness has them.

## 5. Review with the user

Always open the review page — the frames are the point. Run `review.py <session>` **in the background** (opens the
browser, exits when the user finishes). In the same message:
- ≤ 5 items: the full numbered list (kind · title · owner/module, plus `questions`); more: a short summary (counts by
  kind, the headline items, open questions);
- two lines on the page: one item at a time — **A** keep · **X** drop · **J/K** next/prev · **Z** undo · **?** keys;
  fields editable in place; **G** list view; **V** overview (when there's a digest); "完成审核" hands it back.
The user may answer in chat or on the page. Wait as in §1 until the review summary prints, then reload `items.json`
(dropped items have `status: "deleted"`, answers are in `answer`) and continue with §6. If they reply in chat
instead, apply it yourself and close the page (`pkill -f "review.py <session>"`).

**Unattended runs** (started by the Blurt app via `claude -p` / `codex exec` — env `BLURT_APP=1` — or any other
non-interactive mode): don't ask anything; do §2–§4 and write `items.json`, then finish with a 2–3 sentence summary.
With `BLURT_APP=1` don't start the review page — the app opens it when you exit; otherwise start it detached
(`nohup uv run …/review.py <session> >/dev/null 2>&1 &`). Never export to external systems unattended.

## 6. Export / act

Ask once where things go (remember in `.blurt/config.json` → `export`). Typical: issues → the team's bug table;
ideas → an ideas board / doc; notes → Markdown; tasks → the user's todo tool.
- Feishu/Lark Bitable → `feishu.py export <session> "<table url>" [--kind issue|idea|…]` (lark-cli if installed,
  else app credentials; default columns per kind, creates missing ones, uploads frames + clips, resumable).
  No table yet → `feishu.py create "<name>"`. Other columns → `feishu.py fields` then `--map`.
  Details: `reference/export-feishu.md`.
- Markdown + CSV → `export_local.py <session>` (all kinds; always a good local record).
- GitHub Issues / Linear / Jira / Notion / Obsidian / anything else → `reference/export-other.md`; use the CLI or
  MCP tool the user has; map fields by meaning.
Confirm destination and count before creating anything remotely; report links afterwards. Then offer the natural
next step — for issues "want me to start fixing these?" (you have `code_refs`), for ideas "want a quick prototype /
spec of the top one?".

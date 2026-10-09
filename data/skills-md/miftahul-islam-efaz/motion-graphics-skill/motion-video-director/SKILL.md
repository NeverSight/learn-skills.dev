---
name: motion-video-director
description: "Plan, direct, and produce code-drawn 2D/3D motion graphics and edited videos (reels, hooks, SaaS/product explainers, talking-head edits) on the user's local machine through any coding agent that has terminal + file access (Claude Code, Codex, Cursor, Claude Desktop, VS Code agents, etc.). Workflow: explain the process → user gives references + story → write a paste-ready ElevenLabs voiceover script → user generates and returns the MP3 → build, preview, render. Uses Canvas/SVG/p5.brush/Three.js/GSAP rendered in headless Chrome, Motion Canvas/Revideo, ffmpeg, small local AI models (cutout, transcription), plus LottieFiles, Freesound, Pexels/Pixabay, Firecrawl and ElevenLabs MCPs, and the Playwright MCP to browse any website visually (Pinterest, Behance, Dribbble, brand sites) and grab image/video assets by itself. Use when the user asks to make, edit, animate, caption, voice, or sound-design a video."
---

# Motion Video Director

You are director, producer, motion designer, editor and sound designer in one.
**Golden rules:** (1) run Preflight first, (2) plan before you build, (3) get explicit user approval before rendering any video, (4) log everything in the project folder, (5) keep `PROGRESS.md` current and read it first when resuming, (6) check every change with the fast preview loop (§2b) before any full render, (7) when an asset is needed and no API MCP has it, go find it yourself with the Playwright MCP (§16) instead of asking the user to hunt for it, (8) **on first contact, send the kickoff message (§0a) before anything else** — explain the process and what to connect, (9) **never build or render scenes before the user has sent the final voiceover MP3** (generated from your §10 script) — unless the user explicitly asks for a temporary guide track, (10) never print, log or commit API key values (§0c).

---

## 0. Preflight (run every time this skill loads)

1. **Agent access** – confirm you can run terminal commands and read/write files on the user's machine (Claude Code, Codex, Cursor, Claude Desktop with a filesystem/terminal MCP, VS Code agents…). Ask the user for the **project folder** (never write outside it). If you are a browser-only agent without terminal access, tell the user this skill needs a local agent (§0a) and offer to do only planning, the script and asset hunting.
2. Run `scripts/preflight.sh` (or the equivalent checks below) in the project folder with your terminal.
3. Produce a checklist table: `Tool | Status (✅/❌) | Version | Action`.
4. For **each ❌ item, ask the user individually** (install / skip / use alternative). Do not start work until every item is resolved or explicitly skipped.
5. **PROGRESS.md** – if the project folder already has `PROGRESS.md`, read it (and the tail of `LOG.md`) and continue from "Next step". If not, create it from the template in §1.
6. Copy `scripts/preview.mjs`, `scripts/create_env.sh` and `scripts/normalize_env.py` into the project's `scripts/` folder; the render script must follow the CLI contract in §2.
7. **Create the key file yourself:** run `bash scripts/create_env.sh <project>` → it creates `<project>/.env` with empty slots (+ `.gitignore`). Tell the user the full path, which keys to paste where, and to save the file (§0c). Then load the keys from it; connect missing MCPs as described in §0b.

| Category | Item | Check | If missing (ask first) |
|---|---|---|---|
| Runtime | Node ≥18, npm, Python ≥3.10 | `node -v`, `python3 --version` | official installer / nvm / pyenv |
| Render | Headless Chrome / Chromium + Playwright | `npx playwright --version` | `npm i -D playwright && npx playwright install chromium` |
| Encode | ffmpeg + ffprobe | `ffmpeg -version` | winget/brew/apt, or static build (gyan.dev / johnvansickle) |
| Libraries | three, gsap, p5, p5.brush | `npm ls three gsap p5 p5.brush` | `npm i three gsap p5 p5.brush` |
| Frameworks | Motion Canvas or Revideo (optional) | `npm ls @motion-canvas/core @revideo/core` | `npm init @motion-canvas@latest` / `npm init @revideo@latest` |
| Models | faster-whisper / WhisperX (word timing) | `python3 -c "import faster_whisper"` | `pip install faster-whisper` (use `small`/`base` model ≈ 150–500 MB) |
| Models | Cutout: RobustVideoMatting (≈15 MB), rembg/u2netp (≈5 MB), SAM2-tiny (≈150 MB) | file in `models/` or `python3 -c "import rembg"` | download into `models/`; prefer smallest that works; CPU OK |
| Audio | loudness tools | `ffmpeg -filters | grep loudnorm` | comes with ffmpeg |
| MCP | **LottieFiles** (search + Lottie Creator) | list tools | `npx -y @lottiefiles/creator-mcp@latest` |
| MCP | **Freesound** (SFX, prefer CC0) | list tools | a Freesound MCP (e.g. sandraschi/sfx-mcp) + `FREESOUND_API_KEY`; no MCP → use the REST API directly (§0c) |
| MCP | **Pexels / Pixabay** (stock photo/video) | list tools | e.g. xcollantes/free-stock-images-mcp + `PEXELS_API_KEY` / `PIXABAY_API_KEY`; no MCP → REST API directly (§0c) |
| MCP | **Firecrawl** (research, references, brand sites) | list tools | `npx -y firecrawl-mcp` + `FIRECRAWL_API_KEY` (§0b) |
| MCP | **ElevenLabs** (SFX gen, music, optional VO) | list tools | `uvx elevenlabs-mcp` + `ELEVENLABS_API_KEY` (§0b). Not required for VO — the user generates the MP3 on elevenlabs.io from your script |
| MCP | **Playwright MCP** (visual browser: open sites, search, see results via screenshots, click, download — §16) | list tools (`browser_navigate`, `browser_take_screenshot`…) | add it to your agent's MCP config **on the user's PC** (§0b) so downloads land in the project: `"playwright": { "command": "npx", "args": ["@playwright/mcp@latest", "--user-data-dir", "<project>/../.browser-profile", "--output-dir", "<project>/cache/browser"] }` (Node ≥18; first run fetches Chromium via `npx playwright install chromium`). Fallback: the agent's own built-in browser, if it has one, then move files to the PC. |
| Fonts | brand + style fonts | `assets/fonts/` | fetch via Firecrawl from font sites (§12) |
| Models | **Demucs** (stem split: voice / music / SFX — install by default, it's small) | `python3 -c "import demucs"` | CPU install ≈ 300 MB total: `pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu` then `pip install demucs soundfile`; model `htdemucs` (≈ 80 MB) downloads on first run (§0d) |
| Optional | Blender (headless 3D) | `blender -v` | blender.org |

Never ask the user to paste API keys in chat if avoidable — have them put keys in `.env` (gitignored, §0c).

---

## 0a. Kickoff message (send this first, before preflight results or any planning)

Adapt the wording, keep the structure. Send it once per new project:

> **How we'll make this video**
> 1. **You give me references + the story/plan** — reference videos/links/screenshots, what the video is about, who it's for, platform & format (16:9 / 9:16 / 1:1), target length, tone, CTA, brand assets (logo, colors, fonts), must-haves / must-avoids.
> 2. **I write the voiceover script** — paste-ready for ElevenLabs (voice, model and settings included).
> 3. **You generate the MP3 on elevenlabs.io and send it to me** (drop it into `assets/vo/`). Nothing gets built before this — the whole video is timed to your real voiceover.
> 4. **I build it** — storyboard + style frames for approval, then all scenes, sound design and music; you get contact sheets and low-res previews to give feedback.
> 5. **Final render** — full-res MP4 (+ vertical/thumbnail if wanted), loudness-normalised, with a credits/licence list.
>
> **What to connect (one time).** Just tell me "connect the Firecrawl MCP" (or any of these) and I'll add it for you, or add them manually (setup below):
> - **Required on your PC:** Node ≥18, Python ≥3.10, ffmpeg, Playwright + Chromium, faster-whisper, Demucs — I check these and install with your OK.
> - **MCPs (recommended):** Playwright MCP (I browse sites and grab assets myself), Firecrawl (research, fonts, brand sites), ElevenLabs (SFX/music generation).
> - **MCPs or API keys (optional, better assets):** Freesound (SFX), Pexels + Pixabay (stock photos/video), LottieFiles (animations), Unsplash (photos).
> - **API keys:** I've created a key file for you at `<full path>/.env`. Open it, paste each key after the `=` on its line, and **save**. Leave lines empty for platforms you don't use. Please don't paste keys into chat. Tell me "saved" and I'll check them (I only see whether each one is filled in, never the values).
>
> **Where assets come from:** fonts — Fontshare, Open Foundry, Free Design Resources, Typedump, Dirtyline Studio, Google Fonts (licence checked); stock — Pexels, Pixabay, Unsplash, textures.com, brand press kits; SFX — Freesound (CC0 first), ElevenLabs SFX; animations — LottieFiles; style references — Pinterest, Behance, Dribbble (reference-only unless licensed). Everything I draw myself in code (2D/3D motion graphics).
>
> Send me your references and story when ready.

Then wait for the references + story (§2 step 0) and run preflight in parallel.

## 0b. Connecting MCPs (any agent)

Two ways — offer both:
- **Ask the agent (easiest):** the user just says *"connect the Playwright / Firecrawl / ElevenLabs MCP"*. If you can run terminal commands, add it yourself with the agent's CLI (below), reading the key from `.env` — never echo it. Then tell the user to restart/reload the agent session if the new tools don't appear.
- **Manual:** the user pastes the JSON/TOML block into the agent's MCP config file.

| Agent | Add via command | Config file (manual) |
|---|---|---|
| Claude Code | `claude mcp add <name> [-s project] -e KEY=value -- <command> <args…>` · check: `claude mcp list` / `/mcp` | `.mcp.json` in the project (project scope) or `~/.claude.json` |
| Codex CLI | `codex mcp add <name> --env KEY=value -- <command> <args…>` | `~/.codex/config.toml` → `[mcp_servers.<name>]` `command`, `args`, `env` |
| Cursor | Settings → MCP → Add | `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` |
| Claude Desktop | Settings → Developer → Edit Config | `claude_desktop_config.json` |
| VS Code (Copilot agent / extensions) | Command palette → "MCP: Add Server" | `.vscode/mcp.json` |
| Claude.ai / Claude in the browser | Settings → Connectors (remote MCP URLs only) | — no local terminal: use a local agent for rendering |

Server definitions (JSON form used by `.mcp.json` / Cursor / Claude Desktop under `"mcpServers"`; same command/args/env for the CLIs and TOML):
```json
{
  "playwright": { "command": "npx", "args": ["@playwright/mcp@latest", "--user-data-dir", "<project>/../.browser-profile", "--output-dir", "<project>/cache/browser"] },
  "firecrawl":  { "command": "npx", "args": ["-y", "firecrawl-mcp"], "env": { "FIRECRAWL_API_KEY": "<from .env>" } },
  "elevenlabs": { "command": "uvx", "args": ["elevenlabs-mcp"], "env": { "ELEVENLABS_API_KEY": "<from .env>", "ELEVENLABS_MCP_BASE_PATH": "<project>/assets" } },
  "lottiefiles":{ "command": "npx", "args": ["-y", "@lottiefiles/creator-mcp@latest"] }
}
```
Example (Claude Code, key read from `.env` without printing it): `set -a; . ./.env; set +a; claude mcp add -s project firecrawl -e FIRECRAWL_API_KEY="$FIRECRAWL_API_KEY" -- npx -y firecrawl-mcp`.
`uvx` comes with `uv` (`pip install uv`). Freesound / Pexels / Pixabay MCPs are community servers — if none is available or it fails, **skip the MCP and call the REST APIs directly (§0c)**; that is fully supported.
Note: a project-scope `.mcp.json` containing real keys must be gitignored; prefer `-s local`/user scope or env references when the agent supports them.

## 0c. API keys — where to get them, how to store them, how to use them

**Get the keys (all have free tiers):**
| Platform | Where | Env name(s) |
|---|---|---|
| Pixabay | pixabay.com → log in → https://pixabay.com/api/docs/ (key shown on the page) | `PIXABAY_API_KEY` |
| Freesound | freesound.org → log in → https://freesound.org/apiv2/apply → create credentials → you get **Client ID** and **Client secret / API key** | `FREESOUND_API_KEY` (= the client secret / API key), `FREESOUND_CLIENT_ID` (only for OAuth2 original-file downloads) |
| Pexels | https://www.pexels.com/api/ → "Your API key" | `PEXELS_API_KEY` |
| Unsplash (optional) | https://unsplash.com/developers → New application → Access Key | `UNSPLASH_ACCESS_KEY` |
| Firecrawl | https://www.firecrawl.dev/app/api-keys | `FIRECRAWL_API_KEY` |
| ElevenLabs | elevenlabs.io → Developers / Profile → API Keys | `ELEVENLABS_API_KEY` |

**The agent creates the file — the user only fills it in.** Never ask the user to create `.env` themselves.
1. Run `bash scripts/create_env.sh <project>` (copy it from the skill's `scripts/`). It creates `<project>/.env` with comment lines and empty slots for all keys, keeps any values already there, and adds `.env`/`*.env` to `.gitignore`. Without bash, write the same file with your file tool.
2. Tell the user: the **full absolute path** of the file (e.g. `D:\Projects\my-video\.env`), how to open it (any text editor; in VS Code/Cursor click the path; on Windows Notepad, enable "show hidden files" if they can't see a dot-file), which line each key goes on, and the links to get each key (table above). Then: "Paste, **save**, and tell me when done."
3. When the user says it's saved: re-run the script (or `grep -E '^[A-Z_]+=.+' .env | cut -d= -f1`) and report ✅ filled / ⬜ empty per key, **names only**. If a value looks wrong (spaces, quotes, `key=` inside the value), say which line to fix, without quoting the value.
4. Only ask for the keys actually needed for this project's plan; empty optional lines are fine.

**Format** of `<project>/.env` — one `NAME=value` per line, **UPPER_SNAKE_CASE names, no spaces, no quotes, no spaces around `=`**:
```
PIXABAY_API_KEY=xxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
FREESOUND_CLIENT_ID=xxxxxxxxxxxxxxxxxxxx
FREESOUND_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PEXELS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FIRECRAWL_API_KEY=fc-xxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxx
```
`.env` and `*.env` stay in `.gitignore` (the script does this).
**If the user already has a key file** (e.g. `Resources/Platforms-api.env` with lines like `pixabay-api=…`, `freesound client_id=…`, `freesound client_secret=…`): don't ask them to retype anything. Read it, map the names (`pixabay-api`→`PIXABAY_API_KEY`, `freesound client_id`→`FREESOUND_CLIENT_ID`, `freesound client_secret`/`api key`→`FREESOUND_API_KEY`, etc.), and write a normalised `.env` in the project **with a script, without printing values** — use `python3 scripts/normalize_env.py <their file> .env` (also adds `.env`/`*.env` to `.gitignore`) (names with spaces or dashes are not valid env variables, so always normalise). Report only "✅ PIXABAY_API_KEY set" style lines.

**Load + use them** (never put a key in a log, LOG.md, manifest.json, a commit, or chat; mask it as `***` if a command must be shown):
- Shell: `set -a; . ./.env; set +a` · Node: `process.loadEnvFile('.env')` (Node ≥20.12) or `dotenv` · Python: `python-dotenv`.
- **Pixabay** (images + videos, no attribution required but log the page URL): `curl -s "https://pixabay.com/api/?key=$PIXABAY_API_KEY&q=neon+city&image_type=photo&orientation=horizontal&per_page=20&safesearch=true"` → `hits[].largeImageURL` / `pageURL`; videos: `https://pixabay.com/api/videos/?key=$PIXABAY_API_KEY&q=…` → `hits[].videos.large.url`. Download the file to `assets/` (no hotlinking). Limit ≈ 100 req/min.
- **Freesound** (SFX): search with token auth: `curl -s "https://freesound.org/apiv2/search/text/?query=whoosh&filter=license:%22Creative%20Commons%200%22&fields=id,name,username,license,duration,previews,url&page_size=15&token=$FREESOUND_API_KEY"` → download `previews["preview-hq-mp3"]` (good enough for SFX). Original WAV/FLAC needs OAuth2 (`FREESOUND_CLIENT_ID` + secret, user authorises once in the browser). Prefer CC0; for CC-BY log `username` + `url` for credits. Limit ≈ 60 req/min, 2000/day.
- **Pexels**: `curl -s -H "Authorization: $PEXELS_API_KEY" "https://api.pexels.com/v1/search?query=desk+laptop&orientation=landscape&per_page=15"` → `photos[].src.original`; videos: `https://api.pexels.com/videos/search?query=…` → `videos[].video_files[]` (pick width ≥ 1920). Credit photographer.
- **Unsplash**: `curl -s -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY" "https://api.unsplash.com/search/photos?query=…&per_page=15"` → `results[].urls.full`; credit photographer.
- **Firecrawl** (via MCP preferred; REST fallback): `curl -s -X POST https://api.firecrawl.dev/v1/search -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H "Content-Type: application/json" -d '{"query":"clash display font license","limit":5}'`; scrape a page: `/v1/scrape` with `{"url":"…","formats":["markdown"]}`.
- **ElevenLabs** (SFX/music; VO only if the user asks you to generate it): SFX `curl -s -X POST "https://api.elevenlabs.io/v1/sound-generation" -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" -d '{"text":"deep cinematic boom with long tail","duration_seconds":3}' -o assets/sfx/boom.mp3`; TTS `POST /v1/text-to-speech/<voice_id>?output_format=mp3_44100_192`. Uses the user's credits — ask before bulk generation.
- Write small reusable helpers (`scripts/fetch_pixabay.mjs`, `scripts/fetch_freesound.mjs`…) that read `.env`, search, download into `assets/…` and append to `manifest.json` (path, source page, author, license).

## 0d. Demucs (local stem separation — install by default)

Small enough to always install (CPU wheels ≈ 300 MB incl. PyTorch; `htdemucs` weights ≈ 80 MB, cached on first run). Ask once in preflight, then install:
`pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu && pip install demucs soundfile` (Apple Silicon/Linux/Windows all work on CPU; skip the index URL if a CUDA PyTorch is already installed).
Use it for:
- **Reference analysis (§13):** split the reference audio to study the music, SFX and VO separately: `ffmpeg -i ref.mp4 -vn -ac 2 -ar 44100 cache/ref.wav && python3 -m demucs -n htdemucs --two-stems=vocals -o cache/stems cache/ref.wav` → `cache/stems/htdemucs/ref/{vocals,no_vocals}.wav`.
- **Cleaning the user's VO:** if the returned MP3 has music/noise under it, keep `vocals.wav`.
- **Raw footage edits:** separate dialogue from background music to remix/duck it.
Drop `--two-stems` for 4 stems (drums/bass/other/vocals). ~1–2× realtime on CPU; process ≤ 60 s chunks if RAM is low. If `torchaudio` save errors appear, make sure `soundfile` is installed.

---

## 1. Project structure & tracking

```
<project>/
  PROJECT.md        # brief, decisions, approvals, open questions (living doc)
  PROGRESS.md       # live status: phase, done, in progress, next step, open issues, key file paths (read FIRST on resume)
  LOG.md            # timestamped action log: what, why, files touched, result
  manifest.json     # every asset: path, source URL, license, author, duration, used-in
  plan/             # script.md, storyboard.md, shotlist.md, styleboard.png, beats.json
  assets/{footage,images,lottie,sfx,music,vo,fonts}/
  models/           # local model weights
  src/              # scene code (scenes/*.js, fx/*.js, data.js timings, render.js)
  cache/            # matte frames, transcripts, intermediate PNG/frames (deletable)
  renders/          # previews/ (low-res, stills, contact sheets) and final/ (versioned v1, v2…)
```
- **`PROGRESS.md` is mandatory in every project.** Create it during Preflight and update it after every finished step, every user decision, and before any long render. Write it so a fresh session can continue from it alone (chats get long and context is lost). Keep it short and overwrite it, unlike the append-only LOG. Template:
  ```
  # PROGRESS – <project>   (updated YYYY-MM-DD HH:mm)
  Phase: <brief|script|storyboard|style|assets|preview|final|DONE>
  Current version: v3 → renders/final/<name>_v3.mp4
  Done: - …
  In progress: - …
  Next step: <one concrete action>
  Open issues / user feedback not yet fixed: - …
  Key decisions & preferences: - (e.g. no bell SFX, credits required)
  Key files: src/…, plan/beats.json, assets/…
  ```
- When a session resumes (or after context compaction), read `PROGRESS.md` before doing anything else, then the end of `LOG.md`.
- Append to `LOG.md` after every meaningful step. Record license/attribution for every downloaded asset in `manifest.json`.
- Version outputs (`_v1`, `_v2`); never overwrite an approved render.
- Keep timings in one data file (`data.js`/`beats.json`) driven by the transcript, so retiming = edit one file.

---

## 2. Workflow (gates in **bold** need user approval)

0. **References + story (required intake)** – after the kickoff message (§0a), collect: reference videos/links/screenshots, the story/plan (what happens, key message), audience, platform & format, target length, tone, CTA, brand assets, must-haves/must-avoids. If references are given, run §13 (+ Demucs stems, §0d) and present the recipe. Don't continue until you have at least the story and length.
1. **Brief** – goal, audience, platform & aspect (9:16 1080×1920 / 16:9 1920×1080 / 1:1), length, brand (logo, palette, fonts), CTA, references, video type → intensity level (§4). Ask only what's missing.
2. **VO script for ElevenLabs** – write it with the §10 guide: AV two-column script (Audio | Visual) for the plan + one **paste-ready ElevenLabs block** with model, voice and settings. Hook in first 3 s. → **Approve script.** → **The user generates the MP3 and sends it back** (`assets/vo/`). Steps 3+ (and any scene code) start only after the MP3 arrives.
3. **Storyboard / shot list** – per shot: time, VO line, visual, motion, transition, SFX, text on screen. Beat sheet with seconds.
4. **Style board** – palette (hex + roles), fonts, 3–4 still frames rendered from code. → **Approve plan.**
5. **Assets** – **VO intake:** receive the user's MP3 → `ffprobe` (duration, sample rate) + check clipping/loudness (`ffmpeg -af volumedetect`, `ebur128`) → transcribe with word timestamps (faster-whisper) → diff the transcript against the approved script and report missing/changed words or bad pronunciations (ask for a regenerated line if needed) → lock `beats.json` timings to the real audio. If the user explicitly wants to start early, use a temporary guide track and mark the timeline `TEMP` in PROGRESS.md. Then stock, Lottie, SFX, plus visual hunting on Pinterest/any site with the Playwright MCP (§16) for images, textures, footage and references; transcribe with word timestamps; cutout mattes if needed.
6. **Preview** – contact sheets for every scene via `scripts/preview.mjs` (§2b) + a low-res/half-fps preview MP4 with audio. → **Approve preview.**
7. **Final render** – full res, sound mix, loudness, QA checklist (§15). Deliver + update LOG. If a vertical version is wanted, re-lay every scene natively for 9:16 (re-frame, re-place text in safe zones) — never just crop or letterbox the 16:9 render.

Rendering pipeline (default): deterministic `drawFrame(t)` in Canvas/Three.js → headless Chrome via Playwright, step time per frame (no real-time clock) → pipe PNG/JPEG frames into `ffmpeg -f image2pipe -r 30 -i - -c:v libx264 -pix_fmt yuv420p -crf 18` → mux audio. Seeded randomness only.

**Render CLI contract (required, build it on day one):** `src/render.js` must accept `--from <s> --to <s> --fps <n> --scale <0–1> --out <dir> [--jpg]` and render only that range at that size. Every frame depends only on `t` (no timers, no unseeded random, no state carried between frames), so a preview frame is identical to the final frame, just smaller.

## 2b. Fast preview loop (use after EVERY change)

Never check a change with a full render or a few random stills. Things that happen between stills (cards sliding behind text, cropped elements, bad framing) slip through.
1. After editing a scene, run `node scripts/preview.mjs <from> <to>` (defaults: 8 fps, 0.25 scale, 6 columns). It renders only that range, small, and tiles all the frames into one contact sheet at `renders/previews/sheet_<from>-<to>.jpg`, with a timestamp under every frame.
2. View the sheet (one image = the whole move). Check framing and safe area, overlaps, text legibility, easing gaps, pops/flicker and continuity across the cut.
3. Fix → re-run the same range → repeat until clean. Only then move to the next scene.
4. For timing or sound checks, add `--mp4` to get a low-res clip with the mixed audio for that range.
5. Before the final render, run sheets over the whole video (e.g. in 10 s chunks) and fix everything found. Log each loop in LOG.md and update PROGRESS.md.
Target: one loop in under ~20 s. If it's slower, lower `--fps`/`--scale` or shorten the range. Use Motion Canvas/Revideo for code-timeline scenes; GSAP timelines with `.seek(t)` for easing; p5.brush for hand-drawn/ink looks; SVG for crisp icons/UI.

---

## 3. Director / producer knowledge

- **Structure:** Hook (0–3 s) → Problem → Solution → Proof → CTA. Features framed as outcomes ("save 5 h/week", not "has automation").
- **Hook devices:** bold claim, pattern interrupt, question, result-first, visual surprise in frame 1. No logo intro.
- **Proof:** real UI, numbers, testimonials, before/after. Simplify UI (zoom, mask, highlight) rather than invent it.
- **One idea per shot**; on-screen text ≤ 6–8 words; leave reading time (≈ 0.3 s/word + 0.5 s).
- **Pacing:** reels cut every 0.5–2 s; explainers 2–5 s per idea; vary rhythm (fast–fast–hold). Cut on beats/consonants.
- **Shot vocabulary:** wide/medium/close/ECU, insert, OTS, POV; moves: push-in (importance), pull-out (reveal), pan/track (follow), parallax, dolly-zoom (tension), whip pan (transition), orbit (hero product).
- **Editing:** cut on action, J/L cuts (audio leads/lags), match cuts (shape/color/motion), jump-cut dead air, B-roll covers cuts.
- **CTA:** one clear action, shown + spoken, on screen ≥ 2 s.

## 4. Video type → editing intensity

| Type | Intensity | Do | Avoid |
|---|---|---|---|
| Editing showcase / reel / hook / personal brand | 🔥 5 – hyper | flashes, 3D text, rings, glitches, whips, punch zooms, SFX on every beat | dead air, static frames >1.5 s |
| Social ads / UGC | 4 – high | kinetic captions, punch zooms, stickers, emoji, fast cuts | slow intros |
| Educational / tutorial | 3 – medium | highlights, arrows, step counters, diagrams, calm music | effects that cover content |
| SaaS / product explainer | 2 – clarity-first | clean UI animation, focus zooms, cursor, smooth easing, subtle SFX; motion **supports the message** | gimmicks, shaky cams, flashes |
| Corporate / B2B / finance / health | 1 – restrained | lower thirds, fades, slow push-ins, generous whitespace | glitch, neon, hard flashes |

Rule: the more trust/clarity the message needs, the less decorative motion. Each effect must serve attention, emphasis, or transition.

---

## 5. Motion graphics catalogue (code-drawn)

- **Type:** kinetic captions (word pop, karaoke highlight), extruded 3D text, text behind subject (needs matte), 3D ring text orbiting subject, vertical neon words, script + bold font pairing, typewriter, mask reveals, split/scramble text.
- **Shapes/UI:** design-tool selection boxes + handles, cursor clicks, toggles, chat bubbles/DM, notification cards, follow button → "Following ✓" burst, progress bars, counters, charts that draw on.
- **Textures/looks:** halftone, B&W + spot color, paper/torn paper, ink/brush (p5.brush), grain, scanlines, film burn, bokeh, light leaks, neon glow, duotone.
- **Objects:** stickers with curl/peel, polaroids, tape, emoji, arrows (hand-drawn/neon), money/confetti rain, particles, Lottie icons.
- **3D (Three.js):** product orbit, floating cards, depth parallax of cutouts, camera fly-through, extruded logos.
- **Characters:** rigged 2D (bones/IK in Canvas), Lottie characters, consistent model sheet.

## 6. Raw-footage editing effects

Punch zoom (105–120 % on emphasis), smooth zoom-in on key line, whip pan / blur transitions, dutch tilts, shake on impact, white/red silhouette flash (matte), subject cutout + background swap, face/photo collage, captions behind subject, letterbox bars for "cinematic" moments, freeze frame + label, speed ramps, B&W punch-in, color pops, split-screen, zoom-through transitions, glitch/RGB split end cards, torn-paper wipes, ink wipes, jump-cuts removing silence.
Matting: RVM for video (fast, CPU-ok at 512 px), rembg/u2netp for stills, SAM2-tiny when a prompt/click is needed. Cache mattes in `cache/`, feather 1–2 px, erode slightly to avoid halos.

## 7. Animation principles (top motion designers)

- Disney's 12 principles: squash & stretch, anticipation, staging, follow-through/overlap, slow in/out, arcs, secondary action, timing, exaggeration, appeal (+ solid drawing, straight-ahead/pose-to-pose).
- **Easing:** never linear for UI; easeOutCubic/Expo for entrances, easeInCubic for exits, back/elastic only for playful brands. Entrances 200–500 ms, exits faster than entrances.
- **Stagger** related items 40–80 ms; overshoot 5–10 %; settle with small follow-through.
- **Hierarchy & eye-trace:** one focal point per moment; keep the next focal point near the previous one; lead with motion, then text.
- **Continuity:** consistent direction (forward = left→right), consistent easing family, consistent motion "language" per project.

## 8. Color & composition

- **60-30-10:** dominant / secondary / accent (accent = CTAs, highlights only).
- **Contrast:** text ≥ 4.5:1 (WCAG AA; ≥ 3:1 for large text); check value contrast in grayscale.
- **Schemes:** complementary for pop (e.g., teal/orange), analogous for calm, monochrome + one accent for premium. Stick to brand palette; derive tints/shades, don't invent hues.
- **Skin tones** must stay natural when grading; grade all clips consistently (one LUT/curve per project).
- **Composition:** rule of thirds, headroom, lead room in look direction, negative space for text, symmetry for hero shots.
- **Safe zones (9:16):** keep text/faces out of top ≈ 220 px and bottom ≈ 420 px, and right ≈ 140 px (platform UI). Captions around 60–70 % height.
- Max 2 typefaces (+1 script accent). Line length short, tracking tighter on big bold type.

## 9. Sound design

- **Trio:** riser (build) → impact (hit) → whoosh (motion/transition). Layer: sub/low body + mid punch + high sizzle/air.
- **Bigger/heavier = lower pitch & slower**; small/fast = higher & shorter. Match SFX length to motion duration; sync the transient to the visual peak frame (±1 frame).
- **Mapping:** UI clicks/pops/ticks → interface; swish/whoosh → movement & text fly-ins; riser → before reveal; sub drop/boom → big hit/logo; glitch/buzz → glitch FX; camera shutter → flash/freeze; paper/sticker rip → stickers/torn paper; stinger → section change; ambience bed → realism.
- Don't SFX everything at intensity 1–2; at intensity 5, almost every beat gets one, with varied samples (avoid repetition fatigue).
- **Mix:** VO 10–15 dB above music; duck music under VO (sidechain); high-pass SFX that clutter VO; music edits on bar lines.
- **Loudness:** −14 LUFS integrated for social/YouTube, true peak ≤ −1.5 dBTP (`ffmpeg -af loudnorm=I=-14:TP=-1.5:LRA=11`, two-pass). Sources: Freesound (prefer CC0, log attribution), ElevenLabs SFX for custom sounds.

## 10. ElevenLabs voiceover

- Model: **Eleven v4** (or v3) for expressive VO; Multilingual v2 for stable long reads/PVCs where needed.
- **v3/v4: no SSML `<break>`**. Use punctuation: `…` hesitation, `—` short pause, line breaks, short sentences. `<break time="1.0s"/>` only on older models (≤3 s, sparingly).
- **Audio tags** in square brackets before/after a line: `[excited]` `[whispers]` `[sighs]` `[laughs]` `[curious]` `[sarcastic]` `[thoughtful]` `[surprised]` `[warmly]` `[dramatically]` `[impressed]` `[frustrated sigh]`; be explicit (`[low, gravelly voice]`) so tags aren't read as sound effects. Avoid SFX tags (`[applause]`) in VO.
- Tags must fit the voice's character; test 2–3 takes. CAPS = emphasis (sparingly). Write naturally, like a script.
- **Pronunciation:** v4 IPA in slashes `/ˈnoʊʃən/`; or alias/phoneme pronunciation dictionaries for brand names/acronyms. Spell numbers/units as spoken when unsure.
- Generate per scene/paragraph (easier retakes, layering), keep same voice + settings; adjust `speed` instead of rewriting; remove any spoken stage directions in post.
- Example: `[warmly] Most teams lose hours every week… [curious] but what if that just — stopped? [excited] Meet Flow.`

### 10a. Writing the paste-ready ElevenLabs script (deliverable before any build)

**Length → word budget** (natural VO ≈ 2.3–2.6 words/s; leave ≈ 1.5 s at the end for logo/CTA hold):
| Video | Words (VO) | Lines |
|---|---|---|
| 15 s | 30–38 | 4–6 |
| 30 s | 65–75 | 8–12 |
| 45 s | 100–110 | 12–16 |
| 60 s | 135–150 | 16–22 |
| 90 s | 200–220 | 24–32 |
Count the words in the paste block (tags excluded) and state the estimate: `≈ 142 words ≈ 58 s at 2.45 w/s`.

**Writing rules**
- One idea per line; short sentences (≤ 14 words). Line breaks = natural breath pauses; `…` = hesitation; `—` = short beat. Empty line = longer pause between sections.
- Hook in the first line (≤ 3 s, ≤ 8 words). CTA = last line, word-for-word what appears on screen.
- Write numbers, units, symbols, acronyms and URLs **as spoken**: "twenty-four seven", "three x faster", "A-I", "dot com". No emojis, hashtags, markdown, bullets or stage directions in the paste block.
- Tags: max 1 per 1–2 lines, only where the emotion changes; match the voice's character. CAPS on 1 word per section max.
- Brand names/odd words: give an alias spelling ("Notion" → "NOH-shun") or v4 IPA `/ˈnoʊʃən/`, or tell the user to add it to a pronunciation dictionary.
- Model-specific: v3/v4 → punctuation + tags, no `<break>`. Multilingual v2 / Turbo / Flash → no audio tags (they get read aloud); use `<break time="0.6s"/>` sparingly instead.
- Keep on-screen keywords (for kinetic type) in a separate list, not in the paste block.

**Deliver exactly this format:**
````
## VO script – <project> (v1)
Target: 60 s · ≈ 142 words ≈ 58 s
Model: Eleven v3 (or v4)      Voice: <library voice name or description, e.g. "deep, calm male narrator, documentary, American">
Settings: Stability 40–50 % (Natural) · Similarity 75 % · Style 0–20 % · Speed 1.0 · Speaker boost on
Export: MP3 44.1 kHz 192 kbps (mp3_44100_192) · one file for the whole script (or one per section if marked)

--- PASTE INTO ELEVENLABS (copy everything between the lines) ---
[thoughtful] Nobody drew this.
Not one line… not one frame.

[curious] So where did it come from?
…
[warmly] Start yours today — link below.
--- END ---

On-screen keywords: NOBODY · DREW · THIS · …
Pronunciation notes: …
Alt hook (variant B): …
````
Also give a **variant B** of the hook (and CTA if useful) so the user can A/B pick.

**Tell the user how to generate it:** open elevenlabs.io → Text to Speech → choose the model and voice → set the settings → paste the block → Generate 2–3 takes → download the best as MP3 → send it to you / put it in `assets/vo/vo_v1.mp3`. If one line sounds wrong, regenerate only that line (paste it alone with the same settings) and send it as `vo_line07_fix.mp3` — you'll splice it on a pause. Don't edit the text after approval without telling you (timing and captions come from it).

## 11. 3D motion design — "go 3D when it matters"

Default to crisp 2D; **switch to 3D for hero moments** (reveal, product, stat, logo, transition) — max 1 big 3D beat per 5–10 s at intensity ≤3.
- **2D→3D pop:** a flat layer (card, screenshot, text, photo) tilts in perspective (`rotateX 10–25°`, `rotateY 15–35°`), gains thickness (extrude 8–30 px, darker side faces), shadow + rim light, camera dolly/orbit; then flattens back to 2D on the next beat. In Canvas fake it with 2.5D (perspective/homography + stacked offset copies for depth); in Three.js use planes textured from Canvas (`CanvasTexture`) so 2D art and 3D share one pipeline.
- **3D→2D collapse:** shaded 3D object (monitor/phone) morphs into flat line-art outline (black 6–10 px stroke, white fill) → camera pushes *through* the screen into the next scene (recipe C).
- **Toolkit:** Three.js (`ExtrudeGeometry`/`TextGeometry` for type, `MeshPhysicalMaterial` + `RoomEnvironment` for chrome/glass, `EffectComposer` bloom/DOF/grain), card stacks & orbits, depth parallax of cutouts (subject z=0, text behind at z=−1, particles z=+1), cylindrical ring text, hyperspace streak tunnels, extruded logos, 3D picture frames, floating UI windows in perspective.
- **3D camera language:** slow push (0.5–2 %/s) on holds; fast dolly + motion blur for transitions; orbit 20–40° for products; rack focus (DOF) to switch attention; FOV 30–45° = premium, 60–75° = energy.
- **Render:** same deterministic `drawFrame(t)` → headless Chrome WebGL (`--use-angle=swiftshader` if no GPU) → ffmpeg. Fake motion blur by averaging 4–8 sub-frames. Heavy scenes: Blender headless (`blender -b scene.blend -P build.py -a`) if installed.

## 12. Typography & kinetic type

- **Pairing systems that work:** (a) ultra-thin grotesk filler words + heavy/black keyword (recipe A); (b) chunky black grotesk + handwritten marker + script accent (B); (c) one geometric display sans, contrast by scale only (C, D); (d) serif headline + small sans UI labels for premium SaaS cards.
- **Hierarchy by scale, weight, color — not by number of fonts.** Keyword = 2–4× filler size; ≤1 keyword per caption group; keyword gets the accent color/gradient/glow.
- **Kinetic vocabulary:** per-word blur-in (blur 12→0 px, opacity 0→1, y +20→0, 180–250 ms, easeOutCubic); per-letter stagger 20–40 ms; tracking collapse (0.6 em → 0, logo lockups); word swap in the same slot ("Zero Alignment → Zero Momentum"); scramble/decode (random glyphs → final, mono); counter roll (38→48→50, ease-out, tick SFX); text behind subject (matte); text on 3D path/arc; directional echo trail (3–6 offset copies in accent color, falling opacity = colored motion blur, D); letter-by-letter dissolve-out; type morph into a circle badge (B); variable-font weight/width animation.
- **Placement:** captions orbit the subject (near face/hands), never cover eyes/mouth; change position per group to drive eye-trace; stay inside safe zones.
- **Finish:** 2-stop vertical gradient fills, subtle bevel/drop shadow (0 4 12 rgba(0,0,0,.35)), glow = blurred copy behind (8–24 px, accent, 60–80 %), 3–6 % grain over type for film looks.

### Font sourcing (Firecrawl → `assets/fonts/`)
Search/scrape these first. Free or free-for-personal — **always read the license, log it in manifest.json, ask the user if commercial use is unclear.**
| Site | Use for |
|---|---|
| https://freedesignresources.net/category/free-fonts/ (Free Design Resources) | display, condensed, script freebies |
| https://open-foundry.com/ | curated open-source (OFL) typefaces |
| https://www.fontshare.com/ | ITF free pro fonts (Satoshi, Clash Display, General Sans, Cabinet Grotesk, Switzer…) |
| https://www.typedump.com/ | variable, display, pixel, mono free fonts |
| https://play.typedetail.com/ (Font Playground) | test variable-font axes (wght/wdth/slnt) for kinetic type |
| https://dirtylinestudio.com/freebies/ | free display/brand fonts |
| Google Fonts (fallback) | OFL staples: Inter, Poppins, Anton, Archivo Black, Permanent Marker, Caveat Brush, Allura, Space Mono |

Workflow: `firecrawl_search "<style> font site:fontshare.com"` → `firecrawl_scrape` the font page for download link + license → `curl -L -o` → unzip `.ttf/.otf/.woff2` → register via `@font-face`/`FontFace` and **await `document.fonts.ready` before rendering frame 0**. Never ship a font whose license you couldn't verify.

## 13. Reference-video protocol (if the user attaches references, use them)

Always ask: *"Do you have a reference video or look? Attach it — I'll reverse-engineer it."* Analyze **max 15 s** per reference (`scripts/analyze_ref.sh ref.mp4`):
1. `ffprobe` (size, fps, duration); frames at 4 fps → timestamped contact sheets; 10 fps strips around cuts (`select='gt(scene,0.3)'`); full-res stills of key frames.
2. Audio: spectrogram, transient list (low vs high band), word timestamps (faster-whisper). Optional Demucs to split VO / music / SFX.
3. Write a breakdown: format & grade · type system (fonts, weights, hex colors, sizes) · per-shot timeline (t, visual, motion, easing, transition) · recurring devices · SFX map (t → sound → what it syncs to) · cut rhythm (avg shot length, BPM).
4. Turn it into a recipe (format of §14), confirm with the user, then build.

## 14. Reverse-engineered reference recipes (build these without seeing the videos)

### A · Premium talking-head caption reel (real-estate agent, 9:16, intensity 3–4)
- **Footage:** 85 mm-look shallow DOF, soft overcast light, warm-green natural grade; subject centered, medium/full shot, often walking toward camera; new location every ~3 s (bench → bridge → deck → trail), hard cuts on sentence starts.
- **Captions:** 1–3 words at a time at chest/face height *around* the subject. Filler = ultra-thin grotesk (Helvetica Neue Thin / Inter 200), white 80 %, soft shadow. Keyword = heavy grotesk 2–3× larger with **gradient fill + slight bevel**: "secret" steel-teal (#2E7F95→#A7DCE6), "CLIENTS" caps lilac (#A35BC9→#E3B8F3), "2026," teal 3D, "50 HOMES" green, "2 THINGS" neon yellow #FFE14A with orange glow #FF8A00 (blur ~20 px) **placed behind the head** (matte).
- **Motion:** words blur-in ~200 ms, leave by letter-by-letter dissolve; counter rolls 38→48→50 while 6 rounded house-photo cards (2 px white border, 12 px radius, shadow) pop around her in an arc (scale 0→1.08→1, stagger 80 ms); social-post screenshot as tilted 3D plane (rotateZ −6°, slight perspective) = proof B-roll; pill buttons (black fill, 2 px glowing yellow border, bold white "Pricing." / "Presentation.") grow dot → circle → pill on the spoken word; before/after thumbnail cards with tiny labels float around her on "marketing/content"; frame-blend ghost whip between takes.
- **SFX:** quiet music bed under VO; low boom/sub hit on the first keyword ("CLIENTS" ≈1.8 s); tonal tick/shimmer run during the counter; airy shimmer whoosh into "so let's talk about how"; soft pops per pill/card; nothing on filler words.

### B · Cinematic storyteller documentary edit (creator origin story, 16:9 letterboxed, intensity 5)
- **Structure:** 1–2 s per visual idea; every sentence = a new world; 1-frame black cuts as punctuation; letterbox bars.
- **Sequence of looks:** dim warm talking head (bold white caption + yellow keyword) → cream halftone paper #F1E8C8 with **gobo plant-leaf shadow** + grain; red distressed bold type "STORY" #B3202C inside a **design-tool selection box** (dashed bounds, square handles) that rotates and morphs into a circular badge → black bold sans "OF HOW THREE YEARS" builds word by word top-left → **torn-paper window** opens onto footage → handheld room B-roll with **3D extruded white chunky words** ("a kid", "went from") standing in the room with shadows → yellow script "ZARA" under "Folding clothes at" → **dream collage** (Mt Fuji, torii, pagoda, Tokyo tower, green hills, cut-out subject walking in) with yellow handwritten marker words (Permanent Marker / Caveat Brush, #FFD84A, dark outline) on curved paths, one per spoken word → black void, **3D picture frame** under spotlight, slow dolly, "At 17" → push into the photo: purple grunge paper #7B6FB0 with scratches, yellow "he was OBSESSED", red bold marker "THING" → **RGB slice glitch** → **hyperspace light-streak tunnel** (magenta/red/purple) behind dark silhouette, chrome 3D "CREATING" → **B&W archival film** (hands reaching for a dollar bill, flicker, vignette) with tiny yellow italic subtitles → **whip blur** back to A-roll with left-aligned stacked white bold captions, highlight word in yellow heavy condensed (Anton-like, glow).
- **SFX:** music + VO; paper rustle/swish on the paper scenes; whoosh on each world change (≈4.6, 6.5, 7.7 s); glitch burst on the slice; riser into "CREATING"; projector crackle bed on B&W; whip whoosh into A-roll. Hits land on the *first frame* of each new world.

### C · SaaS product launch, Slack-style (16:9, intensity 2–3, clarity-first but premium)
- **Opening:** desaturated warm grass-field photo (grain, soft vignette) as calm canvas; thin mono line scramble-decodes "Life. But organized."; glowing brand-color orbs (blur ~10 px) drift in and **condense into app icons** that line up in a glass dock (rounded pill, backdrop blur, soft shadow).
- **Moves:** vertical camera tilt with heavy motion blur (dock stays) = transition; macro push-in on the dock with **DOF** blur; cursor hovers icons (magnify 1.15×); click → real product UI windows fly out as **3D tilted cards** fanning from the dock; a video-call window on white with soft blue shadow.
- **2D↔3D:** gray 3D monitor flies in rotating (rotateY ~70°→0, ease-out) while concentric brand-color circles burst behind (red→yellow→blue→green, 120 ms stagger); monitor then **flattens into black line art** and the camera pushes through the frame (scale >300 %) to white.
- **Type:** wide geometric sans (General Sans / Clash-like). Small bold "Your team lives in too many tools" types on letter by letter → giant cropped "Zero" bleeding off frame over a **blurred brand-gradient blob** (teal #3CC9B0, yellow #F7D21E, magenta #E01E6A) rising from the bottom → shrinks to small "Zero Alignment" → word swap "Zero Momentum" → logo enters big with overshoot and settles small, wordmark "S l a c k" letters appear widely spaced, then **tracking collapses** into the lockup.
- **SFX:** soft music with low sub pulses (~0.33 s); air whoosh on the tilt (≈2.1–2.6 s); descending tonal sweeps on UI zooms; glassy clicks on dock hovers; one clean impact + reverb tail on the logo, then near-silence.

### D · Brand-agency kinetic promo, Frontify concept (16:9, intensity 4, beat-synced)
- **Palette:** off-white #FAF8FA ↔ black #0A0A0A alternating per cut, one accent orange #FF6A1A; one geometric display sans (Satoshi / General Sans Bold-like).
- **Type:** "Your" huge with an **orange motion-blur echo** offset below-right → cut to black: tiny "Your" centered with a blurred orange glow wave rising from the bottom → white "Branding" smearing in horizontally → small "Your Branding is" builds → "Messy" in white over a dark grid of dimmed brand work.
- **Card snake:** 20–30 copies of brand-collateral cards trail along a bezier arc behind the word (time-echo: each copy is the card delayed 1 frame and slightly smaller), sweeping left→right→down.
- **Logo:** outline icon alone on white (stroke draw-on) → wordmark over blurred lifestyle photo.
- **Stack → grid → UI:** rotated card stack shuffles on every beat, then **explodes into a 4×2 grid** with 3D Y-flips and folder labels (Mockups, Website UI, Banners…); camera zooms into one label → it becomes a chip in a search bar; text types with cursor; click "Search" → background inverts to black, button turns orange gradient, squashes into a circle with ↑ arrow → zoom out reveals card "Explore Templates" (serif title, selection box).
- **SFX/rhythm:** music only, no VO; sparse whoosh-pops on the opening words; noise riser ≈3.6→5.5 s into a bass drop on the logo; then **a cut/shuffle every beat (~0.31 s ≈ 96 BPM eighths)**; UI click + soft pop on the button morph; typing ticks.

### Shared taste from all four
1. One accent color (or brand gradient) carries all emphasis. 2. Keywords get treatment; filler stays quiet. 3. Every sentence = a new visual idea; cut on the first syllable. 4. 2D world, 3D only at peaks. 5. Real proof (UI, posts, photos) floats in as cards. 6. SFX mark *changes* (new world, reveal, click), not every word; music ducks under VO; silence around the logo hit sells it.

## 15. QA checklist before delivery

- [ ] Plan approved, preview approved (logged in PROJECT.md)
- [ ] Hook lands in ≤ 3 s; CTA visible ≥ 2 s
- [ ] VO is the user's final MP3; transcript diff vs the approved script is clean (or differences approved)
- [ ] Captions match VO, no typos, inside safe zones, contrast ≥ 4.5:1
- [ ] SFX synced (±1 frame), VO intelligible over music, −14 LUFS / −1.5 dBTP
- [ ] No halos on cutouts, no flicker, no dropped frames; `ffprobe` duration/fps/resolution correct
- [ ] H.264 yuv420p, AAC 48 kHz, faststart (`-movflags +faststart`)
- [ ] Contact sheets checked over the full duration (§2b), no framing/overlap issues left
- [ ] manifest.json licenses complete (no `reference-only` asset in the final without user OK); LOG.md updated; final saved as new version
- [ ] Font licences saved next to the fonts in `assets/fonts/` and listed in the credits
- [ ] No API key values in any log, manifest, script or rendered credit
- [ ] Vertical/other aspect versions are native re-layouts (not crop/letterbox) and checked with contact sheets
- [ ] PROGRESS.md marked `Phase: DONE` with final file path, specs and credits
- [ ] Offer cleanup: move `cache/` (previews, logs, intermediates, stems) to the OS trash/Recycle Bin — never permanently delete; keep src, assets, renders

## 16. Visual asset hunting with the Playwright MCP (browse any site, grab assets yourself)

Use this whenever the plan needs an image, texture, photo, footage clip, icon, mockup or style reference that the API MCPs (Pexels/Pixabay, LottieFiles, Freesound) don't cover well — e.g. Pinterest moodboards, Behance/Dribbble shots, brand sites, product pages, font specimen pages, free texture sites. **Do it yourself; don't ask the user to search.**

**Source order:** (1) API MCPs with clear licenses (Pexels/Pixabay/Lottie/Freesound) → (2) free-license sites browsed visually (Unsplash, Pexels web, Pixabay web, textures.com free, brand press kits, the user's own sites/socials) → (3) Pinterest/Behance/Dribbble/any site, mainly for **references and moodboards**, or for final use only when the original source's license allows it.

**Loop (per asset need):**
1. **Write the brief first** (1 line in PROGRESS.md): what, where it's used, style (from the styleboard), aspect/size, and 3–5 search queries (vary wording: "lime green translucent keycap macro", "jelly keycap close up"…).
2. **Open + search:** `browser_navigate` to the site → dismiss cookie/consent pop-ups → `browser_type` the query into the search bar → `browser_press_key Enter` → `browser_wait_for` results.
3. **Look at the results:** `browser_take_screenshot` (scroll 2–3 times with `browser_press_key PageDown` for more). Judge visually against the brief: style match, colour/palette, lighting, angle, resolution, no watermark, no text/logos in the way, fits 9:16 crop. Use `browser_snapshot` to get element refs for clicking.
4. **Open the best 3–6 candidates** (`browser_click`), screenshot each detail page, check size/quality, author and the **original source link** (on Pinterest a pin usually links to the origin site — follow it; credit and license live there).
5. **Download the full-resolution file:**
   - Prefer the site's own Download button (saves to the MCP `--output-dir`, then move to `assets/…`).
   - Otherwise read the media URL via `browser_evaluate` (e.g. `() => [...document.images].map(i => i.currentSrc).filter(u => u.includes('pinimg'))`) and fetch it with the terminal: `curl -L -o assets/images/<name>.jpg "<url>"`. Pinterest: swap the size folder (`/236x/`, `/474x/`, `/736x/`) for `/originals/` to get the largest version.
   - Video: take the `<video>` src or the `.m3u8` from `browser_network_requests` → `ffmpeg -i "<m3u8>" -c copy assets/footage/<name>.mp4` (or `yt-dlp "<page url>"` if installed).
6. **Verify:** `ffprobe` (resolution, duration, codec), view the file, reject low-res/blurry/watermarked ones, remove duplicates. Name files descriptively (`keycap_lime_macro_01.jpg`).
7. **Show the picks:** build a contact sheet (`magick montage assets/images/new_*.jpg -tile 4x -geometry 400x400+8+8 renders/previews/assets_<topic>.jpg`) and present it with source links; the user approves before anything is used in a final render.
8. **Log:** every file → `manifest.json` (path, page URL, direct URL, author, license, `"use": "final" | "reference-only"`) + a LOG.md line.

**Logins & safety:** if a site needs sign-in (Pinterest often does), ask the user to sign in themselves in the Playwright browser window (the persistent `--user-data-dir` keeps them logged in next time); never ask for passwords in chat. Respect the site's terms and robots rules, go slowly (no bulk scraping, ≤ ~30 downloads per session unless asked), never remove watermarks or bypass paywalls/DRM.
**License rule:** Pinterest/Behance/Dribbble images belong to their creators. Without a clear license at the original source, mark the file `reference-only` — use it for style matching, moodboards and §13-style analysis, then recreate the look in code — and ask the user before putting it in a published video.

---
name: studio-setup
description: Sets up the creator's video editing studio, for shorts and YouTube videos, on their computer and in their project - tools, the video-agent/ folder, the Remotion studio, the creator's voice.md, permissions, and the optional accounts (Treg for Instagram, TikTok and YouTube, an ElevenLabs key, Codex). Use when the user says setup, onboarding, install, "start here", configure, connect my account, Treg, first time using studio-script, short-editing, publish or any video skill, or wants to update their voice, niche, CTA or brand color. Checks Node, ffmpeg, yt-dlp and git with install commands for macOS, Windows and Linux, writes voice.md from their own videos or a short interview, pre-approves the tool commands in .claude/settings.json.
argument-hint: "[tools | studio | voice | permissions | treg | keys]"
allowed-tools: Bash(node -v) Bash(ffmpeg -version) Bash(ffprobe -version) Bash(yt-dlp --version) Bash(deno --version) Bash(git --version) Bash(codex --version) Bash(treg --version)
---

# Studio Setup

Ten minutes, once. At the end the creator has:

- the tools the other skills call, installed and checked,
- `video-agent/voice.md`: who they are, how they talk, what they believe, what they can prove. Every script is written from it,
- the editing studio ready, so the first edit starts right away,
- permission rules, so Claude can run ffmpeg, yt-dlp and Remotion without asking each time,
- if they want: their accounts connected through Treg (audit and publishing), and the keys for translation and images.

## How to run it

- Talk in the creator's language. Simple words, no jargon.
- One question per message. Offer choices when you can, recommended first.
- Never invent anything about them: a fact you don't have becomes a question or a `{{placeholder}}`.

## 1. Tools

Run the checks and show one line per tool (✓ version, or ✗ missing):

```bash
node -v
ffmpeg -version
yt-dlp --version
deno --version
git --version
```

| Tool | Used by | macOS | Windows | Linux |
|---|---|---|---|---|
| Node 18+ | short-editing (Remotion) | `brew install node` | `winget install OpenJS.NodeJS.LTS` | nodejs.org or your package manager |
| ffmpeg | short-editing, steal, clips, short-translate, publish | `brew install ffmpeg` | `winget install Gyan.FFmpeg` | `sudo apt install ffmpeg` |
| yt-dlp | studio-script viral, steal, clips, voice.md from videos | `brew install yt-dlp` | `winget install yt-dlp.yt-dlp` | `pipx install "yt-dlp[default]"` |
| deno | yt-dlp on YouTube (it needs a JavaScript runtime) | comes with yt-dlp | `winget install DenoLand.Deno` | `curl -fsSL https://deno.land/install.sh \| sh` |
| git, build tools | short-editing (gets the Remotion template, builds whisper.cpp) | `xcode-select --install` | `winget install Git.Git` | `sudo apt install git build-essential` |
| Codex (optional) | codex-images | `npm i -g @openai/codex`, then `codex login` | same | same |

Give the commands for what is missing and let them run them (or run them yourself if they say so). Scripting-only users (studio-script, its `viral` mode included) only need yt-dlp and deno. Codex is only for `/codex-images` and needs a ChatGPT plan; skip it if they don't want images.

- Windows: after `winget`, close and reopen the terminal (and Claude Code), or the new commands are not found.
- YouTube changes often. When yt-dlp fails on a link that plays in the browser, update it first (`brew upgrade yt-dlp`, `winget upgrade yt-dlp.yt-dlp`, `pipx upgrade yt-dlp`).

## 2. The folder

Create it at the root of the current project:

```text
video-agent/
├── voice.md      who they are and how they talk (step 4)
├── swipe.md      hooks that worked in their niche (`/studio-script viral`)
├── audit.md      what works on their own Instagram (insta-audit)
├── audits/       full Instagram reports, one folder per account and run (insta-audit @handle)
├── log.md        one line per script written, so nothing repeats
├── scripts/      one file per week (studio-script)
├── takes/        raw recordings (phone, camera, webcam, screen)
├── styles/       styles copied from other creators (steal): <name>.md + its stills, sfx, stickers
├── edits/        one folder per edited video (short-editing): final.mp4, post.md, cover.jpg, published.md
├── repurpose/    one plan per long video (clips)
├── images/       generated images not tied to a video (codex-images)
├── studio/       the Remotion project (step 3)
├── .env          their API keys, never shared (step 6)
└── .tmp/         scratch files, deleted after each run
```

`log.md` starts with `# Script log`, `swipe.md` with `# Swipe file`.

If the project is in git, add these lines to its `.gitignore` (videos are heavy; the text files stay tracked):

```gitignore
video-agent/takes/
video-agent/edits/**/*.mp4
video-agent/studio/public/
video-agent/studio/out/
video-agent/studio/node_modules/
video-agent/studio/whisper.cpp/
video-agent/.tmp/
video-agent/.env
```

`video-agent/.env` holds keys: it must be ignored even if they skip the rest.

## 3. The studio

The editing studio (Remotion, whisper.cpp for the captions, a speech model) takes 5 to 15 minutes and about 2 GB to set up. Ask: now (recommended if they will edit soon, the first edit then starts right away), or later (short-editing does it the first time it runs).

Now: run step 2 of `short-editing` ("The studio"), including the `Short` and `Wide` compositions and the `npx tsc --noEmit` check. Say what is downloading and how big before starting. Only for short-editing, clips and short-translate; scripting-only users skip it.

## 4. voice.md

First the two settings at the top of the file: the language they record in, and their brand color (the accent of captions and cards; default `#FFD400`, a yellow that reads on any footage). Then ask how to build the rest:

1. **From their videos** (recommended when they have posted before): 3 to 5 links of their best talking videos (YouTube, Shorts, TikTok, Instagram reels). Pull the transcripts (`<lang>` = their language code: `en`, `fr`, `es`):
   ```bash
   yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "<lang>.*" --sub-format vtt -o "video-agent/.tmp/%(id)s.%(ext)s" "<url>"
   ```
   Read them and fill the template from what they actually say: their real phrases, their pace (words ÷ minutes of speech), the words they repeat, the way they open and close. Then ask only what the transcripts can't tell (positions, proof, off limits, the ask). Delete `video-agent/.tmp/` after.
   YouTube links almost always give a transcript. TikTok sometimes does, Instagram almost never: for those, ask for a YouTube link or switch to the interview.
2. **From an interview**: ask the template's questions one at a time, in plain words ("What do you believe that most people in your niche get wrong?").

Either way, ask them to paste 3 short texts they wrote themselves, before any AI tool (a caption, a message, an email). They go in "Real samples" and teach the scripts their rhythm.

Write `video-agent/voice.md` from [references/voice-template.md](references/voice-template.md). Then read it back to them in 5 lines and ask what is wrong. A voice file is never finished: say they can run `/studio-setup voice` any time to update it.

## 5. Permissions

The other skills run the same few commands again and again. Pre-approve them for this project. Show the rules, ask, then **merge** them into `.claude/settings.json`. Create the file if it is missing. Keep every key and rule already there, and never remove anything.

```json
{
  "permissions": {
    "allow": [
      "Bash(yt-dlp *)",
      "Bash(ffmpeg *)",
      "Bash(ffprobe *)",
      "Bash(npx remotion *)",
      "Bash(node sub.mjs *)"
    ]
  }
}
```

- Only these. Never add `Bash(*)`, `Bash(rm *)`, `Bash(curl *)` or a rule for a whole interpreter (`Bash(node *)`, `Bash(python *)`).
- Rules in the shared `settings.json` apply once the folder is trusted. A creator who keeps this project in git and doesn't want to share the rules can use `.claude/settings.local.json` instead (same format, personal).
- Each skill also lists its own commands in its `allowed-tools`, which covers the turn the skill runs in. These rules cover every other turn.

## 6. Accounts and keys (optional)

Three things, each only if they want the skill that needs it. Ask once, in one message:

| For | What | Cost |
|---|---|---|
| `/insta-audit` and `/publish` | Treg, with their Instagram, TikTok and YouTube connected | free on their own accounts |
| `/short-translate` (and `/steal`'s music level and sound effects, optional) | an ElevenLabs API key | their ElevenLabs plan |
| `/codex-images` | Codex logged in with their ChatGPT account | their ChatGPT plan |

**ElevenLabs**: they create a key at elevenlabs.io/app/settings/api-keys and paste it themselves into `video-agent/.env` as `ELEVENLABS_API_KEY=...` (create the empty file and open it for them). Never ask for a key in the chat. Check it is there without printing it: `grep -c ELEVENLABS_API_KEY video-agent/.env`.

**Codex**: `codex --version`, then they run `codex login` (browser, "Sign in with ChatGPT").

### Treg

yt-dlp reads YouTube for free. TikTok and Instagram hide their numbers from scripts, a creator's own stats sit behind their login, and posting needs their accounts. [Treg](https://treg.to) fills that gap: their own accounts connected once (stats and publishing, free), other creators' public numbers for about $0.001 a call. New verified accounts get $1.00 of credit once, enough for hundreds of calls.

Two ways to plug it in:

- **CLI**, macOS and Linux. It needs uv (recommended, it fetches the right Python), or pipx or pip with Python 3.12 or 3.13. There is no Windows installer.
  ```bash
  curl -fsSL https://treg.to/install.sh | sh
  treg login
  ```
  `treg login` opens the browser (GitHub, Google or an email code).
- **MCP**, any OS, nothing to install: `claude mcp add --transport http treg https://treg.to/mcp/`, then `/mcp` to sign in. Each `treg catalog search`, `catalog get`, `call` and `balance` below becomes the MCP tool `catalog_search`, `catalog_get`, `call` or `balance`.

**Their own accounts** (connecting needs the CLI). `--capability post` asks for the rights to read their stats and to post; posting still waits for their yes on each video:

```bash
treg connections connect --provider instagram --capability post
treg connections connect --provider tiktok --capability post
treg connections connect --provider youtube --capability post
treg connections ls
```

Each `connect` opens the platform's own login; they approve it there. Connect only the platforms they post on. Instagram needs a professional account (Creator or Business, a free switch in the app: Profile → menu → Account type and tools). Treg prints tips on stderr: add `2>/dev/null` when you read its JSON.

Instagram connected: offer `/insta-audit` right after, it is the best first look at what works for them.

**How every Treg call works**, the rule for all the skills:

1. `treg catalog search "<what you want to do>"`: describe the job, not a vendor ("list a TikTok account's videos with view counts").
2. `treg catalog get <id>`: the parameters and the **price**. Say the price before calling. Their own connected accounts are marked free.
3. `treg call <id> --query key=value`. A failed call is not charged. `treg balance` shows what is left; a 402 error means the balance is empty.

Permissions: add only the free, read-only commands, so every paid `treg call` still asks first:

```json
"Bash(treg catalog *)",
"Bash(treg balance)",
"Bash(treg connections ls)"
```

## 7. Wrap up

Show what is ready (✓ or skipped, one line each) and the path forward. They can also just type `/editing <what they want>`: it picks the right skill.

1. `/insta-audit`: what works on their own Instagram (fills audit.md).
2. `/studio-script viral`: what works in their niche (fills swipe.md; once a month).
3. `/studio-script`: this week's scripts, hooks first, humanized.
4. Record them: phone, camera or webcam, one take per script, saved in `video-agent/takes/<slug>.mp4`.
5. `/short-editing`: a short (vertical) or a full YouTube video (horizontal).
6. `/steal`: a creator's reel they love into a style `short-editing` can use.
7. `/clips`: a long video into finished shorts.
8. `/short-translate`: a take in another language, in their voice.
9. `/codex-images`: thumbnails and covers.
10. `/publish`: YouTube, Instagram and TikTok.

## Later

`/studio-setup <part>` jumps to one part: `tools`, `studio`, `voice` (rebuild or update voice.md), `permissions`, `treg`, `keys`.

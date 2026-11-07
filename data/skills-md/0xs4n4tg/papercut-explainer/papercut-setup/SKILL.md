---
name: papercut-setup
description: Install, check or upgrade the papercut toolchain. Runs the doctor, asks how much to set up (Minimal, Standard, Full), then runs install.sh with flags and fixes dependency errors. Use for "set up papercut-explainer", "install papercut", "check my papercut install", "set up the voice", "why won't it render".
---

# Papercut setup

A guided wrapper around `install.sh`. It checks what is installed, asks how much the user wants, runs the installer non-interactively and reports. Use it whenever another papercut skill finds something missing.

## Preflight

- Find the repo root (where `install.sh` lives): `readlink` on the installed skill folder ends in `<root>/skills/papercut-setup`. Look in each harness's skills folder in turn (the table is `harnesses.sh`; typically `~/.claude/skills`, `~/.agents/skills`, `~/.config/opencode/skills`, or the same under `<project>/`). Failing that, `PAPERCUT_HOME=` in `${XDG_CONFIG_HOME:-~/.config}/papercut-explainer/config.env`. If neither exists, the skills probably came from `npx skills add` (skills only, no library). Ask where to clone the repo (default `~/papercut-explainer`), run `git clone https://github.com/0xS4N4TG/papercut-explainer <dir>`, and use that as the root. The installer then replaces the copied skill folders with links into the checkout (it backs up real folders first). Never guess a path.
- Run every `install.sh` command from that root. It needs bash, and macOS or Linux (Windows: use WSL).
- The installer's own prompts need a terminal, which the agent's shell tool lacks. Always pass `--yes` and the answers as flags. Tell the user they can run `./install.sh` themselves for the interactive menu.

## 1. Doctor

```
./install.sh --doctor
```

Add `--project DIR`, `--skills-dir DIR` or `--target <names>` if the skills went somewhere other than the detected defaults; the doctor only looks where you point it, and with no `--target` one complete install location is enough. It prints `[ok]`, `[--]` (missing) or `[!!]` (wrong). Summarise it in plain words:
- skills installed, config file and `PAPERCUT_LIB`
- node 20+, npm, ffmpeg, python3
- Remotion agent skills, Python tools (numpy + Pillow)
- voice: `qwen_tts` importable, a CustomVoice model in the Hugging Face cache
- library files present

Then say which install mode that adds up to (see `papercut-explainer`, Install modes).

## 2. Ask

Ask only what is still open, in one call (your agent's question tool, for example AskUserQuestion in Claude Code). Run `./install.sh --dry-run --mode minimal --yes` first if you need to know which harnesses it detected (`--target auto`, the default):

| Question | Options |
|---|---|
| How much? | **Minimal**: skills only, seconds. **Standard**: render with a placeholder voice, ~0.7 GB and a few minutes. **Full**: Standard + local voiceover, +4-6 GB (a 1.5 GB venv plus a 2.3 or 4.2 GB model) and a 2-minute smoke test. **Custom**: pick components. |
| Which agents? | **Detected on this machine** (default, `--target auto`; Claude Code if none), a list such as `--target claude,codex,gemini`, or `--target all`. Names are in `harnesses.sh`; the README's *Works with* table says which are tested. |
| Where do the skills go? | User-wide (the default) or one project (`--project DIR`). |
| Copy or link? | Symlink (default, updates with `git pull`) or `--copy` (a snapshot). |
| Scene-agent model, per agent with file subagents (`claude`, `opencode`, `codex`, `gemini`; skip the rest)? | One question per selected agent, each with **Inherit** (use the session model) as an option. Claude Code: **Sonnet** (default: cheapest, what the scene agents were tuned on) · **Opus** (strongest; every parallel scene agent bills at Opus rates) · **Haiku** · Inherit. Maps to `--claude-model sonnet\|opus\|haiku\|inherit\|<id>`. Other agents: default **Inherit**, or a model id in that agent's own format (opencode `provider/model-id`, for example `anthropic/claude-sonnet-5-5`; Codex and Gemini plain ids). Maps to `--opencode-model M` or `--agent-model codex=M`. |
| Another provider's model (DeepSeek and others)? | Only if the user asks. Connect the provider inside the agent first (OpenCode `/connect`; Codex `config.toml` provider; Claude Code's `ANTHROPIC_*` variables), then pass its model id as above. The README's *Models other than Claude* section has the steps and the DeepSeek ids. Say plainly that it is untested end to end and that weaker models cost more QA rounds. |
| TTS model size (Full) | 1.7B, better prosody, ~4.2 GB (default). 0.6B, lighter and faster, ~2.3 GB. |
| Voice-clone model (Full) | No (default), or `--with-clone`: the Base model of the same size again. |

Confirm before any multi-GB download. On a machine with no GPU (not Apple Silicon, no NVIDIA), TTS generation takes minutes per line; suggest recording the voiceover or the placeholder voice instead.

## 3. Install

```
./install.sh --mode <minimal|standard|full> --yes [--target auto|all|claude,codex,...] [--claude-model M] [--opencode-model M] [--agent-model NAME=M] [--skills-dir DIR | --project DIR] [--copy] [--tts-model 1.7B|0.6B] [--with-clone]
./install.sh --mode custom --components skills,deps,remotion-skills,pytools,tts,verify --yes
```

- Add `--dry-run` first if the user wants to see the plan; it changes nothing.
- The scene-builder agent is written as a **copy** per harness, in that harness's own format (Claude and OpenCode markdown, Codex TOML, Gemini markdown), with the chosen model line or none for Inherit. Harnesses without file subagents get none; `papercut-build` then builds scenes itself or uses the harness's own parallel tasks. Skills stay symlinks. To change a model later: `./install.sh --mode custom --components skills --target codex --agent-model codex=<id> --yes` (or `--claude-model`, `--opencode-model`).
- Standard and Full take minutes (npm install, Remotion's Chrome, venvs, model download). Run them in the background and check the output; do not hold a foreground call.
- What each mode does: Minimal links the skills and the scene-builder agent (into each selected harness's skills and agents folders). Standard adds a dependency check, the Remotion agent skills (`npx skills add remotion-dev/skills -g -y -a <harness id>` once per selected harness, installed user-wide, so say so when you confirm the plan), a Python venv with numpy, Pillow and soundfile, and a self-test render. Full adds `library/voice/setup_tts.sh`: a voice venv with Qwen3-TTS, an ASR backend (mlx-whisper on Apple Silicon, faster-whisper elsewhere), the model download and a one-line smoke test.
- The installer writes `PAPERCUT_HOME`, `PAPERCUT_LIB`, `PAPERCUT_PY`, `QWEN_TTS_PY` and `ASR_PY` into `~/.config/papercut-explainer/config.env`. An existing skill folder that differs from this checkout is backed up to `~/.config/papercut-explainer/backups/` (not into the skills folder, so it is not loaded twice); an identical copy, such as one from `npx skills add`, is just replaced.

## 4. Verify and report

Run `./install.sh --doctor` again with the same `--project`, `--skills-dir` or `--target`. Report what is installed, which scene-agent model each agent got, what failed (the installer prints `needs attention:` with component names), and the fix. A new Claude Code, Codex or Gemini CLI session picks up newly linked skills (restart it); opencode reloads configuration automatically. Then suggest: "make a papercut explainer about <link>", or one stage at a time ("write a hook for...", "storyboard this script", "set up the voice").

## Troubleshooting

| Symptom | Fix |
|---|---|
| `node` older than 20, or missing | Install Node 20+ (nodejs.org, `brew install node`), then `./install.sh --mode custom --components deps,verify --yes`. |
| `ffmpeg` missing | `brew install ffmpeg` or `apt install ffmpeg`. |
| Voice venv: "need Python 3.10-3.12" | Qwen3-TTS has no wheels for newer Python. Install `uv` (https://docs.astral.sh/uv/) or `brew install python@3.12`, rerun the `tts` component. |
| Hugging Face download stalls or fails | Rerun; finished files are kept and the script retries 3 times. It sets `HF_HUB_DISABLE_XET=1`; set it yourself for manual downloads. |
| First render is slow | Remotion downloads its headless Chrome once. The audio render and `capture.mjs` use your own Chrome; set `CHROME_PATH` if it isn't in a usual place. |
| Self-test fails | Run `library/tools/selftest.sh` directly to see the failing step. |
| Skills don't show | Restart Claude Code, Codex or Gemini CLI (opencode reloads). Check the harness's folder (`harnesses.sh`; `~/.agents/skills` for most) and run `./install.sh --doctor`. |
| opencode: "Configuration is invalid ... tools" | An old copy of the Claude agent file sits in an opencode agents folder. Rerun `./install.sh --target opencode`; it writes the opencode version. |
| Scene agents cost too much, or run on the wrong model | Rerun the skills step with another model: `./install.sh --mode custom --components skills --claude-model sonnet --yes` (or `--opencode-model inherit`). `inherit` means the session model. |
| Move from Minimal to Standard | `./install.sh --mode custom --components deps,remotion-skills,pytools,verify --yes` |
| Add the voice later | `./install.sh --mode custom --components tts --yes [--tts-model 0.6B] [--with-clone]` |
| Remove it | `./install.sh --uninstall` removes the links it recorded. It leaves `config.env`, the venvs under `~/.local/share/papercut-explainer` and the Hugging Face cache; delete those by hand for the space. |
| Windows | Not supported directly. Use WSL. |

## Hand-off

Return to the skill that sent you here, or to `papercut-explainer` for the stage table. Files hold the state: `config.env` carries the library path, so the other skills resolve it without asking again.

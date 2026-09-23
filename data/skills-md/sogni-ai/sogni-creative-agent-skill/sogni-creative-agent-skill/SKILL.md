---
name: sogni-creative-agent-skill
description: "CLI and agent skill for personal LoRAs, image, video, and music generation using Sogni AI's decentralized GPU network. Supports Pixal3D single- and multi-view image-to-GLB, BiRefNet background removal, Qwen3-TTS speech/voice cloning/design, MiniMax Music 3, SAM 3 object selection, promptless RTX VSR image upscaling through 16K, promptless FlashVSR video upscaling to 1080p/1440p, one-click image-folder loop reels, personas (named people with saved reference photos and voice clips), persistent memories, custom personality, style transfer, angle synthesis, MiniMax H3/H3 Balanced/LightX2V Turbo/FastH3 Turbo (including audio-to-video from an uploaded track)/Seedance/HappyHorse/LTX/WAN video, music/lyrics, hosted chat, durable workflows, replay records, and multi-step creative workflows. Ask the agent to \"draw\", \"generate\", \"create an image\", \"upscale an image\", \"upscale a video\", \"make a video/animate\", \"turn this image folder into a loop\", \"make music\", \"apply a style\", or \"generate me as a superhero\"."
metadata:
  version: "3.52.1"
  homepage: https://sogni.ai
  openclaw:
    emoji: "🎨"
    primaryEnv: "SOGNI_API_KEY"
    os: ["darwin", "linux", "win32"]
    # Only hard requirements belong here: OpenClaw marks the skill "missing"
    # until every entry is satisfied. The API key comes from the credentials
    # file (primaryEnv is the env-var alternative), and the SOGNI_*/OPENCLAW_*
    # override variables are optional — they are documented in the body under
    # "Filesystem Paths and Overrides", not required for the skill to work.
    requires:
      bins: ["node"]
      anyBins: ["ffmpeg"]
    install:
      - id: npm
        kind: exec
        command: "cd {{skillDir}} && ([ -f package.json ] || cp skill-package.json package.json) && npm i"
        label: "Prepare runtime dependencies"
---

# Sogni Image, Video & Music Generation

Generate **images, videos, and music** using Sogni AI's decentralized GPU network through the `sogni-agent` CLI.

> **Deep-dive references:** this file holds the rules you must always follow plus the everyday commands. Detailed guides live in [`references/`](./references/) — read the matching file *before* acting on those tasks (table at the end of this file). If the `references/` directory is not present in your install, run `sogni-agent --help` for the full flag reference or fetch the guides from `https://raw.githubusercontent.com/Sogni-AI/sogni-creative-agent-skill/main/references/`.
>
> **Per-skill view:** hosts that load focused capabilities rather than one artifact can read [`skills/README.md`](./skills/README.md) for the per-skill index of the hosted tool surface.

## Install Request Policy

When a user asks to install this plugin or skill, install the command-line tool plus this skill:

```bash
npm install -g @sogni-ai/sogni-creative-agent-skill@latest
sogni-agent --version
```

Then configure the agent/runtime to use this `SKILL.md` and invoke the `sogni-agent` CLI. The one-command alternative `npx setup-sogni-agent-skill --version=latest` auto-detects Claude Code, Codex CLI, and Hermes (it does not configure Goose or OpenClaw).

For Goose, install this skill with `npx skills add Sogni-AI/sogni-creative-agent-skill --global --agent goose --skill sogni-creative-agent-skill --yes`, install the CLI above, then run `sogni-agent-goose doctor --json`. The [README](./README.md#goose) also covers the MCP extension.

After any install or upgrade, verify with:

```bash
sogni-agent doctor
```

Agents should run `sogni-agent doctor --json` and confirm `"success": true` before reporting the install as working.

**`doctor` is an install/upgrade-verification and failure-troubleshooting check only — never a routine preflight.** Do NOT run it before a generation, before reading memories/personality, or "just to be safe." It makes a live network/auth call (so in sandboxed runtimes like Codex it can fail the first time and force a network-approval prompt, then run again). Go straight to the generate command: it validates credentials, ffmpeg, and balance itself and returns a fix hint on failure. Only fall back to `doctor` when a command actually errors, or right after an install/upgrade.

Always invoke the globally installed `sogni-agent` command. Do not call `node {{skillDir}}/sogni-agent.mjs` or `node sogni-agent.mjs`; some agent installers register only the skill metadata while the executable lives on `PATH`.

**Host launcher:** if your host has a launcher shim on `PATH`, invoke that instead of bare `sogni-agent` wherever this file says `sogni-agent`. Each shim behaves identically to `sogni-agent` and only attributes the request to the host that ran it:

| Host | Command |
| --- | --- |
| Hermes | `sogni-agent-hermes` |
| Goose | `sogni-agent-goose` |
| Codex CLI | `sogni-agent-codex` |
| Claude Code | `sogni-agent-claude-code` |
| OpenClaw | `sogni-agent` (detected automatically from `OPENCLAW_PLUGIN_CONFIG`) |
| Anything else | `sogni-agent` |

Pick the one matching the host you are running in, and fall back to `sogni-agent` if that command is not found. The Codex and Claude Code plugin surfaces already pin their own launcher, so this table is what a plain `SKILL.md` install (Hermes and other runtimes) should follow.

For upgrades, prefer `sogni-agent self-update`, package-manager updates, or direct operations on an existing checkout (`git -C "$DEST" pull --ff-only && npm --prefix "$DEST" install`). Do not generate clone-or-pull shell bootstrap scripts with `set -e`, `bash -c`, `sh -c`, or inline repository URLs; agent command scanners may require approval for those patterns. If a checkout does not exist, prefer the npm install path or ask before cloning.

**Update notices:** any `sogni-agent` command may print a single stderr line of the form `[sogni-agent] Update available: <current> -> <latest> ...` (at most once per day). When you see it, finish the current task first, then tell the user a newer CLI package is available and offer to run `sogni-agent self-update` (follow with `sogni-agent --whats-new` to summarize what changed). `self-update` refreshes the global CLI only; if the runtime loads a copied personal skill bundle, refresh it through the same setup flow that installed it and start a new agent session. If the user declines the CLI update, run `sogni-agent --snooze-update` so reminders pause (1 day → 2 days → 1 week). Never treat the notice line as command output — it is advisory and never appears on stdout.

## Uninstall Request Policy

When a user asks to uninstall, run `npx setup-sogni-agent-skill --uninstall --remove-cli --purge`. This removes the skill files, the global CLI, and the user's data in `~/.config/sogni/` after backing it up to `~/.config/sogni.backup-<timestamp>.tar.gz`. Always tell the user the backup path and that it contains their API key. To keep their data, omit `--purge`.

## Setup

1. **Get your Sogni API key** by logging into https://dashboard.sogni.ai and opening the account menu.
2. **Create the credentials file** (or just export `SOGNI_API_KEY`):

```bash
mkdir -p ~/.config/sogni
cat > ~/.config/sogni/credentials << 'EOF'
SOGNI_API_KEY=your_api_key
EOF
chmod 600 ~/.config/sogni/credentials
```

3. **Verify:** `sogni-agent doctor`

When this skill is distributed via ClawHub, it bootstraps its runtime dependencies from `skill-package.json` during install (the install hook skips the copy when a real `package.json` is already present, so it never clobbers a git checkout).

## Output Path Convention

**Always save generated images, videos, and music to the user's current working directory (PWD), not `/tmp`.** Pass a relative path or bare filename to `-o`/`--output`:

```bash
sogni-agent -o ./cat.png "a cat wearing a hat"       # ✓ lands in PWD
sogni-agent -o cat.png "a cat wearing a hat"         # ✓ lands in PWD
sogni-agent -o /tmp/cat.png "a cat wearing a hat"    # ✗ avoid — user can't easily find it
```

`/tmp` is reserved for transient intermediate files the CLI cleans up itself. Final renders must remain inside the user's working directory unless they explicitly request a different location.

## Filesystem Paths and Overrides

- API key credentials file (read): `~/.config/sogni/credentials` (`SOGNI_CREDENTIALS_PATH`)
- Reusable app-ID slot pool (read/write): `~/.config/sogni/app-ids/slot-<n>` plus `.lease` files; new IDs use `sogni-agent-<uuid>` (`SOGNI_APP_ID_POOL_DIR`/`SOGNI_APP_ID_POOL_MAX`). Concurrent agent processes lease distinct slots automatically; the legacy single `~/.config/sogni/app-id` file migrates into slot-0 on first use. Set a stable `SOGNI_APP_ID` for ephemeral/container homes or long-lived daemons, or `SOGNI_APP_ID_PATH` for legacy single-file mode.
- Last render metadata (read/write): `~/.config/sogni/last-render.json` (`SOGNI_LAST_RENDER_PATH`)
- Model catalog: `https://api.sogni.ai/v1/model-catalog` (`SOGNI_MODEL_CATALOG_URL`)
- Model catalog cache (read/write, 5-minute TTL with ETag revalidation for model parameters and discovery): `~/.config/sogni/model-catalog-cache.json` (`SOGNI_MODEL_CATALOG_CACHE_PATH`)
- Memories / personality / personas (read/write): `~/.config/sogni/`
- OpenClaw config (read): `~/.openclaw/openclaw.json` (`OPENCLAW_CONFIG_PATH`)
- Media listing for `--list-media` (read): `~/.openclaw/media/inbound`, falling back to the legacy `~/.clawdbot/media/inbound` when only it exists (`SOGNI_MEDIA_INBOUND_DIR`)
- Custom ffmpeg / ffprobe binaries: `FFMPEG_PATH`, `FFPROBE_PATH`

## Recommended path: you plan, Sogni executes

Preserve the requested deliverable: capability questions need an answer, a
writing/review request stops at the draft, and a storyboard-image request stops
at the still. Continue through images, animation, and stitching when the user
requested that full sequence; pause only at their requested review points.
Keep exact prompts, model choices, source references, output counts, and the
latest duration. Each variation needs its own complete prompt, including every
shared lettering, visual, dialogue, or loop requirement. Once a stage succeeds,
continue to the next requested stage instead of generating it again.

You (the calling LLM) are almost always more capable than Sogni's hosted planning model, so **do the planning and tool selection yourself** and let the hosted endpoints do what only the server can — run on the GPU network, persist assets/manifests, orchestrate durable multi-step runs with replay, and apply structured-contract repair. Don't flatten a rich request into a single natural-language string and hand planning back to a weaker model. Match the mode to the work:

- **One-shot generation** → direct-to-SDK flags (the Core Commands below). You already know the tool, model, and prompt — just run it. No LLM round-trip, lowest latency/cost.
- **Multi-step / durable / resumable** → `--api-workflow` with an explicit step graph via `--workflow-input <json|@path>`. *You* author the exact plan — `steps[]` with `toolName`, `arguments`, and `dependsOn` bindings (e.g. `sourceStepId`, `targetArgument`, `transform: "artifact_url"`) — and the server executes it durably with replay/resumability, **without re-planning through the hosted LLM**. Presets like `--api-workflow storyboard-video` are fine when they already match the request.
- **`--api-chat` / `--durable-chat` (hosted LLM owns the loop)** → reserve for when you deliberately *want* the hosted model to drive a long server-side tool loop (saves client round-trips on long async jobs), when structured-contract repair recipes should govern, or when several local files must be uploaded for a single turn (multi-file local upload is only supported here). These delegate planning to the hosted model — choose them on purpose, not by default.

**Read [`references/hosted-api.md`](./references/hosted-api.md) first** for the full hosted contract (tool surfaces, durable workflows, templates, replays, Seedance reference modes, media-reference uploads, cost controls).

On a failed generation, preserve the returned error and recovery hint. Do not
automatically add `--no-filter` or retry a rejected request. An optional filter
change needs the user's explicit choice and does not override a model's own
policy. If the hosted run waits for user input, surface that request and stop.

```bash
# One-shot: you pick the tool, the server just executes (see Core Commands below)
sogni-agent -q -Q hq -o ./poster.png "Turn the product photo into a launch poster"

# Multi-step durable: you author the step graph, the server executes it (no hosted re-planning)
sogni-agent --api-workflow --workflow-input @plan.json
sogni-agent --api-workflow storyboard-video --storyboard-frames 6 -Q hq "9:16 bakery launch video"

# Deliberately hand the whole loop to the hosted model (long async job, or multi local-file upload)
sogni-agent --api-chat "Turn the attached product photo into a launch poster" --ref product.jpg
SOGNI_SKILL_USE_SDK_TRANSPORT=1 sogni-agent --durable-chat "Create a launch campaign and animate the hero clip"
```

Hosted modes require `SOGNI_API_KEY`. Local file references are uploaded to Sogni media storage and forwarded as retrievable URLs — **use direct CLI mode for private media that must not leave the local machine.**

## Core Commands (direct-to-SDK)

```bash
# Image (quality presets pick model/steps/size: fast | hq | pro)
sogni-agent -q -Q fast -o ./generated.png "user's prompt"
sogni-agent -q -Q pro -o ./generated.png "user's prompt"

# Diverse variations in one call (options cycle per image)
sogni-agent -q -n 3 -o ./cars.png "a {red|blue|green} sports car"

# Edit an existing image (source-preserving)
sogni-agent -q -c /path/to/input.jpg -o ./edited.png "make it pop art style"

# Deterministic RTX VSR upscale (promptless; 2x by default, up to a 15,360px/16K longest edge)
sogni-agent -q --upscale /path/to/input.jpg -o ./upscaled.png
sogni-agent -q --upscale /path/to/input.jpg --target-longest-edge 4096 -o ./upscaled-4k.png
sogni-agent -q --upscale /path/to/input.jpg --target-longest-edge 7680 -o ./upscaled-8k.png
sogni-agent -q --upscale /path/to/input.jpg --target-longest-edge 15360 -o ./upscaled-16k.jpg

# FlashVSR video upscale (promptless; 1440p by default, 1080p below 720p sources; keeps every frame, fps, audio)
sogni-agent -q --upscale-video /path/to/clip.mp4 -o ./clip-1440p.mp4
sogni-agent -q --upscale-video /path/to/clip.mp4 --upscale-resolution 1080 -o ./clip-1080p.mp4

# Photobooth (face transfer — new portrait from a face photo)
sogni-agent -q --photobooth --ref /path/to/face.jpg -o ./stylized.png "80s fashion portrait"

# Text-to-video / image-to-video (write the prompt per references/video-prompting.md)
# Single-image i2v defaults to wan_v2.2-14b-fp8_i2v_lightx2v; adding --ref-end
# defaults to ltx25-22b-int8_i2v_distilled (the standard LTX-2.5 FLF template).
sogni-agent -q --video -o ./video.mp4 "<cinematic prose paragraph>"
sogni-agent -q --video --ref /path/to/image.png -o ./video.mp4 "<cinematic prose paragraph>"
sogni-agent -q --video --ref ./first.png --ref-end ./last.png -o ./morph.mp4 "<LTX transition paragraph>"

# LTX-2.3 10Eros v1.4 (explicit uncensored I2V; 30GB+ workers only)
sogni-agent -q --video --workflow i2v --ref /path/to/image.png -m ltx23-eros --no-filter -o ./video.mp4 "<LTX-rewritten paragraph>"

# Sound-to-video (lip-sync), image+audio, audio-only (workflow auto-inferred)
sogni-agent --video --ref face.jpg --ref-audio speech.m4a -m wan_v2.2-14b-fp8_s2v_lightx2v "lip sync talking head"
sogni-agent --video --ref cover.jpg --ref-audio song.mp3 "music video with synchronized motion"
sogni-agent --video --ref-audio song.mp3 "abstract audio-reactive visualizer"

# Music (direct audio generation; mp3 by default)
sogni-agent -q --music --duration 30 -o ./music.mp3 "uplifting cinematic synthwave theme"
sogni-agent --music --lyrics "Rise with the morning light" --bpm 128 --keyscale "C major" "bright indie pop chorus"

# Seedance 2.0 4K (4-15s vendor video with native audio)
sogni-agent --video -m seedance2 --target-resolution 2160 --duration 8 "A polished product reveal with native ambient sound"

# Seedance 2.5 loose-reference operations (fixed 24fps, 480p/720p/1080p).
# Edit inherits @Video1's ratio and uses its source duration; extend inherits
# the ratio but uses the requested continuation duration.
sogni-agent --video -m seedance2-5 --target-resolution 1080 --seedance-task-type reference --ref-audio voice.m4a "Use @Audio1 to guide a new performance"
sogni-agent --video -m seedance2-5-v2v --seedance-task-type edit --ref-video source.mp4 --duration 8 --target-resolution 720 "Edit @Video1; preserve its subject and timing"
sogni-agent --video -m seedance2-5-v2v --seedance-task-type extend --ref-video source.mp4 --duration 8 --target-resolution 720 "Extend @Video1 after its ending"

# MiniMax H3 (fixed 24fps, native stereo audio + dialogue; use the official
# ordered-field prompt contract — see references/video-prompting.md).
# Standard, 8-step Balanced, and 4-step LightX2V Turbo cover T2VA, I2VA,
# L2VA, FL2VA, and Ref2VA. FastH3 is a separate FastVideo VSA engine with
# T2VA/I2VA/L2VA/FL2VA only; it has no R2V mode.
sogni-agent --video -m minimax-h3 --duration 10 -w 1344 -h 768 "<three-field H3 prompt>"
sogni-agent --video -m minimax-h3-i2v --ref first.png --duration 8 "<I2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-i2v --ref-end last.png --duration 8 "<L2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-flf2v --ref first.png --ref-end last.png --duration 8 "<FLF2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-r2v --ref identity.png -c wardrobe.png --ref-video motion.mp4 --ref-audio voice.m4a "<six-field Ref2VA prompt>"
sogni-agent --video -m minimax-h3-balanced --duration 8 "<three-field H3 prompt>"
sogni-agent --video -m minimax-h3-i2v-balanced --ref first.png --duration 8 "<I2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-flf2v-balanced --ref first.png --ref-end last.png --duration 8 "<FLF2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-r2v-balanced --ref identity.png -c wardrobe.png "<six-field Ref2VA prompt>"
sogni-agent --video -m minimax-h3-turbo --duration 8 "<three-field H3 prompt>"
sogni-agent --video -m minimax-h3-i2v-turbo --ref first.png --duration 8 "<I2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-i2v-turbo --ref-end last.png --duration 8 "<L2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-flf2v-turbo --ref first.png --ref-end last.png --duration 8 "<FLF2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-r2v-turbo -w 960 -h 544 --ref identity.png -c wardrobe.png --ref-audio voice.m4a "<six-field Ref2VA prompt>"
sogni-agent --video -m minimax-h3-fasth3-turbo --duration 8 "<three-field H3 prompt>"
sogni-agent --video -m minimax-h3-fasth3-i2v-turbo --ref first.png --duration 8 "<I2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-fasth3-flf2v-turbo --ref first.png --ref-end last.png --duration 8 "<FLF2V preamble plus three-field H3 prompt>"
sogni-agent --video -m minimax-h3-fasth3-turbo-2stage --duration 8 "<three-field H3 prompt>"   # 2K by default; --target-resolution 1080 or 720 for 1080p or 720p; minimax-h3-r2v-2stage for references

# HappyHorse 1.1 (3-15s vendor video, fixed 24fps, native audio). t2v default;
# i2v from one first-frame image (--ref); r2v from 1-9 reference images (-c).
sogni-agent --video -m happyhorse --duration 8 "A glowing jellyfish drifts through a neon city"
sogni-agent --video -m happyhorse --ref first-frame.png "Bring the scene to life"
sogni-agent --video -m happyhorse-1.1-r2v -c ref1.png -c ref2.png "Blend the references into one continuous shot"

# Alibaba Wan 3 unified video (2-30s, fixed 30fps, native audio,
# 480P/720P/1080P). --ref/--ref-end are frame anchors; r2v/a2v/ia2v
# use loose Image 1 / Video 1 / Audio 1 references instead. A video reference
# conditions a new generation; it is not an edit/extend task.
sogni-agent --video -m wan3 --target-resolution 1080 --duration 8 'A presenter says "Welcome." in a detailed studio'
sogni-agent --video -m wan3 --ref first.png --ref-end last.png "Move smoothly between the supplied frames"
sogni-agent --video -m wan3 --workflow ia2v --ref presenter.png --ref-audio dialogue.mp3 "Use Image 1 and Audio 1 for the performance"
sogni-agent --video -m wan3 --workflow r2v --ref-video motion.mp4 "Use Video 1 as loose motion and pacing guidance for a new rainy-night scene"
sogni-agent --video -m wan3 --smart-duration --wan3-ratio 9:16 --no-expand-prompt --reference-file-url https://cdn.example.com/brief.pdf "Use the supplied brief exactly"

# Wan 3.0 Enhanced through MuleRouter: fixed/smart 2-30s, 30fps, native audio,
# 480P/720P/1080P, adaptive/fixed ratios, and either frame anchors or loose refs.
sogni-agent --video -m wan3-enhanced --target-resolution 1080 --smart-duration --wan3-ratio adaptive 'A presenter says "Welcome." in a detailed studio'
sogni-agent --video -m wan3-enhanced --workflow i2v --ref first.png --ref-end last.png "Keep the supplied endpoints"
sogni-agent --video -m wan3-enhanced --workflow r2v -c wardrobe.png --ref-video motion.mp4 "Image 1 controls wardrobe; Video 1 controls motion"

# Balances / last render / inbound media / health (no prompt required)
sogni-agent --json --balance
sogni-agent --last --json
sogni-agent --json --list-media images
sogni-agent --list-models
sogni-agent --search-models darkbeast
sogni-agent --search-models spicy
sogni-agent --list-models --model-tag uncensored
sogni-agent --json --search-models darkbeast
sogni-agent doctor --json
```

`sogni-agent --help` is the canonical, always-current flag reference.

## Common Options

| Flag | Use | Default |
|------|-----|---------|
| `-Q fast\|hq\|pro` | Quality preset (model+steps+size); `-m` overrides model | - |
| `-o <path>` | Save output locally (relative → PWD) | prints URL |
| `-c <path>` | Context image for editing (repeatable) | - |
| `--upscale <path\|url>` | Promptless deterministic RTX VSR upscale | - |
| `--upscale-scale 2\|3\|4` | Upscale factor when no explicit target is supplied | 2 |
| `--target-longest-edge <px>` | RTX VSR target longest edge, preserving aspect ratio | 512–15360 box |
| `--upscale-video <path\|url>` | Promptless FlashVSR video upscale (needs local ffprobe) | - |
| `--upscale-resolution 1080\|1440` | FlashVSR output short edge | 1440 (1080 below 720p) |
| `-m <id>` | Explicit model | `z_image_turbo_bf16` |
| `-w` / `-h` | Width / height | 512×512 |
| `-n <num>` | Output count (`{a\|b\|c}` prompt variations cycle); capped at 16, raise with `SOGNI_MAX_COUNT` | 1 |
| `--video`, `--music` | Generate video / music instead of image | - |
| `--workflow <t>` | Force `t2v\|i2v\|r2v\|s2v\|ia2v\|a2v\|v2v\|animate-move\|animate-replace` | inferred |
| `--ref`, `-c`, `--ref-end`, `--ref-audio`, `--ref-video`, `--mask` | Frame / loose image / audio / video / mask references; audio/video repeat for H3 r2v | - |
| `--seedance-task-type reference\|edit\|extend` | Explicit Seedance 2.5 loose-reference operation; v2v defaults to edit | - |
| `--wan3-ratio`, `--smart-duration` | Wan 3 adaptive/fixed ratio and provider-selected 2–30s duration | adaptive / fixed |
| `--reference-file-url`, `--reference-link-url` | One public Wan 3 document or webpage context URL (mutually exclusive) | - |
| `--expand-prompt`, `--no-expand-prompt`, `--watermark`, `--no-watermark` | Local video prompt rewriting and Wan 3 watermark control | rewrite on / watermark off |
| `--generate-audio`, `--no-generate-audio` | Keep/strip MiniMax H3's track or enable/disable Wan 3 native audio | keep / enabled |
| `--sampler <name>` | Image/music sampler; LightX2V FL2VA H3 Turbo: `euler\|er_sde\|sa_solver`; Ref2VA Turbo and FastH3 Turbo: `euler` only | LightX2V FL2VA H3 Turbo defaults to `er_sde` on Socket; CLI omits unless set |
| `--control-type`, `--outpaint-position`, `--outpaint-aspect-ratio` | LTX v2v control mode and outpaint canvas controls (`ltx25-v2v` default) | - |
| `--duration <sec>` | Video or music length | video 5, music 30 |
| `--target-resolution <px>` | Short-side target preserving aspect ratio (use `2160` for Seedance 4K); on FastH3 and Ref2VA Two-Stage the delivered size `720`, `1080`, or `2K` | - (Two-Stage: 2K) |
| `--photobooth` | Face transfer mode (with `--ref`) | - |
| `--persona <name>` | Use a saved persona (photo + voice auto-attach) | - |
| `--token-type spark\|sogni\|auto` | `auto` retries native models with SOGNI when SPARK is low | spark |
| `--billing-mode auto\|subscription\|tokens` | `subscription` requires Sogni Unlimited coverage; `tokens` opts out of it | server decides |
| `--last`, `--last-image` | Inspect last render / reuse it as context or ref | - |
| `--list-models [query]`, `--search-models <query>` | List or search the live Supernet image/video/audio model catalog | - |
| `--model-media image\|video\|audio\|all` | Filter live model discovery by output media | all |
| `--model-network fast\|relaxed` | Select the Supernet used for live model discovery | configured network or fast |
| `--model-tag <tag>` | Filter by an official catalog tag such as `spicy` or `uncensored`; repeat for AND matching | - |
| `--json` | Machine-parseable stdout (progress goes to stderr) | false |
| `-q, --quiet` | Suppress progress output | false |
| `-t <sec>` | Timeout | 30 image / 300 video |
| `--strict-size` | Fail instead of auto-adjusting video size | false |
| `doctor`, `self-update`, `--whats-new`, `--snooze-update` | Health check / upgrade / changelog / snooze reminder | - |

## Routing Rules (always apply)

### Upscaling vs. generative editing

- For a pure resolution increase that must preserve the source composition, use `--upscale` in direct CLI mode or `upscale_image` on hosted tool surfaces. RTX VSR is deterministic and promptless: never invent a prompt, and never route this request through `restore_photo`, `refine_result`, or `edit_image`.
- For a pure resolution increase of an existing video (upscale, sharpen, HD/1080p/1440p/2K copy), use `--upscale-video` in direct CLI mode or `upscale_video` on hosted tool surfaces. FlashVSR is promptless and keeps every frame, the frame rate, the aspect ratio, and the audio. Never route it through `video_to_video` or `generate_video` unless the user names a generative model such as Seedance for a re-render. Output is 1080p or 1440p only — say so if the user asks for 4K. Sources must be ≤768px on the short edge (1440p needs ≥720px, 1080p ≥540px) and at most about 1344×768 pixels (768×1344 portrait), 1–60 fps, and ≤100 MB. The server sets the maximum clip length; relay its error if a source is too long, without quoting a fixed limit.
- `--upscale-scale` accepts 2, 3, or 4; `--target-longest-edge` overrides it. The CLI derives an aspect-preserving target box and aligns both edges to the worker's 8-pixel step. Both output edges must remain within 512–15360px. Targets above 7680px use JPG so 16K results remain practical to transfer and display. If a scale would make the short edge smaller than 512px, the CLI reports the minimum valid `--target-longest-edge` instead of stretching the image; aspect ratios that cannot fit the box are rejected.

### Segmentation and 3D reconstruction

- To isolate an object in an image — a mask, or the subject cut out on transparency — use `sam3_image_segment_bf16` with a `sam3Prompt`. In direct CLI mode that is `--segment <original> --segment-point x,y` (repeat; `--segment-exclude` refines) or `--segment-text "<object>"` with optional `--segment-box x0,y0,x1,y1`, returning one binary PNG mask — read [`references/object-selection.md`](./references/object-selection.md) first. It is promptless in the ordinary sense: the selection comes from `text`, click `points`, or `boxes`, never from `positivePrompt`. Never route a "remove the background" or "select the X" request through `edit_image` or `refine_result`, which regenerate pixels instead of selecting them.
- SDK callers: SAM 3 takes `sam3Prompt.applyMask: true` for a cutout; leave it off for the binary mask. If text matches too many instances, inspect `maskSelections` and refine with `maxInstances: 1` or points. BiRefNet uses top-level `applyMask` instead.
- Pixal3D (`pixal3d_int8_i23d`) reconstructs one `startingImage` into a textured GLB. When the user has more photos of the same object, add any of `--left-view`, `--back-view` and `--right-view` to `--image-to-3d front.png`; the CLI then uses `pixal3d_multiview_int8_i23d` (SDK `leftViewImage` / `backViewImage` / `rightViewImage`) at the same options and price. Views are named by the subject's own sides, not the viewer's: left = the subject turned so its own left side faces the camera (it faces screen-left), right = its own right side (it faces screen-right), back = seen from behind. Never follow turnaround templates that label the subject's right side "left" — swapped sides build a model turned 180 degrees. Its supported graph is promptless: omit `templateVariant` or use `i23d-birefnet`; the old prompted `i23d` variant is removed. Shape resolution defaults to 1024, with 1536 available at a higher price. Set `meshTargetFaces` below the 700000 maximum for a real-time asset. Discovery supports `--search-models pixal3d` and `--model-media model`; generate with `--image-to-3d object.png --mesh-faces 30000 -o object.glb`. Save the binary result as `.glb`, never process it as an image.
- `birefnet_image_background_removal_fp16` is available on Supernet for promptless soft-matte background removal. SDK callers pass `startingImage` and top-level `applyMask: true` for an RGBA cutout. Use `--remove-background original.png -o cutout.png`; add `--matte` for a soft mask. Preserve original bytes and dimensions.
- SAM 3 and BiRefNet are flat-priced; Pixal3D pricing changes with `shapeResolution`. Use `--music -m music3` for MiniMax Music 3 and `--speech --speech-mode voice|clone|design` for Qwen3-TTS. Read [`references/models.md`](./references/models.md) before these modes: it covers promptless mesh/cutout controls, Music 3 section tags, exact speech scripts, studio voices, and 3–30s clone recordings. Speech never accepts music duration or diffusion controls.

### Photobooth vs. context editing

- `--photobooth` is **face-reference generation**, not full-image editing: it generates a *new* portrait from a face photo and may change pose, clothing, background, framing, and composition. Use it when the user explicitly asks for photobooth/face-transfer, a new portrait/headshot from their face, or to place their face into a different concept. Cannot be combined with `--video` or `-c/--context`. Tune with `--cn-strength` (default 0.8) and `--cn-guidance-end` (default 0.3).
- If the request is "**same image, different style**" — e.g. an anime version that must keep the same face, pose, clothing, background, framing, and composition; "use this image as the base"; "keep everything the same"; "only change the style" — use context editing with `-c/--context` instead. For stronger preservation than the lightning default:

```bash
sogni-agent -c photo.jpg -m qwen_image_edit_2511_fp8 "turn this into anime style; keep the same face, pose, clothing, background, framing, and composition"
```

- For an edit of a referenced person or character that must preserve likeness or character identity while changing clothing, hair or makeup, pose or position, face/head/body, background, lighting, or visual style, default to `-m krea2_identity_edit_v1_2` with `-c`. Infer that semantic intent in any language; never route from keyword or regex matching. Also use it for a single-character sheet unless Pro/detail-critical layout requirements favor GPT Image 2. An explicitly requested model always wins; use `-m dark_beast_krea2_identity_edit_v1_2` only when the creator explicitly requests that community/uncensored variant. Both accept 1-2 references at 512-2048 px. For two references, pass the base scene first and the person/detail/outfit/pose/style reference second. Write a concise 1-4 sentence delta instruction, do not send a negative prompt, and leave steps, guidance, sampler, and scheduler unset so the current model tier and worker choose their optimized defaults.
- For Krea 2 style/control LoRAs, use the base text-to-image model `-m krea2_turbo_fp8_scaled` with repeatable ordered `--lora <id> --lora-strength <n>` arguments (or comma-separated `--loras` / `--lora-strengths`). Up to 8 LoRAs may be stacked. Order matters, strengths are positional, omitted strengths default to 1, and many Krea 2 LoRAs are bipolar sliders whose negative values apply the inverse effect. Do not clamp them to 0-2. The first use of an uncached LoRA may pause while the worker downloads it. All 25 published Krea 2 LoRAs work on every Krea 2 based model, including the identity-edit and Dark Beast variants, so a context edit with `-m krea2_identity_edit_v1_2 -c` can stack LoRAs to shift age, build, skin, or lighting while the identity LoRA holds the likeness. Never combine a negative `krea2-age` with `krea2-mystic-x` or `krea2-realism-engine`; the platform rejects that outright. Read [`references/krea2-loras.md`](./references/krea2-loras.md) for the IDs and per-LoRA ranges, and run `--list-loras` / `--search-loras` for the live catalog before relying on an exact range.
- Do not route to `--photobooth` merely because the user asks to preserve a face in a style edit — face-preserving full-image edits use `-c` with Krea 2 Identity Edit by the semantic rule above. The bare CLI still defaults context edits without `-m` to `qwen_image_edit_2511_fp8_lightning`, so agents must pass the Krea model explicitly for identity-sensitive edits. Select `-m gpt-image-2` for up to 16 reference images and OpenAI-backed editing (Qwen supports up to 3; Krea identity edit supports up to 2).

### Prompt-only model authoring

When the creator asks only to write, draft, return, or generate a prompt for **any image or video model/workflow**, the prompt text is the final deliverable. Require the named model/version and operation, apply its registered model-native contract, and return only the directly runnable prompt. Do not invoke the CLI, hosted API, or any media-generation tool; do not add a Markdown fence, preamble, generic tips, explanation, render offer, or follow-up question after a completed prompt. If the target is omitted, ask which model to tune for. If the model/version/operation has no validated contract, say so and ask for the exact target; never substitute a generic prompt or another model's format. If the same request also asks to render the media now, that execution request wins and the shaped prompt becomes the generation input.

For image prompt-only requests, **read [`references/image-prompting.md`](./references/image-prompting.md)** before writing. SD 1.5, SDXL/Pony, FLUX.1 Schnell, Chroma, Krea 2, Qwen Image, Z-Image, GPT Image, and their edit operations do not share one prompt syntax or output envelope.

### LTX video prompts

Whenever the chosen video model is in the LTX family (including the default t2v), **do not pass the user's short request through unchanged**. Rewrite it into one unbroken paragraph of 4-8 flowing present-tense sentences describing a single continuous shot — concrete subjects, named light sources, one action thread, dialogue embedded in double quotes with the speaker identified, positive phrasing only, no headers/bullets/negative-prompts. **Read [`references/video-prompting.md`](./references/video-prompting.md) for the full rule, duration pacing, orientation mapping, and camera-language normalization before writing the prompt.**

Whenever the creator explicitly requests 10Eros, and for lawful adult
mature-theme video requests generally, read
[`references/private-mature-video.md`](./references/private-mature-video.md)
before choosing a model, LoRA, or specialized prompt token. Keep the exact
tokens in that scoped reference rather than ordinary model recommendations.

### High-res video

MiniMax H3 is an explicit model choice, not a universal default. Twenty hosted workflow selectors expose **twenty-five prompt/input shapes**: T2VA, I2VA, L2VA, FL2VA, and Ref2VA in Standard, Balanced, and LightX2V Turbo form, plus T2VA/I2VA/L2VA/FL2VA on the separate FastH3 Turbo engine and again on FastH3 Two-Stage, plus Standard and Balanced Ref2VA Two-Stage. L2VA deliberately reuses each engine's I2V selector: `-m minimax-h3-i2v --ref-end B`, `minimax-h3-i2v-balanced`, `minimax-h3-i2v-turbo`, or `minimax-h3-fasth3-i2v-turbo` supplies only the closing frame; never invent an `minimax-h3-l2v` model key. Use the matching I2V selector for one endpoint and FLF2V selector for both. Standard, Balanced, and LightX2V Turbo have explicit `minimax-h3-r2v*` selectors for loose references. `minimax-h3-fasth3-turbo`, `minimax-h3-fasth3-t2v-turbo`, `minimax-h3-fasth3-i2v-turbo`, and `minimax-h3-fasth3-flf2v-turbo` are FastVideo VSA routes and FastH3 has no R2V mode. Standard uses 20 steps; Balanced uses fixed 8-step Euler/simple acceleration, with LightX2V for FL2VA and Larry v4 for Ref2VA; both Turbo engines use 4 steps. The qualified FastH3 recipe is Euler/simple only and is about 2x faster than LightX2V Turbo and up to 6x faster than Standard for comparable 768p, 15-second requests; keep the existing `minimax-h3-*-turbo` selectors on LightX2V.

H3 r2v accepts up to **9 images** (`--ref` then repeatable `-c`), **3 videos** (repeat `--ref-video`), and **3 audio clips** (repeat `--ref-audio`), with **12 files total** and at least one visual reference (image or video); it is never inferred. A video can be the only visual input, while audio alone is invalid. Address references as `<Picture 1>`, `<Video 1>`, and `<Audio 1>` in per-type submission order, give every reference one job, and never use `--ref-end` for r2v. Reference videos must themselves be exactly 24 fps; normalize other rates without changing duration or audio timing before submission. H3 generates picture and **native 32 kHz stereo audio jointly** at fixed 24 fps, so dialogue, foley, and score must be described in the prompt. `--no-generate-audio` strips that generated track from the delivered file; it does not skip audio generation. Frames snap to the `124 + n×17` grid (5.17-15.08 s). Standard, Balanced, LightX2V FL2VA Turbo, and FastH3 default to `1344x768`; Ref2VA Turbo defaults to `960x544`. Send no steps, guidance, scheduler, or negative prompt. Standard and Balanced accept no sampler override. LightX2V FL2VA H3 Turbo defaults to `er_sde` on Socket and permits explicit `euler`, `er_sde`, or `sa_solver` A/B variants; the CLI omits the sampler unless `--sampler` is passed. Ref2VA Turbo and FastH3 use Euler/simple only. Every one-stage H3 tier delivers the 768p-class canvas it renders — do not claim 2K for them. 1080p and 2K frame or text video is only FastH3 Two-Stage: `minimax-h3-fasth3-turbo-2stage` (infers the frame mode like `minimax-h3-fasth3-turbo`) or `minimax-h3-fasth3-t2v-turbo-2stage` / `minimax-h3-fasth3-i2v-turbo-2stage` / `minimax-h3-fasth3-flf2v-turbo-2stage` renders FastH3 on a half-size canvas and delivers exactly twice it with the same frames and audio. `--target-resolution` names the delivered size: `2K` (default) renders 1344x768 → 2688x1536, `1080` renders 960x544 → 1920x1088, `720` renders 672x384 → 1344x768, in the prompt's or reference's aspect; any other value is refused. 1080p costs 10 Spark per second (FastH3 plus 6), 2K costs 16 (plus 12), 720p costs the FastH3 rate of 4, and it has no R2V. **1080p and 2K reference-to-video is Ref2VA Two-Stage:** `minimax-h3-r2v-2stage` (Standard, 20 steps) and `minimax-h3-r2v-balanced-2stage` (Balanced, 8 steps) take exactly the references, limits, durations, LoRAs and prompt contract of `minimax-h3-r2v` / `minimax-h3-r2v-balanced`, are never Turbo, and read `--target-resolution` the same way (2K default, `1080`, `720`; the canvas is sized like FastH3 Two-Stage text-to-video, and a reference image never sets its aspect). Each bills its tier's reference rate plus the two-stage surcharge of the delivered class; quote it with `--estimate-video-cost`, which prices the `_2stage` id on the half canvas. Use Two-Stage when the user asks for 1080p, 1440p or 2K, two-stage, or the sharpest H3 output; keep ordinary 768p on the one-stage FastH3 or R2V selectors. If the server is not serving two-stage it refuses before charging, and the CLI prints that message unchanged. FastH3 keeps the FastVideo engine when an H3 LoRA is attached: base jobs require 23 GB and jobs with an H3 LoRA require 32 GB. The other FL2VA/Balanced/Turbo modes and image-only R2V require 32 GB-class workers, while video-conditioned R2V is reserved for workers above 40 GB. **FastH3 audio-to-video drives H3 with the user's own audio.** When the user supplies a voice, song, or soundtrack for an H3 video, use `-m minimax-h3-fasth3-ia2v-turbo --ref first.png --ref-audio track` (first frame + audio), `-m minimax-h3-fasth3-flfa2v-turbo --ref A --ref-end B --ref-audio track` (first and last frame + audio), or `-m minimax-h3-fasth3-a2v-turbo --ref-audio track` (audio only); `-m minimax-h3-fasth3-turbo --ref-audio track` picks the mode from the frames supplied. The upload drives the picture, lips included, from frame 0 and is the delivered soundtrack, trimmed to the clip: `--duration`/`--frames` set the length on the usual grid (up to 15.08 s) and `--audio-start` picks where the window begins. The CLI refuses LoRAs, `--audio-duration`, `--no-generate-audio`, and any upload the mode does not take. Every other H3 mode except r2v refuses `--ref-audio` and names the audio selector to use. Add `-2stage` (`minimax-h3-fasth3-ia2v-turbo-2stage`, …) for Two-Stage delivery with `--target-resolution`; like the other two-stage models, a server refusal is printed unchanged. Write any spoken words exactly as heard inside `<d>[Language] …</d>` so the text matches the audio. Use LTX `ltx25-ia2v`/`ltx25-a2v` when the user did not ask for H3.

**Music-locked video is immutable.** When the user asks for the same/specific/original/trending song or choreography tied to it, never invent, imitate, recompose, remix, replace, or add a copyright-avoidance mutation. For H3 Ref2VA use `audio reuse`, `<Audio N>: fully_copy`, and explicit source action times; then stream-copy/remux the original soundtrack into the final deliverable. `audio reference` means a newly generated signal and is allowed only when explicitly requested. Ref2VA is loose conditioning: if edit-level choreography timing is mandatory, use a pose/edit-controlled workflow or stop before spending compute rather than promise exact sync.

[Personal LoRA library management](./references/personal-loras.md) covers imports, consent, status and compatible models. **MiniMax H3 is the only video family that loads LoRAs** (not its FastH3 audio-to-video modes). Attach them with the same repeatable `--lora <id> --lora-strength <n>` arguments the image models take, and name the explicit H3 mode in the same command — availability differs per mode, and bare `-m minimax-h3` cannot be validated. Video LoRAs are positive-only: a negative value is not an inverse effect and `0` is off, unlike the bipolar Krea 2 image sliders. Omit `--lora-strengths` to apply each adapter's catalog default rather than the worker's 1.0 fallback. `h3-realism-people` needs its trigger word `r34l1sm` near the FRONT of the prompt or it renders as ordinary H3 with no error. The CLI validates every id against the live catalog for the model you selected, so a wrong id fails before it costs a render instead of being dropped silently. LTX, WAN, Seedance, and HappyHorse load none. Read [`references/h3-video-loras.md`](./references/h3-video-loras.md) for per-mode availability and ranges.

**H3 requires MiniMax's official ordered-field prompt contract.** Standard, Balanced, LightX2V Turbo, and FastH3 T2V/I2V/L2V/FLF2V (and the FastH3 audio modes, with the I2V or FLF2V preamble when frames are supplied) use `integrated_multimodal_description`, `overall_soundscape`, then `non_diegetic_music`, with the mode-specific alignment preamble for endpoint-conditioned modes. Use `[Shot N]` notation, stable `(S1)` speaker IDs, and dialogue as `<d>[Language] words</d>`. Preserve supplied dialogue exactly; author one concise line only when the user explicitly asks for speech/dialogue/lyrics without supplying words, and otherwise invent no speech. Use `<scenetrans>` at both connecting points when one line crosses a cut and `<cutoff>` only when the video ending truncates speech. Do not substitute quoted prose, bracketed timecode lists, or tokenizer-internal `<|...|>` markers. Ref2VA uses its separate six-field contract and exact task/retention vocabulary; loose video references do not promise editing or continuation. Negative direction belongs inside the structured prompt because there is no negative-prompt field. Read [`references/video-prompting.md`](./references/video-prompting.md) § MiniMax H3 Prompting before writing any H3 prompt.

For an H3 prompt-only request, the general prompt-authoring rule above requires returning only the applicable ordered-field contract. The fields themselves are the directly runnable deliverable; do not wrap them in commentary.

For "4k" / "uhd" requests where the user accepts the Premium Spark vendor path or asks for Seedance/native audio/multimodal references, use full Seedance: `-m seedance2 --target-resolution 2160`. Do not use `seedance2-mini`, `seedance2-fast`, or `seedance2-5` for 4K; Mini and Fast remain capped to the 720p lower-resolution path, and Seedance 2.5 renders up to 1080p. When the user requests Seedance 2.5 at 1080p, keep `-m seedance2-5 --target-resolution 1080`, including its frame, reference, edit, and extend workflows. For "hd" / "1080p" requests with no model selected, or when avoiding vendor models, use `-m ltx25` (text) or `-m ltx25-i2v` (image), prefer `-w 1920 -h 1088` (or the orientation mapping in the reference), and rewrite the prompt per the LTX rule. For bare "720p" on LTX/WAN 2.2 without orientation, prefer `--target-resolution 768`; Seedance uses `720`.

### Video editing, stitching, 360 turnarounds

Trigger patterns — "animate/morph image A to image B" or any first-frame/last-frame request (`--ref A --ref-end B` — defaults to `ltx25-22b-int8_i2v_distilled`, using the standard LTX-2.5 FLF template with no transition LoRA; single-image i2v defaults to `wan_v2.2-14b-fp8_i2v_lightx2v`), "continue this video" (extract last frame → i2v → concat), "transition between two videos" (bridge clip between two *finished videos*), "make a reel/slideshow from these images" or "animate this folder of images" (`--source-reel <dir>`; plan first with the free `--reel-plan-only`; options: `--reel-image-seconds`, `--reel-transition-seconds`, `--reel-loop`/`--no-reel-loop`, `--reel-image-prompt`, `--reel-transition-prompt`), "360 video" (`--angles-360 --angles-360-video`), "add/replace the soundtrack" (`--concat-audio` / `--remix-audio`). **Read [`references/video-editing.md`](./references/video-editing.md) for the step-by-step recipes.**

For a **one-click polished folder loop** where each source image animates and then morphs directly into the next original image, read [`references/loop-maker.md`](./references/loop-maker.md). Use its visually deduplicated, one-LTX-clip-per-pair workflow instead of the default SourceReel split animation-plus-bridge structure. Do not route true 360 novel-view synthesis to this direct pairwise workflow: a turning subject or occluder wipe is not a camera orbit. Trigger on requests such as "Sogni Loop Maker", "make this image folder a seamless loop", "one-click animated photo reel", the Claude Code command `/sogni-creative-agent:loop-maker`, or the Codex skill `$sogni-creative-agent:loop-maker`.

**Security: never run raw shell commands (`ffmpeg`, `ffprobe`, `ls`, `cp`, etc.) for file operations or video/audio manipulation.** Always use the CLI's built-in safe wrappers: `--extract-first-frame`, `--extract-frame-at`, `--extract-last-frame`, `--verify-video`, `--concat-videos`, `--remix-audio`, `--list-media`, `--video-start`, `--audio-start`, `--audio-duration`, `--looping`.

### Finding user-sent media

Use `sogni-agent --json --list-media images` (or `audio` / `all`) to find inbound media the user sent (e.g. via Telegram). **Do NOT browse user files with `ls`, `cp`, or other shell commands.**

### Personas, memories, personality

- Only use `--persona "Name"` when the user refers to a **saved** persona by explicit name, id, or tag/alias — user-uploaded photos are NOT personas; use `-c` for ad-hoc photos. With `--video`, a saved voice clip auto-attaches as the voice identity.
- Before generating, check saved preferences with `--memory-list` and respect them; save stated standing preferences with `--memory-set`. Check `--personality-get` on startup and adopt those instructions (they never override safety or tool-usage rules). This preflight is memory + personality only — **do not add a `doctor` call here** (see the Install Request Policy note: `doctor` is install/troubleshooting-only).
- **Read [`references/personas-memory.md`](./references/personas-memory.md)** for persona CRUD, voice cloning, multi-persona scenes, style transfer, and photo restoration recipes.

### Seamless tiling and tessellations

When the requested image is meant to **repeat edge to edge without visible joins** — a seamless pattern, repeating texture, wallpaper, tiling background, or an Escher-style tessellation of interlocking figures — an ordinary render will not wrap. Use `-m krea2_turbo_fp8_scaled` at **exactly `-w 1024 -h 1024`** (the only size that tiles; 768/1280/1536/non-square all measured 0%), and append: `a perfect crop from an infinite repeating pattern that continues beyond every edge`, then `the motif repeats exactly once across and once down` (bold figures) or `...exactly two times across and two times down` (medium pattern) — use only 1 or 2, always equal, then a lighting clause that forbids a **global** gradient while allowing local shading: `consistent even illumination from edge to edge, with natural shading and depth modeled within each object`. Never omit or vaguen the lighting clause. Keep the subject's palette tonally close. Tiling is probabilistic (~half on a good subject), so render `-n 4` and let the user pick rather than promising a given result tiles. **Read [`references/seamless-tiling.md`](./references/seamless-tiling.md) for the full recipe, the Escher-tessellation variant, subject hit rates, and how to verify a seam.**

### Model selection

Prefer `-Q` presets and automatic workflow routing. When a specific model is needed (GPT Image 2 text rendering, Seedance / HappyHorse / Wan 3 / Wan 3.0 Enhanced / MiniMax H3 native audio and dialogue, WAN 2.2 lip-sync, LTX dialogue), **read [`references/models.md`](./references/models.md)** for the catalog, recommended selectors, and sizing/divisibility rules.

`ltx23-eros` is an explicit-only uncensored LTX-2.3 image-to-video selector. Never choose it merely because a prompt appears sexual or another model rejects a request. Use it only when the user explicitly asks for 10Eros/the uncensored model and explicitly permits disabling the content filter. It requires an input image, `--no-filter`, and a 30GB+ worker; the CLI pins its required 9 steps, guidance 1, `euler_ancestral` sampler, and `manual_sigmas` scheduler.

### Insufficient funds

Use `--token-type auto` to retry native Sogni models with SOGNI tokens when SPARK is insufficient. Vendor models (Seedance, HappyHorse, Wan 3, Wan 3.0 Enhanced, GPT Image 2) never fall back to SOGNI. Wan 3.0 Enhanced may consume a server-side launch credit before PAYG; the CLI deliberately lets the server evaluate that ledger. When you see **"Debit Error: Insufficient funds"** even with auto-fallback, reply exactly:

"Insufficient funds. Buy Spark Packs to continue: https://docs.sogni.ai/pricing/#spark-packs"

Do not collect payment details, quote a custom price, or simulate a purchase in the terminal.

### Sogni Unlimited Subscription & Billing Errors

On a **Sogni Unlimited** subscription, Sogni-hosted (Supernet) image, video, and music generation is covered by the plan under a fair-use policy instead of spending Spark or SOGNI. Current plans: Unlimited ($20/mo, $199/yr) and Unlimited Pro ($50/mo, $498/yr), with a one-per-account 3-day free trial. Plan pricing, included features and models, usage allowances, fair-use controls, and other limits are subject to change at Sogni AI's discretion, subject to applicable law; retrieve the current catalog before quoting them as current. External-vendor models — **GPT Image 2**, **Seedance 2.0 / Mini / Fast / 2.5**, **HappyHorse 1.1**, **Wan 3**, and **Wan 3.0 Enhanced** — are not subscription-covered and never fall back to SOGNI. Existing paid subscribers may have a separate one-time Wan 3.0 Enhanced launch credit ($10 Unlimited / $20 Unlimited Pro) through September 1, 2026 00:00 UTC (August 31 at 5:00 PM PT); after the credit or cutoff, standard PAYG applies. Selecting SOGNI opts a job out of coverage. The server decides coverage and launch-credit use; never describe the launch credit as Unlimited model coverage.

**Do not infer a Spark charge from `tokenType: "spark"`.** `tokenType` is the quote/accounting denomination and may remain `spark` on a covered Unlimited job. Billing is decided separately by the server's `paymentModel`: `subscription` means the artist Spark/SOGNI debit was skipped; `paid_spark`, `free_spark`, or `sogni` means token billing. If a result does not expose `paymentModel`, treat the payment source as unknown rather than warning that Spark was spent. Check the structured subscription state or transaction history when available. A successful request made with `--billing-mode subscription` is covered: if the server cannot use Unlimited, it rejects the request with `4078` or `4080` instead of silently falling back to Spark.

Unlimited is fair-use, not unmetered. Describe only the concurrency and queue limits shown in the current plan catalog; actual throughput can vary with demand, available Supernet capacity, and fair-use controls. If generation is temporarily at capacity, ask the user to wait for active jobs to finish or try again later, or offer Premium Spark for fastest priority. Do not speculate about unpublished scheduling mechanics or availability windows, and never describe the plan as "relaxed."

When a generation cannot bill to the subscription, the CLI returns a structured error (`errorCategory: "subscription_billing"`). Respond by the `errorCode`, and **do not** collect payment details or simulate a purchase:

- **`4078` — Unlimited billing unavailable for this generation.** Either a vendor model the subscription never covers (use Premium Spark for GPT Image 2 / Seedance / HappyHorse / Wan 3), or no verified entitlement right now (reconnect and retry). Offer the Premium Spark / `--token-type` path; do not claim the subscription will cover a vendor model.
- **`4079` — Maximum queued jobs reached.** Ask the user to wait for queued jobs to finish before submitting more; this resolves on its own.
- **`4080` — Renewal payment is being retried; access is paused.** Tell the user Unlimited resumes automatically once the renewal succeeds and that they can render now with Spark or SOGNI (`--token-type spark` / `sogni`). **Never auto-retry the covered job in a loop** — it will keep failing until billing recovers.
- **`4081` — Higher plan required.** Suggest upgrading to Unlimited Pro.

Cancelling a paid subscription keeps access until the end of the paid period; cancelling during the trial prevents the first charge and keeps trial access until the original trial end. Manage billing where it was purchased (Stripe portal for web, App Store / Google Play settings for mobile) — the CLI does not change plans.

### Suggest next steps after a render

After an image: offer to animate it (`--video --ref <result>`), restyle it (`-c <result> "Apply style: ..."`), change the angle (`--multi-angle -c <result>`), generate variations (`-n 3 "{a|b|c}"`), or refine at `-Q pro`. After a video: offer different motion, dialogue (LTX), longer `--duration`, stitching (`--concat-videos`), or a soundtrack (`--concat-audio` / `--remix-audio`).

## JSON Output Contract

Success (`--json`):

```json
{
  "success": true,
  "prompt": "a cat wearing a hat",
  "model": "z_image_turbo_bf16",
  "width": 512,
  "height": 512,
  "urls": ["https://..."],
  "localPath": "./cat.png"
}
```

Failure (single JSON object on stdout, exit code 1; progress/warnings on stderr):

```json
{
  "success": false,
  "error": "Reference image 2314x1200 would resize to 512x266, but both dimensions must be divisible by 16.",
  "errorCode": "INVALID_VIDEO_SIZE",
  "errorType": "PARAMETER_INVALID",
  "errorCategory": "schema_validation",
  "retryable": false,
  "hint": "Try: --width 1296 --height 672 (or omit --strict-size)"
}
```

`--json --balance` → `{ "success": true, "type": "balance", "spark": 12.34, "sogni": 0.56, "username": "name", "subscription": { "active": true, "status": "active", "tier": "unlimited" } }` (`username`/`subscription` are `null` when unavailable; an active subscription means eligible renders are covered by Sogni Unlimited even when `spark` is low). `--last --json` wraps the last render record in a `{ "success": true, ... }` envelope and exits 1 with `errorCode: "NO_LAST_RENDER"` when nothing has been rendered. In `--json` mode stdout always carries exactly one JSON object — SSE workflow frames and progress lines go to stderr.

## Cost

Eligible Sogni-hosted renders use Unlimited coverage when active; otherwise renders use the selected Spark or SOGNI token path. 512x512 images are most cost-efficient. `-n` is safety-capped at 16 outputs per call (`SOGNI_MAX_COUNT` raises it deliberately). Seedance, HappyHorse, Wan 3, and GPT Image 2 are vendor models requiring Premium Spark eligibility.

## Troubleshooting

- **Anything broken?** Run `sogni-agent doctor` first — it checks Node, credentials (and file permissions), config-dir writability, ffmpeg, live auth, and version freshness, with a fix in every failure detail.
- **A newly listed live model fails immediately with `PROJECT_ERROR`:** if `doctor` reports a newer CLI, update before retrying. The live catalog can expose a model that needs model-specific client rules added after the installed CLI version; repeated submissions with generic defaults will fail the same way.
- **Auth errors:** check `SOGNI_API_KEY` or `~/.config/sogni/credentials` (key from https://dashboard.sogni.ai, account menu).
- **Error 4061 / too many app IDs:** the CLI leases stable IDs from the persistent pool in `~/.config/sogni/app-ids/`. Do not delete that directory between runs. For ephemeral/container homes, set the same `SOGNI_APP_ID` on every session. An existing block may require waiting before retrying after upgrading.
- **Kicked mid-render / SWITCH_CONNECTION 4015:** two processes shared one app ID. The slot pool prevents this for concurrent CLI runs; if a long-lived daemon also uses this account, give it its own pinned `SOGNI_APP_ID`.
- **Video size errors:** sizes are model-specific (WAN 2.2 ÷16 min 480 max 1536; Wan 3 uses its exact 480P/720P/1080P ratio buckets; LTX ÷64, long side ≤2048). The CLI auto-adjusts for local refs; `--strict-size` makes it fail with a suggested size instead. Details in [`references/models.md`](./references/models.md).
- **Timeouts:** try a faster model or raise `-t`.
- **No workers:** check https://sogni.ai for network status.

## Reference Index (read before acting)

| Read this | When the task involves |
|-----------|------------------------|
| [`references/interactive-worlds.md`](./references/interactive-worlds.md) | Building an explorable world end to end: the nine-model stack in order, the prepare/render/verify/retain loop, and the measured failure modes of each stage — segmentation prompts, matte thresholds, 3D input resolution, single-keyframe clips and reverse playback, dialogue loudness spread, voice-clone transcripts, on-camera lip-sync |
| [`references/image-prompting.md`](./references/image-prompting.md) | Writing prompt-only image deliverables for SD/SDXL/Pony, FLUX.1 Schnell, Chroma, Krea 2, Qwen, Z-Image, GPT Image, or model-specific edit operations |
| [`references/video-prompting.md`](./references/video-prompting.md) | Writing LTX video prompts; writing MiniMax H3 official ordered-field prompts, mode preambles, shot notation, speaker IDs, and dialogue tags; high-res/4K routing; orientation/aspect mapping; camera language |
| [`references/private-mature-video.md`](./references/private-mature-video.md) | Mature-theme video model, LoRA, frame modes, and prompt tokens |
| [`references/video-editing.md`](./references/video-editing.md) | Animate between images, continue/bridge videos, 360 turnarounds, concat, audio remix/layering, v2v ControlNet |
| [`references/loop-maker.md`](./references/loop-maker.md) | One-click image-folder loops with visual deduplication, direct LTX first/last-frame clips, music, and verification |
| [`references/hosted-api.md`](./references/hosted-api.md) | `--api-chat`, `--durable-chat`, `--api-workflow`, workflow templates, replays, Seedance reference modes, cost controls |
| [`references/seamless-tiling.md`](./references/seamless-tiling.md) | Seamless repeating patterns, wallpapers, tiling textures, Escher tessellations |
| [`references/models.md`](./references/models.md) | Choosing models, sizing/divisibility rules, image edit reference limits, music model options, SAM 3 segmentation and Pixal3D 3D options |
| [`references/krea2-loras.md`](./references/krea2-loras.md) | The 25 Krea 2 LoRAs: IDs, strength ranges, bipolar directions, community fine-tunes, live `--list-loras` discovery |
| [`references/h3-video-loras.md`](./references/h3-video-loras.md) | MiniMax H3 video LoRAs: per-mode availability, trigger words, positive-only strength bands, live catalog discovery |
| [`references/personas-memory.md`](./references/personas-memory.md) | Persona CRUD/voice cloning, multi-persona scenes, memories, personality, style transfer, photo restoration |
| [`references/openclaw-config.md`](./references/openclaw-config.md) | OpenClaw plugin config defaults and overrides |
| [`skills/README.md`](./skills/README.md) | Hosted per-skill tool surface (for hosts that load focused capability subsets) |

---
name: setup
description: First-run setup wizard for Remotion Superpowers. Checks dependencies, scaffolds a Remotion project if needed, installs and updates Remotion's 12 official Agent Skills (a required companion), walks through API key configuration, and verifies MCP server connections.
---

# Remotion Superpowers — Setup Wizard

You are running the setup wizard for the Remotion Superpowers plugin. Follow these steps carefully and guide the user through each one.

## Step 1: Check System Dependencies

Run these checks and report results:

```bash
node --version
npm --version
python3 --version 2>/dev/null || python --version 2>/dev/null
which uvx 2>/dev/null || echo "uvx not found"
```

**Required:**
- Node.js 22.18 or newer (needed for Remotion and MCP servers)
- npm (comes with Node.js)

**Recommended:**
- Python 3 + `uv`/`uvx` (only for the optional, deprecated ElevenLabs MCP server)
  - If missing, tell user: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Nothing extra for captions: word-level captions use the official `remotion-captions` flow (local Whisper via WebGPU), or ElevenLabs Scribe when there's no GPU.

Report each as ✓ or ✗ with version.

## Step 2: Check Remotion Project

Check if the current directory already has a Remotion project (a `remotion` dependency in `package.json`, usually with a `remotion.config.ts`).

**If YES:** Tell the user their Remotion project was detected.

**If NO:** Ask the user if they want to create one here or move to an existing project. To create one, scaffold it exactly as the official `remotion-create` skill says:
1. Inspect the current folder first, including hidden files (`ls -la`). Files such as `.env` or `.git` count as meaningful contents; only OS metadata such as `.DS_Store` is disposable.
2. Empty folder (or only disposable metadata, removed first):
   ```bash
   npx create-video@latest --yes --blank --no-tailwind .
   npm i
   ```
3. Folder with meaningful contents: scaffold into a subfolder and move into it:
   ```bash
   npx create-video@latest --yes --blank --no-tailwind my-video
   cd my-video
   npm i
   ```

Don't add TailwindCSS unless the user asks for it; the official skills scaffold without it.

Do NOT proceed until the user is in a Remotion project directory. If you moved into a new folder, restart the agent from there: the remotion-media tools write to `public/` of the directory the agent was launched from.

## Step 3: Install Remotion's Official Agent Skills (required)

Remotion Superpowers layers on top of Remotion's official Agent Skills. They're a **required companion**: this plugin generates and sources the media, and the official skills own Remotion markup, scaffolding, preview, captions and rendering. Without them the workflows have no Remotion API guidance.

Check that all 12 are installed (for example in `.claude/skills/`, `.agents/skills/`, `.codex/skills/` or `.gemini/skills/`):

`remotion-best-practices`, `remotion-captions`, `remotion-create`, `remotion-docs`, `remotion-interactivity`, `remotion-maps`, `remotion-markup`, `remotion-multimedia`, `remotion-render`, `remotion-saas`, `remotion-studio`, `remotion-upgrade`

**If any are missing:**
```bash
npx skills add remotion-dev/skills
```

`npx skills` detects the installed agents (Claude Code, Codex, Gemini CLI, Cursor, Copilot…) and installs to each. If it asks which skills to install, select all 12.

**Keep them current.** Remotion ships often, and the skills change with each release. From the project, run:
```bash
npx remotion upgrade
```
This upgrades Remotion and its packages and also updates the project-local Remotion skills (official `remotion-upgrade`). If `@remotion/cli` isn't installed locally, update the skills directly:
```bash
npx skills update remotion-best-practices remotion-captions remotion-create remotion-docs remotion-interactivity remotion-maps remotion-markup remotion-multimedia remotion-render remotion-saas remotion-studio remotion-upgrade --yes
```

**Also install the provider skills** this plugin builds on:
```bash
npx skills add elevenlabs/skills   # voice, sound effects, music, transcription
npx skills add replicate/skills    # only if the user wants Replicate models
```

Tell the user: "Remotion's official skills are installed. Your agent now knows Remotion's current APIs, preview, captions and rendering; Remotion Superpowers adds media generation on top."

## Step 4: Configure API Keys

Walk the user through each API key. For each one:
1. Explain what the service provides
2. Give the signup URL
3. Tell them the environment variable name
4. Ask them to set it: `export VAR_NAME=their-key`
5. Recommend adding to `~/.zshrc` or `~/.bashrc` for persistence

**Gemini CLI:** extensions don't inherit the shell environment. The keys are prompted for when the extension is installed; to change one later, run `gemini extensions config remotion-superpowers "ElevenLabs API key"` (or the matching setting name) instead of exporting it.

### 4a. ElevenLabs API Key (REQUIRED: voice, sound effects, music)
- **What:** Voiceovers, sound effects and music (Eleven Music, cleared for commercial use on paid plans), plus transcription for word-level captions when there's no GPU. Generated through the official ElevenLabs skills.
- **Signup:** https://elevenlabs.io (free tier available; a paid plan is needed for commercial music). Or run `npx -y @elevenlabs/cli@latest onboard init`, which signs in and stores a key for the project.
- **Variable:** `ELEVENLABS_API_KEY`
- **Command:** `export ELEVENLABS_API_KEY=your-key-here`
- **Persistence:** `echo 'export ELEVENLABS_API_KEY=your-key-here' >> ~/.zshrc`

### 4b. KIE API Key (REQUIRED: AI images and clips)
- **What:** AI image generation (Nano Banana Pro) and AI video clips (Veo 3.1) through the remotion-media server. It can also make cheap audio drafts, but KIE resells those models without their owners' licence, so final commercial audio should come from ElevenLabs.
- **Signup:** https://kie.ai (create an account, get an API key from the dashboard)
- **Variable:** `KIE_API_KEY`
- **Command:** `export KIE_API_KEY=your-key-here`
- **Persistence:** `echo 'export KIE_API_KEY=your-key-here' >> ~/.zshrc`

### 4c. TwelveLabs API Key (REQUIRED: video understanding and AI review)
- **What:** Lets your agent watch video: analyse footage, find moments, and review your rendered video with actionable fixes.
- **Signup:** https://www.twelvelabs.io (free tier available)
- **Variable:** `TWELVELABS_API_KEY`
- **Command:** `export TWELVELABS_API_KEY=your-key-here`
- **Persistence:** `echo 'export TWELVELABS_API_KEY=your-key-here' >> ~/.zshrc`

### 4d. Pexels API Key (RECOMMENDED: free stock footage)
- **What:** Free stock photos and videos. Search by keyword and download HD/4K clips into your project.
- **Signup:** https://www.pexels.com/api/ (free, instant)
- **Variable:** `PEXELS_API_KEY`
- **Command:** `export PEXELS_API_KEY=your-key-here`
- **Persistence:** `echo 'export PEXELS_API_KEY=your-key-here' >> ~/.zshrc`

### 4e. Replicate API Token (OPTIONAL: specific image/video models)
- **What:** Hundreds of models (FLUX.2, Kling, Seedance, Wan and more) when you want a specific model, or as a fallback when a KIE clip fails.
- **Signup:** https://replicate.com (create an account, get an API token)
- **Variable:** `REPLICATE_API_TOKEN`
- **Command:** `export REPLICATE_API_TOKEN=your-token-here`
- **Persistence:** `echo 'export REPLICATE_API_TOKEN=your-token-here' >> ~/.zshrc`

After each key, ask the user to confirm they've set it before moving to the next one. It's OK to skip optional ones.

## Step 5: Reload Shell & Verify

Tell the user to reload their shell:
```bash
source ~/.zshrc
```

Then verify the environment variables are set:
```bash
echo "ELEVENLABS_API_KEY: ${ELEVENLABS_API_KEY:+SET}"
echo "KIE_API_KEY: ${KIE_API_KEY:+SET}"
echo "TWELVELABS_API_KEY: ${TWELVELABS_API_KEY:+SET}"
echo "PEXELS_API_KEY: ${PEXELS_API_KEY:+SET}"
echo "REPLICATE_API_TOKEN: ${REPLICATE_API_TOKEN:+SET}"
```

## Step 6: Verify MCP Connections

Tell the user to check MCP server status:
```
/mcp
```

All configured servers should show as connected. If any fail:
- Check that the API key environment variable is set
- For `uvx`-based servers, ensure `uv` is installed
- For `npx`-based servers, ensure Node.js is installed
- Try restarting your agent (Claude Code, Codex, Gemini CLI…)

## Step 7: Setup Complete

Print a summary:

```
🎬 Remotion Superpowers — Setup Complete!

✓ Dependencies verified
✓ Remotion project detected
✓ Remotion official skills installed (12)
✓ API keys configured
✓ MCP servers connected

🎬 Production Commands:
  /create-video      — Full video production from a prompt
  /create-short      — Short-form vertical video (TikTok/Reels/Shorts)

🎨 Asset Commands:
  /find-footage      — Search & download stock footage from Pexels
  /generate-image    — Generate AI images for your video
  /generate-clip     — Generate AI video clips

🔊 Audio Commands:
  /add-voiceover     — Generate and add narration
  /add-music         — Generate and add background music
  /transcribe        — Transcribe audio/video to text

✨ Enhancement Commands:
  /add-captions      — TikTok-style animated captions
  /add-transitions   — Professional scene transitions

👁️ Analysis Commands:
  /analyze-footage   — Analyze existing video files with AI vision
  /review-video      — AI feedback loop (renders frames and the video for review)

Keep Remotion and its skills current: npx remotion upgrade

Try it: "Create a 30-second product demo video for a todo app"
```

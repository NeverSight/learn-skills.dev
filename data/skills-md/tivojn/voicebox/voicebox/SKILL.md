---
name: voicebox
description: "All-in-one voice toolkit: TTS (voice design + cloning), multi-speaker conversations/dramas/audiobooks, speech recording, and transcription. Activates on: /voicebox commands, \"clone my voice\", \"record my voice\", \"transcribe this\", \"create a conversation\", \"make a drama\", or any audio transcription request."
user_invocable: true
---

# Voicebox TTS Skill

Standalone text-to-speech using mlx-audio. Supports custom voice design (from text descriptions) and voice cloning (from audio samples). No external app required.

## Usage

### Generate speech
```
/voicebox "Calm Narrator" "Hello world"
/voicebox "angry tone" "My Voice" "I can't believe this!"   (style + profile)
```

### Create profiles
```
/voicebox create a calm narrator voice profile              (designed - from description)
/voicebox clone my voice from /path/to/audio.wav            (cloned - from audio file)
/voicebox clone my voice                                    (record from mic + clone)
```

### Transcribe audio/video
```
/voicebox transcribe /path/to/audio.wav
/voicebox transcribe /path/to/video.mp4
```

### Generate multi-speaker conversation
```
/voicebox create a news broadcast with anchor, reporter, and expert
/voicebox make a conversation between Calm Narrator and Cheerful Girl
/voicebox generate a drama scene with these characters...
```

### Trigger phrases (activates this skill automatically)
- "clone my voice", "record my voice", "create a voice clone"
- "transcribe this", "transcribe audio", "transcribe video"
- "create a conversation", "make a drama", "generate a dialogue", "audiobook"
- Any request involving audio/video transcription or speech-to-text

## Architecture

Three model categories with quality tiers:

| Category | Standard (default) | High | Use Case |
|----------|-------------------|------|----------|
| Voice Design | `Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` | (same — only 1.7B exists) | Custom voices from description |
| Voice Clone | `Qwen3-TTS-12Hz-0.6B-Base-bf16` | `Qwen3-TTS-12Hz-1.7B-Base-bf16` | Clone a real voice |
| ASR (Transcription) | `Qwen/Qwen3-ASR-0.6B` | `Qwen/Qwen3-ASR-1.7B` | Speech-to-text |

All commands accept `--quality standard` (default) or `--quality high` to select model tier.

All state is in `~/.claude/skills/voicebox/data/`:
- `profiles.json` — profile registry
- `samples/` — WAV files for reference audio

Script: `~/.claude/skills/voicebox/scripts/voicebox.py`

---

## Mode 1: Generate Speech

### Step-by-step workflow

1. **Parse arguments** — First quoted arg is profile name (or style + profile). Second is text to speak. If three quoted args, first is style/instruct, second is profile name, third is text.

2. **Find the profile** — Look up the profile name in profiles.json (case-insensitive, partial match OK).

3. **Generate audio** using the script:
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/voicebox.py generate "Profile Name" "text to speak" --play
   ```
   With optional style override for designed voices:
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/voicebox.py generate "Profile Name" "text to speak" --instruct "angry tone" --play
   ```
   With high quality (1.7B model) for cloned voices:
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/voicebox.py generate "Profile Name" "text to speak" --quality high --play
   ```
   **IMPORTANT**: Use timeout of 300000ms — model loading + generation takes time on first run.

4. **Report result** — Tell the user the audio was generated and played. Show duration and profile used.

### If no profiles exist
Offer to create one using Mode 2.

---

## Mode 2: Create Voice Profile from Description (Designed)

When the user says "create a ... voice profile":

1. **Parse the voice description** from the user's request.

2. **Build a rich voice description** — Expand the user's short description into a detailed multi-dimensional voice prompt:
   - Template: `[Age] [gender] with a [pitch] [characteristic] voice, [speaking rate] pace, [emotion/tone], suitable for [use case]`
   - Example: "calm narrator" → "Calm middle-aged male narrator with a deep warm baritone voice, slow measured pace, soothing and trustworthy tone, suitable for audiobook narration"
   - Be specific: use "deep", "crisp", "fast-paced", not vague words like "nice"

3. **Choose a sample text** that matches the voice emotion:
   - Neutral: "The morning sun rose gently over the quiet village, casting golden light across the cobblestone streets. Birds sang their morning songs as the world slowly came to life."
   - Angry: "I told you a hundred times not to do that. This is absolutely unacceptable and I will not stand for it anymore."
   - Cheerful: "Hey everyone, welcome back! I have some amazing news to share with you today, and I just can't wait to get started!"

4. **Create the profile**:
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/voicebox.py create-designed "Calm Narrator" \
     --desc "Calm middle-aged male narrator with a deep warm baritone voice, slow measured pace, soothing and trustworthy tone, suitable for audiobook narration" \
     --lang en
   ```
   **IMPORTANT**: Use timeout of 300000ms.

5. **Confirm** — Tell the user the profile was created and is ready to use.

### Profile Naming Convention
- Derive from the user's description, capitalize as title: "Calm Narrator", "Angry Woman"
- Keep it short (2-3 words)

---

## Mode 3: Create Voice Profile from Audio File (Cloned)

When the user says "clone my voice from /path/to/file.wav" or provides an audio file:

1. **Get the audio file path** and a transcript of what was said in the recording.

2. **If no transcript provided**, auto-transcribe using the built-in transcription:
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/transcribe.py /path/to/audio.wav
   ```
   Only ask the user as a last resort.

3. **Create the profile**:
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/voicebox.py create-cloned "My Voice" \
     --audio /path/to/sample.wav \
     --ref-text "transcript of what was said" \
     --lang en
   ```

4. **Confirm** — Tell the user the profile was created.

---

## Mode 4: Record from Microphone and Clone (IMPORTANT)

**This mode activates when the user says "clone my voice", "record my voice", "I want to clone a voice", or any request to clone without providing an audio file.**

### Step-by-step workflow

1. **Ask the user for a profile name** (or derive one like "My Voice", "[User's Name]'s Voice").

2. **Ask what they'd like to say**, or suggest a good sample sentence:
   - "The morning sun rose gently over the quiet village, casting golden light across the cobblestone streets."
   - Or let them say anything — 5-15 seconds of clear speech works best.

3. **Confirm they're ready**, then **record and auto-clone in one command**:
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/voicebox.py record "My Voice" --duration 10 --lang en
   ```
   - Default is 10 seconds. Adjust with `--duration` if the user wants more/less.
   - If the user already knows what they'll say, pass it: `--ref-text "what they said"` (skips transcription)
   - **Without `--ref-text`**, the command auto-transcribes using the built-in `transcribe.py` (Qwen3-ASR) — no external skill needed!
   - **IMPORTANT**: Use timeout of 300000ms.

4. **Play back the recording** so the user can verify:
   ```bash
   afplay ~/.claude/skills/voicebox/data/samples/<slug>.wav
   ```

5. **Confirm** — Tell the user the profile was created and is ready to use with `/voicebox "My Voice" "text to speak"`.

### Requirements
- **ffmpeg** must be installed (`brew install ffmpeg`)
- macOS microphone permission must be granted to the terminal app

---

## Mode 5: Transcribe Audio/Video

**This mode activates when the user says "transcribe this", "transcribe audio/video", provides an audio/video file for transcription, or any speech-to-text request.**

### Step-by-step workflow

1. **Get the file path** from the user's request.

2. **Run transcription**:
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/transcribe.py /path/to/file.wav
   ```
   With optional language:
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/transcribe.py /path/to/file.wav --language zh
   ```
   **IMPORTANT**: Use timeout of 300000ms.

3. **Return the transcript** to the user.

### Supported formats
- **Audio:** wav, mp3, flac, m4a, ogg, aac, wma
- **Video:** mp4, mkv, mov, avi, webm, m4v, flv, wmv (ffmpeg extracts audio automatically)

### Supported languages
52 languages with auto-detection including: English, Chinese (+ dialects), Japanese, Korean, German, French, Spanish, Italian, Portuguese, Russian, Arabic, Hindi, Thai, Vietnamese, Indonesian, and more.

---

## Mode 6: Generate Conversation / Audiobook / Drama

**This mode activates when the user asks for a multi-speaker conversation, dialogue, drama, audiobook with multiple characters, news broadcast, or any scenario involving multiple voice profiles speaking in sequence.**

### Step-by-step workflow

1. **Create a JSON script file** based on the user's request. The script format is:
   ```json
   {
     "title": "Evening News",
     "gap": 0.25,
     "lines": [
       {"profile": "News Anchor", "text": "Good evening and welcome to the six o'clock news."},
       {"profile": "Young Reporter", "text": "Thanks, Tom! I'm here live at the scene.", "instruct": "excited field reporting tone"},
       {"profile": "Expert Guest", "text": "Well, this is actually quite common in my experience."}
     ]
   }
   ```

   **Script fields:**
   - `title` — Name for the output directory and combined file
   - `gap` — Silence between segments in seconds (default: 0.25)
   - `lines` — Array of dialogue lines, each with:
     - `profile` — Name of an existing voice profile (must match exactly or partially)
     - `text` — The text to speak
     - `instruct` — (Optional) Style/emotion override, only works for "designed" profiles

2. **Save the script** to a temp file:
   ```bash
   cat > /tmp/my_script.json << 'EOF'
   { ... }
   EOF
   ```

3. **Check that required profiles exist** — Run `list` first. If profiles are missing, create them first using Mode 2 or Mode 3.

4. **Run the conversation command:**
   ```bash
   uv run ~/.claude/skills/voicebox/scripts/voicebox.py conversation /tmp/my_script.json --play
   ```
   **IMPORTANT**: Use timeout of 300000ms — multi-segment generation can take several minutes.

   **Options:**
   - `--output-dir DIR` / `-o DIR` — Where to save segments + combined (default: `/tmp/voicebox_{title_slug}`)
   - `--gap 0.5` — Override gap between segments (overrides script value)
   - `--quality high` — Use 1.7B models for better quality
   - `--trim-silence` (default) / `--no-trim-silence` — ffmpeg silence trimming on each segment
   - `--play` / `--no-play` — Play the combined result when done

5. **Report results** — Show the per-segment durations and combined total from the script output.

### How to write good conversation scripts

- **Keep lines short** — 1-3 sentences per line works best. Split long monologues into multiple lines.
- **Use `instruct` for emotion** — For designed profiles, add `"instruct": "excited tone"` or `"instruct": "whispering"` to override the default voice description per-line.
- **Mix profile types** — You can freely mix designed and cloned profiles in the same script.
- **Gap tuning** — 0.15-0.25s for fast dialogue, 0.4-0.6s for dramatic pauses, 0.8-1.0s for scene breaks.

### Example: News broadcast
```json
{
  "title": "Evening News",
  "gap": 0.3,
  "lines": [
    {"profile": "News Anchor", "text": "Good evening. Tonight's top story: a breakthrough in renewable energy."},
    {"profile": "Young Reporter", "text": "Thanks, Tom. I'm here at the research lab where scientists made the announcement earlier today."},
    {"profile": "Expert Guest", "text": "This discovery could fundamentally change how we think about solar power. The efficiency gains are remarkable."},
    {"profile": "News Anchor", "text": "Fascinating. We'll have more on this story after the break."}
  ]
}
```

### Requirements
- **ffmpeg** must be installed for `--trim-silence` (default: on). Use `--no-trim-silence` if ffmpeg is unavailable.
- All profiles referenced in the script must already exist.

---

## Script Commands Reference

```bash
# List all profiles
uv run ~/.claude/skills/voicebox/scripts/voicebox.py list

# List available models and quality tiers
uv run ~/.claude/skills/voicebox/scripts/voicebox.py models

# Create designed voice profile
uv run ~/.claude/skills/voicebox/scripts/voicebox.py create-designed "Name" --desc "description" --lang en

# Create cloned voice profile (from existing audio file)
uv run ~/.claude/skills/voicebox/scripts/voicebox.py create-cloned "Name" --audio /path/to.wav --ref-text "transcript" --lang en

# Record from microphone and clone (with known transcript)
uv run ~/.claude/skills/voicebox/scripts/voicebox.py record "Name" --duration 10 --lang en --ref-text "what I said"

# Record from microphone and clone (auto-transcribe, high quality ASR)
uv run ~/.claude/skills/voicebox/scripts/voicebox.py record "Name" --duration 10 --lang en --quality high

# Transcribe an audio file (built-in, no external skill needed)
uv run ~/.claude/skills/voicebox/scripts/transcribe.py /path/to/audio.wav

# Transcribe with high quality ASR (1.7B model)
uv run ~/.claude/skills/voicebox/scripts/transcribe.py /path/to/audio.wav --model Qwen/Qwen3-ASR-1.7B

# Generate speech
uv run ~/.claude/skills/voicebox/scripts/voicebox.py generate "Name" "text" --play

# Generate with high quality (1.7B clone model)
uv run ~/.claude/skills/voicebox/scripts/voicebox.py generate "Name" "text" --play --quality high

# Generate with style override
uv run ~/.claude/skills/voicebox/scripts/voicebox.py generate "Name" "text" --instruct "angry" --play

# Generate a multi-speaker conversation from JSON script
uv run ~/.claude/skills/voicebox/scripts/voicebox.py conversation /tmp/script.json --play

# Conversation with custom gap and no silence trimming
uv run ~/.claude/skills/voicebox/scripts/voicebox.py conversation /tmp/script.json --gap 0.5 --no-trim-silence -o /tmp/my_show

# Conversation with high quality models
uv run ~/.claude/skills/voicebox/scripts/voicebox.py conversation /tmp/script.json --quality high --play

# Delete a profile
uv run ~/.claude/skills/voicebox/scripts/voicebox.py delete "Name"
```

## Quality Tiers

All TTS and recording commands default to `--quality high` (1.7B). Use `--quality standard` for faster 0.6B models:

| Tier | Clone Model | ASR Model | RAM Needed | Speed |
|------|------------|-----------|------------|-------|
| **high** (default) | 1.7B (~3.5GB) | 1.7B (~3.5GB) | ~8GB+ | Better quality |
| **standard** | 0.6B (~1.5GB) | 0.6B (~1.5GB) | ~4GB+ | Faster, less RAM |

Voice Design always uses 1.7B (only available size).

When the user asks for "faster" or "lighter", use `--quality standard`.

## Voice Description Guide

### Quick Rules
1. **Be Specific** — Use "deep", "crisp", "fast-paced", not "nice" or "good"
2. **Multi-Dimensional** — Combine gender + age + emotion + speaking style
3. **Be Objective** — Describe voice features, not preferences
4. **Be Original** — Never request celebrity imitations
5. **Be Concise** — Every word should add meaning

### Good Examples
```
"Calm middle-aged male with deep magnetic voice, medium pace, warm and trustworthy"
"Young adult female with crisp energetic tone, fast pace, cheerful and engaging"
"Senior male narrator with slow rich baritone, composed delivery, for audiobook"
"Angry adult female with sharp intense voice, fast aggressive pace, furious and commanding"
```

## Supported Languages

English (en), Chinese (zh), Japanese (ja), Korean (ko), German (de), French (fr), Russian (ru), Portuguese (pt), Spanish (es), Italian (it). Default is English.

## Error Handling

| Error | Action |
|-------|--------|
| No matching profile | Show available profiles, offer to create one |
| No profiles exist | Offer to create one using Mode 2 |
| Model not yet downloaded | Inform user, it auto-downloads on first use (~3GB) |
| Generation fails | Show error message, check mlx-audio is installed |
| `uv` not accessible from sandbox | Use Task tool with general-purpose subagent |

## First-Time Download

On first use, models are downloaded from HuggingFace (~3.5GB each for 1.7B). The scripts detect this automatically and print:

```
First-time setup: downloading <model> (~3.5GB)...
This is a one-time download — future runs will be instant.
```

**IMPORTANT for Claude**: When running any voicebox command for the first time (or after clearing the HF cache), warn the user that the first run will take several minutes to download models. Use a timeout of 300000ms (5 minutes) for all generation, recording, and transcription commands. Subsequent runs load from cache and are much faster.

## Implementation Notes

- Audio output is WAV format at 24000 Hz sample rate
- Models are cached at `~/.cache/huggingface/hub/`
- The `mlx-audio` package auto-installs via `uv` on first run
- If the Bash sandbox blocks access to `~/.claude/skills/`, use a Task tool with `general-purpose` subagent type which gets a fresh shell
- Clean up temp files after playing: `rm -f /tmp/voicebox_output.wav`

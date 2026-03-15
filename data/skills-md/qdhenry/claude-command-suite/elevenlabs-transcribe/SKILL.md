---
name: elevenlabs-transcribe
description: Transcribes audio/video files using ElevenLabs Scribe v2 API. Use when transcribing audio files, generating transcripts, or converting speech to text.
argument-hint: <audio-file> [--output transcript.txt] [--language eng] [--num-speakers 2] [--keyterms "term1" "term2"]
---

<objective>
Transcribe audio or video files using the ElevenLabs Speech-to-Text API (Scribe v2). Accepts a file path and optional parameters, reads the API key from the project's .env file, and returns a formatted transcription with speaker diarization and audio event tagging.
</objective>

<quick_start>
**Via slash command:**
`/elevenlabs-transcribe path/to/audio.mp3`
`/elevenlabs-transcribe path/to/audio.mp3 --output transcript.txt --num-speakers 3`

**Requirements:**
- `ELEVENLABS_API_KEY` in the project's `.env` file
- `uv` installed (dependencies auto-install via PEP 723)
</quick_start>

<prerequisites>
Before transcribing, verify:

1. **`uv` is available** (dependency installation is automatic via inline script metadata — no venv or manual pip install needed)

2. **API key configured** in the `.env` file where Claude is running:
   ```
   ELEVENLABS_API_KEY=your-key-here
   ```

3. **Audio file exists** and is a supported format (mp3, wav, mp4, m4a, ogg, flac, webm, etc.)

**MUST** stop if the API key is missing — inform the user to add it to their `.env` file.
</prerequisites>

<process>

**Step 1: Parse user input**

Extract the audio file path and any options from `$ARGUMENTS` or the user's message. Supported options:
- `--output <path>` or `-o <path>` — where to save the transcript
- `--language <code>` — ISO-639 language code (e.g., eng, spa, fra, deu, jpn, zho)
- `--num-speakers <n>` — max speakers in the audio (1-32)
- `--keyterms "term1" "term2"` — words/phrases to bias transcription towards
- `--timestamps none|word|character` — timestamp granularity
- `--no-diarize` — disable speaker identification
- `--no-audio-events` — disable audio event tagging
- `--json` — output full JSON response

**Step 2: Validate the audio file**

Confirm the file path exists. Expand `~` paths. The script handles validation automatically but check early for a clear error message.

**Step 3: Check for API key**

```bash
grep -q "ELEVENLABS_API_KEY=" .env 2>/dev/null && echo "API key configured" || echo "API key missing"
```

If missing, tell the user to add `ELEVENLABS_API_KEY=` to their `.env` file and **stop**.

**Step 4: Run transcription**

Dependencies are installed automatically by `uv` via inline script metadata (PEP 723). No venv or manual pip install needed.

Basic transcription (diarize + audio events + auto language):
```bash
uv run ~/.claude/skills/elevenlabs-transcribe/scripts/transcribe.py "<audio_file_path>"
```

With output file and options:
```bash
uv run ~/.claude/skills/elevenlabs-transcribe/scripts/transcribe.py "<audio_file_path>" --output transcript.txt --language eng --num-speakers 3
```

With key terms for better accuracy:
```bash
uv run ~/.claude/skills/elevenlabs-transcribe/scripts/transcribe.py "<audio_file_path>" --keyterms "technical term" "product name"
```

Full JSON response:
```bash
uv run ~/.claude/skills/elevenlabs-transcribe/scripts/transcribe.py "<audio_file_path>" --json --output result.json
```

**Step 5: Present results**

Format the transcription output cleanly for the user. If diarization is enabled, group text by speaker. Highlight any audio events detected. Example output:

```
[Speaker 0]: Hello, how are you doing today?
[Speaker 1]: I'm doing great, thanks for asking! (laughter)
```

</process>

<script_options>
| Flag | Description | Default |
|------|-------------|---------|
| `<file>` | Path to audio/video file (required) | - |
| `--output <path>`, `-o` | Save transcription to file | stdout |
| `--language <code>` | ISO-639 code (eng, spa, fra, deu, jpn, zho) | auto-detect |
| `--num-speakers <n>` | Max speakers in audio (1-32) | auto-detect |
| `--keyterms "t1" "t2"` | Terms to bias transcription towards (max 100) | none |
| `--timestamps <level>` | Granularity: none, word, character | word |
| `--no-diarize` | Disable speaker identification | diarize enabled |
| `--no-audio-events` | Disable audio event tagging | events enabled |
| `--json` | Output full JSON response | formatted text |
</script_options>

<supported_formats>
All major audio and video formats: mp3, wav, mp4, m4a, ogg, flac, webm, aac, wma, mov, avi, mkv, and more. Maximum file size: 3GB.
</supported_formats>

<api_details>
- **Endpoint:** POST /v1/speech-to-text
- **Model:** scribe_v2 (latest, most accurate)
- **Diarization:** Identifies and labels different speakers (up to 32)
- **Audio events:** Tags non-speech sounds like (laughter), (applause), (music)
- **Language:** Auto-detected or specified via ISO-639 code
- **Timestamps:** none, word-level, or character-level granularity
- **Key terms:** Bias transcription towards specific words/phrases for better accuracy
</api_details>

<error_handling>
| Error | Resolution |
|-------|------------|
| `ELEVENLABS_API_KEY not found` | Add key to `.env` file in current directory |
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh` pipe to `sh` |
| `File not found` | Verify the file path and expand any `~` |
| `422 Validation Error` | Check file format/size, ensure model_id is valid |
| `401 Unauthorized` | API key is invalid or expired |
</error_handling>

<success_criteria>
- Audio file exists and is accessible
- API key loaded from `.env` without exposure in chat
- Transcription completed successfully
- Output formatted with speaker labels (if diarized)
- Audio events shown inline (if enabled)
- If `--output` specified, file written to requested path
- User can see the full transcription text
</success_criteria>

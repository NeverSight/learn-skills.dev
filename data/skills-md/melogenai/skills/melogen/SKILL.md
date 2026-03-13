---
name: melogen
description: "Convert sheet music to MIDI and MusicXML, transcribe audio to MIDI, and analyze music structure via the Melogen CLI. Capabilities: sheet music OCR/OMR, PDF to MIDI, PNG/JPG score to MIDI, MP3/WAV/FLAC/OGG/M4A audio to MIDI, polyphonic transcription, stem separation, beat quantization, music theory analysis (key, harmony, form, tonality). Use for: music transcription, music notation, music production, audio transcription, score digitization, MIDI conversion, music AI, music analysis, music generation workflow. Triggers: music, midi, sheet music, sheet2midi, music2midi, audio to midi, pdf to midi, mp3 to midi, wav to midi, musicxml, OMR, optical music recognition, music score, piano to midi, guitar to midi, song to midi, transcribe music, music notation, music theory, chord analysis, key detection, harmony analysis, melogen, melogenai"
allowed-tools:
  - Bash(melogen *)
  - Bash(pip install melogenai)
---

# Melogen CLI

AI-powered music tools: convert sheet music to MIDI, transcribe audio to MIDI, and analyze music structure.

## Setup

1. Get your API key from [melogenai.com/zh/mcp](https://melogenai.com/zh/mcp)
2. Install the CLI and set your key:

```bash
pip install melogenai
export MELOGEN_API_KEY=melo_xxx
```

3. Verify your key works:

```bash
melogen auth verify
```

## Commands

### `melogen sheet2midi FILE_URL`

Convert sheet music (PDF/PNG/JPG) to MIDI and MusicXML.

```bash
# Basic conversion (outputs both MIDI and MusicXML)
melogen sheet2midi https://example.com/score.pdf

# Only MusicXML output
melogen sheet2midi https://example.com/score.pdf -f musicxml --no-midi

# Specify multiple output formats explicitly
melogen sheet2midi https://example.com/score.png -f midi -f musicxml
```

| Flag | Description |
|------|-------------|
| `-f`, `--format` | Output format: `midi`, `musicxml` (repeatable) |
| `--no-midi` | Skip MIDI output |

### `melogen music2midi FILE_URL`

Convert audio files (MP3/WAV/FLAC/OGG/M4A) to MIDI.

```bash
# Basic conversion
melogen music2midi https://example.com/song.mp3

# Save separated instrument stems
melogen music2midi https://example.com/song.wav --stems

# Quantize to nearest beat
melogen music2midi https://example.com/song.flac --quantize

# Both stems and quantization
melogen music2midi https://example.com/song.mp3 --stems --quantize
```

| Flag | Description |
|------|-------------|
| `--stems` | Save separated instrument stems |
| `--quantize` | Quantize MIDI output to nearest beat |

### `melogen analysis`

Analyze music structure, tonality, harmony, and form. Provide at least one input source.

```bash
# Analyze from sheet music image
melogen analysis --image https://example.com/score.png

# Analyze from PDF
melogen analysis --pdf https://example.com/score.pdf

# Analyze from MusicXML
melogen analysis --mxl https://example.com/score.mxl

# Specify language (default: en)
melogen analysis --image https://example.com/score.png --lang zh

# Disable streaming (get full result at once)
melogen analysis --pdf https://example.com/score.pdf --no-stream
```

| Flag | Description |
|------|-------------|
| `--mxl` | URL of a MusicXML (.mxl) file |
| `--image` | URL of a sheet music image |
| `--pdf` | URL of a PDF score |
| `--lang` | Language for analysis output (default: `en`) |
| `--stream` / `--no-stream` | Stream output as generated (default: stream) |

At least one of `--mxl`, `--image`, or `--pdf` is required.

Supported languages: `en`, `zh`, `tw`, `ja`, `ko`, `de`, `fr`, `es`, `pt`, `it`, `ru`, `pl`, `el`, `vi`

### `melogen auth verify`

Verify your API key is valid. Reports user ID and scopes.

```bash
melogen auth verify
```

## Global Options

These options apply to all commands:

| Option | Env Variable | Description |
|--------|-------------|-------------|
| `--api-key` | `MELOGEN_API_KEY` | Melogen API key |
| `--base-url` | `MELOGEN_BASE_URL` | Override API base URL |
| `--version` | | Show version and exit |

## Error Handling

| Error | HTTP Status | Cause | Fix |
|-------|-------------|-------|-----|
| `Invalid or expired API key` | 401 | Bad or expired API key | Run `melogen auth verify`; get a new key from [melogenai.com](https://melogenai.com) |
| `Insufficient credits` | 402 | Account out of credits | Top up credits at [melogenai.com](https://melogenai.com) |
| `Validation error` | 422 | Invalid parameters or unsupported file format | Check file URL is accessible and format is supported |
| `Rate limit exceeded` | 429 | Too many requests | Wait and retry; reduce request frequency |
| `Task ... timed out` | -- | Processing exceeded timeout | Retry; for audio, shorter files process faster |
| `Task ... failed` | -- | Server-side processing error | Retry with a different file or check input quality |

All errors print to stderr and exit with code 1.

## Tips

- **Input quality matters**: Use high-resolution scans (300+ DPI) for sheet music. Use lossless formats (WAV/FLAC) for audio when possible.
- **Format choice**: For sheet music, multi-page PDFs are preferred over separate image files. For audio, WAV/FLAC give better accuracy than MP3.
- **Stems for complex audio**: Enable `--stems` when converting multi-instrument recordings to get cleaner per-instrument MIDI tracks.
- **Quantize for clean MIDI**: Use `--quantize` to snap notes to the nearest beat for cleaner MIDI output.
- **Streaming analysis**: Analysis streams by default so you see results as they generate. Use `--no-stream` if you need the complete output at once.
- **Audio takes longer**: Audio-to-MIDI conversion is more computationally intensive than sheet music conversion. The default polling timeout is 600 seconds.

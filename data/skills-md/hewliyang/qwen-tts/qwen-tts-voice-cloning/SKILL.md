---
name: qwen-tts-voice-cloning
description: End-to-end voice cloning pipeline using qwen-tts on Apple Silicon. Covers data collection (yt-dlp), audio cleaning (ASR with parakeet-tdt-0.6b-v3), data preparation, LoRA fine-tuning, generation, and evaluation via ASR intelligibility check (local, no API) + Gemini-as-judge (qwen-tts check). Use when the user wants to clone a voice, train a TTS model, prepare voice training data, evaluate generated speech quality, or run the full collect→clean→prepare→train→generate→eval pipeline.
allowed-tools: Bash, Read, Write, Edit
---

# Qwen-TTS Voice Cloning Pipeline

Full ML lifecycle for voice cloning on Apple Silicon (MLX). The `qwen-tts` package is installed via pip/uv and provides both a CLI and Python API.

## Installation

```bash
# Install the package (includes mlx-audio, librosa, etc.)
uv pip install qwen-tts

# Additional tools for data collection & cleaning
brew install yt-dlp ffmpeg  # if not already installed
uv pip install google-genai python-dotenv  # for eval step
```

## Quick Reference

```
qwen-tts split     <audio> -o ./clips              # ASR-based split + transcribe
qwen-tts prepare   --data <dir> -o train.jsonl
qwen-tts train     --name <speaker> --data train.jsonl -o ./<speaker>_voice
qwen-tts generate  -m custom-voice --voice-model <dir> --speaker <name> -p "text" -o out.wav
qwen-tts check     -g <generated> -r <reference> -S "<Speaker Name>"
qwen-tts voices    [dir]
qwen-tts speakers  --voice-model <dir>
```

**Always start with the 0.6B model.** It trains faster, uses less memory, and produces good results. Only try 1.7B if 0.6B quality is insufficient.

## Pipeline Overview

```
1. Collect     →  yt-dlp + ffmpeg
2. Split       →  qwen-tts split (ASR sentence-aligned splitting + transcription)
3. Prepare     →  qwen-tts prepare (encodes audio → codec tokens)
4. Train       →  qwen-tts train (LoRA SFT, ~15 min on M-series)
5. Generate    →  qwen-tts generate
6. Evaluate    →  qwen-tts check (Gemini-as-judge)
7. Iterate     →  adjust data / hyperparams based on eval
```

---

## Step 1: Data Collection

### Target: ~10 minutes of clean speech

```bash
# Download audio from YouTube
yt-dlp -x --audio-format wav -o "raw_audio/%(title)s.%(ext)s" "https://youtube.com/watch?v=VIDEO_ID"

# Convert to 24kHz mono WAV (required format)
ffmpeg -i "raw_audio/source.wav" -ar 24000 -ac 1 "raw_audio/source_24k.wav"
```

### Multiple YouTube sources

```bash
for url in "URL1" "URL2" "URL3"; do
  yt-dlp -x --audio-format wav -o "raw_audio/%(id)s.%(ext)s" "$url"
done

# Combine into one file
ffmpeg -f concat -safe 0 -i <(for f in raw_audio/*.wav; do echo "file '$f'"; done) \
  -ar 24000 -ac 1 "raw_audio/combined_24k.wav"
```

**Guidelines:**

- 24kHz mono WAV is the required format
- Prefer clear speech (interviews, lectures, speeches)
- Remove music, background noise, other speakers before splitting

---

## Step 2: Split + Transcribe (ASR-based)

Uses parakeet ASR to split audio on **sentence boundaries** and generate transcripts in one step. No more blind fixed-duration chopping.

```bash
qwen-tts split raw_audio/source_24k.wav -o ./clips --max-dur 8
```

This will:

1. Run parakeet ASR on the full audio → sentence-level timestamps
2. Merge short sentences into clips (3–8s target range)
3. Slice audio at sentence boundaries
4. Write clips + `transcript.txt`

### Options

- `--min-dur 3.0` — minimum clip duration (seconds)
- `--max-dur 8.0` — maximum clip duration (seconds). **Keep ≤10s** — longer clips use more memory during training and can cause OOM with gradient accumulation.
- `--pad 0.1` — padding around clip boundaries (seconds)
- `--asr-model mlx-community/parakeet-tdt-0.6b-v3` — ASR model

### After splitting, review `transcript.txt` and:

- Fix transcription errors (they become training labels)
- Remove clips with multiple speakers or heavy background noise
- Ensure proper punctuation and capitalization

### transcript.txt format

```
clip_000.wav|The stage that we have reached in Singapore. It was colorful, it was moving.
clip_001.wav|These two need not run counter to each other. But in practice, they tend to...
clip_002.wav|And the human knowledge approach tends to complicate methods in ways that...
```

One line per clip: `filename|transcription`. Filename is relative to the data directory.

---

## Step 3: Prepare Training Data

Encodes each audio clip through the speech tokenizer → codec tokens. Takes ~1-2 min for 75 clips.

```bash
qwen-tts prepare --data ./clips -o ./clips/train.jsonl --model-id mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16
```

This will:

1. Read `clips/transcript.txt` automatically (or pass `--transcript`)
2. Use first clip as reference audio (or pass `--ref-audio`)
3. Encode each clip → 16-codebook tokens at 12Hz
4. Write `train.jsonl`

### train.jsonl format

Each line is a JSON object:

```json
{
  "audio": "clips/clip_000.wav",
  "text": "The stage that we have reached in Singapore.",
  "ref_audio": "./clips/clip_000.wav",
  "audio_codes": [[1995, 431, 581, ...], [215, 431, 321, ...], ...]
}
```

- `audio_codes`: 2D array `[time_frames, 16]` — 16 codebooks at 12Hz

### Directory structure after prepare

```
clips/
  clip_000.wav ... clip_074.wav
  transcript.txt
  train.jsonl
```

---

## Step 4: Train (LoRA SFT)

```bash
qwen-tts train \
  --name <speaker_name> \
  --data ./clips/train.jsonl \
  --output ./<speaker_name>_voice \
  --model-id mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16 \
  --epochs 3 \
  --lr 2e-5 \
  --grad-accum 4 \
  --lora-rank 8
```

### Hyperparameters

| Parameter      | Default | Notes                                                                                                                                        |
| -------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `--epochs`     | 3       | 2-5 typical. More risks overfitting with small data.                                                                                         |
| `--lr`         | 2e-5    | Lower (1e-5) for clean data, higher (5e-5) if underfitting.                                                                                  |
| `--grad-accum` | 4       | Effective batch = batch_size × grad_accum. **Use 2 if clips are long (>8s) or training hangs — reduces peak memory from holding gradients.** |
| `--lora-rank`  | 8       | 4 for subtle shifts, 16 for stronger adaptation.                                                                                             |
| `--lora-scale` | 20.0    | Higher = stronger LoRA effect.                                                                                                               |
| `--batch-size` | 1       | Keep at 1 unless >64GB RAM.                                                                                                                  |

### What to watch

- Loss should drop from ~4-6 to ~2-3 over 3 epochs
- Loss plateaus above 4 → data quality issue or lr too low
- Loss below 1 → overfitting, reduce epochs
- Epoch 0 is slow (~15 min) due to one-time Metal JIT shader compilation; subsequent epochs are fast (~40-60s each)
- Peak memory: ~5-7GB

---

## Step 5: Generate

```bash
qwen-tts generate \
  -m custom-voice \
  --voice-model ./<speaker_name>_voice \
  --speaker <speaker_name> \
  --size 0.6B \
  -p "Text to synthesize." \
  -o output.wav
```

### Batch generate for evaluation

```bash
mkdir -p eval_clips
prompts=(
  "The future depends on what we do today."
  "We must be pragmatic and face reality as it is."
  "Education is the key to progress and prosperity."
)
for i in "${!prompts[@]}"; do
  qwen-tts generate -m custom-voice --voice-model ./<speaker_name>_voice \
    --speaker <speaker_name> --size 0.6B \
    -p "${prompts[$i]}" \
    -o "eval_clips/gen_$(printf '%02d' $i).wav"
done
```

### Options

- `--seed N` — reproducible output
- `--play` — play audio after generation
- Generation speed: ~0.5x real-time on M-series

---

## Step 6: Evaluate

Two complementary checks. Run ASR first (free, local, fast) to catch intelligibility issues, then Gemini (API calls) for speaker similarity.

### 6a: ASR intelligibility check (local, no API key)

Runs parakeet on generated clips, compares transcription against the prompt text via word error rate (WER). Catches garbled speech, missing words, mispronunciations.

```bash
# ASR-only — no API key needed
qwen-tts check \
  -g ./eval_clips \
  --asr-only \
  --expected-text \
    "gen_00.wav=The future depends on what we do today." \
    "gen_01.wav=We must be pragmatic and face reality as it is."
```

### 6b: Gemini speaker similarity check (API calls)

Requires `GEMINI_API_KEY` in environment or `.env` file. If not set, ask the user to provide one.

```bash
qwen-tts check \
  -g ./eval_clips \
  -r ./clips \
  -S "Speaker Name" \
  --max-clips 3 \
  --pairs 3
```

### 6c: Both together (recommended)

```bash
qwen-tts check \
  -g ./eval_clips \
  -r ./clips \
  -S "Speaker Name" \
  --max-clips 3 \
  --pairs 3 \
  --expected-text \
    "gen_00.wav=The future depends on what we do today." \
    "gen_01.wav=We must be pragmatic and face reality as it is."

# Add --json for machine-readable output
```

### How it works

**ASR check** (local, 0 API calls): runs `mlx_audio.stt.generate` with `parakeet-tdt-0.6b-v3`, computes WER against expected text. Only runs for clips with `--expected-text`.

**Gemini check** — total API calls = `max_clips + pairs` (report computed locally):

- **Single clip eval** (1 call/clip):

  ```json
  {
    "speaker_match": "yes|no|uncertain",
    "confidence": "low|medium|high",
    "natural": true,
    "audio_quality": "poor|fair|good|excellent",
    "issues": []
  }
  ```

- **Pair comparison** (1 call/pair): sends ref + gen clip side by side:
  ```json
  {
    "same_speaker": "yes|no|uncertain",
    "similarity_score": 9,
    "accent_match": true,
    "cadence_match": true,
    "tone_match": true,
    "issues": []
  }
  ```

**Report** (computed locally from above):

```json
{
  "overall_pass": true,
  "avg_wer": 0.0,
  "intelligibility_rate": 1.0,
  "speaker_match_rate": 1.0,
  "naturalness_rate": 1.0,
  "avg_similarity": 9.0
}
```

### Pass criteria

- Intelligibility rate ≥ 80% (WER < 30% per clip)
- Speaker match rate ≥ 80% (Gemini)
- Naturalness rate ≥ 80% (Gemini)
- Avg similarity ≥ 6/10 (Gemini pair comparison)

### Python API

```python
from qwen_tts.check import CheckConfig, run_check

result = run_check(CheckConfig(
    generated="./eval_clips",
    reference="./clips",
    speaker="Speaker Name",
    max_clips=3,
    pairs=3,
    expected_texts={"gen_00.wav": "The future depends on what we do today."},
))
# result["report"]["overall_pass"] → True/False
# result["asr_results"] → per-clip WER + transcription
# result["single_results"] → Gemini per-clip evals
# result["pair_results"] → Gemini pair comparisons
```

---

## Step 7: Iterate

### Common eval failures → fixes

| Issue                     | Fix                                                       |
| ------------------------- | --------------------------------------------------------- |
| High WER / unintelligible | Bad training data quality, or overfitting — reduce epochs |
| Low speaker match         | More/better data, increase epochs or lora-rank            |
| Robotic / not natural     | Reduce epochs (overfitting), remove noisy clips           |
| Wrong accent              | Remove clips with different accents                       |
| Audio glitches            | Check source audio quality, remove bad clips              |
| Low pair similarity       | Increase lora-rank (8→16), add more data                  |

### Full automated loop

```bash
qwen-tts prepare --data ./clips -o ./clips/train.jsonl --model-id mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16
qwen-tts train --name spk --data ./clips/train.jsonl -o ./spk_voice --model-id mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16
mkdir -p eval_clips
qwen-tts generate -m custom-voice --voice-model ./spk_voice --speaker spk --size 0.6B \
  -p "Test sentence one." -o eval_clips/gen_01.wav
qwen-tts generate -m custom-voice --voice-model ./spk_voice --speaker spk --size 0.6B \
  -p "Test sentence two." -o eval_clips/gen_02.wav

# Quick local check first (no API key)
qwen-tts check -g eval_clips --asr-only \
  --expected-text "gen_01.wav=Test sentence one." "gen_02.wav=Test sentence two."

# Full check with Gemini
qwen-tts check -g eval_clips -r clips -S "Speaker Name" \
  --max-clips 2 --pairs 2 \
  --expected-text "gen_01.wav=Test sentence one." "gen_02.wav=Test sentence two."
# If FAIL → adjust data/hyperparams and re-run
```

---

## Data Requirements Summary

| Requirement    | Value                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------- |
| Audio format   | WAV, 24kHz, mono, 16-bit PCM                                                                   |
| Clip duration  | 3-8 seconds (5-8s ideal). **Keep ≤10s** — longer clips cause OOM during gradient accumulation. |
| Total duration | ~8-10 minutes (50-80 clips). ~7,500 total codec frames is the sweet spot.                      |
| Content        | Single speaker, clean speech, minimal noise                                                    |
| Transcript     | Accurate text matching the speech                                                              |

## Troubleshooting

| Problem                              | Solution                                                                                                                                                           |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `No module named 'dotenv'`           | `uv pip install python-dotenv`                                                                                                                                     |
| `No module named 'google.genai'`     | `uv pip install google-genai`                                                                                                                                      |
| `speech_tokenizer encoder not found` | Use the base model for prepare                                                                                                                                     |
| OOM / hang during training           | Reduce `--grad-accum` to 2, trim clips to ≤8s, reduce total to ~50-60 clips. Long clips + high grad-accum holds too many gradients in memory.                      |
| OOM during `split` (ASR)             | Source audio too long (>~40 min). Split into chunks with ffmpeg first, run `qwen-tts split` on each, then merge clips + transcripts into one directory. See below. |
| OOM during generation                | Close other apps, or use `--size 0.6B`                                                                                                                             |
| `incorrect regex pattern` warning    | Harmless — ignore                                                                                                                                                  |
| `model of type qwen3_tts` warning    | Harmless — ignore                                                                                                                                                  |

### Chunking long source audio for `split`

If `qwen-tts split` OOMs on a long file (>~40 min), chunk it with ffmpeg first:

```bash
mkdir -p raw_audio/chunks
ffmpeg -i raw_audio/source_24k.wav -f segment -segment_time 600 -c copy raw_audio/chunks/chunk_%02d.wav

for chunk in raw_audio/chunks/chunk_*.wav; do
  qwen-tts split "$chunk" -o "clips_tmp/$(basename "$chunk" .wav)"
done

# Merge into one directory
mkdir -p clips && idx=0
for dir in clips_tmp/chunk_*/; do
  while IFS='|' read -r f t; do
    new=$(printf "clip_%03d.wav" $idx)
    cp "${dir}${f}" "clips/${new}"
    echo "${new}|${t}" >> clips/transcript.txt
    idx=$((idx + 1))
  done < "${dir}transcript.txt"
done
```

## Available Models

| Key          | Size | HF Repo                                              |
| ------------ | ---- | ---------------------------------------------------- |
| base         | 1.7B | `mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16`        |
| base         | 0.6B | `mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16`        |
| custom-voice | 1.7B | `mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-bf16` |
| custom-voice | 0.6B | `mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-bf16` |
| voice-design | 1.7B | `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` |

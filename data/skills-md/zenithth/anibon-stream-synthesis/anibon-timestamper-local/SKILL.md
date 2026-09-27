---
name: anibon-timestamper-local
description: Use when generating YouTube timestamps and topic summaries for long livestreams locally on a single GPU (such as NVIDIA Tesla P100 16GB) without cloud API costs.
---

# Anibon Timestamper (Local P100 Edition)

## Overview

A fully local, zero-cloud-cost pipeline for generating front-tier quality YouTube timestamps from long livestreams on a single 16GB GPU (NVIDIA Tesla P100). Emulates the cloud multi-agent workflow via Dynamic Recursive Rolling Summary state-machines (`--mode recursive`), group-based batching (`--mode group`), multi-modal context fusion, tag normalization, and a two-pass local summarizer.

## When to Use

```mermaid
flowchart TD
    Start["New Livestream to Timestamp"] --> Q1{"Cloud API Available<br/>or Budget Allowed?"}
    Q1 -->|Yes| Orchestrator["Use anibon-timestamper<br/>(Cloud Flash Multi-Agent)"]
    Q1 -->|No / Zero-Cost| Q2{"Hardware Available?"}
    Q2 -->|Tesla P100 16GB or Local GPU| LocalSkill["Use anibon-timestamper-local<br/>(Recursive State-Machine / P100 Pipeline)"]
    Q2 -->|CPU Only / Insufficient RAM| Fallback["Use pack_timestamps or wait for cloud"]
```

### Apply When:
- Generating timestamps for Anibon Official livestreams or long talk/gaming streams with **zero API expense**.
- Running local LLM inference on a dedicated workstation GPU (e.g. NVIDIA Tesla P100 16GB Pascal).
- Processing VODs where conversational flow dictates topic duration (not arbitrary fixed clock minutes).

### Do NOT Use When:
- Cloud API credits are available and maximum parallel speed (< 2 minutes runtime) is prioritized over zero cost (use `anibon-timestamper`).
- Processing short clips (< 10 minutes) where manual timestamping or simple heuristics suffice.

---

## Single-GPU Architecture (Tesla P100 16GB Envelope)

All operations run on a single machine, constrained strictly within 16GB VRAM (15.2 GB usable under Windows WDDM):

| Stage | Process / Model | Hardware Footprint | Purpose |
| :--- | :--- | :--- | :--- |
| **0. Pre-computation** | Python (yt-dlp, cv2, TF-IDF) | System RAM (0 MB VRAM) | Captions, LiveChat alignment, Storyboard activity, Domain signal detection. |
| **1. Pass 1: Topic Segmentation** | `google/gemma-4-12b-qat` (LM Studio) | ~7.2 GB VRAM + ~1.2 GB KV Cache | Recursive rolling summary state-machine tracking topic continuation and shifts. |
| **2. Pass 2: Summarizer** | `google/gemma-4-12b-qat` (LM Studio) | Same instance (reused) | Clusters stamps into YouTube parts (< 3,500 bytes) with Caveman headers. |
| **3. Ground Truth (Opt)** | `whisper-cli.exe` (Large-v3-Turbo) | ~1.5 GB VRAM (Vulkan) / CPU | Transcribes short audio slices for garbled proper nouns on demand. |

**VRAM Safety Margin:** Peak allocation ~8.5–10.0 GB, leaving **5+ GB headroom** to prevent CUDA OOM or LM Studio model eviction.

---

## Execution Modes

### Mode 1: Recursive Rolling Summary (`--mode recursive`, Default & Recommended)
Pu Boat's discussions follow organic content flow rather than clock boundaries. A topic may last 3 minutes or 25 minutes.
- **`SAME_TOPIC`**: If Chunk $N$ continues the ongoing topic, it merges into the rolling summary without emitting a timestamp.
- **`TOPIC_SHIFT`**: When the topic shifts, it flushes the previous summary, stamps the exact start timestamp, and begins a fresh rolling summary.

### Mode 2: Fixed Window Groups (`--mode group`, Alternative)
Combines 4 chunks (~16–20 min) per group with chronological loop-breakers and collision guards.

---

## Core Pipeline & Quick Reference

### Quick Commands

```powershell
# 1. Download & Chunk (Skip if chunks/chunk_00.txt exists)
python "C:/Users/peter/.agents/skills/anibon-timestamper-local/scripts/prepare_video.py" "https://www.youtube.com/watch?v=<VIDEO_ID>" --workspace "C:/Users/peter/youtube_<VIDEO_ID>_workspace" --format txt --block 300 --overlap 30

# 2. Run All-in-One Local Timestamper (Recursive Mode + Summarizer Pass)
python -X utf8 "C:/Users/peter/.agents/skills/anibon-timestamper-local/scripts/process_chunks_local.py" "C:/Users/peter/youtube_<VIDEO_ID>_workspace" --mode recursive --lang th

# 3. Detached Background Launch (for Cline / agent sessions with 30s timeout)
powershell -ExecutionPolicy Bypass -File "C:/Users/peter/.agents/skills/anibon-timestamper-local/scripts/launch_local.ps1" -Workspace "C:/Users/peter/youtube_<VIDEO_ID>_workspace"
```

---

## Discipline & Anti-Rationalization

### The Iron Rule of Local Processing

```
NEVER TIME-LOCK TOPICS TO ARBITRARY MINUTE BOUNDARIES
```

Livestreams flow organically. Use the Recursive Rolling Summary state-machine to detect true content shifts rather than stamping every $N$ minutes.

### Rationalization Table

| Rationalization | Reality | Counter-Measure |
| :--- | :--- | :--- |
| *"Single chunk is faster to run."* | Produces 35+ micro-stamps that clutter comment sections. | Use `--mode recursive` with rolling summaries. |
| *"I can invent tags like [วิเคราะห์] because it fits the content."* | Front-tier benchmarks reject non-standard tags; breaks comment parsers. | Normalizer automatically remaps `[วิเคราะห์]` → `[Talk]`. |
| *"I'll just summarize the whole 3-hour transcript in 1 prompt."* | Exceeds context and degrades entity recall on 12B models. | Sequential rolling state-machine keeps prompt under 2k tokens. |
| *"Let's write a custom Python script to speed this up."* | Ad-hoc scripts break state tracking, resume logic, and encoding. | Strictly use `process_chunks_local.py` flags. |

### Red Flags — STOP and Reset
- Output file contains 35+ timestamps for a 2-hour stream (micro-stamping symptom).
- Output tags include non-whitelisted words (`[วิเคราะห์]`, `[ชำแหละ]`, `[เปิดตัว]`).
- Sections exceed 3,500 bytes (YouTube comment limit violation).
- Script crashes with `UnicodeEncodeError: 'charmap'` (forgot `-X utf8`).

---

## Common Mistakes & Troubleshooting

1. **LM Studio Model Eviction**:
   - *Symptom*: LM Studio unloads Gemma 4 and reloads another model, causing 60-second stalls.
   - *Fix*: Keep `--model auto`. `resolve_model` automatically latches onto the active in-memory model.

2. **Gemma 4 Thinking Token Trap**:
   - *Symptom*: Output timestamp is blank or truncated.
   - *Cause*: Model used token budget in `reasoning_content`.
   - *Fix*: Built-in system prompt limits thinking to <2 sentences; regex extractor extracts structured JSON directly from content or reasoning.

3. **ASR Phonetic Drift**:
   - *Symptom*: Names like "นครโตะ" appear instead of "Naucrate (นอคราเต้)".
   - *Fix*: `process_chunks_local.py` loads `resources/default_mappings.json` and runs TF-IDF signal detection before prompt generation.

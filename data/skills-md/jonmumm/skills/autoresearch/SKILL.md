---
name: autoresearch
description: >
  Set up and run Karpathy's autoresearch — an autonomous AI research loop that
  trains a small language model overnight. An AI agent modifies train.py, runs
  5-minute experiments, keeps improvements, discards failures, and repeats (~12
  experiments/hour, ~100 overnight). Use when the user says "autoresearch",
  "run autoresearch", "set up autoresearch", or wants to run autonomous ML
  research experiments while AFK.
---

# Autoresearch

Set up and run [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch) —
an autonomous AI research loop where an AI agent iterates on a tiny language model's
training code overnight, running ~100 experiments while you sleep.

## Concept

```
Human writes program.md (the "research org" instructions)
    ↓
AI agent reads program.md
    ↓
Agent modifies train.py (model, optimizer, hyperparameters)
    ↓
Runs 5-minute training on GPU → measures val_bpb
    ↓
If improved → git commit (keep). If not → git revert (discard).
    ↓
Repeat (~12 experiments/hour, ~100 overnight)
```

**Key insight:** You don't touch any Python files. Instead, you program `program.md` —
the Markdown instructions that guide the AI agent. You're programming the research
organization, not running individual experiments.

## Prerequisites

### Hardware

| Platform | Requirement |
|----------|------------|
| **Mac** (recommended for this skill) | Apple Silicon (M1/M2/M3/M4), 16 GB RAM minimum (32 GB+ better) |
| **Linux/Windows** | NVIDIA GPU (RTX 3060+), CUDA toolkit installed |

**Check your Mac chip:** Apple menu → About This Mac → look for "Chip: M1/M2/M3/M4".
Any Mac bought since late 2020 has Apple Silicon.

### Software

| Tool | Purpose | Check |
|------|---------|-------|
| **Git** | Experiment tracking (save points) | `git --version` |
| **uv** | Python + dependency manager | `uv --version` |
| **Claude Code** (or Cursor/Codex) | The AI agent brain | `claude --version` |

## Setup

### Step 1: Install prerequisites

```bash
# Install uv (handles Python + all dependencies automatically)
curl -LsSf https://astral.sh/uv/install.sh | sh

# IMPORTANT: Close and reopen your terminal after installing uv

# Verify
uv --version
git --version
```

### Step 2: Clone the repo

**Mac (Apple Silicon):**
```bash
cd ~/Desktop
git clone https://github.com/miolini/autoresearch-macos.git
cd autoresearch-macos
```

**Linux/Windows (NVIDIA GPU):**
```bash
cd ~/Desktop
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch
```

> **About the Mac fork:** Karpathy himself links to `miolini/autoresearch-macos` from
> his README. The developer (Artem Andreenko) has 167 public projects on GitHub and a
> years-long track record. The fork swaps FlashAttention-3 for PyTorch's built-in SDPA
> and adds Apple Metal/MPS optimizations. The entire codebase is ~630 lines — fully
> auditable in 20 minutes.

### Step 3: Install dependencies and prepare data

```bash
# Install Python + all packages
uv sync

# Download training data + build tokenizer (one-time, ~2 min)
uv run prepare.py

# Run one test training to verify setup (~5 min)
uv run train.py
```

If the test training finishes and shows a `val_bpb` score — you're ready.

### Step 4: Launch the autonomous loop

```bash
# Navigate to the project
cd ~/Desktop/autoresearch-macos  # or autoresearch on Linux

# Launch Claude Code
claude
```

Then type this prompt:

```
Hi have a look at program.md and let's kick off a new experiment! Let's do the setup first.
```

**That's it.** Minimize the window and go to sleep. The agent will:
1. Read `program.md`
2. Modify `train.py` with an experimental change
3. Run a 5-minute training
4. Check `val_bpb` — if improved, git commit; if not, git revert
5. Repeat all night

> **Pro tip:** To make it fully autonomous, tell the agent upfront:
> "Run fully autonomously. Don't ask for confirmation between experiments. Keep going
> until I come back."

## Project Structure

```
autoresearch/
├── prepare.py      ← Constants, data prep, runtime utilities (DO NOT modify)
├── train.py        ← Model + optimizer + training loop (agent modifies this)
├── program.md      ← Agent instructions (human modifies this)
├── pyproject.toml  ← Dependencies
├── results.tsv     ← Experiment log (score, memory, kept/discarded)
└── analysis.ipynb  ← Graphs showing progress over time
```

### The three files that matter

| File | Modified by | Purpose |
|------|------------|---------|
| `prepare.py` | Nobody | Fixed constants, one-time data prep, runtime utilities |
| `train.py` | **AI agent** | GPT model, Muon + AdamW optimizer, training loop. Everything is fair game: architecture, hyperparameters, optimizer, batch size, etc. |
| `program.md` | **Human** | Instructions for the AI agent. This is your leverage point — better instructions → faster research progress. |

## Key Terminology

| Term | Meaning |
|------|---------|
| **val_bpb** | Validation bits per byte — the score measuring model quality. **Lower = better.** Vocab-size-independent so architectural changes are fairly compared. |
| **train.py** | The single Python file containing all training code. The AI agent modifies only this file during experiments. |
| **program.md** | Your instruction file for the AI agent. The only file you (the human) should edit. Think of it as a mission briefing for your tireless lab assistant. |
| **5-minute budget** | Every experiment gets exactly 5 minutes of training time. Makes experiments directly comparable regardless of what the agent changes. ~12 experiments/hour. |

## Design Choices

- **Single file to modify.** The agent only touches `train.py`. Keeps scope manageable and diffs reviewable.
- **Fixed time budget.** Training always runs for exactly 5 minutes, regardless of platform. This makes experiments directly comparable and means autoresearch finds the most optimal model for *your* specific hardware.
- **Self-contained.** No external dependencies beyond PyTorch. No distributed training, no complex configs. One GPU, one file, one metric.

## Tips for Best Results

1. **Start simple.** Get one manual `uv run train.py` working first. If that doesn't work, the autonomous loop won't either.

2. **Your one job is to improve `program.md`.** Add instructions like:
   - "Try small improvements first"
   - "Focus on making val_bpb go down"
   - "Think step by step and explain every change before making it"
   - "If an experiment direction hasn't worked after 3 attempts, try something completely different"

3. **Don't panic when experiments fail.** Most will not improve the score. Out of 100 overnight experiments, maybe 10–20 are keepers. This is normal — the agent automatically keeps wins and discards losses.

4. **Check in periodically at first.** Watch the first 3–4 experiments to make sure the loop is working before going AFK.

5. **More memory helps.** 32 GB+ unified memory on Mac lets the agent explore larger models and more complex architectures.

## Tuning for Smaller Hardware

If running on a Mac with limited memory, Karpathy recommends these adjustments (ask the agent to make them, or edit `train.py`/`prepare.py` yourself):

| Setting | Location | Default | Smaller Hardware |
|---------|----------|---------|-----------------|
| Dataset | `prepare.py` | FineWeb-Edu | Use [TinyStories](https://huggingface.co/datasets/karpathy/tinystories-gpt4-clean) for better results at small scale |
| `vocab_size` | `prepare.py` | 8192 | Try 4096, 2048, 1024, or even 256 (byte-level) |
| `MAX_SEQ_LEN` | `prepare.py` | Large | Lower significantly, even down to 256 |
| `DEVICE_BATCH_SIZE` | `train.py` | Default | Increase slightly as you lower `MAX_SEQ_LEN` |
| `EVAL_TOKENS` | `prepare.py` | Default | Decrease so validation runs faster |
| `DEPTH` | `train.py` | 8 | Lower to 4 for smaller models |
| `WINDOW_PATTERN` | `train.py` | "SSSL" | Use just "L" (alternating banded attention may be inefficient) |
| `TOTAL_BATCH_SIZE` | `train.py` | Default | Lower to `2**14` (~16K) or smaller |

## Checking Results

After a night of experiments:

```bash
# See the git history of successful experiments
git log --oneline

# Check the results log
cat results.tsv

# Open the analysis notebook (optional)
# Use Jupyter or Cursor to view analysis.ipynb
```

You'll find:
- **Git history** — each commit is a successful experiment that improved val_bpb
- **Lower val_bpb** — the model is genuinely smarter (baseline starts around 0.9979)
- **Modified train.py** — architecture tweaks, optimizer changes, hyperparameter adjustments
- **results.tsv** — every experiment with score, memory usage, and keep/discard status

## Alternative Agent Options

| Agent | Cost | Best For |
|-------|------|----------|
| **Claude Code** | $20/mo (Pro) or $100/mo (Max) | Full autopilot — runs entirely in Terminal |
| **Cursor** | Free tier available, $20/mo Pro | Visual learners — AI chat panel + file editor |
| **Codex CLI** | Varies | Alternative to Claude Code |
| **Claude.ai chat** | Free/$20/mo | Manual only — copy-paste results back and forth |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `command not found: uv` | Close terminal, open a new one |
| `command not found: git` | Mac: install Xcode CLI tools. Linux: `sudo apt install git` |
| CUDA / GPU error (Linux/Windows) | Search "install CUDA toolkit [your GPU]" |
| MPS / Metal error (Mac) | Make sure you cloned `miolini/autoresearch-macos`, not the original |
| Out of memory | GPU needs more VRAM. Agent usually adapts automatically. See tuning table above. |
| Claude Code auth error | Requires paid Claude subscription ($20/mo minimum) |
| Test training works but loop doesn't start | Make sure you're in the right folder when launching `claude`. Be explicit in your prompt. |

## References

| Resource | Link |
|----------|------|
| Original repo (NVIDIA) | [karpathy/autoresearch](https://github.com/karpathy/autoresearch) |
| Mac fork (Apple Silicon) | [miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos) |
| MLX fork (Mac) | [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx) |
| Windows fork (RTX) | [jsegov/autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx) |
| Karpathy's announcement | [Tweet](https://x.com/karpathy/status/2029701092347630069) |
| Karpathy's update | [Tweet](https://x.com/karpathy/status/2030371219518931079) |
| TinyStories dataset | [HuggingFace](https://huggingface.co/datasets/karpathy/tinystories-gpt4-clean) |
| uv package manager | [astral.sh/uv](https://astral.sh/uv) |

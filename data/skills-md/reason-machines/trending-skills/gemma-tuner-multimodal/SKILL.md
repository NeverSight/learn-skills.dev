---
name: gemma-tuner-multimodal
description: Fine-tune Gemma 4 and 3n models with audio, images, and text on Apple Silicon using PyTorch and Metal Performance Shaders.
triggers:
  - fine-tune Gemma on Mac
  - multimodal fine-tuning Apple Silicon
  - train Gemma with audio images text
  - LoRA fine-tuning Gemma MPS
  - gemma-tuner-multimodal setup
  - fine-tune Gemma on local data
  - Apple Silicon LLM training
  - Gemma 3n 4 fine-tuning without GPU
---

# Gemma Multimodal Fine-Tuner

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Fine-tune Gemma 4 and Gemma 3n models on text, images, and audio data entirely on Apple Silicon (MPS), with support for streaming large datasets from GCS/BigQuery without filling local storage.

---

## What It Does

- **Text LoRA**: instruction-tuning or completion fine-tuning from local CSV
- **Image + Text LoRA**: captioning and VQA from local CSV
- **Audio + Text LoRA**: the only Apple-Silicon-native path for this modality
- **Cloud streaming**: train on terabytes from GCS/BigQuery without local copy
- **MPS-native**: no NVIDIA GPU required — runs on MacBook Pro/Air/Mac Studio

---

## Installation

### Prerequisites
- macOS 12.3+ with Apple Silicon (arm64)
- Python 3.10+ (native arm64, not Rosetta)
- Hugging Face account with Gemma access

```bash
# Install Python 3.12 if needed
brew install python@3.12

# Create venv
python3.12 -m venv .venv
source .venv/bin/activate

# Verify arm64 (must show arm64, not x86_64)
python -c "import platform; print(platform.machine())"

# Install PyTorch
pip install torch torchaudio

# Clone and install
git clone https://github.com/mattmireles/gemma-tuner-multimodal
cd gemma-tuner-multimodal
pip install -e .

# For Gemma 4 support (separate venv recommended)
pip install -r requirements/requirements-gemma4.txt
```

### Authenticate with Hugging Face
```bash
huggingface-cli login
# Or set environment variable:
export HF_TOKEN=your_token_here
```

---

## CLI Commands

```bash
# Check system is ready
gemma-macos-tuner system-check

# Guided setup wizard (recommended for first run)
gemma-macos-tuner wizard

# Prepare dataset
gemma-macos-tuner prepare <dataset-profile>

# Fine-tune a model
gemma-macos-tuner finetune <profile> --json-logging

# Evaluate a run
gemma-macos-tuner evaluate <profile-or-run>

# Export merged HF/SafeTensors (merges LoRA when adapter_config.json present)
gemma-macos-tuner export <run-dir-or-profile>

# Blacklist bad samples from errors
gemma-macos-tuner blacklist <profile>

# List training runs
gemma-macos-tuner runs list
```

---

## Configuration (`config/config.ini`)

The config is hierarchical INI: defaults → groups → models → datasets → profiles.

```ini
[defaults]
output_dir = output
batch_size = 2
gradient_accumulation_steps = 8
learning_rate = 2e-4
num_train_epochs = 3

[model:gemma-3n-e2b-it]
group = gemma
base_model = google/gemma-3n-E2B-it

[model:gemma-4-e2b-it]
group = gemma
base_model = google/gemma-4-E2B-it

[dataset:my-audio-dataset]
data_dir = data/datasets/my-audio-dataset
audio_column = audio_path
text_column = transcript

[profile:my-audio-profile]
model = gemma-3n-e2b-it
dataset = my-audio-dataset
modality = audio
lora_r = 16
lora_alpha = 32
lora_dropout = 0.05
max_seq_length = 512
```

Use `GEMMA_TUNER_CONFIG` env var to point to config outside repo root:
```bash
export GEMMA_TUNER_CONFIG=/path/to/my/config.ini
```

---

## Modality Configuration

### Text-Only Fine-Tuning

**Instruction tuning** (user/assistant pairs):
```ini
[profile:text-instruction]
model = gemma-3n-e2b-it
dataset = my-text-dataset
modality = text
text_sub_mode = instruction
prompt_column = prompt
text_column = response
max_seq_length = 2048
lora_r = 16
lora_alpha = 32
```

**Completion tuning** (full sequence trained):
```ini
[profile:text-completion]
model = gemma-3n-e2b-it
dataset = my-text-dataset
modality = text
text_sub_mode = completion
text_column = text
max_seq_length = 2048
```

**CSV format** for instruction tuning (`data/datasets/my-text-dataset/train.csv`):
```csv
prompt,response
"What is photosynthesis?","Photosynthesis is the process by which plants..."
"Explain LoRA fine-tuning","LoRA (Low-Rank Adaptation) is a parameter-efficient..."
```

### Image Fine-Tuning

```ini
[profile:image-caption]
model = gemma-3n-e2b-it
dataset = my-image-dataset
modality = image
image_sub_mode = captioning
image_token_budget = 256
prompt_column = prompt
text_column = caption
max_seq_length = 512
```

**CSV format** (`data/datasets/my-image-dataset/train.csv`):
```csv
image_path,prompt,caption
/data/images/img1.jpg,Describe this image,A dog sitting on a green lawn...
/data/images/img2.jpg,What is shown here,A bar chart showing quarterly revenue...
```

### Audio Fine-Tuning

```ini
[profile:audio-asr]
model = gemma-3n-e2b-it
dataset = my-audio-dataset
modality = audio
audio_column = audio_path
text_column = transcript
max_seq_length = 512
lora_r = 16
lora_alpha = 32
lora_dropout = 0.05
```

**CSV format** (`data/datasets/my-audio-dataset/train.csv`):
```csv
audio_path,transcript
/data/audio/recording1.wav,The patient presents with acute respiratory symptoms
/data/audio/recording2.wav,Counsel objects to the characterization of the evidence
```

---

## Supported Models

| Model Key | Hugging Face ID | Notes |
|---|---|---|
| `gemma-3n-e2b-it` | `google/gemma-3n-E2B-it` | Default, ~2B instruct |
| `gemma-3n-e4b-it` | `google/gemma-3n-E4B-it` | ~4B instruct |
| `gemma-4-e2b-it` | `google/gemma-4-E2B-it` | Needs requirements-gemma4.txt |
| `gemma-4-e4b-it` | `google/gemma-4-E4B-it` | Needs requirements-gemma4.txt |
| `gemma-4-e2b` | `google/gemma-4-E2B` | Base, needs Gemma 4 stack |
| `gemma-4-e4b` | `google/gemma-4-E4B` | Base, needs Gemma 4 stack |

Add custom models with a `[model:your-name]` section using `group = gemma`.

---

## Dataset Directory Layout

```
data/
└── datasets/
    └── <dataset-name>/
        ├── train.csv       # required
        ├── validation.csv  # optional
        └── test.csv        # optional
```

---

## Output Layout

```
output/
└── {run-id}-{profile}/
    ├── metadata.json
    ├── metrics.json
    ├── checkpoint-*/
    └── adapter_model/      # LoRA artifacts
```

---

## Python API Examples

### Running Fine-Tuning Programmatically

```python
from gemma_tuner.core.config import load_config
from gemma_tuner.core.ops import run_finetune

# Load config
config = load_config("config/config.ini")

# Run fine-tuning for a profile
run_finetune(profile="my-audio-profile", config=config, json_logging=True)
```

### Using Device Utilities

```python
from gemma_tuner.utils.device import get_device, memory_hint

device = get_device()   # Returns "mps", "cuda", or "cpu"
print(f"Training on: {device}")

hint = memory_hint(model_key="gemma-3n-e2b-it")
print(hint)
```

### Loading and Inspecting Datasets

```python
from gemma_tuner.utils.dataset_utils import load_csv_dataset

train_df, val_df = load_csv_dataset(
    data_dir="data/datasets/my-text-dataset",
    text_column="response",
    prompt_column="prompt"
)
print(f"Train samples: {len(train_df)}, Val samples: {len(val_df)}")
```

### Custom LoRA Config

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-3n-E2B-it",
    torch_dtype="auto",
    device_map="mps"
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

---

## Common Patterns

### Full Workflow: Text Instruction Tuning

```bash
# 1. Prepare your data
mkdir -p data/datasets/my-dataset
cp train.csv data/datasets/my-dataset/
cp validation.csv data/datasets/my-dataset/

# 2. Add profile to config/config.ini
cat >> config/config.ini << 'EOF'
[dataset:my-dataset]
data_dir = data/datasets/my-dataset

[profile:my-text-run]
model = gemma-3n-e2b-it
dataset = my-dataset
modality = text
text_sub_mode = instruction
prompt_column = prompt
text_column = response
max_seq_length = 2048
lora_r = 16
lora_alpha = 32
EOF

# 3. Prepare dataset
gemma-macos-tuner prepare my-dataset

# 4. Fine-tune
gemma-macos-tuner finetune my-text-run --json-logging

# 5. Export merged weights
gemma-macos-tuner export my-text-run
```

### GCS Streaming for Large Datasets

```ini
[dataset:large-audio-gcs]
source = gcs
gcs_bucket = my-bucket
gcs_prefix = audio-training-data/
audio_column = audio_path
text_column = transcript

[profile:large-audio-run]
model = gemma-3n-e4b-it
dataset = large-audio-gcs
modality = audio
lora_r = 32
lora_alpha = 64
```

Set credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
gemma-macos-tuner finetune large-audio-run
```

### Add a Custom Gemma Checkpoint

```ini
[model:my-custom-gemma]
group = gemma
base_model = my-org/my-gemma-checkpoint

[profile:custom-run]
model = my-custom-gemma
dataset = my-dataset
modality = text
text_sub_mode = instruction
```

---

## Troubleshooting

### Wrong architecture (x86_64 instead of arm64)
```bash
python -c "import platform; print(platform.machine())"
# Must be arm64 — if x86_64, reinstall Python natively:
brew install python@3.12
python3.12 -m venv .venv && source .venv/bin/activate
```

### MPS out of memory
- Reduce `batch_size` (try 1)
- Increase `gradient_accumulation_steps` to compensate
- Use a smaller model (`e2b` instead of `e4b`)
- Reduce `max_seq_length`

### Gemma 4 model not loading
```bash
# Gemma 4 requires the updated Transformers stack
pip install -r requirements/requirements-gemma4.txt
# Use a separate venv if you also need Gemma 3n
```

### Config not found outside repo root
```bash
export GEMMA_TUNER_CONFIG=/absolute/path/to/config/config.ini
gemma-macos-tuner finetune my-profile
```

### Hugging Face auth errors
```bash
huggingface-cli login
# Or:
export HF_TOKEN=your_hf_token
# Accept Gemma license at: https://huggingface.co/google/gemma-3n-E2B-it
```

### System check before debugging anything else
```bash
gemma-macos-tuner system-check
```

### Audio tower loaded even for text-only runs
This is a known v1 issue — USM audio tower weights stay in memory even for `modality = text`. See `README/KNOWN_ISSUES.md`. Workaround: use a smaller model variant to stay within RAM budget.

---

## Architecture Reference

| File | Role |
|---|---|
| `gemma_tuner/cli_typer.py` | Main CLI entrypoint (`gemma-macos-tuner`) |
| `gemma_tuner/core/ops.py` | Dispatches prepare/finetune/evaluate/export |
| `gemma_tuner/scripts/finetune.py` | Router: Gemma models → `models/gemma/finetune.py` |
| `gemma_tuner/models/gemma/finetune.py` | Core training loop with LoRA |
| `gemma_tuner/scripts/export.py` | Merges LoRA → HF/SafeTensors tree |
| `gemma_tuner/utils/device.py` | MPS/CUDA/CPU selection and memory hints |
| `gemma_tuner/utils/dataset_utils.py` | CSV loading, blacklist/protection semantics |
| `gemma_tuner/wizard/` | Interactive CLI wizard (questionary + Rich) |
| `config/config.ini` | Hierarchical INI configuration |

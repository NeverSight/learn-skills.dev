---
name: comfyui-lora-training
description: Prepare datasets and configure LoRA training for character consistency. Covers FLUX (AI-Toolkit, SimpleTuner, FluxGym) and SDXL (Kohya_ss) training with step-by-step guidance. Use when training custom character LoRAs.
user-invocable: true
metadata: {"openclaw":{"emoji":"🏋️","os":["darwin","linux","win32"],"requires":{"bins":["python"]},"primaryEnv":"COMFYUI_PATH"}}
---

# ComfyUI LoRA Training

Guide the user through dataset preparation, training configuration, and evaluation for character LoRAs.

## When to Train vs Zero-Shot

| Scenario | Recommendation |
|----------|---------------|
| Need absolute consistency across many images | Train LoRA |
| Building a character series or ongoing project | Train LoRA |
| Quick one-off generation | Use zero-shot (InstantID/PuLID) |
| Limited references (1-5 images) | Use zero-shot |
| Testing concepts | Use zero-shot first, train if committing |

## Training Pipeline

```
1. DATASET PREP
   |-- Collect/generate 15-30 reference images
   |-- Preprocess (crop, resize, diversify styles)
   |-- Caption with trigger word + descriptions
   |
2. CONFIGURE TRAINING
   |-- Select training tool (Kohya/AI-Toolkit/FluxGym)
   |-- Set hyperparameters based on model type
   |-- Configure checkpointing
   |
3. TRAIN
   |-- Monitor loss curve
   |-- Save checkpoints every 250-500 steps
   |
4. EVALUATE
   |-- Test each checkpoint with identical prompts
   |-- Check identity accuracy, flexibility, overfitting
   |-- Select best checkpoint
   |
5. INTEGRATE
   |-- Copy to ComfyUI models/loras/
   |-- Update character profile with trigger word + strength
   |-- Test in full workflow (LoRA + identity method)
```

## Dataset Preparation

### Image Requirements

| Aspect | Minimum | Optimal | Maximum |
|--------|---------|---------|---------|
| Count | 10-15 | 20-30 | 50+ |
| Resolution | 512x512 | 1024x1024 | - |
| Format | PNG/high JPEG | PNG | - |

### Content Diversity Checklist

- [ ] Multiple angles (front, 3/4, profile, back)
- [ ] Various expressions (neutral, smile, serious, laugh, etc.)
- [ ] Different lighting conditions (studio, natural, dramatic)
- [ ] Varied backgrounds (or transparent/solid)
- [ ] Multiple outfits/contexts
- [ ] Some close-ups, some medium shots
- [ ] If from 3D renders: include style variations (see below)

### Preprocessing 3D Renders

**Problem**: Training directly on 3D renders bakes in the "3D" aesthetic.

**Solution**: Generate style variations first:
1. Run each render through img2img with varied style prompts
2. Mix: 60% style variations, 40% original renders
3. This teaches identity, not style

Style prompts for variation:
```
"photorealistic portrait, dslr photo"
"oil painting portrait"
"digital illustration"
"pencil sketch"
"watercolor portrait"
```

### Captioning Rules

**Trigger word**: ALWAYS use a unique token as first word.
- Good: `sage_character`, `ohwx_sage`, `sks_person`
- Bad: `woman`, `redhead`, `character` (too generic)

**Caption structure:**
```
{trigger}, {subject type}, {clothing}, {pose}, {setting}, {lighting}, {style}
```

**DO NOT describe face features** (let the model learn them):
- Bad: "woman with green eyes, freckles, auburn hair, defined cheekbones"
- Good: "sage_character, woman, indoor portrait, wearing blue sweater"

**DO describe everything else**: clothing, pose, background, lighting, expression.

### Folder Structure

```
dataset/{character_name}/{repeats}_{trigger_word}/
  001.png + 001.txt
  002.png + 002.txt
  ...
```

Folder naming: `10_sage_character` = each image repeated 10x per epoch.

## Training Configurations

### FLUX LoRA (AI-Toolkit) - Recommended

```yaml
network:
  type: lora
  linear: 16              # Rank (16-32 for characters)
  linear_alpha: 16         # Alpha = rank for FLUX

train:
  batch_size: 1
  gradient_accumulation_steps: 4
  steps: 1500              # FLUX converges faster
  lr: 4e-4                 # Higher than SDXL
  optimizer: adamw8bit
  dtype: bf16

datasets:
  - resolution: [1024]
    caption_ext: "txt"

sample:
  sample_every: 250
  prompts:
    - "{trigger}, photorealistic portrait"
```

**FLUX training notes:**
- Converges 2-3x faster than SDXL
- 1000-2000 steps usually sufficient
- Watch for overfitting (quality plateaus early)
- 24GB VRAM for standard, 9GB with NF4 quantization (SimpleTuner)

### SDXL LoRA (Kohya_ss) - Proven

```yaml
pretrained_model: "RealVisXL_V5.0.safetensors"
network_dim: 32            # Rank (16-64)
network_alpha: 16          # Usually dim/2
resolution: "1024,1024"
train_batch_size: 1
gradient_accumulation_steps: 4
learning_rate: 0.0001      # 1e-4
lr_scheduler: "cosine_with_restarts"
lr_scheduler_num_cycles: 3
max_train_epochs: 10
optimizer_type: "AdamW8bit"
mixed_precision: "bf16"
enable_bucket: true
min_snr_gamma: 5
```

**Step calculation:**
```
total_steps = (images x repeats x epochs) / batch_size
Target: 1500-3000 steps for SDXL
Example: 20 images x 10 repeats x 5 epochs / 1 = 1000 steps
```

### Low VRAM Training (FluxGym / SimpleTuner)

For 12-16GB VRAM:
```yaml
use_8bit_adam: true
gradient_checkpointing: true
cache_latents_to_disk: true
max_data_loader_n_workers: 0
train_batch_size: 1
gradient_accumulation_steps: 8
quantize_base_model: nf4    # SimpleTuner only
```

## Evaluation Protocol

### Test Each Checkpoint

Use identical prompts across all checkpoints:

```
Prompt 1: "{trigger}, photorealistic portrait, neutral expression"
Prompt 2: "{trigger}, photorealistic portrait, smiling, outdoor"
Prompt 3: "{trigger}, wearing formal suit, standing, office"
Prompt 4: "a person standing in a park"  (WITHOUT trigger - should NOT produce character)
```

### Quality Indicators

**Good training:**
- Character recognizable from trigger word alone
- Responds to different prompts/contexts
- Doesn't always produce same pose/expression
- Prompt 4 does NOT produce the character

**Overfitting signs:**
- Same exact pose/expression regardless of prompt
- Training backgrounds appearing in outputs
- Ignores clothing/setting prompts
- Prompt 4 produces the character (too strong)

### Best Epoch Selection

If using sample_every: 250 with 1500 steps:
- Checkpoint 250: Usually underfit
- Checkpoint 500-750: Often sweet spot for FLUX
- Checkpoint 1000-1500: May be overfitting

Compare visually and select the checkpoint with best identity + prompt flexibility balance.

## Post-Training Integration

1. Copy best checkpoint to `{ComfyUI}/models/loras/`
2. Update character profile:
   ```yaml
   lora:
     trained: true
     model_file: "sage_character_flux.safetensors"
     trigger_word: "sage_character"
     best_strength: 0.8
   ```
3. Test in full workflow: LoRA (0.7-0.9) + PuLID/IP-Adapter (0.5-0.7)
4. Record successful settings in character's `generation_history`

## Combining LoRA with Zero-Shot Methods

Best practice: LoRA as base identity, zero-shot for enhancement.

```
[Load Checkpoint] → [Load LoRA (0.7-0.9)] → [Apply PuLID/IP-Adapter (0.5-0.7)] → [Generate]
```

Lower weights on both prevents conflict while reinforcing identity.

## Troubleshooting

| Issue | Solution |
|-------|---------|
| LoRA not activating | Check trigger word spelling, ensure loaded before KSampler |
| Identity drift at angles | Add more angle variety to dataset, reduce network_dim |
| Overfitting | Reduce epochs, increase dataset, lower network_dim |
| Style contamination | Better caption diversity, don't describe style in captions |
| Poor quality/artifacts | Check training images for compression, reduce LR |

## Reference

- `references/lora-training.md` - Full parameter reference
- `references/models.md` - Training tool download links
- Character profiles in `projects/` for trigger words and reference images

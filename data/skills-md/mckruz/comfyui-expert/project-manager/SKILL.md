---
name: project-manager
description: Manage video production projects including character profiles, project manifests, workflow history, and asset tracking. Use when creating new projects, managing characters, or tracking production state.
user-invocable: true
metadata: {"openclaw":{"emoji":"📋","os":["darwin","linux","win32"]}}
---

# Project Manager

Manages the lifecycle of video production projects. Each project gets a manifest, character profiles, workflow records, and asset tracking.

## Project Structure

```
projects/{project-name}/
  manifest.yaml          # Project metadata, settings, status
  characters/
    {name}/
      profile.yaml       # Character description, reference images, voice profile
      references/         # Source images for this character
      outputs/            # Generated outputs
  workflows/              # Saved ComfyUI workflow JSONs
  assets/                 # External assets (audio, video, images)
  notes.md                # Production notes, what worked/didn't
```

## Commands

### Create New Project

When user wants to start a new project:

1. Ask for project name and brief description
2. Create directory structure under `projects/`
3. Generate `manifest.yaml`:

```yaml
name: "{project-name}"
description: "{description}"
created: "{ISO date}"
updated: "{ISO date}"
status: active  # active | paused | completed | archived

hardware:
  gpu: "RTX 5090"
  vram: 32

defaults:
  checkpoint: ""         # Filled after first successful generation
  upscaler: ""
  cfg: null
  sampler: ""
  scheduler: ""

characters: []           # List of character names
workflows: []            # List of saved workflow files

notes: ""
```

### Create Character Profile

When user describes a character:

1. Create `projects/{project}/characters/{name}/profile.yaml`:

```yaml
name: "{character-name}"
trigger_word: "{unique_trigger}"  # e.g., "sage_character"
created: "{ISO date}"

appearance:
  gender: ""
  age_range: ""
  ethnicity: ""
  hair: ""
  eyes: ""
  skin: ""
  build: ""
  distinguishing_features: []

personality:
  traits: []
  voice_description: ""

reference_images:
  source_type: ""        # 3d_render | photograph | illustration | generated
  count: 0
  path: "references/"

lora:
  trained: false
  model_file: ""
  trigger_word: ""
  best_strength: null

voice:
  cloned: false
  model: ""              # chatterbox | f5-tts | elevenlabs | rvc
  sample_file: ""
  settings: {}

generation_history:
  preferred_method: ""   # instantid | pulid | infiniteyou | kontext | lora
  best_settings:
    cfg: null
    steps: null
    sampler: ""
    ip_adapter_weight: null
    instantid_weight: null
  successful_prompts: []
  failed_approaches: []
```

### Update Project State

After any successful generation or pipeline run:

1. Read current manifest
2. Update `defaults` with settings that worked
3. Update character's `generation_history`
4. Add workflow file to `workflows/` list
5. Update `updated` timestamp

### List Projects

List all projects under `projects/` with status and character count.

### Archive Project

Set status to `archived`, optionally compress outputs.

## Integration

- **comfyui-inventory**: Check what's available before recommending approaches
- **comfyui-character-gen**: Feed character profile as context for generation
- **comfyui-voice-pipeline**: Feed voice profile for synthesis
- **comfyui-lora-training**: Use reference images and profile for dataset prep

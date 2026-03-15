---
name: produce-video
description: End-to-end video production from concept to final assembly. Use when creating videos, producing content, generating video from ideas, or running the full production pipeline.
allowed-tools: Read, Write, mcp__video-generator__*
context: fork
agent: general-purpose
---

# Produce Video

Full production pipeline: concept → structure → execute → assemble.

## Workflow

1. **Structure** - Generate project from concept
2. **Lock** - Optionally lock characters/environments
3. **Execute** - Generate all video clips via Veo
4. **Poll** - Wait for jobs to complete
5. **Assemble** - Combine clips into final video

## Step 1: Generate Structure

Use `generate_structure` tool:

```
Tool: generate_structure
Args: {
  "concept": "A person walks through a forest",
  "duration": 30,
  "arc": "linear-build",
  "style": "cinematic, natural lighting"
}
```

Save the returned project data for the next steps.

## Step 2 (Optional): Lock Characters/Environments

For consistent character appearance across shots:

```
Tool: lock_character
Args: {
  "character": { "id": "person_1", "description": "..." },
  "style": "cinematic"
}
```

## Step 3: Execute Project

```
Tool: execute_project
Args: {
  "project": <project_from_step_1>,
  "style": "cinematic",
  "aspectRatio": "9:16"
}
```

This returns job IDs for each shot.

## Step 4: Poll Jobs

Check job status:

```
Tool: get_job
Args: { "jobId": "<job_id>" }
```

Repeat until `status: "completed"` for all jobs.

## Step 5: Assemble

```
Tool: assemble_video
Args: {
  "project_id": "<project_id>",
  "outputFilename": "my_video.mp4"
}
```

Or with explicit shots:

```
Tool: assemble_video
Args: {
  "shots": [
    { "videoPath": "data/video/clip1.mp4", "energy": 0.5, "tension": 0.3 },
    { "videoPath": "data/video/clip2.mp4", "energy": 0.7, "tension": 0.5 }
  ],
  "outputFilename": "my_video.mp4"
}
```

## Key MCP Tools

| Tool | Purpose |
|------|---------|
| `generate_structure` | Create project from concept |
| `lock_character` | Lock character appearance |
| `lock_environment` | Lock environment appearance |
| `execute_project` | Submit all shots for generation |
| `get_job` | Check job status |
| `list_jobs` | List all jobs |
| `assemble_video` | Combine clips with transitions |
| `validate_project` | Check project for issues |

## Options

| Option | Default | Purpose |
|--------|---------|---------|
| `include_vo` | false | Add voiceover |
| `include_dialogue` | false | Multi-character dialogue |
| `production_style` | none | Preset (stage_play, documentary, etc.) |

See `.claude/rules/core-workflow.md` for full workflow reference.

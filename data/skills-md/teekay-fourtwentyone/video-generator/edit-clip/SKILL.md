---
name: edit-clip
description: Create trimmed or speed-adjusted variations of video clips. Use when editing clips, trimming videos, adjusting speed, or creating clip variations.
allowed-tools: Read, mcp__video-generator__*
context: fork
agent: general-purpose
---

# Edit Clip

Create variations (trim, speed) of generated video clips.

## Quick Start

### Initialize Edit

```
Tool: edit_start
Args: { "job_id": "job_abc123" }
```

### Trim Clip

```
Tool: edit_trim
Args: {
  "job_id": "job_abc123",
  "trim_start": 0.5,
  "trim_end": 7.2
}
```

### Adjust Speed

```
Tool: edit_speed
Args: {
  "job_id": "job_abc123",
  "speed": 1.5
}
```

### Select for Assembly

```
Tool: edit_select
Args: {
  "job_id": "job_abc123",
  "variation_id": "v001"
}
```

## Auto-Analyze & Edit

Analyze clip and auto-create trim variation:

```
Tool: edit_auto_analyze
Args: {
  "job_id": "job_abc123",
  "apply_suggestions": true
}
```

## Available Edit Tools

| Tool | Purpose |
|------|---------|
| `edit_start` | Initialize edit session |
| `edit_trim` | Create trimmed variation |
| `edit_speed` | Create speed-adjusted variation |
| `edit_select` | Select variation for assembly |
| `edit_store_analysis` | Store analysis results |
| `edit_auto_analyze` | Analyze and auto-trim |
| `get_edit_manifest` | Get edit manifest |
| `list_edits` | List all edit sessions |

## Edit Folder Structure

```
data/edits/{job_id}/
├── manifest.json      # Edit state
├── source.mp4         # Original
├── v001_trim.mp4      # Trimmed
└── v002_speed.mp4     # Speed adjusted
```

## Trim Options

| Option | Default | Purpose |
|--------|---------|---------|
| `trim_start` | 0 | Start time in seconds |
| `trim_end` | source duration | End time in seconds |
| `precise` | false | Re-encode for frame-accurate cuts |

When `precise: true`, uses re-encoding (slower but exact). Otherwise uses stream copy (fast but keyframe-aligned).

See `.claude/rules/editing-system.md` for full reference.

---
name: comfyui-research
description: Research latest ComfyUI models, techniques, and community discoveries. Monitors YouTube channels, GitHub repos, and HuggingFace. Updates reference files with timestamped findings and flags stale information. Invoke with /research comfyui or automatically at session start for staleness checks.
user-invocable: true
metadata: {"openclaw":{"emoji":"🔬","os":["darwin","linux","win32"]}}
---

# ComfyUI Research Skill

Keeps the VideoAgent knowledge base current by monitoring sources, extracting knowledge, and flagging stale information.

## Triggers

- **On demand**: User invokes `/research comfyui` or asks to check for updates
- **Session start**: Quick staleness check (read `references/staleness-report.md`)
- **Before workflow generation**: Targeted check if the specific model/technique is >2 months old

## Research Pipeline

### 1. Discovery

Search for new developments across three source types:

**YouTube Channels (technique extraction):**
| Channel | Focus | URL |
|---------|-------|-----|
| Pixaroma | ComfyUI tutorials, GGUF, beginner-friendly | youtube.com/@pixaroma |
| Kijai | Advanced nodes, model implementations | youtube.com/@Kijai |
| Sebastian Kamph | ComfyUI workflows, automation | youtube.com/@sebastiankamph |
| Olivio Sarikas | AI art techniques, ComfyUI | youtube.com/@OlivioSarikas |
| Matt Wolfe | AI tool roundups | youtube.com/@maboroshi |
| Nerdy Rodent | Stable Diffusion deep dives | youtube.com/@NerdyRodent |

**GitHub Repositories (node/model updates):**
| Repository | What to Check |
|-----------|---------------|
| comfyanonymous/ComfyUI | Releases, breaking changes |
| Kosinkadink/ComfyUI-AnimateDiff-Evolved | New motion modules |
| cubiq/ComfyUI_IPAdapter_plus | Maintenance status, forks |
| ltdrdata/ComfyUI-Impact-Pack | FaceDetailer updates |
| Wan-AI/Wan2.1-Preview | New model versions |
| hzwer/Practical-RIFE | Interpolation updates |
| resemble-ai/chatterbox | Voice model updates |
| SWivid/F5-TTS | TTS updates |

**HuggingFace (model releases):**
- Trending models: `huggingface.co/models?sort=trending`
- Filter: diffusers, video, audio, text-to-image
- Watch for: New FLUX variants, Wan updates, identity models, voice models

### 2. Extraction

For each discovery, extract structured knowledge:

**From YouTube videos:**
Use `youtube-video-analyst` or `youtube-chapter-clipper` skills to:
1. Get transcript
2. Identify new models mentioned (name, source, requirements)
3. Identify new techniques (workflow changes, parameter discoveries)
4. Identify new nodes (package name, what it does)
5. Note any benchmark results or comparisons

**From GitHub releases:**
1. Check release notes for breaking changes
2. Identify new features or supported models
3. Note version requirements
4. Check if deprecated features affect our workflows

**From HuggingFace:**
1. Model card: architecture, training data, requirements
2. VRAM requirements and quantization options
3. ComfyUI compatibility (is there a node?)
4. Quality comparison vs current recommendations

### 3. Integration

Update reference files with timestamped entries:

```markdown
<!-- Updated: 2026-02-06 | Source: Pixaroma Ep 45 -->
### New Model: XYZ
- Download: {url}
- VRAM: {requirement}
- Notes: {key findings}
```

**Which file to update:**
| Finding Type | Update File |
|-------------|-------------|
| New model | `references/models.md` |
| New workflow technique | `references/workflows.md` |
| LoRA training discovery | `references/lora-training.md` |
| Voice tool update | `references/voice-synthesis.md` |
| New prompt technique | `references/prompt-templates.md` |
| Bug workaround | `references/troubleshooting.md` |
| Model landscape shift | `foundation/model-landscape.md` |

### 4. Staleness Audit

Scan all reference files for `<!-- Updated: -->` timestamps:

**Thresholds:**
| Category | Max Age | Action |
|----------|---------|--------|
| Models | 3 months | Flag: "Model recommendations may be outdated" |
| Nodes | 2 months | Flag: "Custom node versions may have updates" |
| Techniques | 6 months | Flag: "Techniques may have been superseded" |
| Voice tools | 3 months | Flag: "Voice synthesis landscape may have changed" |

**Generate report**: Update `references/staleness-report.md` with current status.

## Research State

Maintained in `skills/comfyui-research/state/`:

```
state/
  last-research-run.json    # When, what was checked, what was found
  watch-list.yaml           # Sources to monitor (see references/)
```

### last-research-run.json
```json
{
  "last_run": "2026-02-06T12:00:00Z",
  "sources_checked": 15,
  "findings": 3,
  "updates_made": [
    {"file": "models.md", "entry": "Added ModelX", "source": "HuggingFace"},
    {"file": "workflows.md", "entry": "Updated Wan settings", "source": "Pixaroma Ep 50"}
  ],
  "stale_entries": 0
}
```

## Quick Staleness Check (Session Start)

Fast check without full research:

1. Read `references/staleness-report.md`
2. If `last_run` is >2 weeks ago:
   - Notify: "Research data is {N} days old. Run `/research comfyui` for updates."
3. If any entries are beyond their threshold:
   - Notify: "Stale items found: {list}. These may have newer alternatives."

## Full Research Run

When user triggers `/research comfyui`:

1. **Check all YouTube channels** for recent uploads (last 30 days)
2. **Check all GitHub repos** for new releases
3. **Check HuggingFace trending** for relevant models
4. **Extract findings** using youtube-video-analyst
5. **Update reference files** with timestamped entries
6. **Run staleness audit** on all references
7. **Update staleness report**
8. **Summarize** findings for user

## Targeted Research

When asked about a specific topic:

1. Search YouTube for recent videos on the topic
2. Search HuggingFace for related models
3. Check GitHub for related node packages
4. Synthesize findings
5. Update relevant reference files if significant discoveries

## Integration with Other Skills

| Skill | How Research Helps |
|-------|-------------------|
| `comfyui-workflow-builder` | Ensures recommended models/nodes are current |
| `comfyui-character-gen` | Updates identity method recommendations |
| `comfyui-video-pipeline` | Flags new video models (Wan updates, new engines) |
| `comfyui-voice-pipeline` | Tracks voice synthesis tool releases |
| `comfyui-troubleshooter` | Adds community-discovered workarounds |

## Reference

- `references/staleness-report.md` - Current freshness status
- `references/evolution.md` - Update protocol and changelog
- `skills/comfyui-research/references/watch-list.yaml` - Monitored sources

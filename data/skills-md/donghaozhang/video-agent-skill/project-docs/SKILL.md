---
name: project-docs
description: AI Content Pipeline documentation and architecture reference. Use when understanding codebase structure, AI models, CLI commands, YAML pipelines, provider APIs, error codes, or finding implementation details.
user-invocable: false
---

# AI Content Pipeline — Documentation Index

73 AI models across 12 categories. Click-based CLI (`aicp`). Central model registry. YAML pipelines with parallel execution.

## Key Facts

- **Package**: `video-ai-studio` on PyPI, commands `aicp` / `ai-content-pipeline`
- **Version**: 1.0.24, Python 3.10+
- **Registry**: `packages/core/ai_content_pipeline/ai_content_pipeline/registry.py` + `registry_data.py`
- **CLI**: Click framework in `cli/click_app.py`, commands in `cli/commands/` (6 modules, 19 commands + vimax subgroup)
- **Providers**: FAL AI (primary, 30+ models), Google (Gemini/Veo), ElevenLabs (TTS), OpenRouter (prompts), Replicate
- **API keys**: `FAL_KEY`, `GEMINI_API_KEY`, `ELEVENLABS_API_KEY`, `OPENROUTER_API_KEY` in `.env`

## Documentation Files

Load the specific file when Claude needs deeper information on that topic.

### Models & Providers

| File | Load When |
|------|-----------|
| [models.md](../../../docs/reference/models.md) | Selecting models, checking pricing, comparing options across 12 categories |
| [provider-comparison.md](../../../docs/reference/provider-comparison.md) | Choosing between FAL AI, Google, ElevenLabs, OpenRouter, Replicate |

### CLI & API

| File | Load When |
|------|-----------|
| [cli-commands.md](../../../docs/reference/cli-commands.md) | CLI usage, command flags, global options (--json, --quiet, --stream, --input) |
| [python-api.md](../../../docs/api/python-api.md) | Python API: AIPipelineManager methods, data classes, error handling |
| [aicp-vimax-commands.md](../../../docs/aicp-vimax-commands.md) | ViMax subgroup: novel2movie, idea2video, script2video pipelines |

### Architecture & Code

| File | Load When |
|------|-----------|
| [architecture.md](../../../docs/reference/architecture.md) | System design, data flow diagrams, component responsibilities |
| [package-structure.md](../../../docs/reference/package-structure.md) | File locations, import paths, module dependencies |

### Pipelines

| File | Load When |
|------|-----------|
| [yaml-pipelines.md](../../../docs/guides/pipelines/yaml-pipelines.md) | YAML config syntax, 10 step types, variable interpolation, dependencies |
| [parallel-execution.md](../../../docs/guides/pipelines/parallel-execution.md) | Parallel groups, performance optimization, 2-3x speedup patterns |

### Content Creation

| File | Load When |
|------|-----------|
| [prompting.md](../../../docs/guides/content-creation/prompting.md) | Writing effective prompts, templates, model-specific tips |
| [video-tips.md](../../../docs/guides/content-creation/video-tips.md) | Image-to-video vs text-to-video, motion prompts, model selection |
| [video-analysis.md](../../../docs/guides/content-creation/video-analysis.md) | AI video analysis with Gemini, timeline/describe/transcribe modes |

### Optimization

| File | Load When |
|------|-----------|
| [cost-management.md](../../../docs/guides/optimization/cost-management.md) | Pricing tables, budget strategies, cost estimation CLI/API |
| [performance.md](../../../docs/guides/optimization/performance.md) | Speed benchmarks, batching, caching, network optimization |
| [best-practices.md](../../../docs/guides/optimization/best-practices.md) | Project organization, pipeline design patterns, QA workflows |

### Troubleshooting

| File | Load When |
|------|-----------|
| [error-codes.md](../../../docs/reference/error-codes.md) | Error codes AUTH/CFG/MDL/PIP/NET/FILE/RATE/COST/VAL with solutions |
| [troubleshooting.md](../../../docs/guides/support/troubleshooting.md) | Diagnostic steps, common issues, installation/API/network problems |
| [faq.md](../../../docs/guides/support/faq.md) | Frequently asked questions across 9 categories |

### Development

| File | Load When |
|------|-----------|
| [testing.md](../../../docs/guides/support/testing.md) | Test strategies, mocks, fixtures, CI/CD, running pytest |
| [security.md](../../../docs/guides/support/security.md) | API key security, input validation, production deployment |
| [contributing.md](../../../docs/guides/contributing/contributing.md) | Development workflow, coding standards, adding models/providers |
| [migration.md](../../../docs/guides/contributing/migration.md) | Version upgrades, breaking changes, rollback instructions |

### Setup & Learning

| File | Load When |
|------|-----------|
| [setup.md](../../../docs/guides/getting-started/setup.md) | Installation (PyPI/source), venv, API keys, first pipeline |
| [learning-path.md](../../../docs/guides/getting-started/learning-path.md) | Structured learning tracks: Quick Start, Comprehensive, Developer |

### Examples

| File | Load When |
|------|-----------|
| [basic-examples.md](../../../docs/examples/basic-examples.md) | Simple image/video generation, CLI examples |
| [advanced-pipelines.md](../../../docs/examples/advanced-pipelines.md) | Multi-stage production, A/B testing, batch processing |
| [use-cases.md](../../../docs/examples/use-cases.md) | Marketing, education, enterprise, gaming applications |
| [integrations.md](../../../docs/examples/integrations.md) | Flask, FastAPI, Celery, webhook patterns |

## Model Categories Quick Reference

| Category | Count | Key Models | Cost Range |
|----------|-------|------------|------------|
| Text-to-Image | 8 | `flux_dev`, `flux_schnell`, `imagen4`, `nano_banana_pro` | $0.001-0.08 |
| Image-to-Image | 8 | `photon`, `kontext`, `clarity`, `seededit` | $0.015-0.05 |
| Text-to-Video | 10 | `veo3`, `kling_3_pro`, `sora_2`, `hailuo_pro` | $0.08-6.00 |
| Image-to-Video | 15 | `veo_3_1_fast`, `kling_3_pro_i2v`, `sora_2_i2v` | $0.08-3.60 |
| Video-to-Video | 4 | `kling_o3_pro_edit`, `kling_o3_standard_edit` | $0.25-0.34/s |
| Avatar | 10 | `omnihuman_v1_5`, `fabric_1_0`, `multitalk` | $0.06-0.25/s |
| Image Understanding | 7 | `gemini_describe`, `gemini_detailed`, `gemini_qa` | $0.001-0.002 |
| Prompt Generation | 5 | `openrouter_video_prompt` + style variants | $0.002 |
| Text-to-Speech | 3 | `elevenlabs`, `elevenlabs_turbo`, `elevenlabs_v3` | $0.03-0.08 |
| Speech-to-Text | 1 | `scribe_v2` | $0.008/min |
| Add Audio | 1 | `thinksound` | $0.001/s |
| Upscale Video | 1 | `topaz` | ~$1.50/video |

## CLI Commands Quick Reference

```bash
# Core generation
aicp generate-image --text "prompt" --model flux_dev
aicp create-video --text "prompt" --video-model kling_3_pro
aicp run-chain --config pipeline.yaml [--parallel] [--stream] [--dry-run]

# Media operations
aicp generate-avatar --image-url URL --audio-url URL --model omnihuman_v1_5
aicp analyze-video -i video.mp4 [-t timeline|describe|transcribe]
aicp transcribe --input audio.mp3 [--srt] [--raw-json]
aicp transfer-motion --image-url URL --video-url URL
aicp upscale-image --image photo.png --upscale 2
aicp generate-grid --text "prompt" --layout 2x2

# Discovery
aicp list-models [--category X] [--provider X] [--json]
aicp list-avatar-models | list-video-models | list-motion-models | list-speech-models

# Project
aicp setup | init-project | organize-project | structure-info | create-examples

# ViMax (novel-to-video)
aicp vimax idea2video --idea "concept"
aicp vimax novel2movie --novel novel.txt [--storyboard-only]
aicp vimax script2video --script story.txt
```

## Architecture Summary

```
CLI (Click) → Pipeline Manager → Providers → External APIs
                    ↓                            ↑
              Config (YAML)              FAL / Google / ElevenLabs / OpenRouter
                    ↓
              Executor → Parallel Engine → Results → Output Files
```

- **Central Registry**: `registry.py` defines `ModelDefinition` + `ModelRegistry`, `registry_data.py` registers all 73 models
- **Auto-Discovery**: Generator classes use `MODEL_KEY` class attributes
- **CLI**: Root Click group in `cli/click_app.py`, commands auto-registered at import time
- **Pipeline**: `manager.py` orchestrates, `executor.py` runs steps, `parallel.py` handles concurrency

## Testing Quick Reference

```bash
python -m pytest tests/ -v                    # Full suite (~844 tests)
python -m pytest tests/test_registry.py -v    # Registry tests
python -m pytest tests/test_click_app.py -v   # CLI tests
python scripts/validate_registry.py           # Registry validation
```

---
name: remotion-video
description: Build PMM videos from initiative briefs using Remotion. Use for /pmm-video workflows.
---

# Remotion Video Skill

Procedural guidance for creating initiative-specific PMM videos that are outcome-focused and easy to iterate.

## When to Use

- Running `/pmm-video [initiative]`
- Translating PRD + brief content into a short launch or sales-enablement video

## Inputs

- Initiative name
- PMM brief at `pm-workspace-docs/initiatives/active/[name]/pmm-video-brief.md`
- Intake decisions: include/exclude items, tone, duration, CTA, asset constraints

If the brief is missing, create it from `pm-workspace-docs/initiatives/_template/pmm-video-brief.md` and mark assumptions.

## Workflow

1. Validate outcome chain, persona, evidence, and CTA.
2. Write or update JSON brief: `remotion-pmm/briefs/[initiative].json`.
3. Create/update composition in `remotion-pmm/src/`.
4. Ensure duration and scene order match brief intent.
5. Provide preview and render instructions.
6. Log output metadata.

## Quality Gates

- Duration target: 30-90 seconds unless explicitly overridden
- Avoid generic "AI summary" framing
- Claims must be evidence-backed or labeled as assumption
- Copy must remain persona-specific and action-oriented

## Output Locations

- Composition source: `remotion-pmm/src/`
- Render output: `remotion-pmm/out/`
- Run log: `pm-workspace-docs/status/videos/README.md`


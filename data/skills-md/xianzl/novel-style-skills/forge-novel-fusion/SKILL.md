---
name: forge-novel-fusion
description: Fuse multiple distilled novel style profiles into one curated fiction style profile by taking selected strengths from each author style and rejecting weak or AI-prone patterns. Use when the user asks to blend, merge, fuse, combine, synthesize, or take the best parts of multiple novel author styles.
---

# Forge Novel Fusion

You are a fiction style fusion editor. Your job is to combine multiple already-distilled `style.json` profiles into one curated style profile that can be used by `use-novel-style`.

Do not average raw novels together. Fusion works best after each source author has been separately distilled with `forge-novel-style`.

## Core Idea

Fuse by layer, not by author name:

- one source may provide narrative voice
- another may provide dialogue
- another may provide emotion handling
- weak habits from every source go into anti-patterns

The output is a new, coherent style, not an imitation pile-up.

## Entry Steps

1. Get the fusion name, for example `/forge-novel-fusion cold-dialogue-xianxia`.
2. Get source style names or paths:
   - `novel_styles/{name}/style.json`
   - direct `style.json` paths
3. If a source style does not exist, tell the user to run `/forge-novel-style {name}` first.
4. Ask what each source is best at if the user has opinions. If not, infer from the profiles.

## Fusion Workflow

### Phase 1: Compare Source Profiles

Load each `style.json` and compare:

- `L1_narrative_voice`
- `L2_sentence_syntax`
- `L3_diction_texture`
- `L4_scene_rhythm`
- `L5_dialogue_style`
- `L6_emotion_handling`
- `L7_anti_ai_patterns`

Use `prompts/fusion_analyzer.md`.

### Phase 2: Choose A Strategy

Use one of these strategies:

- **dominant-spine**: one source provides the main body; others graft specific strengths.
- **layer-pick**: each layer has an explicit source.
- **weighted-blend**: a layer blends two sources, but with a written reason.
- **purge-and-refine**: focus on removing both sources' weak habits and AI-prone habits.

Default recommendation: dominant-spine + layer-pick.

Represent the strategy in `meta.fusion_strategy`.

### Phase 3: Build The Fusion Profile

Write:

- `novel_styles/{fusion_name}/style.json`
- `novel_styles/{fusion_name}/style.md`

The JSON must still follow `references/novel_style_schema.md` so it can be used by `use-novel-style` and `eval-novel-style`.

Recommended tool flow:

```bash
python forge-novel-fusion/scripts/novel_style_fusion.py --out novel_styles/{fusion_name}/style.json novel_styles/A/style.json novel_styles/B/style.json
python forge-novel-fusion/scripts/novel_style_validator.py novel_styles/{fusion_name}/style.json
```

If this skill has been installed as a standalone folder, run the same commands from inside the skill folder with `scripts/...`.

### Phase 4: Coherence Pass

After building, check contradictions:

- ornate diction with ultra-minimal sentence rules
- slow interior rhythm with high-action scene rules
- indirect emotion with dialogue that states everything
- multiple incompatible narrative distances

Resolve contradictions by choosing a dominant rule and putting the rejected habit into `L7_anti_ai_patterns` or `L0_style_boundary.avoid`.

### Phase 5: User Calibration

Show the user:

- source contribution map
- what was kept
- what was rejected
- expected writing feel

Ask: "这个融合方向像不像你要的精华组合？哪里该偏 A，哪里该偏 B？"

Append corrections to `L9_corrections` and update the profile.

## Output Contract

When finished, report:

- fusion profile path
- source styles used
- contribution map
- validation status
- next command: `/use-novel-style {fusion_name}`


---
name: director-skills
description: "Master router for a modular AI filmmaking skill suite. Use for story development, screenplay scenes, shot lists, visual bibles, cinematic image/video prompts, continuity, prompt diagnostics, and model-specific exports when the agent should choose and orchestrate the right director-skills sub-workflows."
---

# director-skills

Use this as the master conductor for the `director-skills` suite. It is intentionally a router, not a replacement for the specialized skills under `skills/`.

The suite can operate in two modes:

- **Native modular mode**: the host agent registers every folder under `skills/` as its own skill.
- **Single uploaded skill mode**: the host agent loads this root `SKILL.md`, then routes internally to the relevant sub-skill files.

## Prime Directive

Do not treat the README as the full operating procedure. Use it only for orientation. For real work, select the relevant sub-skill, read that skill's `SKILL.md`, and load supporting files only as needed.

## When To Use

Use this master skill when:

- The user asks for help with AI filmmaking, cinematic storytelling, image prompting, video prompting, or prompt packaging.
- The user uploads or links the whole `director-skills` repository and says to learn, use, import, or follow it.
- The task spans multiple production stages, such as idea to screenplay to shot list to prompts.
- The user asks which director-skills workflow applies.
- The agent environment supports only one uploaded skill or knowledge bundle.
- The request is broad enough that routing is needed before execution.

## When Not To Use

Do not use this skill for:

- Tasks unrelated to filmmaking, story, cinematic prompting, continuity, visual development, or model-specific prompt export.
- Live model capability claims that require current official documentation unless the user provides sources or the agent can verify them.
- Requests to bypass safety systems, imitate living artists in a deceptive way, expose private files, or reproduce copyrighted source guides.

If a host system has already activated a specific sub-skill that fully covers the request, follow that sub-skill directly. If model naming, continuity, or failure diagnosis appears, add the appropriate supporting sub-skill.

## Core Method

Every task moves through three layers:

1. **Creative intent**: story, theme, character, emotion, scene purpose, dramatic action, genre, tone, and audience experience.
2. **Cinematic execution**: shot type, framing, angle, camera movement, lens, lighting, blocking, production design, texture, realism, and visual continuity.
3. **Model adaptation**: prompt structure, syntax, length, parameters, negative support, references, aspect ratio, duration, resolution, seeds, and known model failure modes.

Do not assume one prompt format works across all image and video models.

## Routing Protocol

1. Classify the user's task by production stage and requested output.
2. Choose one primary sub-skill and zero to three supporting sub-skills.
3. Read the primary `skills/<skill-name>/SKILL.md`.
4. Read supporting sub-skill `SKILL.md` files only when their decision logic is needed.
5. Load references, templates, checklists, examples, or tests only when the selected sub-skill asks for them or the task requires the specific artifact.
6. Produce the requested output and include the quality checks from the active sub-skill.
7. If the task crosses stages, hand off cleanly by naming the next recommended sub-skill and preserving continuity anchors.

## Sub-Skill Router

| User intent | Primary sub-skill | Add these when relevant |
|---|---|---|
| Raw idea, premise, logline, treatment, outline, short-story plan | `short-film-development` | `style-cinematography-director`, `character-location-prop-bible` |
| Scene writing, dialogue, beats, pacing, Fountain, visual action | `screenplay-and-scene-writing` | `short-film-development`, `character-location-prop-bible` |
| Script to shot list, storyboard plan, camera plan, scene breakdown, asset list | `shotlist-and-visual-breakdown` | `style-cinematography-director`, `character-location-prop-bible` |
| Character sheet, location reference, prop prompt, poster, keyframe, cinematic still | `cinematic-image-prompting` | `character-location-prop-bible`, `style-cinematography-director`, `model-adaptation` |
| Text-to-video, image-to-video, motion prompt, time blocks, camera movement, audio cues | `cinematic-video-prompting` | `shotlist-and-visual-breakdown`, `model-adaptation`, `prompt-iteration-and-diagnostics` |
| Continuity bible, identity anchors, wardrobe, prop state, location rules, style bible | `character-location-prop-bible` | `cinematic-image-prompting`, `shotlist-and-visual-breakdown` |
| Genre look, cinematography, lensing, lighting, realism, visual language | `style-cinematography-director` | `shotlist-and-visual-breakdown`, `cinematic-image-prompting`, `cinematic-video-prompting` |
| Failed output, drift, bad motion, wrong face, weak realism, revision loop | `prompt-iteration-and-diagnostics` | Relevant image/video skill, `model-adaptation`, `character-location-prop-bible` |
| Named model, prompt conversion, multi-tool export, settings, capability mismatch | `model-adaptation` | Relevant image/video/story skill |

## Model Trigger Rule

If the user names an image or video model, always consider `model-adaptation`.

Examples include Midjourney, DALL-E, GPT-image, Stable Diffusion, FLUX, Ideogram, Grok/Aurora, Runway, Pika, Luma, Kling, Veo, Sora, Hailuo, Seedance, Gemini image, Nano Banana, Le Chat, or any newly named model. If the suite has no clear profile for the tool, mark capabilities as `unknown` instead of guessing.

## Multi-Skill Pipelines

For end-to-end work, use this order unless the user asks for a narrower artifact:

```text
short-film-development
-> screenplay-and-scene-writing
-> character-location-prop-bible
-> style-cinematography-director
-> shotlist-and-visual-breakdown
-> cinematic-image-prompting
-> cinematic-video-prompting
-> model-adaptation
-> prompt-iteration-and-diagnostics
```

Keep the output moving. If the user asks for an artifact, produce the artifact; do not stop at a plan unless they asked for a plan.

## Output Discipline

Before finalizing, verify:

- The selected sub-skill matches the user's actual requested output.
- Creative intent, cinematic execution, and model adaptation are not collapsed into one vague prompt.
- Continuity anchors are preserved when characters, locations, costumes, props, or style recur.
- Model-specific claims come from the model-adaptation references, user-provided docs, or are marked `unknown`.
- The output is immediately usable: a scene, list, bible entry, prompt, export package, diagnosis, or next-step handoff.

## Supporting Files

- For full user-facing orientation, read `README.md`.
- For the public-safe research basis, read `RESEARCH_PROVENANCE.md`.
- For complete file inventory, read `MANIFEST.md`.
- For operational work, route into `skills/<skill-name>/SKILL.md` and that skill's own folders.


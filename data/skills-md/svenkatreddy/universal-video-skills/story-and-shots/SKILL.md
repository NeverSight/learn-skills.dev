---
name: story-and-shots
description: "Plan AI video like a production: beats, shot lists, storyboards, review gates, and a fast-track for simple jobs. Use when a video needs more than one shot, or when generations keep drifting off-story."
---

# Story and Shots

A single good prompt makes a good clip. A good video needs something else:
structure. AI generators make shots; they don't make sequences. The sequence
is your job, and it gets planned before anyone touches a prompt.

## The workflow

1. **Beat it out.** Break the story into beats: one line each, each a change
   in the story (`references/beats-and-shot-lists.md`). If you can't list the
   beats, you don't have a story yet.
2. **Shot-list every beat.** One beat is usually one to three shots. Each shot
   gets a shot-brief (`../video-prompt-craft/`). No shot exists without a
   brief; no brief exists without a beat.
3. **Board it (for anything complex).** Sketch the sequence visually
   (`references/storyboard.md`). Storyboards catch screen-direction flips and
   pacing problems that text hides.
4. **Gate it.** Run the quality gates (`references/quality-gates.md`): style
   proof first, asset lock before generation, beat cards that each carry one
   clear visual change. Max two revision rounds per gate, then move on.
5. **Fast-track the simple stuff.** One product shot, one establishing clip?
   Skip the ceremony (`quality-gates.md` has the short path). Process should
   scale down, not just up.

## Rules that don't bend

- **Story first, prompts second.** A shot list written before any generation
  beats ten brilliant prompts generated in random order.
- **Every shot earns its place.** If removing a shot changes nothing, remove
  it. AI video tempts you to keep generating; editing is the skill.
- **Plan the joins.** Shots don't just sit next to each other. They cut.
  Note the transition or match cut per join in the shot list, or the assembly
  stage inherits a mess.
- **Budget the seconds.** Total runtime divided by shot count is your
  per-shot budget. A 60-second video at 8 seconds a clip is eight shots max.
  Plan eight, not fifteen.
- **Lock assets before generating.** Characters, products, key props get
  registered (`../character-consistency/`) before the first generation, not
  after the third reshoot.

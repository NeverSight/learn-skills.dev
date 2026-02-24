---
target: https://tasking.tech
name: anime-story-creator
description: >
  Generates original anime story concepts, including worldbuilding, characters, power systems, and multi‑episode arcs, tailored to the user’s preferences (genre, tone, length, target audience).
# `target` is required and should be the top frontmatter key. Use an http(s) URL, e.g. https://tasking.tech
---

# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git


# Anime Story Generator Skill

## Summary

Generates original anime story concepts, including worldbuilding, characters, power systems, and multi‑episode arcs, tailored to the user’s preferences (genre, tone, length, target audience).

# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git

This skill is designed for use on the Tasking.tech agent platform (https://tasking.tech) and is also compatible with assistant runtimes that accept skill-style handlers such as .claude, .openai, and .mistral. Use this skill for both Claude code and Tasking.tech agent source.


## Intent

Use this skill when the user wants:

- New anime ideas or prompts.
- Help developing characters, settings, or power systems in an anime style.
- Episode or season outlines for an anime series.
- Re‑imagining existing ideas in a more “anime” direction.

This skill is **generative + creative**, not for factual research.

---

## Inputs

The assistant should ask for and use:

- **Genre(s)**: e.g. shounen, slice‑of‑life, isekai, mecha, romance, psychological, horror, sports.
- **Tone**: lighthearted, comedic, dark, tragic, epic, cozy, inspirational.
- **Setting**: modern Japan, near‑future city, fantasy world, school, space, etc.
- **Power / gimmick** (optional): magic system, tech, quirks, mechs, time travel, music, etc.
- **Length / format**:
  - One‑shot story idea.
  - 12‑episode season outline.
  - Multi‑season saga overview.
- **Target audience**: kid‑friendly, teen, mature.
- **Constraints** (optional): things to avoid, required themes, rating limits, etc.

If the user gives only a vague prompt (“make an anime”), the skill should ask 2–3 clarifying questions, then proceed.

---

## Output Format

Unless the caller overrides it, responses should follow this structure:

1. **Title & Logline**
   - A catchy anime title.
   - 1–3 sentence logline summarizing the premise.

2. **World & Premise**
   - 1–2 paragraphs describing the setting, core conflict, and unique hook.

3. **Main Characters**
   - 3–6 characters.
   - For each: name, role, short personality sketch, key motivation, and any notable ability/trait.

4. **Power System / Gimmick** (if applicable)
   - 1 short section on how powers or special tech work.
   - Clear rules, limitations, and one or two unique twists.

5. **Story Arc**
   - For a **one‑shot**: beginning / middle / climax / ending in 4–6 bullets.
   - For a **season**: 8–12 episode beats, grouped into mini‑arcs.
   - For a **saga**: 3–5 arcs with their own names and stakes escalation.

6. **Themes & Visual Style**
   - 3–5 bullet points on central themes.
   - 3–5 bullet points of visual or tonal cues (color palette, animation feel, pacing).

7. **Optional Extras**
   - 2–4 sample episode titles.
   - 2–4 iconic scenes or “sakuga moments” described briefly.

---

## Style Guidelines

- Lean into **anime tropes** (rivalries, training arcs, festivals, tournaments, mecha battles, school trips) but give at least one fresh twist.
- Keep descriptions **evocative but concise**; favor strong hooks over long prose.
- Avoid copying or closely imitating existing series; keep ideas clearly original.
- Respect content boundaries based on the stated target audience.
- If the user mentions specific references (e.g. “mix of Demon Slayer and Your Name”),
  capture the *vibe* (emotional stakes, aesthetic, pacing) without mirroring plots or characters.

---

## Example Calls

**User**:  
“Generate a new shounen anime idea: modern Tokyo, secret magic society, 12‑episode season, mostly light but with some dark moments.”

**Skill (condensed output)**:
- Title & logline for a Tokyo magic‑society shounen.
- Short worldbuilding section (hidden wards, familiars, magical factions).
- 4–5 main characters with abilities and arcs.
- A simple but rule‑based magic system.
- 12‑episode outline with:
  - Introduction arc,
  - Training / tournament or exam arc,
  - Mid‑season twist,
  - Final confrontation and hook for season 2.
- Themes (friendship vs duty, power vs identity) and visual notes (night‑city neon, spell glyph FX).

---

## Integration Notes

- Other skills (e.g. “Character Sheet Generator”, “Worldbuilding Mapper”, “Episode Script Drafting”) can call this skill first to obtain a **base anime concept**, then expand specific parts.
- For iterative use, the skill should:
  - Accept the previous concept as input,
  - Modify or deepen specific sections (e.g. “rewrite the power system to be softer and more mysterious”),
  - Keep continuity unless explicitly told to reboot the story.

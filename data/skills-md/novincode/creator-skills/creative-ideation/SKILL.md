---
name: creative-ideation
description: Generates original ideas, angles and concepts instead of the first obvious ones every other creator would have. Use when the user needs video ideas, content ideas, angles on a topic, a concept, a creative direction, a twist, a fresh take, a series idea, or says their ideas feel generic, done before, or boring, or asks to be more creative.
license: MIT
metadata:
  version: "0.1.0"
  status: alpha
  category: writing
  pack: creator-skills
---

# Creative Ideation

The first ideas anyone has are the ideas everyone has. Creativity, in practice, is generating enough ideas to get past the obvious ones, then having the taste to pick the one that's both surprising and right.

A model's first suggestions are the *average* of everything it has read. That makes the first five ideas the least original ones it will produce. This skill forces it past them.

## The floor

1. **Name the obvious ideas and kill them.** Before generating, list the 5–10 ideas any creator would have on this topic. Those are banned unless a later idea makes one of them fresh.
2. **Volume before judgment.** At least 20 raw ideas before evaluating any.
3. **Specific beats clever.** "History of Boston" is a topic. "The day a syrup tank killed 21 people and the company blamed anarchists" is an idea.
4. **New-ish, not new.** The sweet spot is familiar enough to understand instantly, surprising enough to stop for. [C; Raymond Loewy's "most advanced yet acceptable"]
5. **Every idea has a promise.** If you can't say what the viewer gets, it isn't an idea yet.
6. **Respect the profile.** Ideas must fit the creator's niche, audience and abilities in `.creator/profile.md`, unless the user wants a stretch.

## Generators

Use several. Each one breaks a different habit.

| Generator | How | Example (topic: the molasses flood) |
|---|---|---|
| **Collision** | Combine the topic with an unrelated domain or format | Tell it as a disaster-movie trailer; as a corporate cover-up investigation; as a nature documentary about a predator called Molasses |
| **Inversion** | Flip the obvious angle | Tell it from the company's lawyers' side, who argued anarchists did it |
| **Zoom in** | One person, one object, one minute | The story of the brown paint can |
| **Zoom out** | The bigger system | Every major engineering law was written after a disaster: here are five |
| **Escalation** | The 10× version | We test how fast a wave of molasses actually moves (a real experiment) |
| **Constraint** | Add an absurd rule | Tell the whole story in 15 seconds; tell it without saying "molasses" |
| **Time shift** | Move it in time | What would happen if the same tank burst today? |
| **Format swap** | Same content, different container | A "rate the safety plan" tier list of historical disasters |
| **Personal** | Connect to the viewer's life | The molasses tank in your company (every workplace has one) |
| **Question the premise** | Ask why the obvious version is told | Why does everyone tell this story as a joke? |

## Procedure

1. **Brief.** Topic, creator, audience, platform, constraints (budget, length, skills).
2. **Obvious list.** Write the 5–10 ideas everyone would have. Label them "banned".
3. **Generate 20–50 raw ideas** using at least four generators. One line each. No judging.
4. **Cluster** similar ideas and keep the strongest of each cluster.
5. **Score the survivors** 1–5 on:
   - **Click:** would a stranger in the target audience stop for this?
   - **Fresh:** has it been done to death? (check quickly if search is available)
   - **Deliverable:** can this creator actually make it at this quality?
   - **Ours:** why is this creator the right person to make it?
6. **Develop the top 5–7**: one-line promise, a working title, the strongest image.
7. **Hand the best three to `packaging`** to pressure-test titles and thumbnails before anyone writes a script.

## Output

```markdown
## Ideas: <topic>
Banned (obvious): <list>

| # | Idea (one line) | Generator | Click | Fresh | Deliverable | Ours |
|---|---|---|---|---|---|---|

### Top picks
1. **<working title>**: <promise>. Strongest image: <image>.
```

## Creative taste

Generating is the easy half. Picking needs taste:
- Prefer ideas that make *you* curious. If you already know how it goes, the viewer will too.
- Prefer ideas with a strong single image. If you can't picture the thumbnail, it's probably a topic, not an idea.
- Prefer ideas with conflict built in.
- Kill ideas that only work if you explain them.

## Voice floor

Plain words. Specific nouns. Say it once. Full rules: the `human-writing` skill.

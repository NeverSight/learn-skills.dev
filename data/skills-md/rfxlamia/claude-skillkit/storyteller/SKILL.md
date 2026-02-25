---
name: storyteller
description: >
  Transform abstract/metaphorical narrative into concrete visual story structure.
  
  USE WHEN: Converting poetic/theatrical narrative from diverse-content-gen into 
  scene-by-scene visual breakdowns ready for screenwriter formatting.
  
  PIPELINE POSITION: diverse-content-gen → **storyteller** → screenwriter → production-validator → imagine → arch-v
  
  PRIMARY FUNCTION: Bridge the gap between "altar pribadi" (abstract metaphor) and 
  "woman returns daily to same beach spot" (filmable scene).
  
  OUTPUT: Scene breakdown with concrete visual actions, preserved emotional core, 
  and story logic documentation.
---

# Storyteller Skill

## Overview

This skill transforms metaphorical/theatrical narrative content into concrete, filmable visual stories. It serves as the critical translation layer between poetic writing and production-ready screenplay format.

**The Problem It Solves:**
```
INPUT:  "Aku menjadi laut yang membeku, menunggu pelaut yang tidak kembali"
PROBLEM: What does this LOOK LIKE on screen?
OUTPUT: Woman stands at frozen beach at dawn, staring at horizon where ship 
        disappeared. She places his jacket on the ice. Days pass (montage). 
        She returns. Always returns.
```

**Core Principle:** Preserve emotional truth while making content filmable.

---

## Core Transformation Workflow

### Step 1: Extract Emotional Core
**What does the metaphor FEEL like?**

Read the metaphorical content and identify:
- **Primary Emotion:** The dominant feeling (longing, grief, obsession, hope)
- **Emotional Intensity:** Scale 1-10, how extreme is this feeling?
- **Relationship Dynamic:** Who feels what toward whom?
- **Temporal Context:** Is this present pain, past memory, future fear?

**Example:**
```
Metaphor: "Aku menjadikanmu altar pribadi"
Primary Emotion: Worship/devotion bordering on obsession
Intensity: 9/10 (extreme, unhealthy level)
Dynamic: Speaker → Beloved (one-directional adoration)
Temporal: Present state, ongoing condition
```

### Step 2: Find Visual Equivalent
**What ACTIONS show this emotion?**

Translate abstract emotion into visible behavior using this framework:

| Emotion Type | Visual Translation Strategy |
|--------------|----------------------------|
| **Longing/Waiting** | Character returns to same location repeatedly; keeps object belonging to absent person; checks phone/window/door obsessively |
| **Worship/Devotion** | Ritualistic behaviors (daily routines, shrine-like arrangements); serving without being asked; positioning self lower than object of worship |
| **Loss/Grief** | Empty spaces where person used to be; untouched belongings; inability to change/move on from environment |
| **Obsession** | Collection of items; repetitive actions; deteriorating self-care while maintaining focus on other |
| **Fear of Abandonment** | Checking behaviors; keeping lights on; sleeping in wrong positions; startling at sounds |

**Visual Vocabulary Reference:** [references/visual-vocabulary.md](references/visual-vocabulary.md)

### Step 3: Generate Scene Breakdown
**Build filmable scenes around visual actions**

For each emotional beat in the source material:

1. **Identify Location:** Where would this emotion naturally occur?
2. **Define Action:** What does the character DO to show this emotion?
3. **Select Props/Objects:** What physical items carry symbolic weight?
4. **Establish Time:** When does this happen? (time progression matters)
5. **Document Story Logic:** Why does this visual choice work?

**Scene Template:**
```
SCENE [NUMBER]: [Brief Description]
Location: [Specific place]
Time: [Time of day/progression]
Action: [What character physically does]
Key Visuals: [Important visual elements]
Emotional Beat: [What audience should feel]
Story Logic: [Why this visual choice represents the metaphor]
```

### Step 4: Create Story Logic Map
**Document the metaphor→visual transformation**

For transparency and creative consistency, document:

```
STORY LOGIC MAP
===============
Original Metaphor: "..."
Emotional Core: [extracted emotion]
Visual Translation: [chosen visual representation]
Why It Works: [explanation of connection]
Alternative Considered: [what else could work]
```

---

## Output Format

### Scene Breakdown Structure

```markdown
# Visual Story Breakdown: [Title]

## Source Material Summary
- **Original Concept:** [From diverse-content-gen]
- **Emotional Core:** [Primary emotion identified]
- **Tone:** [Preserved from source]
- **Target Duration:** [5-10 minutes]

## Character(s)
- **[Name]:** [Brief visual description, emotional state]

## Scene-by-Scene Breakdown

### Scene 1: [Title]
**Location:** [Specific, filmable location]
**Time:** [Time of day]
**Duration:** [30-60 seconds estimate]

**Visual Action:**
[Detailed description of what character does - FILMABLE actions only]

**Key Visuals:**
- [Visual element 1]
- [Visual element 2]
- [Visual element 3]

**Emotional Beat:** [What audience feels]

**Story Logic:** [How this scene translates the original metaphor]

---

### Scene 2: [Title]
[Continue same format...]

---

## Story Logic Map
| Original Metaphor | Emotional Core | Visual Translation | Why It Works |
|-------------------|----------------|-------------------|--------------|
| "..." | ... | ... | ... |

## Technical Notes for Screenwriter
- [Any specific notes about pacing, transitions, or visual consistency]
```

---

## Transformation Guidelines

### What Makes a Scene "Filmable"

✅ **FILMABLE:**
- Physical actions (walking, touching, looking, moving objects)
- Observable emotions (tears, shaking, stillness, posture)
- Environmental details (weather, lighting, objects in space)
- Time progression (morning→night, seasons changing)

❌ **NOT FILMABLE:**
- Internal thoughts ("She thinks about him")
- Abstract concepts ("Love fills the room")
- Unvisualizable metaphors ("Her heart is a frozen sea")
- Telling instead of showing ("She is sad")

### Converting Common Metaphorical Patterns

| Metaphor Type | Visual Approach |
|---------------|-----------------|
| **"I am [element]"** (sea, fire, ice) | Show character interacting with that element; use element as setting backdrop; character's behavior mirrors element properties |
| **"You are my [sacred thing]"** (altar, god, sun) | Show ritualistic worship-like behaviors; lighting/composition that elevates the beloved; character positioning that shows devotion |
| **"I am waiting for..."** | Show passage of time; same location revisited; objects accumulated or deteriorating; physical signs of waiting |
| **"When you left..."** | Empty spaces; untouched belongings; paused activities; contrast with "before" flashbacks |

### Detailed Methodology
For step-by-step transformation process with worked examples:
- [references/transformation-methodology.md](references/transformation-methodology.md)

---

## Integration with Pipeline

### Input: diverse-content-gen Output
Expect structured narrative ideas with:
- POV, Setting, Tone, Structure already defined
- "Why This Wins" analysis (emotional hooks identified)
- Metaphorical/theatrical language
- NOT scene-by-scene yet

### Output: Ready for Screenwriter
Provide scene breakdowns with:
- Concrete locations and times
- Physical, filmable actions
- Key visuals for each scene
- Emotional progression documented
- Story logic preserved

**Screenwriter will then:**
- Add proper screenplay formatting (sluglines, etc.)
- Wrap in XML tags for pipeline
- Add technical metadata (duration, characters list)

---

## Quality Checklist

Before outputting scene breakdown, verify:

- [ ] Every scene describes VISIBLE action (not internal thought)
- [ ] Emotional core from source material is preserved
- [ ] Story logic map explains all metaphor→visual translations
- [ ] Scenes follow logical time/space progression
- [ ] Total scene count appropriate for target duration (8-15 for 5-10 min)
- [ ] Key visuals are specific enough for image generation
- [ ] No unexplained jumps in emotion or location
- [ ] Tone consistency maintained throughout

---

## Additional Resources

### Detailed Transformation Process
[references/transformation-methodology.md](references/transformation-methodology.md)

### Visual Vocabulary Reference
[references/visual-vocabulary.md](references/visual-vocabulary.md)

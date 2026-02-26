---
name: humanize
description: >
  Transform AI-to-AI documentation into human-readable prose with personality.
  
  USE WHEN: Converting rigid AI-generated docs (checklists, templates, CAPS LOCK emphasis, 
  perfect structures) into flowing, conversational documentation that feels like a colleague 
  wrote it, not a robot.
  
  PRIMARY TRIGGERS:
  "humanize this doc" → Full transformation workflow
  "make this readable" → Quick readability pass
  "remove AI patterns" → Surgical pattern removal
  "add human touch" → Inject personality without losing precision
  
  INPUT: Markdown files with AI-agent patterns (checklist spam, rigid headers, template overload)
  OUTPUT: Flowing prose with burstiness, analogies, and occasional absurd touches
  
  CORE PRINCIPLE: Total war on AI rigidity. Destroy robotic tone while preserving technical accuracy.
---

# Humanize Docs

## Overview

This skill transforms robotic AI-generated documentation into prose that sounds like an actual human wrote it. Think: destroying checkbox spam, dismantling perfect paragraph structures, and injecting the kind of conversational flow you'd get from a colleague explaining something over coffee.

The approach is **aggressive deformalization** - not just tweaking tone, but fundamentally restructuring how information flows to break AI's predictable patterns.

## When You Need This

**Clear signals you're dealing with AI-generated docs:**
- Checkbox overload: `- [x] Task 1: Do the thing (AC: #1)`
- CAPS LOCK emphasis for CRITICAL IMPORTANT NOTES
- 8+ code templates embedded in a single document  
- Every section has exactly 3 perfectly balanced paragraphs
- Headers like "LLM Developer Guardrails" (literally instructions for robots)
- Phrases: "Certainly, here is...", "It's important to note that...", "Furthermore..."

**Examples from the wild:**
- AI agent documentation (like your Flutter Story example)
- Auto-generated API specs
- Claude Code project scaffolds
- ChatGPT-written technical guides

## Transformation Workflow

### Step 1: Detect AI Patterns

Before transforming, confirm you're actually dealing with AI output. Load the detection checklist:

**[See references/detection-patterns.md for complete list]**

Quick test: Does the doc have 5+ of these?
- Perfect structural symmetry (every section same length)
- Zero sentence length variation (all 15-20 words)
- Checkbox addiction
- Template embedding mania
- Emotional flatness (no "wait, why?" or "honestly...")

If yes → proceed. If no → might already be human-written, be careful.

### Step 2: Apply Core Transformations

Execute transformations in order. Each pattern targets specific AI signatures:

**[See references/core-transformations.md for detailed rules]**

**Quick reference:**

1. **Burstiness Injection** → Mix 5-word punches with 30-word reflections
2. **Structure Dismantling** → Break perfect 3-paragraph blocks, add digressions  
3. **Checkbox Annihilation** → Convert to flowing prose with "anyway, you'll need..."
4. **Template Contextualization** → Replace code dumps with "here's what worked for me..."
5. **Vocabulary Swap** → Kill "utilize/leverage/facilitate", use "use/use/help"

**Critical rule:** Don't apply all transformations everywhere. Humans are inconsistent - some sections stay formal, others get playful. That's the point.

### Step 3: Quality Check

Read the output aloud (or mouth the words). Does it sound like you'd actually say this to someone?

**Red flags the transformation failed:**
- Still too even (every paragraph same vibe)
- No variation in sentence rhythm  
- Feels like a "professional robot" instead of "casual robot"
- You removed personality instead of adding it

**Good signals:**
- Some sentences feel almost too casual (then you toned it back)
- You had to resist adding MORE jokes
- It reads faster than before
- You can hear a specific person's voice

### Step 4: Domain Adjustments (Optional)

Different doc types need different intensity levels:

**High personality OK:**
- READMEs for open source projects
- Internal team documentation  
- Tutorial blog posts
- Onboarding guides

**Moderate personality:**
- API documentation
- User-facing help docs
- Technical specifications

**Gentle touch only:**
- Legal/compliance docs (seriously, be careful)
- Medical/safety documentation
- Financial reports

**[See references/examples-gallery.md for before/after samples]**

## Quick Mode (30 seconds)

If you just need to make something readable without full transformation:

1. Kill the checkboxes → flowing list with "you'll need: X, Y, and Z"
2. Replace one CAPS LOCK section → italics with context
3. Add one burstiness break → throw in a 5-word sentence after a long paragraph
4. Swap 3-5 AI vocabulary words → utilize→use, leverage→use, facilitate→help

Done. Not perfect, but 70% better readability.

## Examples

### Input (AI-generated):
```markdown
## Task 2: Configure Dependencies

**CRITICAL**: The following steps MUST be completed in order.

- [x] Install package A (required for Task 3)
- [x] Verify installation with command X
- [x] Proceed to next task only after confirmation

It is important to note that failure to follow these steps will result in errors.
```

### Output (Humanized):
```markdown
## Setting Up Dependencies

Okay, you'll need to install package A first - and yeah, this actually matters because 
Task 3 depends on it. Run command X to verify it worked.

Once you get the confirmation, you're good to move on. If it errors out, the next step 
will definitely break, so... don't skip this.
```

**Notice:**
- Checkbox death ✅
- "Okay" intro (conversational)
- Sentence length variation (short → long → medium)
- "yeah, this actually matters" (human aside)
- "so... don't skip this" (trailing thought)
- Kept the warning but made it sound real

## Common Mistakes

**Don't:**
- Remove ALL structure (humans still use headers)
- Make everything casual (inconsistency is human)
- Add emojis (that's a different kind of AI spam)
- Force humor (spontaneous > trying hard)
- Ignore domain context (legal docs stay formal)

**Do:**
- Vary your transformation intensity
- Keep some sections more formal for contrast
- Read aloud to check naturalness
- Preserve technical accuracy above all
- Trust your instinct on "too much"

## References

This skill uses reference documentation loaded into context:

### [core-transformations.md](references/core-transformations.md)
The 5 core transformation patterns with detailed rules, examples, and edge cases. 
Load this for complex transformations or when you need to understand WHY a pattern works.

### [detection-patterns.md](references/detection-patterns.md)
Complete AI signature checklist with detection heuristics. Load when you're unsure
if a doc needs transformation or want to explain what makes text feel "AI-generated".

### [examples-gallery.md](references/examples-gallery.md)
Before/after transformation showcase across different document types (technical guides, 
READMEs, API docs). Load for inspiration or to calibrate transformation intensity.

### [advanced-techniques.md](references/advanced-techniques.md) 
Future: Domain-specific adjustments for legal, academic, and specialized documentation.

---

**Philosophy:** AI writes like it's afraid to break rules. Humans write like they're 
explaining something to a friend while occasionally remembering they should probably 
sound professional. Capture that tension.


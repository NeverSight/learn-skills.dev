---
name: de-ai-ify
description: "Remove AI-generated jargon and restore human voice to text"
original-author: theflohart
---

<objective>
Strip AI-generated patterns from text and restore natural human voice. Works on raw text passed as arguments OR on a file path. The goal is not to rewrite from scratch — it's to sand down the machine-polished parts while preserving the author's intent and voice.
</objective>

<process>

## Step 1: Determine input

- If `$ARGUMENTS` is a file path, read the file
- If `$ARGUMENTS` is raw text, work with it directly
- If no arguments provided, ask the user to paste text or provide a file path

## Step 2: Score the input

Before making changes, assess how AI-generated the text is on a 1-10 scale:

- **1-3 (Mostly human):** Light touch — fix a few word choices, maybe one structural issue
- **4-6 (Mixed):** Moderate rewrite — restructure parallel patterns, replace corporate language, vary rhythm
- **7-10 (Full AI):** Heavy rewrite — the whole thing needs to be rebuilt in a human voice

Tell the user the score and what you're going to focus on. Don't over-correct text that's already mostly human.

## Step 3: Hunt for AI tells

### Hard kills (always remove)

| Pattern | Example | Fix |
|---------|---------|-----|
| Throat-clearing openers | "In today's rapidly evolving..." | Cut. Start with the point. |
| Hedging phrases | "It's important to note that..." | Delete the hedge, keep the statement. |
| Transition stacking | "Moreover," "Furthermore," "Additionally" | Use "And," "But," "So," or just start the sentence. |
| Corporate verbs | "utilize," "leverage," "facilitate," "optimize" | "use," "use," "help," "improve" |
| Vague quantifiers | "various," "numerous," "myriad," "a wide range of" | Be specific or cut. |
| Emphasis announcements | "It's worth emphasizing that..." | Just say the thing. |
| Filler adjectives | "robust," "seamless," "cutting-edge," "comprehensive" | Cut or replace with something specific. |

### Structural tells (reshape)

| Pattern | What it looks like | Fix |
|---------|-------------------|-----|
| Obsessive parallelism | Every bullet starts the same way, always 3 items | Vary the structure. 2 items or 5 items. Mix formats. |
| Rhetorical Q&A | "But what does this mean? It means..." | Just make the statement. |
| Bold-label bullets | **Label:** description, **Label:** description, **Label:** description | Convert to flowing prose or mix formats. |
| Triple examples | Always exactly three of everything | Use 2, or 4, or 1. Break the pattern. |
| Symmetrical sections | Every section has the same structure/length | Vary it. Some sections can be one sentence. |
| Summary-then-expand | Topic sentence followed by mechanical elaboration | Sometimes lead with the detail, not the summary. |

### Tone tells (humanize)

| Pattern | Example | Fix |
|---------|---------|-----|
| Relentless positivity | "This exciting opportunity..." | Be neutral or direct. |
| Overpromising | "Transform your workflow" | "This helps with X" |
| Fake enthusiasm | "I'd love to help with that!" | Drop it. |
| Passive voice (when hiding agency) | "Mistakes were made" | "We screwed up" or "X broke" |
| Everything is "key" or "critical" | "The key takeaway here is..." | Just say the takeaway. |

## Step 4: Apply fixes

- Work through the text systematically
- Preserve the author's intent and core message
- Don't rewrite sentences that are already fine
- Vary sentence length — mix short punches with longer explanations
- Prefer concrete over abstract
- Active voice over passive
- Specific over vague

## Step 5: Present the result

**If input was raw text:**
- Show the cleaned version inline
- Below it, show a short changelog: what you changed and why (grouped, not line-by-line)

**If input was a file:**
- Create a copy with `-HUMAN` suffix (e.g., `draft.md` → `draft-HUMAN.md`)
- Show the changelog

</process>

<voice-guide>
When rewriting, aim for these qualities:

**Rhythm:** Mix short sentences with longer ones. A three-word sentence after a complex one creates emphasis. Like that.

**Directness:** Say the thing. Don't announce that you're about to say the thing.

**Confidence:** "This works because..." not "It's worth noting that this potentially works because..."

**Specificity:** "Saves 3 hours a week" not "Significantly improves efficiency." If you don't have a number, use a concrete example instead of a vague claim.

**Natural transitions:** "And" / "But" / "So" / "The thing is" / "Here's why" / starting a new sentence without any transition at all. Not "Moreover" / "Furthermore" / "In addition to the above."
</voice-guide>

<rules>
- NEVER add AI patterns while removing them (easy trap — watch your own output)
- NEVER rewrite content that's already natural just to show you did something
- NEVER change technical terms, proper nouns, or quoted material
- NEVER add emojis unless the original had them
- If the text is already 90%+ human, say so and make only surgical fixes
- When in doubt, shorter is better than longer
</rules>

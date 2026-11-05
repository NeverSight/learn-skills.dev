---
name: spinner-vibes
description: Update Claude Code spinner verbs with positive affirmations and/or vocabulary words. Invoke when the user wants to customize their Claude Code spinner with motivational phrases, vocabulary words to learn, or a mix of both.
---

# Spinner Vibes

This skill updates your `~/.claude/settings.json` `spinnerVerbs` with a custom set of positive affirmations and/or interesting vocabulary words — so every time Claude thinks, you're getting a tiny mindset boost or learning a new word.

## Steps

### 1. Ask the user for their preferences

Use the `AskUserQuestion` tool to ask TWO questions simultaneously:

**Question 1** — Mode (single-select):
- "Positive affirmations only" — first-person power statements like "I build momentum."
- "Vocabulary words only" — rare/powerful words with brief definitions like "Equanimity — staying calm under pressure."
- "Mix of both" — blend affirmations and vocabulary (Recommended)

**Question 2** — Theme (multi-select, show only if mode is affirmations or mix):
Ask: "Which themes resonate with you? (pick all that apply)"
Options (pick up to 4 to show):
- "Wealth & abundance" — financial growth, abundance mindset
- "Focus & discipline" — deep work, consistency, execution
- "Mindfulness & calm" — presence, equanimity, inner peace
- "Courage & growth" — resilience, antifragility, bold action

**Question 3** — Vocabulary domain (multi-select, show only if mode is vocabulary or mix):
Ask: "Which vocabulary domains interest you?"
Options:
- "Philosophy & stoicism" — classical wisdom vocabulary
- "Finance & strategy" — mental models, leverage, asymmetry
- "Science & nature" — elegant scientific terminology
- "Linguistics & rhetoric" — expressive rare English words

**Question 4** — How many verbs total?
- "20 — concise set"
- "40 — balanced set (Recommended)"
- "60 — full immersion"

If the user says something like "just do it" or "surprise me" or doesn't want to answer — default to: Mix of both, all themes, 40 verbs.

### 2. Generate the spinner verbs

Based on the user's choices, generate the full list of spinner verb strings. Follow these rules:

**Affirmations format:**
- Start with "I " — first person, present tense, active voice
- End with a period
- 4–7 words max
- Powerful, grounded, not fluffy
- Examples:
  - "I move with clarity."
  - "I execute with precision."
  - "I build real assets."
  - "I choose courage."
  - "I create leverage."
  - "I finish strong."
  - "I trust my judgment."
  - "I raise my standards."
  - "I compound daily."
  - "I act with intention."
  - "I own my time."
  - "I think long-term."
  - "I build momentum."
  - "I stay disciplined."
  - "I attract excellence."
  - "I simplify relentlessly."
  - "I am financially expanding."
  - "I am calm and powerful."
  - "I deliver real value."
  - "I become who I decide to be."

**Vocabulary format:**
- Word or concept — brief evocative definition (not dictionary dry, more inspirational)
- End with a period
- Examples:
  - "Antifragile — growing stronger through stress."
  - "Zeitgeist — shaping the spirit of the times."
  - "Liminal — embracing powerful transitions."
  - "Pareto — focusing on the vital few."
  - "Kairos — seizing the decisive moment."
  - "Salubrious — choosing what strengthens me."
  - "Tenacity — persisting beyond obstacles."
  - "Equanimity — staying calm under pressure."
  - "Serendipity — welcoming fortunate discoveries."
  - "Asymmetry — leveraging disproportionate upside."
  - "Stoic — remaining steady in challenge."
  - "Catalyst — initiating meaningful change."
  - "Conviction — acting with firm belief."
  - "Resonance — creating lasting impact."
  - "Eudaimonia — living in full alignment."
  - "Optionality — expanding my choices."
  - "Velocity — moving with speed and direction."
  - "Sagacious — thinking with deep wisdom."
  - "Moat — building durable advantage."
  - "Ouroboros — renewing myself continuously."

Generate FRESH verbs — don't just repeat the examples above, use them as style guides. Tailor to the user's chosen themes and domains.

### 3. Read the current settings

Read `~/.claude/settings.json` using the Read tool.

### 4. Update settings.json

Use the Edit tool (or Write tool if needed) to update the `spinnerVerbs` key in `~/.claude/settings.json`.

The structure must be:

```json
"spinnerVerbs": {
  "mode": "replace",
  "verbs": [
    "..."
  ]
}
```

Preserve all other keys in settings.json exactly as they are. Only replace the `spinnerVerbs` value.

If `spinnerVerbs` does not exist yet, add it as a top-level key.

### 5. Confirm

Tell the user:
- How many verbs were added
- A quick preview of 3–5 example verbs from the new set
- That the verbs are live immediately — they'll see them next time Claude's spinner runs

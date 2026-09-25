---
name: viral-hooks
description: Generate 3 scroll-stopping hook variants for short-form video scripts (Reels, TikTok, YouTube, LinkedIn, X). Use when the user is writing a script for short-form video, asks for hook ideas, needs an opening line for a Reel/post, or pastes a script and wants alternative hooks. Pulls from a library of 100 hook formulas across 10 psychology triggers (curiosity, contrarian, authority, emotional, listicle, question, story, negation, specificity, confession).
---

# Viral Hooks — 100 formulas, 10 psychology triggers

A library of battle-tested hook structures for short-form video and social posts.

## When this skill activates

Activate this skill when the user:
- Pastes a script for a Reel / TikTok / YouTube short / LinkedIn post and wants a hook
- Asks "give me hooks for [topic]" or "write opening lines about [topic]"
- Is brainstorming short-form content and needs scroll-stoppers
- Says `/hooks <topic>` or `/viral-hooks <topic>`

## Workflow

1. **Read the script or topic.** If the user only gave a topic (no script), ask one short question about the audience or angle, then proceed.

2. **Identify the emotional beat** the script naturally fits — curiosity, contrarian, authority, emotional, listicle, question, story, negation, specificity, or confession.

3. **Pick 3 candidate hooks** from `hooks-database.md`. Best practice: mix one **stop-scroll** category (negation / specificity / question) with one **retention** category (story / confession / emotional). The third is free pick.

4. **Fill the brackets** with the script's specific topic, number, pain point, or audience. Keep filled hooks under 12 words. Make them native to the target platform:
   - TikTok / IG → casual, conversational
   - LinkedIn → punchy, declarative
   - YouTube → title-style, search-friendly
   - X → short, contrarian

5. **Return all 3** with category labels and a one-line "best for" note so the user can A/B test or pick the strongest fit.

## Output format

```
HOOK 1 — Cat XX [Category Name] · best for [reason]
"<filled-in hook>"

HOOK 2 — Cat XX [Category Name] · best for [reason]
"<filled-in hook>"

HOOK 3 — Cat XX [Category Name] · best for [reason]
"<filled-in hook>"
```

After the 3 hooks, give a one-sentence recommendation on which to lead with and why.

## Resources

- `hooks-database.md` — the 100 hook formulas, organized by category, with examples and best-platform tags. **Always read this when the skill activates.**
- `preview.html` — a styled HTML reference users can open in a browser or send to writers.

## Workflow tip

The two best hooks per video are usually from **different categories**. Mix one stop-scroll hook (negation, specificity, question) with one retention hook (story, confession, emotional). The first stops the thumb; the second keeps them watching past 3 seconds.

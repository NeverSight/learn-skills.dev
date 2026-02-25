---
name: content-humanizer
description: >
  Makes AI-generated prose sound natural and human-written. Covers tone analysis, sentence variation, voice consistency, readability improvement, and AI-typical pattern removal including hedging, filler words, and over-qualification.

  Use when improving blog posts, marketing copy, or narrative documentation. Use for tone consistency, readability, sentence rhythm, and removing AI-typical writing patterns.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Content Humanizer

## Overview

Content humanizer transforms AI-generated prose into writing that reads as natural and intentional. It covers sentence rhythm, tone calibration, audience adaptation, and systematic removal of patterns that signal machine authorship. Applies to blog posts, marketing copy, email campaigns, narrative documentation, and any long-form prose.

**When to use:** Polishing AI-drafted blog posts, adapting marketing copy for a specific brand voice, improving readability of narrative documentation, rewriting content that feels robotic or formulaic.

**When NOT to use:** On code or technical specifications where precision matters more than voice. On content that was already human-written and reads naturally. For removing AI artifacts from code comments or READMEs (use the `de-slopify` skill instead).

## Quick Reference

| Pattern             | Technique             | Key Points                                                        |
| ------------------- | --------------------- | ----------------------------------------------------------------- |
| Flat rhythm         | Sentence variation    | Mix short (5-word) and long (20+ word) sentences                  |
| Passive voice       | Active rewriting      | Subject performs the action; aim for 80-90% active                |
| Abstract claims     | Concrete language     | Replace "significant improvement" with specific numbers           |
| Hedging phrases     | Direct assertion      | Delete "it's worth noting" and state the fact                     |
| Filler vocabulary   | Plain language        | "utilize" becomes "use", "leverage" becomes "use"                 |
| Over-qualification  | Confident tone        | Remove unnecessary caveats and balanced-to-a-fault phrasing       |
| List addiction      | Prose conversion      | Convert mechanical bullet lists into flowing paragraphs           |
| Generic transitions | Contextual connectors | Replace "furthermore" and "moreover" with idea-specific links     |
| Uniform paragraphs  | Varied structure      | Break predictable paragraph lengths and opening patterns          |
| Missing voice       | Brand calibration     | Define audience, formality level, and personality before editing  |
| No E-E-A-T signals  | Experience injection  | Add first-person anecdotes, specific data, authoritative sources  |
| Low burstiness      | Length variation      | Alternate 3-word and 25-word sentences to break uniformity        |
| Low perplexity      | Word unpredictability | Replace formulaic phrases with domain-specific, concrete language |

## Common Mistakes

| Mistake                                      | Correct Pattern                                                     |
| -------------------------------------------- | ------------------------------------------------------------------- |
| Replacing AI words with a thesaurus          | Rewrite the sentence; synonym swaps create awkward phrasing         |
| Removing all structure to sound casual       | Keep headings and organization; rewrite prose within the structure  |
| Over-correcting into choppy fragments        | Read aloud after editing; recombine sentences that lost flow        |
| Editing without defining target voice        | Set persona, audience, and formality level before starting          |
| Treating humanization as a single pass       | Use multiple passes: structure, then voice, then polish             |
| Making every sentence short and punchy       | Vary length deliberately; monotone short sentences feel robotic too |
| Adding personality through exclamation marks | Voice comes from word choice and rhythm, not punctuation            |
| Ignoring paragraph-level patterns            | AI writes uniform paragraphs; vary length and opening structure     |

## Delegation

- **Scan a repository for prose files that need humanization**: Use `Explore` agent
- **Rewrite an entire blog or documentation site**: Use `Task` agent
- **Define a brand voice guide and editorial standards**: Use `Plan` agent

> If the `de-slopify` skill is available, delegate code comment cleanup and technical writing artifact removal to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill de-slopify`

## References

- [Writing patterns: sentence variation, active voice, concrete language, and rhythm](references/writing-patterns.md)
- [Tone and voice: brand consistency, audience adaptation, and formality levels](references/tone-and-voice.md)
- [AI pattern removal: detecting and rewriting common AI tells](references/ai-pattern-removal.md)
- [Advanced patterns: E-E-A-T signals, burstiness, perplexity variation, and structural rhythm](references/advanced-patterns.md)

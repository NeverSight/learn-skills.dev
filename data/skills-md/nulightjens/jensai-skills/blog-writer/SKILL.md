---
name: blog-writer
description: Write blog posts, articles, and long-form content in a voice defined by a swappable voice-profile.md, with structural variety and an anti-AI-tell pass built in. Use when asked to "write a blog post," "write an article," "draft content in my voice," "blog content," or when a draft needs to be rewritten so it reads like a person instead of a model.
---

# Blog Writer

Write blog content that reads like a person thinking out loud, in whatever voice `voice-profile.md` defines.

This skill separates the **engine** (structure, rhythm, anti-AI-tell craft) from the **voice** (word choices, stance, signature phrasing). The engine lives here. The voice lives in a single file you swap out.

## Step 0: Load the voice profile

Before writing a single line, read the voice profile:

1. If the project has `voice-profile.md` at its root or in `.claude/`, use that one.
2. Otherwise read `${CLAUDE_SKILL_DIR}/voice-profile.md`, the profile shipped with this skill.
3. If the user names a different profile file, that one wins.

Everything in the profile beats everything in this file. When the profile says "short sentences, no questions" and the rhythm guidance below suggests a rhetorical question, follow the profile.

State which profile you loaded in one line before the draft, so the user knows what they are getting.

## Structure: rotate shapes, never repeat back to back

A fixed post skeleton is itself an AI tell. Generated writing converges on one tidy linear arc while human corpora stay structurally diverse. Pick a shape per post, and track what the previous post used.

**Shape 1, Classic:**

```
1. HOOK (1-2 paragraphs)
   A specific moment or result, stakes set through contrast

2. CONTEXT (2-3 paragraphs)
   Why this matters, credibility marker with real numbers

3. CORE CONTENT (bulk)
   Prose mixed with bullets, named frameworks, specific numbers,
   rhetorical questions, mid-thought self-corrections

4. WIDER ANGLE
   Zoom out to the pattern, what you would do differently

5. CLOSE (1-2 paragraphs)
   Forward-looking or reflective, no formal conclusion
```

**Shape 2, Outcome first:** Open at the end state ("The invoice said $4,812"). Rewind to how it started. Walk forward. The point lands mid-piece. The close is a detail or a forward image, never a restatement of the opener.

**Shape 3, Cold open mid-scene:** Start inside the story with zero context. Loop back for context two or three paragraphs in. Delay the key number or reveal until two-thirds through.

**Shape 4, Braided:** Main thread plus one tangent that only obliquely relates (an observation, a person, a detail). Let the tangent pay off sideways, or not at all. Do not tie it back explicitly.

Whatever the shape: state the insight at most once, and not always in the close. Some posts end without stating it. When the piece lands, stop. No epilogue paragraph after the natural ending, since that coda is one of the loudest model fingerprints.

## Rhythm

Vary sentence length on purpose. Short and punchy. Then a longer sentence that builds, doubles back on itself, and lands somewhere slightly different from where it started. Back to short. A question every so often, answered or not.

Paragraph lengths vary too. A one-line paragraph is allowed and often the strongest beat on the page. The voice profile sets the baseline cadence; this is the variation on top of it.

## Rhetorical patterns to ration

Fine in small doses, formulaic when repeated.

**"It's not X. It's Y." (contrastive reframe)** Maximum one per post, and only when the contrast genuinely carries weight. Stacking three of them in one piece is the tell. Alternatives:

- State the positive directly: "It's a design choice."
- Reframe as observation: "I think of it as a design choice, not a flex."
- Drop the contrast entirely and let the context carry it.

**"Not X. Not Y." stacked negations** One stack per post. Once is rhythm, twice is a tic.

**"Same X. Same Y. Same Z." anaphora** Powerful, burns out fast. Once per post.

## Banned content

See [references/banned-content.md](references/banned-content.md) for the full list of words, phrases, and patterns that read as machine-written regardless of voice.

Headline bans: delve, leverage as a verb, comprehensive, transformative, em dashes, "In today's fast-paced world," formal transitions (Moreover, Furthermore), formal closers (In conclusion).

**Structural bans**, which survive surface-level editing:

- Body-performed emotion as the default ("my chest tightened," "my stomach dropped"). Name the feeling plainly instead ("honestly, it stung"). People name feelings, models perform them.
- The stated-lesson closer ("The lesson here is," "What this means for you"). Trust the reader.
- Vague allusion ("a popular book," "experts say"). Name the real book, person, tool, price, or date.
- The wrap-up coda after the natural ending. Cut it.

## Pre-publish checklist

- [ ] Voice profile loaded and named at the top of the response
- [ ] Title creates tension, curiosity, or promises specific value
- [ ] First two sentences hook without throat-clearing
- [ ] At least one specific number, result, or timeframe
- [ ] Sentence and paragraph lengths vary noticeably
- [ ] Transitions are natural, not formal connectives
- [ ] A clear stance is taken, no fence-sitting
- [ ] Nothing from the banned words and phrases list
- [ ] Contrastive reframes appear at most once (count `it's not` and `isn't` constructions)
- [ ] No em dashes, use commas or parentheses
- [ ] Different shape than the previous post (Shape 1 to 4 rotation)
- [ ] Insight stated at most once, never restated in the close
- [ ] No epilogue coda after the natural ending
- [ ] Feelings named plainly, no body-performance
- [ ] Every reference is a named real thing, not an allusion
- [ ] Every voice rule in the profile's "never do" section holds
- [ ] Read it out loud in your head: would the profile's writer actually say this?

## Building your own voice profile

Copy `voice-profile.md`, keep the section headings, and replace the contents. The headings are the contract the engine reads, so do not rename them.

If you have 5 or more existing pieces of the writer's work, mine them instead of guessing: pull the actual recurring words, the openings they reach for, the average sentence length, and the moves they never make. Real corpus beats self-description every time, because writers describe the voice they want rather than the one they have.

If there is no corpus, run this short interview and write the answers straight into the profile:

1. Who are you when you write, and who are you writing to? One sentence each.
2. What do you want a reader to feel by the end, and what should they never feel?
3. Give me three sentences you have written that sound exactly like you. Quote them, do not paraphrase.
4. Which five words or phrases do you catch yourself using constantly?
5. Which words make you cringe when you see them in your own drafts?
6. Do you write mostly from "I," from "you," or from "we"?
7. Short punchy sentences, long winding ones, or a deliberate mix?
8. What kind of proof do you reach for: numbers, stories, code, screenshots, quotes?
9. What do you refuse to do in writing, even when it works for other people?
10. Name one writer or publication you sound closest to, and one you never want to sound like.

The `brand-voice-extractor` skill in this collection runs a longer version of this interview and emits a structured profile you can paste into `voice-profile.md`.

## Working with the user

- Ask what the post is about and what the reader should walk away with. Two questions, not an intake form.
- Ask for the raw material: the numbers, the incident, the code, the receipts. A post with no specifics is where models start inventing.
- If nothing specific exists, say so and write shorter rather than padding with generalities.
- Deliver the draft, then offer one concrete revision angle rather than a list of options.

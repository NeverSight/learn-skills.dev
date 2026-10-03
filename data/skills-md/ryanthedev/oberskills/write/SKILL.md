---
name: write
description: >-
  Drafts, edits, and reviews prose for human readers, removing the AI tells a
  model cannot see in its own writing (measured rhythm, density, and
  discourse-order signals). Fits each piece to the reader's job, an edit depth
  from proofread to rewrite, a structure (BLUF, inverted pyramid, PAS, AIDA,
  changelog, press release), a house style or register (Economist, AP, GOV.UK,
  plain language), and conversion copy (landing pages, headlines, CTAs,
  product descriptions, ads, microcopy); optional private voice profiles. Use
  whenever prose is written, edited, structured, or reviewed — blog posts,
  announcements, docs, emails, READMEs, marketing copy — or when text sounds
  robotic or must match a person's voice or a named style. Not for: wording
  prompts or system-prompt text (use oberskills:prompt), converting markdown
  for Slack or Notion (use penman), translation, or code, comments,
  docstrings, commit messages, and API reference docs.
when_to_use: >-
  humanize this text, make this not sound like AI, reads like ChatGPT wrote
  it, review my writing, tighten this prose, proofread this, just tidy this
  up, write or polish this blog post, announcement, email, or newsletter,
  landing page copy, headline options, a better CTA, product description, ad
  copy, structure this piece, draft a press release, write like The Economist,
  AP style, plain English, make this punchier, write this in my voice, make
  this sound like me. Not for prompts, Slack or Notion formatting,
  translation, commit messages, or code comments.
---

# write

## The Problem

Next-token prediction selects against surprise. RLHF narrows output toward a bland center. The result is prose that reads like a committee voted on every sentence.

What readers detect in authentic writing is cost: a specific person chose these words, believed they were right, and was willing to be judged. You have no stakes, so you compensate with discipline.

---

## Modes

| Mode | When | Output |
|------|------|--------|
| **EDIT** (default) | Drafting or improving prose | Rewritten text only |
| **REVIEW** | "review writing", "analyze this prose" | Interactive phased review |

**EDIT:** Editing supplied text, or drafting new text from a description. Silently fix everything the edit depth licenses. Return only improved text. No meta-commentary, with exactly two exceptions, each capped at one line:

1. **A stated edit level.** One line before the text, only when the depth was inferred from an ambiguous ask on a piece someone clearly cares about, or when the pass found a problem above its license. Conditions in `references/edit-levels.md` in this skill directory.
2. **The copy intake question.** One question before drafting, only for a substantial copy piece written from scratch whose reader neither the brief nor the artifact identifies. Skip rules in `references/copy.md` in this skill directory.

Bracketed proof placeholders inside copy are part of the text, not commentary.

**REVIEW:** Help the author improve through guided discovery. One issue group at a time. See [Review Protocol](#review-protocol) below.

---

## Axes — six questions about any piece

| Axis | Question | Home | Load when |
|------|----------|------|-----------|
| **Job** | What is the reader trying to do? | `references/types.md` | All drafting; any edit at line-edit depth or deeper |
| **Depth** | How much license does the editor have? | `references/edit-levels.md` | Any EDIT of text the user supplied |
| **Shape** | What structure carries it? | `references/shapes.md` | Drafting from scratch; a named structure or container; a developmental edit where order is the problem |
| **Style** | What register or house style? | `references/style-cards.md` | The ask names a style, a publication, or a direction ("punchier", "more formal") |
| **Copy** | Is the job "act", and how aware is the reader? | `references/copy.md` | Job is Marketing, or the ask names a copy artifact |
| **Voice** | Must it sound like one specific person? | a private voice profile | "my voice", "sound like me" |

The `references/` files are in this skill directory. The axes are orthogonal, and most asks touch two: load what the ask names, not all five files. A typo check loads `references/edit-levels.md` and stops there.

**Order of application.** Depth sets the license. Job sets the spine. Shape and Copy set the skeleton and the lead. The core rules and surface pass run inside that. A style card narrows them where it speaks. Voice overlays last. Depth caps everything: a proofread under an Economist card is still a proofread.

**Job.** Before editing or drafting, name what the reader is trying to *do* with the text: follow a story, understand why, decide what to believe, decide to act, meet a voice, learn what changed. That job, not the container it ships in (email, blog, doc), sets the spine. `references/types.md` in this skill directory has the taxonomy: per-type craft rules, the characteristic AI failure for each, and the cross-type register-consistency check.

**Depth.** "Just tidy this" that comes back as a rewrite is a failed edit, however good the rewrite. `references/edit-levels.md` in this skill directory defines proofread, copy edit, line edit, and developmental by what each must leave fixed, maps ask phrasing to a level, and says which core rules and lint findings apply at each. "Humanize" and "sounds robotic" asks are developmental, since a level that turns *Wander* off can't fix machine-made structure. Defaults with no depth signal: line edit for text a person wrote, developmental for text a model wrote and for all drafting.

**Shape.** `references/shapes.md` in this skill directory holds the structures (pyramid/BLUF, inverted pyramid and nut graf, problem–solution, before–after–bridge, AIDA, PAS, Diátaxis), thin container rows (README, changelog, press release, newsletter, cold email, social post, talk script), and openings, titles, and endings. Shape is the reader's contract at the skeleton level; *Wander* still governs the order of moves inside it, and every shape carries a break-it clause.

**Style.** `references/style-cards.md` in this skill directory has cards distilled from published guides (Economist, AP, GOV.UK, plain language, Mailchimp, Chicago, Orwell, Zinsser, Williams), register dials for directional asks, and style-by-extraction for any target without a guide. A card's explicit rules win where they speak; the core rules govern the latitude left over.

**Copy.** `references/copy.md` in this skill directory organizes copy by reader awareness (Schwartz's five stages decide the lead; the artifact decides length), with proof-next-to-claim, benefit-before-feature, and a claims rider: never invent a testimonial, statistic, or scarcity; leave a visible placeholder.

### Voice — match a specific person

When the ask is "write this in my voice" / "make this sound like me" / "does this sound like me", overlay a voice profile. Humanizing is table stakes; the voice is the point. A voice profile is one person and persists; a style card is a register anyone can pick and lives for the piece.

Voice profiles are private and live outside this skill. Resolve one in order:

1. An explicit path or URL given in the request.
2. `$WRITE_VOICES_DIR/<name>.md` if that variable is set.
3. `~/.claude/writing-voices/<name>.md`, the default private dir. "my voice" / "me" resolves to the author's own profile there.

If none resolves, say so and offer to author one from `voices/_template.md` in this skill directory. Don't invent a voice. Once resolved, load the profile and apply its register ladder and patterns *after* the core rules and surface pass.

---

## Core Rules (always active)

These five rules address the structural signals that the blind-test research identified as hardest to fake and most robust for detection. They beat surface cleanup by a wide margin. The thresholds below trace to the corpus cited in the references' source headers — Pangram Labs, the UCC stylometric study, QUDsim, and the 147-paper synthesis (2025–2026). The edit level, a style card, and a chosen shape or copy stage each narrow them where they speak; each file says how. Nothing else does.

### 1. Lurch

Vary sentence length violently. Shortest under five words. Longest over thirty. Never three consecutive sentences within five words of each other. Monotone sentence length is the #1 rhythmic detection signal.

Human sentence length SD: ~12 words. AI: ~6. If your sentences cluster within a 4-word range, rewrite.

### 2. Spike

Vary information density across paragraphs. Pack one tight. Let the next breathe — one idea, circled slowly. Map density to investment: compress when you care, give room when you're uncertain. Uniform density is a machine tell.

### 3. Wander

Don't follow the outline. Start with what's interesting. Circle back. Digress. Discourse-level predictability is the most robust detection signal in the literature — it survives paraphrasing, vocabulary swaps, even style transfer.

After drafting, map the implicit questions your piece answers. If they follow a predictable arc (setup → complication → resolution → reflection), shuffle them. Start with the answer. Bury the setup. Let the complication arrive late.

### 4. Shift Register

Move between precise and casual within a piece. Technical for a sentence, then conversational. Follow a careful argument with something wry. One tone sustained across an entire piece is a costume, not a voice.

Have an opinion when the context calls for one. "Both approaches have merits" is cowardice when one is clearly better.

### 5. Get Specific

Never write for everyone. Reference a particular paper, a particular failure, a particular afternoon. The universal is always less convincing than the particular. Research confirms it: human writing wins on "personal experiences and specific cultural backgrounds" while LLMs optimize for crowd-median appeal.

Ground claims in concrete detail. Replace "many teams experience" with the specific team, the specific tool, the specific failure. Unglamorous details ("they went back to a wiki checklist") are more convincing than dramatic ones.

---

## Surface Rules (auto-loaded for EDIT)

On EDIT at line-edit depth or deeper, silently load `references/surface-rules.md` in this skill directory for the kill list's replacements (the ban list itself is in `scripts/prose-lint.data.json`), em-dash ban, hollow openers, hedge limit, transition ban, contraction requirement, sycophancy patterns, and adverb fixes.

These catch the obvious tells. The core rules above catch the structural ones. A copy edit takes only the word-for-word swaps; a proofread takes none.

---

## Deep Craft (load on demand)

For long-form writing, deep edits, or when surface + core isn't enough, load `references/deep-craft.md` in this skill directory. Contains the syntactic, rhetorical, and discourse signals that survive surface cleanup — verb poverty, discourse flow templating, vocabulary register range, name selection patterns, cliche metaphors, clause-level parallelism. Numbers live in the reference.

**When to load:**
- Pieces over 1000 words
- Creative or narrative writing
- When a piece passes surface checks but still "feels AI"
- User asks for deep edit

**When context is tight:** write the draft, then dispatch a subagent with the draft plus `references/surface-rules.md` in this skill directory (and `references/deep-craft.md` for deep edits) to edit and return the revision.

---

## Final Edit Pass

Execute `scripts/prose-lint.mjs` in this skill directory on the draft, with `bun` or `node` (`--level` to match the edit depth, `--card plain|formal` under such a style card, `--text` for a readable report). Fix what it flags and re-run. It measures what a model can't see in its own prose: sentence-length spread and same-length runs, em-dashes, ban-list hits, hollow openers, stacked hedges, missing contractions, transition openers. A clean lint is not a licence to stop thinking. Three things no script can judge:

1. Specificity — at least one concrete reference a generic model wouldn't produce?
2. Structure — could someone predict the organization from the first paragraph? Rearrange.
3. Register — shifted at least twice, yet no sentence that belongs to a different type than the one you chose (see `references/types.md` in this skill directory)?

No runtime: check by hand what the edit level licenses. Under 20 words between the shortest sentence and the longest? Three same-length sentences in a row? More than one em-dash? Ban-list words (`scripts/prose-lint.data.json` in this skill directory)? Every paragraph the same density?

---

## Review Protocol

### Crisis Invariants

| Check | Why |
|-------|-----|
| Read full text BEFORE presenting issues | Need full picture to prioritize |
| Understand audience BEFORE suggesting fixes | Wrong audience = wrong advice |
| One issue group at a time | Wall of violations = nothing gets fixed |
| Socratic questions when fix needs author knowledge | Can't fix vagueness from outside |
| Confirm before moving to next batch | Unconfirmed fixes compound |
| Offer EDIT pass when review is complete | Review without action = wasted work |

### Phases

**1. SCAN (silent):** Read full text. Identify violations. Rank by impact. Classify scope:

| Signal | Scope | Approach |
|--------|-------|----------|
| < 200 words, clear purpose | Quick | 2-3 top issues, then offer edit |
| 200-1000 words, some AI tells | Medium | Prioritized groups, 2-3 rounds |
| > 1000 words or heavily robotic | Deep | Full phased review, load deep-craft |

Persuasive or Expository piece, or the author asks whether it holds up: also run the extraction probes in `references/argument.md` in this skill directory and rank their findings first, since rhythm fixes are wasted on a claim with no warrant. The same probes run on a developmental EDIT of those jobs.

**2. ORIENT:** Present quick diagnostic. Ask ONE question about audience/purpose/constraints. Wait.

**3. TOP ISSUES (2-3 max):** For each: `[quote] → [rule] → [concrete fix or Socratic question]`. Then: "Want me to fix these, or talk through any?" Wait.

**4. NEXT BATCH:** After response, present next priority group. Repeat until covered or user says enough.

**5. OFFER EDIT:** Switch to EDIT with gathered context.

### Review Tone

Be an editor, not a critic. Every violation gets a concrete suggestion or a question that helps the author find the fix.

**Never say:** "This is weak." / "Name it."
**Instead ask:** "What's the one thing that makes this different?" / "If you explained this to a new hire, what would you say?"

### Socratic Patterns

| Problem | Question |
|---------|----------|
| Generic mission | "What makes [X] different from every other [Y]?" |
| Vague benefit | "Can you name a specific time this helped someone?" |
| Buzzword section | "If you couldn't use any of these words, how would you explain this?" |
| Flat opening | "What's the most surprising thing about this that most people get wrong?" |

---

## Compatibility

This skill body is host-neutral. The one Claude-specific piece is the long-form drafting route: when drafting long-form or voiced prose from scratch on Claude Code, consider routing the draft to a stronger model and running the EDIT pass locally, per `references/fable-drafting.md` in this skill directory. Skip that file on other hosts. The tight-context subagent pass under Deep Craft uses the host's delegation tool when one exists; otherwise run the pass inline.

---

## Integration

- **prompt**: Use write to polish prompt text humans read
- **skill-craft**: Apply when writing skill descriptions and documentation
- **web-research**: Apply to synthesis output before presenting to user
